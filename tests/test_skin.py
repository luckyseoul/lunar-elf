"""Unit tests for Phase 0 skin-depth math."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lunar_elf.skin import loss_tangent, skin_depth


def test_skin_depth_10hz_1e7():
    d = float(skin_depth(10.0, 1e-7))
    assert 4.5e5 < d < 5.5e5  # ~503 km


def test_loss_tangent_conduction_dominated():
    t = float(loss_tangent(10.0, 1e-7, eps_r=5.5))
    assert t > 10.0
