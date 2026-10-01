# Corrections to the cavity-Q and path claims

Corrected wording for overstated claims in the manuscript (`paper/paper.html`), the quantitative appendices, the optional report, and the README headline, Model B, and historical-outcome sections of `luckyseoul/lunar-elf`. The manuscript and the README are not rewritten here.

Figures are taken from the repository at commit `8aa7940863de40c6eb71b1cf34ba37a1127ef260` and from `paper/MODEL_AUDIT_2026-09-05.md`. The lunar Q tables are not doubled. A weak-loss energy balance is twice the repository formula only inside the perturbative check; Q of order 1 is outside that regime, and the lossy wall also shifts frequency and stored energy.

Replacement count: **32**.

---

## 1. Manuscript — `paper/paper.html`

### 1. Abstract (quantitative sentences)

**Wrong:** loss tangents "\(\tan\delta=\sigma/(\omega\varepsilon)\gg 1\)" for literature-bracketed outer-shell conductivities at 1–30 Hz; impedance-method "\(Q\lesssim 2\)" and the 20,000-draw results (median \(Q\simeq 0.78\), 95th percentile \(Q\simeq 1.85\), maximum \(Q\simeq 2.0\), 100% with \(Q<5\)) stated as cavity quality factors; nearside–farside and PKT contrasts "do not create a high-\(Q\) resonator." Findings: loss-tangent headline; M2; M7; historical-scope note in the audit conclusion. The Monte Carlo digits are the manuscript's own rounding of `paper/CAMPAIGN_REPORT.md`.

**Replacement:**

> At 1–30 Hz, nominal and Apollo-style outer-shell envelopes are conduction-dominated, but \(\tan\delta\gg 1\) does not hold for every supplied profile and frequency. The optimistic profile's shell statistic is 1.9143 at 30 Hz: only moderately conduction-dominated. That does not imply low-loss transmission through the whole Moon. Without a conducting ionosphere there is no closed Earth-like Schumann cavity. Figures previously reported as cavity quality factors — including \(Q\lesssim 2\) on the named n = 1 profiles and a 20,000-draw Monte Carlo with median \(Q\simeq 0.78\), 95th percentile \(Q\simeq 1.85\), maximum \(Q\simeq 2.0\), and 100% of draws below 5 — are historical outputs of the wall proxy \(Q\approx\omega\mu_0 h/[2\,\mathrm{Re}(Z_g+Z_i)]\) at \(h=100\) km and \(\sigma_\mathrm{iono}=1\times 10^{-5}\) S/m. They are not a validated cavity \(Q\), not an antenna efficiency, and not a global upper bound. The same checked-in sweep already reaches \(Q=7.480575\) (n = 1) and \(Q=11.626608\) (n = 3) for pessimistic_warm at \(h=200\) km and \(\sigma_\mathrm{iono}=1\times 10^{-3}\) S/m. Nearside–farside and PKT contrasts change bulk path attenuation; they were not shown to create or to rule out a high-\(Q\) resonator.

### 2. §1, end of the first paragraph

**Wrong:** "explicit modal quality-factor estimates" are offered as the test of the low-loss-dielectric description. Finding: M2 (the modal \(Q\) is the defective wall proxy). The conductivity comparison itself is not withdrawn.

**Replacement:**

> That terminology is tested here against published conductivity structure, skin depth, and loss tangent. The modal numbers in §4 are historical outputs of a wall-impedance proxy, not an independent cavity-\(Q\) measurement.

### 3. Figure 2 caption

**Wrong:** "Values \(\gg 1\) indicate conduction-dominated (weakly conducting) behavior across 1–100 Hz." Finding: loss-tangent headline. The audit's optimistic shell statistic is 1.9143 at 30 Hz (`paper/MODEL_AUDIT_2026-09-05.md`). `paper/QUANTITATIVE_RESULTS.md` prints the same case as \(1.91\times 10^{0}\).

**Replacement:**

> **Figure 2.** Loss tangent \(\tan\delta=\sigma/(\omega\varepsilon)\) for the outer-shell (0–300 km) sample-count log-mean conductivity. Nominal and Apollo-style envelopes at 1–30 Hz are conduction-dominated. The optimistic profile is not: its shell statistic is 1.9143 at 30 Hz. Values \(\gg 1\) are not claimed for every profile or for the whole 1–100 Hz axis.

### 4. §3 paragraph above Table 1, and Table 1 caption

**Wrong:** half-circumference attenuations "show that shell-guided global standing waves are not viable," and \(\sigma_\mathrm{eff}\) is presented as though the unweighted log mean were a unique shell conductivity. Findings: M0 (bulk path diagnostic, not a link budget; a through-rock path does not rule out other coupling); M4 (sample-count log mean is tabulation-dependent). Table 1 rounds `paper/OPTIONAL_REPORT.md` (for example Grimm LF \(1.38\times 10^{-7}\) S/m to \(1.4\times 10^{-7}\)). No depth-weighted conductivity for those four literature profiles is given in the files cited here. The factor 2.65–4.76 applies only to the four named synthetic profiles in the audit.

**Replacement:**

> Table 1 lists outer-shell metrics at 10 Hz. \(\sigma_\mathrm{eff}\) is the unweighted log mean of tabulated samples in the outer 300 km, not a depth-weighted conductivity, and it changes if the same profile is re-tabulated. \(A_{1/2\mathrm{circ}}\) is a good-conductor skin-effect integral along a prescribed half-circumference. It is a material-path diagnostic for that path. It is not a link budget, and it does not decide forced-current, near-field, or surface-to-orbit coupling. On this diagnostic, nominal and midmantle-resolved profiles span many skin depths; that statement is limited to shell-guided circumferential attenuation.

Table 1 caption, replace the present caption with:

