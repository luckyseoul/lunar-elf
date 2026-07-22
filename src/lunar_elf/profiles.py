"""Electrical conductivity profiles for Moon (and Earth validation).

Profiles are literature-bracketed synthetics consistent with Apollo-era and
modern inversions (Sonett et al. 1971; Dyal & Parkin 1971; Mittelholz et al.
2021; Grimm 2023/2024). They are *not* digitizations of a single figure, but
log-linear / Arrhenius-style envelopes that span published bounds so Q results
can be stated as ranges rather than point values.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np

from .constants import R_EARTH, R_MOON

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "profiles"


@dataclass(frozen=True)
class ConductivityProfile:
    """Tabulated radial conductivity profile, center → surface."""

    name: str
    description: str
    r: np.ndarray  # m, increasing, from near center to surface
    sigma: np.ndarray  # S/m
    eps_r: np.ndarray  # relative permittivity
    radius: float  # planetary radius m

    def sigma_at(self, r: np.ndarray | float) -> np.ndarray:
        r = np.asarray(r, dtype=float)
        # clamp to tabulated range
        return np.exp(
            np.interp(
                np.clip(r, self.r[0], self.r[-1]),
                self.r,
                np.log(np.clip(self.sigma, 1e-20, None)),
            )
        )

    def eps_r_at(self, r: np.ndarray | float) -> np.ndarray:
        r = np.asarray(r, dtype=float)
        return np.interp(np.clip(r, self.r[0], self.r[-1]), self.r, self.eps_r)

    def depth_km(self) -> np.ndarray:
        return (self.radius - self.r) / 1e3

    def to_csv(self, path: Path | str) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        arr = np.column_stack(
            [
                self.r,
                self.depth_km(),
                self.sigma,
                self.eps_r,
            ]
        )
        header = "r_m,depth_km,sigma_S_m,eps_r"
        np.savetxt(path, arr, delimiter=",", header=header, comments="")


def _arrhenius_sigma(
    T: np.ndarray,
    sigma0: float,
    Ea_eV: float,
) -> np.ndarray:
    """Simple Arrhenius silicate conductivity σ = σ0 exp(-Ea / kT)."""
    k_eV = 8.617333262145e-5
    return sigma0 * np.exp(-Ea_eV / (k_eV * np.clip(T, 1.0, None)))


def _lunar_temperature(depth_m: np.ndarray, T_surf: float = 250.0, T_core: float = 1600.0) -> np.ndarray:
    """Crude radial temperature model (cold lithosphere → warm mantle).

    Not a thermal inversion product — only to shape Arrhenius σ(r) into a
    continuous, physically plausible rise with depth.
    """
    # Lithosphere ~ cool for first ~200–400 km, then rise toward mantle
    z = np.asarray(depth_m, dtype=float)
    # Two-layerish smooth profile
    T = T_surf + (T_core - T_surf) * (1.0 - np.exp(-z / 4.5e5)) ** 1.3
    return T


def _make_radial_grid(radius: float, n: int = 400) -> np.ndarray:
    # denser near surface (log-ish in depth)
    depth = np.geomspace(1.0, radius * 0.999, n)
    r = radius - depth
    r = np.sort(r)
    r[0] = max(r[0], 1e3)  # avoid exact center singularity
    r[-1] = radius
    return r


def build_lunar_profile(
    name: str,
    description: str,
    sigma_surf: float,
    sigma_mid: float,
    sigma_deep: float,
    eps_crust: float = 5.5,
    eps_mantle: float = 8.0,
    n: int = 500,
) -> ConductivityProfile:
    """Piecewise-log conductivity with smooth transitions (depth-controlled)."""
    R = R_MOON
    r = _make_radial_grid(R, n)
    depth = R - r

    # Log-linear hinges at ~50 km, 300 km, 800 km
    z_knots = np.array([0.0, 5e4, 3e5, 8e5, R])
    s_knots = np.array(
        [
            sigma_surf,
            sigma_surf * 1.5,
            sigma_mid,
            sigma_deep,
            min(sigma_deep * 30.0, 1.0),
        ]
    )
    log_s = np.interp(depth, z_knots, np.log(s_knots))
    sigma = np.exp(log_s)

    eps = np.where(depth < 3e5, eps_crust, eps_mantle)
    return ConductivityProfile(name, description, r, sigma, eps.astype(float), R)


def profile_optimistic_cold() -> ConductivityProfile:
    """Best-case resistive outer shell (upper bound for 'dielectric' claims)."""
    return build_lunar_profile(
        name="optimistic_cold",
        description="Cold resistive lithosphere: σ~1e-8–1e-7 S/m outer 200 km; slow rise.",
        sigma_surf=1e-8,
        sigma_mid=3e-7,
        sigma_deep=1e-4,
        eps_crust=4.0,
    )


def profile_nominal_mittelholz_like() -> ConductivityProfile:
    """Nominal envelope consistent with modern orbital inversions.

    Outer shell highly resistive; midmantle rising toward 1e-3–1e-2 S/m class values.
    """
    return build_lunar_profile(
        name="nominal",
        description="Nominal literature-bracketed Moon: outer ~1e-7–1e-6, deeper ~1e-3+.",
        sigma_surf=1e-7,
        sigma_mid=5e-6,
        sigma_deep=3e-3,
        eps_crust=5.5,
    )


def profile_apollo_classic() -> ConductivityProfile:
    """Apollo dual-spacecraft style: very resistive outer hundreds of km."""
    return build_lunar_profile(
        name="apollo_classic",
        description="Apollo-era style: σ ≲ 1e-6–1e-5 through outer few hundred km.",
        sigma_surf=5e-8,
        sigma_mid=1e-6,
        sigma_deep=1e-3,
        eps_crust=5.0,
    )


def profile_pessimistic_warm() -> ConductivityProfile:
    """Warmer / more conductive outer shell (lower-bound Q)."""
    return build_lunar_profile(
        name="pessimistic_warm",
        description="Warmer outer shell: σ~1e-5 near surface class values earlier with depth.",
        sigma_surf=1e-5,
        sigma_mid=1e-4,
        sigma_deep=1e-2,
        eps_crust=7.0,
    )


def profile_homogeneous(sigma: float = 1e-7, eps_r: float = 5.5, n: int = 200) -> ConductivityProfile:
    R = R_MOON
    r = _make_radial_grid(R, n)
    return ConductivityProfile(
        name=f"homogeneous_{sigma:.0e}",
        description=f"Homogeneous Moon σ={sigma:.2e} S/m",
        r=r,
        sigma=np.full_like(r, sigma),
        eps_r=np.full_like(r, eps_r),
        radius=R,
    )


def profile_earth_crust_mantle() -> ConductivityProfile:
    """Very simplified Earth conductivity for Schumann validation floor."""
    R = R_EARTH
    r = _make_radial_grid(R, 300)
    depth = R - r
    # continental-ish: 1e-3 near surface wet, rising then mantle
    z_knots = np.array([0.0, 1e4, 1e5, 4e5, 1e6, R])
    s_knots = np.array([1e-2, 1e-3, 1e-2, 1e-1, 1.0, 1e2])
    sigma = np.exp(np.interp(depth, z_knots, np.log(s_knots)))
    eps = np.full_like(r, 10.0)
    return ConductivityProfile(
        name="earth_simple",
        description="Simplified Earth σ(r) for cavity validation",
        r=r,
        sigma=sigma,
        eps_r=eps,
        radius=R,
    )


LUNAR_PROFILES: dict[str, Callable[[], ConductivityProfile]] = {
    "optimistic_cold": profile_optimistic_cold,
    "nominal": profile_nominal_mittelholz_like,
    "apollo_classic": profile_apollo_classic,
    "pessimistic_warm": profile_pessimistic_warm,
}


def all_lunar_profiles() -> list[ConductivityProfile]:
    return [fn() for fn in LUNAR_PROFILES.values()]


def save_all_profiles(out_dir: Path | str | None = None) -> list[Path]:
    out_dir = Path(out_dir) if out_dir else DATA_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for p in all_lunar_profiles() + [profile_earth_crust_mantle(), profile_homogeneous()]:
        path = out_dir / f"{p.name}.csv"
        p.to_csv(path)
        paths.append(path)
    return paths
