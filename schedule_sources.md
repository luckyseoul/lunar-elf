# Sources for the night-charging schedule

Sources dated 2026-10-01. Quotes are from the files and pages cited below. Computed lines are the arithmetic and geometry behind `NIGHT_CHARGING_SCHEDULE.md`.

## Repository, `luckyseoul/lunar-elf` at `main`

Repository files at ref `main`.

### `paper/ENERGY_DELIVERY_REVIEW_2026-09-05.md`

- "Use **50 W continuous receiver DC** as a review target, not an inferred user requirement."
- "Beam availability | 10%, assumed; not an orbit-coverage result"
- "Continuous user load | 50 W DC"
- "Storage round-trip efficiency | 90%, assumed"
- "Receiver DC during charging | **550 W**"
- "Transmitting / receiving diameter | 1 m / 1.5 m"
- "Wavelength / slant range | 1.064 µm / 1,000 km"
- "Ideal centred aperture capture | 68.276%"
- "Laser / PV conversion | 40% / 50%, assumed"
- "Source DC during charging | **4.028 kW**, before other losses and auxiliaries"
- "Usable energy for actual 162-minute gap | 135 Wh"
- "Usable energy for a conservative three-hour gap | 150 Wh"
- "Storage at an assumed usable 150 Wh/kg | **1 kg** for three hours; **118 kg** for a 354-hour night"
- Formula printed there: `P_receiver = P_load + P_load*(1-d)/(eta*d)`.
- "a static 0.5 m offset at the receiver (0.5 µrad) reduces capture to about 49.4% and raises source demand to **5.57 kW**. A 1 m offset raises it to about **15.9 kW**."
- "its three-spacecraft design estimates **3,220 kg per beamcraft**."
- Gate 3: "Propagate an orbit and terrain model for one selected far-side site or latitude band. Integrate storage state through source eclipses, blocked passes, multiple users and at least one missed pass. The current screen does not establish this schedule or continuous service."
- Citation printed in that section: `https://ntrs.nasa.gov/api/citations/20230018143/downloads/PowerBeamingFromLunarOrbitForSmallScienceLanders.pdf`

### `results/antenna_review_2026-09-05/energy_trade/night_service.json`

50 W, `duty_assumed` 0.1 row:

- `storage_roundtrip_efficiency_assumed`: 0.9
- `receiver_dc_during_pass_w`: 550.0
- `source_dc_during_pass_w`: 4027.7557014193403
- `three_hour_usable_storage_wh`: 150
- `three_hour_storage_kg_at_assumed_150whkg`: 1.0
- `full_night_storage_kg_at_assumed_150whkg`: 118.0
- `capture_fraction`: 0.682762362928548
- `wavelength_m`: 1.064e-06
- `distance_m`: 1000000.0
- `tx_diameter_m`: 1
- `rx_diameter_m`: 1.5
- `tx_conversion_assumed`: 0.4
- `rx_conversion_assumed`: 0.5

### `results/antenna_review_2026-09-05/energy_trade/summary.json`

Used only as context that the screen's limitations include: "Optical/RF capture is ideal focused diffraction, not terrain/coverage/pointing validation" and "Conversion efficiencies and usable storage density are explicit scenario assumptions." No schedule quantity was taken from this file.

### `results/antenna_review_2026-09-05/night_service/README.md`

- "The 10% availability is an assumption; no orbit, terrain, eclipse or service availability is established."
- Table: 0 m capture 0.682762, source DC 4.028 kW; 0.5 m capture 0.493977, source DC 5.567 kW; 1 m capture 0.173351, source DC 15.864 kW.
- "An assumed 18-minute charging window followed by 162 minutes without a beam requires 550 W receiver DC while charging at 90% storage round-trip efficiency. The direct load consumes 15 Wh while charging; 150 Wh enters storage and supplies 135 Wh to the load afterward. Minimum usable storage is consequently 135 Wh; the separate three-hour sizing is 150 Wh. At an assumed usable 150 Wh/kg, these are 0.9 kg and 1 kg, compared with 118 kg for a 354-hour night."

### `paper/ANTENNA_ALTERNATIVES_2026-09-05.md`

Orbit statements recorded there, checked against the PDFs rather than reused as primary numbers:

