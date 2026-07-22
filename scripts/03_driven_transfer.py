#!/usr/bin/env python3
"""Driven / source–receiver transfer proxies (path + impedance)."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lunar_elf.constants import R_MOON  # noqa: E402
from lunar_elf.profiles import all_lunar_profiles, profile_nominal_mittelholz_like  # noqa: E402
from lunar_elf.skin import effective_shell_sigma, path_attenuation_db  # noqa: E402
from lunar_elf.sphere.impedance import (  # noqa: E402
    cavity_q_from_impedances,
    ideal_schumann_freq,
    ionosphere_impedance,
    profile_surface_impedance,
)

OUT = ROOT / "results" / "phase1"
FIG = ROOT / "paper_figs"
OUT.mkdir(parents=True, exist_ok=True)


def geometric_spreading_db(theta_rad: np.ndarray) -> np.ndarray:
    s = np.sin(np.clip(theta_rad, 1e-3, np.pi - 1e-3))
    ref = np.sin(np.deg2rad(10.0))
    return -10.0 * np.log10(s / ref)


def main() -> None:
    freqs = np.logspace(0, 2, 60)
    thetas_deg = np.array([10.0, 30.0, 60.0, 90.0, 120.0, 180.0])

    # Path-based transfer for all profiles
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    for prof in all_lunar_profiles():
        sig = effective_shell_sigma(prof, 3e5)
        L = R_MOON * np.deg2rad(90.0)
        att = path_attenuation_db(L, freqs, sig)
        ax.semilogx(freqs, -att, label=prof.name, lw=2)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Transmission (dB) over 90° great-circle arc")
    ax.set_title("Source–receiver transfer proxy (shell path attenuation)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig_transfer_90deg.png", dpi=160)
    fig.savefig(OUT / "fig_transfer_90deg.png", dpi=160)
    plt.close(fig)

    # Angular map for nominal profile
    prof = profile_nominal_mittelholz_like()
    sig = effective_shell_sigma(prof, 3e5)
    f_list = [1.0, 3.0, 10.0, 30.0]
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    for f in f_list:
        Larc = R_MOON * np.deg2rad(thetas_deg)
        att = path_attenuation_db(Larc, f, sig)
        geo = geometric_spreading_db(np.deg2rad(thetas_deg))
        ax.plot(thetas_deg, -(att + geo), "o-", label=f"{f:g} Hz", lw=2)
    ax.set_xlabel("Angular separation (deg)")
    ax.set_ylabel("Relative field level (dB, ref. geom. at 10°)")
    ax.set_title(f"Angular transfer — nominal (σ_eff={sig:.2e} S/m)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG / "fig_transfer_vs_angle.png", dpi=160)
    plt.close(fig)

    # Impedance-based "driven" cavity response proxy: 1/|Zg+Zi| vs f (Model B)
    freqs_lin = np.linspace(1, 80, 120)
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    for prof in all_lunar_profiles():
        resp = []
        for f in freqs_lin:
            zg = profile_surface_impedance(prof, float(f))
            zi = ionosphere_impedance(float(f), 1e-5)
            resp.append(1.0 / abs(zg.Z + zi))
        resp = np.array(resp)
        ax.plot(freqs_lin, resp / (resp.max() + 1e-30), label=prof.name, lw=2)
    ax.axvline(ideal_schumann_freq(1, R_MOON), color="k", ls=":", alpha=0.5, label="ideal f₁")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Normalized 1/|Z_g+Z_i|")
    ax.set_title("Model B driven proxy (admittance of cavity walls)")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG / "fig_driven_multipoles.png", dpi=160)
    plt.close(fig)

    # Ringing times from q_table
    q_path = OUT / "q_table.csv"
    print("Driven transfer figures written.")
    if q_path.exists():
        print("\nRinging time estimates (τ ≈ Q / (π f)), Model B n=1:")
        with q_path.open() as fh:
            for row in csv.DictReader(fh):
                if row["model"] != "B_closed" or int(float(row["n"])) != 1:
                    continue
                q = float(row["Q"])
                f = float(row["f_hz"])
                tau = q / (np.pi * f)
                print(f"  {row['profile']:18s}  Q≈{q:.3g}  f≈{f:.1f} Hz  τ_ring≈{tau*1e3:.2f} ms")


if __name__ == "__main__":
    main()