> **Table 1.** Outer-shell (0–300 km sample-count log-mean) metrics at 10 Hz for literature-anchored profiles. Attenuations are path diagnostics, not a delivered-power budget. No shell-path \(Q\) is reported: the old \(\beta/(2\alpha)\) ratio is not an upper bound.

### 5. Figure 4 caption

**Wrong:** the figure is "illustrating strong global-shell damping" in language a reader can take as a power-transfer result. Finding: M0.

**Replacement:**

> **Figure 4.** Good-conductor skin-effect attenuation along a prescribed half lunar circumference for the synthetic profile suite. This is a bulk path diagnostic, not a link budget and not a transmitter-to-load efficiency.

### 6. Equation (3) and the Model C paragraph in §4

**Wrong:** equation (3), \(Q\approx\omega\mu_0 h/[2\,\mathrm{Re}(Z_g+Z_i)]\), is the cavity quality factor, and Model C "recovers \(Q\sim 4\)–6" in "order-of-magnitude agreement with terrestrial Schumann \(Q\)." Findings: M2; M0 if \(Q\) is read as power-transfer performance. Printed Model C values in `paper/QUANTITATIVE_RESULTS.md` are 3.69, 4.85, and 5.77.

**Replacement:**

> Planetary surface impedance \(Z_g(\omega)\) is computed from a layered magnetotelluric-style recursion through \(\sigma(r)\); ionospheric impedance \(Z_i\) is a uniform half-space proxy. The repository then forms the wall proxy
>
> \(Q_\mathrm{repo}\approx\omega\mu_0 h/[2\,\mathrm{Re}(Z_g+Z_i)]\). (3)
>
> For peak phasors in a thin vacuum TEM cavity the weak-loss energy balance is \(Q=\omega\mu_0 h/(R_g+R_i)\), without the extra 2. At \(f=10\) Hz, \(h=100\) km, and \(R_g=R_i=0.01\,\Omega\), that balance is 394.784176 and the repository returns 197.392088. Galejs' one-lossy-wall reduction at the ideal PEC frequency is \(Q=\omega\mu_0 h/\mathrm{Re}(Z_s)\) (Galejs, 1965, as cited in the 2026-09-05 audit). The lunar tables are not replaced by twice these numbers. The proxy is perturbative, and a result of order 1 is outside that regime: the lossy boundary also shifts frequency and stored energy. The Earth stack (Model C) uses the same proxy — printed \(Q=3.69\), 4.85, and 5.77 for \(n=1,2,3\) — and does not independently validate it.

The ideal-frequency sentence \(f_1\approx 38.8\) Hz and the statement that the physical Moon has no dense conducting ionosphere are unchanged. Those statements are not the defect.

### 7. Table 2 caption

**Wrong:** "Primary metric: impedance method (Eq. 3)" presented as Model B cavity \(Q\). Findings: M2; M1 if read as an eigenmode; M7 for scope. Table body digits remain historical proxy outputs. Within the synthetic suite, "\(Q\lesssim 2\)" is already false for pessimistic_warm at \(n=2\) and \(n=3\): `paper/QUANTITATIVE_RESULTS.md` prints 2.63 and 3.12 (the campaign file prints 3.11 for \(n=3\)).

**Replacement caption:**

> **Table 2.** Historical outputs of the repository wall proxy (Eq. 3) for an artificial lid at \(h=100\) km, evaluated at the ideal PEC multipole frequencies. Not a validated cavity \(Q\), not an eigenfrequency, and not a bound over other lid heights or conductivities.

### 8. Ringing-time sentence in §4

**Wrong:** \(\tau\approx Q/(\pi f_1)\) of a few milliseconds is evidence against a sustained global ring, using the proxy \(Q\) as if it were cavity \(Q\). Finding: M2. The arithmetic definition can stay; the physical claim cannot.

**Replacement:**

> Ringing times formed as \(\tau\approx Q_\mathrm{repo}/(\pi f_1)\) are a few milliseconds when the proxy is of order 1 at \(f_1\sim 39\) Hz. They inherit the wall proxy and are not a measured ring-down of a lunar eigenmode.

### 9. Figure 5 caption

**Wrong:** "All values remain \(\mathcal{O}(1)\), far below high-\(Q\) resonator behavior," offered without the lid scope and as cavity \(Q\). Findings: M2; M7.

**Replacement:**

> **Figure 5.** Fundamental-mode wall proxy for literature and regional profiles at \(h=100\) km. These historical outputs are \(\mathcal{O}(1)\) for this lid only. They are not a validated cavity \(Q\) and not a maximum over artificial upper boundaries.

### 10. §4.1 Monte Carlo, including "No high-\(Q\) island appears in the envelope."

**Wrong:** the draw statistics are reported as Model B cavity \(Q\) and as the absence of a high-\(Q\) island. Findings: M2; M7; historical-scope note. Manuscript digits, not the campaign file's extra precision: median 0.78, percentiles 0.30 and 1.85, maximum 2.01, 100% below 5, 65% below 1. Campaign file prints median 0.778, p05 0.295, and 64.7% below 1. The two roundings are not combined in one sentence.

**Replacement:**

> To avoid reliance on a single \(\sigma(r)\), we draw 20,000 synthetic profiles spanning optimistic to pessimistic literature bounds and evaluate the wall proxy for \(n=1\) at \(h=100\) km and \(\sigma_\mathrm{iono}=1\times 10^{-5}\) S/m. Under that formula and those boundaries the manuscript distribution is: median \(Q=0.78\); 5th / 95th percentiles \(0.30\) / \(1.85\); maximum \(Q=2.01\); 100% of draws have proxy \(Q<5\); 65% have proxy \(Q<1\). This is not a validated cavity \(Q\) and not a maximum over artificial lids. The checked-in sensitivity file already contains pessimistic_warm, \(h=200\) km, \(\sigma_\mathrm{iono}=1\times 10^{-3}\) S/m, with \(Q=7.480575\) (\(n=1\)) and \(Q=11.626608\) (\(n=3\)). No high-\(Q\) island is claimed, and none is ruled out, beyond this proxy and this lid.

