#!/usr/bin/env python3
"""Explicit watts-first screening models; not a lunar Maxwell/thermal solver.

RMS currents and voltages throughout. Loops are isolated, coplanar, circular
single turns with uniform current; receiver and transmitter are small relative
to separation. Exact resonant two-port power balance is used after dipole M.
Beam capture assumes an ideal, range-focused, uniformly illuminated circular
aperture. Converter efficiencies and storage specific energy are assumptions.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import platform
from pathlib import Path

from scipy.special import j0, j1

MU0 = 4 * math.pi * 1e-7
C0 = 299792458.0
R_MOON = 1737400.0
RHO_CU = 1.724e-8  # ohm m, nominal room-temperature IACS value
DENSITY_CU = 8960.0  # kg/m3, engineering assumption


def loop(radius_m: float, wire_mm2: float) -> dict:
    length = 2 * math.pi * radius_m
    section = wire_mm2 * 1e-6
    wire_radius = math.sqrt(section / math.pi)
    return dict(radius_m=radius_m, wire_mm2=wire_mm2,
                length_m=length, area_m2=math.pi * radius_m**2,
                resistance_ohm=RHO_CU * length / section,
                copper_kg=DENSITY_CU * length * section,
                # Thin circular wire external inductance; internal term omitted.
                inductance_h=MU0 * radius_m * (math.log(8*radius_m/wire_radius)-2))


def coupled_power(tx: dict, rx: dict, f_hz: float, distance_m: float,
                  input_w: float) -> dict:
    """Maximum coil-to-load efficiency, ideal lossless tuning, finite loading.

    M=mu0*A1*A2/(4*pi*r^3), equatorial coplanar dipole approximation.
    Rload=R2*sqrt(1+x), x=(omega*M)^2/(R1*R2).
    Source sees R1+(omega*M)^2/(R2+Rload). No amplifier/rectifier credit.
    """
    if distance_m < 5 * max(tx['radius_m'], rx['radius_m']):
        raise ValueError('Dipole screening requires separation >=5 loop radii')
    w = 2 * math.pi * f_hz
    kr = w * distance_m / C0
    if kr > 0.1:
        raise ValueError('Quasistatic screening requires kr <=0.1')
    r1, r2 = tx['resistance_ohm'], rx['resistance_ohm']
    mutual = MU0 / (4*math.pi) * tx['area_m2'] * rx['area_m2'] / distance_m**3
    x = (w*mutual)**2/(r1*r2)
    load = r2 * math.sqrt(1+x)
    reflected = (w*mutual)**2/(r2+load)
    i1sq = input_w/(r1+reflected)
    i2sq = (w*mutual)**2*i1sq/(r2+load)**2
    out = i2sq*load
    # Cancellation-safe version of (sqrt(1+x)-1)/(sqrt(1+x)+1).
    eta = x/(math.sqrt(1+x)+1)**2
    b = MU0*math.sqrt(i1sq)*tx['area_m2']/(4*math.pi*distance_m**3)
    radiation_r = 320*math.pi**4*(tx['area_m2']/(C0/f_hz)**2)**2
    return dict(f_hz=f_hz, distance_m=distance_m, input_w=input_w,
                tx_radius_m=tx['radius_m'], rx_radius_m=rx['radius_m'],
                tx_wire_mm2=tx['wire_mm2'], rx_wire_mm2=rx['wire_mm2'],
                tx_copper_kg=tx['copper_kg'], rx_copper_kg=rx['copper_kg'],
                mutual_h=mutual, coupling_figure_x=x, load_ohm=load,
                tx_current_rms_a=math.sqrt(i1sq), rx_current_rms_a=math.sqrt(i2sq),
                rx_induced_emf_at_loaded_tx_current_rms_v=w*mutual*math.sqrt(i1sq),
                rx_open_circuit_at_fixed_input_rms_v=w*mutual*math.sqrt(input_w/r1),
                load_w=out, coil_efficiency=eta,
                tx_heat_w=i1sq*r1, rx_heat_w=i2sq*r2,
                energy_balance_error_w=input_w-out-i1sq*r1-i2sq*r2,
                rx_field_rms_t=b, tx_radiation_resistance_ohm=radiation_r,
                tx_radiated_w=i1sq*radiation_r,
                tx_q=w*tx['inductance_h']/r1,
                required_r_each_for_50pct_ohm=w*abs(mutual)/math.sqrt(8),
                ka_tx=w*tx['radius_m']/C0, kr=kr)


def beam(wavelength_m: float, distance_m: float, tx_diameter_m: float,
         rx_diameter_m: float, tx_efficiency: float, rx_efficiency: float) -> dict:
    """Scalar diffraction at designed focal range; no pointing/obscuration loss."""
    x = math.pi * tx_diameter_m * (rx_diameter_m/2) / (wavelength_m*distance_m)
    capture = float(1-j0(x)**2-j1(x)**2)
    return dict(wavelength_m=wavelength_m, distance_m=distance_m,
                tx_diameter_m=tx_diameter_m, rx_diameter_m=rx_diameter_m,
                first_null_diameter_m=2.44*wavelength_m*distance_m/tx_diameter_m,
                capture_fraction=capture, tx_conversion_assumed=tx_efficiency,
                rx_conversion_assumed=rx_efficiency,
                ideal_end_to_end_efficiency=capture*tx_efficiency*rx_efficiency,
                input_w_for_100w_load=100/(capture*tx_efficiency*rx_efficiency),
                # A geometric scale, not a validated pointing-error allocation.
                quarter_rx_radius_angle_rad=rx_diameter_m/(8*distance_m))


def cable(distance_m: float, voltage_v: float, input_w: float = 10000,
          loss_fraction: float = 0.05) -> dict:
    """Conductor-only sizing at fixed input current, two-wire return circuit.

    No regolith return assumed. Converters, insulation, minimum mechanical
    gauge, thermal qualification, and voltage-clearance mass are not included.
    """
    section = 2*RHO_CU*distance_m*input_w/(loss_fraction*voltage_v**2)
    return dict(distance_m=distance_m, voltage_v=voltage_v, input_w=input_w,
                conductor_mm2=section*1e6,
                total_copper_kg=2*distance_m*section*DENSITY_CU,
                load_w=input_w*(1-loss_fraction), loss_w=input_w*loss_fraction)


def night_service(load_w: float, duty: float, storage_efficiency: float = .9) -> dict:
    """Energy-only condition; does not establish orbit visibility or cadence.

    The beam directly powers the current load during a pass. Only off-pass
    energy incurs round-trip storage loss. A three-hour gap is an assumed
    sizing case, independent of average duty. Receiver hardware mass excluded.
    """
    receive_w = load_w + load_w*(1-duty)/(storage_efficiency*duty)
    optics = beam(1.064e-6, 1e6, 1, 1.5, .4, .5)
    return dict(load_w=load_w, duty_assumed=duty,
                storage_roundtrip_efficiency_assumed=storage_efficiency,
                receiver_dc_during_pass_w=receive_w,
                source_dc_during_pass_w=receive_w/optics['ideal_end_to_end_efficiency'],
                three_hour_usable_storage_wh=3*load_w,
                three_hour_storage_kg_at_assumed_150whkg=3*load_w/150,
                full_night_storage_kg_at_assumed_150whkg=354*load_w/150,
                assumed_optical_link=optics)


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open('w', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    loops = []
    for f, at, ar, wire, distance in itertools.product(
            [1, 3, 10, 30], [10, 30, 100, 300, 1000], [1, 10, 100],
            [0.5, 2.5, 10, 50, 100], [1000, 3000, 10000, 30000, 100000]):
        if distance < 5*max(at, ar) or 2*math.pi*f*distance/C0 > .1:
            continue
        loops.append(coupled_power(loop(at, wire), loop(ar, wire), f, distance, 100))
    beams = []
    for distance, diameter, receive in itertools.product(
            [10000, 100000, 1000000, 64500000, 384400000], [.1, .3, 1, 10, 100], [1.5, 10]):
        beams.append(beam(1.064e-6, distance, diameter, receive, .4, .5))
    for f, distance, diameter, receive in itertools.product(
            [2.45e9, 5.8e9, 35e9], [10000, 100000, 1000000], [1, 10, 100], [1.5, 10, 100]):
        beams.append(beam(C0/f, distance, diameter, receive, .6, .7))
    cables = [cable(d, v) for d, v in itertools.product([1000, 4000, 10000, 100000, 5e6], [3000, 10000, 100000])]
    stores = [dict(load_w=p, blackout_h=h, usable_specific_energy_wh_per_kg=s,
                   energy_wh=p*h, storage_kg=p*h/s)
              for p,h,s in itertools.product([5,50,100,500], [3,70,100,354], [100,150])]
    examples = [coupled_power(loop(100,2.5), loop(rx,2.5), 10, d, 100)
                for rx,d in itertools.product([10,100], [1000,10000])]
    for name, rows in [('loops',loops),('beams',beams),('cables',cables),('storage',stores)]:
        write_csv(args.out/f'{name}.csv', rows)
    (args.out/'night_service.json').write_text(json.dumps(
        [night_service(p,d) for p,d in itertools.product([5,50,100],[.05,.1,.2,.5])],
        indent=2)+'\n')
    summary = dict(status='screening estimates, not qualified lunar power systems',
                   constants=dict(mu0=MU0,c0=C0,copper_resistivity_ohm_m=RHO_CU,
                                  copper_density_kg_m3=DENSITY_CU),
                   counts=dict(loops=len(loops), beams=len(beams), cables=len(cables), storage=len(stores)),
                   loop_examples=examples,
                   los_range_15m_tx_1m_rx_km=(math.sqrt(2*R_MOON*15)+math.sqrt(2*R_MOON))/1000,
                   limitations=['Loop model excludes Moon, plasma, soil, nearby metal, and AC heating corrections.',
                                'At least 5-radius point-dipole separation: errors quantified by independent quadrature.',
                                '100mm2 wire and30Hz approach copper skin depth: DC losses optimistic.',
                                'No loop signal detectability is counted as harvested power.',
                                'Optical/RF capture is ideal focused diffraction, not terrain/coverage/pointing validation.',
                                'Conversion efficiencies and usable storage density are explicit scenario assumptions.',
                                'Conductor masses exclude insulation, structure, deployment, converters and gauge floor.'])
    (args.out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    metadata=dict(host=platform.node(),platform=platform.platform(),python=platform.python_version(),
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (args.out/'runtime.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(json.dumps(dict(counts=summary['counts'],loop_examples=examples),indent=2))


if __name__ == '__main__':
    main()
