"""Literature-anchored lunar conductivity profiles.

Primary sources encoded here
----------------------------
Grimm (2023/2024), arXiv:2305.01462 / Icarus:
  - Preferred LF inversion valid ~400–1200 km:
        σ(z) = 1.76e-4 * exp(z_km / 210)   [S/m]
  - Model-top constraint ~3e-5 S/m (not true surface)
  - Near-surface: Dyal & Parkin (1977) σ < 1e-8 S/m for z < 80 km;
    lunar rocks at T<300 K even lower (~1e-10)
  - HF band (200–550 km) gives higher σ; Grimm argues likely biased —
    retained as an upper-envelope end-member only

Mittelholz et al. (2021), JGR Planets (global LP orbital sounding):
  - Global upper/midmantle structure; less sensitive to shallowest crust
  - Constructed here as a smooth global envelope consistent with published
    orbital-class midmantle conductivities (midmantle rising toward 1e-3–1e-2),
    with a resistive lid. Not a figure digitization; labeled as such.

Hood et al. (1982) bounds: outer shell highly resistive; LF Grimm lies
near the upper end of classical Apollo bounds in the resolved band.

Regional lateral variants (for optional 3-D / path work)
-------------------------------------------------------
- Nearside (Procellarum / KREEP-influenced): warmer / slightly more conductive
- Farside highlands: colder / more resistive lid
- PKT (Procellarum KREEP Terrane): enhanced heat production → elevated σ
  in upper mantle relative to global mean (order-of-magnitude regional contrast)
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .constants import R_MOON
from .profiles import ConductivityProfile, _make_radial_grid

DATA = Path(__file__).resolve().parents[2] / "data" / "profiles"
LIT = Path(__file__).resolve().parents[2] / "data" / "literature"


def grimm_lf_sigma(depth_km: np.ndarray | float) -> np.ndarray:
    """Grimm LF analytic fit, valid ~400–1200 km; extrapolated with care outside."""
    z = np.asarray(depth_km, dtype=float)
    # Core of fit
    sig = 1.76e-4 * np.exp(z / 210.0)
    return sig


def _assemble(
    name: str,
    description: str,
    depth_km: np.ndarray,
    sigma: np.ndarray,
    eps_r: float = 5.5,
) -> ConductivityProfile:
    depth_m = depth_km * 1e3
    r = R_MOON - depth_m
    # sort ascending r
    order = np.argsort(r)
    r = r[order]
    sigma = np.asarray(sigma, dtype=float)[order]
    # floor / ceiling
    sigma = np.clip(sigma, 1e-12, 1e2)
    eps = np.full_like(r, eps_r)
    # denser near surface if needed — already on grid
    return ConductivityProfile(name, description, r, sigma, eps, R_MOON)


def profile_grimm_lf_preferred(n: int = 500) -> ConductivityProfile:
    """Grimm preferred LF profile with physically resistive lid.

    Construction:
      z < 80 km:  σ = 1e-9 … 1e-8 (Dyal & Parkin upper-bound region)
      80–400 km:  log-linear bridge to Grimm LF at 400 km
      400–1200 km: Grimm LF formula
      >1200 km:   continue gently toward ~0.06 S/m class deep values
    """
    depth = np.linspace(0.0, 0.999 * R_MOON / 1e3, n)
    sig = np.empty_like(depth)

    sig400 = float(grimm_lf_sigma(400.0))  # ~1.2e-3
    for i, z in enumerate(depth):
        if z <= 80.0:
            # cold lid: well below 1e-8 upper limit
            sig[i] = 1e-9 * 10 ** (z / 80.0)  # 1e-9 → 1e-8
        elif z <= 400.0:
            # log bridge 1e-8 @80 → sig400 @400
            t = (z - 80.0) / (400.0 - 80.0)
            log_s = np.log10(1e-8) + t * (np.log10(sig400) - np.log10(1e-8))
            sig[i] = 10**log_s
        elif z <= 1200.0:
            sig[i] = float(grimm_lf_sigma(z))
        else:
            # soft approach to deep ~0.06
            base = float(grimm_lf_sigma(1200.0))
            t = min((z - 1200.0) / 400.0, 1.0)
            sig[i] = base * (0.06 / base) ** t if base > 0 else 0.06

    return _assemble(
        "grimm_lf_preferred",
        "Grimm (2023) LF fit 400–1200 km + Dyal–Parkin resistive lid; preferred 1-D.",
        depth,
        sig,
    )


def profile_grimm_hf_envelope(n: int = 500) -> ConductivityProfile:
    """Grimm HF-style elevated upper-mantle envelope (use as upper bound only).

    Grimm cautions HF is likely biased high; retained for sensitivity.
    Approximates: higher σ for 200–550 km, join LF below ~900 km.
    """
    depth = np.linspace(0.0, 0.999 * R_MOON / 1e3, n)
    base = profile_grimm_lf_preferred(n)
    sig = base.sigma_at(R_MOON - depth * 1e3).copy()
    for i, z in enumerate(depth):
        if 150.0 <= z <= 550.0:
            # elevate by up to ~10× in mid of band (schematic of HF excess)
            boost = 10.0 ** (1.0 * np.exp(-((z - 300.0) / 120.0) ** 2))
            sig[i] = float(sig[i] * boost)
        elif z < 150.0:
            # still more conductive than cold lid but below HF peak
            sig[i] = max(sig[i], 3e-5 * 10 ** (-(150.0 - z) / 80.0))
    return _assemble(
        "grimm_hf_envelope",
        "Grimm HF-band elevated upper-mantle envelope (likely biased; upper bound).",
        depth,
        sig,
    )


def profile_mittelholz_like(n: int = 500) -> ConductivityProfile:
    """Global orbital-class envelope inspired by Mittelholz et al. (2021).

    Not a point-digitization of their figure. Constructed to represent a global
    average with:
      - resistive outer lid
      - midmantle conductivities in the 1e-4 … 1e-2 class
      - smooth rise (orbital sounding resolves upper/midmantle, not regolith)
    """
    depth = np.linspace(0.0, 0.999 * R_MOON / 1e3, n)
    # knots (depth_km, sigma)
    knots_z = np.array([0.0, 50.0, 150.0, 300.0, 500.0, 800.0, 1200.0, 1700.0])
    knots_s = np.array([5e-9, 3e-8, 5e-6, 1e-4, 8e-4, 5e-3, 2e-2, 5e-2])
    log_s = np.interp(depth, knots_z, np.log10(knots_s))
    return _assemble(
        "mittelholz_like",
        "Mittelholz-like global orbital envelope (constructed; not figure-digitized).",
        depth,
        10**log_s,
    )


def profile_hood_upper_bound(n: int = 400) -> ConductivityProfile:
    """Conservative upper-bound outer shell (highly resistive) for classical Apollo bounds."""
    depth = np.linspace(0.0, 0.999 * R_MOON / 1e3, n)
    knots_z = np.array([0.0, 100.0, 300.0, 500.0, 800.0, 1200.0, 1700.0])
    knots_s = np.array([1e-9, 1e-8, 1e-6, 1e-4, 1e-3, 1e-2, 5e-2])
    log_s = np.interp(depth, knots_z, np.log10(knots_s))
    return _assemble(
        "hood_upper_resistive",
        "Classical Apollo-era highly resistive outer-shell end-member (Hood-class).",
        depth,
        10**log_s,
    )


# --- Regional lateral variants ------------------------------------------------

def profile_nearside_warm(n: int = 500) -> ConductivityProfile:
    """Nearside: modestly elevated σ (higher heat flow / thinner lithosphere)."""
    base = profile_grimm_lf_preferred(n)
    depth = (R_MOON - base.r) / 1e3
    sig = base.sigma.copy()
    # boost upper 600 km by ~3–5×
    boost = np.where(depth < 600.0, 4.0 * np.exp(-depth / 400.0) + 1.0, 1.0)
    return _assemble(
        "nearside_warm",
        "Nearside warmer variant of Grimm LF preferred (elevated upper-mantle σ).",
        depth,
        sig * boost,
        eps_r=6.0,
    )


def profile_farside_cold(n: int = 500) -> ConductivityProfile:
    """Farside highlands: colder, thicker resistive lid."""
    base = profile_grimm_lf_preferred(n)
    depth = (R_MOON - base.r) / 1e3
    sig = base.sigma.copy()
    # suppress upper 500 km
    factor = np.where(depth < 500.0, 0.2 + 0.8 * (depth / 500.0), 1.0)
    return _assemble(
        "farside_cold",
        "Farside colder variant: thicker resistive lid relative to Grimm LF.",
        depth,
        sig * factor,
        eps_r=5.0,
    )


def profile_pkt(n: int = 500) -> ConductivityProfile:
    """Procellarum KREEP Terrane: enhanced radiogenic heating → higher σ."""
    base = profile_nearside_warm(n)
    depth = (R_MOON - base.r) / 1e3
    sig = base.sigma.copy()
    # additional PKT boost focused 50–400 km
    pkt = 1.0 + 8.0 * np.exp(-((depth - 200.0) / 150.0) ** 2)
    return _assemble(
        "pkt",
        "Procellarum KREEP Terrane: nearside + localized upper-mantle conductivity boost.",
        depth,
        sig * pkt,
        eps_r=6.5,
    )


LITERATURE_PROFILES = {
    "grimm_lf_preferred": profile_grimm_lf_preferred,
    "grimm_hf_envelope": profile_grimm_hf_envelope,
    "mittelholz_like": profile_mittelholz_like,
    "hood_upper_resistive": profile_hood_upper_bound,
    "nearside_warm": profile_nearside_warm,
    "farside_cold": profile_farside_cold,
    "pkt": profile_pkt,
}


def all_literature_profiles() -> list[ConductivityProfile]:
    return [fn() for fn in LITERATURE_PROFILES.values()]


def save_literature_profiles(out_dir: Path | None = None) -> list[Path]:
    out = Path(out_dir) if out_dir else DATA
    out.mkdir(parents=True, exist_ok=True)
    paths = []
    for p in all_literature_profiles():
        path = out / f"{p.name}.csv"
        p.to_csv(path)
        paths.append(path)
    # also write Grimm formula reference table
    LIT.mkdir(parents=True, exist_ok=True)
    z = np.array([0, 50, 80, 200, 400, 600, 800, 1000, 1200, 1400])
    ref = np.column_stack([z, grimm_lf_sigma(z), profile_grimm_lf_preferred().sigma_at(R_MOON - z * 1e3)])
    np.savetxt(
        LIT / "grimm_lf_reference_table.csv",
        ref,
        delimiter=",",
        header="depth_km,grimm_lf_formula_S_m,preferred_with_lid_S_m",
        comments="",
    )
    (LIT / "SOURCES.md").write_text(
        """# Literature profile sources

## Grimm LF (preferred)
- Grimm, R.E. (2023/2024). Lunar mantle structure… Apollo 12–Explorer 35.
  arXiv:2305.01462 / Icarus.
- Analytic fit (400–1200 km): σ = 1.76×10⁻⁴ exp(z_km/210) S/m
- Near-surface bound: Dyal & Parkin (1977) σ < 10⁻⁸ S/m for z < 80 km
- PDF cached: grimm_2023_arxiv2305.01462.pdf (if download succeeded)

## Mittelholz-like
- Inspired by Mittelholz et al. (2021), JGR Planets — global LP orbital sounding.
- **Constructed envelope**, not a digitization of their published figure.
- Use for global-average comparison against Grimm Apollo-site 1-D.

## Regional
- Nearside / farside / PKT: order-of-magnitude thermal asymmetry variants
  for lateral-path and two-hemisphere experiments (not inverted data products).
"""
    )
    return paths