### 11. Figure 6 caption

**Wrong:** "the entire support lies well below terrestrial Schumann \(Q\)." Finding: M2 (same formula cannot be compared to terrestrial Schumann \(Q\) as a validation). M7 for the implied global maximum.

**Replacement:**

> **Figure 6.** Distribution of the Model B fundamental wall proxy (20,000 draws) at \(h=100\) km and \(\sigma_\mathrm{iono}=1\times 10^{-5}\) S/m. Median and 95th percentile refer to that proxy only. The histogram is not a measurement of lunar cavity \(Q\) and is not a comparison that validates the formula against terrestrial Schumann \(Q\).

### 12. Figure 7 caption

**Wrong:** "values remain \(\lesssim 2\) across the envelope." Findings: M2; M7. Also, inside the named Model B table, pessimistic_warm already prints 2.63 and 3.12 at \(n=2\) and \(n=3\).

**Replacement:**

> **Figure 7.** Monte Carlo wall proxy versus outer-shell sample-count effective conductivity, for the \(h=100\) km, \(\sigma_\mathrm{iono}=1\times 10^{-5}\) S/m campaign. More conductive walls lower \(\mathrm{Re}(Z_g)\) inside this proxy. The cloud is not an upper bound of 2 on cavity \(Q\).

### 13. §5 Lateral heterogeneity (the \(Q\) and "transmission" sentences)

**Wrong:** two-hemisphere "effective cavity \(Q\sim 0.8\)–0.9" and "does not produce a high-\(Q\) global mode"; "modulates transmission." Findings: M2; M7; M0. The decibel figures are the paper's approximations of `paper/OPTIONAL_REPORT.md`: farside 35.7 dB, PKT column 267.6 dB over 90°, mixed path through PKT 136.9 dB. Those path integrals are not the angular-spreading curve in Figure 9. Keep them as path diagnostics.

**Replacement:**

> One-dimensional inversions miss nearside–farside structure and the Procellarum KREEP Terrane. Regional columns change local surface impedance and the shell-path attenuation diagnostic. Two equal-area hemisphere combinations of the same wall proxy give about 0.8–0.9 (`paper/OPTIONAL_REPORT.md` prints 0.801, 0.879, and 0.781). That is not a validated cavity \(Q\). Piecewise great-circle skin-effect integrals at 10 Hz are about 36 dB (farside; table value 35.7 dB) to about 268 dB (PKT; table value 267.6 dB) over 90°, and about 137 dB (table value 136.9 dB) on a mixed path through PKT. Lateral contrast changes that path diagnostic. It does not establish a delivered-power link, and it does not by itself create or forbid a high-\(Q\) global mode.

### 14. Figure 9 caption

**Wrong:** "Source–receiver transfer proxy versus angular separation" with "path attenuation plus geometric spreading," as if the curve were a transfer function. Finding: angular-transfer sign reversal in the audit (associated with M0). Isolated spreading contribution from 10° to 90° is +7.6033 dB; cylindrical spreading as stated would be −7.6033 dB.

**Replacement:**

> **Figure 9.** Angular curve formed from bulk plane-wave attenuation along a prescribed arc plus a geometric-spreading term. The spreading sign is reversed: its isolated contribution from 10° to 90° is +7.6033 dB, where the stated cylindrical spreading is −7.6033 dB. Antipodal behavior on this curve is an imposed geometric proxy, not a wave solution, and the curve is not a link budget. The companion response \(1/|Z_g+Z_i|\) is likewise not delivered power.

### 15. §6, Model B bullet and the three-dimensional "bound" bullet

**Wrong:** "Model B ionospheres are artificial proxies for bounding \(Q\)." And "the regional path and two-hemisphere estimates bound the effect of first-order asymmetry." Findings: M7; M2; M0. The other limitation bullets (resolution, Mittelholz construction, Model A not a leaky-mode catalog) stay.

**Replacement, Model B bullet:**

> Model B ionospheres are artificial lids used to evaluate a wall-impedance proxy at stated \(h\) and \(\sigma_\mathrm{iono}\). They do not upper-bound cavity \(Q\). The \(h=100\) km, \(\sigma_\mathrm{iono}=1\times 10^{-5}\) S/m campaign is one case; the checked-in sweep includes \(Q=7.480575\) and \(Q=11.626608\). An engineered global ionosphere would still need its own construction, maintenance, and net-energy budget. These proxy values are not a power-transfer result.

**Replacement, asymmetry bullet:**

> Full three-dimensional Maxwell solutions with continuous lateral structure remain future work. The regional path integrals and two-hemisphere proxy combinations are first-order diagnostics, not a bound on asymmetry.

### 16. §7 Conclusion, and the acknowledgments sentence that calls the package a cavity-\(Q\) calculation

**Wrong:** \(\tan\delta\gg 1\) at 1–30 Hz; "cavity quality factors remain \(Q\lesssim 2\) across the explored envelope"; lateral structure "does not enable high-\(Q\) global resonances." Findings: loss-tangent headline; M2; M7; M0. Acknowledgments: "layered surface-impedance cavity \(Q\)" over-names the proxy.

**Replacement, conclusion:**

> Continuous electrical-conductivity profiles from Apollo and orbital magnetic sounding, literature-bracketed envelopes, and a 20,000-draw Monte Carlo show that the outer several hundred kilometers of the Moon are a weakly conducting, large-skin-depth medium at ELF rather than a low-loss dielectric — with the quantitative limit that the optimistic shell statistic is 1.9143 at 30 Hz, so \(\tan\delta\gg 1\) is not true for every profile and frequency. Absence of a conducting ionosphere precludes a closed Schumann-type cavity. Historical wall-proxy outputs at \(h=100\) km and \(\sigma_\mathrm{iono}=1\times 10^{-5}\) S/m are of order 1 for the n = 1 campaign (manuscript maximum \(Q\simeq 2.0\), 100% of those draws below 5) and are not a validated cavity \(Q\) or a global upper bound. Lateral nearside–farside and PKT structure changes path attenuation and does not, on these diagnostics, demonstrate a high-\(Q\) global resonance. The same observation-based template is a geophysical starting point for other airless bodies, not a wireless-power closure.

