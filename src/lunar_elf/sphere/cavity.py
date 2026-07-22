"""Spherical cavity response and modal Q estimation.

Models
------
A — Open Moon: interior layers only; exterior vacuum radiation / no upper wall.
    No trapped Schumann cavity. We report surface impedance and a proxy
    "would-be" attenuation for near-surface guided energy.

B — Closed cavity: Moon interior + vacuum gap + conducting ionosphere shell.
    Full radial stack; resonance peaks in a driven response give f_n and Q_n.

C — Earth validation: Earth σ(r) + vacuum gap + ionosphere.

Driven diagnostic
-----------------
For a fixed multipole n we compute a cavity transfer function from a unit
"voltage" source at the surface (discontinuity in du) to the ionosphere /
observation level. Resonances appear as peaks in |R(ω)|; Q ≈ f0 / FWHM.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.signal import find_peaks

from ..constants import C0, R_EARTH, R_MOON
from ..profiles import ConductivityProfile
from .layers import Layer, pec_shell, profile_to_layers, vacuum_layers
from .transfer import propagate_stack, surface_admittance


@dataclass
class CavityModel:
    name: str
    layers: list[Layer]
    r_surface: float  # planetary surface
    r_observe: float  # observation / ionosphere inner edge
    description: str = ""


def build_model_A_open(profile: ConductivityProfile, n_body: int = 60) -> CavityModel:
    layers = profile_to_layers(profile, n_body)
    return CavityModel(
        name=f"A_open_{profile.name}",
        layers=layers,
        r_surface=profile.radius,
        r_observe=profile.radius,
        description="Open Moon: interior only, no ionosphere",
    )


def build_model_B_closed(
    profile: ConductivityProfile,
    h_iono_km: float = 100.0,
    sigma_iono: float = 1e-5,
    n_body: int = 50,
    n_vac: int = 12,
    n_iono: int = 4,
) -> CavityModel:
    """Moon + vacuum cavity + lossy ionosphere shell."""
    body = profile_to_layers(profile, n_body)
    r_s = profile.radius
    r_i = r_s + h_iono_km * 1e3
    vac = vacuum_layers(r_s, r_i, n_vac)
    # thin ionosphere shell ~20 km effective
    iono_top = r_i + 2e4
    iono = vacuum_layers(r_i, iono_top, max(n_iono - 1, 1))
    # replace iono layers with conducting
    iono = [
        Layer(L.r_inner, L.r_outer, sigma=sigma_iono, eps_r=1.0) for L in iono
    ]
    # cap with stronger outer conductor
    iono.append(pec_shell(iono_top, iono_top + 5e3, sigma=1e2))
    layers = body + vac + iono
    return CavityModel(
        name=f"B_closed_{profile.name}_h{h_iono_km:.0f}",
        layers=layers,
        r_surface=r_s,
        r_observe=r_i,
        description=f"Closed cavity h={h_iono_km} km, σ_iono={sigma_iono:.1e}",
    )


def build_model_C_earth(
    profile: ConductivityProfile,
    h_iono_km: float = 70.0,
    sigma_iono: float = 1e-5,
    n_body: int = 40,
    n_vac: int = 10,
) -> CavityModel:
    return build_model_B_closed(
        profile,
        h_iono_km=h_iono_km,
        sigma_iono=sigma_iono,
        n_body=n_body,
        n_vac=n_vac,
    )


def ideal_schumann_freq(n: int, radius: float) -> float:
    """Ideal PEC cavity Schumann frequency f_n = (c/2πR) √[n(n+1)]."""
    return (C0 / (2.0 * np.pi * radius)) * np.sqrt(n * (n + 1))


def logarithmic_derivative_at(
    model: CavityModel,
    n: int,
    f_hz: float | complex,
    r_target: float | None = None,
) -> complex:
    """Propagate from center and return Y = u'/u at r_target (default surface)."""
    omega = 2.0 * np.pi * f_hz
    # truncate layers up to target
    r_t = model.r_surface if r_target is None else r_target
    use: list[Layer] = []
    for L in model.layers:
        if L.r_inner >= r_t - 1e-3:
            break
        if L.r_outer > r_t:
            use.append(Layer(L.r_inner, r_t, L.sigma, L.eps_r, L.mu_r))
            break
        use.append(L)
    if not use:
        raise ValueError("no layers below target radius")
    state = propagate_stack(use, n, omega)
    return surface_admittance(state)


