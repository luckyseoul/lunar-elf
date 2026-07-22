"""Skin depth, loss tangent, and path-attenuation utilities (Phase 0)."""

from __future__ import annotations

import numpy as np

from .constants import C0, EPS0, MU0, R_MOON
from .profiles import ConductivityProfile


def omega(f_hz: float | np.ndarray) -> np.ndarray:
    return 2.0 * np.pi * np.asarray(f_hz, dtype=float)


def skin_depth(f_hz: float | np.ndarray, sigma: float | np.ndarray, mu: float = MU0) -> np.ndarray:
    """Good-conductor skin depth δ = √(2/ωμσ). Valid when σ ≫ ωε."""
    w = omega(f_hz)
    s = np.asarray(sigma, dtype=float)
    return np.sqrt(2.0 / (w * mu * np.clip(s, 1e-30, None)))


def loss_tangent(
    f_hz: float | np.ndarray,
    sigma: float | np.ndarray,
    eps_r: float | np.ndarray = 5.5,
) -> np.ndarray:
    """tan δ = σ / (ωε). ≫1 ⇒ conduction-dominated; ≪1 ⇒ low-loss dielectric."""
    w = omega(f_hz)
    eps = np.asarray(eps_r, dtype=float) * EPS0
    return np.asarray(sigma, dtype=float) / (w * eps)


def attenuation_nepers_per_m(f_hz: float | np.ndarray, sigma: float | np.ndarray) -> np.ndarray:
    """Plane-wave α ≈ 1/δ in good-conductor limit (Np/m)."""
    return 1.0 / skin_depth(f_hz, sigma)


def path_attenuation_db(
    path_length_m: float,
    f_hz: float | np.ndarray,
    sigma: float | np.ndarray,
) -> np.ndarray:
    """Power attenuation over a path of constant σ: A_dB = 20 log10(e) * L/δ."""
    alpha = attenuation_nepers_per_m(f_hz, sigma)
    # field ~ e^{-αL}; power ~ e^{-2αL}; dB field uses 20 log10
    return 20.0 * np.log10(np.e) * alpha * path_length_m


def circumferential_path_m(radius: float = R_MOON, fraction: float = 1.0) -> float:
    return fraction * 2.0 * np.pi * radius


def radial_optical_depth(
    profile: ConductivityProfile,
    f_hz: float,
    r_inner: float | None = None,
    r_outer: float | None = None,
) -> float:
    """τ = ∫_{r_in}^{r_out} dr/δ(r) — cumulative skin-depths through the shell."""
    r_outer = profile.radius if r_outer is None else r_outer
    r_inner = 0.5 * profile.radius if r_inner is None else r_inner
    mask = (profile.r >= r_inner) & (profile.r <= r_outer)
    r = profile.r[mask]
    sig = profile.sigma[mask]
    if r.size < 2:
        return 0.0
    delta = skin_depth(f_hz, sig)
    # integrate in r ascending
    return float(np.trapezoid(1.0 / delta, r))


def effective_shell_sigma(
    profile: ConductivityProfile,
    depth_max_m: float = 3e5,
) -> float:
    """Log-mean σ over outer shell (surface to depth_max)."""
    depth = profile.radius - profile.r
    mask = depth <= depth_max_m
    if not np.any(mask):
        return float(profile.sigma[-1])
    return float(np.exp(np.mean(np.log(np.clip(profile.sigma[mask], 1e-30, None)))))


def shell_metrics(
    profile: ConductivityProfile,
    frequencies: np.ndarray,
    shell_depth_m: float = 3e5,
) -> dict[str, np.ndarray | float]:
    """Bundle of Phase-0 metrics used in paper tables."""
    sig_eff = effective_shell_sigma(profile, shell_depth_m)
    eps_eff = float(np.mean(profile.eps_r[(profile.radius - profile.r) <= shell_depth_m]))
    circ = circumferential_path_m(profile.radius)

    delta = skin_depth(frequencies, sig_eff)
    tan_d = loss_tangent(frequencies, sig_eff, eps_eff)
    att_half = path_attenuation_db(0.5 * circ, frequencies, sig_eff)  # antipode-ish half turn
    att_full = path_attenuation_db(circ, frequencies, sig_eff)

    # free-space wavelength scale
    lam = C0 / frequencies

    return {
        "sigma_eff": sig_eff,
        "eps_r_eff": eps_eff,
        "f_hz": frequencies,
        "skin_depth_km": delta / 1e3,
        "loss_tangent": tan_d,
        "att_half_circ_db": att_half,
        "att_full_circ_db": att_full,
        "lambda_km": lam / 1e3,
        "circ_km": circ / 1e3,
    }


def regime_label(tan_d: float) -> str:
    if tan_d < 0.1:
        return "low-loss dielectric"
    if tan_d < 1.0:
        return "transition"
    if tan_d < 100.0:
        return "weak conductor (conduction-dominated)"
    return "good conductor"
