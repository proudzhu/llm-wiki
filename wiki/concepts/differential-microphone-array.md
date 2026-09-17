---
type: concept
created: 2026-05-13
updated: 2026-09-17
sources:
  - raw/papers/tashev-2008-sound-capture-spatial-filter/full-text.md
  - raw/papers/wechsler-2024-neural-directional-filtering/full-text.md
  - raw/papers/zhu-2025-kronecker-superdirective-beamforming/full-text.txt
  - raw/papers/cohen-2019-differential-kronecker-beamforming/full-text.txt
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

## Kronecker Product Differential Beamforming

[[sources/cohen-2019-differential-kronecker-beamforming|Cohen, Benesty & Chen 2019]] introduced **differential Kronecker product beamformers**: when the physical array decomposes into two virtual ULAs ($M = M_1 M_2$, steering vector $\mathbf{d} = \mathbf{d}_1 \otimes \mathbf{d}_2$), the differential filter follows the same decomposition $\mathbf{h} = \mathbf{h}_1 \otimes \mathbf{h}_2$. This adds a new design axis to classical differential beamforming: the KP cardioid/dipole/hypercardioid/supercardioid achieve higher DF and WNG than the traditional designs with $M_2$ microphones, and occupy a more favorable DF–WNG tradeoff than minimum-norm designs with the same total $M$ — see [[concepts/kronecker-product-beamforming|Kronecker Product Beamforming]].

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

- [[sources/cohen-2019-differential-kronecker-beamforming|Cohen, Benesty & Chen 2019: Differential Kronecker Product Beamforming]] — Kronecker-decomposed differential beamformers (KP cardioid/dipole/hypercardioid/supercardioid)
- [[sources/wechsler-2024-neural-directional-filtering|Wechsler et al. 2024: Neural Directional Filtering]] — neural directional filtering surpasses the order-per-microphone limit: a 3rd-order DMA pattern (6-mic CDMA classically) realized with 4 microphones
- [[sources/huang-2026-ndf-joint-neural-directional-filtering|Huang et al. 2026: NDF+]]
- [[sources/tashev-2008-sound-capture-spatial-filter|Tashev et al. 2008: Sound Capture System and Spatial Filter for Small Devices]] — back-to-back unidirectional variant (9.6 mm baseline)
