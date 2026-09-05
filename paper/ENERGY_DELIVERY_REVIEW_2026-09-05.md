# Lunar energy delivery: adversarial review and practical design targets

2026-09-05. Objective: send and receive useful energy, especially at far-side or
dark lunar locations. Four agents reviewed the physics, code, practical
alternatives and numerical evidence. Computation ran on soulkiller, NUKA and
Jellyfin. All four mesh hosts were inventoried; Orin was left available because
these small analytic calculations did not need its ARM/CUDA-specific capabilities.

**Recommendation:** pursue optical charging for isolated far-side instruments,
and cable-fed power stations for fixed local infrastructure. Retain inductive
coupling for the short charging gap at a rover dock. Conventional kilometre-scale
ELF power transfer fails the explicit source-to-load examples by many orders of
magnitude. The existing repository's cavity calculations are not a rigorous
proof against every electromagnetic architecture.

Far side, lunar night and permanently shadowed polar terrain are separate cases.
The far side receives sunlight; being hidden from Earth does not remove local
daytime solar generation. Night requires storage or another available source;
terrain can block an otherwise well-designed beam.

## The decisive delivered-power result

At 10 Hz, put 100 W into a single-turn copper loop of **100 m radius**, with
2.5 mm² wire. It contains 628 m of conductor and 14.1 kg of bare copper. An
identical coplanar receiver 1 km away receives only:

- **51.2 pW** in the magnetic-dipole screening model;
- **53.6 pW** in Jellyfin's independent finite-filament Neumann integration and
  complex two-port circuit solve.

Both allow ideal tuning and the optimum receiving load. Neither includes a
rectifier, driver losses or the lunar environment. The finite-loop calculation
changes the answer by 4.67%, with no practical improvement in usefulness. The
computed 15 pT field can be interesting for sensing while its energy remains
negligible. At 10 km the dipole result drops to **51.2 aW**.

The full screening grid has 1,320 valid loop cases across 1–30 Hz, transmitter
radii 10–1,000 m, receiver radii 1–100 m, wire areas 0.5–100 mm², and separations
1–100 km. Each uses 100 W input and is restricted to separation at least five
loop radii and `kr <= 0.1`. Its largest output is **0.737 µW**, requiring two
100 m radius loops with 100 mm² wire at 1 km and 30 Hz: about **1,126 kg of copper**
in the pair. This is a finite engineering screen, not global optimization or a
universal upper bound.

Adding turns at fixed radius and copper mass increases voltage and resistance
together, leaving the ideal power-transfer figure unchanged. A superconducting
escape is physically conditional: two 100 m radius loops at 1 km and 10 Hz need
total residual AC resistance below roughly **2.19 µΩ per loop** for 50% ideal
efficiency, excluding refrigeration. At 10 km that threshold becomes 2.19 nΩ.
No net-power or mass advantage over a local cable has been established.

Derivations and additional electric-antenna checks:
[physics review](ANTENNA_PHYSICS_REVIEW_2026-09-05.md).

## Viable architectures and their limits

| Situation | Recommended candidate | Quantitative anchor | What remains to establish |
| --- | --- | --- | --- |
| Fixed loads within a few km | Two-conductor high-voltage cable and converters | Relevant 3 km ground systems have been tested; conductor mass/loss can be calculated directly | Flight insulation, deployment, joints, thermal cycling and complete system mass |
| Mobile or inaccessible receiver within line of sight | Laser, tuned photovoltaic receiver, buffer storage | NASA BEACON concept: 3.8 kW laser electrical input for up to 500 W user power at 1–10 km | Pointing, heat rejection, terrain, dust and source availability; this is a concept |
| Sparse far-side science stations during night | Periodic optical charging from lunar orbit | Explicit 50 W night-survival budget below | Actual orbit/site schedule, outages, radiator and spacecraft mass |
| Repeated rover charging at a dock | Cable- or beam-fed short-range inductive coupler | Mutual coupling and measured coil losses determine efficiency | Demonstrate regulated watts across the real gap and misalignment envelope |
| Shadowed polar load near illuminated terrain | Cable baseline; compare mirrors and laser | Sunlight redirection avoids electrical-to-laser conversion | Solar angular extent, final optical aperture, terrain and shadow intervals |

