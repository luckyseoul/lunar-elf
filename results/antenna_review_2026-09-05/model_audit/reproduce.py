#!/usr/bin/env python3
"""Read-only numerical audit; stdout is JSON. No campaign files are regenerated."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path
import socket
import sys

import numpy as np
import scipy


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path)
    args = parser.parse_args()
    repository = (args.repository if args.repository is not None else Path(__file__).resolve().parents[3]).resolve()
    sys.path.insert(0, str(repository / "src"))

    from lunar_elf.constants import EPS0, MU0, R_MOON
    from lunar_elf.profiles import ConductivityProfile, all_lunar_profiles, profile_homogeneous
    from lunar_elf.skin import effective_shell_sigma, loss_tangent
    from lunar_elf.sphere.cavity import estimate_q_from_spectrum
    from lunar_elf.sphere.eigenmodes import cavity_characteristic, find_mode_real_axis_q
    from lunar_elf.sphere.energy_q import path_q_proxy
    from lunar_elf.sphere.impedance import cavity_q_from_impedances, ideal_schumann_freq
    from lunar_elf.sphere.layers import k_complex

    result = {
        "baseline_git_sha": "d939c36609a36295d0f3819187baaba95fdcd545",
        "host": socket.gethostname(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "source_sha256": {
            str(p.relative_to(repository)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted((repository / "src").rglob("*.py"))
        },
    }
    profiles = []
    for profile in all_lunar_profiles():
        sigma = effective_shell_sigma(profile)
        depths = np.linspace(0, 3e5, 10001)
        depth_mean = np.exp(np.trapezoid(np.log(profile.sigma_at(profile.radius - depths)), depths) / 3e5)
        k = k_complex(2 * np.pi * 10, sigma, 5.5)
        mode = find_mode_real_axis_q(profile, 1)
        profiles.append({
            "profile": profile.name,
            "sigma_eff_unweighted_S_m": sigma,
            "sigma_depth_weighted_log_mean_S_m": float(depth_mean),
            "depth_mean_over_sample_mean": float(depth_mean / sigma),
            "loss_tangent_30Hz": float(loss_tangent(30, sigma, profile.eps_r[-1])),
            "reported_path_Q_upper_10Hz": path_q_proxy(sigma, 10, 1)["Q_path_upper"],
            "same_material_beta_over_2alpha_10Hz": k.real / (-2 * k.imag),
            "reported_cavity_Q": mode.Q,
            "reported_eigenfrequency_real_Hz": mode.f_hz.real,
            "scan_lower_boundary_Hz": 0.3 * ideal_schumann_freq(1, R_MOON),
            "eigenfrequency_is_scan_boundary": bool(np.isclose(mode.f_hz.real, 0.3 * ideal_schumann_freq(1, R_MOON))),
            "method": mode.method,
        })
    result["named_profiles"] = profiles

    # Exact same log-linear physical profile, different tabulation density.
    def resampled(depths):
        z = np.asarray(depths, dtype=float) * 3e5
        return ConductivityProfile("resampled", "identical log-linear depth function", (3e5 - z)[::-1],
                                   np.exp(np.log(1e-8) + (z / 3e5) * np.log(1e4))[::-1],
                                   np.full(len(z), 5.5), 3e5)

    result["sampling_invariance"] = {
        "uniform_grid_sigma_eff": effective_shell_sigma(resampled([0, .5, 1])),
        "surface_dense_sigma_eff": effective_shell_sigma(resampled([0, .05, .1, .5, 1])),
        "exact_depth_log_mean": 1e-6,
    }

    # Independent energy/loss integrals for a weak-loss thin TEM cavity, unit area.
    omega, height, magnetic_amplitude, ground_R, upper_R = 2 * np.pi * 10, 1e5, 1, .01, .01
    energy = .5 * MU0 * height * magnetic_amplitude**2
    power = .5 * (ground_R + upper_R) * magnetic_amplitude**2
    result["tem_energy_balance"] = {
        "f_Hz": 10, "height_m": height, "ground_R_ohm": ground_R, "upper_R_ohm": upper_R,
        "Q_from_total_energy_and_wall_loss": omega * energy / power,
        "Q_repository": cavity_q_from_impedances(10, height, ground_R, upper_R)["Q"],
    }

    # A known narrow resonance: supplied amplitude has half-power width f0/Q.
    frequencies = np.linspace(9, 11, 40001)
    true_Q, f0 = 100, 10
    amplitude = 1 / np.sqrt(1 + (2 * true_Q * (frequencies / f0 - 1))**2)
    result["known_lorentzian_amplitude"] = {
        "true_half_power_Q": true_Q,
        "repository_fit": estimate_q_from_spectrum(frequencies, amplitude, n_peaks=1)[0],
    }

    simple = profile_homogeneous(sigma=1e-10)
    chis = [cavity_characteristic(simple, 1, 10, sigma_iono=s) for s in [1e-8, 1e-2]]
    result["characteristic_ionosphere_sensitivity"] = {
        "sigma_iono_pair_S_m": [1e-8, 1e-2],
        "chi_pair": [[c.real, c.imag] for c in chis],
        "identical": bool(chis[0] == chis[1]),
    }
    try:
        cavity_characteristic(simple, 1, 10 + .1j)
        complex_result = "accepted"
    except Exception as error:
        complex_result = f"{type(error).__name__}: {error}"
    result["complex_frequency_characteristic"] = complex_result
    result["geometric_spreading_10_to_90_deg"] = {
        "physical_cylindrical_field_change_dB": -10 * np.log10(1 / np.sin(np.deg2rad(10))),
        "script_plotted_contribution_dB": 10 * np.log10(1 / np.sin(np.deg2rad(10))),
    }
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
