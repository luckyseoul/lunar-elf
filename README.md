# lunar-elf

**Quantitative ELF electromagnetic modeling of the lunar outer shell**

Supporting the research note:

> **The Lunar Outer Shell as a Weakly Conducting, Large–Skin-Depth Medium at Extremely Low Frequencies**

Nicholas D. Perry · Council Bluffs, Iowa · nick@perrybrandsllc.com

[![License](https://img.shields.io/badge/license-Research-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

---

## Headline Results

| Claim | Result |
|-------|--------|
| Loss tangent at 1–30 Hz | $\tan\delta \gg 1$ (conduction-dominated) |
| Physical Moon (no ionosphere) | **No closed Schumann-type cavity** |
| Hypothetical 100 km ionosphere | Cavity $Q \lesssim 2$ for literature profiles |
| Monte Carlo (20 000 draws) | median $Q \approx 0.78$, max $Q \approx 2.0$, **100% have $Q < 5$** |
| Nearside / farside / PKT paths | Path attenuation changes; no high-$Q$ resonator |

The outer shell is a **weakly conducting medium with large skin depth**, not a classical low-loss dielectric waveguide or high-$Q$ planetary resonator.

---

## Historical Context: Tesla Planetary-Resonator Framing

This repository grew out of a systematic reverse-engineering of Nikola Tesla’s early planetary-resonator and wireless-power concepts (Earth–ionosphere cavity modes, global standing waves in the ELF band, and related grounded-dielectric waveguide ideas) and their proposed extension to the Moon.

Tesla’s historical claims assumed:

- a conducting lower boundary (Earth’s surface or an equivalent),
- an insulating volume that could support low-loss propagation,
- and an upper conducting boundary (the ionosphere) that closed a global cavity capable of high-$Q$ resonance in the ~7–40 Hz range.

On Earth those ingredients exist (with well-documented Schumann resonances). On the Moon they do not. Modern electromagnetic sounding (Apollo-era magnetometer experiments, Grimm 2023 LF inversions, Mittelholz et al. global conductivity structure) shows a continuous, temperature-dependent conductivity gradient in the outer hundreds of kilometers. There is no stable global ionosphere to act as an upper wall, and the outer shell itself is conduction-dominated at ELF ($\tan\delta \gg 1$).

The quantitative work in this repository therefore tests the Tesla-derived framing against the actual lunar conductivity structure:

1. **Model A (physical Moon)** — open upper boundary → no closed cavity.
2. **Model B (exploratory artificial lid)** — hypothetical conducting boundary at 100 km imposed as an upper-bound experiment → cavity $Q$ remains of order unity (median Monte Carlo $Q \approx 0.78$, maximum $\approx 2$).
3. Path-integral and lateral experiments — circumferential attenuation of tens to hundreds of dB for literature-bracketed profiles.

**Outcome of the reverse-engineering:** the lunar outer shell does not support the high-$Q$ global ELF modes required by the historical Tesla planetary-resonator architecture. The same calculations show it is a weakly conducting, large-skin-depth medium whose primary scientific value is geophysical (magnetotelluric / induction sounding), not as a planetary waveguide or wireless-power cavity.

The code, profiles, and figures document both the original exploratory motivation and the quantitative constraints that closed that path.

---

## Key Figures

### Conductivity Structure

![Literature-bracketed conductivity profiles](paper_figs/fig_sigma_profiles.png)

*Literature-bracketed $\sigma(r)$ profiles (optimistic / nominal / Apollo-style / pessimistic) used throughout the campaign.*

![Literature conductivity envelopes](paper_figs/fig_literature_sigma.png)

*Grimm (2023) LF preferred fit and related envelopes.*

### Skin Depth & Loss Regime

![Skin depth vs frequency](paper_figs/fig_skin_depth.png)

*Electromagnetic skin depth $\delta = \sqrt{2/\omega\mu\sigma}$ across the profile suite.*

![Loss tangent](paper_figs/fig_loss_tangent.png)

*Loss tangent $\tan\delta = \sigma/(\omega\varepsilon)$. Across the nominal and Apollo-style envelopes at 1–30 Hz, $\tan\delta \gg 1$: conduction current dominates.*

![Skin depth vs depth](paper_figs/fig_skin_vs_depth.png)

### Path Attenuation

![Circumferential path attenuation](paper_figs/fig_path_attenuation.png)

*Half-circumference and full-path attenuation. Nominal profiles produce tens to hundreds of dB of loss — global shell-guided waves are not supported.*

### Cavity Quality Factor

![Q summary](paper_figs/fig_Q_summary.png)

*Model B (artificial 100 km ionosphere) cavity $Q$ for named profiles. Physical Moon (Model A) has no closed cavity ($Q \equiv 0$).*

![Monte Carlo Q histogram](paper_figs/fig_mc_Q_hist.png)

*20 000 literature-bracketed Monte Carlo draws. Median $Q \approx 0.78$; maximum $Q \approx 2.0$; 100% of draws have $Q < 5$.*

![Q vs frequency](paper_figs/fig_Q_vs_freq.png)

### Surface Impedance & Transfer

![Surface impedance](paper_figs/fig_surface_impedance.png)

![90° transfer function](paper_figs/fig_transfer_90deg.png)

![Transfer vs angle](paper_figs/fig_transfer_vs_angle.png)

### Lateral / Regional Experiments

![Lateral path attenuation](paper_figs/fig_lateral_paths.png)

![Lateral Q](paper_figs/fig_lateral_Q.png)

---

## Exploratory Case: Artificial Ionosphere (Model B)

The physical Moon has no stable global ionosphere, so there is no closed Earth-like Schumann cavity (Model A → $Q \equiv 0$).  
As an exploratory upper-bound exercise we nevertheless imposed a **hypothetical conducting lid at 100 km** (Model B) and recomputed cavity quality factors with the impedance formula

$$
Q \approx \frac{\omega\mu_0 h}{2\,\mathrm{Re}(Z_g+Z_i)}\,.
$$

This is the most favorable simple artificial boundary that still respects the measured radial conductivity structure of the outer shell. Even under that assumption:

| Profile | $Q$ (n=1, ~38.8 Hz) | Ringing time $\tau \approx Q/(\pi f)$ |
|---------|---------------------|--------------------------------------|
| optimistic_cold | 0.35 | ~3 ms |
| nominal | 0.58 | ~5 ms |
| apollo_classic | 0.44 | ~4 ms |
| pessimistic_warm | 2.01 | ~16 ms |

Monte Carlo (20 000 literature-bracketed $\sigma(r)$ draws under the same artificial lid):

- median $Q \approx 0.78$
- maximum $Q \approx 2.0$
- **100 % of draws have $Q < 5$**

Conclusion of the exploratory case: adding an artificial upper wall does not produce a high-$Q$ global resonator. Distributed loss from the continuous conductivity gradient keeps $Q$ of order unity. The physical open-Moon case remains cavity-free.

Sensitivity of the artificial lid height and conductivity is examined in `paper_figs/fig_iono_sensitivity.png` and `results/campaign/iono_sensitivity.csv`.

---

## Paper & Reports

- **Rendered PDF**: [`paper/Lunar_Outer_Shell_ELF.pdf`](paper/Lunar_Outer_Shell_ELF.pdf)
- **HTML source**: [`paper/paper.html`](paper/paper.html)
- **Numeric appendices**:
  - [`paper/QUANTITATIVE_RESULTS.md`](paper/QUANTITATIVE_RESULTS.md)
  - [`paper/CAMPAIGN_REPORT.md`](paper/CAMPAIGN_REPORT.md)
  - [`paper/OPTIONAL_REPORT.md`](paper/OPTIONAL_REPORT.md)

---

## Physics Summary

1. **Phase 0** — Outer-shell $\sigma_{\mathrm{eff}}$, skin depth $\delta=\sqrt{2/\omega\mu\sigma}$, loss tangent $\tan\delta=\sigma/(\omega\varepsilon)$, circumferential path attenuation.
2. **Phase 1** — Layered surface impedance looking into $\sigma(r)$:
   - **Model A**: open Moon (no ionosphere) → no closed cavity.
   - **Model B**: artificial ionosphere (exploratory upper bound) with the $Q$ formula above.
   - **Model C**: Earth validation smoke test.
3. **Literature profiles** — Grimm (2023) LF fit $\sigma=1.76\times10^{-4}\exp(z_{\mathrm{km}}/210)$ plus Dyal–Parkin lid; Mittelholz-like global envelope; regional nearside/farside/PKT variants.
4. **Monte Carlo** — 20 000 literature-bracketed $\sigma(r)$ draws for $Q$ distributions under Model B.
5. **Lateral** — Piecewise great-circle paths and two-hemisphere effective $Q$.

---

## Quick Start

```bash
cd lunar-elf
python scripts/00_build_profiles.py
python scripts/01_skin_maps.py
python scripts/02_cavity_q_sweep.py
python scripts/03_driven_transfer.py
python scripts/04_make_paper_figs.py
python scripts/06_optional_tasks.py   # literature profiles, eigenmodes, lateral
# optional heavy MC:
python scripts/05_heavy_campaign.py --workers 80 --mc 20000
```

Figures land in `paper_figs/`; tables and CSVs in `results/`.

---

## Repository Layout

```
src/lunar_elf/          # core library (profiles, skin, sphere impedance, eigenmodes)
scripts/                # 00–06 analysis pipelines
data/profiles/          # CSV conductivity profiles
data/literature/        # source notes + Grimm arXiv PDF
paper/                  # manuscript + quantitative reports
paper_figs/             # publication-ready figures (PNG)
results/                # phase0 / phase1 / campaign / optional outputs
tests/
```

---

## Citation

If you use the results or code, please cite the accompanying note:

> Perry, N. D. (2026). *The Lunar Outer Shell as a Weakly Conducting, Large–Skin-Depth Medium at Extremely Low Frequencies*. Independent research note. Available in this repository (`paper/Lunar_Outer_Shell_ELF.pdf`).

---

## License

Research code accompanying an independent research note. See repository for terms.
