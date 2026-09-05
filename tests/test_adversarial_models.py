"""Independent regression targets for known model defects at d939c366.

Strict expected failures preserve the baseline and make each unresolved issue
visible; a source correction must remove the corresponding xfail marker.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lunar_elf.constants import MU0
from lunar_elf.profiles import ConductivityProfile, profile_homogeneous
from lunar_elf.skin import effective_shell_sigma
from lunar_elf.sphere.cavity import estimate_q_from_spectrum
from lunar_elf.sphere.eigenmodes import cavity_characteristic, find_mode_real_axis_q
from lunar_elf.sphere.energy_q import path_q_proxy
from lunar_elf.sphere.impedance import cavity_q_from_impedances
from lunar_elf.sphere.layers import k_complex


@pytest.mark.xfail(strict=True, reason="M2: cavity wall formula omits half the total stored energy")
def test_thin_cavity_q_matches_independent_tem_energy_balance():
    f, height, ground_R, upper_R = 10., 1e5, .01, .01
    stored_energy_per_area = MU0 * height / 2  # peak magnetic field 1 A/m
    wall_power_per_area = (ground_R + upper_R) / 2
    expected = 2 * np.pi * f * stored_energy_per_area / wall_power_per_area
    actual = cavity_q_from_impedances(f, height, ground_R, upper_R)["Q"]
    assert actual == pytest.approx(expected)


@pytest.mark.xfail(strict=True, reason="M3: dielectric phase constant cannot upper-bound conductive beta/(2 alpha)")
def test_claimed_path_q_bound_contains_same_material_propagation_ratio():
    f, sigma, eps_r = 10., 1e-5, 5.5
    k = k_complex(2 * np.pi * f, sigma, eps_r)
    claimed_upper = path_q_proxy(sigma, f, 1e6, eps_r)["Q_path_upper"]
    assert claimed_upper >= k.real / (-2 * k.imag)


@pytest.mark.xfail(strict=True, reason="M4: shell log mean weights sample count instead of physical depth")
def test_effective_sigma_invariant_under_exact_profile_resampling():
    def profile(z):
        z = np.asarray(z) * 3e5
        return ConductivityProfile("same", "same log-linear profile", (3e5 - z)[::-1],
                                   np.exp(np.log(1e-8) + z / 3e5 * np.log(1e4))[::-1],
                                   np.full(len(z), 5.5), 3e5)
    coarse = profile([0, .5, 1])
    dense_surface = profile([0, .05, .1, .5, 1])
    assert effective_shell_sigma(coarse) == pytest.approx(effective_shell_sigma(dense_surface))


@pytest.mark.xfail(strict=True, reason="M1: monotonic wall admittance endpoint is reported as an eigenmode")
def test_eigenmode_diagnostic_rejects_unbracketed_scan_endpoint():
    try:
        mode = find_mode_real_axis_q(profile_homogeneous(), 1, f_span=(5, 60))
    except ValueError:
        return  # valid future behavior: explicitly reject missing resonance
    assert 5 < mode.f_hz.real < 60


@pytest.mark.xfail(strict=True, reason="M5: amplitude FWHM uses half amplitude instead of half power")
def test_amplitude_lorentzian_recovers_known_half_power_q():
    frequencies = np.linspace(9, 11, 40001)
    amplitude = 1 / np.sqrt(1 + (200 * (frequencies / 10 - 1))**2)
    fit = estimate_q_from_spectrum(frequencies, amplitude, n_peaks=1)[0]
    assert fit["Q"] == pytest.approx(100, rel=.001)


@pytest.mark.xfail(strict=True, reason="M6: computed ionosphere impedance is unused in characteristic")
def test_cavity_characteristic_responds_to_upper_wall_conductivity():
    profile = profile_homogeneous(sigma=1e-10)
    low = cavity_characteristic(profile, 1, 10, sigma_iono=1e-8)
    high = cavity_characteristic(profile, 1, 10, sigma_iono=1e-2)
    assert abs(low - high) > 1e-12
