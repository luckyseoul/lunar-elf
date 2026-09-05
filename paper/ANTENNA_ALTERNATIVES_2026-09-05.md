# Practical energy delivery alternatives: adversarial review

Reviewed 2026-09-05 against `d939c36609a36295d0f3819187baaba95fdcd545`.
Scope incorporates the user's clarification: **send and receive useful energy,
especially on the lunar far side and during darkness**. Literature checked live;
engineering calculations below are screening estimates, not qualified designs.

## Recommendation

The strongest practical direction is a **local source plus an engineered power
distribution system**. Use a two-conductor high-voltage cable for fixed loads or
tethered exploration; test optical power delivery where mobility or terrain makes
a cable costly. For isolated far-side instruments, the interesting orbital use
case is periodic battery charging to survive the night. An ELF field that can be
detected does not establish a power-transfer capability.

| Mission | Leading architecture | Evidence and decision |
| --- | --- | --- |
| Fixed 100 W–10 kW load a few km from a power source | High-voltage cable, converters, local buffer storage | Best near-term baseline; relevant ground prototypes already exist |
| Mobile or difficult-to-reach load with line of sight | Laser and wavelength-matched photovoltaic receiver | Real terrestrial delivered-power demonstrations; lunar systems remain engineering concepts |
| Isolated far-side science station through lunar night | Local daytime solar; storage sized against periodic optical charging from lunar orbit | Credible development path for a fleet; substantial spacecraft infrastructure |
| Rover docking or an enclosed transfer interface | Closely coupled inductive charging, with frequency selected for that interface | Useful wireless niche; metre-scale or smaller geometry must be demonstrated |
| Shadowed polar site near illuminated terrain | Cable first; compare sunlight redirection and laser delivery | Source visibility, receiver area and storage govern the trade |
| Global ELF power transmission through the Moon | No viable design established | Present repository has no source-to-load model or electrical receiver |

