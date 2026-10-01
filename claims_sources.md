# Sources for the claim corrections

Sources retrieved 2026-10-01 from `https://raw.githubusercontent.com/luckyseoul/lunar-elf/main/<path>` at `main` commit `8aa7940863de40c6eb71b1cf34ba37a1127ef260` (committer timestamp `2026-09-05T12:59:04Z`, 7:59 AM CT). Line numbers refer to the files at that commit. `paper/ENERGY_DELIVERY_REVIEW_2026-09-05.md` is not a source for these corrections; loop-power claims from that review are not used.

Line numbers below refer to those files. Quotes are the sentences used in the claim corrections. Numerical replacements appear only in the audit quotes or in the claim-file quotes.

---

## `paper/MODEL_AUDIT_2026-09-05.md`

Baseline stated in the file (lines 1–5):

> Reviewed 2026-09-05. Numerical source baseline: `d939c36609a36295d0f3819187baaba95fdcd545`. The independently fetched README at `41bd2da0a390f6b9a99ac8f4dc73af2aef6b1e9a` supplies additional planetary wireless-power framing; its changes do not change the audited numerical source.

Conclusion (lines 5–7):

> **Conclusion:** this repository contains useful conductivity and wall-impedance calculations, but it does not yet calculate transmitted or received electrical power. Its broad numerical claims about cavity quality and independent eigenmode validation have material defects. These defects do not establish viable planetary ELF wireless power. They establish that the existing proxies cannot settle that question or rank practical antennas.

> For the requested energy application, a candidate must specify transmitter electrical input, actual current distribution, source impedance and matching loss, the propagation geometry, receiver mutual impedance or aperture, receiver loss and load, and conversion to usable DC watts. No existing production path provides this chain. Losing a free oscillation rapidly does not prevent a continuously driven source from supplying a load; the question becomes the required input power and achievable efficiency.

### M0 (lines 11–17)

> The plotted source–receiver quantity is bulk plane-wave attenuation evaluated along a prescribed great-circle arc. The other plotted response is normalized `1/abs(Zg+Zi)`. Neither contains an antenna, a source normalization, a receiving load, or an outgoing-wave solution. The open-Moon branch directly returns `Q=0` as a label for the absence of its assumed upper wall. It does not compute the radiative quality factor of an antenna or induced power at another site.

> Consequently, the repository does not calculate a transmitter-to-load efficiency, and its attenuation plot is not a link budget. In particular, a forced current, near-field loop coupling, surface-to-orbit beam, and a wave constrained to propagate through rock are different boundary-value problems. A result for the last one cannot rule out the others.

### M1 (lines 21–27)

> `find_mode_real_axis_q` never calls the Riccati integrator or cavity characteristic. It scans wall admittance, returns the same impedance formula as `Q`, and constructs a complex frequency from a width estimate. The field named `residual` is the *height* of the response, not a characteristic residual near zero. These values are not independent eigenfrequencies or an independent validation of the wall formula.

> For every named profile in the independent replay, the alleged fundamental frequency is **11.6513774062 Hz**, exactly the lower scan endpoint `0.3*f_ideal`. The optional published table also repeatedly has that endpoint. A monotonic wall response with an endpoint maximum has no bracketed resonance whose width can identify a pole.

### M2 (lines 31–39)

> For peak phasors in a thin vacuum TEM cavity with unit footprint, let the magnetic field amplitude be `H`. Equal integrated electric and magnetic energies give total stored energy `U = mu0*h*|H|^2/2`. The two walls dissipate `P = (Rg+Ri)*|H|^2/2`. Therefore `Q = omega*U/P = omega*mu0*h/(Rg+Ri)`. The repository divides this by another two.

> The independent test uses `f=10 Hz`, `h=100 km`, and `Rg=Ri=0.01 ohm`: energy balance gives **394.784176**, whereas the repository returns **197.392088**. These low wall losses place the check in the perturbative regime. Galejs' primary Schumann-resonance derivation, Appendix equations (14)–(19), also reduces to `Q=omega*mu0*h/Re(Zs)` at the ideal PEC frequency with one lossy wall.

