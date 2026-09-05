# Adversarial antenna and power-transfer physics review

Date: 2026-09-05. Source baseline inspected: `d939c36609a36295d0f3819187baaba95fdcd545`. This report adds analysis; it does not rewrite the existing manuscript or change its calculations. The user's clarified objective is **sending and receiving useful energy, especially on the far side or during darkness**. Detecting a field is therefore insufficient: the relevant result is DC power delivered to a load, after the receiver and its losses.

**Decision:** ordinary ELF antennas are not a reasonable route to useful power across kilometres or around the Moon. That conclusion follows from explicit source/receiver coupling calculations below, independently of the repository's questionable cavity-Q bounds. Short-range resonant inductive charging is viable; cables and optical power links deserve the principal engineering effort for remote loads. A superconducting local link is a conditional research idea, with numerical loss requirements provided below. No viable planetary ELF power system has been established.

## What the repository establishes, and what it does not

The missing conducting upper wall rules out the familiar Earth–ionosphere Schumann-cavity geometry. It does **not** imply zero electromagnetic coupling, zero radiation, zero induced currents, or the absence of every possible open-system mode. The manuscript acknowledges the missing open-boundary Maxwell solution in its limitations.

There is no antenna feed, current normalization, port impedance matrix, receiving load, rectifier, or delivered-power calculation in the inspected source. `scripts/03_driven_transfer.py` plots attenuation along an assumed shell path and a normalized `1/|Zg+Zi|`. Neither is a transfer impedance in volts per injected ampere. A wall admittance cannot establish source coupling to a particular receiver, and normalized curves discard precisely the scale needed for power feasibility.

Three physics problems prevent promoting the current numerical results into a rigorous antenna no-go theorem:

1. **Cavity Q has a factor-of-two benchmark discrepancy.** For a weakly lossy thin TEM cavity, using peak phasors, total time-averaged stored energy per area is `U/A = μ h |H|²/2`; dissipation at the two walls is `P/A = (Rg+Ri)|H|²/2`. Consequently `Q = ωμh/(Rg+Ri)`. `sphere/impedance.py:138` instead divides by `2(Rg+Ri)`. Galejs's Appendix, equations (14)–(19), gives the same single-wall weak-loss result at the ideal modal frequency. This is an independent analytic benchmark, **not** permission simply to double every lunar result: wall reactance, energy inside the walls and strong damping require a solved field problem when the predicted Q is around one. [Galejs, *Schumann Resonances*, NBS 1965](https://nvlpubs.nist.gov/nistpubs/jres/69D/jresv69Dn8p1043_A1b.pdf)
2. **The claimed shell-path upper bound combines inconsistent propagation constants.** `sphere/energy_q.py:119–133` combines the conductor attenuation constant with the lossless dielectric phase constant. In a homogeneous medium, writing `k=β−iα`, Maxwell's equations give `β²−α²=ω²με` and `2αβ=ωμσ`; when conduction dominates, `β≈α`, so `β/(2α)≈1/2`, not the much smaller value produced by the code. Overestimating phase velocity decreases this ratio, so the stated reasoning for an upper bound points in the wrong direction. Even the corrected ratio is a propagation proxy, not an independently established loaded cavity Q.
3. **Local, shell and external paths are different boundary-value problems.** A geometric-mean conductivity across the outer 300 km is not a justified effective material for a surface antenna's predominantly shallow near field. A plane-wave skin-loss factor along a selected circumferential path does not upper-bound an exterior diffracted field. A proper solution needs vector fields, material interface conditions, the feed and an outgoing boundary condition. The scalar TM interface claim in `sphere/transfer.py` also requires correction before treating its solutions as physical TM modes across conductivity/permittivity jumps.

These defects weaken the quantitative claims of the repository; they do not supply the enormous receiver coupling needed for useful ELF power.

## Direct power calculation: copper ELF loops

Use an explicit, favourable baseline: a single-turn circular transmitter of radius 100 m, copper area 2.5 mm², 10 Hz, and 100 W dissipated in its wire. Copper resistivity is `1.724e-8 Ω m` and density `8960 kg/m³`; these are stated room-temperature design constants, not measured lunar operating values. The transmitter contains 628.3 m of wire and 14.07 kg of copper, excluding insulation, supports and electronics.

All currents and voltages below are RMS. With wire resistance `Rt=ρ 2πa/Ac`, current `It=sqrt(Pwire/Rt)` and loop area `At=πa²`, the values are:

