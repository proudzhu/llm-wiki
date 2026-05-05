---
type: concept
created: 2026-05-05
updated: 2026-05-05
sources:
  - wiki/sources/liebich-2018-doa-dependency-anc-headphones.md
tags:
  - acoustics
  - hrtf
  - headphones
  - direction-of-arrival
---

# Device-Specific HRTF (DHRTF)

**Device-Specific Head-Related Transfer Functions (DHRTF)** are HRTF measurements that include the acoustic influence of a hearing device (e.g., in-ear headphones) mounted on the head. Unlike standard HRTFs that describe sound propagation to the bare eardrum, DHRTFs capture the transfer functions between the device's own microphones, incorporating the device's acoustic effects.

## Definition

DHRTFs measure the acoustic transfer paths between the microphones embedded in a hearing device (e.g., the outer and inner microphones of an ANC headphone) as a function of sound direction. The key transfer function is the **primary path** $P(z)$, which describes the transmission from the outer (ambient-facing) microphone to the inner (eardrum-facing) microphone.

## Measurement

Liebich et al. (2018) measured DHRTFs using:
- **Head Acoustics HMS II.3** dummyhead with ear simulator
- **Bose QC20** in-ear headphones (without original electronics)
- **4608 directions** on a half-circle loudspeaker array with rotating platform
- **72 directions** on the horizontal plane with a single loudspeaker (extended low-frequency coverage)
- Multiple exponential sweep method at 48 kHz sampling rate

## DOA Dependency

The primary path $P(z)$ measured via DHRTF shows clear DOA dependency:

| Frequency Range | DOA Dependency |
|-----------------|---------------|
| < 200 Hz | Approximately independent |
| 200 Hz – 1 kHz | Moderate (1–2 dB magnitude, 10–20° phase for 50% quantile) |
| > 1 kHz | Severe (resonance effects, >5 dB magnitude, >30° phase) |

The DOA dependency is analogous to how human hearing perceives sound differently from different directions, but now measured through the device's microphones.

## Significance for ANC

Since [[feedforward-anc|Feedforward ANC]] relies on the primary path $P(z)$ to compute the optimal filter, DHRTF variations directly impact ANC performance. [[feedback-anc|Feedback ANC]] depends only on the secondary path $G(z)$ (between loudspeaker and inner microphone), which is DOA-independent due to the fixed positions of these components.

## Related Concepts

- [[primary-path-variability|Primary Path Variability]]
- [[feedforward-anc|Feedforward ANC]]
- [[feedback-anc|Feedback ANC]]
- [[anc-attenuation-bounds|ANC Attenuation Bounds]]
- [[direction-of-arrival-estimation|Direction-of-Arrival Estimation]]

## Related Sources

- [[../sources/liebich-2018-doa-dependency-anc-headphones|Liebich 2018: DOA Dependency of ANC Headphones]]
