# Night-charging orbit and site schedule

Nicholas D. Perry
2026-10-01

Gate 3 of the 2026-09-05 energy review remains open. Continuous night service is not established.

## 1. Scope

The open item is an orbit and site schedule for a 50 W night-survival optical charging service. The 2026-09-05 energy review set **50 W continuous receiver DC** as the comparison case, not a measured payload requirement. Its illustrative case assumed **10% beam availability**. That assumption is an 18-minute charge every three hours. It is not an orbit-coverage result. The night-service note in the repository states the same limit: no orbit, terrain, eclipse, or service availability is established.

Gate 3 is still open. It asks for a propagated orbit and terrain model for one selected far-side site or latitude band, with storage integrated through source eclipses, blocked passes, multiple users, and at least one missed pass. The sections below record the load arithmetic already in the repository, quote the orbits and contact statements in the NASA power-beaming papers, and give one geometric example. The geometry is not that propagation.

No contact fraction below is a far-side night charging duty cycle.

## 2. Load and storage budget

Numbers in this section are from `paper/ENERGY_DELIVERY_REVIEW_2026-09-05.md`, `results/antenna_review_2026-09-05/night_service/README.md`, and the 50 W, duty 0.1 row of `results/antenna_review_2026-09-05/energy_trade/night_service.json`, unless marked as arithmetic on those values.

For a constant load served directly while the beam is present, with storage supplying only the gap, the review uses

`P_receiver = P_load + P_load*(1-d)/(eta*d)`.

| Quantity | Value | Status |
| --- | ---: | --- |
| Continuous load, `P_load` | 50 W DC | Comparison case, not a measured payload requirement |
| Beam availability, `d` | 0.10 | Assumed. 18 min / 180 min. Not a coverage result |
| Storage round-trip, `eta` | 0.90 | Assumed |
| Receiver DC while charging | 550 W | Calculated from the formula at the assumed `d` and `eta` |
| Ideal centred capture | 68.276% (JSON 0.682762362928548; README table 0.682762) | Ideal focused aperture at the link below |
| Laser conversion | 40% | Assumed |
| PV conversion | 50% | Assumed |
| Source DC while charging | 4.028 kW (JSON 4027.7557014193403 W) | Calculated for the ideal link, before other losses and auxiliaries |

Check on the formula, using only the assumed `d` and `eta`:

`50 + 50*(1-0.10)/(0.90*0.10) = 50 + 50*0.90/0.09 = 50 + 500 = 550 W`.

The optical example those watts sit on is 1 m transmit, 1.5 m receive, 1.064 µm, 1,000 km slant. That link is the review's screen. It is not the NASA beamcraft (section 3).

The concurrent 50 W is taken directly during the pass. Only the gap goes through storage. On the assumed 18-minute-on / 162-minute-off cycle the README records:

- direct load during the pass: 15 Wh
- energy into storage: 150 Wh
- energy returned to the load over 162 minutes: 135 Wh
- round-trip loss in that cycle: 15 Wh

Arithmetic: `50 W × 18/60 h = 15 Wh`, and `50 W × 162/60 h = 135 Wh`. At 90% round trip, `135/0.90 = 150 Wh` must enter storage.

Storage mass uses an **assumed usable 150 Wh/kg**. It is not a measured cell. The review applies that figure to usable energy delivered to the load, not to the watt-hours pushed into storage:

- 135 Wh usable for the 162-minute gap is `135/150 = 0.9 kg` (README)
- a separate three-hour block, `50 W × 3 h = 150 Wh`, is `150/150 = 1 kg`
- a 354-hour night with no beam, `50 W × 354 h = 17,700 Wh = 17.7 kWh`, is `17700/150 = 118 kg`

The 354-hour night and the 118 kg figure are the review's full-night case if the beam is unavailable. They are not a prediction that the beam is absent for 354 hours. Half of the NSSDC synodic period (section 3) is 354.36 h, not 354 h. This budget keeps 354 h, because that is the number the review and the NASA papers use. The 0.36 h difference is `50 × 0.36 = 18 Wh`, or `18/150 = 0.12 kg` at the same assumed specific energy. A site-specific night length is still a required input.

Pointing is already in the screen and is not an orbit result. The night-service README, for the same optics and the 50 W load, gives:

| Fixed offset at the receiver | Capture | Source DC while charging |
| --- | ---: | ---: |
| 0 m | 0.682762 | 4.028 kW |
| 0.5 m (0.5 µrad at 1,000 km) | 0.493977 | 5.567 kW |
| 1 m | 0.173351 | 15.864 kW |

The energy review rounds the 0.5 m and 1 m cases to about 49.4% and 5.57 kW, and about 15.9 kW. Offsets are fixed errors, not RMS jitter. Other optical, electronic, thermal, and platform losses are excluded.

## 3. Orbit candidates actually stated in the sources

