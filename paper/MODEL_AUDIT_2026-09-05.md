# Adversarial model audit: what the existing code can say about lunar power transfer

Reviewed 2026-09-05. Numerical source baseline: `d939c36609a36295d0f3819187baaba95fdcd545`. The independently fetched README at `41bd2da0a390f6b9a99ac8f4dc73af2aef6b1e9a` supplies additional planetary wireless-power framing; its changes do not change the audited numerical source. Existing production code, tables, and figures were preserved in this audit.

**Conclusion:** this repository contains useful conductivity and wall-impedance calculations, but it does not yet calculate transmitted or received electrical power. Its broad numerical claims about cavity quality and independent eigenmode validation have material defects. These defects do not establish viable planetary ELF wireless power. They establish that the existing proxies cannot settle that question or rank practical antennas.

For the requested energy application, a candidate must specify transmitter electrical input, actual current distribution, source impedance and matching loss, the propagation geometry, receiver mutual impedance or aperture, receiver loss and load, and conversion to usable DC watts. No existing production path provides this chain. Losing a free oscillation rapidly does not prevent a continuously driven source from supplying a load; the question becomes the required input power and achievable efficiency.

## Findings, ordered by consequence

### M0 — High: normalized transfer proxies cannot substantiate delivered-power claims

**Locations:** `scripts/03_driven_transfer.py:44–53,80–94`; `src/lunar_elf/sphere/impedance.py:127–135`; `paper/paper.html:392–400`; README historical-context and artificial-ionosphere sections at the fetched revision.

The plotted source–receiver quantity is bulk plane-wave attenuation evaluated along a prescribed great-circle arc. The other plotted response is normalized `1/abs(Zg+Zi)`. Neither contains an antenna, a source normalization, a receiving load, or an outgoing-wave solution. The open-Moon branch directly returns `Q=0` as a label for the absence of its assumed upper wall. It does not compute the radiative quality factor of an antenna or induced power at another site.

Consequently, the repository does not calculate a transmitter-to-load efficiency, and its attenuation plot is not a link budget. In particular, a forced current, near-field loop coupling, surface-to-orbit beam, and a wave constrained to propagate through rock are different boundary-value problems. A result for the last one cannot rule out the others.

**Minimum remedy:** retain the bulk-attenuation results as explicitly defined material/path diagnostics. Add a port-normalized power model for each candidate. Compare watts delivered per kilogram, installation length/area, and available input watt. For far-side delivery, include occultation and relay/storage needs. Do not treat a change in cavity `Q` alone as a power-transfer solution.

### M1 — High: the advertised eigenmode cross-check returns the original impedance estimate

**Locations:** `src/lunar_elf/sphere/eigenmodes.py:129–174`; `paper/OPTIONAL_REPORT.md:16–43`.

`find_mode_real_axis_q` never calls the Riccati integrator or cavity characteristic. It scans wall admittance, returns the same impedance formula as `Q`, and constructs a complex frequency from a width estimate. The field named `residual` is the *height* of the response, not a characteristic residual near zero. These values are not independent eigenfrequencies or an independent validation of the wall formula.

For every named profile in the independent replay, the alleged fundamental frequency is **11.6513774062 Hz**, exactly the lower scan endpoint `0.3*f_ideal`. The optional published table also repeatedly has that endpoint. A monotonic wall response with an endpoint maximum has no bracketed resonance whose width can identify a pole.

**Minimum remedy:** relabel these outputs as wall-admittance diagnostics and reject endpoint maxima as resonance measurements. For an actual modal check, impose the correct vector boundary conditions, solve a complex-frequency characteristic, report its residual, and demonstrate spatial and root convergence. A real cross-check must not simply return the quantity being checked.

### M2 — High: the cavity formula fails an elementary weak-loss energy balance by a factor of two

**Locations:** `src/lunar_elf/sphere/impedance.py:136–138`; `src/lunar_elf/lateral.py:92`; `paper/paper.html:283–289`.

For peak phasors in a thin vacuum TEM cavity with unit footprint, let the magnetic field amplitude be `H`. Equal integrated electric and magnetic energies give total stored energy `U = mu0*h*|H|^2/2`. The two walls dissipate `P = (Rg+Ri)*|H|^2/2`. Therefore `Q = omega*U/P = omega*mu0*h/(Rg+Ri)`. The repository divides this by another two.

