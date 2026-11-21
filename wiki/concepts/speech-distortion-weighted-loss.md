---
type: concept
created: 2026-11-21
updated: 2026-11-21
sources:
  - raw/papers/braun-2021-loss-functions-speech-enhancement/full-text.md
tags:
  - loss-function
  - speech-enhancement
  - deep-learning
  - speech-distortion
  - noise-reduction
---

# Speech-Distortion-Weighted Loss (SDW)

The **speech-distortion-weighted (SDW) loss** is a single-channel DNN training objective that scores the speech and noise components of the enhanced output separately, with one weight trading speech distortion against noise reduction:

$$
\mathcal{L}_{\mathrm{SDW}} = \lambda \left\langle |S - GS|^{2} \right\rangle \;+\; (1-\lambda) \left\langle |GN|^{2} \right\rangle, \qquad 0 < \lambda < 1,
$$

evaluated per T-F bin from the estimated gain $G$, the clean speech $S$, and the noise $N$. It is the deep-learning counterpart of the classical speech-distortion-constrained noise-reduction criterion (see [[concepts/speech-distortion-constrained-noise-reduction|Speech-Distortion-Constrained Noise Reduction]] for the multichannel Wiener/PMWF lineage, from which the same trade-off parameter descends). It was introduced for real-time neural enhancement by Xia et al. (ICASSP 2020, "Weighted speech distortion losses") and evaluated independently by [[sources/braun-2021-loss-functions-speech-enhancement|Braun & Tashev 2021]].

## Structural Properties

- **It is a magnitude loss, not a phase-aware one.** Equation (17) never contains the noisy spectrum $X$, so nothing in it depends on the phase of $G$: a zero-phase (real, non-negative) gain is optimal. Braun & Tashev therefore classify SDW in the magnitude column of their taxonomy despite its complex-looking form.
- **The weight is data dependent.** The best $\lambda$ was 0.3 in Xia et al. 2020, 0.5 in Xu et al. 2020, and **0.6** in Braun & Tashev's reverberant setting. There is no closed-form rule connecting $\lambda$ to SNR or corpus; the paper calls SNR-dependent adjustments "heuristic and difficult to determine".
- **It has no complex counterpart.** Unlike every other row of the taxonomy, SDW cannot be written in a phase-aware form, which is why it takes no part in the [[concepts/mixed-magnitude-complex-loss|magnitude-complex mixture]].

## The Reverberant-Data Counter-Result

On non-reverberant data SDW had been reported to beat plain MSE. Braun & Tashev's controlled test on reverberant CHiME-2 did not reproduce that: at its PESQ-optimal $\lambda=0.6$, SDW scored **3.12 PESQ / 9.61 dB SI-SDR**, below magnitude MSE (3.16 / 9.57) and below cMSE (3.10 / 9.58) on PESQ — i.e. the decomposition-driven loss lost to the naive baseline. Their reading is data dependence rather than a defect in the criterion: with reverberant speech the "speech" term already contains late reverberation, so penalizing its deviation from $GS$ pushes the gain toward reproducing the room response.

## Related Concepts

- [[concepts/speech-distortion-constrained-noise-reduction|Speech-Distortion-Constrained Noise Reduction]] — the classical constrained-optimization framework SDW descends from
- [[concepts/generalized-loss-function|Generalized Loss Function]] — Li et al. 2020's generalization, which also separates speech-distortion and residual-noise terms but targets a *preset* residual-noise level
- [[concepts/mixed-magnitude-complex-loss|Mixed Magnitude-Complex Loss]]
- [[concepts/frequency-domain-loss|Frequency Domain Loss]]
- [[concepts/pesq|PESQ]] / [[concepts/si-sdr|SI-SDR]]

## Related Sources

- [[sources/braun-2021-loss-functions-speech-enhancement|Braun & Tashev 2021: A Consolidated View of Loss Functions]] — the reverberant-data counter-result, the $\lambda=0.6$ optimum, and the zero-phase-optimality argument that files SDW as a magnitude loss