- "NASA's *Power Beaming from Lunar Orbit for Small Science Landers* studies 50 W night operation using 1.07 µm lasers. Its architecture has three orbital planes at 800 km, 3 kW optical lasers, 1.4 m transmitting mirrors and 1.5 m receiving arrays. Passes last roughly 10–35 minutes; storage bridges approximately three hours rather than a whole night."
- "Each beamcraft is estimated at 3,220 kg, including 1,084 kg of propulsion."
- The same file states the horizon example "on a smooth Moon of radius 1,737.4 km". That radius matches the fact sheet below. It is not an orbit altitude.
- Illustrative night energy in that file: "17.7 kWh at 50 W" and "118" kg at an assumed 150 Wh/kg. Arithmetic check: `50*354 = 17700 Wh`.

The alternatives file's "roughly 10–35 minutes" is coarser than the ASCEND wording "over 35 minutes" and "10 to 12 minutes." Pass length in the schedule is the PDF wording, not this paraphrase.

## NASA PDFs

### ASCEND abstract, NTRS 20230018143

URL: `https://ntrs.nasa.gov/api/citations/20230018143/downloads/PowerBeamingFromLunarOrbitForSmallScienceLanders.pdf`

Text extracted with `pdftotext -layout` from the downloaded file.

- "Due to the length of the lunar night, batteries power for even low power (~50 W) night operation would require addition of 250 kg or more of battery and thermal insulation mass"
- "A 50-Watt night power requirement was adopted as representative need of a 100-kg science on a CLPS-style lander."
- "the laser technology chosen was a diode-pumped fiber laser, with a high beam quality at a wavelength of 1.07 microns."
- "power conversion efficiency of the receiver is typically on the order of 50%."
- "three spacecraft in lunar polar orbits with orbital planes separated by 60°."
- "or two orbiters in orthogonal polar orbital planes plus another in equatorial orbit"
- "For both cases, the orbital altitude of 800 km above the surface was chosen, with an orbital period of 3.17 hours."
- "The maximum distance for the beam to travel is 1600 km, while the minimum distance is the orbital altitude 800 km."
- "The 800-km polar orbits were propagated forward for a ten-year period using the Copernicus software [5], showing that perturbations give small changes in eccentricity and inclination, but the orbits remain stable even with no propulsive stationkeeping."
- "The pass duration ranges from over 35 minutes, for the best-case geometry of the satellite passing directly overhead, to a worst-case pass duration of 10 to 12 minutes. This reduces the battery needed to survive and operate during the lunar night from requiring a duration of 354 hours of operation down to a slightly less than 3 hours"
- "a 10° horizon mask is assumed"
- "for sites within about 30 degrees of the pole, all three satellites will be in view on every orbit."
- "If the landers to be powered were distributed only to near-equatorial (within ~30° latitude of the equator) sites, a single beamcraft in equatorial orbit would be sufficient; likewise, to distribute power only to near-polar sites (within ~30° latitude of the poles), a single polar-orbiting beamcraft would be sufficient."
- "an electrical to optical conversion efficiency of 38%."
- "A 1.4-meter diameter mirror was selected"
- "at the maximum beaming distance of 1500 km, a 1.5-meter diameter array will equal the diameter of the full-width half maximum (FWHM) of the beam, which includes roughly half of the beam power."
- "Total mass of the orbital spacecraft is 3220 kg, including the mass of the propulsion system, 1084 kg"

No sentence in this PDF states a far-side night contact fraction.

### Compass briefing, NTRS 20230018523

URL: `https://ntrs.nasa.gov/api/citations/20230018523/downloads/Power%20Beaming%20From%20Lunar%20Orbit%20Final%20version.pdf`

Separate document from the citation above. Text extracted the same way.

- "survive the 354 hr night"
- "a three beamcraft constellation at 800 km, each in a polar orbit, separated in right ascension by 60° was chosen to provide global coverage for at least 24 minutes out of every 3 hrs."
- "the polar orbits provide increasingly improved surface coverage with latitude."
- "there are ‘frozen orbits’ whose parameters change little over time but oscillate [7]." Reference 7 is Folta and Quinn, "Lunar frozen orbits," 2006. That paper was not opened. No frozen-orbit altitude is quoted from it.
- "The 800 km polar orbits were evaluated over 10 years of operations"
- "Each beamcraft charges their assigned landers for 15 minutes each during each orbit."
- "Nine minutes have been allotted to this search and lock"
- "The lander will need about 640 W of power for the 15-minute pass"
- "The required beamcraft laser input power is 7600 W."
- "a 3 kW laser (output)" and "a 1.45 m optical ‘telescope’"
- "main efficiency losses are a 38% efficient laser and 50% efficient lander PV"

