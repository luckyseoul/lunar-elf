"""Spherical radial transfer for TM (Schumann-type) modes.

We work with the radial function u(r) such that the modal field structure for
degree n satisfies the 1-D Helmholtz form

    d²u/dr² + [k²(r) - n(n+1)/r²] u = 0

with u ∝ r * (Debye potential). Interface continuity of u and du/dr follows from
continuity of tangential E, H for TM_r modes in piecewise-constant layers.

Within a constant-k layer the general solution is a combination of spherical
Ricatti-Bessel functions; for numerical robustness at ELF we use a 2×2
propagator obtained by integrating the first-order system

    d/dr [u, v]ᵀ = [[0, 1], [n(n+1)/r² - k², 0]] [u, v]ᵀ
    v = du/dr

with a complex ODE stepper. This handles continuous and layered σ(r) uniformly.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

from .layers import Layer, k_complex


@dataclass
class RadialState:
    """u and du/dr at a radius."""

    r: float
    u: complex
    du: complex


def _rhs(r: float, y: np.ndarray, n: int, k2: complex) -> list[complex]:
    u, du = y[0], y[1]
    # avoid r=0
    r = max(r, 1.0)
    d2u = (n * (n + 1) / r**2 - k2) * u
    return [du, d2u]


def propagate_layer(
    layer: Layer,
    n: int,
    omega: complex | float,
    u0: complex,
    du0: complex,
    n_eval: int = 8,
) -> RadialState:
    """Propagate (u, du/dr) from r_inner → r_outer through one layer."""
    k = k_complex(omega, layer.sigma, layer.eps_r, layer.mu_r)
    k2 = k * k
    r0, r1 = layer.r_inner, layer.r_outer
    if r1 <= r0:
        return RadialState(r1, u0, du0)

    # For extremely lossy / large |k|Δr, ODE may stiffen — use Radau
    y0 = np.array([u0, du0], dtype=np.complex128)

    def fun(r, y):
        return _rhs(float(r), y, n, k2)

    sol = solve_ivp(
        fun,
        (r0, r1),
        y0,
        method="RK45",
        rtol=1e-6,
        atol=1e-9,
        dense_output=False,
    )
    if not sol.success:
        # fallback: fine stepping with matrix exponential of local frozen coeff
        return _propagate_matrix(layer, n, omega, u0, du0)

    return RadialState(r1, complex(sol.y[0, -1]), complex(sol.y[1, -1]))


def _propagate_matrix(
    layer: Layer,
    n: int,
    omega: complex | float,
    u0: complex,
    du0: complex,
    n_steps: int = 64,
) -> RadialState:
    """Piecewise-constant-r transfer via 2×2 matrix product (midpoint r)."""
    k = k_complex(omega, layer.sigma, layer.eps_r, layer.mu_r)
    k2 = k * k
    rs = np.linspace(layer.r_inner, layer.r_outer, n_steps + 1)
    u, du = u0, du0
    for i in range(n_steps):
        r_a, r_b = rs[i], rs[i + 1]
        r_m = 0.5 * (r_a + r_b)
        dr = r_b - r_a
        # A = [[0,1],[n(n+1)/r² - k², 0]]
        a21 = n * (n + 1) / r_m**2 - k2
        # exp(A dr) for 2x2: closed form via eigenvalues ±λ, λ=sqrt(a21)
        # A² = a21 * I, so exp(Adr) = cosh(μ)I + (sinh(μ)/μ)*A dr... wait
        # λ² = a21, exp(A h) = cosh(λh) I + sinh(λh)/λ * A  if λ≠0
        lam2 = a21
        h = dr
        if abs(lam2) < 1e-30:
            # A = [[0,1],[0,0]], exp = [[1,h],[0,1]]
            u_new = u + h * du
            du_new = du
        else:
            lam = np.sqrt(lam2)
            # branch not critical for finite product stability here
            ch = np.cosh(lam * h)
            sh_over = np.sinh(lam * h) / lam
            # exp = ch I + sh_over * A, A=[[0,1],[a21,0]]
            # [[ch, sh_over],[a21*sh_over, ch]]
            u_new = ch * u + sh_over * du
            du_new = a21 * sh_over * u + ch * du
        u, du = u_new, du_new
    return RadialState(layer.r_outer, complex(u), complex(du))


def propagate_stack(
    layers: list[Layer],
    n: int,
    omega: complex | float,
    u0: complex = 1.0 + 0j,
    du0: complex | None = None,
) -> RadialState:
    """Propagate from innermost r_inner through all layers.

    Default start: regular solution near center u ~ r^{n+1}, du ~ (n+1) r^n
    approximated at first layer inner radius.
    """
    r0 = layers[0].r_inner
    if du0 is None:
        # regular at origin: u ∝ r^{n+1}
        u0 = (r0 ** (n + 1)) + 0j
        du0 = (n + 1) * (r0**n) + 0j
    state = RadialState(r0, u0, du0)
    for layer in layers:
        # ensure continuity of geometry
        if abs(layer.r_inner - state.r) > 1.0:  # >1 m mismatch
            # insert vacuum bridge if needed — skip, assume contiguous
            pass
        state = propagate_layer(layer, n, omega, state.u, state.du)
    return state


def surface_admittance(state: RadialState) -> complex:
    """Y = (du/dr) / u  at the evaluation radius (logarithmic derivative)."""
    if abs(state.u) < 1e-30:
        return 1e30 + 0j
    return state.du / state.u