The independent test uses `f=10 Hz`, `h=100 km`, and `Rg=Ri=0.01 ohm`: energy balance gives **394.784176**, whereas the repository returns **197.392088**. These low wall losses place the check in the perturbative regime. Galejs' primary Schumann-resonance derivation, Appendix equations (14)–(19), also reduces to `Q=omega*mu0*h/Re(Zs)` at the ideal PEC frequency with one lossy wall. [Galejs, *Schumann resonances*, NBS, 1965](https://nvlpubs.nist.gov/nistpubs/jres/69D/jresv69Dn8p1043_A1b.pdf).

**Minimum remedy:** derive and validate the chosen approximation and conventions before regenerating quantitative claims. **Do not infer that the actual lunar eigenmode `Q` is simply twice the table**: a perturbation formula evaluated at an ideal frequency is uncontrolled when it predicts `Q` of order one and the lossy boundary also shifts frequency and stored energy. The Earth smoke test inherits this same formula and cannot independently validate it.

### M3 — High: the shell-path “Q upper bound” mixes incompatible propagation constants

**Locations:** `src/lunar_elf/sphere/energy_q.py:119–133`; `paper/QUANTITATIVE_RESULTS.md:11,40`.

The code combines good-conductor attenuation `alpha=sqrt(omega*mu*sigma/2)` with dielectric phase constant `beta=omega*sqrt(mu*epsilon)` and calls `beta/(2*alpha)` an upper bound. In a conductive medium, the same complex wavenumber sets both constants. A *larger* assumed phase speed makes this ratio smaller, so the stated direction of the bound does not follow.

At 10 Hz, using the nominal effective conductivity and `epsilon_r=5.5`, the claimed upper value is **0.1079738**; the repository's own exact material wavenumber gives `Re(k)/[-2 Im(k)] = 0.5117942`. For the warm profile the comparison is **0.0112573 versus 0.5001267**. The inequality already fails within its own homogeneous material model.

**Minimum remedy:** remove the upper-bound designation. Use consistent complex propagation constants for homogeneous diagnostics. Even that propagation ratio is not automatically a temporal eigenmode quality factor in a strongly lossy dispersive system, and is not an antenna-efficiency calculation.

### M4 — Medium: effective shell conductivity changes under pure re-tabulation

**Locations:** `src/lunar_elf/skin.py:72–81`; `src/lunar_elf/profiles.py:90–97`.

The “outer 300 km log mean” averages sample values without depth weights, but the grid is logarithmically concentrated near the surface. Identical log-linear physical profiles sampled on three uniformly spaced depths and five surface-dense depths return **1.000e-6** and **2.0893e-7 S/m**, respectively. The exact depth-weighted geometric mean is **1.000e-6 S/m** in both cases.

For the four existing named profiles, a depth-weighted log mean is **2.65–4.76 times** the current sample-count mean. In the nominal profile it changes `1.3123e-7` to `6.2510e-7 S/m`; the corresponding homogeneous skin-attenuation proxy changes by the square root of that ratio. This is not a correction to a true spherical propagation solution: neither averaging rule by itself derives an effective antenna channel.

**Minimum remedy:** name and implement the intended physical weighting, including exact shell endpoints, then test invariance under re-tabulation. Keep material averaging separate from a justified propagation model.

### M5 — Medium: spectrum Q uses half amplitude instead of half power

**Location:** `src/lunar_elf/sphere/cavity.py:187–234`.

The function explicitly accepts an amplitude response but computes its width at half amplitude. A synthetic amplitude Lorentzian with known half-power `Q=100` returns **57.735026**, the expected erroneous factor `1/sqrt(3)`. The production “eigenmode” helper has the same half-amplitude issue, in addition to the absence of a resonance.

**Minimum remedy:** specify whether the input is amplitude or power and use the appropriate threshold (`peak/sqrt(2)` for amplitude), require both crossings, and reject clipped or unbracketed peaks.

### M6 — High for proposed solver reuse: the dormant characteristic ignores its ionosphere

**Locations:** `src/lunar_elf/sphere/eigenmodes.py:100–119`; `src/lunar_elf/sphere/impedance.py:102`.

`cavity_characteristic` computes both `Zg` and `Zi` but neither appears in its returned value. Changing ionospheric conductivity by **a factor of one million**, from `1e-8` to `1e-2 S/m`, gives exactly the same characteristic in the replay. Calling the advertised complex-frequency function at `10+0.1j Hz` raises a `TypeError` through real-valued skin-depth conversion. The module also states that negative imaginary frequency decays under `exp(+j omega t)`; the decaying sign for that convention is positive.

