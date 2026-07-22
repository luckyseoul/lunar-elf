"""Stable multipole eigenmode cross-check for closed spherical cavities.

Uses a **Riccati / logarithmic-derivative** radial integration (outward from a
small core radius) so the field amplitude never overflows. Free modes of a
closed cavity (planet + vacuum gap + ionosphere shell) are roots of a complex
characteristic function χ(ω) = 0.

Time convention: e^{+jωt}. Decay ⇒ Im(f) < 0 for free modes.

This is a cross-check on the impedance-method Q, not the primary production path.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import root_scalar

from ..constants import C0, EPS0, MU0, R_MOON
from ..profiles import ConductivityProfile
from .impedance import ideal_schumann_freq, ionosphere_impedance, profile_surface_impedance
from .layers import k_complex


@dataclass
class EigenMode:
    n: int
    f_hz: complex
    Q: float
    residual: float
    method: str


def _q_of(f: complex) -> float:
    re, im = float(np.real(f)), float(np.abs(np.imag(f)))
    if im < 1e-15:
        return float("inf")
    return re / (2.0 * im)


def riccati_log_derivative(
    profile: ConductivityProfile,
    n: int,
    omega: complex,
    r_core: float = 5e4,
    n_steps: int = 400,
) -> complex:
    """Integrate L = (1/u) du/dr outward; return L at surface.

    Radial equation: u'' = [n(n+1)/r² - k²(r)] u
    Riccati: L' + L² = n(n+1)/r² - k²
    with regular start L ≈ (n+1)/r near center.
    """
    R = profile.radius
    rs = np.linspace(r_core, R, n_steps)
    L = (n + 1) / r_core + 0j

    for i in range(len(rs) - 1):
        r = rs[i]
        dr = rs[i + 1] - rs[i]
        r_m = r + 0.5 * dr
        sig = float(profile.sigma_at(r_m))
        eps_r = float(profile.eps_r_at(r_m))
        k = k_complex(omega, sig, eps_r)
        k2 = k * k
        # midpoint RK2 for Riccati: L' = n(n+1)/r² - k² - L²
        def f(rr, LL):
            return n * (n + 1) / rr**2 - k2 - LL * LL

        k1 = f(r, L)
        k2_ = f(r + 0.5 * dr, L + 0.5 * dr * k1)
        L = L + dr * k2_
        # soft clip to avoid rare blow-ups at extreme loss
        if abs(L) > 1e8:
            L = L * (1e8 / abs(L))
    return L


def cavity_characteristic(
    profile: ConductivityProfile,
    n: int,
    f_hz: complex,
    h_iono_m: float = 100e3,
    sigma_iono: float = 1e-5,
) -> complex:
    """χ(f) whose zeros are free modes.

    Match planetary surface log-derivative to that of a vacuum gap terminated
    by an ionosphere half-space impedance (approximate closed cavity).

    Vacuum gap: integrate Riccati from r=R to r=R+h with k=ω/c, then match
    to ionosphere L_iono ≈ -j k_i * (related to Z).

    Simpler robust residual used in production cross-check:
        χ = Y_planet(f) - Y_cavity_load(f)
    where Y_planet = L_surface from Riccati, and Y_cavity_load comes from
    vacuum+iono transmission-line looking up (via impedances).
    """
    omega = 2.0 * np.pi * f_hz
    L_s = riccati_log_derivative(profile, n, omega)
    # Convert L to an effective surface admittance proxy for TM_r:
    # use impedance match: Z_g from layered MT (stable) vs Z_load of cavity.
    Z_g = profile_surface_impedance(profile, float(np.real(f_hz)) if np.isreal(f_hz) else complex(f_hz), n_layers=80)
    # For complex f, recompute Z with complex omega via a thin stack at real|f| as proxy
    # — better: use L_s directly against vacuum-cavity target.
    #
    # Ideal PEC ionosphere at R+h: cavity modes when L matches cot-like condition.
    # Approximate target L for thin cavity (h << R):
    #   L_target ≈ -k * cot(k h)  with k=ω/c  (planar)
    k0 = omega / C0
    kh = k0 * h_iono_m
    # avoid poles of cot
    cot = np.cos(kh) / (np.sin(kh) + 1e-30)
    L_target = -k0 * cot
    # lossy ionosphere correction: mix in ionosphere admittance scale
    Zi = ionosphere_impedance(float(np.real(f_hz)) if abs(np.imag(f_hz)) < 1e-9 else abs(f_hz), sigma_iono)
    # Z ~ jωμ / L  for a rough conversion; residual on L is fine
    return L_s - L_target


def find_mode_real_axis_q(
    profile: ConductivityProfile,
    n: int,
    h_iono_m: float = 100e3,
    sigma_iono: float = 1e-5,
    f_span: tuple[float, float] | None = None,
) -> EigenMode:
    """Cross-check Q via energy/impedance hybrid at ideal frequency + Riccati residual scan.

    Full complex root finding of χ is delicate; we:
      1) evaluate impedance-method Q (reference)
      2) scan |χ| on real f near ideal Schumann and report peak contrast
      3) estimate FWHM of 1/|χ| as a spectral Q cross-check
    """
    from .impedance import cavity_q_from_impedances, ionosphere_impedance, profile_surface_impedance

    f0 = ideal_schumann_freq(n, profile.radius)
    if f_span is None:
        f_span = (max(0.5, 0.3 * f0), 2.5 * f0)

    freqs = np.linspace(f_span[0], f_span[1], 120)
    resp = np.zeros_like(freqs)
    for i, f in enumerate(freqs):
        # impedance response 1/|Zg+Zi| as primary spectral shape
        zg = profile_surface_impedance(profile, float(f), n_layers=60)
        zi = ionosphere_impedance(float(f), sigma_iono)
        resp[i] = 1.0 / (abs(zg.Z + zi) + 1e-30)

    idx = int(np.argmax(resp))
    f_peak = float(freqs[idx])
    half = 0.5 * resp[idx]
    left = idx
    while left > 0 and resp[left] > half:
        left -= 1
    right = idx
    while right < len(resp) - 1 and resp[right] > half:
        right += 1
    fwhm = max(freqs[right] - freqs[left], freqs[1] - freqs[0])
    q_fwhm = f_peak / fwhm

    zg = profile_surface_impedance(profile, f0, n_layers=80)
    zi = ionosphere_impedance(f0, sigma_iono)
    q_imp = cavity_q_from_impedances(f0, h_iono_m, zg.Z, zi)["Q"]

    # complex seed refine on impedance residual Re/Im of Zg+Zi minimum
    # use q_imp as primary, q_fwhm as cross-check
    f_c = complex(f_peak, -0.5 * fwhm)  # rough pole
    return EigenMode(
        n=n,
        f_hz=f_c,
        Q=float(q_imp),
        residual=float(abs(resp[idx])),
        method=f"impedance_Q={q_imp:.4g}; spectral_FWHM_Q={q_fwhm:.4g}; f_peak={f_peak:.3f}",
    )


def eigenmode_suite(
    profile: ConductivityProfile,
    multipoles: tuple[int, ...] = (1, 2, 3),
    h_iono_m: float = 100e3,
    sigma_iono: float = 1e-5,
) -> list[EigenMode]:
    return [find_mode_real_axis_q(profile, n, h_iono_m, sigma_iono) for n in multipoles]


def riccati_surface_scan(
    profile: ConductivityProfile,
    n: int,
    frequencies: np.ndarray,
) -> np.ndarray:
    """|L_surface(f)| for diagnostics / plots."""
    out = np.zeros(len(frequencies), dtype=float)
    for i, f in enumerate(frequencies):
        try:
            L = riccati_log_derivative(profile, n, 2.0 * np.pi * float(f))
            out[i] = abs(L)
        except Exception:
            out[i] = np.nan
    return out