| Quantity | Value |
|---|---:|
| Transmitter resistance | 4.3329 Ω |
| Transmitter current | 4.8041 A |
| Magnetic dipole moment `It At` | 150,925 A m² |
| Dipole magnetic field at 1 km in the loop plane | 15.09 pT |
| Approximate loop inductance | 1.471 mH |
| Wire-loss quality factor `ωL/Rt` | 0.02133 |
| Free-space radiation resistance | `3.81e-17 Ω` |

For two small coplanar loops at separation `r` large compared with their radii, the magnitude of their vacuum mutual inductance is

`M ≈ μ0 At Ar/(4πr³)`.

The receiving loop has open-circuit voltage `Voc=ω M It`. Even allowing ideal lossless tuning and optimal resistive matching, its available load power is

`PL,max = Voc²/(4Rr)`.

The following receiver loops use the same 2.5 mm² copper. They are oriented to intercept the equatorial field of the surface transmitter; the loop areas are not arbitrary effective apertures.

| Receiver radius | Separation | `M` | `Voc` | Ideal matched-load power | `PL/Pwire` |
|---|---:|---:|---:|---:|---:|
| 10 m | 1 km | 0.987 nH | 0.298 µV | **51.2 fW** | `5.12e-16` |
| 100 m | 1 km | 98.7 nH | 29.8 µV | **51.2 pW** | `5.12e-13` |
| 10 m | 10 km | 0.987 pH | 0.298 nV | `5.12e-20 W` | `5.12e-22` |
| 100 m | 10 km | 98.7 pH | 29.8 nV | **51.2 aW** | `5.12e-19` |

These are dipole approximations and favourable engineering references, not rigorous upper bounds across every possible lunar material configuration. They omit rectifier, converter, tuning-capacitor and transmitter losses. The transmitter power normalization is its wire loss; reflected receiver loading is negligible for these extremely weak links. A source-receiver calculation with finite loops refines the geometric factors without repairing an approximately twelve-order efficiency deficit.

At the 1 km, 100 m receiver case, one watt delivered under this model would require approximately `1.95e12 W` of transmitter wire dissipation. Equivalently, that receiver would require about **2.11 µT RMS**, rather than the available 15.09 pT. Integrating the 51.2 pW for 336 hours collects only **61.9 µJ** before conversion losses. Coherent integration can improve signal detection; it cannot increase received energy.

The low wire-loss Q is a practical warning against invoking resonance without an equivalent circuit. At 10 Hz the 100 m loop has only 0.0924 Ω inductive reactance against 4.33 Ω resistance. Ideal series compensation would require approximately 0.172 F, and would not eliminate the wire resistance. Raising frequency improves the mutual voltage, but the simple `f²` received-power extrapolation eventually fails as AC losses, distributed capacitance, radiation, ground coupling and receiver loading change.

### Why more turns and impedance transformers do not fix this

At fixed loop radius, copper mass and transmitted Joule power, N turns increase wire length by N and reduce wire cross-section by N. Thus `R∝N²`, allowable current `I∝1/N`, and magnetic moment `NIA` remains constant. On reception, `Voc∝N` but `Rr∝N²`, leaving `Voc²/(4Rr)` unchanged. The coupling figure of merit below is also unchanged. Turns and transformers are useful for matching real electronics; they do not create an efficiency gain at fixed copper resources.

At fixed copper mass `Mc`, a circular transmitter's moment obeys the particularly useful scaling

`m = (a/2) sqrt(Pwire Mc/(ρ ρmass))`.

Increasing radius therefore helps linearly, but extending wire over large terrain is an infrastructure commitment. Magnetic cores can change coupling and losses; a permeability multiplier without core geometry, demagnetization, saturation and AC-loss calculations is not a design.

## Resonance: a real local solution, with explicit conditions

For two ideally tuned reciprocal coils with resistances `R1,R2`, mutual inductance M and negligible radiation, define

`χ = ω² M²/(R1R2) = k²Q1Q2`.

Optimizing the receiver load gives

`ηmax = (sqrt(1+χ)-1)/(sqrt(1+χ)+1)`.