**Replacement, acknowledgments sentence:**

> Quantitative results were produced with the open `lunar-elf` package (layered surface impedance, a wall-loss proxy rather than a validated cavity \(Q\), path integrals, Monte Carlo, and regional path experiments).

---

## 2. `paper/QUANTITATIVE_RESULTS.md`

### 17. Method summary, items 1 and 2

**Wrong:** "outer-shell (0–300 km) log-mean \(\sigma_\mathrm{eff}\)" as the shell conductivity; "shell-path Q upper bound \(Q\lesssim\beta/(2\alpha)\)" with dielectric \(\beta\) and good-conductor \(\alpha\); Model A "no ionosphere \(\Rightarrow\) no cavity"; Model B "\(Q\approx\omega\mu_0 h/[2\,\mathrm{Re}(Z_g+Z_i)]\)" as the cavity formula. Findings: M4; M3; M0; M2.

**Replacement:**

> 1. **Phase 0** — outer-shell (0–300 km) sample-count log-mean \(\sigma_\mathrm{eff}\) (not depth-weighted); skin depth \(\delta=\sqrt{2/\omega\mu\sigma}\); loss tangent \(\tan\delta=\sigma/(\omega\varepsilon)\); circumferential path attenuation as a good-conductor skin-effect integral. The old ratio \(\beta/(2\alpha)\) with \(\beta=\omega\sqrt{\mu\varepsilon}\) and \(\alpha=\sqrt{\omega\mu\sigma/2}\) is not an upper bound and is not reported as \(Q\).
> 2. **Phase 1** — planar layered surface-impedance recursion looking into \(\sigma(r)\). Model **A**: open Moon; the code label \(Q=0\) means the assumed upper wall is absent, not a radiative \(Q\). Model **B**: artificial ionosphere; historical proxy \(Q_\mathrm{repo}\approx\omega\mu_0 h/[2\,\mathrm{Re}(Z_g+Z_i)]\), which is not the weak-loss energy balance and not a validated eigenmode \(Q\). Model **C**: Earth stack run through the same proxy (smoke output only).

Item 3 (literature-bracketed synthetics) stays.

### 18. Phase 0 table (header "Q_path ≲") and the terminology note's reach

**Wrong:** column "Q_path ≲" is an upper bound. \(\sigma_\mathrm{eff}\) column is the unweighted mean. The terminology note's "\(\tan\delta\gg 1\)" is limited to nominal and Apollo-style envelopes and must not be read as the whole suite; optimistic_cold at 30 Hz is printed \(1.91\times 10^{0}\). Findings: M3; M4; loss-tangent headline.

**Replacement note, placed under the Phase 0 table in place of any upper-bound reading of the last column:**

> Rename the last column from "Q_path ≲" to "inconsistent \(\beta/(2\alpha)\)" or drop it. It is not an upper bound. At 10 Hz the audit evaluates that claimed upper value as 0.1079738 (nominal; this table prints 0.108) against the repository's own material wavenumber \(\mathrm{Re}(k)/[-2\,\mathrm{Im}(k)]=0.5117942\), and 0.0112573 (warm) against 0.5001267. The Model A block prints the warm 10 Hz entry as 0.0113; this Phase 0 block prints 0.0127. Those two printed cells are not forced to one rounded value. A larger assumed phase speed makes \(\beta/(2\alpha)\) smaller, so the inequality does not run the way an upper bound would. The ratio is not a temporal eigenmode \(Q\) and not an antenna efficiency.
>
> \(\sigma_\mathrm{eff}\) is a sample-count log mean. A log-linear test profile returns \(1.000\times 10^{-6}\) S/m on three uniform depths and \(2.0893\times 10^{-7}\) S/m on five surface-dense depths; the depth-weighted geometric mean is \(1.000\times 10^{-6}\) S/m either way. For the four named profiles the depth-weighted log mean is 2.65–4.76 times the sample-count mean. Nominal \(1.3123\times 10^{-7}\) S/m (printed \(1.31\times 10^{-7}\)) becomes \(6.2510\times 10^{-7}\) S/m. The skin-attenuation proxy scales with the square root of that conductivity ratio. Neither average is an antenna channel.
>
> The terminology note may keep "\(\tan\delta\gg 1\)" only for the nominal and Apollo-style envelopes at 1–30 Hz. It must not cover optimistic_cold, whose 30 Hz entry is \(1.91\times 10^{0}\) (audit shell statistic 1.9143).

### 19. Model A preamble ("cavity Q ≡ 0" and "Shell-path upper bounds")

**Wrong:** "cavity Q ≡ 0 in the impedance formula" read as a computed quality factor, and "Shell-path upper bounds for any would-be circumferential standing wave." Findings: M0; M3.

**Replacement:**

> No conducting ionosphere means no Earth-like closed Schumann cavity. In the impedance code, \(Q=0\) is a label for the missing upper wall, not a radiative quality factor and not induced power at another site. The former "Q_path ≲" column is the inconsistent \(\beta/(2\alpha)\) ratio, not an upper bound on a circumferential standing wave. Half-circumference and round-trip attenuations remain good-conductor path diagnostics only.

### 20. Model B preamble ("Primary metric: impedance-method cavity Q")

**Wrong:** impedance-method cavity \(Q\) as the primary physical metric, and the table's "Q_path ≲" column. Findings: M2; M3; M7. Named n = 1 proxy values printed here are optimistic_cold 0.348, nominal 0.577, apollo_classic 0.444, pessimistic_warm 2.01, at f = 38.84 Hz. Those may be quoted only as historical proxy outputs at this lid.

