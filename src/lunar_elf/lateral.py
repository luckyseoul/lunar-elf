"""Lateral heterogeneity: nearside / farside / PKT path experiments.

Not a full 3-D Maxwell solve. Provides quantitative bounds on how regional
σ contrasts change:
  1) regional cavity Q (local 1-D column under a station)
  2) great-circle path attenuation with piecewise-constant regional segments
  3) two-hemisphere effective Q (harmonic mean of wall conductances)

These bound the paper's claim under PKT / nearside–farside asymmetry without
requiring a full 3-D code.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .constants import R_MOON
from .literature_profiles import (
    profile_farside_cold,
    profile_grimm_lf_preferred,
    profile_nearside_warm,
    profile_pkt,
)
from .profiles import ConductivityProfile
from .skin import effective_shell_sigma, path_attenuation_db
from .sphere.impedance import (
    cavity_q_from_impedances,
    ideal_schumann_freq,
    ionosphere_impedance,
    profile_surface_impedance,
)


@dataclass
class RegionalResult:
    name: str
    Q_n1: float
    Re_Zg: float
    sigma_eff: float
    att_90deg_10Hz_db: float


def regional_column_metrics(
    profile: ConductivityProfile,
    h_iono_m: float = 100e3,
    sigma_iono: float = 1e-5,
) -> RegionalResult:
    f = ideal_schumann_freq(1, R_MOON)
    zg = profile_surface_impedance(profile, f, n_layers=80)
    zi = ionosphere_impedance(f, sigma_iono)
    q = cavity_q_from_impedances(f, h_iono_m, zg.Z, zi)["Q"]
    sig = effective_shell_sigma(profile, 3e5)
    att = float(path_attenuation_db(R_MOON * np.pi / 2, 10.0, sig))
    return RegionalResult(profile.name, q, float(np.real(zg.Z)), sig, att)


def piecewise_path_attenuation(
    segments: list[tuple[ConductivityProfile, float]],
    f_hz: float,
) -> dict:
    """segments: list of (profile, angle_deg along path). Returns total att dB."""
    total_db = 0.0
    parts = []
    for prof, ang in segments:
        sig = effective_shell_sigma(prof, 3e5)
        L = R_MOON * np.deg2rad(ang)
        att = float(path_attenuation_db(L, f_hz, sig))
        total_db += att
        parts.append({"profile": prof.name, "angle_deg": ang, "att_db": att, "sigma_eff": sig})
    return {"f_hz": f_hz, "total_att_db": total_db, "segments": parts}


def two_hemisphere_effective_q(
    prof_a: ConductivityProfile,
    prof_b: ConductivityProfile,
    h_iono_m: float = 100e3,
    sigma_iono: float = 1e-5,
) -> dict:
    """Crude global Q from two equal-area hemispheres.

    Wall loss ~ Re(Z); effective Re(Z) ≈ (Re Za + Re Zb)/2 for equal area.
    """
    f = ideal_schumann_freq(1, R_MOON)
    from .constants import MU0

    za = profile_surface_impedance(prof_a, f).Z
    zb = profile_surface_impedance(prof_b, f).Z
    zi = ionosphere_impedance(f, sigma_iono)
    re_eff = 0.5 * (float(np.real(za)) + float(np.real(zb)))
    q = (2.0 * np.pi * f * MU0 * h_iono_m) / (2.0 * (re_eff + float(np.real(zi))))
    return {
        "f_hz": f,
        "Re_Za": float(np.real(za)),
        "Re_Zb": float(np.real(zb)),
        "Re_Z_eff": re_eff,
        "Q_eff": float(q),
        "Q_a": cavity_q_from_impedances(f, h_iono_m, za, zi)["Q"],
        "Q_b": cavity_q_from_impedances(f, h_iono_m, zb, zi)["Q"],
    }


def run_lateral_suite() -> dict:
    """Full optional lateral experiment package."""
    global_p = profile_grimm_lf_preferred()
    near = profile_nearside_warm()
    far = profile_farside_cold()
    pkt = profile_pkt()

    columns = {
        p.name: regional_column_metrics(p)
        for p in (global_p, near, far, pkt)
    }

    # Paths: global, nearside-only arc, farside-only, mixed equator crossing, through PKT
    paths = {}
    for f in (1.0, 10.0, 30.0):
        paths[f"global_90_{f:g}Hz"] = piecewise_path_attenuation([(global_p, 90.0)], f)
        paths[f"nearside_90_{f:g}Hz"] = piecewise_path_attenuation([(near, 90.0)], f)
        paths[f"farside_90_{f:g}Hz"] = piecewise_path_attenuation([(far, 90.0)], f)
        paths[f"mixed_NS_90_{f:g}Hz"] = piecewise_path_attenuation([(near, 45.0), (far, 45.0)], f)
        paths[f"through_PKT_90_{f:g}Hz"] = piecewise_path_attenuation(
            [(pkt, 30.0), (near, 30.0), (far, 30.0)], f
        )

    hemi = {
        "nearside_farside": two_hemisphere_effective_q(near, far),
        "pkt_farside": two_hemisphere_effective_q(pkt, far),
        "global_global": two_hemisphere_effective_q(global_p, global_p),
    }

    return {
        "columns": {k: vars(v) for k, v in columns.items()},
        "paths": paths,
        "hemispheres": hemi,
    }
