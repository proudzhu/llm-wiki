---
type: concept
created: 2026-05-21
updated: 2026-08-24
sources:
  - raw/papers/guo-2023-iva-survey/full-text.md
  - raw/papers/dong-2026-spatially-regularized-switching-iva/full-text.md
  - raw/papers/ruan-2024-speech-extraction-low-snr/full-text.md
  - raw/papers/scheibler-2020-fast-independent-vector-extraction/full-text.md
tags:
  - blind-source-separation
  - audio-source-separation
  - optimization-algorithms
---

# Independent Vector Analysis

**Independent Vector Analysis (IVA)** is a multivariate extension of Independent Component Analysis (ICA) for frequency-domain [[concepts/blind-source-separation|blind source separation]] of convolutive audio mixtures. IVA models each source as a random vector spanning all frequency bins and exploits inter-frequency statistical dependencies to jointly estimate unmixing matrices, thereby inherently resolving the permutation ambiguity that plagues per-bin ICA.

## Problem Setting

Given $M$ microphone observations in the STFT domain:

$$\mathbf{x}^{(k)}[z] = \mathbf{A}^{(k)}\mathbf{s}^{(k)}[z], \quad k = 1, \ldots, K$$

IVA seeks unmixing matrices $\mathbf{W}^{(k)}$ for all frequency bins simultaneously by minimizing:

$$\mathcal{I}_{\mathrm{IVA}} = \sum_n E_{\mathbf{y}_n}\log g(\mathbf{y}_n) - 2\sum_k \log|\det\mathbf{W}^{(k)}| - \text{const.}$$

where $\mathbf{y}_n = [y_n^{(1)}, \ldots, y_n^{(K)}]^T$ is the estimated source vector of source $n$ across all frequency bins.

## Key Properties

1. **Permutation-free**: By modeling joint distributions $g(\mathbf{y}_n)$ across frequency bins, the separated sources are automatically aligned — no post-hoc permutation alignment is needed.
2. **Source prior flexibility**: Common choices include multivariate Laplacian, Gaussian mixture models, Student-t mixtures, and deep-learning-based priors.
3. **Separation vs. extraction**: Full IVA separates all sources simultaneously; [[concepts/independent-vector-extraction|Independent Vector Extraction (IVE)]] targets a single source of interest — and at extremely low SNR, the choice of optimization parameter (mixing vs. demixing vector) becomes decisive ([[concepts/ogive|OGIVE]]).

## Three Assumptions

1. Elements in a source vector are independent of elements in other source vectors.
2. Within a source vector, dependencies exist among elements (across frequency bins).
3. The number of sources $N \leq M$ (number of microphones).

## Optimization Methods

Six main families of update rules have been developed for IVA:

| Family | Key idea | Convergence |
|--------|----------|-------------|
| [[concepts/natural-gradient\|Natural Gradient]] | Step-size-based Riemannian descent (premultiply by $\mathbf{W}^{\mathrm{H}}\mathbf{W}$) | Slow; step-size sensitive |
| FastIVA | Newton fixed-point iteration | Fast; no step-size |
| AuxIVA | Auxiliary function (majorize-minimize) | Monotonic; stable |
| EM | Expectation-maximization for latent variables | Handles noise models |
| BCD (IP/ISS/IPA) | Block coordinate descent with closed-form updates | Widely used; efficient |
| EVD | Eigenvalue decomposition for extraction ([[concepts/fast-independent-vector-extraction\|FIVE]]) | Very fast for single source |

AuxIVA (Ono 2011) is the most widely adopted baseline due to its guaranteed monotonic convergence without tuning parameters.

## Relationship to ILRMA and FastMNMF

IVA combined with Nonnegative Matrix Factorization gives **[[concepts/independent-low-rank-matrix-analysis|Independent Low-Rank Matrix Analysis (ILRMA)]]**, which uses NMF to model source spectral structure. [[concepts/multichannel-nmf|MNMF]] generalizes the rank-1 spatial model of ILRMA to a full-rank per-source spatial property matrix, and [[concepts/fastmnmf|FastMNMF]] further imposes joint diagonalizability of these spatial covariances for computational efficiency. The dual derivation of ILRMA from the IVA cost function (this page) and the MNMF Gaussian likelihood is unified in [[sources/sawada-2019-bss-ilrma-review|Sawada et al. 2019]].

## Related Concepts

- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/blind-source-extraction|Blind Source Extraction]]
- [[concepts/independent-vector-extraction|Independent Vector Extraction]]
- [[concepts/ogive|OGIVE]]
- [[concepts/fast-independent-vector-extraction|Fast Independent Vector Extraction]]
- [[concepts/natural-gradient|Natural Gradient]]
- [[concepts/independent-low-rank-matrix-analysis|Independent Low-Rank Matrix Analysis]]
- [[concepts/multichannel-nmf|Multichannel NMF]]
- [[concepts/fastmnmf|FastMNMF]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/switching-independent-vector-analysis|Switching Independent Vector Analysis]]
- [[concepts/iterative-source-steering|Iterative Source Steering]]
- [[concepts/spatial-regularization|Spatial Regularization]]

## Related Sources

- [[sources/guo-2023-iva-survey|Guo, Luo & Li 2023: IVA Survey]]
- [[sources/nishikori-2026-fast-multichannel-nmf-block-diagonal-scm-bss|Nishikori et al. 2026: Distributed FastMNMF for BSS]]
- [[sources/dong-2026-spatially-regularized-switching-iva|Dong et al. 2026: Spatially-Regularized Switching IVA with ISS]]
- [[sources/sawada-2019-bss-ilrma-review|Sawada et al. 2019: BSS/ILRMA Review]]
- [[sources/ruan-2024-speech-extraction-low-snr|Ruan, Liao, Chen & Lu 2024: Speech Extraction Under Extremely Low SNR Conditions]]
- [[sources/scheibler-2020-fast-independent-vector-extraction|Scheibler & Ono 2020: Fast Independent Vector Extraction]]
