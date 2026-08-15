---
type: concept
created: 2026-08-15
updated: 2026-08-15
sources:
  - raw/papers/tashev-2008-sound-capture-spatial-filter/full-text.md
tags:
  - microphone-array
  - beamforming
  - spatial-audio
  - small-device
  - directional-microphone
---

# Back-to-Back Microphone Array

A **back-to-back microphone array** is a small-baseline two-microphone geometry in which two *unidirectional* (e.g. subcardioid) capsules are placed close together and oriented in opposite directions, so that the front capsule faces the desired source and the rear capsule faces away. The configuration was introduced by Tashev, Mihov, Gleghorn & Acero (2008) for sound capture on cell phones and other small handheld devices.

## Motivation

Small handheld devices (cell phones, PDAs, ultra-mobile PCs) need to capture speech from ~1 m (arm's length) but cannot accommodate large microphone baselines. Constrained by the small device size and the need to keep microphones away from the loudspeaker, the inter-capsule distance is typically 30–50 mm; Tashev et al. used **9.6 mm**. At 16 kHz, 9.6 mm corresponds to roughly a quarter of the sampling period, which makes classical time-delay-based [[concepts/beamforming\|beamforming]] and [[concepts/differential-microphone-array\|differential microphone array]] techniques unreliable. The back-to-back geometry sidesteps this by relying on the *intrinsic directional response* of each capsule as the primary spatial cue, rather than on inter-microphone phase differences.

## Distinction from Differential Microphone Arrays

| Property | Differential Microphone Array (DMA) | Back-to-Back Array |
|---|---|---|
| Capsule type | Omnidirectional | Unidirectional (subcardioid, etc.) |
| Primary spatial cue | Pressure difference between closely-spaced omni mics | Different directional responses of the two capsules |
| Beamformer target | Frequency-invariant directivity pattern | Maximum front-back energy ratio |
| Sub-baseline reliability | Degrades at very small spacing due to noise amplification | Robust to very small spacing — relies on level, not delay |

## Beamformer Design

Because each capsule has its own measured directivity pattern $U_F(f,\theta)$, $U_R(f,\theta)$, the front and rear beam outputs are formed as linear combinations of the two microphone signals with weights optimized to **maximize the front-back energy ratio** (rather than the conventional maximum-SNR / minimum-variance criteria):

$$
Q_{F\text{const}} = \max_{\mathbf{W}_{FF},\mathbf{W}_{FR}} \frac{\int_{-\Delta\theta}^{+\Delta\theta} (\mathbf{W}_{FF}\mathbf{X}_F(\theta) + \mathbf{W}_{FR}\mathbf{X}_R(\theta))\,d\theta}{\int_{-\pi+\Delta\theta}^{\pi-\Delta\theta} (\mathbf{W}_{FF}\mathbf{X}_F(\theta) + \mathbf{W}_{FR}\mathbf{X}_R(\theta))\,d\theta}
$$

with the analogous $Q_{R\text{const}}$ for the rear beam. Unity-gain and zero-phase-shift constraints in the desired direction are enforced via punishing functions. With $\Delta\theta = 30^\circ$ the front beam covers $[-30^\circ, +30^\circ]$ and the rear beam covers $[150^\circ, -150^\circ]$.

## Why It Works at Very Small Spacing

The 9.6 mm baseline makes inter-microphone delay (per frame or per bin) a weak feature — the optimizer in Tashev et al. (2008) effectively disabled both delay-based features ($G_\text{Del/fr} \approx 0.89$, $G_\text{Del/bin} \approx 0.99$, where 1 means disabled). The system relies on **level-difference features** instead, which are produced by the directional response of the capsules (the level difference between the front and rear beams encodes whether the source is in front of or behind the device). See [[concepts/probability-based-spatial-filter\|Probability-Based Spatial Filter]] for the post-filter that consumes these features.

## Related Concepts

- [[concepts/probability-based-spatial-filter\|Probability-Based Spatial Filter]]
- [[concepts/beamforming\|Beamforming]]
- [[concepts/differential-microphone-array\|Differential Microphone Array]]
- [[concepts/directivity-pattern\|Directivity Pattern]]
- [[concepts/fixed-beamformer\|Fixed Beamformer]]

## Related Sources

- [[sources/tashev-2008-sound-capture-spatial-filter|Tashev, Mihov, Gleghorn & Acero 2008: Sound Capture System and Spatial Filter for Small Devices]]