The far side has sunlight during its local day. Its distinct problem is Earth
occultation; lunar night is a separate, recurring energy-storage problem.
Permanently shadowed polar regions add a third geometry. These cases should not
share one assumed availability factor. [NASA Moon facts](https://science.nasa.gov/moon/facts/)

## 1. Size the service in watts and watt-hours

An antenna proposal must specify source electrical power, delivered regulated DC
power, any useful delivered heat, duty cycle, longest outage, receiver size and
mass, and total source/receiver thermal burden. For a constant load served
directly while a beam is present, with storage supplying the load between passes,
a necessary average-energy condition at availability fraction `d` is

`P_received_during_pass >= P_load + P_load (1-d) / (d eta_storage)`.

Here `eta_storage` is round-trip efficiency for the stored portion. This does not
guarantee that storage survives the longest gap. At 20% availability, 50 W
continuous demand and 90% storage efficiency require at least 272.2 W while
receiving. At 5%, the requirement becomes 1,105.6 W. A source serving several users
must additionally share its available beam time among them.

Illustrative energy requirements for a 354-hour night are 17.7 kWh at 50 W,
35.4 kWh at 100 W, and 354 kWh at 1 kW. With an **assumed** usable system specific
energy of 150 Wh/kg, those correspond to 118, 236 and 2,360 kg, before adding any
thermal overhead excluded from that assumption. Reducing survival demand is
therefore as valuable as improving transmission efficiency. These are energy
arithmetic, not predictions for a selected battery product.

## 2. Cable distribution is the benchmark to beat

NASA's 2024 Watts on the Moon finalists underwent a 48-hour test with a three-km
source-to-user power path and thermal-vacuum conditions. The winning H.E.L.P.S.
design used an 800 V cable and batteries at both ends. This is stronger evidence
than a conceptual antenna diagram, although it is not a lunar deployment.
[NASA competition results](https://www.nasa.gov/news-release/nasa-awards-1-5-million-at-watts-on-the-moon-challenge-finale/)

NASA's current catalog lists a MIPS cable for >10 kW at 3 kV over 1–3 km, an
Astrobotic 10 kV DC/10 kW cable concept extending to four km, and TULIPS combining
power and communications. Listed readiness levels are 5–6, depending on the
system. TYMPO targets >90% end-to-end delivery of 100 W–10 kW across tethers shorter
than ten km; that efficiency is a project objective, not a test result established
by this review. [NASA power technology catalog](https://www.nasa.gov/power/),
[TYMPO project](https://techport.nasa.gov/projects/116287)

An explicit conductor-only calculation shows the voltage trade. Assume two
aluminum conductors, resistivity `rho = 2.82e-8 ohm m` and density 2,700 kg/m³;
temperature effects, joints, insulation and converter losses are omitted:

`R_pair = 2 rho L / A`, `I = P_source / V_source`,
`P_line_loss = I² R_pair`, `mass_pair = 2 L A density`.

| One-way distance | Each conductor area | Source voltage | Source power | Conductor loss | Bare conductor mass |
| --- | --- | --- | --- | --- | --- |
| 1 km | 1 mm² | 3 kV | 10 kW | 627 W, 6.27% | 5.4 kg |
| 3 km | 3 mm² | 3 kV | 10 kW | 627 W, 6.27% | 48.6 kg |
| 3 km | 1 mm² | 10 kV | 10 kW | 169 W, 1.69% | 16.2 kg |

Higher voltage reduces conductor mass and loss, but requires a qualified
insulation/connector/converter system. These numbers do not establish a minimum
flight cable mass. Mechanical support, thermal cycling, dust, deployment and
repair can dominate. Include a dedicated return conductor: low near-surface lunar
conductivity makes an assumed ground return especially unconvincing. Cross-lunar
thousand-km cable deployment is a different infrastructure scale from these
local links.

## 3. Optical power delivery: useful power has been demonstrated

DARPA reported >800 W delivered electrically over 8.6 km for 30 seconds in its
2025 POWER demonstration. Its reported >20% efficiency was **laser optical output
to receiver electrical output at shorter distances**; it was not a wall-plug
efficiency measurement for the record-distance shot. The test was terrestrial.
[DARPA results](https://www.darpa.mil/news/2025/darpa-program-distance-record-power-beaming)

NASA's BEACON study gives a concrete lunar comparison: a concept supplying up to
500 W to a user at 1–10 km from a solar-powered tower. It allocates 3.8 kW to the
laser, ~1.6 kW optical output and a 1.5 m receiver, with allowances for beam
capture, cell packing, PV conversion and power management. Thus 500/3,800 is only
13.2% from laser electrical input to useful user power, excluding the rest of the
station. The complete concept is about 623 kg with margins. Its selected site
still has long shadow intervals; the laser stops when the source is dark.
This is a conceptual design, not flown hardware.
[BEACON engineering study, pp. 2–13](https://ntrs.nasa.gov/api/citations/20240014584/downloads/BEACON%20Final.pdf)

Reasonable implementation choices are a stationary receiver during charging,
closed-loop pointing, a protective shutter, measured receiver temperature, and a
buffer battery. A receiver advertised at high optical-to-electric efficiency
still needs a path for the unconverted heat. A second conversion at every active
relay compounds losses; a mirror relay can redirect a beam with less conversion
loss, at the cost of another aligned aperture and line of sight.

For terrain screening, on a smooth Moon of radius 1,737.4 km, a 15 m transmitter
and 1 m receiver have a combined geometric horizon of approximately
`sqrt(2Rh_tx) + sqrt(2Rh_rx) = 9.1 km`. Crater walls can shorten this drastically.
A tower alone does not establish far-side access or uninterrupted sunlight.

## 4. Periodic orbital charging is a credible far-side use case

NASA's *Power Beaming from Lunar Orbit for Small Science Landers* studies 50 W
night operation using 1.07 µm lasers. Its architecture has three orbital planes
at 800 km, 3 kW optical lasers, 1.4 m transmitting mirrors and 1.5 m receiving
arrays. Passes last roughly 10–35 minutes; storage bridges approximately three
hours rather than a whole night. The selected laser has 38% electrical-to-optical
efficiency; receiving PV conversion is around 50%. Each beamcraft is estimated
at 3,220 kg, including 1,084 kg of propulsion. A single orbiter can serve a
restricted latitude group in their scenario. This is an engineering concept,
not a current service or a demonstrated cost advantage for one payload.
[NASA orbital power study](https://ntrs.nasa.gov/api/citations/20230018143/downloads/PowerBeamingFromLunarOrbitForSmallScienceLanders.pdf)

**Recommendation:** investigate a chosen far-side site or latitude band and its
actual power schedule before optimizing global coverage. The valuable first
service is replenishing a small survival battery across repeated passes. A fleet
of low-power instruments may justify shared infrastructure more readily than one
instrument. Local solar uses the same receiving area during daytime if the
selected cell technology supports both illumination spectra.

The reason to prefer relatively close lunar orbit over distant L2 for compact
receivers is diffraction. For an ideal uniformly illuminated circular aperture
focused at the receiver, the first Airy null has radius
`r = 1.22 lambda range / D_tx`. At 1.064 µm:

| Range | Transmitting diameter | First-null beam radius |
| --- | --- | --- |
| 10 km | 0.1 m | 0.130 m |
| 1,000 km | 1 m | 1.30 m |
| 64,500 km | 1 m | 83.7 m |
| 64,500 km | 10 m | 8.37 m |

These are ideal focal-plane diffraction calculations; beam quality, oblique reception,
pointing, vibration and obscurations add loss. For a centred one-metre-diameter
receiver at 64,500 km, the ideal Airy-pattern capture fraction is only 0.0131%
with a one-metre transmitter and 1.30% with a ten-metre transmitter. Here
`fraction = 1 - J0(x)^2 - J1(x)^2`,
`x = pi D_tx radius_rx / (lambda range)`.

An L2 power-beaming paper assumes a one-metre receiver and adaptive transmitter
aperture, with five-to-fifty-nanoradian pointing errors. Its own aperture formula
implies about 69 m at 64,500 km. Enclosing the first Airy disk within a one-metre
receiver would require about 167 m. Its zero-elevation coverage mask also omits
terrain blockage. Therefore its coverage result is insufficient to establish
practical continuous energy delivery.
[Donmez and Kurt, equations 4–5 and Table I](https://arxiv.org/html/2402.16320v1)

## 5. Microwave power is real; aperture size remains the price

NRL reported 1.6 kW over approximately one km in a terrestrial 10 GHz
demonstration, using a rectenna to produce DC. This is a useful counterexample
to the claim that wireless energy itself is unrealistic. It does not validate a
compact far-side receiver fed from distant orbit.
[NRL demonstration](https://www.navy.mil/Press-Office/News-Stories/display-news/Article/3005894/nrl-conducts-successful-terrestrial-microwave-power-beaming-demonstration/)

At 35 GHz, a ten-metre aperture over 1,000 km has a first-null beam radius of
about 1.05 km by the same ideal diffraction calculation. Increasing frequency
helps enormously compared with ELF, but a metre-size rover remains a tiny target
in that beam. For short links with large apertures, use a focused Fresnel-field
calculation rather than applying far-field Friis blindly. Compare rectifier
efficiency at the **actual incident power density**, along with transmitter
efficiency and radiator mass. ESA's 35 GHz lunar-rover study built a demonstrator
with over 1,000 rectifying elements; its executive summary does not establish
flight delivery of useful watts over km distances.
[ESA project report](https://nebula.esa.int/sites/default/files/2024-11/C4000135862ESR.pdf)

## 6. Clever alternatives worth bounded experiments

**Redirect sunlight before converting it.** Near an illuminated polar ridge,
mirrors can supply a shadowed receiver without electrical-to-laser conversion.
NASA's Light Bender work targets this architecture. Its later robotic assembly
project describes ten-metre mirrors on a ten-metre mast and a concept for kW-class
delivery over several km. The reported prototype work demonstrates assembly;
it does not demonstrate the complete lunar power service. It deserves a ray-optics
and deployment trade against cable and laser delivery.
[NASA Light Bender](https://www.nasa.gov/general/light-bender/),
[robotic assembly project](https://techport.nasa.gov/projects/147012)

The finite apparent size of the Sun must be included. A simple uncollimated
reflection spreads over a scale of `range × 0.0093 rad`, approximately nine metres
per km, before the finite mirror size is included. A claimed compact remote solar
spot therefore needs a complete optical-throughput calculation including solar
angular extent and all intervening apertures. This screening argument is not a
refutation of the multi-element Light Bender design. Neither mirror nor laser
creates energy while its own source is in darkness.

**Use delivered heat deliberately.** This review proposes an optical receiver
that routes photovoltaic waste heat to a thermostatically controlled survival
enclosure, or accepts direct optical heating when electrical demand is low. With
an assumed 50% PV efficiency, 100 W absorbed optically yields about 50 W electrical
and up to 50 W heat before routing losses. Only the useful, controllable fraction
of that heat belongs in the service budget. A 50 W heater and a 50 W electrical
load might thus share one receiver; excessive or badly distributed heat instead
becomes a liability. The combination is a candidate engineering trade, not a
claim of scientific novelty.

**Bring the receiver close for the final charging step.** Cable-fed or
optically-fed docking stations can charge a rover through a sealed inductive
interface, avoiding a frequently mated dusty power connector. Choose a suitable
switching frequency and demonstrate coil alignment and efficiency across the
actual gap. NASA is developing proximity charging for lunar applications.
[NASA proximity-charger project overview](https://ntrs.nasa.gov/api/citations/20240011234/downloads/20240011234.pdf)

**Use transmission only where local production and storage lose.** A far-side
station can generate solar power locally during daylight. For continuous high
loads or permanent shadow, include local nuclear generation in a serious mission
trade. NASA's fission program describes a 40 kW-class development system;
this is a future capability, not presently available lunar infrastructure.
[NASA fission surface power](https://www.nasa.gov/exploration-systems-development-mission-directorate/fission-surface-power/)

## 7. Preserve the useful ELF science without confusing it with power

The existing repository's manuscript Figure 9 explicitly describes a transfer
**proxy**. Its normalized path response cannot supply antenna efficiency,
receiver power, matching loss or load voltage. Neither a large skin depth nor a
low cavity Q establishes a complete source-to-load result.

Receiving ELF for science is nevertheless practical. Lunar Magnetotelluric
Sounder hardware operated in 2025 with >50 m electrode baselines, a fluxgate on a
2.5 m mast and reported magnetic noise around 3 pT/sqrt(Hz). This supplies a
realistic sensing benchmark, not a power-harvesting result.
[LMS initial results](https://www.hou.usra.edu/meetings/leag2025/pdf/5063.pdf)

A 2026 team abstract reports that unexpectedly strong plasma conductivity and
magnetometer elevation attenuated the induction signal; its analysis emphasizes
surface-to-orbiter magnetic transfer functions. Any passive follow-on must model
sensor/plasma coupling and interference rather than assuming an ideal electrode
or noiseless magnetic receiver.
[LMS 2026 results](https://meetingorganizer.copernicus.org/EGU26/EGU26-8526.html)

## 8. Concrete next gate

Build one comparison around a selected mission: **50 W continuous far-side
survival service**, plus **500 W charging of a stationary receiver a few km from
a surface source**. These are review targets, not user-specified requirements.
For each, calculate integrated delivered watt-hours, longest outage and storage
state over an illumination/orbit/terrain timeline. Compare a qualified cable
baseline, optical delivery and local generation. Include receiver and source
radiators, conversion losses, aperture deployment and spare capacity.

For a ground prototype, the acceptance measurement should be regulated receiver
DC energy divided by source DC energy over a complete charge/discharge cycle,
including pointing and controls. For a heating variant, separately calorimeter
the delivered useful heat. Detecting a coherent field, producing an open-circuit
voltage, or reporting laser optical watts is not that acceptance test.

An initial numerical screen is now reproducible in
[`09_night_service_sensitivity.py`](../scripts/09_night_service_sensitivity.py).
With an **assumed** 18-minute charging window and 162-minute gap, a 50 W load needs
550 W receiver DC during charging at 90% storage round-trip efficiency. The ideal
1 m transmitter and 1.5 m receiver at 1,000 km give 68.276% capture at 1.064 µm:
40% laser and 50% PV efficiencies then require 4.028 kW source DC. A fixed 0.5 m
pointing offset raises this to 5.567 kW. The zero-offset thermal budget assigns
2.417 kW of non-optical laser input to source heat and **up to 550 W** of captured
non-DC optical power to receiver heat. The receiver allocation assumes complete
absorption; reflection or transmission can lower heat without increasing DC
output. Beam power missing the receiver is not receiver heat. It needs 135 Wh
usable storage for the assumed gap; separately, three
hours at 50 W is 150 Wh. Independent soulkiller and NUKA executions agree, and
quadrature convergence and analytic-centre checks pass.
[`Night-service evidence and limitations`](../results/antenna_review_2026-09-05/night_service/README.md)

No evaluated primary source demonstrates global ELF delivery of useful lunar
power. The viable paths found here use known energy conversion and distribution
methods, with the most promising development opportunity being reliable,
scheduled power service to small instruments during darkness.