The separate radial-transfer module's claimed TM interface continuity also needs derivation before use: for the common tangential-magnetic radial variable, continuity requires a derivative weighted by complex permittivity, not the unchanged `u'` propagated through every conductivity jump. The energy helper uses uncalibrated electric and magnetic field proxies. None of these unused helpers should be promoted to a delivered-power solver without analytic benchmarks.

**Minimum remedy:** derive one consistent field variable and time convention, impose all interfaces and radiation/load boundaries, support analytic complex-frequency evaluation, and validate against homogeneous spheres and simple lossy cavities.

### M7 — High claim-scope issue: the checked-in sensitivity sweep already exceeds Q = 2

**Evidence:** `results/campaign/iono_sensitivity.csv`, 972 rows; extrema preserved with the source digest in `sensitivity_extrema.json` beside the replay.

The checked-in proxy results contain `pessimistic_warm`, `h=200 km`, `sigma_iono=1e-3 S/m` with **Q=7.480575** for `n=1`, and **Q=11.626608** for `n=3`. The `Q~2` maximum applies to the particular `h=100 km`, `sigma_iono=1e-5 S/m` campaign. It is not a demonstrated maximum over artificial upper boundaries. The fetched README's “most favorable simple artificial boundary” wording is contradicted by the repository's own sweep.

**Minimum remedy:** scope every table and conclusion to the assumed boundary parameters. An engineered global ionosphere still requires an independently justified construction, maintenance, and net-energy budget; these larger proxy values are not evidence for practical power transfer.

## Additional checks and practical interpretation

The angular-transfer plot has a geometric-spreading sign reversal: `scripts/03_driven_transfer.py:34–37` produces a field change, then lines 69–70 subtract it as if it were positive attenuation. From 10 to 90 degrees its isolated contribution is **+7.6033 dB**, where the stated cylindrical-spreading assumption gives **-7.6033 dB**. This also highlights that its antipodal behavior is an imposed geometric proxy, not a wave solution.

The headline that loss tangent is always much greater than one is too strong for all supplied profiles and frequencies. The optimistic named profile's current shell statistic gives **1.9143 at 30 Hz**, a transition to only moderately conduction-dominated response. The exact complex wavenumber should be used when assessing such cases. This does not imply low-loss transmission through the whole Moon.

For the energy task, the justified next calculations are conventional port-normalized models of local inductive coupling, line-of-sight RF/optical transfer with explicit relays, and a cable benchmark. High antenna resonance `Q`, high planetary-cavity `Q`, low bulk attenuation, and high end-to-end DC efficiency are different quantities. The current evidence neither demonstrates a practical global ELF power system nor prohibits all lunar wireless power.

## Reproduction and evidence

Artifacts are under [`results/antenna_review_2026-09-05/model_audit/`](../results/antenna_review_2026-09-05/model_audit/). Source SHA-256 maps are embedded in both JSON replays. Numeric source hashes and all resulting diagnostic values match exactly between **soulkiller** (Python 3.14.4, NumPy 2.4.4, SciPy 1.17.1) and **NUKA** (Python 3.14.4, NumPy 2.3.5, SciPy 1.18.1). This is independent execution of the diagnostic calculations, not independent validation of all physical assumptions. Nuka used the isolated directory `/tmp/lunar-elf-review-20260905-model`; other remote checkouts were untouched. GPU work is unnecessary for these small analytic counterexamples.

From the repository root:

```bash
python results/antenna_review_2026-09-05/model_audit/reproduce.py
python -m pytest -q -rx tests/test_skin.py tests/test_adversarial_models.py
python -m pytest -q --runxfail tests/test_adversarial_models.py
```

The original suite passes **2/2**. The expanded suite reports **2 passed, 6 strict expected failures**. These are explicitly unresolved regression targets; running with `--runxfail` produces **six assertion failures**, as recorded in `pytest_runxfail.txt`. The expected-failure status does not represent repaired source. Nuka lacked pytest, so its verification used the complete numerical replay script; `pytest_nuka.txt` records that limitation. The 20,000-draw Monte Carlo campaign was not rerun: the critical findings are analytic counterexamples and direct inspection, not sampling uncertainty that further identical draws would resolve.

Exact remote copy/replay commands:

```bash
ssh -F /home/nick/.ssh/mesh.config nuka 'mkdir -p /tmp/lunar-elf-review-20260905-model'
rsync -a -e 'ssh -F /home/nick/.ssh/mesh.config' src tests results/antenna_review_2026-09-05/model_audit/reproduce.py nuka:/tmp/lunar-elf-review-20260905-model/
ssh -F /home/nick/.ssh/mesh.config nuka 'python3 /tmp/lunar-elf-review-20260905-model/reproduce.py --repository /tmp/lunar-elf-review-20260905-model'
```

`SHA256SUMS.txt` covers the replay, captured outputs, regression targets, and this report.
