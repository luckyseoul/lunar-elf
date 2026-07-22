#!/usr/bin/env python3
"""Phase 1: surface-impedance cavity Q (Models A/B/C) — numerically stable."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lunar_elf.constants import R_EARTH, R_MOON  # noqa: E402
from lunar_elf.profiles import all_lunar_profiles, profile_earth_crust_mantle  # noqa: E402
from lunar_elf.skin import circumferential_path_m, effective_shell_sigma  # noqa: E402
from lunar_elf.sphere.energy_q import path_q_proxy  # noqa: E402
from lunar_elf.sphere.impedance import (  # noqa: E402
    earth_schumann_check,
    ideal_schumann_freq,
    ionosphere_impedance,
    profile_surface_impedance,
    schumann_q_suite,
)

OUT = ROOT / "results" / "phase1"
FIG = ROOT / "paper_figs"
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)


def run_open_path_bounds() -> list[dict]:
    rows = []
    for prof in all_lunar_profiles():
        sig = effective_shell_sigma(prof, 3e5)
        for f in (1.0, 3.0, 10.0, 30.0):
            pq = path_q_proxy(sig, f, circumferential_path_m(R_MOON))
            rows.append(
                {
                    "model": "A_open",
                    "profile": prof.name,
                    "n": 0,
                    "f_hz": f,
                    "Q": 0.0,  # no closed cavity
                    "Q_path_upper": pq["Q_path_upper"],
                    "Re_Zg": float("nan"),
                    "Re_Zi": float("nan"),
                    "skin_depth_km": pq["skin_depth_km"],
                    "round_trip_att_db": pq["round_trip_att_db"],
                    "note": "no_ionosphere_no_cavity",
                }
            )
            print(
                f"[A] {prof.name:16s} f={f:5.1f}  δ={pq['skin_depth_km']:.1f} km  "
                f"Q_cavity=0 (open)  Q_path≲{pq['Q_path_upper']:.3g}  "
                f"RT_att={pq['round_trip_att_db']:.1f} dB"
            )
    return rows


def run_closed_suite() -> list[dict]:
    rows = []
    # frequency sweep of Q for n=1 for figures
    freqs = np.linspace(1.0, 80.0, 80)
    q_curves = {}

    for prof in all_lunar_profiles():
        print(f"[B] {prof.name} ...", flush=True)
        suite = schumann_q_suite(
            prof,
            h_iono_m=100e3,
            sigma_iono=1e-5,
            multipoles=(1, 2, 3),
            open_cavity=False,
        )
        sig = effective_shell_sigma(prof, 3e5)
        for s in suite:
            pq = path_q_proxy(sig, s["f_hz"], circumferential_path_m(R_MOON))
            row = {
                "model": "B_closed",
                "profile": prof.name,
                "n": s["n"],
                "f_hz": s["f_hz"],
                "Q": s["Q"],
                "Q_path_upper": pq["Q_path_upper"],
                "Re_Zg": s["Re_Zg"],
                "Re_Zi": s["Re_Zi"],
                "skin_depth_km": s["delta_top_km"],
                "round_trip_att_db": pq["round_trip_att_db"],
                "note": "h=100km_sigma_iono=1e-5",
            }
            rows.append(row)
            print(
                f"     n={s['n']}  f={s['f_hz']:.2f} Hz  "
                f"ReZg={s['Re_Zg']:.3e}  ReZi={s['Re_Zi']:.3e}  "
                f"Q={s['Q']:.3g}  Q_path≲{pq['Q_path_upper']:.3g}"
            )

        # Q(f) curve for n-independent formula (use each f)
        qf = []
        for f in freqs:
            zg = profile_surface_impedance(prof, float(f))
            zi = ionosphere_impedance(float(f), 1e-5)
            from lunar_elf.sphere.impedance import cavity_q_from_impedances

            qi = cavity_q_from_impedances(float(f), 100e3, zg.Z, zi)
            qf.append(qi["Q"])
        q_curves[prof.name] = np.array(qf)

    np.savez_compressed(OUT / "q_vs_freq_B.npz", f=freqs, **q_curves)
    return rows


def run_earth_validation() -> list[dict]:
    prof = profile_earth_crust_mantle()
    print("[C Earth] ...", flush=True)
    suite = earth_schumann_check(prof, h_iono_m=70e3, sigma_iono=1e-4)
    rows = []
    for s in suite:
        row = {
            "model": "C_earth",
            "profile": prof.name,
            "n": s["n"],
            "f_hz": s["f_hz"],
            "Q": s["Q"],
            "Q_path_upper": float("nan"),
            "Re_Zg": s["Re_Zg"],
            "Re_Zi": s["Re_Zi"],
            "skin_depth_km": s["delta_top_km"],
            "round_trip_att_db": float("nan"),
            "note": "h=70km_sigma_iono=1e-4",
        }
        rows.append(row)
        print(
            f"     n={s['n']}  f_ideal={s['f_hz']:.2f} Hz  "
            f"ReZg={s['Re_Zg']:.3e}  Q={s['Q']:.3g}"
        )
    return rows


def run_sensitivity_iono() -> list[dict]:
    """Q vs ionosphere height / conductivity for nominal Moon."""
    from lunar_elf.profiles import profile_nominal_mittelholz_like

    prof = profile_nominal_mittelholz_like()
    rows = []
    f = ideal_schumann_freq(1, R_MOON)
    zg = profile_surface_impedance(prof, f)
    for h_km in (50.0, 70.0, 100.0, 150.0):
        for sig_i in (1e-6, 1e-5, 1e-4, 1e-3):
            zi = ionosphere_impedance(f, sig_i)
            from lunar_elf.sphere.impedance import cavity_q_from_impedances

            qi = cavity_q_from_impedances(f, h_km * 1e3, zg.Z, zi)
            rows.append(
                {
                    "h_km": h_km,
                    "sigma_iono": sig_i,
                    "Q": qi["Q"],
                    "Re_Zg": qi["Re_Zg"],
                    "Re_Zi": qi["Re_Zi"],
                    "f_hz": f,
                }
            )
    with (OUT / "sensitivity_iono.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote ionosphere sensitivity ({len(rows)} rows)")
    return rows


def plot_q_summary(rows: list[dict]) -> None:
    b = [r for r in rows if r["model"] == "B_closed" and int(r["n"]) == 1]
    if not b:
        return
    names = [r["profile"] for r in b]
    q = [r["Q"] for r in b]
    qp = [r["Q_path_upper"] for r in b]

    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    x = np.arange(len(names))
    w = 0.35
    ax.bar(x - w / 2, q, w, label=r"Cavity $Q$ (impedance method, Model B)", color="C0")
    ax.bar(x + w / 2, qp, w, label=r"Shell-path $Q$ upper bound", color="C1")
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=15, ha="right")
    ax.set_ylabel("Quality factor Q (n=1)")
    ax.set_title(
        "Lunar global-mode Q vs conductivity profile\n"
        "Model B: artificial ionosphere at 100 km (physical Moon has none)"
    )
    ax.set_yscale("log")
    ax.axhline(5, color="gray", ls="--", alpha=0.7, label="Earth Schumann Q ~ few–10")
    ax.legend(fontsize=8)
    ax.grid(True, which="both", axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG / "fig_Q_summary.png", dpi=160)
    fig.savefig(OUT / "fig_Q_summary.png", dpi=160)
    plt.close(fig)


def plot_q_vs_freq() -> None:
    path = OUT / "q_vs_freq_B.npz"
    if not path.exists():
        return
    data = np.load(path)
    f = data["f"]
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    for key in data.files:
        if key == "f":
            continue
        ax.semilogy(f, data[key], label=key, lw=2)
    ax.axvline(ideal_schumann_freq(1, R_MOON), color="k", ls=":", alpha=0.5, label="ideal f₁")
    ax.axhline(5, color="gray", ls="--", alpha=0.5)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Cavity Q (impedance method)")
    ax.set_title("Model B: Q(f) for lunar profiles + 100 km ionosphere")
    ax.legend(fontsize=8)
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG / "fig_Q_vs_freq.png", dpi=160)
    plt.close(fig)


def plot_Z_vs_freq() -> None:
    freqs = np.logspace(0, 2, 60)
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    for prof in all_lunar_profiles():
        reZ = [profile_surface_impedance(prof, float(f)).Z.real for f in freqs]
        ax.loglog(freqs, reZ, label=prof.name, lw=2)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel(r"Re$(Z_s)$ (Ω)")
    ax.set_title("Lunar surface impedance (looking down)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig_surface_impedance.png", dpi=160)
    plt.close(fig)


def main() -> None:
    all_rows: list[dict] = []
    all_rows.extend(run_open_path_bounds())
    all_rows.extend(run_closed_suite())
    all_rows.extend(run_earth_validation())
    run_sensitivity_iono()

    keys = [
        "model",
        "profile",
        "n",
        "f_hz",
        "Q",
        "Q_path_upper",
        "Re_Zg",
        "Re_Zi",
        "skin_depth_km",
        "round_trip_att_db",
        "note",
    ]
    csv_path = OUT / "q_table.csv"
    with csv_path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        for r in all_rows:
            w.writerow({k: r.get(k, "") for k in keys})
    print(f"Wrote {csv_path}")

    with (OUT / "q_table.json").open("w") as fh:
        json.dump(all_rows, fh, indent=2, default=float)

    plot_q_summary(all_rows)
    plot_q_vs_freq()
    plot_Z_vs_freq()
    print("Done phase1.")


if __name__ == "__main__":
    main()
