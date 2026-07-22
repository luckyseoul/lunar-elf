"""Physical constants and planetary radii."""

from __future__ import annotations

import numpy as np

# SI
MU0 = 4.0 * np.pi * 1e-7
EPS0 = 8.854187817e-12
C0 = 1.0 / np.sqrt(MU0 * EPS0)  # ≈ 2.9979e8

# Planetary
R_MOON = 1.7374e6  # m
R_EARTH = 6.371e6  # m

# Convenience
KM = 1e3
