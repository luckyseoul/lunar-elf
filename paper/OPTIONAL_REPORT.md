# Optional tasks — complete

Generated: 2026-07-22 22:42:44 on soulkiller

## 1. Literature-anchored profiles

Grimm (2023) LF analytic fit σ=1.76×10⁻⁴ exp(z/210) for 400–1200 km, with Dyal–Parkin resistive lid. Mittelholz-like global envelope (constructed, not figure-digitized). HF envelope retained as upper bound only.

| Profile | σ_eff(0–300 km) | δ(10 Hz) km | tanδ(10 Hz) | A_½circ(10 Hz) dB |
|---|---:|---:|---:|---:|
| grimm_lf_preferred | 1.38e-07 | 428.5 | 4.51e+01 | 110.6 |
| grimm_hf_envelope | 5.67e-06 | 66.8 | 1.85e+03 | 709.6 |
| mittelholz_like | 1.62e-06 | 125.1 | 5.29e+02 | 379.1 |
| hood_upper_resistive | 3.01e-08 | 916.9 | 9.85e+00 | 51.7 |

## 2. Multipole eigenmode / impedance cross-check

| Profile | n | Q | notes |
|---|---:|---:|---|
| grimm_lf_preferred | 1 | 0.781 | impedance_Q=0.7814; spectral_FWHM_Q=0.8114; f_peak=11.651… |
| grimm_lf_preferred | 2 | 0.642 | impedance_Q=0.642; spectral_FWHM_Q=0.8541; f_peak=20.181… |
| grimm_lf_preferred | 3 | 0.452 | impedance_Q=0.4522; spectral_FWHM_Q=0.9015; f_peak=28.540… |
| grimm_hf_envelope | 1 | 1.11 | impedance_Q=1.111; spectral_FWHM_Q=0.5071; f_peak=11.651… |
| grimm_hf_envelope | 2 | 1.32 | impedance_Q=1.316; spectral_FWHM_Q=0.4773; f_peak=20.181… |
| grimm_hf_envelope | 3 | 1.47 | impedance_Q=1.47; spectral_FWHM_Q=0.4636; f_peak=28.540… |
| mittelholz_like | 1 | 1.08 | impedance_Q=1.08; spectral_FWHM_Q=0.7376; f_peak=11.651… |
| mittelholz_like | 2 | 1.08 | impedance_Q=1.078; spectral_FWHM_Q=0.7727; f_peak=20.181… |
| mittelholz_like | 3 | 0.991 | impedance_Q=0.9907; spectral_FWHM_Q=0.8114; f_peak=28.540… |
| hood_upper_resistive | 1 | 0.494 | impedance_Q=0.4937; spectral_FWHM_Q=0.8114; f_peak=11.651… |
| hood_upper_resistive | 2 | 0.339 | impedance_Q=0.3386; spectral_FWHM_Q=0.9015; f_peak=20.181… |
| hood_upper_resistive | 3 | 0.197 | impedance_Q=0.1966; spectral_FWHM_Q=1.014; f_peak=28.540… |
| farside_cold | 1 | 0.828 | impedance_Q=0.8284; spectral_FWHM_Q=0.8541; f_peak=11.651… |
| farside_cold | 2 | 0.662 | impedance_Q=0.6615; spectral_FWHM_Q=0.9015; f_peak=20.181… |
| farside_cold | 3 | 0.431 | impedance_Q=0.431; spectral_FWHM_Q=0.9545; f_peak=28.540… |
| pkt | 1 | 0.936 | impedance_Q=0.9362; spectral_FWHM_Q=0.7055; f_peak=11.651… |
| pkt | 2 | 0.926 | impedance_Q=0.9258; spectral_FWHM_Q=0.7376; f_peak=20.181… |
| pkt | 3 | 0.864 | impedance_Q=0.8639; spectral_FWHM_Q=0.7376; f_peak=28.540… |
| nearside_warm | 1 | 0.776 | impedance_Q=0.7756; spectral_FWHM_Q=0.7727; f_peak=11.651… |
| nearside_warm | 2 | 0.694 | impedance_Q=0.6937; spectral_FWHM_Q=0.8114; f_peak=20.181… |
| nearside_warm | 3 | 0.57 | impedance_Q=0.5697; spectral_FWHM_Q=0.8541; f_peak=28.540… |

## 3. Lateral heterogeneity (PKT / nearside–farside)

### Regional columns

| Region | Q_n1 | Re(Zg) | σ_eff | att 90° @10 Hz (dB) |
|---|---:|---:|---:|---:|
| grimm_lf_preferred | 0.781 | 1.571e+01 | 1.38e-07 | 55.3 |
| nearside_warm | 0.776 | 1.585e+01 | 5.20e-07 | 107.4 |
| farside_cold | 0.828 | 1.459e+01 | 5.73e-08 | 35.7 |
| pkt | 0.936 | 1.246e+01 | 3.23e-06 | 267.6 |

### Two-hemisphere effective Q

| Pair | Q_eff | Q_a | Q_b |
|---|---:|---:|---:|
| nearside_farside | 0.801 | 0.776 | 0.828 |
| pkt_farside | 0.879 | 0.936 | 0.828 |
| global_global | 0.781 | 0.781 | 0.781 |

### Path attenuation samples (10 Hz)

- **global_90_10Hz**: 55.3 dB
- **nearside_90_10Hz**: 107.4 dB
- **farside_90_10Hz**: 35.7 dB
- **mixed_NS_90_10Hz**: 71.5 dB
- **through_PKT_90_10Hz**: 136.9 dB

## Conclusion

Literature-anchored 1-D profiles, multipole cross-checks, and regional nearside/farside/PKT experiments all continue to show **no high-Q global cavity**: open Moon has no ionospheric wall; even with an artificial wall, Q remains O(1); lateral contrasts change path attenuation but do not create a high-Q resonator.
