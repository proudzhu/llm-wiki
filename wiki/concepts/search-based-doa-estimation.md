---
type: concept
created: 2026-08-22
updated: 2026-08-22
sources:
  - raw/papers/tesch-2024-spatially-selective-nonlinear-filters/full-text.md
tags:
  - direction-of-arrival
  - multi-channel
  - speech-separation
  - spatial-filtering
  - peak-finding
---

# Search-based DoA Estimation (for SSF)

**Search-based DoA estimation** for the [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Filter (SSF)]] is a blind-localization strategy proposed by Tesch & Gerkmann (2024): evaluate the SSF on a grid of candidate target directions, compute the energy of each filtered output, and detect speaker locations as peaks in the resulting energy curve. It exploits the SSF's inherent spatial selectivity to turn the filter itself into a localizer, at the cost of one SSF forward pass per candidate direction.

## Procedure

1. **Grid search** — for each candidate target direction $\varphi \in \{0^\circ, 4^\circ, \dots, 356^\circ\}$ (4° resolution used in the paper), run the SSF on the mixture and obtain the filtered signal $\hat{S}_\varphi(k, i)$.
2. **Speech-active framing** — partition the filtered signal into 10 ms non-overlapping segments and compute per-segment energy; mark segments as speech-active if their energy is within 45 dB of the maximum energy in the mixture (following [44]).
3. **Average energy curve** — average per-segment energy over speech-active segments to obtain a robust energy-per-direction curve $E(\varphi)$.
4. **Peak finding** — run `scipy.signal.find_peaks` on the normalised $E(\varphi)$:
   - Initial parameters: prominence 0.009, height 0.05, width 1.
   - If too few peaks are detected, re-run with relaxed parameters (no width requirement, prominence 0.001, height 0.025).
   - Merge peaks that are close together and have similar height (likely the same speaker).
   - If more peaks than expected speakers are found, keep the highest ones.

## Properties

- **Computationally expensive**: requires as many SSF forward passes as there are candidate directions (≈90 at 4° resolution). The authors note this is "too computationally demanding for most realistic applications" and propose the [[concepts/dnn-based-doa-classifier|DNN-based classifier]] as the practical alternative.
- **Accurate despite cost**: the mean angular error is small (1.57° for 2 speakers with JNF-SSF, growing to 3.54° for 5 speakers).
- **Diagnostic value**: visualising the per-direction energy curve and per-direction POLQA score (Figure 4 of the source) reveals the spatial selectivity profile of the SSF and explains why slight uncorrelated DoA errors are sometimes *beneficial* — the POLQA peak can be offset from the true direction, so an uncorrelated error that lands on the POLQA peak improves separation.

## Empirical Findings (Tesch & Gerkmann 2024)

Mean angular error vs. number of speakers (Table IV):

| Method | 2 spk | 3 spk | 5 spk |
|:-------|:------|:------|:------|
| search (JNF-SSF) | 1.57 ± 0.12° | 2.06 ± 0.19° | 3.54 ± 0.25° |
| search (McNet-SSF) | 2.07 ± 0.07° | 2.53 ± 0.15° | 3.99 ± 0.23° |
| [[concepts/dnn-based-doa-classifier\|DNN classifier]] | **1.06 ± 0.03°** | **1.24 ± 0.09°** | **2.13 ± 0.19°** |

When McNet-SSF is steered with search-based DoAs (row 7 of Table II), separation performance is *slightly better* than with oracle DoAs for 2 and 3 speakers (ΔPOLQA 1.91 vs. 1.85, 1.80 vs. 1.76) — a counter-intuitive effect explained by the POLQA-curve observation above. For 5 speakers, search-based (1.43) matches oracle (1.43).

JNF-SSF yields tighter localization than McNet-SSF — JNF's stronger spatial selectivity produces sharper energy peaks.

## Related Concepts

- [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Non-Linear Filter (SSF)]]
- [[concepts/dnn-based-doa-classifier|DNN-based DoA Classifier]]
- [[concepts/joint-nonlinear-filtering|Joint Nonlinear Filtering (JNF)]]
- [[concepts/mcnet|McNet]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]

## Related Sources

- [[sources/tesch-2024-spatially-selective-nonlinear-filters|Tesch & Gerkmann 2024: Multi-channel Speech Separation Using Spatially Selective Deep Non-linear Filters]]
