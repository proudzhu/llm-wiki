---
type: concept
created: 2026-05-13
updated: 2026-05-13
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

## Related Concepts

- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/neural-directional-filtering|Neural Directional Filtering]]
- [[concepts/beamforming|Beamforming]]

## Related Sources

- [[sources/huang-2026-ndf-joint-neural-directional-filtering|Huang et al. 2026: NDF+]]