### Landis, Oleson, and coauthors, ASCEND abstract (NTRS 20230018143)

This is the PDF cited in the energy review. What it states:

- Target night load: 50 W, described as representative for a 100 kg science payload on a CLPS-style lander. The same paragraph says batteries for even low power (~50 W) night operation would require addition of 250 kg or more of battery and thermal insulation. That 250 kg is their statement, not this review's 118 kg storage line. The two figures use different specific-energy assumptions; the two figures are not reconciled here.
- Wavelength 1.07 µm. Receiver conversion "typically on the order of 50%." Selected laser electrical-to-optical efficiency 38%. Mirror diameter 1.4 m. At a stated maximum beaming distance of 1,500 km, a 1.5 m array is sized to the full-width half-maximum, "which includes roughly half of the beam power."
- Altitude **800 km** for both geometries below. Stated orbital period **3.17 hours**. Stated beam distance: minimum 800 km, maximum 1,600 km.
- Geometry chosen for detailed analysis: **three spacecraft in lunar polar orbits, planes separated by 60°**. The other geometry that met their criteria, and was not the detailed case: two orbiters in orthogonal polar planes plus one in equatorial orbit.
- Pass duration "ranges from over 35 minutes, for the best-case geometry of the satellite passing directly overhead, to a worst-case pass duration of 10 to 12 minutes." Storage is described as reduced "from requiring a duration of 354 hours of operation down to a slightly less than 3 hours."
- A 10° horizon mask is stated for the equatorial SOAP view-factor discussion. No table of contact minutes from SOAP is printed in the text.
- Latitude dependence, in their words: near-equatorial sites often see only one satellite; sites farther from the equator can be served by two satellites on each orbit; within about 30° of the pole, all three are in view on every orbit. A single equatorial beamcraft is stated as sufficient if landers are only within ~30° of the equator. A single polar beamcraft is stated as sufficient if landers are only within ~30° of the poles.
- The 800 km polar orbits "were propagated forward for a ten-year period" in Copernicus. They report small changes in eccentricity and inclination and say the orbits "remain stable even with no propulsive stationkeeping." No element table is printed.
- Spacecraft mass: **3,220 kg** total, of which **1,084 kg** is the propulsion system for insertion. That matches the mass the energy review quotes.
- The laser is used only during local night. Daytime power is solar on the same array.

The abstract does **not** give a far-side night contact fraction. It does not give a contact fraction at any named far-side site. "Over 35 minutes" and "10 to 12 minutes" are pass lengths, not a duty cycle. "Slightly less than 3 hours" is their storage-duration claim for the constellation concept, not a computed gap for one far-side asset.

### Compass briefing derived from the same study (NTRS 20230018523)

This is a separate document. It is not the PDF linked from the energy review. It repeats 800 km, three polar beamcraft separated by 60° in right ascension, 50 W nighttime, and a 354 h night. Additional statements that are in this briefing and not in the ASCEND abstract text:

- The constellation was "chosen to provide global coverage for at least 24 minutes out of every 3 hrs." The driving case shown is an equatorial lander. Polar orbits "provide increasingly improved surface coverage with latitude."
- Arithmetic on those two stated numbers, not a figure they print: `24/180 = 0.1333`. That quotient is a restatement of "at least 24 minutes out of every 3 hrs." It is their global-coverage claim for the three-spacecraft constellation in the equatorial driving case. It is not a far-side night contact fraction, and it is not a measurement at one site.
- Each beamcraft "charges their assigned landers for 15 minutes each during each orbit," with nine minutes allotted to search and lock. The lander "will need about 640 W" for that 15-minute pass; "the required beamcraft laser input power is 7600 W." Laser output in this briefing is 3 kW, and the optic is stated as 1.45 m, not the abstract's 1.4 m. Both diameters, 1.4 m and 1.45 m, are recorded; neither is selected.
- Eighteen landers, half in shadow at a given time; each beamcraft energizes three shadowed landers each orbit.
- Frozen orbits are mentioned, with a citation to Folta and Quinn (2006), and the 800 km polar orbits "were evaluated over 10 years." The briefing does not state a frozen-orbit altitude. Folta and Quinn is cited above but is not used as a source for an altitude, so no altitude is taken from it.

Nothing in either NASA document is a terrestrial demonstration. Both are lunar orbit studies. Neither replaces the review's 10% assumption with a far-side schedule.

### Lunar constants used below

From the NSSDC Moon Fact Sheet, as cited below:

- volumetric mean radius 1,737.4 km
- GM `0.00490 × 10^6 km^3/s^2` (4,900 km^3/s^2 as printed)
- sidereal rotation period 655.720 h
- revolution period 27.3217 days
- synodic period 29.53 days

