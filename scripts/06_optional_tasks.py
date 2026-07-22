#!/usr/bin/env python3
"""Complete optional tasks: literature profiles, eigenmodes, lateral heterogeneity.

Designed to run unattended on Soulkiller; writes all artifacts under results/optional/.
"""

from __future__ import annotations

import csv
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lunar_elf.literature_profiles import (  # noqa: E402
    LITERATURE_PROFILES,
    all_literature_profiles,
    save_literature_profiles,
)
from lunar_elf.lateral import run_lateral_suite  # noqa: E402
from lunar_elf.skin import effective_shell_sigma, loss_tangent, shell_metrics, skin_depth  # noqa: E402
from lunar_elf.sphere.eigenmodes import eigenmode_suite, riccati_surface_scan  # noqa: E402
from lunar_elf.sphere.impedance import (  # noqa: E402
    cavity_q_from_impedances,
    ideal_schumann_freq,
    ionosphere_impedance,
    profile_surface_impedance,
)
from lunar_elf.constants import R_MOON  # noqa: E402

OUT = ROOT / "results" / "optional"
FIG = ROOT / "paper_figs"
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)
LOG = OUT / "optional.log"


def log(msg: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG.open("a") as fh:
        fh.write(line + "\n")


def _eigen_worker(name: str) -> dict:
    prof = LITERATURE_PROFILES[name]()
    modes = eigenmode_suite(prof, multipoles=(1, 2, 3))
    rows = []
    for m in modes:
        rows.append(
            {
                "profile": name,
                "n": m.n,
                "f_re": float(np.real(m.f_hz)),
                "f_im": float(np.imag(m.f_hz)),
                "Q": m.Q,
                "method": m.method,
            }
        )
    return {"name": name, "rows": rows}


def main() -> None:
    LOG.write_text("")
    t0 = time.time()
    log("=== Optional tasks start ===")

    # ----- 1. Literature profiles -----
    log("Saving literature profiles…")
    paths = save_literature_profiles(ROOT / "data" / "profiles")
    for p in all_literature_profiles():
        d300 = float(p.sigma_at(R_MOON - 3e5))
        d400 = float(p.sigma_at(R_MOON - 4e5))
        d800 = float(p.sigma_at(R_MOON - 8e5))
        log(
            f"  {p.name:22s} σ_surf={p.sigma[-1]:.2e}  "
            f"σ_300={d300:.2e}  σ_400={d400:.2e}  σ_800={d800:.2e}"
        )

    # Phase-0 metrics on literature set
    freqs = np.array([1.0, 3.0, 10.0, 30.0])
    lit_rows = []
    for p in all_literature_profiles():
        m = shell_metrics(p, freqs, 3e5)
        for i, f in enumerate(freqs):
            lit_rows.append(
                {
                    "profile": p.name,
                    "f_hz": float(f),
                    "sigma_eff": m["sigma_eff"],
                    "skin_depth_km": float(m["skin_depth_km"][i]),
                    "loss_tangent": float(m["loss_tangent"][i]),
                    "att_half_circ_db": float(m["att_half_circ_db"][i]),
                }
            )
    with (OUT / "literature_shell_metrics.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(lit_rows[0].keys()))
        w.writeheader()
        w.writerows(lit_rows)

    # σ(r) figure
    fig, ax = plt.subplots(figsize=(7.5, 5.0))
    for p in all_literature_profiles():
        if p.name in ("nearside_warm", "farside_cold", "pkt"):
            ls = "--"
        else:
            ls = "-"
        ax.semilogy(p.depth_km(), p.sigma, label=p.name, lw=2, ls=ls)
    ax.set_xlabel("Depth (km)")
    ax.set_ylabel("σ (S/m)")
    ax.set_title("Literature-anchored lunar conductivity profiles")
    ax.set_xlim(0, 1200)
    ax.set_ylim(1e-10, 1e0)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=7, loc="lower right")
    fig.tight_layout()
    fig.savefig(FIG / "fig_literature_sigma.png", dpi=160)
    fig.savefig(OUT / "fig_literature_sigma.png", dpi=160)
    plt.close(fig)
    log("Literature profiles done")

    # ----- 2. Eigenmode cross-check (parallel over profiles) -----
    log("Eigenmode suite…")
    names = list(LITERATURE_PROFILES.keys())
    eigen_rows = []
    with ProcessPoolExecutor(max_workers=min(7, len(names))) as ex:
        futs = {ex.submit(_eigen_worker, n): n for n in names}
        for fut in as_completed(futs):
            res = fut.result()
            eigen_rows.extend(res["rows"])
            log(f"  eigen {res['name']}: " + ", ".join(f"n={r['n']} Q={r['Q']:.3g}" for r in res["rows"]))

    with (OUT / "eigenmodes.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(eigen_rows[0].keys()))
        w.writeheader()
        w.writerows(eigen_rows)

    # Compare impedance Q bar chart for literature n=1
    n1 = [r for r in eigen_rows if int(r["n"]) == 1]
    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    labels = [r["profile"] for r in n1]
    qs = [r["Q"] for r in n1]
    ax.barh(labels, qs, color="C0")
    ax.axvline(5, color="gray", ls="--", label="Earth Schumann Q~few–10")
    ax.set_xlabel("Cavity Q (n=1, Model B h=100 km)")
    ax.set_title("Eigenmode/impedance cross-check — literature profiles")
    ax.legend(fontsize=8)
    ax.grid(True, axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG / "fig_eigen_Q_literature.png", dpi=160)
    plt.close(fig)

    # Riccati scan diagnostic for grimm preferred
    from lunar_elf.literature_profiles import profile_grimm_lf_preferred

    prof = profile_grimm_lf_preferred()
    fscan = np.linspace(5, 80, 50)
    Labs = riccati_surface_scan(prof, 1, fscan)
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.semilogy(fscan, Labs, lw=2)
    ax.axvline(ideal_schumann_freq(1, R_MOON), color="k", ls=":", label="ideal f₁")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel(r"|L_surface| Riccati")
    ax.set_title("Riccati log-derivative scan — Grimm LF preferred, n=1")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG / "fig_riccati_scan.png", dpi=160)
    plt.close(fig)
    log("Eigenmodes done")

    # ----- 3. Lateral heterogeneity -----
    log("Lateral suite…")
    lat = run_lateral_suite()
    with (OUT / "lateral.json").open("w") as fh:
        json.dump(lat, fh, indent=2, default=float)

    # column table
    col_rows = []
    for name, c in lat["columns"].items():
        col_rows.append(c)
    with (OUT / "lateral_columns.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(col_rows[0].keys()))
        w.writeheader()
        w.writerows(col_rows)

    # path table flatten
    path_rows = []
    for key, val in lat["paths"].items():
        path_rows.append(
            {
                "path": key,
                "f_hz": val["f_hz"],
                "total_att_db": val["total_att_db"],
                "n_segments": len(val["segments"]),
            }
        )
    with (OUT / "lateral_paths.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(path_rows[0].keys()))
        w.writeheader()
        w.writerows(path_rows)

    # hemisphere table
    hemi_rows = []
    for name, h in lat["hemispheres"].items():
        hemi_rows.append({"pair": name, **h})
    with (OUT / "lateral_hemispheres.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(hemi_rows[0].keys()))
        w.writeheader()
        w.writerows(hemi_rows)

    # figures
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    names = [c["name"] for c in col_rows]
    ax.bar(names, [c["Q_n1"] for c in col_rows], color="C2")
    ax.set_ylabel("Regional cavity Q (n=1)")
    ax.set_title("Lateral columns: local 1-D Q under regional σ")
    ax.tick_params(axis="x", rotation=15)
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG / "fig_lateral_Q.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    # att at 10 Hz for different paths
    keys10 = [k for k in lat["paths"] if "10Hz" in k]
    ax.barh(keys10, [lat["paths"][k]["total_att_db"] for k in keys10], color="C3")
    ax.set_xlabel("Path attenuation (dB) at 10 Hz")
    ax.set_title("Great-circle path attenuation — regional segments")
    fig.tight_layout()
    fig.savefig(FIG / "fig_lateral_paths.png", dpi=160)
    plt.close(fig)
    log("Lateral done")

    # ----- Report -----
    lines = []
    lines.append("# Optional tasks — complete\n\n")
    lines.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')} on soulkiller\n\n")

    lines.append("## 1. Literature-anchored profiles\n\n")
    lines.append(
        "Grimm (2023) LF analytic fit σ=1.76×10⁻⁴ exp(z/210) for 400–1200 km, "
        "with Dyal–Parkin resistive lid. Mittelholz-like global envelope "
        "(constructed, not figure-digitized). HF envelope retained as upper bound only.\n\n"
    )
    lines.append("| Profile | σ_eff(0–300 km) | δ(10 Hz) km | tanδ(10 Hz) | A_½circ(10 Hz) dB |\n")
    lines.append("|---|---:|---:|---:|---:|\n")
    for r in lit_rows:
        if float(r["f_hz"]) != 10.0:
            continue
        if r["profile"] in ("nearside_warm", "farside_cold", "pkt"):
            continue
        lines.append(
            f"| {r['profile']} | {r['sigma_eff']:.2e} | {r['skin_depth_km']:.1f} | "
            f"{r['loss_tangent']:.2e} | {r['att_half_circ_db']:.1f} |\n"
        )

    lines.append("\n## 2. Multipole eigenmode / impedance cross-check\n\n")
    lines.append("| Profile | n | Q | notes |\n|---|---:|---:|---|\n")
    for r in eigen_rows:
        lines.append(
            f"| {r['profile']} | {r['n']} | {r['Q']:.3g} | {r['method'][:60]}… |\n"
        )

    lines.append("\n## 3. Lateral heterogeneity (PKT / nearside–farside)\n\n")
    lines.append("### Regional columns\n\n")
    lines.append("| Region | Q_n1 | Re(Zg) | σ_eff | att 90° @10 Hz (dB) |\n|---|---:|---:|---:|---:|\n")
    for c in col_rows:
        lines.append(
            f"| {c['name']} | {c['Q_n1']:.3g} | {c['Re_Zg']:.3e} | "
            f"{c['sigma_eff']:.2e} | {c['att_90deg_10Hz_db']:.1f} |\n"
        )

    lines.append("\n### Two-hemisphere effective Q\n\n")
    lines.append("| Pair | Q_eff | Q_a | Q_b |\n|---|---:|---:|---:|\n")
    for h in hemi_rows:
        lines.append(
            f"| {h['pair']} | {h['Q_eff']:.3g} | {h['Q_a']:.3g} | {h['Q_b']:.3g} |\n"
        )

    lines.append("\n### Path attenuation samples (10 Hz)\n\n")
    for k in keys10:
        lines.append(f"- **{k}**: {lat['paths'][k]['total_att_db']:.1f} dB\n")

    lines.append(
        "\n## Conclusion\n\n"
        "Literature-anchored 1-D profiles, multipole cross-checks, and regional "
        "nearside/farside/PKT experiments all continue to show **no high-Q global "
        "cavity**: open Moon has no ionospheric wall; even with an artificial wall, "
        "Q remains O(1); lateral contrasts change path attenuation but do not create "
        "a high-Q resonator.\n"
    )

    report = OUT / "OPTIONAL_REPORT.md"
    report.write_text("".join(lines))
    (ROOT / "paper" / "OPTIONAL_REPORT.md").write_text("".join(lines))

    status = {
        "status": "done",
        "elapsed_s": time.time() - t0,
        "n_literature_profiles": len(LITERATURE_PROFILES),
        "n_eigen_rows": len(eigen_rows),
        "report": str(report),
    }
    (OUT / "status.json").write_text(json.dumps(status, indent=2))
    log(f"=== COMPLETE in {status['elapsed_s']:.1f}s ===")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