> **Minimum remedy:** derive and validate the chosen approximation and conventions before regenerating quantitative claims. **Do not infer that the actual lunar eigenmode `Q` is simply twice the table**: a perturbation formula evaluated at an ideal frequency is uncontrolled when it predicts `Q` of order one and the lossy boundary also shifts frequency and stored energy. The Earth smoke test inherits this same formula and cannot independently validate it.

### M3 (lines 41–49)

> The code combines good-conductor attenuation `alpha=sqrt(omega*mu*sigma/2)` with dielectric phase constant `beta=omega*sqrt(mu*epsilon)` and calls `beta/(2*alpha)` an upper bound. In a conductive medium, the same complex wavenumber sets both constants. A *larger* assumed phase speed makes this ratio smaller, so the stated direction of the bound does not follow.

> At 10 Hz, using the nominal effective conductivity and `epsilon_r=5.5`, the claimed upper value is **0.1079738**; the repository's own exact material wavenumber gives `Re(k)/[-2 Im(k)] = 0.5117942`. For the warm profile the comparison is **0.0112573 versus 0.5001267**. The inequality already fails within its own homogeneous material model.

> **Minimum remedy:** remove the upper-bound designation.

### M4 (lines 51–57)

> The “outer 300 km log mean” averages sample values without depth weights, but the grid is logarithmically concentrated near the surface. Identical log-linear physical profiles sampled on three uniformly spaced depths and five surface-dense depths return **1.000e-6** and **2.0893e-7 S/m**, respectively. The exact depth-weighted geometric mean is **1.000e-6 S/m** in both cases.

> For the four existing named profiles, a depth-weighted log mean is **2.65–4.76 times** the current sample-count mean. In the nominal profile it changes `1.3123e-7` to `6.2510e-7 S/m`; the corresponding homogeneous skin-attenuation proxy changes by the square root of that ratio. This is not a correction to a true spherical propagation solution: neither averaging rule by itself derives an effective antenna channel.

### M5 (lines 61–65)

> The function explicitly accepts an amplitude response but computes its width at half amplitude. A synthetic amplitude Lorentzian with known half-power `Q=100` returns **57.735026**, the expected erroneous factor `1/sqrt(3)`. The production “eigenmode” helper has the same half-amplitude issue, in addition to the absence of a resonance.

### M6 (lines 69–75)

> `cavity_characteristic` computes both `Zg` and `Zi` but neither appears in its returned value. Changing ionospheric conductivity by **a factor of one million**, from `1e-8` to `1e-2 S/m`, gives exactly the same characteristic in the replay. Calling the advertised complex-frequency function at `10+0.1j Hz` raises a `TypeError` through real-valued skin-depth conversion.

> None of these unused helpers should be promoted to a delivered-power solver without analytic benchmarks.

### M7 (lines 79–85)

> The checked-in proxy results contain `pessimistic_warm`, `h=200 km`, `sigma_iono=1e-3 S/m` with **Q=7.480575** for `n=1`, and **Q=11.626608** for `n=3`. The `Q~2` maximum applies to the particular `h=100 km`, `sigma_iono=1e-5 S/m` campaign. It is not a demonstrated maximum over artificial upper boundaries. The fetched README's “most favorable simple artificial boundary” wording is contradicted by the repository's own sweep.

> An engineered global ionosphere still requires an independently justified construction, maintenance, and net-energy budget; these larger proxy values are not evidence for practical power transfer.

### Loss tangent, angular transfer, historical scope (lines 87–93)

> The angular-transfer plot has a geometric-spreading sign reversal: `scripts/03_driven_transfer.py:34–37` produces a field change, then lines 69–70 subtract it as if it were positive attenuation. From 10 to 90 degrees its isolated contribution is **+7.6033 dB**, where the stated cylindrical-spreading assumption gives **-7.6033 dB**. This also highlights that its antipodal behavior is an imposed geometric proxy, not a wave solution.

> The headline that loss tangent is always much greater than one is too strong for all supplied profiles and frequencies. The optimistic named profile's current shell statistic gives **1.9143 at 30 Hz**, a transition to only moderately conduction-dominated response. The exact complex wavenumber should be used when assessing such cases. This does not imply low-loss transmission through the whole Moon.