**Replacement:**

> Model B is a hypothetical lid, not the most favorable simple artificial boundary and not an upper bound. The table's \(Q_\mathrm{cavity}\) column is the repository wall proxy at the height and ionospheric conductivity used for this run (the \(Q\sim 2\) campaign maximum belongs to \(h=100\) km and \(\sigma_\mathrm{iono}=1\times 10^{-5}\) S/m, not to every lid). pessimistic_warm in this table is already 2.01, 2.63, and 3.12 for \(n=1,2,3\). The column is not summarized as \(Q\lesssim 2\) and is not multiplied by two. "Q_path ≲" is dropped or relabeled as the inconsistent \(\beta/(2\alpha)\) ratio (printed here down to 0.0222 on pessimistic_warm, \(n=1\)).

### 21. Model C closing sentence

**Wrong:** "Expected cavity Q of order few–tens for a reasonable ground+ionosphere stack — use as smoke test, not a precision Earth model," which still treats the output as expected cavity \(Q\). Finding: M2. Printed values: n = 1, 2, 3 give \(Q=3.69\), 4.85, 5.77 at ideal \(f=10.59\), 18.34, 25.94 Hz.

**Replacement:**

> Earth ideal \(f_1\approx 10.6\) Hz is the PEC formula; observed Earth Schumann resonance is ~7.8 Hz with ionosphere corrections. The printed stack (\(Q=3.69\), 4.85, 5.77) is the same wall proxy as Model B, a smoke output only. It does not independently validate the formula, and it is not a precision Earth model.

### 22. Ringing times (Model B, n = 1)

**Wrong:** "Short \(\tau\) \(\Rightarrow\) no sustained global ring," from proxy \(Q\). Finding: M2. Printed pairs: optimistic_cold 0.348 and 0.003 s; nominal 0.577 and 0.005 s; apollo_classic 0.444 and 0.004 s; pessimistic_warm 2.01 and 0.016 s; \(f_1=38.84\) Hz.

**Replacement:**

> \(\tau_\mathrm{ring}\approx Q_\mathrm{repo}/(\pi f)\) using the wall proxy at the ideal PEC frequency. The printed times (0.003 s, 0.005 s, 0.004 s, 0.016 s) are not a measured ring-down and do not by themselves show that a driven source cannot supply a load.

### 23. Paper-ready claims 1, 3, and 4

**Wrong:** claim 1, "\(\tan\delta\gg 1\)" for literature-bracketed conductivities at 1–30 Hz; claim 3, cavity \(Q\) "remains modest"; claim 4, shell-guided global standing waves "are not supported" as a general closure. Findings: loss-tangent headline; M2; M7; M0. Claim 2 (no closed global cavity without an ionosphere) and claim 5 (1-D radial scope) stay, with claim 2 read as geometry, not as \(Q=0\) radiation.

**Replacement:**

> 1. At 1–30 Hz, nominal and Apollo-style outer-shell envelopes have \(\tan\delta\gg 1\). The optimistic shell statistic is 1.9143 at 30 Hz (this file prints \(1.91\times 10^{0}\)). The outer shell is not a low-loss dielectric. Moderately large \(\tan\delta\) on the optimistic end-member still does not imply low-loss transmission through the whole Moon.
> 3. With a hypothetical 100 km ionosphere, the historical wall proxy depends on \(\mathrm{Re}(Z_g)+\mathrm{Re}(Z_i)\). Call the resulting numbers proxy outputs for the stated lid, not cavity \(Q\) and not an upper bound. The checked-in sweep exceeds the \(Q\sim 2\) campaign maximum.
> 4. Circumferential shell paths for nominal \(\sigma\) span many skin depths (half-circumference attenuations of tens to hundreds of dB on this diagnostic). That is a statement about the prescribed shell path, not a link budget and not a ban on other ELF coupling geometries.

---

## 3. `paper/CAMPAIGN_REPORT.md`

### 24. Section title and interpretation under the Monte Carlo list

**Wrong:** "Monte Carlo cavity Q" and "high-Q global modes (\(Q\gtrsim 10\)) are essentially absent under Model B; the physical open Moon (Model A) has no cavity at all." Findings: M2; M7; M0. The draw statistics themselves stay as campaign outputs: N = 20000, median 0.778, mean 0.923, p05/p95 = 0.295/1.85, max 2.01, 64.7% below 1, 100% below 5 and below 10.

**Replacement:**

> ## Monte Carlo wall proxy (Model B formula, n = 1, h = 100 km, \(\sigma_\mathrm{iono}=1\times 10^{-5}\) S/m)
>
> Interpretation: across this literature-bracketed envelope, the defective wall proxy does not produce values \(\gtrsim 10\). Median 0.778, maximum 2.01, and 100% of draws below 5 are historical outputs of that formula at this lid. They are not a validated cavity \(Q\), not an antenna efficiency, and not a global upper bound. Model A does not compute a cavity: \(Q=0\) labels a missing upper wall. The physical Moon still has no stable global ionosphere, so there is no closed Earth-like Schumann cavity.

### 25. "Named profiles (Model B)" framing

**Wrong:** the table is presented as cavity \(Q\) next to the campaign interpretation. Finding: M2; M7. Printed n = 1 values: apollo_classic 0.444, nominal 0.577, optimistic_cold 0.348, pessimistic_warm 2.01. pessimistic_warm n = 3 is 3.11 in this file (3.12 in `paper/QUANTITATIVE_RESULTS.md`). Both prints are retained and are not reconciled.

**Replacement lead-in:**