The [alternatives review](ANTENNA_ALTERNATIVES_2026-09-05.md) contains the primary
sources and readiness distinctions. A terrestrial power-beaming demonstration
supports a technology direction; it is not a lunar deployment result.

Microwaves remain possible when large apertures are acceptable. At 5.8 GHz,
10 km, and 10 m transmitting and receiving diameters, the ideal focused circular
aperture model captures 2.28%. With explicitly assumed 60% transmitting and 70%
receiving conversion efficiencies, 100 W delivered needs about **10.4 kW source
DC**, before other losses. Under the optical example at 1.064 µm, a 0.1 m
transmitter and 1.5 m receiver at 10 km need about **514 W** for the same 100 W
load with 40% laser and 50% PV efficiency. These ideal comparisons omit realistic
beam quality and cell packing; they explain why optical transport deserves the
first compact-receiver study.

Neither example sees through the Moon. Even on smooth terrain, a 15 m source
tower and 1 m receiver have a combined horizon of only **9.08 km**. A 10 km
surface link needs favourable topography or extra height. Distant L2 is also not
a compact-aperture shortcut: at 64,500 km, the same optical wavelength with 1 m
transmitter and 1.5 m receiver captures just 0.0295%, requiring **1.70 MW** source
DC for 100 W delivered under the assumed converters. A 10 m transmitter and
10 m receiver improves that ideal budget dramatically, but moves the problem to
large deployed optics, nanoradian pointing and infrastructure mass.

## Development target: an optical night-survival charging service