> High antenna resonance `Q`, high planetary-cavity `Q`, low bulk attenuation, and high end-to-end DC efficiency are different quantities. The current evidence neither demonstrates a practical global ELF power system nor prohibits all lunar wireless power.

The audit does not quote the headline set “median Q≈0.78, max Q≈2.0, 100% Q<5, named Q 0.35/0.58/0.44/2.01” as its own measurements. Those digits are taken from the claim files below and, consistent with the scope stated in M7, are historical proxy outputs only at `h=100 km` and `sigma_iono=1e-5 S/m`.

---

## `paper/paper.html`

Title (line 105): “The Lunar Outer Shell as a Weakly Conducting, Large–Skin-Depth Medium at Extremely Low Frequencies.”

Abstract claims used (lines 115–128):

> At 1–30 Hz, literature-bracketed outer-shell conductivities yield loss tangents \(\tan\delta=\sigma/(\omega\varepsilon)\gg 1\): conduction current dominates displacement current. The outer shell is therefore a *weakly conducting medium with large skin depth*, not a low-loss dielectric. Without a conducting ionosphere there is no closed Earth-like Schumann cavity. Even granting a hypothetical 100 km ionosphere, impedance-method cavity quality factors remain \(Q\lesssim 2\) across named profiles, and a 20 000-draw Monte Carlo over the conductivity envelope finds median \(Q\simeq 0.78\), 95th percentile \(Q\simeq 1.85\), and maximum \(Q\simeq 2.0\) (100% of draws have \(Q<5\)). Nearside–farside and Procellarum KREEP Terrane contrasts alter path attenuation but do not create a high-\(Q\) resonator.

§1 (lines 137–139):

> Prior qualitative arguments have sometimes described the outer shell as a “low-loss dielectric.” That terminology is tested here against published conductivity structure and explicit modal quality-factor estimates.

Skin-depth definition left unchanged (lines 193–199):

> \(\displaystyle \delta=\sqrt{\frac{2}{\omega\mu\sigma}}\,,\)

> For \(f=10\) Hz and \(\sigma=10^{-7}\) S/m with \(\mu=\mu_0\), \(\delta\approx 500\) km.

Loss tangent definition (lines 204–211), including the round example the audit does not replace:

> \(\displaystyle \tan\delta=\frac{\sigma}{\omega\varepsilon}\,.\)

> Thus for \(\sigma=10^{-7}\) S/m, \(\tan\delta\sim 30\)–50 \(\gg 1\): conduction current dominates. A true low-loss dielectric would require \(\tan\delta\ll 1\), i.e. \(\sigma\ll 10^{-9}\) S/m at 10 Hz.

Figure 2 caption (lines 217–219):

> Loss tangent \(\tan\delta=\sigma/(\omega\varepsilon)\) for outer-shell (0–300 km) log-mean conductivity of the synthetic profile suite. Values \(\gg 1\) indicate conduction-dominated (weakly conducting) behavior across 1–100 Hz.

Attenuation claim (lines 232–235):

> Half-circumference field attenuations of tens to hundreds of decibels show that shell-guided global standing waves are not viable for nominal and midmantle-resolved profiles.

Table 1 caption and body (lines 240–255). Caption: “Outer-shell (0–300 km log-mean) metrics at 10 Hz for literature-anchored profiles.” Body used only as the manuscript’s own rounding, checked against `OPTIONAL_REPORT.md`: Grimm LF preferred \(1.4\times 10^{-7}\), 429 km, 45, 111 dB; Mittelholz-like \(1.6\times 10^{-6}\), 125 km, 530, 379 dB; Hood-class \(3.0\times 10^{-8}\), 917 km, 9.9, 52 dB; Grimm HF \(5.7\times 10^{-6}\), 67 km, 1850, 710 dB.

Figure 4 caption (lines 262–264):

> Circumferential path attenuation (half lunar circumference) for the synthetic profile suite, illustrating strong global-shell damping at ELF for all but the most extremely resistive end-members.

No-ionosphere sentence kept, and the defective formula (lines 270–289):

