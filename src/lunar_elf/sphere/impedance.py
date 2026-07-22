"""Stable surface-impedance recursion and Schumann-cavity Q estimates.

At ELF the planar layered impedance recursion (magnetotelluric style) is an
excellent approximation for the local surface impedance of the Moon. Cavity Q
then follows from the standard energy balance between vacuum-gap stored energy
and wall dissipation (ground + optional ionosphere):

    Q ≈ ω μ₀ h / [2 Re(Z_g + Z_i)]

for a cavity of height h ≪ R (Sentman / Wait order-of-magnitude form).
This is numerically robust and sufficient for paper-grade bounds.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..constants import C0, EPS0, MU0, R_EARTH, R_MOON
from ..profiles import ConductivityProfile
from .layers import k_complex


@dataclass
class ImpedanceResult:
    f_hz: float
    Z: complex  # Ohm
    delta_km: float
    sigma_top: float


def layer_impedance_recursion(
    thicknesses: np.ndarray,
    sigmas: np.ndarray,
    eps_rs: np.ndarray,
    f_hz: float,
    mu_r: float = 1.0,
) -> complex:
    """Recursive surface impedance looking into a stack (top = index 0).

    thicknesses[i], sigmas[i] from the surface downward.
    Deepest layer is treated as a half-space.
    """
    omega = 2.0 * np.pi * f_hz
    mu = mu_r * MU0
    n = len(sigmas)
    # half-space impedance of deepest layer: Z = ωμ / k  (for e^{+jωt}, k with Im<=0)
    k_n = k_complex(omega, float(sigmas[-1]), float(eps_rs[-1]), mu_r)
    if abs(k_n) < 1e-30:
        Z = complex(np.sqrt(mu / (eps_rs[-1] * EPS0 + 1e-30)))  # dielectric
    else:
        Z = omega * mu / k_n

    # recurse upward (from deep to surface): indices n-2 ... 0
    for i in range(n - 2, -1, -1):
        k = k_complex(omega, float(sigmas[i]), float(eps_rs[i]), mu_r)
        if abs(k) < 1e-30:
            Z0 = complex(np.sqrt(mu / (eps_rs[i] * EPS0 + 1e-30)))
            # dielectric layer transmission-line style
            gamma = 1j * omega * np.sqrt(mu * eps_rs[i] * EPS0)
        else:
            Z0 = omega * mu / k  # intrinsic
            gamma = 1j * k  # propagation constant for e^{-gamma z} into medium
            # With our k branch (Re>=0, Im<=0), for z downward into Earth use
            # careful tanh. Use γ = jk with Re(γ)>=0 for decay into medium.
            if np.real(gamma) < 0:
                gamma = -gamma
                Z0 = -Z0

        d = float(thicknesses[i])
        # Z_in = Z0 * (Z + Z0 tanh(γd)) / (Z0 + Z tanh(γd))
        th = np.tanh(gamma * d)
        # numerical guard
        if abs(th) > 1e6:
            Z = Z0
        else:
            Z = Z0 * (Z + Z0 * th) / (Z0 + Z * th + 1e-30)
    return complex(Z)


def profile_surface_impedance(
    profile: ConductivityProfile,
    f_hz: float,
    n_layers: int = 80,
    max_depth_m: float | None = None,
) -> ImpedanceResult:
    """Surface impedance of a planetary profile (flat-layer stack)."""
    R = profile.radius
    max_depth = 0.9 * R if max_depth_m is None else max_depth_m
    # layers from surface downward
    depths = np.linspace(0.0, max_depth, n_layers + 1)
    thicknesses = np.diff(depths)
    r_mids = R - 0.5 * (depths[:-1] + depths[1:])
    sigmas = profile.sigma_at(r_mids)
    eps_rs = profile.eps_r_at(r_mids)
    Z = layer_impedance_recursion(thicknesses, sigmas, eps_rs, f_hz)
    # skin depth of top material for reference
    s0 = float(sigmas[0])
    from ..skin import skin_depth

    dlt = float(skin_depth(f_hz, s0))
    return ImpedanceResult(f_hz=f_hz, Z=Z, delta_km=dlt / 1e3, sigma_top=s0)


def ionosphere_impedance(f_hz: float, sigma: float = 1e-5, eps_r: float = 1.0) -> complex:
    """Half-space impedance of a uniform ionosphere proxy."""
    omega = 2.0 * np.pi * f_hz
    k = k_complex(omega, sigma, eps_r)
    if abs(k) < 1e-30:
        return complex(np.sqrt(MU0 / (eps_r * EPS0)))
    return complex(omega * MU0 / k)


def cavity_q_from_impedances(
    f_hz: float,
    h_m: float,
    Z_ground: complex,
    Z_iono: complex | None = None,
) -> dict[str, float]:
    """Q ≈ ω μ₀ h / [2 Re(Z_g + Z_i)].

    If Z_iono is None (open cavity / no upper wall), dissipation has no upper
    bound from this formula — return Q=0 to signal "no cavity".
    """
    omega = 2.0 * np.pi * f_hz
    if Z_iono is None:
        return {
            "f_hz": f_hz,
            "h_km": h_m / 1e3,
            "Re_Zg": float(np.real(Z_ground)),
            "Re_Zi": float("nan"),
            "Q": 0.0,
            "note": "open_no_ionosphere",
        }
    re = float(np.real(Z_ground) + np.real(Z_iono))
    re = max(re, 1e-30)
    q = (omega * MU0 * h_m) / (2.0 * re)
    return {
        "f_hz": f_hz,
        "h_km": h_m / 1e3,
        "Re_Zg": float(np.real(Z_ground)),
        "Re_Zi": float(np.real(Z_iono)),
        "Q": float(q),
        "note": "closed",
    }


def ideal_schumann_freq(n: int, radius: float) -> float:
    return (C0 / (2.0 * np.pi * radius)) * np.sqrt(n * (n + 1))


def schumann_q_suite(
    profile: ConductivityProfile,
    h_iono_m: float = 100e3,
    sigma_iono: float = 1e-5,
    multipoles: tuple[int, ...] = (1, 2, 3),
    open_cavity: bool = False,
) -> list[dict]:
    """Compute impedance-based Q for multipoles at ideal Schumann frequencies."""
    rows = []
    for n in multipoles:
        f = ideal_schumann_freq(n, profile.radius)
        zg = profile_surface_impedance(profile, f)
        if open_cavity:
            qi = cavity_q_from_impedances(f, h_iono_m, zg.Z, None)
        else:
            zi = ionosphere_impedance(f, sigma_iono)
            qi = cavity_q_from_impedances(f, h_iono_m, zg.Z, zi)
        rows.append(
            {
                "profile": profile.name,
                "n": n,
                "f_hz": f,
                "Re_Zg": qi["Re_Zg"],
                "Re_Zi": qi["Re_Zi"],
                "Q": qi["Q"],
                "delta_top_km": zg.delta_km,
                "sigma_top": zg.sigma_top,
                "h_km": h_iono_m / 1e3,
                "open": open_cavity,
            }
        )
    return rows


def earth_schumann_check(
    profile: ConductivityProfile,
    h_iono_m: float = 70e3,
    sigma_iono: float = 1e-4,
) -> list[dict]:
    """Earth validation with given ground profile."""
    # temporarily use Earth radius for ideal f via override
    rows = []
    for n in (1, 2, 3):
        f = ideal_schumann_freq(n, R_EARTH)
        # force impedance at Earth f with earth profile
        zg = profile_surface_impedance(profile, f)
        zi = ionosphere_impedance(f, sigma_iono)
        qi = cavity_q_from_impedances(f, h_iono_m, zg.Z, zi)
        rows.append(
            {
                "profile": profile.name,
                "n": n,
                "f_hz": f,
                "Re_Zg": qi["Re_Zg"],
                "Re_Zi": qi["Re_Zi"],
                "Q": qi["Q"],
                "delta_top_km": zg.delta_km,
                "h_km": h_iono_m / 1e3,
            }
        )
    return rows