> Named-profile outputs of the same wall proxy at the campaign lid (\(h=100\) km). Not eigenmode \(Q\). The n = 1 column is the set later quoted as 0.35 / 0.58 / 0.44 / 2.01. pessimistic_warm at n = 3 is 3.11 in this file, so a summary line \(Q\lesssim 2\) does not fit the table.

---

## 4. `paper/OPTIONAL_REPORT.md`

### 26. §2 "Multipole eigenmode / impedance cross-check"

**Wrong:** the table is an eigenmode cross-check. `spectral_FWHM_Q` is a half-power quality factor. `f_peak=11.651…` on every n = 1 row is a resonance frequency. Findings: M1; M5; the dormant helper (M6) is not used to repair it. Every n = 1 note in the table prints `f_peak=11.651…`. The audit's fundamental is 11.6513774062 Hz = \(0.3 f_\mathrm{ideal}\). The n = 2 and n = 3 peak strings (20.181…, 28.540…) are the same helper's reported peaks; the audit text certifies the fundamental endpoint, not a separate identity for those two strings, so they are not relabeled as \(0.3 f_n\).

**Replacement:**

> ## 2. Wall-admittance scan (not an eigenmode cross-check)
>
> `find_mode_real_axis_q` does not call the Riccati integrator or the cavity characteristic. It returns the wall-impedance formula as \(Q\). The field named residual is the height of the response, not a characteristic residual near zero. For every named profile the reported fundamental is the scan endpoint 11.6513774062 Hz = \(0.3 f_\mathrm{ideal}\). The n = 1 rows below print that endpoint (`f_peak=11.651…`). A monotonic wall response with an endpoint maximum has no bracketed resonance whose width is a pole. `spectral_FWHM_Q` is a half-amplitude width: a synthetic amplitude Lorentzian with half-power \(Q=100\) returns 57.735026 = \(1/\sqrt{3}\). These lunar rows are not rescaled by \(\sqrt{3}\). There is no bracketed peak to rescale.
>
> `cavity_characteristic` is not used in place of this table. It computes \(Z_g\) and \(Z_i\) and uses neither. Changing ionospheric conductivity from \(1\times 10^{-8}\) to \(1\times 10^{-2}\) S/m leaves the characteristic unchanged. Calling the complex-frequency function at \(10+0.1j\) Hz raises TypeError. Unused radial-transfer and energy helpers stay unused.

The numeric columns may remain only under that relabeling, as diagnostics, not as confirmed \(Q\).

### 27. §3 regional \(Q\) and two-hemisphere \(Q_\mathrm{eff}\)

**Wrong:** columns \(Q_{n1}\) and \(Q_\mathrm{eff}\) read as cavity quality factors (0.781, 0.776, 0.828, 0.936; pairs 0.801, 0.879, 0.781). Findings: M2; M7. Path attenuations at 10 Hz (55.3, 107.4, 35.7, 71.5, 136.9 dB, and the 90° column 267.6 dB for PKT) are not identified by the audit as the sign-reversed spreading term. Keep them as path diagnostics (M0: not a link budget).

**Replacement lead-in:**

> Regional and two-hemisphere \(Q\) entries are the same wall proxy as §2, not validated cavity \(Q\) and not a bound on lateral coupling. Path-attenuation samples at 10 Hz stay labeled as good-conductor integrals on the stated arcs (global 55.3 dB, nearside 107.4 dB, farside 35.7 dB, mixed 71.5 dB, through PKT 136.9 dB, PKT column at 90° 267.6 dB). They are not a source–receiver power budget. The angular-transfer spreading reversal (+7.6033 dB versus −7.6033 dB from 10° to 90°) is a separate curve and is not one of these samples.

### 28. Conclusion

**Wrong:** literature profiles, "multipole cross-checks," and regional experiments "show no high-\(Q\) global cavity" and "even with an artificial wall, \(Q\) remains \(O(1)\)." Findings: M1; M2; M7; loss-tangent headline is not this paragraph's main defect, but "no high-\(Q\)" is the same over-scope.

**Replacement:**

> Literature-anchored 1-D profiles document shell conductivity, skin depth, and path-attenuation diagnostics. The multipole table is a wall-admittance scan that returns its own impedance formula, including the scan endpoint 11.6513774062 Hz as the reported fundamental. It is not an independent eigenmode validation. Regional nearside / farside / PKT experiments change those path diagnostics and do not create a demonstrated high-\(Q\) resonator. They also do not upper-bound cavity \(Q\): open-Moon \(Q=0\) is a missing-wall label, and \(O(1)\) values are historical proxy outputs for the artificial wall that was actually run, not for every simple lid.

The §1 sentence "HF envelope retained as upper bound only" refers to Grimm's conductivity envelope, not to shell-path \(Q\). Leave it.

---

## 5. README.md — headline, historical outcome, Model B

The "Review status — 2026-09-05" section already says the historical results are not validated antenna efficiencies or rigorous global power-transfer bounds. That section is unchanged. The sections below it still contradict that status; corrected wording is given here. Physics Summary item 2 still says "exploratory upper bound" and is not rewritten in this note. The Model B sentence in item 31 is the wording that applies to that item.

### 29. Headline Results table and the sentence under it

**Wrong:** "Loss tangent at 1–30 Hz \(\tan\delta\gg 1\)" with no profile limit; "Cavity \(Q\lesssim 2\) for literature profiles"; Monte Carlo "median \(Q\approx 0.78\), max \(Q\approx 2.0\), 100% have \(Q<5\)" as headline cavity results; "no high-\(Q\) resonator" as a demonstrated negative. The physical-Moon row (no closed Schumann-type cavity) stays. Findings: loss-tangent headline; M2; M7; M0.

**Replacement table:**