> Ideal closed-cavity Schumann frequencies for a sphere of lunar radius \(R\) are \(f_n=(c/2\pi R)\sqrt{n(n+1)}\), so \(f_1\approx 38.8\) Hz. The physical Moon has no dense conducting ionosphere to form the upper wall of an Earth-like cavity (Model A).

> \(\displaystyle Q\approx\frac{\omega\mu_0 h}{2\,\mathrm{Re}(Z_g+Z_i)}\,.\)

> An Earth validation stack (Model C) recovers \(Q\sim 4\)–6 for the first three multipoles—order-of-magnitude agreement with terrestrial Schumann \(Q\) of a few to ten.

Table 2 caption (lines 294–295): “Model B cavity \(Q\) (artificial 100 km ionosphere) at ideal multipole frequencies for literature and regional columns. Primary metric: impedance method (Eq. 3).” Body digits left as historical outputs (Grimm LF 0.78 / 0.64 / 0.45 through PKT 0.94 / 0.93 / 0.86).

Ringing (lines 317–318):

> Ringing times \(\tau\approx Q/(\pi f_1)\) are a few milliseconds for \(Q\sim 1\) at \(f_1\sim 39\) Hz—orders of magnitude too short for a sustained global ring.

Figure 5 caption (lines 324–325):

> Fundamental-mode cavity \(Q\) for literature and regional profiles under Model B (\(h=100\) km). All values remain \(\mathcal{O}(1)\), far below high-\(Q\) resonator behavior.

§4.1 (lines 331–342):

> median \(Q=0.78\);

> 5th / 95th percentiles: \(0.30\) / \(1.85\);

> maximum \(Q=2.01\);

> **100% of draws have \(Q<5\)**; 65% have \(Q<1\).

> No high-\(Q\) island appears in the envelope.

Figure 6 caption (lines 348–350):

> Monte Carlo distribution of Model B fundamental-mode \(Q\) (20 000 draws). Median and 95th percentile are marked; the entire support lies well below terrestrial Schumann \(Q\).

Figure 7 caption (lines 357–359):

> Monte Carlo \(Q\) versus outer-shell effective conductivity. More conductive walls lower \(\mathrm{Re}(Z_g)\) and can raise \(Q\) slightly, but values remain \(\lesssim 2\) across the envelope.

§5 (lines 365–371):

> Two equal-area hemisphere combinations yield effective cavity \(Q\sim 0.8\)–0.9—still \(\mathcal{O}(1)\). Piecewise great-circle paths at 10 Hz give \(\sim\)36 dB (farside) to \(\sim\)268 dB (PKT) of attenuation over 90°, and \(\sim\)137 dB on a mixed path through PKT. Lateral contrast modulates transmission but does not produce a high-\(Q\) global mode.

Figure 9 caption (lines 385–386):

> Source–receiver transfer proxy versus angular separation for a nominal outer-shell conductivity (path attenuation plus geometric spreading).

§6 bullets used (lines 396–400):

> Model B ionospheres are artificial proxies for bounding \(Q\); the physical Moon lacks this wall.

> Full three-dimensional Maxwell solutions with continuous lateral structure remain future work; the regional path and two-hemisphere estimates bound the effect of first-order asymmetry.

> Displacement current and vacuum radiation for the open Moon are not treated as a closed eigenvalue problem; Model A is geometric (no cavity), not a leaky-mode catalog.

The last of these is left in place. Also left: vertical-resolution bullet and the Mittelholz “not a point digitization” bullet (lines 392–395).

Conclusion (lines 405–413):

> Loss tangents satisfy \(\tan\delta\gg 1\) at 1–30 Hz. The absence of a conducting ionosphere precludes a closed Schumann-type cavity; even with a hypothetical ionosphere, cavity quality factors remain \(Q\lesssim 2\) across the explored envelope. Lateral nearside–farside and PKT structure modulates path attenuation but does not enable high-\(Q\) global resonances.

Acknowledgments (lines 418–419):

> Quantitative results were produced with the open `lunar-elf` modeling package (layered surface-impedance cavity \(Q\), path integrals, Monte Carlo, and regional path experiments).