Half of that synodic period: `29.53 × 24 / 2 = 354.36 h`. The NASA papers and the energy review state 354 h. Both can be true as a rounded night length. Neither is a night duration at a crater floor.

A period check at 800 km, using the fact-sheet radius and GM and a circular orbit, is in section 4. It is not a new orbit candidate.

No repeating-ground-track altitude is given in the sources cited here. None is adopted.

## 4. One geometric example

This is plane geometry for a sphere and a circular polar orbit. It is not a propagated schedule. It does not establish beam availability.

**Site.** Chang'e-4 lander, as located by the LROC caption cited below: 45.4561°S, 177.5885°E. That longitude is on the far hemisphere. The caption also lists "-5927 elevation." The elevation is not applied. No local horizon angles were on the page text used here.

**Orbit.** One circular polar orbit at the NASA altitude of 800 km. Timing uses their stated period of 3.17 h, not a refit. Inclination is taken as exactly 90°. The node is inertially fixed. The Moon's sidereal rotation is the fact-sheet 655.720 h, applied only as a uniform drift of the site relative to that node.

**Radius.** `a = 1737.4 + 800 = 2537.4 km`.

**Zero-elevation central angle.** Line of sight is above the local horizontal when `cos γ ≥ R/a`:

`R/a = 1737.4/2537.4 = 0.684717`

`γ = arccos(0.684717) = 0.816581 rad = 46.787°`

Geometric limb range at that angle: `sqrt(a^2 − R^2) = 1,849 km`. The NASA text's maximum beam distance is 1,600 km, so their link cutoff is inside the geometric limb. The primary lines below do not apply the 1,600 km cutoff or the 10° mask.

**Overhead pass.** If the orbital plane contains the site, the in-view set on a circular polar orbit is one arc of width `2γ` per revolution. Fraction of that orbit:

`γ/π = 0.259926`

Duration at the stated 3.17 h period:

`0.259926 × 3.17 × 60 = 49.44 min`

The same overhead fraction applies at any latitude, because the threshold is the angle from the site and an overhead pass reaches zero central angle. Latitude changes how often the pass is overhead, not the length of a perfectly overhead pass. This 49.44 min window is longer than the NASA "over 35 minutes" best case. It is a different quantity: zero mask, out to the geometric limb, visibility rather than a beamed pass. It is not a confirmation of their SOAP result.

Two cutoffs, still geometry, using angles they state:

- Elevation at least 10°, the mask stated for their equatorial SOAP figure. Solved central angle 37.599°. Overhead fraction `0.208884`. Duration `0.208884 × 3.17 × 60 = 39.73 min`. Slant range at the edge of that mask: 1,572 km.
- Slant range at most 1,600 km, their stated maximum beam distance. Central angle 38.534°. Overhead fraction `0.214078`. Duration `40.72 min`.

**Long-term fraction for this one orbiter.** Let `κ = R/a` and let `Ω` be the longitude of the ascending node relative to the site. With inclination 90°, the fraction of each revolution in view at elevation ≥ 0 is

`f(Ω) = (1/π) arccos(κ / A(Ω))` when `A(Ω) > κ`, else 0,

`A(Ω) = sqrt(1 − cos^2 φ sin^2 Ω)`.

Averaging `f` over one period of `Ω` at `φ = −45.4561°`, with 1,000,001 uniform samples, gives **0.194590**. At this latitude `sin γ > cos|φ|`, so every node has some zero-mask contact (`node fraction 1` in the same sample). The contacts are not of equal length. The 0.194590 figure is the time average, not the overhead orbit's 0.259926.

The same average at latitude 0°, same orbit and same mask, is **0.1095**. That is not the review's assumed 10%. The numerical proximity is not evidence that the assumed duty is an orbit result. The equator is where the NASA papers say coverage is hardest, and their remedy is three planes, not this single orbit.

**Period check, not used for the minutes above.** Circular two-body period with the fact-sheet GM:

`T = 2π sqrt(a^3 / μ)`, `μ = 4900 km^3/s^2`, `a = 2537.4 km`,

`T = 3.1869 h`.

Shifting the printed GM by one in the last digit (4,895 and 4,905 km^3/s^2) moves the period to 3.1885 h and 3.1852 h. The paper's 3.17 h sits slightly outside that band. The example therefore keeps 3.17 h as their stated period. The fact-sheet GM is too coarse, and the two-body model too bare, to "correct" it.

**Ground-track step, not a revisit time.** Using 3.17 h and 655.720 h:

`360° × 3.17 / 655.720 = 1.740°` of longitude per revolution.

About 206.85 such steps fit in one sidereal rotation. Whether those steps repeat on the site is not established from a period rounded to 0.01 h. No repeating ground track is claimed.