| Claim | Result |
|-------|--------|
| Loss tangent at 1–30 Hz | Nominal and Apollo-style envelopes: conduction-dominated. Optimistic shell statistic 1.9143 at 30 Hz: not \(\tan\delta\gg 1\). |
| Physical Moon (no ionosphere) | **No closed Schumann-type cavity.** Code \(Q=0\) is a missing-wall label, not a radiative \(Q\). |
| Hypothetical 100 km ionosphere at \(\sigma_\mathrm{iono}=1\times 10^{-5}\) S/m | Historical wall-proxy outputs of order 1 on the n = 1 named set (README prints 0.35 / 0.58 / 0.44 / 2.01). Not a validated cavity \(Q\) and not \(Q\lesssim 2\) as a bound. |
| Monte Carlo (20,000 draws), same lid | Historical proxy: median \(Q\approx 0.78\), max \(Q\approx 2.0\), 100% of these draws \(Q<5\). Not a global maximum. Checked-in sweep: \(Q=7.480575\) (n = 1) and \(Q=11.626608\) (n = 3). |
| Nearside / farside / PKT paths | Path-attenuation diagnostic changes. Not a link budget and not a high-\(Q\) result either way. |

**Replacement sentence under the table:**

> The outer shell is a weakly conducting medium with large skin depth, not a classical low-loss dielectric waveguide. The repository does not yet calculate transmitted or received electrical power, and the wall proxy is not a planetary resonator \(Q\).

### 30. Historical Context — conductivity sentence, Model B list item, and the Outcome paragraph

**Wrong:** "the outer shell itself is conduction-dominated at ELF (\(\tan\delta\gg 1\))" with no exception; Model B "imposed as an upper-bound experiment → cavity \(Q\) remains of order unity (median Monte Carlo \(Q\approx 0.78\), maximum \(\approx 2\))"; the outcome sentence that the shell "does not support the high-\(Q\) global ELF modes required by the historical Tesla planetary-resonator architecture" and is not "a planetary waveguide or wireless-power cavity," stated as if the proxy had closed the power question. Findings: loss-tangent headline; M2; M7; M0. The Tesla ingredient list and the statement that the Moon has no stable global ionosphere stay.

**Replacement, conductivity sentence:**

> There is no stable global ionosphere to act as an upper wall. Nominal and Apollo-style envelopes are conduction-dominated at 1–30 Hz; the optimistic shell statistic is 1.9143 at 30 Hz, so \(\tan\delta\gg 1\) is not a blanket result. That limit does not imply low-loss transmission through the whole Moon.

**Replacement, list item 2:**

> 2. **Model B (exploratory artificial lid)** — hypothetical conducting boundary at 100 km with \(\sigma_\mathrm{iono}=1\times 10^{-5}\) S/m, not an upper-bound experiment. The wall proxy's historical outputs on that lid have median Monte Carlo \(Q\approx 0.78\) and maximum \(\approx 2\). The formula is low by a factor of two against a weak-loss balance (394.784176 versus 197.392088 in the perturbative check) and still must not be doubled for the lunar tables. The checked-in sweep is higher at other lids (\(Q=7.480575\) and \(11.626608\)).

**Replacement, outcome paragraph:**

> **Outcome of the reverse-engineering:** the calculations that were meant to recover a Tesla-style high-\(Q\) lunar cavity do not. What they actually return is a wall-impedance proxy under one artificial lid, plus bulk path attenuation, not a validated cavity \(Q\), not an antenna efficiency, and not a global upper bound on wireless power. The outer shell remains, on the conductivity diagnostics, a weakly conducting, large-skin-depth medium whose primary scientific value in this repository is geophysical (magnetotelluric / induction sounding). A continuously driven source is a different question from the decay of a free oscillation: the missing quantities are input power, matching, geometry, and received watts. Those are not settled here.

The sentence "The code, profiles, and figures document both the original exploratory motivation and the quantitative constraints that closed that path." overclaims closure. Corrected wording:

> The code, profiles, and figures document the exploratory motivation and the proxy outputs that failed to support a high-\(Q\) lunar cavity claim. They do not close every lunar wireless-power architecture.

### 31. Exploratory Case: Artificial Ionosphere (Model B), including the \(Q\equiv 0\) lead-in, the "most favorable" sentence, the formula, the named table, and the conclusion

**Wrong:** "Model A → \(Q\equiv 0\)" as a computed cavity result; "exploratory upper-bound exercise"; "most favorable simple artificial boundary"; the formula presented as cavity \(Q\); the conclusion that an artificial wall "does not produce a high-\(Q\) global resonator" and "keeps \(Q\) of order unity." Findings: M0; M7; M2. Named README digits 0.35, 0.58, 0.44, 2.01 and ringing times ~3, ~5, ~4, ~16 ms match `paper/QUANTITATIVE_RESULTS.md` (0.348 / 0.003 s, 0.577 / 0.005 s, 0.444 / 0.004 s, 2.01 / 0.016 s) at 38.84 Hz. Keep the digits only as proxy history. Monte Carlo lines: median \(\approx 0.78\), maximum \(\approx 2.0\), 100% below 5.

**Replacement:**

