"""Layered spherical media for transfer-matrix EM."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..constants import EPS0, MU0
from ..profiles import ConductivityProfile


@dataclass
class Layer:
    r_inner: float  # m
    r_outer: float  # m
    sigma: float  # S/m
    eps_r: float = 1.0
    mu_r: float = 1.0

    @property
    def thickness(self) -> float:
        return self.r_outer - self.r_inner


def profile_to_layers(profile: ConductivityProfile, n_layers: int = 80) -> list[Layer]:
    """Resample a continuous profile into n_layers constant-property shells."""
    r_edges = np.linspace(profile.r[0], profile.radius, n_layers + 1)
    layers: list[Layer] = []
    for i in range(n_layers):
        r_in, r_out = float(r_edges[i]), float(r_edges[i + 1])
        r_mid = 0.5 * (r_in + r_out)
        layers.append(
            Layer(
                r_inner=r_in,
                r_outer=r_out,
                sigma=float(profile.sigma_at(r_mid)),
                eps_r=float(profile.eps_r_at(r_mid)),
            )
        )
    return layers


def k_complex(omega: complex | float, sigma: float, eps_r: float = 1.0, mu_r: float = 1.0) -> complex:
    """Complex wave number k = ω√(μ ε_c) with ε_c = ε - iσ/ω (e^{-iωt} convention → +iσ/ω in k²).

    We use time factor e^{+jωt} common in engineering: k² = ω²με - jωμσ
    equivalently k² = ω²μ(ε - jσ/ω).
    """
    w = complex(omega)
    if abs(w) < 1e-30:
        return 0j
    mu = mu_r * MU0
    eps = eps_r * EPS0
    # k² = ω² με - j ω μ σ
    k2 = (w**2) * mu * eps - 1j * w * mu * sigma
    k = np.sqrt(k2)
    # branch: Im(k) <= 0 for e^{+jωt} decaying into conductor... 
    # With e^{+jωt}, passive media need Im(k) <= 0 for e^{-j k r} ~ decay in +r for some conventions.
    # We force Re(k) >= 0 and Im(k) <= 0 for lossy media.
    if k.real < 0:
        k = -k
    if k.imag > 0:
        k = -k
    return complex(k)


def vacuum_layers(r_inner: float, r_outer: float, n: int = 10) -> list[Layer]:
    edges = np.linspace(r_inner, r_outer, n + 1)
    return [
        Layer(float(edges[i]), float(edges[i + 1]), sigma=0.0, eps_r=1.0)
        for i in range(n)
    ]


def pec_shell(r_inner: float, r_outer: float, sigma: float = 1e6) -> Layer:
    """Highly conducting shell (ionosphere proxy)."""
    return Layer(r_inner, r_outer, sigma=sigma, eps_r=1.0)
