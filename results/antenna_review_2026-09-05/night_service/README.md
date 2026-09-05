# Night-service optical sensitivity evidence

This is an ideal optics and energy-accounting screen. The 10% availability is an
assumption; no orbit, terrain, eclipse or service availability is established.

Replay from the repository root:

```bash
python scripts/09_night_service_sensitivity.py \
  --out results/antenna_review_2026-09-05/night_service/replay
```

The script integrates the ideal focused Airy intensity across a displaced
receiver disk, doubles radial and angular quadrature resolution, and checks the
centred result against the analytic Bessel encircled-power formula. It also
checks the energy balance of the assumed charge/discharge cycle. These checks
raise an error on failure.

The source was copied to `/tmp/lunar-elf-review-20260905-night/` on NUKA, executed
there with Python 3, NumPy and SciPy, and its JSON/CSV outputs were retrieved.
`local/` records the soulkiller execution; `nuka/` records the separate NUKA
execution. Their assumptions and numerical result sections agree exactly.
`parity.json` records the source and output SHA-256 hashes. Each result also
records runtime hostname, versions, timestamp and source hash.

| Fixed pointing offset at receiver | Capture fraction | Required source DC while charging |
| --- | --- | --- |
| 0 m | 0.682762 | 4.028 kW |
| 0.1 m | 0.674135 | 4.079 kW |
| 0.3 m | 0.608513 | 4.519 kW |
| 0.5 m | 0.493977 | 5.567 kW |
| 1 m | 0.173351 | 15.864 kW |

Parameters: 1.064 µm; 1,000 km range; 1 m transmitter diameter; 1.5 m receiver
diameter; 40% laser efficiency; 50% PV efficiency; 50 W continuous load.
The offsets are fixed errors, not RMS jitter values. Additional optical,
electronic, thermal and platform losses are excluded.

An assumed 18-minute charging window followed by 162 minutes without a beam
requires 550 W receiver DC while charging at 90% storage round-trip efficiency.
The direct load consumes 15 Wh while charging; 150 Wh enters storage and supplies
135 Wh to the load afterward. Minimum usable storage is consequently 135 Wh;
the separate three-hour sizing is 150 Wh. At an assumed usable 150 Wh/kg, these
are 0.9 kg and 1 kg, compared with 118 kg for a 354-hour night.

At zero pointing offset, the thermal budget assigns all laser electrical input
not emitted optically to source heat: 2.417 kW during charging. It assigns all
captured optical power not converted to DC to receiver heat: **up to 550 W**.
Reflection or transmission can reduce that heat without increasing DC output;
conversion efficiency alone does not determine absorption. The ~511 W of beam
power missing the receiver is not receiver heat. Storage has a further 15 Wh
round-trip loss per cycle, whose timing and location require separate
charging/discharging models. Conversion heat is not automatically useful heating.

Useful next checks are a complete charging-cycle power/thermal experiment,
receiver capture under pointing disturbances and nonuniform illumination, and an
actual site/orbit schedule including eclipses, terrain, other users and failures.
