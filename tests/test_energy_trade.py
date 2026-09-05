"""Power conservation and independently known limiting cases of review models."""
import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    'energy_trade', Path(__file__).resolve().parents[1]/'scripts/07_antenna_energy_trade.py')
trade = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trade)


def test_power_conservation_with_non_negligible_receiver_loading():
    tx, rx = trade.loop(100,2.5), trade.loop(100,2.5)
    # Synthetic microohm coils stress loading; not a superconducting design claim.
    tx['resistance_ohm'] = rx['resistance_ohm'] = 1e-6
    r = trade.coupled_power(tx,rx,10,1000,100)
    assert r['load_w'] > 50
    assert r['load_w'] + r['tx_heat_w'] + r['rx_heat_w'] == pytest.approx(100)
    assert r['load_w']/100 == pytest.approx(r['coil_efficiency'])


def test_reciprocity_and_weak_coupling_range_scaling():
    tx,rx = trade.loop(100,2.5),trade.loop(10,10)
    r = trade.coupled_power(tx,rx,10,1000,100)
    reciprocal = trade.coupled_power(rx,tx,10,1000,100)
    distant = trade.coupled_power(tx,rx,10,10000,100)
    assert r['coil_efficiency'] == pytest.approx(reciprocal['coil_efficiency'],abs=0)
    assert r['load_w']/distant['load_w'] == pytest.approx(1e6)


def test_reject_geometry_outside_stated_approximation():
    tx=trade.loop(100,2.5)
    with pytest.raises(ValueError):
        trade.coupled_power(tx,tx,10,100,100)
    with pytest.raises(ValueError):
        trade.coupled_power(tx,tx,30,1e6,100)


def test_airy_first_zero_encloses_approximately_84_percent():
    # First zero of J1: independent textbook aperture benchmark.
    r=trade.beam(1,1,1,2*3.8317059702075125/trade.math.pi,.4,.5)
    assert r['capture_fraction'] == pytest.approx(.837784869173314,rel=1e-12)
    assert 0 < r['ideal_end_to_end_efficiency'] < .2


def test_cable_mass_scaling_in_voltage_and_length():
    a=trade.cable(1000,10000)
    b=trade.cable(2000,10000)
    c=trade.cable(1000,20000)
    assert b['total_copper_kg'] == pytest.approx(4*a['total_copper_kg'])
    assert c['total_copper_kg'] == pytest.approx(a['total_copper_kg']/4)
    assert a['input_w'] == a['load_w']+a['loss_w']
