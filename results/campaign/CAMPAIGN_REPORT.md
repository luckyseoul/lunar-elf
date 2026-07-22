# Heavy campaign results (Soulkiller local)

Generated: 2026-07-22 22:34:17

## Monte Carlo cavity Q (Model B, n=1, h=100 km)

- N draws: **20000**
- median Q: **0.778**
- mean Q: **0.923**
- p05 / p95: **0.295** / **1.85**
- max Q: **2.01**
- fraction Q < 1: **64.7%**
- fraction Q < 5: **100.0%**
- fraction Q < 10: **100.0%**

Interpretation: across the literature-bracketed envelope, high-Q global modes (Q≳10) are essentially absent under Model B; the physical open Moon (Model A) has no cavity at all.

## Named profiles (Model B)

| Profile | n | f (Hz) | Q | Re(Zg) | σ_eff |
|---|---:|---:|---:|---:|---:|
| apollo_classic | 1 | 38.84 | 0.444 | 3.063e+01 | 6.26e-08 |
| apollo_classic | 2 | 67.27 | 0.483 | 4.980e+01 | 6.26e-08 |
| apollo_classic | 3 | 95.13 | 0.504 | 6.846e+01 | 6.26e-08 |
| nominal | 1 | 38.84 | 0.577 | 2.267e+01 | 1.31e-07 |
| nominal | 2 | 67.27 | 0.646 | 3.597e+01 | 1.31e-07 |
| nominal | 3 | 95.13 | 0.691 | 4.825e+01 | 1.31e-07 |
| optimistic_cold | 1 | 38.84 | 0.348 | 4.018e+01 | 1.28e-08 |
| optimistic_cold | 2 | 67.27 | 0.312 | 7.984e+01 | 1.28e-08 |
| optimistic_cold | 3 | 95.13 | 0.273 | 1.314e+02 | 1.28e-08 |
| pessimistic_warm | 1 | 38.84 | 2.01 | 3.723e+00 | 1.21e-05 |
| pessimistic_warm | 2 | 67.27 | 2.63 | 4.961e+00 | 1.21e-05 |
| pessimistic_warm | 3 | 95.13 | 3.11 | 5.936e+00 | 1.21e-05 |

## Artifacts

- `results/campaign/mc_q.csv`
- `results/campaign/named_q.csv`
- `results/campaign/iono_sensitivity.csv`
- `results/campaign/path_attenuation.csv`
- `results/campaign/progress.json`
- `results/campaign/campaign.log`
- `paper_figs/fig_mc_Q_hist.png`
- `paper_figs/fig_mc_Q_vs_sigma.png`
- `paper_figs/fig_iono_sensitivity.png`