def cavity_response(
    model: CavityModel,
    n: int,
    frequencies: np.ndarray,
) -> np.ndarray:
    """Scalar response diagnostic vs real frequency.

    For closed cavities we use the mismatch between interior surface admittance
    and the admittance of the vacuum+ionosphere stack looking upward — resonance
    when the cavity "round trip" condition is met (minimum |Y_in + Y_up| or peak
    of 1/|Y_in+Y_up|).

    For open models, |1/Y_surface| tracks a surface-impedance related response.
    """
    freqs = np.asarray(frequencies, dtype=float)
    resp = np.zeros(freqs.size, dtype=float)

    # Pre-split layers at surface
    body = [L for L in model.layers if L.r_outer <= model.r_surface + 1.0]
    upper = [L for L in model.layers if L.r_inner >= model.r_surface - 1.0]

    for i, f in enumerate(freqs):
        omega = 2.0 * np.pi * f
        if not body:
            resp[i] = 0.0
            continue
        st_body = propagate_stack(body, n, omega)
        Y_in = surface_admittance(st_body)

        if not upper:
            # open: use surface impedance magnitude proxy Z ~ 1/Y
            resp[i] = float(np.abs(1.0 / (Y_in + 1e-30)))
            continue

        # Propagate upper stack from surface outward with two independent
        # solutions and form upward-looking admittance via a thin vacuum start.
        # Simpler approach: integrate full stack and compare u at observe to surface source.
        # Use boundary condition u(r_top)=0 (PEC outer) and measure u(surface) sensitivity.
        # ---
        # Practical closed-cavity resonance finder:
        # Full propagate center → top; outer PEC requires u(r_top)≈0 for free modes.
        # Driven: force du jump. Response = |u(r_obs)/u_scale|.
        st_full = propagate_stack(model.layers, n, omega)
        # Free-mode residual: |u(top)| for regular interior start (not normalized)
        # Normalize by surface |u| to get a geometric residual
        # Re-propagate to surface for normalization
        st_s = propagate_stack(body, n, omega)
        u_top = st_full.u
        u_s = st_s.u
        # Resonance when u_top small relative to cavity energy proxy
        residual = abs(u_top) / (abs(u_s) + 1e-30)
        resp[i] = 1.0 / (residual + 1e-30)

    return resp


def estimate_q_from_spectrum(
    frequencies: np.ndarray,
    response: np.ndarray,
    n_peaks: int = 3,
    min_prominence: float | None = None,
) -> list[dict[str, float]]:
    """Find peaks and estimate Q = f0 / FWHM from |response| spectrum."""
    freqs = np.asarray(frequencies, dtype=float)
    y = np.asarray(response, dtype=float)
    if y.size < 5:
        return []

    # log-scale prominence often better for large dynamic range
    y_p = y / (np.max(y) + 1e-30)
    prom = min_prominence if min_prominence is not None else 0.05
    peaks, props = find_peaks(y_p, prominence=prom, distance=max(3, len(y) // 50))
    if peaks.size == 0:
        # take global max as single peak
        peaks = np.array([int(np.argmax(y_p))])

    # sort by height
    order = np.argsort(y[peaks])[::-1]
    peaks = peaks[order[:n_peaks]]

    results = []
    for idx in peaks:
        f0 = float(freqs[idx])
        half = 0.5 * y[idx]
        # left FWHM
        left = idx
        while left > 0 and y[left] > half:
            left -= 1
        right = idx
        while right < len(y) - 1 and y[right] > half:
            right += 1
        # interpolate
        def _cross(i0, i1):
            if i0 == i1 or y[i1] == y[i0]:
                return float(freqs[i0])
            t = (half - y[i0]) / (y[i1] - y[i0])
            return float(freqs[i0] + t * (freqs[i1] - freqs[i0]))

        f_l = _cross(left, min(left + 1, len(y) - 1))
        f_r = _cross(max(right - 1, 0), right)
        fwhm = max(f_r - f_l, freqs[1] - freqs[0])
        q = f0 / fwhm if fwhm > 0 else np.nan
        results.append({"f0_hz": f0, "fwhm_hz": fwhm, "Q": q, "peak_height": float(y[idx])})
    return results


def free_mode_residual(
    model: CavityModel,
    n: int,
    f_complex: complex,
) -> complex:
    """Complex residual for free modes of closed cavity: u(top) with regular interior.

    Roots of residual(f) = 0 are eigenfrequencies (with Im part → damping).
    """
    omega = 2.0 * np.pi * f_complex
    st = propagate_stack(model.layers, n, omega)
    return st.u


def refine_complex_root(
    model: CavityModel,
    n: int,
    f_seed_hz: float,
    imag_seed: float = -0.1,
    n_iter: int = 20,
) -> complex | None:
    """Secant search for complex eigenfrequency near f_seed."""
    z0 = complex(f_seed_hz, imag_seed)
    z1 = complex(f_seed_hz * 1.02, imag_seed * 1.1)
    f0 = free_mode_residual(model, n, z0)
    f1 = free_mode_residual(model, n, z1)
    for _ in range(n_iter):
        if abs(f1 - f0) < 1e-30:
            break
        z2 = z1 - f1 * (z1 - z0) / (f1 - f0)
        if abs(z2 - z1) < 1e-6 * max(1.0, abs(z1)):
            return z2
        z0, f0 = z1, f1
        z1, f1 = z2, free_mode_residual(model, n, z2)
    if abs(f1) < abs(f0):
        return z1
    return z0


def q_from_complex_freq(f: complex) -> float:
    """Q = Re(f) / (2 |Im(f)|) for time factor e^{+jωt} with Im(f)<0 for decay.

    If Im(f)>0 our branch may flip; use absolute value of imag part.
    """
    re = float(np.real(f))
    im = float(np.abs(np.imag(f)))
    if im < 1e-15:
        return float("inf")
    return re / (2.0 * im)
