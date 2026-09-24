---
type: concept
created: 2026-05-13
updated: 2026-09-24
sources:
  - raw/papers/pan-2020-microphone-array-beamforming/full-text.txt
  - raw/papers/wechsler-2024-neural-directional-filtering/full-text.md
  - raw/papers/huang-2025-steerable-neural-directional-filtering/full-text.md
  - raw/papers/zhu-2025-kronecker-superdirective-beamforming/full-text.txt
  - raw/papers/cohen-2019-differential-kronecker-beamforming/full-text.txt
  - raw/papers/desena-2012-higher-order-differential/full-text.md
tags:
  - fixed-beamformer
  - spatial-audio
  - microphone-array
---

# Fixed Beamformer

A fixed beamformer (FBF) applies predetermined, time-invariant weights to microphone array signals to achieve spatial selectivity. Unlike adaptive beamformers, FBFs do not adjust their weights based on the acoustic scene.

## Types

| Type | Description | Characteristics |
|------|-------------|-----------------|
| Delay-and-Sum | Aligns signals by time delay, then sums | Simple, robust (max WNG), limited directivity |
| Differential Microphone Array (DMA) | Uses spatial differences between microphones | Frequency-invariant patterns, low-frequency noise amplification |
| Superdirective | Maximizes directivity factor | High directivity, sensitive to noise |
| Orthogonal Series Expansion | Approximates a target beampattern via an orthogonal series (Chebyshev, Legendre, Jacobi, spherical harmonics) | Flexible pattern design, relaxed sensor placement; robustness/pattern-accuracy trade-off via a loading parameter |

## Limitations

Conventional FBFs are fundamentally limited by:
- Compact array with small aperture
- Limited number of microphones
- Low white noise gain (WNG) at low frequencies for higher-order patterns
- **Directivity upper bound**: for fixed beamformers the directivity is capped at the square of the sensor count ($M^2$), so small arrays cannot reach the directivity many far-field applications need — breaking this limit is listed as an open problem by [[sources/pan-2020-microphone-array-beamforming|Pan, Huang & Chen 2020]]

Empirically, a least-squares FBF designed for a minimum WNG of −15 dB on a 4-microphone, 3 cm array approximates a 1st-order cardioid well but cannot approximate a 3rd-order DMA pattern (negative SDRs), and its performance is dominated by white-noise amplification ([[sources/wechsler-2024-neural-directional-filtering|Wechsler et al. 2024]]).

On the design side, [[sources/desena-2012-higher-order-differential|De Sena, Hacihabiboglu & Cvetkovic 2012]] give fixed differential designs a two-parameter user interface — the $(\alpha, \lambda)$ [[concepts/sector-directivity-design|sector-based directivity design]] — and a [[concepts/complex-root-differential-array|complex-root array structure]] showing that the pattern class a fixed differential structure can realize is itself a design decision, not just the weights.

## Low-Rank Superdirective FBFs

For large arrays, the parameter count of a fixed beamformer scales with $M$ per frequency bin. [[concepts/superdirective-beamforming|Superdirective]] designs can be made **low-rank** via [[concepts/kronecker-product-beamforming|Kronecker product decomposition]] (Zhu et al. 2025): the length-$M$ filter becomes a rank-$P$ sum of Kronecker products of short filters, cutting stored parameters by up to 62.5% and inversion dimension by 87.5% ($M = 64$, $P = 2$) while matching the conventional robust superdirective beamformer — attractive for embedded systems where FBF coefficients are precomputed and stored. The lineage starts with differential Kronecker product beamforming ([[sources/cohen-2019-differential-kronecker-beamforming|Cohen, Benesty & Chen 2019]]), which decomposes differential (cardioid/dipole/hypercardioid/supercardioid) fixed designs into two virtual-array subfilters for more flexible DF–WNG tradeoffs.

## Related Concepts

- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/neural-directional-filtering|Neural Directional Filtering]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/superdirective-beamforming|Superdirective Beamforming]]
- [[concepts/kronecker-product-beamforming|Kronecker Product Beamforming]]
- [[concepts/orthogonal-series-expansion-beamforming|Orthogonal Series Expansion Beamforming]]
- [[concepts/frequency-invariant-beamforming|Frequency-Invariant Beamforming]]

## Related Sources

- [[sources/pan-2020-microphone-array-beamforming|Pan, Huang & Chen 2020: Microphone Array Beamforming Methods for Speech Communication and Interaction]] — review of the fixed-beamforming families and their DF–WNG–frequency-invariance trade-offs; $M^2$ directivity upper bound

- [[sources/cohen-2019-differential-kronecker-beamforming|Cohen, Benesty & Chen 2019: Differential Kronecker Product Beamforming]] — Kronecker-decomposed differential fixed beamformers
- [[sources/wechsler-2024-neural-directional-filtering|Wechsler et al. 2024: Neural Directional Filtering]] — LS fixed beamformer baseline results
- [[sources/huang-2026-ndf-joint-neural-directional-filtering|Huang et al. 2026: NDF+]]
- [[sources/huang-2025-steerable-neural-directional-filtering|Huang, Halimeh, Chetupalli, Thiergart & Habets 2025: Steerable Neural Directional Filtering]]
- [[sources/zhu-2025-kronecker-superdirective-beamforming|Zhu et al. 2025: Low-Rank Robust Superdirective Beamforming Using Multidimensional Kronecker Products]] — low-rank superdirective FBF via Kronecker decomposition
- [[sources/desena-2012-higher-order-differential|De Sena, Hacihabiboglu & Cvetkovic 2012: On the Design and Implementation of Higher Order Differential Microphones]] — (α, λ) design framework and complex-root differential structure for fixed higher-order patterns