**What this example omits.** Terrain and crater horizon. Libration. Earthshine is irrelevant; source eclipse is not modeled. Pointing, beam quality, and the 1,000 km review link versus an 800–1,600 km slant. Multi-user sharing, search and lock, and a missed pass. Day versus night: the fraction 0.194590 counts every geometric visibility, including local day, when the NASA concept uses sunlight on the lander and does not claim the laser is on. It also ignores whether the beamcraft is itself in sunlight. Gravity harmonics, third-body motion, and a non-circular orbit are not propagated. One spacecraft, not the three-plane constellation.

## 5. Storage if one pass is missed, and if the night has no beam

The gap used here is the review's illustrative schedule, not a gap from section 4.

Nominal cycle: 18 min beam, 162 min off. That is the assumed 10% (`18/180 = 0.10`). Usable energy in the off interval is 135 Wh, and the README's mass for that minimum is 0.9 kg. The separate three-hour sizing is 1 kg.

**One missed pass** means the next 18-minute window does not occur and the beam returns at the window after that. Time from the end of the last beam to the start of the next beam:

`162 + 18 + 162 = 342 min = 5.7 h`.

Usable energy at 50 W:

`50 × 5.7 = 285 Wh`.

Mass at the assumed usable 150 Wh/kg, on the same basis as the 0.9 kg and 1 kg figures (usable watt-hours, not watt-hours into the cell):

`285 / 150 = 1.9 kg`.

A store sized only to the 135 Wh gap is short by `285 − 135 = 150 Wh`, which is `50 W × 3 h`. The nominal cycle puts 150 Wh into storage to cover 135 Wh. It does not preload this miss. At the assumed 90% round trip, delivering 285 Wh from storage would require `285/0.90 = 316.7 Wh` to have entered storage on an earlier pass. That charge is not in the 550 W, 18-minute example.

If the miss is read instead as two of the review's conservative three-hour blocks, `2 × 150 Wh = 300 Wh` and `300/150 = 2.0 kg`. That reading is also arithmetic on the review's three-hour block. It is not a second orbit result. The 1.9 kg line is the one that follows the 18/162 clock.

**Full night with no beam,** using the review's 354 h:

`50 × 354 = 17,700 Wh = 17.7 kWh`

`17,700 / 150 = 118 kg`.

The 90% factor is not applied again on top of that 118 kg. The review's night mass is usable energy divided by the assumed 150 Wh/kg. If a round-trip loss is later assessed on a full-night discharge, that factor is not in the 118 kg and remains part of the storage model.

| Case | Usable energy at 50 W | Mass at assumed 150 Wh/kg |
| --- | ---: | ---: |
| 162 min gap (illustrative schedule) | 135 Wh | 0.9 kg |
| Conservative 3 h block | 150 Wh | 1 kg |
| One missed 18 min window on that schedule (342 min dark) | 285 Wh | 1.9 kg |
| Two conservative 3 h blocks | 300 Wh | 2.0 kg |
| 354 h with no beam | 17,700 Wh | 118 kg |

None of these masses is a battery design. The 1.9 kg figure is not small in any sense that implies the service works. It only says that, on the assumed clock, one missed window is a few times the nominal gap, while a dark 354 h night is the 118 kg case already in the review. A real miss has whatever length the orbit, the terrain, and the outage produce. That length is not known.

## 6. What is still not established

Required inputs. Not a hardware plan.

1. The continuous load. 50 W is the comparison case in the energy review, not a measured payload requirement.
2. One site or latitude band, with a terrain horizon versus azimuth. The Chang'e-4 coordinates above are only the geometric example's label. Libration belongs in that mask.
3. Local night duration at that site. 354 h is the figure used in the review and stated by the NASA papers. It is not a site integration. Half of the fact-sheet synodic period is 354.36 h and was not substituted.
4. Orbit elements: altitude, eccentricity, inclination, node, and phase. The NASA study states 800 km, polar, 3.17 h, and a three-plane 60° arrangement, plus a 10-year qualitative stability statement. It does not publish the elements or a far-side access file. Frozen-orbit altitude was not stated in the documents opened here.
5. Propagated access intervals, including source eclipses. The 0.194590 line-of-sight average is not those intervals.
6. The split between geometric visibility and beam-on time: range limit, 10° or other mask, search and lock, slew, pointing (the 0.5 m and 1 m offsets already move source power from 4.028 kW to 5.567 kW and 15.864 kW on the review's link), and beamcraft energy while the orbiter is in shadow.
7. How many users share a pass. The Compass briefing assigns 15 minutes of charge to each of three shadowed landers per beamcraft per orbit. That allocation is not a duty cycle at 45.4561°S.
8. Storage round-trip and usable Wh/kg. Both 90% and 150 Wh/kg are assumptions. The mass table falls if either changes.
9. At least one missed pass inside the integrated storage state, with the miss defined by the propagated schedule rather than by adding 18 minutes to the assumed clock.

Until those exist, the service has no demonstrated contact fraction and no claim to continuous night power.
