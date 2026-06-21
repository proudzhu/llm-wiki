---
type: concept
created: 2026-06-21
updated: 2026-06-21
sources:
  - wiki/sources/han-2026-quality-aware-earable-se.md
tags:
  - acoustics
  - biology
  - earable
  - speech-enhancement
  - in-ear-speech
---

# Ear Canal Deformation

**Ear Canal Deformation (ECD)** refers to the geometrical change in shape of the ear canal (external auditory canal) caused by articulatory gestures, head movements, or earphone insertion, which alters air pressure inside the sealed ear canal and degrades in-ear microphone recordings.

## Overview

The ear canal is a tubular structure extending from the pinna to the tympanic membrane (eardrum). Soft tissues surrounding the ear canal, situated between the mandible and the mastoid, are highly deformable. During speech production, articulatory gestures (mandible, lips, tongue, jaw, and velum movement) activate facial muscles that stretch or compress these soft tissues, pulling them to move and changing the shape of the ear canal.

The ear canal model can be discretized into 11 cross sections, whose morphological parameters (diameter, circumference, area, curvature, angulation) all contribute to ECD. Beyond articulatory gestures, head movements and earphone insertion depth also cause slight ECD.

## Air Pressure Variations in the Sealed Ear Canal

When an earphone fully seals the ear canal, a closed cavity forms between the eartip and the eardrum. In this sealed space, ECD alters the available air volume. Per fluid mechanics principles:

- **Volume decrease** (canal walls press inward) → air molecules forced closer → **pressure increase**
- **Volume increase** → **pressure drop**

These ECD-induced pressure fluctuations counteract or "clamp" the intended oscillatory forces of incoming sound waves on the microphone diaphragm, inhibiting its movement.

## Impact on In-Ear Speech Quality

The microphone transducer output follows:

$$u(t) = S_e \cdot (d(t) - d_0(t))$$

where $S_e$ is electronic sensitivity, $d(t)$ is diaphragm displacement, and $d_0(t)$ is initial displacement. ECD-induced pressure imbalance restricts $d(t)$, causing a **stuck-at-low fault** where the output remains permanently biased at a low level and fails to respond to acoustic pressure variations.

**Consequences for dual-microphone speech enhancement**:
- In-ear speech loses temporal and spectral structure (spectrogram appears "masked")
- Cross-channel correlation between in-ear and airborne speech drops by ~30×
- Fusion gains degrade significantly (e.g., PESQ gain drops from 0.960 to 0.623)
- This is a form of **modality imbalance** that existing dual-microphone SE systems (which assume high-quality in-ear speech) do not handle

## Relationship to Occlusion Effect

ECD is distinct from but related to the [[concepts/ear-canal-occlusion-effect|Ear Canal Occlusion Effect]]:
- The **occlusion effect** amplifies bone-conducted low-frequency sound (< 1 kHz, 5–20 dB gain) when the canal is blocked — it is a *static* phenomenon that *enhances* the in-ear signal
- **ECD** is a *dynamic* phenomenon caused by articulatory gestures during speech that *degrades* the in-ear signal via pressure imbalance

Both phenomena co-occur when earphones seal the ear canal, but ECD's negative impact on signal integrity is the focus of quality-aware speech enhancement research.

## Applications

- **Negative impact (speech enhancement)**: Degrades in-ear auxiliary modality quality, addressed by [[concepts/quality-aware-speech-enhancement|Quality-Aware Speech Enhancement]] (QuaSE)
- **Positive sensing (activity recognition)**: ECD measurements via in-ear microphones enable recognition of tongue-jaw movements, articulatory gestures, facial expressions, and biometric authentication

## Related Concepts

- [[concepts/ear-canal-occlusion-effect|Ear Canal Occlusion Effect]]
- [[concepts/bone-conduction|Bone Conduction]]
- [[concepts/quality-aware-speech-enhancement|Quality-Aware Speech Enhancement]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Related Sources

- [[sources/han-2026-quality-aware-earable-se|Han et al. 2026: QuaSE — Quality-Aware Earable Dual-Microphone SE]]
