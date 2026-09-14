---
type: concept
created: 2026-05-13
updated: 2026-09-14
sources:
  - raw/papers/wechsler-2024-neural-directional-filtering/full-text.md
  - raw/papers/huang-2025-steerable-neural-directional-filtering/full-text.md
  - raw/papers/zhu-2025-kronecker-superdirective-beamforming/full-text.txt
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
| Delay-and-Sum | Aligns signals by time delay, then sums | Simple, robust, limited directivity |
| Differential Microphone Array (DMA) | Uses spatial differences between microphones | Frequency-invariant patterns, low-frequency noise amplification |
| Superdirective | Maximizes directivity factor | High directivity, sensitive to noise |

## Limitations

Conventional FBFs are fundamentally limited by:
- Compact array with small aperture
- Limited number of microphones
- Low white noise gain (WNG) at low frequencies for higher-order patterns

Empirically, a least-squares FBF designed for a minimum WNG of −15 dB on a 4-microphone, 3 cm array approximates a 1st-order cardioid well but cannot approximate a 3rd-order DMA pattern (negative SDRs), and its performance is dominated by white-noise amplification ([[sources/wechsler-2024-neural-directional-filtering|Wechsler et al. 2024]]).

## Low-Rank Superdirective FBFs

For large arrays, the parameter count of a fixed beamformer scales with $M$ per frequency bin. [[concepts/superdirective-beamforming|Superdirective]] designs can be made **low-rank** via [[concepts/kronecker-product-beamforming|Kronecker product decomposition]] (Zhu et al. 2025): the length-$M$ filter becomes a rank-$P$ sum of Kronecker products of short filters, cutting stored parameters by up to 62.5% and inversion dimension by 87.5% ($M = 64$, $P = 2$) while matching the conventional robust superdirective beamformer — attractive for embedded systems where FBF coefficients are precomputed and stored.

## Related Concepts

- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/neural-directional-filtering|Neural Directional Filtering]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/superdirective-beamforming|Superdirective Beamforming]]
- [[concepts/kronecker-product-beamforming|Kronecker Product Beamforming]]

## Related Sources

- [[sources/wechsler-2024-neural-directional-filtering|Wechsler et al. 2024: Neural Directional Filtering]] — LS fixed beamformer baseline results
- [[sources/huang-2026-ndf-joint-neural-directional-filtering|Huang et al. 2026: NDF+]]
- [[sources/huang-2025-steerable-neural-directional-filtering|Huang, Halimeh, Chetupalli, Thiergart & Habets 2025: Steerable Neural Directional Filtering]]
- [[sources/zhu-2025-kronecker-superdirective-beamforming|Zhu et al. 2025: Low-Rank Robust Superdirective Beamforming Using Multidimensional Kronecker Products]] — low-rank superdirective FBF via Kronecker decomposition

