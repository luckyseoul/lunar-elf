#!/usr/bin/env python3
"""Ideal optical night-service sensitivity; assumed schedule, not an orbit model.

Replay:
    python scripts/09_night_service_sensitivity.py --out results/night_service

Only NumPy and SciPy are required beyond the standard library. The receiver
integral uses Gauss-Legendre radial quadrature and periodic angular quadrature.
The circular transmitter aperture is uniformly illuminated and phase focused
at a circular receiver normal to the beam. Offset is a fixed transverse aiming
error, not an RMS jitter distribution. Thermal screening assigns all captured
optical power not converted to DC to receiver heat, and all laser electrical
input not emitted optically to source heat. These are explicit conservative heat
allocations, not consequences of conversion efficiencies alone. No
delivered-flight-power claim is made.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import socket
import time

import numpy as np
from numpy.polynomial.legendre import leggauss
import scipy
from scipy.special import j0, j1


def airy_disk_capture(
    offset_m: float,
    wavelength_m: float,
    range_m: float,
    transmitter_diameter_m: float,
    receiver_radius_m: float,
    radial_nodes: int,
) -> float:
    """Integrate normalized focal-plane intensity over an offset receiver disk.

    I(r)/P_optical = pi D_tx^2 / (4 lambda^2 range^2)
                   * [2 J1(pi D_tx r / (lambda range)) / x]^2.

    This normalization integrates to one over the entire focal plane. Receiver
    polar coordinates are centred on the receiver, and shifted from the beam
    centre by offset_m along one transverse axis.
    """
    nodes, weights = leggauss(radial_nodes)
    radius = (nodes + 1.0) * receiver_radius_m / 2.0
    weights = weights * receiver_radius_m / 2.0
    angle_nodes = 4 * radial_nodes
    theta = np.arange(angle_nodes) * (2.0 * np.pi / angle_nodes)
    beam_radius = np.sqrt(
        np.maximum(
            radius[:, None] ** 2
            + offset_m**2
            + 2.0 * radius[:, None] * offset_m * np.cos(theta)[None, :],
            0.0,
        )
    )
    x = np.pi * transmitter_diameter_m * beam_radius / (wavelength_m * range_m)
    amplitude = np.ones_like(x)
    np.divide(2.0 * j1(x), x, out=amplitude, where=x != 0.0)
    intensity = (
        np.pi
        * transmitter_diameter_m**2
        / (4.0 * wavelength_m**2 * range_m**2)
        * amplitude**2
    )
    angular_integral = intensity.mean(axis=1) * (2.0 * np.pi)
    return float(np.dot(weights * radius, angular_integral))


def calculate(radial_nodes: int) -> dict:
    wavelength_m = 1.064e-6
    range_m = 1.0e6
    transmitter_diameter_m = 1.0
    receiver_diameter_m = 1.5
    receiver_radius_m = receiver_diameter_m / 2.0
    load_w = 50.0
    duty_fraction = 0.1
    storage_round_trip_efficiency = 0.9
    laser_efficiency = 0.4
    pv_efficiency = 0.5
    cycle_hours = 3.0
    on_hours = cycle_hours * duty_fraction
    off_hours = cycle_hours * (1.0 - duty_fraction)
    received_dc_w = load_w + load_w * (1.0 - duty_fraction) / (
        duty_fraction * storage_round_trip_efficiency
    )
    optical_received_w = received_dc_w / pv_efficiency
    receiver_pv_heat_w = optical_received_w - received_dc_w
    rows = []
    for offset_m in (0.0, 0.1, 0.3, 0.5, 1.0):
        args = (
            offset_m,
            wavelength_m,
            range_m,
            transmitter_diameter_m,
            receiver_radius_m,
        )
        coarse = airy_disk_capture(*args, radial_nodes)
        fine = airy_disk_capture(*args, 2 * radial_nodes)
        relative_change = abs(fine - coarse) / fine
        if not 0.0 < fine < 1.0 or relative_change > 1.0e-10:
            raise RuntimeError(
                f"Capture quadrature failed at offset={offset_m}: "
                f"coarse={coarse}, fine={fine}, relative_change={relative_change}"
            )
        source_dc_w = received_dc_w / (laser_efficiency * fine * pv_efficiency)
        rows.append(
            {
                "fixed_offset_m": offset_m,
                "fixed_angular_offset_urad": offset_m / range_m * 1.0e6,
                "capture_fraction_n": coarse,
                "capture_fraction_2n": fine,
                "quadrature_relative_change": relative_change,
                "receiver_dc_w_during_on": received_dc_w,
                "source_dc_w_during_on": source_dc_w,
                "transmitted_optical_w_during_on": source_dc_w * laser_efficiency,
                "receiver_optical_w_during_on": optical_received_w,
                "source_laser_heat_w_during_on": source_dc_w * (1.0 - laser_efficiency),
                "receiver_pv_heat_w_during_on": receiver_pv_heat_w,
                "source_dc_wh_per_assumed_cycle": source_dc_w * on_hours,
            }
        )
    x_edge = (
        np.pi * transmitter_diameter_m * receiver_radius_m / (wavelength_m * range_m)
    )
    analytic_center = float(1.0 - j0(x_edge) ** 2 - j1(x_edge) ** 2)
    centered_error = abs(rows[0]["capture_fraction_2n"] - analytic_center)
    if centered_error > 1.0e-12:
        raise RuntimeError(f"Centered analytic capture check failed: {centered_error}")
    energy_into_storage_wh = (received_dc_w - load_w) * on_hours
    usable_off_energy_wh = load_w * off_hours
    energy_balance_error_wh = abs(
        energy_into_storage_wh * storage_round_trip_efficiency - usable_off_energy_wh
    )
    if energy_balance_error_wh > 1.0e-10:
        raise RuntimeError(f"Cycle energy balance failed: {energy_balance_error_wh}")
    usable_specific_energy_wh_kg = 150.0
    return {
        "status": "SCREENING_ONLY_ASSUMED_DUTY_NOT_ORBIT_AVAILABILITY",
        "assumptions": {
            "wavelength_m": wavelength_m,
            "range_m": range_m,
            "transmitter_diameter_m": transmitter_diameter_m,
            "receiver_diameter_m": receiver_diameter_m,
            "constant_load_w": load_w,
            "assumed_duty_fraction": duty_fraction,
            "storage_round_trip_efficiency": storage_round_trip_efficiency,
            "electrical_to_optical_laser_efficiency": laser_efficiency,
            "optical_to_dc_receiver_efficiency": pv_efficiency,
            "assumed_usable_storage_specific_energy_wh_per_kg": usable_specific_energy_wh_kg,
            "direct_load_while_beam_present": True,
            "thermal_allocation": {
                "receiver": (
                    "All captured incident optical power not converted to DC is "
                    "assumed retained as receiver heat. The computed PV heat is an "
                    "upper allocation for that remainder: reflection or transmission "
                    "can lower heat without increasing DC output. Uncaptured beam "
                    "power is not assigned to receiver heat."
                ),
                "source": (
                    "All laser electrical input not emitted optically is assigned "
                    "to source heat for the thermal budget."
                ),
            },
            "source_dc_w_excludes": [
                "spacecraft platform and pointing power",
                "optical path and obscuration losses",
                "cell packing and power management losses",
                "illumination nonuniformity and thermal derating",
                "source energy storage and generation losses",
            ],
            "optical_model": (
                "Scalar ideal circular aperture, uniform illumination, phase focused "
                "at receiver; normal receiver plane; ideal Airy pattern; fixed offset."
            ),
            "availability_not_modeled": [
                "orbital trajectory and eclipses",
                "site terrain and horizon mask",
                "pointing acquisition time and jitter statistics",
                "multiuser beam scheduling",
                "faults and missed passes",
            ],
        },
        "quadrature": {
            "coarse_radial_nodes": radial_nodes,
            "fine_radial_nodes": 2 * radial_nodes,
            "angular_nodes_per_radial_node": 4,
            "relative_convergence_tolerance": 1.0e-10,
            "centered_analytic_tolerance": 1.0e-12,
            "centered_analytic_capture_fraction": analytic_center,
            "centered_analytic_absolute_error": centered_error,
            "maximum_relative_change_n_to_2n": max(
                row["quadrature_relative_change"] for row in rows
            ),
        },
        "assumed_service_cycle": {
            "cycle_hours": cycle_hours,
            "on_minutes": on_hours * 60.0,
            "off_minutes": off_hours * 60.0,
            "receiver_dc_w_during_on": received_dc_w,
            "direct_load_wh_during_on": load_w * on_hours,
            "storage_input_wh_during_on": energy_into_storage_wh,
            "storage_usable_output_wh_during_off": usable_off_energy_wh,
            "storage_round_trip_loss_wh_per_cycle": energy_into_storage_wh
            - usable_off_energy_wh,
            "load_wh_per_cycle": load_w * cycle_hours,
            "energy_balance_absolute_error_wh": energy_balance_error_wh,
            "minimum_storage_usable_wh_for_off_interval": usable_off_energy_wh,
            "minimum_storage_mass_kg_for_off_interval": usable_off_energy_wh
            / usable_specific_energy_wh_kg,
            "three_hour_storage_usable_wh": load_w * 3.0,
            "three_hour_storage_mass_kg": load_w * 3.0 / usable_specific_energy_wh_kg,
            "whole_night_hours": 354.0,
            "whole_night_storage_usable_wh": load_w * 354.0,
            "whole_night_storage_mass_kg": load_w
            * 354.0
            / usable_specific_energy_wh_kg,
            "storage_mass_limitation": (
                "Arithmetic using assumed usable Wh/kg; excludes peripherals and "
                "any thermal or structural mass outside that assumption."
            ),
            "thermal_limitation": (
                "On-state laser/PV conservative heat allocations only, with optical "
                "absorption assumptions stated above; storage heat location is not "
                "assigned because separate charge/discharge efficiencies are unknown."
            ),
        },
        "offset_sensitivity": rows,
        "sources": [
            {
                "title": "Power Beaming from Lunar Orbit for Small Science Landers",
                "url": "https://ntrs.nasa.gov/api/citations/20230018143/downloads/"
                "PowerBeamingFromLunarOrbitForSmallScienceLanders.pdf",
                "use": (
                    "Mission comparison only; this script does not reproduce the "
                    "NASA orbit, beamcraft, or optics model."
                ),
            }
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True, help="Output directory")
    parser.add_argument("--quadrature-n", type=int, default=64, help="Coarse radial nodes")
    args = parser.parse_args()
    if args.quadrature_n < 16:
        parser.error("--quadrature-n must be at least 16")
    started = time.perf_counter()
    result = calculate(args.quadrature_n)
    source_path = Path(__file__).resolve()
    result["provenance"] = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "runtime_hostname": socket.gethostname(),
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "scipy_version": scipy.__version__,
        "source_file_name": source_path.name,
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "computation_elapsed_seconds": time.perf_counter() - started,
    }
    args.out.mkdir(parents=True, exist_ok=True)
    json_path = args.out / "night_service_sensitivity.json"
    json_path.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    csv_path = args.out / "offset_sensitivity.csv"
    rows = result["offset_sensitivity"]
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(
        json.dumps(
            {
                "output": str(json_path),
                "status": result["status"],
                "runtime_hostname": result["provenance"]["runtime_hostname"],
                "source_sha256": result["provenance"]["source_sha256"],
                "centered_capture_fraction": rows[0]["capture_fraction_2n"],
                "centered_source_dc_w": rows[0]["source_dc_w_during_on"],
                "maximum_quadrature_relative_change": result["quadrature"][
                    "maximum_relative_change_n_to_2n"
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
