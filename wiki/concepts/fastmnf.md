---
type: concept
created: 2026-05-20
updated: 2026-05-20
tags:
  - blind-source-separation
  - nonnegative-matrix-factorization
  - spatial-covariance-matrix
  - microphone-arrays
---

# FastMNMF

**Fast Multichannel Nonnegative Matrix Factorization (FastMNMF)** is a blind source separation method that models the observed multichannel signal as a sum of source components with full-rank spatial covariance matrices (SCMs), while assuming **joint diagonalizability** of the SCMs across sources to reduce computational cost.

## Formulation

The observed STFT coefficients $\bm{x}_{ij} \in \mathbb{C}^M$ follow:

$$p(\bm{x}_{ij}) = \mathcal{N}_{\mathbb{C}}\left(\bm{x}_{ij}; \bm{0}, \sum_n h_{ijn}\bm{R}_{in}\right)$$

where $h_{ijn} = \sum_k t_{ikn}v_{kjn}$ (NMF model for source spectrograms) and $\bm{R}_{in}$ is the source SCM.

## Joint Diagonalization Assumption

FastMNMF assumes that all source SCMs can be simultaneously diagonalized by a single transformation matrix $\bm{W}_i$:

$$\bm{W}_i^{\mathsf{H}}\bm{R}_{in}\bm{W}_i = \bm{\Lambda}_{in}, \quad \forall n=1,\dots,N$$

where $\bm{\Lambda}_{in}$ is diagonal. The decorrelated signals $\bm{y}_{ij} = \bm{W}_i^{\mathsf{H}}\bm{x}_{ij}$ then have covariance $\sum_n h_{ijn}\bm{\Lambda}_{in}$.

## Computational Advantage

| Method | Matrix operations |
|--------|-----------------|
| Standard MNMF | Invert $M \times M$ per time-frequency point: $\mathcal{O}(IJM^3)$ |
| FastMNMF | Invert $M \times M$ per frequency per microphone: $\mathcal{O}(IM^4)$ |

FastMNMF avoids the $\mathcal{O}(M^3)$ per time-frequency-point inversions by diagonalizing the spatial model, at the cost of $\mathcal{O}(M^4)$ per frequency for the joint diagonalization.

## Update Rules

- **$\bm{W}_i$** (transformation matrix): Iterative Projection (IP), Eqs. (5)-(7)
- **$t_{ikn}, v_{kjn}$** (NMF variables): MM algorithm, Eqs. (8)-(9)
- **$\bm{\Lambda}_{in}$** (diagonalized SCMs): MM algorithm, Eq. (10)

Parameters are estimated by alternating the above updates. Source images are reconstructed via the multichannel Wiener filter.

## Distributed FastMNMF

For distributed microphone arrays, the SCMs can be constrained to be block-diagonal, with each block corresponding to a subarray. This reduces complexity to $\mathcal{O}(\sum_l M^{(l)4})$ per iteration per frequency while sharing the NMF spectrogram model across subarrays (Nishikori et al. 2026).

## Related Concepts

- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- Independent Low-Rank Matrix Analysis (ILRMA)
- Independent Vector Analysis (IVA)

## Related Sources

- [[sources/nishikori-2026-fast-multichannel-nmf-block-diagonal-scm-bss|Nishikori et al. 2026: Distributed FastMNMF for BSS]]