> The physical Moon has no stable global ionosphere, so there is no closed Earth-like Schumann cavity. Model A returns \(Q=0\) as a label that its formula has no upper wall. That label is not a radiative quality factor.
>
> As an exploratory case we imposed one hypothetical conducting lid at 100 km and \(\sigma_\mathrm{iono}=1\times 10^{-5}\) S/m and evaluated
>
> \(Q_\mathrm{repo}\approx\omega\mu_0 h/[2\,\mathrm{Re}(Z_g+Z_i)]\).
>
> This is not the most favorable simple artificial boundary in the repository. `results/campaign/iono_sensitivity.csv`, as audited, already has pessimistic_warm at \(h=200\) km and \(\sigma_\mathrm{iono}=1\times 10^{-3}\) S/m with \(Q=7.480575\) (\(n=1\)) and \(Q=11.626608\) (\(n=3\)). The weak-loss balance is \(Q=\omega\mu_0 h/(R_g+R_i)\). At \(f=10\) Hz, \(h=100\) km, and \(R_g=R_i=0.01\,\Omega\), that balance is 394.784176 and the repository returns 197.392088. The table below is not doubled.
>
> Historical n = 1 proxy outputs at ~38.8 Hz for this lid, with \(\tau\approx Q_\mathrm{repo}/(\pi f)\):
>
> | Profile | proxy (n = 1) | \(\tau\) from that proxy |
> |---------|-----------------|--------------------------|
> | optimistic_cold | 0.35 | ~3 ms |
> | nominal | 0.58 | ~5 ms |
> | apollo_classic | 0.44 | ~4 ms |
> | pessimistic_warm | 2.01 | ~16 ms |
>
> Monte Carlo, 20,000 literature-bracketed \(\sigma(r)\) draws, same lid and same formula: median \(Q\approx 0.78\), maximum \(Q\approx 2.0\), 100% of these draws \(Q<5\).
>
> Conclusion of the exploratory case: this lid and this proxy do not produce a validated high-\(Q\) global resonator. They also do not cap artificial-boundary proxy \(Q\) at 2, and they do not measure antenna efficiency or delivered watts. The physical open-Moon case remains without a closed Schumann cavity.

The existing pointer to `paper_figs/fig_iono_sensitivity.png` and `results/campaign/iono_sensitivity.csv` can stay, with the sentence above stating what the sweep actually contains.

### 32. Headline wording repeated in Key Figures captions

**Wrong:** the \(Q\) summary caption, "Physical Moon (Model A) has no closed cavity (\(Q\equiv 0\))" as a computed \(Q\); the Monte Carlo caption, "Median \(Q\approx 0.78\); maximum \(Q\approx 2.0\); 100% of draws have \(Q<5\)" as cavity \(Q\). Findings: M0; M2; M7. The loss-tangent caption that already limits \(\tan\delta\gg 1\) to "nominal and Apollo-style envelopes at 1–30 Hz" matches the audit's objection and stays.

**Replacement, \(Q\) summary caption:**

> *Model B wall proxy for named profiles at the 100 km, \(\sigma_\mathrm{iono}=1\times 10^{-5}\) S/m lid. Model A has no closed Schumann cavity; the code value \(Q\equiv 0\) is a missing-wall label, not a radiative \(Q\).*

**Replacement, Monte Carlo caption:**

> *20,000 literature-bracketed draws of the wall proxy at that same lid. Historical outputs: median \(Q\approx 0.78\); maximum \(Q\approx 2.0\); 100% of these draws have proxy \(Q<5\). Not a validated cavity \(Q\) and not a maximum over the ionosphere sweep.*

---

## Leave unchanged

The 2026-09-05 audit does not retract the following. They are unchanged.

- Conductivity profiles as inputs: the Grimm (2023) LF fit \(\sigma=1.76\times 10^{-4}\exp(z_\mathrm{km}/210)\) S/m over ~400–1200 km; the Dyal–Parkin resistive lid (\(\sigma\lesssim 10^{-8}\) S/m for depths \(\lesssim 80\) km); the log-linear bridge; named synthetic envelopes (optimistic / nominal / Apollo-style / pessimistic) and the literature constructions (Mittelholz-like as a constructed envelope, Hood-class resistive shell, regional nearside / farside / PKT variants). The Grimm HF envelope "retained as an upper bound only" because HF is argued to be biased high is a statement about that conductivity envelope, not about shell-path \(Q\).
- The skin-depth definition \(\delta=\sqrt{2/(\omega\mu\sigma)}\) (manuscript equation 1; README and quantitative method). The illustrative evaluation in the manuscript, \(\delta\approx 500\) km at \(f=10\) Hz and \(\sigma=10^{-7}\) S/m with \(\mu=\mu_0\), is the definition applied to a round conductivity, not the defective \(Q\) bound. Applying \(\delta\) to an unweighted log-mean \(\sigma_\mathrm{eff}\) inherits M4; the definition does not change.
- The ideal PEC Schumann frequency formula and the printed ideal \(f_1=38.84\) Hz (quantitative results) / \(f_1\approx 38.8\) Hz (manuscript), with \(R=1737.4\) km and \(c=2.997925\times 10^{8}\) m/s. The audit uses \(0.3 f_\mathrm{ideal}\) as a scan endpoint. It does not replace the PEC formula.
- The statement that the physical Moon has no stable global ionosphere and therefore no closed Earth-like Schumann cavity. What changes is only the identification of code \(Q=0\) with a radiative quality factor.
- Loss-tangent wording that is already limited to the nominal and Apollo-style envelopes at 1–30 Hz (quantitative terminology note; README loss-tangent figure caption). Those sentences are not extended to optimistic_cold or to "always."
- Manuscript limitations that the audit does not touch: limited vertical resolution in the uppermost 200–300 km; Mittelholz-like curve not digitized from a single figure; Model A is geometric and not a leaky-mode catalog.
- Paper-ready claims 2 and 5 in `paper/QUANTITATIVE_RESULTS.md`, read as "no closed cavity without an ionosphere" and "present scope is 1-D radial stratification."
- ELF loop power results in `paper/ENERGY_DELIVERY_REVIEW_2026-09-05.md`. They are not in the manuscript, the quantitative appendix, the campaign report, the optional report, or the README sections rewritten here. They are unchanged here. The README review-status mention of a 50 W night-survival target lies outside those sections and is unchanged.
- Campaign digits (median 0.778, mean 0.923, p05 0.295, p95 1.85, max 2.01, 64.7% below 1, 100% below 5) and the corresponding manuscript roundings, once they are labeled as historical proxy outputs of the stated lid. The defect is the claim, not a silent rewrite of the histogram.

## Outside these corrections

The night-charging schedule is the separate file `NIGHT_CHARGING_SCHEDULE.md` on the same branch. These replacements have not been applied to the manuscript or the README.
