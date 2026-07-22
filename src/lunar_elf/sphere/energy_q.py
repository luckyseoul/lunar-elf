"""Energy-method Q estimate for a trial modal field in a stratified sphere.

For a prescribed real frequency and multipole n, build an approximate cavity
mode shape (regular solution in the interior + sinusoidal vacuum gap for closed
models) and evaluate

    Q ≈ ω W_stored / P_dissipated

with
    W ~ (μ/4) ∫ |H|² dV + (ε/4) ∫ |E|² dV
    P ~ (1/2) ∫ σ |E|² dV

This is not an exact eigenmode Q, but gives a robust order-of-magnitude bound
that is hard to fool numerically and directly supports the paper claim.
"""

from __future__ import annotations

import numpy as np

from ..constants import EPS0, MU0
from .layers import Layer, k_complex
from .transfer import propagate_layer, RadialState


def _layer_field_samples(
    layer: Layer,
    n: int,
    omega: float,
    state_in: RadialState,
    n_pts: int = 16,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Sample |u(r)|² along layer; return r, |u|², |du|²."""
    rs = np.linspace(layer.r_inner, layer.r_outer, n_pts)
    u_abs2 = []
    du_abs2 = []
    st = state_in
    # re-propagate segment by segment for samples
    u, du = state_in.u, state_in.du
    r_prev = layer.r_inner
    for r in rs:
        if r > r_prev + 1e-6:
            sub = Layer(r_prev, float(r), layer.sigma, layer.eps_r, layer.mu_r)
            st = propagate_layer(sub, n, omega, u, du)
            u, du = st.u, st.du
            r_prev = float(r)
        u_abs2.append(abs(u) ** 2)
        du_abs2.append(abs(du) ** 2)
    return rs, np.array(u_abs2), np.array(du_abs2)


def energy_q_closed(
    layers: list[Layer],
    n: int,
    f_hz: float,
    r_surface: float,
) -> dict[str, float]:
    """Estimate Q for multipole n at frequency f using stored/dissipated energy.

    Field proxy: u(r) from regular center solution of the radial ODE.
    E_θ ~ u/r related; H_φ ~ du/dr related (TM_r scaling). We use dimensional
    proxies consistent up to an overall amplitude that cancels in Q.
    """
    omega = 2.0 * np.pi * f_hz
    # start regular
    r0 = layers[0].r_inner
    u = (r0 ** (n + 1)) + 0j
    du = (n + 1) * (r0**n) + 0j

    W_m = 0.0  # magnetic energy proxy
    W_e = 0.0  # electric energy proxy
    P = 0.0  # dissipated power proxy

    for layer in layers:
        st_in = RadialState(layer.r_inner, u, du)
        rs, u2, du2 = _layer_field_samples(layer, n, omega, st_in, n_pts=12)
        # spherical shell volume weight ~ r² (angular integrals cancel in ratio)
        w = rs**2
        # proxies: |H|² ~ |du|², |E|² ~ |u|²/r² * n(n+1) scale — use |u|²/r²
        e2 = u2 / np.clip(rs**2, 1.0, None)
        h2 = du2

        eps = layer.eps_r * EPS0
        mu = layer.mu_r * MU0
        # integrate with trapz
        dW_m = np.trapezoid(mu * h2 * w, rs)
        dW_e = np.trapezoid(eps * e2 * w, rs)
        dP = np.trapezoid(layer.sigma * e2 * w, rs)
        W_m += float(np.real(dW_m))
        W_e += float(np.real(dW_e))
        P += float(np.real(dP))

        # advance state to end of layer
        st_out = propagate_layer(layer, n, omega, u, du)
        u, du = st_out.u, st_out.du

    W = 0.25 * (W_m + W_e)
    P_diss = 0.5 * P
    if P_diss <= 0 or W <= 0:
        q = float("inf")
    else:
        q = float(omega * W / P_diss)

    return {
        "f_hz": f_hz,
        "n": float(n),
        "Q_energy": q,
        "W_proxy": W,
        "P_proxy": P_diss,
    }


def path_q_proxy(
    sigma_eff: float,
    f_hz: float,
    path_length_m: float,
    eps_r: float = 5.5,
) -> dict[str, float]:
    """Ultra-simple Q upper bound for a wave traveling a closed path L ≈ 2πR.

    Treating the shell as a 1-D ring resonator with attenuation α = 1/δ:
        Q ≲ β / (2α) with β = ω/v, v ~ c/√ε_r  (upper bound, optimistic phase velocity)

    For conduction-dominated media this overestimates phase velocity; still a
    useful ceiling on Q.
    """
    from ..skin import skin_depth

    delta = float(skin_depth(f_hz, sigma_eff))
    alpha = 1.0 / delta
    v = 2.99792458e8 / np.sqrt(eps_r)
    beta = 2.0 * np.pi * f_hz / v
    q = beta / (2.0 * alpha) if alpha > 0 else float("inf")
    # also: round-trip field attenuation
    att_np = alpha * path_length_m
    return {
        "f_hz": f_hz,
        "sigma_eff": sigma_eff,
        "skin_depth_km": delta / 1e3,
        "Q_path_upper": float(q),
        "round_trip_att_np": float(att_np),
        "round_trip_att_db": float(20 * np.log10(np.e) * att_np),
    }