Conductivity inputs left unchanged (lines 164–171): Dyal and Parkin (1977) “\(\sigma\lesssim 10^{-8}\) S/m for depths \(\lesssim 80\) km”; Grimm (2023) “\(\sigma=1.76\times 10^{-4}\,\exp(z_{\mathrm{km}}/210)\) S/m”; HF envelope “retained only as an upper bound (Grimm argues HF is likely biased high).”

---

## `paper/QUANTITATIVE_RESULTS.md`

Header constants (lines 5–7): “Moon radius R = 1737.4 km”; “c = 2.997925e+08 m/s”; “Ideal closed-cavity Schumann f₁ = (c/2πR)√2 = **38.84 Hz**”.

Method (lines 11–12):

> 1. **Phase 0** — outer-shell (0–300 km) log-mean σ_eff; skin depth δ=√(2/ωμσ); loss tangent tanδ=σ/(ωε); circumferential path attenuation; shell-path Q upper bound Q ≲ β/(2α) with β=ω√(με).
> 2. **Phase 1** — planar layered surface-impedance recursion looking into σ(r); Model **A** open Moon (no ionosphere ⇒ no cavity); Model **B** artificial ionosphere at 100 km with Q ≈ ωμ₀h / [2 Re(Z_g+Z_i)]; Model **C** Earth validation.

Phase 0 cells cited: optimistic_cold at 30 Hz, tanδ `1.91e+00` (line 21); nominal σ_eff `1.31e-07` and 10 Hz Q_path `0.108` (line 23); pessimistic_warm 10 Hz Q_path `0.0127` (line 29); apollo_classic 30 Hz tanδ `7.50e+00` (line 27).

Terminology note (lines 34):

> Across the nominal and Apollo-style envelopes at 1–30 Hz, **tanδ ≫ 1**: conduction current dominates.

Model A (lines 40):

> No conducting ionosphere ⇒ **no Earth-like closed Schumann cavity** (cavity Q ≡ 0 in the impedance formula). Shell-path upper bounds for any would-be circumferential standing wave in the outer shell:

Model A warm 10 Hz Q_path cell used for the rounding note: `0.0113` (line 58). Nominal 10 Hz Q_path in that block: `0.108` (line 50).

Model B pessimistic_warm row (lines 76–78): Q_cavity `2.01`, `2.63`, `3.12` at n = 1, 2, 3; n = 1 Q_path `0.0222`. Named n = 1 Q_cavity: optimistic_cold `0.348` (line 67), nominal `0.577` (line 70), apollo_classic `0.444` (line 73).

Model C (lines 84–88):

> | 1 | 10.59 | 1.469e-01 | 3.69 |
> | 2 | 18.34 | 1.934e-01 | 4.85 |
> | 3 | 25.94 | 2.300e-01 | 5.77 |

> Earth ideal f₁ ≈ 10.6 Hz (PEC formula); observed Earth Schumann is ~7.8 Hz with ionosphere corrections. Expected cavity Q of order **few–tens** for a reasonable ground+ionosphere stack — use as smoke test, not a precision Earth model.

Ringing table (lines 92–99): “τ_ring ≈ Q / (π f). Short τ ⇒ no sustained global ring.” Times: `0.003`, `0.005`, `0.004`, `0.016` s at f₁ `38.84` Hz for Q `0.348`, `0.577`, `0.444`, `2.01`.

Paper-ready claims (lines 103–107):

> 1. At 1–30 Hz, literature-bracketed outer-shell conductivities give **tanδ ≫ 1** (conduction-dominated)
> 2. Without an ionosphere (**Model A**), there is **no closed global cavity**.
> 3. Even with a **hypothetical** 100 km ionosphere (**Model B**), cavity Q is set by Re(Z_g)+Re(Z_i) and remains modest for conductive profiles
> 4. Circumferential shell paths span many skin depths for nominal σ (half-circumference attenuations of tens to hundreds of dB), so shell-guided global standing waves are not supported.
> 5. Scope is **1-D radial stratification** (layered impedance + path integrals). Lateral heterogeneity is future work.

