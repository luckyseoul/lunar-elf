#!/usr/bin/env python3
"""
Heavy local campaign on Soulkiller — designed to run unattended.

Sweeps (parallel over workers):
  1. Monte Carlo σ(r) envelope → impedance cavity Q distribution (Model B)
  2. Dense (profile × h_iono × σ_iono × n × f) grid
  3. Path-attenuation / transfer maps over f × angle for all profiles + MC draws
  4. Writes progress JSON + final tables under results/campaign/

Usage:
  python scripts/05_heavy_campaign.py [--workers N] [--mc N] [--quick]
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lunar_elf.constants import R_MOON  # noqa: E402
from lunar_elf.profiles import (  # noqa: E402
    LUNAR_PROFILES,
    ConductivityProfile,
    all_lunar_profiles,
    build_lunar_profile,
)
from lunar_elf.skin import (  # noqa: E402
    circumferential_path_m,
    effective_shell_sigma,
    path_attenuation_db,
)
from lunar_elf.sphere.energy_q import path_q_proxy  # noqa: E402
from lunar_elf.sphere.impedance import (  # noqa: E402
    cavity_q_from_impedances,
    ideal_schumann_freq,
    ionosphere_impedance,
    profile_surface_impedance,
)

OUT = ROOT / "results" / "campaign"
OUT.mkdir(parents=True, exist_ok=True)
PROGRESS = OUT / "progress.json"
LOG = OUT / "campaign.log"


def log(msg: str) -> None:
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG.open("a") as fh:
        fh.write(line + "\n")


def write_progress(**kwargs) -> None:
    data = {}
    if PROGRESS.exists():
        try:
            data = json.loads(PROGRESS.read_text())
        except Exception:
            data = {}
    data.update(kwargs)
    data["updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    PROGRESS.write_text(json.dumps(data, indent=2, default=float))


# ---------------------------------------------------------------------------
# Monte Carlo profile generation
# ---------------------------------------------------------------------------

def mc_profile(seed: int) -> ConductivityProfile:
    """Draw a literature-bracketed synthetic profile.

    log10 σ hinges sampled between optimistic and pessimistic envelopes.
    """
    rng = np.random.default_rng(seed)
    # surface, mid (~300 km), deep (~800 km) in log space
    log_surf = rng.uniform(-8.0, -5.0)
    log_mid = rng.uniform(log_surf, -3.5)
    log_deep = rng.uniform(max(log_mid, -4.0), -1.5)
    eps = float(rng.uniform(4.0, 7.5))
    return build_lunar_profile(
        name=f"mc_{seed:05d}",
        description=f"MC draw seed={seed}",
        sigma_surf=10**log_surf,
        sigma_mid=10**log_mid,
        sigma_deep=10**log_deep,
        eps_crust=eps,
        eps_mantle=eps + 1.5,
        n=200,
    )


def _q_for_profile_pack(args: tuple) -> dict:
    """Worker: Model B Q for n=1..3, dense Q(f), path maps — intentionally fat."""
    kind, payload = args
    try:
        if kind == "named":
            name = payload
            prof = LUNAR_PROFILES[name]()
        elif kind == "mc":
            seed = int(payload)
            prof = mc_profile(seed)
        else:
            raise ValueError(kind)

        h = 100e3
        sig_i = 1e-5
        n_layers = 120  # thicker stack → more work per call
        rows_q = []
        for n in (1, 2, 3):
            f = ideal_schumann_freq(n, R_MOON)
            zg = profile_surface_impedance(prof, f, n_layers=n_layers)
            zi = ionosphere_impedance(f, sig_i)
            qi = cavity_q_from_impedances(f, h, zg.Z, zi)
            sig_eff = effective_shell_sigma(prof, 3e5)
            pq = path_q_proxy(sig_eff, f, circumferential_path_m(R_MOON), float(np.mean(prof.eps_r)))
            rows_q.append(
                {
                    "profile": prof.name,
                    "kind": kind,
                    "n": n,
                    "f_hz": f,
                    "Q": qi["Q"],
                    "Re_Zg": qi["Re_Zg"],
                    "Re_Zi": qi["Re_Zi"],
                    "Q_path_upper": pq["Q_path_upper"],
                    "sigma_eff": sig_eff,
                    "sigma_surf": float(prof.sigma[-1]),
                    "delta_top_km": zg.delta_km,
                }
            )

        # dense Q(f) curve (stored only summary stats for MC to keep CSV small)
        freqs = np.logspace(0, 2, 48)  # 1–100 Hz
        qf = []
        for f in freqs:
            zg = profile_surface_impedance(prof, float(f), n_layers=n_layers)
            zi = ionosphere_impedance(float(f), sig_i)
            qi = cavity_q_from_impedances(float(f), h, zg.Z, zi)
            qf.append(qi["Q"])
        qf = np.asarray(qf, dtype=float)
        qf_summary = {
            "profile": prof.name,
            "kind": kind,
            "Qf_min": float(np.min(qf)),
            "Qf_max": float(np.max(qf)),
            "Qf_med": float(np.median(qf)),
            "Q_at_10Hz": float(qf[np.argmin(np.abs(freqs - 10.0))]),
            "Q_at_f1": float(rows_q[0]["Q"]),
        }

        # path att grid
        sig_eff = effective_shell_sigma(prof, 3e5)
        path_rows = []
        for f in (1.0, 3.0, 10.0, 30.0, 100.0):
            for ang in (10.0, 30.0, 60.0, 90.0, 120.0, 180.0):
                L = R_MOON * np.deg2rad(ang)
                att = float(path_attenuation_db(L, f, sig_eff))
                path_rows.append(
                    {
                        "profile": prof.name,
                        "kind": kind,
                        "f_hz": f,
                        "angle_deg": ang,
                        "att_db": att,
                        "sigma_eff": sig_eff,
                    }
                )
        return {
            "ok": True,
            "q": rows_q,
            "path": path_rows,
            "qf": qf_summary,
            "profile": prof.name,
        }
    except Exception as e:
        return {"ok": False, "error": f"{e}\n{traceback.format_exc()}", "payload": str(payload)}


def _iono_sens_pack(args: tuple) -> dict:
    """Worker: (profile_name, h_km, sigma_iono, n) → Q."""
    name, h_km, sig_i, n = args
    try:
        prof = LUNAR_PROFILES[name]()
        f = ideal_schumann_freq(int(n), R_MOON)
        zg = profile_surface_impedance(prof, f, n_layers=60)
        zi = ionosphere_impedance(f, float(sig_i))
        qi = cavity_q_from_impedances(f, float(h_km) * 1e3, zg.Z, zi)
        return {
            "ok": True,
            "row": {
                "profile": name,
                "h_km": h_km,
                "sigma_iono": sig_i,
                "n": n,
                "f_hz": f,
                "Q": qi["Q"],
                "Re_Zg": qi["Re_Zg"],
                "Re_Zi": qi["Re_Zi"],
            },
        }
    except Exception as e:
        return {"ok": False, "error": str(e), "args": args}


def _write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    keys = list(rows[0].keys())
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def run_pool(tasks: list, worker, workers: int, label: str) -> list:
    results = []
    n = len(tasks)
    done = 0
    t0 = time.time()
    log(f"{label}: {n} tasks, workers={workers}")
    write_progress(phase=label, total=n, done=0, status="running")

    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(worker, t): t for t in tasks}
        for fut in as_completed(futs):
            results.append(fut.result())
            done += 1
            if done % max(1, n // 20) == 0 or done == n:
                elapsed = time.time() - t0
                rate = done / elapsed if elapsed > 0 else 0
                eta = (n - done) / rate if rate > 0 else 0
                log(f"  {label}: {done}/{n}  ({100*done/n:.0f}%)  {rate:.1f}/s  ETA {eta:.0f}s")
                write_progress(
                    phase=label,
                    total=n,
                    done=done,
                    rate_per_s=rate,
                    eta_s=eta,
                    status="running",
                    elapsed_s=elapsed,
                )
    log(f"{label}: finished in {time.time()-t0:.1f}s")
    return results


def make_summary_figures(mc_q_rows: list[dict], iono_rows: list[dict]) -> None:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:
        log(f"matplotlib unavailable for campaign figs: {e}")
        return

    figdir = ROOT / "paper_figs"
    figdir.mkdir(exist_ok=True)

    # MC Q histogram n=1
    q1 = [r["Q"] for r in mc_q_rows if int(r["n"]) == 1 and np.isfinite(r["Q"])]
    if q1:
        fig, ax = plt.subplots(figsize=(7.2, 4.5))
        ax.hist(q1, bins=40, color="C0", edgecolor="k", alpha=0.85)
        ax.axvline(np.median(q1), color="C3", ls="--", label=f"median={np.median(q1):.3g}")
        ax.axvline(np.percentile(q1, 95), color="C2", ls=":", label=f"p95={np.percentile(q1,95):.3g}")
        ax.set_xlabel("Cavity Q (Model B, n=1, h=100 km)")
        ax.set_ylabel("MC count")
        ax.set_title(f"Monte Carlo lunar cavity Q (N={len(q1)} draws)")
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(figdir / "fig_mc_Q_hist.png", dpi=150)
        fig.savefig(OUT / "fig_mc_Q_hist.png", dpi=150)
        plt.close(fig)

        # Q vs sigma_eff
        se = [r["sigma_eff"] for r in mc_q_rows if int(r["n"]) == 1]
        qq = [r["Q"] for r in mc_q_rows if int(r["n"]) == 1]
        fig, ax = plt.subplots(figsize=(7.2, 4.5))
        ax.scatter(se, qq, s=8, alpha=0.4)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("σ_eff outer 300 km (S/m)")
        ax.set_ylabel("Cavity Q (n=1)")
        ax.set_title("MC: cavity Q vs outer-shell conductivity")
        ax.grid(True, which="both", alpha=0.3)
        fig.tight_layout()
        fig.savefig(figdir / "fig_mc_Q_vs_sigma.png", dpi=150)
        plt.close(fig)

    # iono sensitivity heatmap for nominal n=1
    if iono_rows:
        nom = [r for r in iono_rows if r["profile"] == "nominal" and int(r["n"]) == 1]
        if nom:
            hs = sorted({r["h_km"] for r in nom})
            ss = sorted({r["sigma_iono"] for r in nom})
            grid = np.full((len(ss), len(hs)), np.nan)
            for r in nom:
                i = ss.index(r["sigma_iono"])
                j = hs.index(r["h_km"])
                grid[i, j] = r["Q"]
            fig, ax = plt.subplots(figsize=(7.2, 4.8))
            im = ax.imshow(grid, origin="lower", aspect="auto", cmap="viridis")
            ax.set_xticks(range(len(hs)))
            ax.set_xticklabels([f"{h:g}" for h in hs])
            ax.set_yticks(range(len(ss)))
            ax.set_yticklabels([f"{s:.0e}" for s in ss])
            ax.set_xlabel("Ionosphere height (km)")
            ax.set_ylabel("σ_iono (S/m)")
            ax.set_title("Nominal Moon: cavity Q vs artificial ionosphere")
            fig.colorbar(im, ax=ax, label="Q")
            fig.tight_layout()
            fig.savefig(figdir / "fig_iono_sensitivity.png", dpi=150)
            plt.close(fig)

    log("Campaign figures written")


def write_campaign_report(mc_q: list[dict], named_q: list[dict], iono: list[dict], path_rows: list[dict]) -> None:
    q1 = [r["Q"] for r in mc_q if int(r["n"]) == 1]
    lines = []
    lines.append("# Heavy campaign results (Soulkiller local)\n\n")
    lines.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    if q1:
        arr = np.array(q1)
        lines.append("## Monte Carlo cavity Q (Model B, n=1, h=100 km)\n\n")
        lines.append(f"- N draws: **{len(arr)}**\n")
        lines.append(f"- median Q: **{np.median(arr):.3g}**\n")
        lines.append(f"- mean Q: **{np.mean(arr):.3g}**\n")
        lines.append(f"- p05 / p95: **{np.percentile(arr,5):.3g}** / **{np.percentile(arr,95):.3g}**\n")
        lines.append(f"- max Q: **{np.max(arr):.3g}**\n")
        lines.append(f"- fraction Q < 1: **{100*np.mean(arr < 1):.1f}%**\n")
        lines.append(f"- fraction Q < 5: **{100*np.mean(arr < 5):.1f}%**\n")
        lines.append(f"- fraction Q < 10: **{100*np.mean(arr < 10):.1f}%**\n\n")
        lines.append(
            "Interpretation: across the literature-bracketed envelope, high-Q "
            "global modes (Q≳10) are essentially absent under Model B; the "
            "physical open Moon (Model A) has no cavity at all.\n\n"
        )

    lines.append("## Named profiles (Model B)\n\n")
    lines.append("| Profile | n | f (Hz) | Q | Re(Zg) | σ_eff |\n|---|---:|---:|---:|---:|---:|\n")
    for r in named_q:
        lines.append(
            f"| {r['profile']} | {r['n']} | {r['f_hz']:.2f} | {r['Q']:.3g} | "
            f"{r['Re_Zg']:.3e} | {r['sigma_eff']:.2e} |\n"
        )

    lines.append("\n## Artifacts\n\n")
    lines.append("- `results/campaign/mc_q.csv`\n")
    lines.append("- `results/campaign/named_q.csv`\n")
    lines.append("- `results/campaign/iono_sensitivity.csv`\n")
    lines.append("- `results/campaign/path_attenuation.csv`\n")
    lines.append("- `results/campaign/progress.json`\n")
    lines.append("- `results/campaign/campaign.log`\n")
    lines.append("- `paper_figs/fig_mc_Q_hist.png`\n")
    lines.append("- `paper_figs/fig_mc_Q_vs_sigma.png`\n")
    lines.append("- `paper_figs/fig_iono_sensitivity.png`\n")

    report = OUT / "CAMPAIGN_REPORT.md"
    report.write_text("".join(lines))
    # also merge key stats into paper/
    (ROOT / "paper" / "CAMPAIGN_REPORT.md").write_text("".join(lines))
    log(f"Wrote {report}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=max(1, min(80, (os.cpu_count() or 8) - 4)))
    ap.add_argument("--mc", type=int, default=2000, help="Monte Carlo profile draws")
    ap.add_argument("--quick", action="store_true", help="Smaller grid for smoke test")
    args = ap.parse_args()

    if args.quick:
        args.mc = min(args.mc, 64)
        workers = min(args.workers, 16)
    else:
        workers = args.workers

    LOG.write_text("")  # reset
    log(f"Campaign start on host={os.uname().nodename} cpus={os.cpu_count()} workers={workers} mc={args.mc}")
    write_progress(status="starting", host=os.uname().nodename, workers=workers, mc=args.mc)

    t_all = time.time()

    # --- Phase A: named + MC profiles ---
    tasks = [("named", name) for name in LUNAR_PROFILES]
    tasks += [("mc", seed) for seed in range(args.mc)]
    results = run_pool(tasks, _q_for_profile_pack, workers, "mc_and_named")

    named_q, mc_q, path_rows, qf_rows = [], [], [], []
    n_fail = 0
    for r in results:
        if not r.get("ok"):
            n_fail += 1
            log(f"FAIL: {r.get('error', r)[:200]}")
            continue
        for row in r["q"]:
            if row["kind"] == "mc":
                mc_q.append(row)
            else:
                named_q.append(row)
        path_rows.extend(r["path"])
        if "qf" in r:
            qf_rows.append(r["qf"])

    _write_csv(OUT / "named_q.csv", named_q)
    _write_csv(OUT / "mc_q.csv", mc_q)
    _write_csv(OUT / "path_attenuation.csv", path_rows)
    _write_csv(OUT / "qf_summary.csv", qf_rows)
    log(f"Q rows: named={len(named_q)} mc={len(mc_q)} path={len(path_rows)} qf={len(qf_rows)} fails={n_fail}")

    # --- Phase B: ionosphere sensitivity dense grid ---
    if args.quick:
        h_list = [50.0, 100.0, 150.0]
        s_list = [1e-6, 1e-5, 1e-4]
        n_list = [1]
        names = list(LUNAR_PROFILES.keys())
    else:
        h_list = [40.0, 50.0, 60.0, 70.0, 80.0, 100.0, 120.0, 150.0, 200.0]
        s_list = [1e-7, 3e-7, 1e-6, 3e-6, 1e-5, 3e-5, 1e-4, 3e-4, 1e-3]
        n_list = [1, 2, 3]
        names = list(LUNAR_PROFILES.keys())

    iono_tasks = [(nm, h, s, n) for nm in names for h in h_list for s in s_list for n in n_list]
    iono_res = run_pool(iono_tasks, _iono_sens_pack, workers, "iono_sensitivity")
    iono_rows = [r["row"] for r in iono_res if r.get("ok")]
    _write_csv(OUT / "iono_sensitivity.csv", iono_rows)
    log(f"Iono rows: {len(iono_rows)}")

    # --- figures + report ---
    make_summary_figures(mc_q, iono_rows)
    write_campaign_report(mc_q, named_q, iono_rows, path_rows)

    elapsed = time.time() - t_all
    write_progress(status="done", elapsed_s=elapsed, mc_q_rows=len(mc_q), iono_rows=len(iono_rows))
    log(f"Campaign COMPLETE in {elapsed:.1f}s  results → {OUT}")

    # compact status for orchestrator
    status = {
        "status": "done",
        "elapsed_s": elapsed,
        "workers": workers,
        "mc_draws": args.mc,
        "mc_q_rows": len(mc_q),
        "iono_rows": len(iono_rows),
        "out": str(OUT),
    }
    if mc_q:
        q1 = np.array([r["Q"] for r in mc_q if int(r["n"]) == 1])
        status["q1_median"] = float(np.median(q1))
        status["q1_p95"] = float(np.percentile(q1, 95))
        status["q1_max"] = float(np.max(q1))
        status["frac_q_lt_5"] = float(np.mean(q1 < 5))
    (OUT / "status.json").write_text(json.dumps(status, indent=2))
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
