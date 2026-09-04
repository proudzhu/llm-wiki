---
type: concept
created: 2026-05-13
updated: 2026-09-04
sources:
  - raw/papers/wechsler-2024-neural-directional-filtering/full-text.md
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

## Related Concepts

- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/neural-directional-filtering|Neural Directional Filtering]]
- [[concepts/beamforming|Beamforming]]

## Related Sources

- [[sources/wechsler-2024-neural-directional-filtering|Wechsler et al. 2024: Neural Directional Filtering]] — LS fixed beamformer baseline results
- [[sources/huang-2026-ndf-joint-neural-directional-filtering|Huang et al. 2026: NDF+]]