Claims 2 and 5 are left. Claim 2 is read as geometry.

---

## `paper/CAMPAIGN_REPORT.md`

Monte Carlo block (lines 5–16):

> ## Monte Carlo cavity Q (Model B, n=1, h=100 km)

> - N draws: **20000**
> - median Q: **0.778**
> - mean Q: **0.923**
> - p05 / p95: **0.295** / **1.85**
> - max Q: **2.01**
> - fraction Q < 1: **64.7%**
> - fraction Q < 5: **100.0%**
> - fraction Q < 10: **100.0%**

> Interpretation: across the literature-bracketed envelope, high-Q global modes (Q≳10) are essentially absent under Model B; the physical open Moon (Model A) has no cavity at all.

Named n = 1 Q (lines 22–31): apollo_classic `0.444`, nominal `0.577`, optimistic_cold `0.348`, pessimistic_warm `2.01`. pessimistic_warm n = 3 Q is `3.11` (line 33), which is not the same print as quantitative `3.12`. Both prints are retained.

This file does not state `sigma_iono`. The \(1\times 10^{-5}\) S/m scope is taken from the M7 quote above, not from this report.

---

## `paper/OPTIONAL_REPORT.md`

§1 conductivity upper-bound sentence left as a Grimm HF statement (line 7):

> HF envelope retained as upper bound only.

§1 table (lines 11–14), used only to check manuscript Table 1 rounding: grimm_lf_preferred `1.38e-07`, δ `428.5`, tanδ `4.51e+01`, A `110.6`; mittelholz_like `1.62e-06`, `125.1`, `5.29e+02`, `379.1`; hood_upper_resistive `3.01e-08`, `916.9`, `9.85e+00`, `51.7`; grimm_hf_envelope `5.67e-06`, `66.8`, `1.85e+03`, `709.6`.

§2 title and a representative n = 1 note (lines 16–20):

> ## 2. Multipole eigenmode / impedance cross-check

> | grimm_lf_preferred | 1 | 0.781 | impedance_Q=0.7814; spectral_FWHM_Q=0.8114; f_peak=11.651… |

Every n = 1 row in lines 20–40 ends with `f_peak=11.651…`. n = 2 rows print `f_peak=20.181…`; n = 3 rows print `f_peak=28.540…`. Those strings are quoted as printed and are not identified with `0.3*f_n`; only the fundamental identity 11.6513774062 Hz = `0.3*f_ideal` is in the audit.

Regional Q and paths (lines 46–67):

> | grimm_lf_preferred | 0.781 | … | … | 55.3 |
> | nearside_warm | 0.776 | … | … | 107.4 |
> | farside_cold | 0.828 | … | … | 35.7 |
> | pkt | 0.936 | … | … | 267.6 |

> | nearside_farside | 0.801 | 0.776 | 0.828 |
> | pkt_farside | 0.879 | 0.936 | 0.828 |
> | global_global | 0.781 | 0.781 | 0.781 |

> - **global_90_10Hz**: 55.3 dB
> - **nearside_90_10Hz**: 107.4 dB
> - **farside_90_10Hz**: 35.7 dB
> - **mixed_NS_90_10Hz**: 71.5 dB
> - **through_PKT_90_10Hz**: 136.9 dB

Conclusion (line 71):

> Literature-anchored 1-D profiles, multipole cross-checks, and regional nearside/farside/PKT experiments all continue to show **no high-Q global cavity**: open Moon has no ionospheric wall; even with an artificial wall, Q remains O(1); lateral contrasts change path attenuation but do not create a high-Q resonator.

---

## `README.md`

Review status, left in place (lines 26–33):

> An adversarial model audit found that the reported eigenmode cross-check reuses the wall-impedance proxy, the cavity-Q formula fails a weak-loss energy-balance benchmark, and several claimed bounds need narrower scope. The historical results below remain available for reproduction; they are **not validated antenna efficiencies or rigorous global power-transfer bounds**.

Headline table (lines 58–64):