This is coil-to-load efficiency, excluding power electronics. It explains both successful resonant power transfer and the failure of the ordinary 10 Hz example: resonance works when mutual coupling is sufficiently large compared with loss. It is not enough that two components share a resonance frequency. Experimental resonant coupling has transferred 60 W over more than 2 m at approximately 40% efficiency. [Kurs et al., *Science* 2007, primary abstract](https://pubmed.ncbi.nlm.nih.gov/17556549/)

**Viable use case: contactless charging at a lunar docking point.** A station powered by solar/storage, a cable, nuclear generation or an optical receiver supplies a kHz–MHz inductive coupler across a short gap. This could avoid repeated exposed electrical contact mating in dusty terrain. It solves the final short gap, while a separate system delivers energy to the station. NASA has a specific proximity-charger development project for lunar rovers. [NASA, *Ultra Fast Proximity Charger*, 2024](https://ntrs.nasa.gov/api/citations/20240011234/downloads/20240011234.pdf)

For a transparent geometric example, two coaxial circular loops of radius 0.5 m, with a nominal thin-wire self-inductance of 3.879 µH, have mutual inductance computed from the complete elliptic-integral formula. **If** both completed resonators attain measured unloaded Q=100 at their selected operating frequency, their ideal results are:

| Axial separation | Mutual inductance | Coupling k | Ideal maximum efficiency |
|---|---:|---:|---:|
| 0.5 m | 0.247 µH | 0.06369 | 73.1% |
| 1 m | 0.0709 µH | 0.01829 | 35.2% |
| 2 m | 0.0130 µH | 0.003351 | 2.66% |

The assumed Q is a design requirement, not an achieved lunar measurement or a claim about 10 Hz copper. Ferrite-backed, multi-turn docking coils have a different inductance/coupling geometry and should be optimized directly. The immediate engineering test is watts delivered across a representative gap, including nearby metal, misalignment, thermal operation and electronics losses.

**Conditional research option: superconducting local loops.** In the 100 m radius, 1 km coplanar geometry at 10 Hz, 50% ideal efficiency requires `χ≥8`. Equal transmitter and receiver losses would each have to satisfy

`Rac ≤ ω|M|/sqrt(8) = 2.19 µΩ`,

corresponding to Q about 42,200. At 10 km, the required residual resistance is 2.19 nΩ and Q about 42 million. Those requirements apply to the entire winding and tuning system, including joints and AC losses. They exclude cryogenic power, deployment mass and critical-current limitations. The Moon's cold regions do not themselves certify superconducting operation under load. This is physically conditional, not mathematically forbidden; it is a poor first investment compared with a cable over the same local distance. A useful proposed superconducting demonstration must report net delivered watts after cryogenic overhead.

## Electric antennas, ground injection and planetary shortcuts

**A short electric dipole is less bad as an ELF radiator than a loop, but the absolute numbers remain severe.** In vacuum, for a thin centre-fed dipole of total length `l` with triangular current distribution,

`Rrad ≈ 20π²(l/λ)²`.

At 10 Hz this gives 2.20 nΩ for 100 m, 0.220 µΩ for 1 km and 22.0 µΩ for 10 km. A capacitively top-loaded design with nearly uniform current can gain a factor of four relative to the same physical length in this ideal expression. These are radiation resistances, not feed impedances or end-to-end efficiencies. For an illustrative terminal capacitance of 10 nF, 10 Hz capacitive reactance is 1.59 MΩ; an untuned 10 kV RMS drive supplies only 6.28 mA. The capacitance is an explicit assumed parameter, not a prediction for a particular deployed wire. Resonant matching moves the difficulty to stored energy, voltage and loss in the matching system. [MIT, *Electromagnetic Fields and Energy*, chapter 12](https://ocw.mit.edu/courses/res-6-001-electromagnetic-fields-and-energy-spring-2008/pages/chapter-12/)

Electric near-field coupling must still be considered through a capacitance/admittance matrix; low far-field radiation alone does not prove its impossibility. However, a useful remote capacitive power link needs receiver dimensions, return electrodes, voltage limits and environmental leakage. None is present in the repository. For deployed surface electric antennas, free-space fields and PEC ground images are both unjustified defaults without the actual material and plasma boundary response.

**Ground electrodes face a different but quantifiable problem.** In the elementary DC homogeneous-half-space model, two widely separated hemispherical electrodes of radius b have combined spreading resistance approximately `1/(πσb)`. For `σ=1e-8 S/m` and `b=1 m`, that is 31.8 MΩ before contact complications. At 100 kV only about 3.14 mA enters the medium. Actual ELF electrodes require complex conductivity, geometry and contact impedance. Replacing a copper return conductor by poorly conducting regolith does not preserve a low-loss power circuit. The elementary result is a benchmark, not a lunar electrode measurement.

**Chu Q does not independently prohibit power transfer.** For a passive, compact, single electric or magnetic dipole radiator in free space, the conventional radiation-Q lower bound is `Qrad ≥ (ka)^−3+(ka)^−1`. At 10 Hz it is approximately `1.09e14` for enclosing radius 100 m and `1.09e11` for 1 km. This is radiation Q, not the wire-loss Q above; material losses can make loaded Q small while making radiation inefficient. Narrowband continuous power does not need wide modulation bandwidth, and near-field power transfer has its own coupling/loss calculation. Using the whole Moon as the enclosing radius requires establishing currents and source coupling on that whole scale; merely naming the Moon the antenna does not establish those currents. Material-loading and multi-mode variants require their corresponding bounds. [Pfeiffer, *Fundamental Efficiency Limits for Small Metallic Antennas*, definitions and assumptions](https://arxiv.org/pdf/1612.07317), [Kong et al., small spherical helix antenna study](https://doi.org/10.1049/el.2016.0982)

**Artificial resonators, active matching, rotating magnets and mechanical antennas require the same energy accounting.** Such devices may improve a particular source impedance, field amplitude, operating frequency or deployment constraint. They cannot turn the existence of a remotely measurable field into net useful received watts. Any active element also supplies energy and belongs in the input-power budget. Any receiving resonator must be loaded, and that loading changes its Q. A proposed Moon-scale mode must demonstrate source and receiver coupling as well as a positive energy balance with radiated and dissipated power included.

## Far-side and darkness architectures worth pursuing

The far side receives sunlight; geographic far side, ordinary lunar night and a permanently shadowed crater are distinct mission cases. Lunar night requires time-shifting or importing energy, whereas the far side requires a suitable source location and communication/beam geometry. [NASA, *Top Moon Questions*](https://science.nasa.gov/moon/top-moon-questions/)

| Mission | Reasonable architecture | Concrete next calculation |
|---|---|---|
| Fixed payload within kilometres of a power source | Two-conductor high-voltage cable; optional inductive final connection | Conductor, insulation, deployment and converter mass at the required watts and distance |
| Rover or inaccessible crater with line of sight to a station | Optical beam to tuned photovoltaic receiver, plus local storage | DC-to-DC efficiency, pointing, receiver heat, terrain occultation and outage duration |
| Distributed far-side/night payloads | Local generation/storage or orbital optical power network | Orbit coverage, source generation, storage during occultation and delivered energy per pass |
| Rover docking or exposed connector avoidance | Resonant inductive charging over a short gap | Measured `k²Q1Q2`, rectified watts and misalignment tolerance |
| Scientific investigation that retains ELF | Low-power magnetic/electric sounding with independent station power | Calibrated complex transfer function and environmental noise; this is a scientific use case, not an energy supply |

NASA's surface-transfer trade study compared cables, RF and laser transmission over 0.1–10 km and selected DC cabling under its assumptions. That study provides a useful comparator, not a universal answer for every mobile mission. [NASA, *Lunar Surface-to-Surface Power Transfer*](https://ntrs.nasa.gov/citations/20080008842)

A NASA orbital-power study explicitly targets 50 W of lunar-night power for small science landers, uses a 1.07 µm laser and approximately 50% photovoltaic conversion, and studies a three-spacecraft coverage architecture. These are conceptual design assumptions/results, not an operational service. [NASA, *Power Beaming from Lunar Orbit*](https://ntrs.nasa.gov/api/citations/20230018143/downloads/PowerBeamingFromLunarOrbitForSmallScienceLanders.pdf)

The useful synthesis is a **power network with different links for different distances**: local or orbital generation, cables or optical links for transport, storage for scheduled outages, and inductive coupling where repeated physical docking makes it worthwhile. A transmitter cannot solve the lunar-night source-energy requirement by itself. For example, a 100 W load over an assumed 336-hour night needs 33.6 kWh before conversion losses and thermal overhead.

## Reproduction of the decisive ELF power numbers

The following standalone calculation reproduces the copper-loop table. It requires only Python's standard library. The finite-size field/flux checks and broader design scan are maintained separately by the coordinating review.

```python
import math

rho = 1.724e-8
wire_area = 2.5e-6
omega = 2 * math.pi * 10
tx_radius = 100.0
tx_area = math.pi * tx_radius**2
tx_resistance = rho * 2 * math.pi * tx_radius / wire_area
tx_current = math.sqrt(100 / tx_resistance)

for rx_radius in (10.0, 100.0):
    rx_area = math.pi * rx_radius**2
    rx_resistance = rho * 2 * math.pi * rx_radius / wire_area
    for separation in (1000.0, 10000.0):
        mutual = 1e-7 * tx_area * rx_area / separation**3
        voltage = omega * mutual * tx_current
        power = voltage**2 / (4 * rx_resistance)
        print(rx_radius, separation, mutual, voltage, power, power / 100)
```

The conclusion is bounded: the specified conventional ELF power links fail by an overwhelming margin; the current repository has not proved a universal theorem about every lunar electromagnetic architecture. The most productive next result is a source-to-load trade study for cables, optical links and local inductive docking at a chosen load, distance and outage schedule.
