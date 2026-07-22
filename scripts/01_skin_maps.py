#!/usr/bin/env python3
"""Phase 0: skin depth, loss tangent, path attenuation tables + figures."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lunar_elf.constants import R_MOON  # noqa: E402
from lunar_elf.profiles import all_lunar_profiles  # noqa: E402
from lunar_elf.skin import (  # noqa: E402
    circumferential_path_m,
    loss_tangent,
    path_attenuation_db,
    regime_label,
    shell_metrics,
    skin_depth,
)
from lunar_elf.sphere.energy_q import path_q_proxy  # noqa: E402

OUT = ROOT / "results" / "phase0"
FIG = ROOT / "paper_figs"
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)

FREQS = np.array([1.0, 3.0, 10.0, 30.0, 100.0])


def main() -> None:
    profiles = all_lunar_profiles()
    rows = []
    summary = {}

    for prof in profiles:
        m = shell_metrics(prof, FREQS, shell_depth_m=3e5)
        summary[prof.name] = {
            "sigma_eff_S_m": m["sigma_eff"],
            "eps_r_eff": m["eps_r_eff"],
            "shell_depth_km": 300.0,
        }
        for i, f in enumerate(FREQS):
            tan = float(m["loss_tangent"][i])
            pq = path_q_proxy(m["sigma_eff"], f, circumferential_path_m(R_MOON), m["eps_r_eff"])
            row = {
                "profile": prof.name,
                "f_hz": float(f),
                "sigma_eff": m["sigma_eff"],
                "skin_depth_km": float(m["skin_depth_km"][i]),
                "loss_tangent": tan,
                "regime": regime_label(tan),
                "att_half_circ_db": float(m["att_half_circ_db"][i]),
                "att_full_circ_db": float(m["att_full_circ_db"][i]),
                "Q_path_upper": pq["Q_path_upper"],
            }
            rows.append(row)
            print(
                f"{prof.name:18s} f={f:6.1f} Hz  δ={row['skin_depth_km']:8.1f} km  "
                f"tanδ={tan:9.2e}  ({row['regime']})  "
                f"A_½circ={row['att_half_circ_db']:8.1f} dB  Q≲{row['Q_path_upper']:.3g}"
            )

    # CSV
    import csv

    csv_path = OUT / "shell_metrics.csv"
    with csv_path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {csv_path}")

    with (OUT / "summary.json").open("w") as fh:
        json.dump(summary, fh, indent=2)

    # --- Figure: σ(r) profiles ---
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    for prof in profiles:
        ax.semilogy(prof.depth_km(), prof.sigma, label=prof.name, lw=2)
    ax.set_xlabel("Depth (km)")
    ax.set_ylabel("Electrical conductivity σ (S/m)")
    ax.set_title("Lunar conductivity profiles (literature-bracketed suite)")
    ax.set_xlim(0, 1000)
    ax.set_ylim(1e-9, 1e0)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig_sigma_profiles.png", dpi=160)
    fig.savefig(OUT / "fig_sigma_profiles.png", dpi=160)
    plt.close(fig)

    # --- Figure: skin depth vs frequency ---
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    f_dense = np.logspace(0, 2, 80)
    for prof in profiles:
        m = shell_metrics(prof, f_dense, 3e5)
        ax.loglog(f_dense, m["skin_depth_km"], label=f"{prof.name} (σ_eff={m['sigma_eff']:.1e})", lw=2)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Skin depth δ (km)  [outer 300 km log-mean σ]")
    ax.set_title("ELF skin depth in the lunar outer shell")
    ax.axhline(R_MOON / 1e3, color="k", ls="--", alpha=0.4, label="R_Moon")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(FIG / "fig_skin_depth.png", dpi=160)
    fig.savefig(OUT / "fig_skin_depth.png", dpi=160)
    plt.close(fig)

    # --- Figure: loss tangent ---
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    for prof in profiles:
        m = shell_metrics(prof, f_dense, 3e5)
        ax.loglog(f_dense, m["loss_tangent"], label=prof.name, lw=2)
    ax.axhline(1.0, color="k", ls="--", alpha=0.5, label="σ = ωε boundary")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel(r"Loss tangent $\tan\delta = \sigma/(\omega\varepsilon)$")
    ax.set_title("Conduction vs displacement current (outer shell)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig_loss_tangent.png", dpi=160)
    fig.savefig(OUT / "fig_loss_tangent.png", dpi=160)
    plt.close(fig)

    # --- Figure: path attenuation ---
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    for prof in profiles:
        m = shell_metrics(prof, f_dense, 3e5)
        ax.semilogx(f_dense, m["att_half_circ_db"], label=prof.name, lw=2)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Field attenuation over ½ circumference (dB)")
    ax.set_title("Circumferential path attenuation (constant-σ_eff shell proxy)")
    ax.set_ylim(0, None)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig_path_attenuation.png", dpi=160)
    fig.savefig(OUT / "fig_path_attenuation.png", dpi=160)
    plt.close(fig)

    # depth-resolved δ at 10 Hz
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    f0 = 10.0
    for prof in profiles:
        d = skin_depth(f0, prof.sigma) / 1e3
        ax.semilogy(prof.depth_km(), d, label=prof.name, lw=2)
    ax.set_xlabel("Depth (km)")
    ax.set_ylabel("Local skin depth δ (km) at 10 Hz")
    ax.set_title("Depth-resolved skin depth at 10 Hz")
    ax.set_xlim(0, 1000)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig_skin_vs_depth.png", dpi=160)
    plt.close(fig)

    print(f"Figures → {FIG}")


if __name__ == "__main__":
    main()
