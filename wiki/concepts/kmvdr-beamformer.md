---
type: concept
created: 2026-09-17
updated: 2026-09-19
sources:
  - raw/papers/wang-2021-kronecker-adaptive-beamforming/full-text.txt
  - raw/papers/pan-2020-microphone-array-beamforming/full-text.txt
tags:
  - beamforming
  - microphone-arrays
  - kronecker-product
  - mvdr
  - adaptive-beamforming
---

# KMVDR Beamformer

**Category**: Structured / Low-Rank Adaptive Beamforming

The **Kronecker MVDR (KMVDR) beamformer** (Wang et al. 2021) is the [[concepts/mvdr-beamformer|MVDR beamformer]] designed within the sum-of-Kronecker-products representation of [[concepts/kronecker-product-beamforming|Kronecker product beamforming]]. It was the first Kronecker adaptive beamformer applicable to **arbitrary array geometries** — earlier Kronecker beamformers required the physical array to decompose into subarrays (linear, rectangular, cubic).

## Formulation

The length-$M$ filter ($M = M_1 M_2$) is written as a rank-$P$ sum of Kronecker products of short subfilters:

$$\mathbf{h} = \sum_{p=1}^{P} \mathbf{h}_{1,p} \otimes \mathbf{h}_{2,p}, \qquad P \leq \min(M_1, M_2)$$

so that the optimization variable is the collection of short subfilters rather than the full filter. With one subfilter family fixed, the beamformer output, its variance, and the distortionless constraint all reduce to an MVDR problem in the other stacked subfilter:

$$\mathbf{h}_2 = \frac{\boldsymbol{\Lambda}_{\mathbf{y}_1}^{-1} \mathbf{d}_1(\vartheta_s)}{\mathbf{d}_1^H(\vartheta_s) \boldsymbol{\Lambda}_{\mathbf{y}_1}^{-1} \mathbf{d}_1(\vartheta_s)}, \qquad \mathbf{h}_1 = \frac{\boldsymbol{\Lambda}_{\mathbf{y}_2}^{-1} \mathbf{d}_2(\vartheta_s)}{\mathbf{d}_2^H(\vartheta_s) \boldsymbol{\Lambda}_{\mathbf{y}_2}^{-1} \mathbf{d}_2(\vartheta_s)}$$

where $\boldsymbol{\Lambda}_{\mathbf{y}_1}, \boldsymbol{\Lambda}_{\mathbf{y}_2}$ are block covariances of sizes $PM_2 \times PM_2$ and $PM_1 \times PM_1$ built from the current estimate of the fixed subfilters, and $\mathbf{d}_1, \mathbf{d}_2$ the correspondingly projected steering vectors. The subfilters are updated **alternately** until the beamformer stops changing, and the final KMVDR filter is the sum $\mathbf{h}_{\mathrm{KMVDR}} = \sum_p \mathbf{h}_{1,p} \otimes \mathbf{h}_{2,p}$.

## Properties

- **Geometry-independent**: the sum-of-Kronecker-products representation is a property of the filter, not of the array — any 3-D geometry works as long as sensor positions are known.
- **Reduced inversions**: each iteration inverts $PM_1 \times PM_1$ and $PM_2 \times PM_2$ matrices instead of one $M \times M$ matrix.
- **Implicit regularization**: on a 16-microphone array with limited snapshots and dynamic interferers, KMVDR outperforms the conventional MVDR in output SINR, with the best performance at rank $P = 1$ — the constrained filter space regularizes the covariance-based estimate.
- **Lineage**: the alternating-iteration scheme generalizes to $N$-way decompositions ([[sources/zhu-2025-kronecker-superdirective-beamforming|Zhu et al. 2025]] LR-RSD), where each stacked group receives an MVDR-like closed-form update with diagonal loading embedded in every subproblem.

## Related Concepts

- [[concepts/kronecker-product-beamforming|Kronecker Product Beamforming]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/adl-mvdr|ADL-MVDR]] — another structured MVDR variant (GRU-based, rather than Kronecker-based)
- [[concepts/beamforming|Beamforming]]

## Related Sources

- [[sources/wang-2021-kronecker-adaptive-beamforming|Wang et al. 2021: Kronecker Product Adaptive Beamforming for Microphone Arrays]]
- [[sources/zhu-2025-kronecker-superdirective-beamforming|Zhu et al. 2025: Low-Rank Robust Superdirective Beamforming Using Multidimensional Kronecker Products]]
- [[sources/pan-2020-microphone-array-beamforming|Pan, Huang & Chen 2020: Microphone Array Beamforming Methods for Speech Communication and Interaction]] — review of the fixed Kronecker-product family (two-stage cascade lineage, adaptive covariance-inversion splitting) that KMVDR later generalized to adaptive beamforming on arbitrary geometries
