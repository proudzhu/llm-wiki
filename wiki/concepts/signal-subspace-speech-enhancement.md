---
type: concept
created: 2026-10-01
updated: 2026-10-01
sources:
  - raw/papers/doclo-2002-gsvd-optimal-filtering/full-text.md
tags:
  - speech-enhancement
  - signal-subspace
  - single-channel
  - linear-algebra
---

# Signal Subspace Speech Enhancement

**Signal subspace speech enhancement** is a family of non-parametric single-microphone techniques that model the clean speech signal as a low-rank vector in an $M$-dimensional vector space, and enhance noisy speech by separating the space into a **signal-plus-noise subspace** (low dimension, corresponding to the clean signal) and its orthogonal complement, the **noise subspace**. Enhancement removes the noise subspace and estimates the clean signal from the remaining signal-plus-noise subspace. The approach relies on the empirically supported low-rank property of clean speech (Flanagan 1980; McAulay & Quatieri 1986), and typically outperforms spectral subtraction in intelligibility and recognition.

All members of the family produce a filter matrix of the form

$$\mathbf{W} = \bar{\mathbf{Q}}^{-T}\,\mathrm{diag}\left\{f\left(\bar{\sigma}_i^2, \bar{\eta}_i^2\right)\right\}\bar{\mathbf{Q}}^{T}$$

where $(\bar{\sigma}_i^2, \bar{\eta}_i^2)$ are the generalized eigenvalues of the noisy-signal and noise correlation matrices, and the gain function $f$ implements the chosen estimation criterion — interpretable as a signal-dependent analysis filterbank, per-component gain, and synthesis filterbank.

## Taxonomy

[[sources/doclo-2002-gsvd-optimal-filtering|Doclo & Moonen 2002]] classify the family along four axes:

| Axis | Options |
|:-----|:--------|
| Noise assumption | white vs. colored (colored requires prewhitening or quotient SVD / frame-dependent processing) |
| Estimate type | least-squares, minimum variance, perceptually relevant (distortion-constrained) |
| Processing | block-based vs. adaptive (subspace tracking) |
| Averaging step | included vs. omitted |

Key members surveyed there:

| Technique | Noise | Estimate | Processing | Averaging |
|:----------|:------|:---------|:-----------|:----------|
| Dendrinos et al. 1991 (SVD) | white | LS of Toeplitz speech data matrix | block | yes (diagonal averaging) |
| Jensen et al. 1995 (QSVD) | colored (implicit prewhitening) | minimum variance | block | yes |
| Ephraim & Van Trees 1995 (KLT) | white | perceptual (min distortion s.t. residual-noise bound) | block | no |
| Huang & Zhao 1997 | white | + short-time energy constraint | block | no |
| Mittal & Phamdo 2000 (KLT) | colored (no prewhitening; speech/noise-dominated frames) | perceptual | block | no |
| Rezayee & Gazor 2001 (adaptive KLT) | white | perceptual | adaptive (PAST with deflation) | no |

## Findings from the Multimicrophone Extension

[[sources/doclo-2002-gsvd-optimal-filtering|Doclo & Moonen 2002]] extend the family to multiple microphones (see [[concepts/gsvd-based-optimal-filtering|GSVD-Based Optimal Filtering]]) and, in the process, establish two facts about the single-channel members:

1. **Symmetry/linear phase**: because the correlation matrices are symmetric Toeplitz (double symmetric), the filter matrix satisfies $\mathbf{W} = J\mathbf{W}J$ for white *and* colored noise and any gain function $f$; the middle column is a linear-phase filter — extending the zero-phase property previously attributed only to averaged SVD-truncation estimators in white noise.
2. **Averaging is suboptimal**: the diagonal-averaging step used by Dendrinos-type and Jensen-type algorithms is unnecessary and even suboptimal — there always exists an individual $L$-dimensional column filter with lower error variance than the $(2L-1)$-dimensional averaged filter, which also doubles the filter length.

## Related Concepts

- [[concepts/gsvd-based-optimal-filtering|GSVD-Based Optimal Filtering]] — the multimicrophone spatio-temporal extension
- [[concepts/singular-value-decomposition|Singular Value Decomposition]] — the underlying matrix factorization
- [[concepts/speech-distortion-constrained-noise-reduction|Speech-Distortion-Constrained Noise Reduction]] — the perceptual estimation criterion of the Ephraim–Van Trees branch
- [[concepts/wiener-filter|Wiener Filter]] — the $f(\cdot)$ gain of the MSE criterion

## Related Sources

- [[sources/doclo-2002-gsvd-optimal-filtering|Doclo & Moonen 2002: GSVD-Based Optimal Filtering for Single and Multimicrophone Speech Enhancement]] — the taxonomy above, the symmetry properties, and the averaging-suboptimality result
