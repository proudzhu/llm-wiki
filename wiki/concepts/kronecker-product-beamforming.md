---
type: concept
created: 2026-09-14
updated: 2026-09-17
sources:
  - raw/papers/zhu-2025-kronecker-superdirective-beamforming/full-text.txt
  - raw/papers/wang-2021-kronecker-adaptive-beamforming/full-text.txt
  - raw/papers/cohen-2019-differential-kronecker-beamforming/full-text.txt
tags:
  - beamforming
  - microphone-arrays
  - kronecker-product
  - low-rank
  - robustness
---

# Kronecker Product Beamforming

**Category**: Low-Rank / Structured Beamforming

## Definition

Kronecker product beamforming decomposes a global (long) beamforming filter of length $M$ into a product of short filters via the Kronecker product, exploiting the factorization $M = \prod_{n=1}^{N} L_n$. This reduces the parameter count from $M$ to $\sum_{n=1}^{N} L_n$ per factor group and shrinks the matrix inversions needed in the design from $M \times M$ to $L_n \times L_n$ — while often *improving* robustness, since the low-rank structure regularizes the filter.

## Development

- **Differential Kronecker product beamforming** ([[sources/cohen-2019-differential-kronecker-beamforming|Cohen, Benesty & Chen 2019]], IEEE/ACM TASLP): the original formulation linking Kronecker decompositions to [[concepts/differential-microphone-array|differential microphone arrays]]. For arrays with $M = M_1 M_2$ microphones whose steering vector factorizes as $\mathbf{d} = \mathbf{d}_1 \otimes \mathbf{d}_2$ (two virtual ULAs), the differential beamformer is decomposed as $\mathbf{h} = \mathbf{h}_1 \otimes \mathbf{h}_2$ ($M_1 + M_2$ coefficients instead of $M_1 M_2$). The global beampattern and [[concepts/white-noise-gain|WNG]] factorize as products of the virtual-array quantities, but the directivity factor and front-to-back ratio do not ($\boldsymbol{\Gamma} \neq \boldsymbol{\Gamma}_1 \otimes \boldsymbol{\Gamma}_2$) — motivating alternating iterations for the KP hypercardioid (DF maximization, ~5 iterations) and KP supercardioid (FBR maximization, ~3 iterations), alongside closed-form KP cardioid and dipole designs.
- **Specific geometries** (rectangular arrays, cube arrays): 2-D/3-D Kronecker decompositions matched to regular array structures.
- **Arbitrary geometries** ([[sources/wang-2021-kronecker-adaptive-beamforming|Wang et al. 2021]], APSIPA-ASC): the first generalization to arbitrary 3-D array geometries — the filter is represented as a **sum of $P$ Kronecker products** of subfilters (a property of the filter, not the array), with the iterative [[concepts/kmvdr-beamformer|KMVDR]] algorithm deriving the MVDR beamformer under this representation.
- **Low-rank differential beamforming with nonuniform linear arrays** (Pei et al. 2025, ICASSP).
- **Multidimensional generalization** (Zhu et al. 2025): extends the mostly two-dimensional formulations to **N-way, rank-P** decompositions applicable to arbitrary array geometries, with a systematic comparison of decomposition modes — building on the arbitrary-geometry framework of Wang et al. 2021.

## Multidimensional, Rank-P Formulation (LR-RSD)

The length-$M$ filter is written as a sum of $P$ Kronecker products of $N$ short filters (Zhu et al. 2025):

$$\mathbf{h}_{\mathrm{P}} = \sum_{p=1}^{P} \mathbf{h}_{N,p} \otimes \mathbf{h}_{N-1,p} \otimes \cdots \otimes \mathbf{h}_{1,p}, \qquad M = \prod_{n=1}^{N} L_n$$

- **Rank $P$** (the number of parallel Kronecker-product terms) trades performance against parameter count: larger $P$ raises the directivity factor but lowers the [[concepts/white-noise-gain|white noise gain]].
- **$N$ and the lengths $L_n$** control the granularity: with uniform decomposition, more groups (larger $N$, shorter filters) monotonically reduce parameters and inversion dimension at nearly unchanged performance.
- Under a distortionless constraint, the short filters are solved by **alternating iteration**: each stacked group $\bar{\mathbf{h}}_n$ (length $PL_n$) has an MVDR-like closed-form update, with [[concepts/diagonal-loading|diagonal loading]] ($\bar{\boldsymbol{\Gamma}}_n + \epsilon \mathbf{I}_{PL_n}$) embedded in every subproblem; convergence in ~18 iterations.

## Complexity

For an $M = 64$ array with $K = 256$ (3-way uniform decomposition, $L_n = 4$), rank $P = 2$ stores 3096 vs. 8256 complex parameters (−62.5%) and inverts at most $8 \times 8$ vs. $64 \times 64$ matrices (−87.5% in dimension), while matching the conventional robust superdirective beamformer's SNR/SIR/STOI (Zhu et al. 2025).

## Related Domains

The same Kronecker decomposition idea appears in multichannel active noise control for reducing the parameter space of large controller matrices (e.g., two-layer Kronecker product decomposition-based robust recursive adaptive filtering), and in adaptive filtering (nearest Kronecker product decomposition for subband adaptive filters).

## Related Concepts

- [[concepts/kmvdr-beamformer|KMVDR Beamformer]]
- [[concepts/superdirective-beamforming|Superdirective Beamforming]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/diagonal-loading|Diagonal Loading]]
- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/fixed-beamformer|Fixed Beamformer]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]

## Related Sources

- [[sources/cohen-2019-differential-kronecker-beamforming|Cohen, Benesty & Chen 2019: Differential Kronecker Product Beamforming]] — the original formulation: two-virtual-array decomposition, KP cardioid/dipole/hypercardioid/supercardioid
- [[sources/wang-2021-kronecker-adaptive-beamforming|Wang et al. 2021: Kronecker Product Adaptive Beamforming for Microphone Arrays]]
- [[sources/zhu-2025-kronecker-superdirective-beamforming|Zhu et al. 2025: Low-Rank Robust Superdirective Beamforming Using Multidimensional Kronecker Products]]
