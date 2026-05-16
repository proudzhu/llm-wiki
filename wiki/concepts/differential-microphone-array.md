---
type: concept
created: 2026-05-13
updated: 2026-05-13
tags:
  - differential-microphone-array
  - beamforming
  - spatial-audio
---

# Differential Microphone Array

A differential microphone array (DMA) is a fixed beamformer that uses spatial differences between closely-spaced microphones to achieve directional sensitivity. DMAs can produce frequency-invariant directivity patterns.

## Types

| Type | Description |
|------|-------------|
| LDMA | Linear DMA - microphones arranged in a line |
| CDMA | Circular DMA - microphones arranged in a circle |

## Key Properties

- **Frequency invariance**: Directivity pattern remains constant across frequency
- **Order limitation**: Maximum order is limited by number of microphones
- **White noise gain**: Low WNG at low frequencies leads to noise amplification

## Limitations

- Restricted to low-order patterns with compact arrays
- Cannot achieve higher-order directivity with limited microphones
- Performance degrades due to noise amplification at low frequencies

## Related Concepts

- [[concepts/fixed-beamformer|Fixed Beamformer]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/virtual-directional-microphone|Virtual Directional Microphone]]

## Related Sources

- [[sources/huang-2026-ndf-joint-neural-directional-filtering|Huang et al. 2026: NDF+]]