> | Loss tangent at 1–30 Hz | $\tan\delta \gg 1$ (conduction-dominated) |
> | Physical Moon (no ionosphere) | **No closed Schumann-type cavity** |
> | Hypothetical 100 km ionosphere | Cavity $Q \lesssim 2$ for literature profiles |
> | Monte Carlo (20 000 draws) | median $Q \approx 0.78$, max $Q \approx 2.0$, **100% have $Q < 5$** |
> | Nearside / farside / PKT paths | Path attenuation changes; no high-$Q$ resonator |

> The outer shell is a **weakly conducting medium with large skin depth**, not a classical low-loss dielectric waveguide or high-$Q$ planetary resonator.

Historical context sentences used (lines 78–88):

> There is no stable global ionosphere to act as an upper wall, and the outer shell itself is conduction-dominated at ELF ($\tan\delta \gg 1$).

> 2. **Model B (exploratory artificial lid)** — hypothetical conducting boundary at 100 km imposed as an upper-bound experiment → cavity $Q$ remains of order unity (median Monte Carlo $Q \approx 0.78$, maximum $\approx 2$).

> **Outcome of the reverse-engineering:** the lunar outer shell does not support the high-$Q$ global ELF modes required by the historical Tesla planetary-resonator architecture. The same calculations show it is a weakly conducting, large-skin-depth medium whose primary scientific value is geophysical (magnetotelluric / induction sounding), not as a planetary waveguide or wireless-power cavity.

> The code, profiles, and figures document both the original exploratory motivation and the quantitative constraints that closed that path.

Key-figure captions used (lines 112, 126, 130):

> *Loss tangent $\tan\delta = \sigma/(\omega\varepsilon)$. Across the nominal and Apollo-style envelopes at 1–30 Hz, $\tan\delta \gg 1$: conduction current dominates.*

> *Model B (artificial 100 km ionosphere) cavity $Q$ for named profiles. Physical Moon (Model A) has no closed cavity ($Q \equiv 0$).*

> *20 000 literature-bracketed Monte Carlo draws. Median $Q \approx 0.78$; maximum $Q \approx 2.0$; 100% of draws have $Q < 5$.*

The loss-tangent caption is already scoped to nominal and Apollo-style envelopes and is left. The other two are replaced.

Model B section (lines 152–174):

> The physical Moon has no stable global ionosphere, so there is no closed Earth-like Schumann cavity (Model A → $Q \equiv 0$).
> As an exploratory upper-bound exercise we nevertheless imposed a **hypothetical conducting lid at 100 km** (Model B) and recomputed cavity quality factors with the impedance formula

> $$
> Q \approx \frac{\omega\mu_0 h}{2\,\mathrm{Re}(Z_g+Z_i)}\,.
> $$

> This is the most favorable simple artificial boundary that still respects the measured radial conductivity structure of the outer shell.

Named table (lines 163–166): optimistic_cold `0.35` / `~3 ms`; nominal `0.58` / `~5 ms`; apollo_classic `0.44` / `~4 ms`; pessimistic_warm `2.01` / `~16 ms`.

> - median $Q \approx 0.78$
> - maximum $Q \approx 2.0$
> - **100 % of draws have $Q < 5$**

> Conclusion of the exploratory case: adding an artificial upper wall does not produce a high-$Q$ global resonator. Distributed loss from the continuous conductivity gradient keeps $Q$ of order unity. The physical open-Moon case remains cavity-free.

Physics Summary item 2 (line 196), noted but not rewritten:

> - **Model B**: artificial ionosphere (exploratory upper bound) with the $Q$ formula above.

Review-status 50 W sentence (lines 40–41), not rewritten and not sourced from the energy review, because that file was not read:

> The most promising development target is a 50 W night-survival service with scheduled optical charging; its orbit availability remains to be established.

---

## Not read

- `paper/ENERGY_DELIVERY_REVIEW_2026-09-05.md` (ELF loop watts). Listed by the GitHub contents API (13594 bytes) and not downloaded.
- `results/campaign/iono_sensitivity.csv`. The Q = 7.480575 and 11.626608 figures are quoted from the audit’s report of that file, not from the CSV itself.
- Source code (`impedance.py`, `eigenmodes.py`, `03_driven_transfer.py`). Findings are taken from the audit’s description of those lines.