Use **50 W continuous receiver DC** as a review target, not an inferred user
requirement. Supply daytime energy locally and use orbiting beam stations to
replenish the receiver battery at night. This is an existing engineering concept
that deserves a bounded experiment, not a claim of new physics or originality.
[NASA orbital power study](https://ntrs.nasa.gov/api/citations/20230018143/downloads/PowerBeamingFromLunarOrbitForSmallScienceLanders.pdf)

For an illustrative 18-minute charging pass every three hours:

| Assumption or result | Value |
| --- | ---: |
| Beam availability | 10%, assumed; not an orbit-coverage result |
| Continuous user load | 50 W DC |
| Storage round-trip efficiency | 90%, assumed |
| Receiver DC during charging | **550 W** |
| Transmitting / receiving diameter | 1 m / 1.5 m |
| Wavelength / slant range | 1.064 µm / 1,000 km |
| Ideal centred aperture capture | 68.276% |
| Laser / PV conversion | 40% / 50%, assumed |
| Source DC during charging | **4.028 kW**, before other losses and auxiliaries |
| Laser conversion heat during charging | **2.417 kW** |
| Receiver PV heat allocation during charging | **Up to 550 W**, if all captured non-DC power is absorbed; before storage/converter heat |
| Usable energy for actual 162-minute gap | 135 Wh |
| Usable energy for a conservative three-hour gap | 150 Wh |
| Storage at an assumed usable 150 Wh/kg | **1 kg** for three hours; **118 kg** for a 354-hour night |

The heat budget conservatively assigns all captured optical power not exported
as DC to receiver heat; reflected or transmitted light could reduce that heat.
The concurrent load is powered directly during a pass; only off-pass energy
passes through storage. For duty `d` and storage round-trip efficiency `eta`,

`P_receiver = P_load + P_load*(1-d)/(eta*d)`.

The orbital study provides a useful feasibility comparison, but its spacecraft
are substantial: its three-spacecraft design estimates **3,220 kg per beamcraft**.
Small receiver batteries do not imply a low-mass overall network or an economic
case for one lander. Shared service for several instruments is the relevant
trade. A missed pass, eclipse, bad pointing or a competing user must be included
in the storage schedule.

Pointing matters even before lunar engineering. For the stated optics, a static
0.5 m offset at the receiver (0.5 µrad) reduces capture to about 49.4% and raises
source demand to **5.57 kW**. A 1 m offset raises it to about **15.9 kW**. These
are integrated optical-intensity calculations, not an assumed receiver cutoff.

Three concrete gates make this proposal reviewable:

1. Measure source DC energy, regulated receiver DC energy and stored energy over
   a complete 18-minute-on/162-minute-off cycle supplying a 50 W load. Include
   control power and source/receiver heat. Optical watts alone do not pass.
2. Measure capture and PV conversion with equivalent pointing error, receiver
   angle, nonuniform illumination and contamination. Demonstrate the receiver's
   transient heat rejection during charging.
3. Propagate an orbit and terrain model for one selected far-side site or latitude
   band. Integrate storage state through source eclipses, blocked passes,
   multiple users and at least one missed pass. The current screen does not
   establish this schedule or continuous service.

## Clever extensions worth testing

**Receive heat when heat is the useful product.** An optical absorber feeding a
thermal enclosure can avoid a PV-to-heater conversion. With assumed 40% laser
efficiency and 90% useful absorptance, 100 W useful heat requires `278/F` W source
DC, where `F` is beam capture. A 50%-efficient PV followed by an electric heater
requires `500/F` W under the same assumptions. Electrical load still needs its
own conversion; heat must be controllable at a useful temperature. Alternatively,
route PV waste heat into survival heating and count each joule once. A thermal
store may bridge passes, but its mass and losses need a separate calculation.

**Redirect sunlight locally, with an honest receiver size.** At 5 km the Sun's
approximately 0.0093 rad angular diameter produces a 46.5 m solar image in a
simple focused system. A 10 m final aperture and 1 m receiver have an ideal
brightness-limited receipt around 49 W optical before losses, despite collecting
roughly 107 kW at the mirror. Multiple optics can trade apertures and acceptance,
but cannot remove conservation of radiance. This favours local receiver-area and
thermal-use studies rather than a small distant solar mirror feeding a rover.

**Combine transport and docking.** A stationary optical or cable-fed charging
station can serve a dust-protected inductive interface. This avoids trying to
make one antenna geometry span orbital transport and a repeatedly connected
rover charging port.

## Repository findings and evidence status

The [model audit](MODEL_AUDIT_2026-09-05.md) identifies eight principal findings:
no normalized source-to-load model; circular eigenmode validation; a factor-two
weak-loss Q discrepancy; an invalid path-Q upper bound; sample-density-dependent
conductivity; incorrect amplitude-width Q; an unused upper-boundary impedance;
and overbroad interpretation of an artificial-ionosphere sweep. The repository's
own sensitivity table already reaches **Q=11.63** under different artificial-wall
parameters. That does not establish a buildable ionosphere or useful power.

The audited numerical source began at
`d939c36609a36295d0f3819187baaba95fdcd545`. Remote README work at
`41bd2da0a390f6b9a99ac8f4dc73af2aef6b1e9a` was merged while preserving the local
logo. Milestone **018135f** contains the model audit and remote replay evidence.
The production numerical code and historical paper were preserved, with an
explicit review-status notice in the README.

- **soulkiller:** model counterexamples, 1,320 loop cases, 131 beam cases, 15 cable
  cases, 32 storage cases, and energy-service budgets.
- **NUKA:** independently replayed the original-model diagnostics; all numerical
  values and source digests matched soulkiller. NUKA lacked pytest, which is
  recorded explicitly. The later pointing/service sensitivity has separate
  execution evidence.
- **Jellyfin:** independently integrated complete circular filaments at 256 and
  512 points and solved the complex circuit. Relative quadrature changes were
  at most `2.53e-14` in the five cases; dipole geometry errors are retained.
- **Local tests:** 7 passed, 6 strict expected failures documenting unrepaired
  historical defects. The expected failures are not fixes or successful physical
  validation. New power tests cover strong receiver loading, conservation,
  reciprocity, range scaling, approximation guards and a known Airy benchmark.

## Replay

From the repository root:

```bash
python3 -m pytest -q -rx
python3 scripts/07_antenna_energy_trade.py --out /tmp/lunar-elf-energy-replay
python3 scripts/08_loop_quadrature_check.py --out /tmp/lunar-elf-quadrature.json
python3 scripts/09_night_service_sensitivity.py --out /tmp/lunar-elf-night-replay
sha256sum -c results/antenna_review_2026-09-05/SHA256SUMS.txt
```

The retained evidence is under
[`results/antenna_review_2026-09-05/`](../results/antenna_review_2026-09-05/).
Runtime records identify actual hosts and script hashes. These checks validate
the stated analytic calculations and their reproducibility. Lunar hardware
qualification, an actual orbital service schedule and a full source-driven
lunar electromagnetic solution remain outside the established results.
