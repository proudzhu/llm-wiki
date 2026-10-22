---
type: concept
created: 2026-08-27
updated: 2026-10-22
sources:
  - raw/papers/guldenschuh-2014-secondary-path-irregularities/full-text.md
  - raw/papers/rout-2012-pso-anc-without-secondary-path/full-text.txt
  - raw/papers/yuan-2026-open-ear-anc-smart-glasses/full-text.md
tags:
  - active-noise-control
  - secondary-path
  - robustness
  - headphones
---

# Secondary Path Variability

**Secondary-path variability** refers to changes in the secondary-path transfer function $G(j\omega)$ (loudspeaker → error microphone inside the ear-cup) of an ANC headphone caused by fit changes: leaks between ear-cup and ear, lifting the headphones, or removing them entirely.

## Key Finding: Leaks Attack the Low Frequencies

[[sources/guldenschuh-2014-secondary-path-irregularities|Guldenschuh & de Callafon (2014)]] measured the secondary-path of prototype headphones under four conditions (tight, one leak, two leaks, completely loose) on a dummy head, plus 16 measurements on two real persons:

- Increased leakage causes primarily a **low-frequency magnitude drop-off** of $G$ — the tight-fit response is lost first below a few hundred Hz
- The additive uncertainty $U_{\max}(\omega)$ relative to the tight nominal model reaches **17.3 dB below 300 Hz** (dominated by the leaky paths, worst around 300 Hz)
- The phase error exceeds 90° around 1300 Hz for open (lifted) headphones

## Open-Ear Wearables: Anatomical Variability

On open-ear devices the variability mechanism differs: there is no ear-cup to leak, but the secondary path (frame speaker → ear) varies with head geometry, ear shape, and glasses fit. [[sources/yuan-2026-open-ear-anc-smart-glasses|Yuan, Liu & Xiao 2026]] measured noticeably different secondary-path impulse responses across participants on smart glasses; a one-time ESS calibration improves mean reduction by 1.6 dB (9.6 → 11.2 dB) and cuts inter-user standard deviation from 1.5 dB to 0.4 dB. At the 100–1000 Hz operating band the long wavelengths make the system robust to glasses displacement (looking down, head shaking, removing/re-wearing: 10.7–11.3 dB vs 11.3 dB at rest) without recalibration. See [[concepts/virtual-in-ear-sensing|Virtual In-ear Sensing]].

## Consequences

1. **Adaptation instability**: a phase deviation >90° between $\hat{G}$ and $G$ makes the FxLMS/NFxLMS adaptation diverge — requires the [[leaky-fxlms-algorithm|leaky FxLMS]]
2. **Feedback instability**: the low-frequency magnitude drop of $G$ forces low-frequency poles outward; the resulting poles outside the unit circle cause ringing. Since $|W(\hat{G} - G)|$ first violates unity gain **below 300 Hz**, the instability manifests at low frequencies
3. **Detection opportunity**: because the adaptive filter $W$ identifies $G^{-1}$, a low-frequency drop in $G$ shows up as **DC-gain growth in $W$** — the basis of the [[dc-gain-stability-constraint|DC-gain stability constraint]]
4. **Gradient-free immunity**: population-based controllers sidestep the estimate entirely — the [[concepts/conditional-reinitialized-pso|CRPSO]]-based ANC of [[sources/rout-2012-pso-anc-without-secondary-path|Rout, Das & Panda 2012]] never identifies $S(z)$; instead it detects the abrupt change itself from a jump in the swarm's global-best squared error (after a converged plateau) and re-randomizes the particle population to re-converge to the new optimum

## Contrast with Primary Path Variability

| | Primary path $P(z)$ | Secondary path $G(z)$ |
|--|--------------------|----------------------|
| Cause | Direction of arrival of the noise | Headphone fit (leaks, lifting) |
| Affects | [[feedforward-anc|Feedforward ANC]] | [[feedback-anc|Feedback ANC]] (and FxLMS adaptation in general) |
| Frequency behavior | Severe above 1 kHz (housing resonances) | Severe below ~300 Hz (leak-induced drop-off) |

## Related Concepts

- [[concepts/dc-gain-stability-constraint|DC-Gain Stability Constraint]] — run-time detection of secondary-path irregularities
- [[concepts/primary-path-variability|Primary Path Variability]] — the feedforward-side analog
- [[concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/online-secondary-path-modeling|Online Secondary-Path Modeling]] — the tracking alternative
- [[concepts/uncertainty-modeling-for-anc|Uncertainty Modeling for ANC]]
- [[concepts/leaky-fxlms-algorithm|Leaky FxLMS Algorithm]] — adaptation-stability remedy
- [[concepts/conditional-reinitialized-pso|Conditional Reinitialized PSO]] — gradient-free population-based remedy that never estimates $S(z)$
- [[concepts/virtual-in-ear-sensing|Virtual In-ear Sensing]] — anatomical (fit-driven) variability on open-ear glasses, handled by one-time ESS calibration + FiLM conditioning

## Related Sources

- [[sources/guldenschuh-2014-secondary-path-irregularities|Guldenschuh & de Callafon 2014: Detection of Secondary-Path Irregularities in ANC Headphones]]
- [[sources/liebich-2018-doa-dependency-anc-headphones|Liebich 2018: DOA Dependency of ANC Headphones]] — complementary primary-path variability measurements
- [[sources/rout-2012-pso-anc-without-secondary-path|Rout, Das & Panda 2012: PSO-Based ANC Without Secondary Path Identification]] — detects abrupt secondary-path changes via the gbest squared-error jump and re-randomizes the PSO population instead of estimating $S(z)$
- [[sources/yuan-2026-open-ear-anc-smart-glasses|Yuan, Liu & Xiao 2026: Active Noise Cancellation on Open-Ear Smart Glasses]] — anatomical secondary-path variability on open-ear glasses; one-time ESS calibration +1.6 dB, inter-user std 1.5→0.4 dB
