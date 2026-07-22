#!/usr/bin/env python3
"""Build and save conductivity profiles."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lunar_elf.profiles import save_all_profiles, all_lunar_profiles  # noqa: E402


def main() -> None:
    paths = save_all_profiles(ROOT / "data" / "profiles")
    print(f"Wrote {len(paths)} profiles to data/profiles/")
    for p in all_lunar_profiles():
        d = p.depth_km()
        print(
            f"  {p.name:20s}  σ(surf)={p.sigma[-1]:.2e}  "
            f"σ(300km)={float(p.sigma_at(p.radius-3e5)):.2e}  "
            f"σ(800km)={float(p.sigma_at(p.radius-8e5)):.2e}"
        )


if __name__ == "__main__":
    main()
