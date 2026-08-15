---
type: concept
created: 2026-05-13
updated: 2026-08-15
sources:
  - raw/papers/tashev-2008-sound-capture-spatial-filter/full-text.md
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

## Back-to-Back Unidirectional Variant

A distinct but related geometry is the [[concepts/back-to-back-microphone-array|back-to-back microphone array]] introduced by Tashev et al. (2008). The two variants differ in capsule type and primary cue:

| Property | Differential MA | Back-to-Back Array |
|---|---|---|
| Capsule type | Omnidirectional | Unidirectional (e.g. subcardioid) |
| Primary spatial cue | Pressure difference (delay) between omni mics | Directional response level difference |
| Beamformer target | Frequency-invariant directivity | Maximum front-back energy ratio |
| Sub-baseline reliability | Degrades at very small spacing (noise amplification) | Robust at very small spacing (e.g. 9.6 mm at 16 kHz) |

For very small baselines where delay-based features become unreliable (Tashev et al.'s optimizer effectively disabled both delay features at 9.6 mm / 16 kHz, where the inter-mic delay is only ~1/4 of the sampling period), the back-to-back geometry's reliance on the intrinsic directional response of each capsule becomes advantageous.

## Related Concepts

- [[concepts/fixed-beamformer|Fixed Beamformer]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/virtual-directional-microphone|Virtual Directional Microphone]]
- [[concepts/back-to-back-microphone-array|Back-to-Back Microphone Array]] — a related small-baseline geometry that uses unidirectional capsules (rather than omni) and front-back level differences

## Related Sources

- [[sources/huang-2026-ndf-joint-neural-directional-filtering|Huang et al. 2026: NDF+]]
- [[sources/tashev-2008-sound-capture-spatial-filter|Tashev et al. 2008: Sound Capture System and Spatial Filter for Small Devices]] — back-to-back unidirectional variant (9.6 mm baseline)
