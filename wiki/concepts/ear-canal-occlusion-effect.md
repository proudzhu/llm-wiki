---
type: concept
created: 2026-04-12
updated: 2026-09-06
sources:
  - wiki/sources/han-2026-quality-aware-earable-se.md
  - raw/papers/hu-2026-abse-net/full-text.md
tags:
- acoustics
- biology
- headphone
---

# Ear Canal Occlusion Effect

**Ear Canal Occlusion Effect** refers to the amplification of bone-conducted sound (specifically the low-frequency components) when the ear canal is blocked or occluded.

## Overview

When a person speaks, the vibrations from their vocal cords and skull radiate into the ear canal walls. In an open ear, these sound waves escape through the ear canal opening. However, if the ear canal is blocked (e.g., by a finger, an earplug, or an in-ear ANC headphone), the sound energy is trapped, leading to a significant increase in sound pressure at the eardrum.

## Characteristics

- **Frequency Range**: The effect is most pronounced at low frequencies, typically below **1 kHz**.
- **Magnitude**: Sound pressure can increase by **5–20 dB**.
- **Perception**: Users often describe the effect as a "booming" or "hollow" sound to their own voice when wearing earplugs or tightly sealed headphones.

## Applications and Solutions

### 1. Whisphone: Leveraging the Effect
The **Whisphone** project (Fukumoto 2025) uses the occlusion effect as a "passive amplifier" to pick up whispered speech from inside the ear canal. This helps overcome the low signal-to-noise ratio of whispers in noisy environments.

### 2. ANC Headphones: Mitigating the Effect
In high-end ANC headphones, the occlusion effect can be unpleasant for users during calls. Solutions include:
- **Vented Design**: Including a small acoustic vent to allow low-frequency pressure to escape (at the cost of some passive isolation).
- **Active Mitigation**: Using the feedback microphone and speaker to actively cancel the "booming" sound of the user's own voice.

### 3. Open-Fit Hearing Aids: Trading Occlusion for Leakage
Open-fit (vented) hearing aids bypass the occlusion effect by leaving the ear canal open, at the cost of **acoustic leakage**: external noise enters the canal through the vent and corrupts the enhanced signal played by the hearing-aid loudspeaker. [[sources/hu-2026-abse-net|Hu et al. 2026]] show a binaural MVDR beamformer loses most of its gain under leakage (SI-SDR 5.216 → 0.878 dB) and address it with active binaural speech enhancement ([[concepts/abse-net|ABSE-NET]]).

## Relationship to Ear Canal Deformation (ECD)

While the occlusion effect is a *static* phenomenon that *amplifies* bone-conducted low-frequency sound when the canal is blocked, **[[concepts/ear-canal-deformation|Ear Canal Deformation (ECD)]]** is a *dynamic* phenomenon caused by articulatory gestures during speech. ECD alters air pressure inside the sealed ear canal, which *degrades* in-ear microphone recordings via a stuck-at-low fault. Both phenomena co-occur in sealed earphones, but ECD's negative impact on in-ear speech quality is the focus of [[concepts/quality-aware-speech-enhancement|Quality-Aware Speech Enhancement]] (QuaSE, Han et al. 2026).

## Related Concepts

- [[concepts/bone-conduction|Bone Conduction]]
- [[concepts/ear-canal-deformation|Ear Canal Deformation]]
- [[concepts/quality-aware-speech-enhancement|Quality-Aware Speech Enhancement]]
- [[sources/fukumoto-2025-whisphone-paper-reading-note|Whisphone]]
- [[concepts/transparency-mode|Transparency Mode]]
- [[concepts/active-binaural-speech-enhancement|Active Binaural Speech Enhancement]]

## Related Sources

- [[sources/fukumoto-2025-whisphone-paper-reading-note|Fukumoto 2025: Whisphone Paper Reading Note]]
- [[sources/han-2026-quality-aware-earable-se|Han et al. 2026: QuaSE — Quality-Aware Earable Dual-Microphone SE]]
- [[sources/hu-2026-abse-net|Hu et al. 2026: ABSE-NET — Active Binaural Speech Enhancement for Open-Fit Hearing Aids]]
