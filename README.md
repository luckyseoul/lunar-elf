# lunar-elf

Quantitative ELF electromagnetic modeling of the lunar outer shell, supporting the note:

**The Lunar Outer Shell as a Weakly Conducting, Large–Skin-Depth Medium at Extremely Low Frequencies**

Nicholas D. Perry · Council Bluffs, Iowa · nick@perrybrandsllc.com

## Headline results

| Claim | Result |
|-------|--------|
| Loss tangent at 1–30 Hz | \(\tan\delta \gg 1\) (conduction-dominated) |
| Physical Moon (no ionosphere) | No closed Schumann-type cavity |
| Hypothetical 100 km ionosphere | Cavity \(Q \lesssim 2\) for literature profiles |
| Monte Carlo (20 000 draws) | median \(Q \approx 0.78\), max \(Q \approx 2.0\), **100% have \(Q < 5\)** |
| Nearside / farside / PKT | Path attenuation changes; no high-\(Q\) resonator |

## Paper

- Rendered PDF: [`paper/Lunar_Outer_Shell_ELF.pdf`](paper/Lunar_Outer_Shell_ELF.pdf)
- HTML source: [`paper/paper.html`](paper/paper.html)
- Numeric appendices: `paper/QUANTITATIVE_RESULTS.md`, `CAMPAIGN_REPORT.md`, `OPTIONAL_REPORT.md`

## Quick start

```bash
cd lunar-elf
python scripts/00_build_profiles.py
python scripts/01_skin_maps.py
python scripts/02_cavity_q_sweep.py
python scripts/03_driven_transfer.py
python scripts/04_make_paper_figs.py
python scripts/06_optional_tasks.py   # literature profiles, eigenmodes, lateral
# optional heavy MC (80 workers):
python scripts/05_heavy_campaign.py --workers 80 --mc 20000
```

Figures land in `paper_figs/`; tables in `results/`.

## Physics (short)

1. **Phase 0** — outer-shell \(\sigma_{\mathrm{eff}}\), skin depth \(\delta=\sqrt{2/\omega\mu\sigma}\), loss tangent \(\tan\delta=\sigma/(\omega\varepsilon)\), path attenuation.
2. **Phase 1** — layered surface impedance looking into \(\sigma(r)\); Model A open Moon; Model B artificial ionosphere with
   \[
   Q \approx \frac{\omega\mu_0 h}{2\,\mathrm{Re}(Z_g+Z_i)}\,;
   \]
   Model C Earth validation.
3. **Literature profiles** — Grimm (2023) LF fit \(\sigma=1.76\times10^{-4}\exp(z_{\mathrm{km}}/210)\) plus Dyal–Parkin lid; Mittelholz-like global envelope; regional nearside/farside/PKT variants.
4. **Monte Carlo** — 20k literature-bracketed \(\sigma(r)\) draws for \(Q\) distributions.
5. **Lateral** — piecewise great-circle paths and two-hemisphere effective \(Q\).

## Layout

```
src/lunar_elf/          # library
scripts/                # 00–06 pipelines
data/profiles/          # CSV conductivity profiles
data/literature/        # sources notes (+ Grimm arXiv PDF if present)
paper/                  # manuscript + reports
paper_figs/             # publication figures
results/                # phase0 / phase1 / campaign / optional
tests/
```

## License

Research code accompanying an independent research note. Cite the paper PDF if you use the results.