The briefing states the 24 minutes and the 3 hours. It does not print the quotient. Arithmetic on those two stated numbers: `24/180 = 0.1333...`.

## Lunar constants

### NSSDC Moon Fact Sheet

URL: `https://nssdc.gsfc.nasa.gov/planetary/factsheet/moonfact.html`

Fetched and read as text. Values used, Moon column:

- Equatorial radius (km) 1738.1
- Polar radius (km) 1736.0
- Volumetric mean radius (km) 1737.4
- GM (x 10^6 km^3/s^2) 0.00490
- Revolution period (days) 27.3217
- Synodic period (days) 29.53
- Sidereal rotation period (hrs) 655.720

Half synodic period, arithmetic: `29.53 * 24 / 2 = 354.36` h. Not substituted for the 354 h figure used in the energy review and the NASA papers.

### Chang'e-4 coordinates

URL: `https://www.lroc.asu.edu/images/1100`

LROC caption text read from the page: "coordinates -5927 elevation, 45.4561°S latitude, 177.5885°E longitude" and "NASA/GSFC/Arizona State University". Elevation was not used as a radius correction. No horizon angles were taken from the page.

## Computed lines

Arithmetic and geometry behind `NIGHT_CHARGING_SCHEDULE.md`. Geometry assumes a sphere of radius 1737.4 km and a circular orbit. It is not an ephemeris.

Load, from the review's assumptions:

```
50 + 50*(1-0.10)/(0.90*0.10) = 550 W
50 * 18/60 = 15 Wh
50 * 162/60 = 135 Wh
135/0.90 = 150 Wh into storage
135/150 = 0.9 kg
50*3 = 150 Wh; 150/150 = 1 kg
50*354 = 17700 Wh; 17700/150 = 118 kg
50*0.36 = 18 Wh; 18/150 = 0.12 kg   # 354.36 h minus 354 h; not the night mass in the schedule
```

Missed illustrative window:

```
162+18+162 = 342 min = 5.7 h
50*5.7 = 285 Wh
285/150 = 1.9 kg
285-135 = 150 Wh short of the 162 min store
285/0.90 = 316.666... Wh that would have to enter storage
2*150 = 300 Wh; 300/150 = 2.0 kg   # alternate reading, two 3 h blocks
18/180 = 0.10
```

Orbit geometry:

```
a = 1737.4 + 800 = 2537.4 km
R/a = 0.6847166391
gamma = arccos(R/a) = 0.8165814988 rad = 46.786674 deg
gamma/pi = 0.25992596
0.25992596 * 3.17 * 60 = 49.4379 min   # reported as 49.44 min
limb range = sqrt(a^2 - R^2) = 1849.28 km

# elevation >= 10 deg, quadratic solution for cos(gamma)
gamma_10 = 37.599079 deg
fraction = 0.20888377
minutes at 3.17 h = 39.7297
slant range at that angle = 1572.03 km

# slant range <= 1600 km
gamma_1600 = 38.5341 deg
fraction = 0.214078
minutes at 3.17 h = 40.718

# long-term zero-mask fraction, one polar orbiter
# f(Omega) = arccos(kappa/A)/pi if A>kappa else 0
# A = sqrt(1 - cos(phi)^2 * sin(Omega)^2)
# mean of 1000001 samples, Omega over 0..pi
phi = -45.4561 deg -> 0.19459048
phi = 0 -> 0.10952085
sin(gamma) = 0.728809 > cos(45.4561 deg) = 0.701456  # every node has some zero-mask contact

# two-body period check, not used for the minutes
mu = 0.00490e6 = 4900 km^3/s^2
T = 2*pi*sqrt(a^3/mu) = 3.186858 h
mu = 4895 -> 3.188485 h
mu = 4905 -> 3.185233 h

# longitude step at the stated 3.17 h and fact-sheet sidereal rotation
360 * 3.17 / 655.720 = 1.740377 deg per revolution
655.720 / 3.17 = 206.8517 revolutions per sidereal rotation
```

The overhead formula used: in-view fraction of one revolution when the orbital plane contains the site is `gamma/pi`, because the in-view arc is `2*gamma` out of `2*pi`. Elevation `ε` satisfies `sin ε = (a cos γ − R) / range` with `range^2 = a^2 + R^2 − 2 a R cos γ`. Zero elevation is `cos γ = R/a`.

## Not used

The FISO briefing and NTRS 20240011011 are not sources. The 20240011011 download returned 404, and that PDF is not used. No number from either document is used. Folta and Quinn 2006 is not a source. No frozen-orbit altitude is stated.
