---
type: concept
created: 2026-04-12
updated: 2026-05-16
sources:
  - wiki/sources/kuang-2024-lightweight-speech-enhancement-bone-air.md
  - wiki/sources/liu-2025-robust-fusion-bc-ac-attention.md
  - wiki/sources/wang-2022-fusing-bc-ac-complex-domain-se.md
tags:
- acoustics
- audio-processing
- biology
---

# Bone Conduction

**Bone Conduction** is the conduction of sound to the inner ear primarily through the bones of the skull, bypassing the eardrum.

## Overview

Unlike standard air conduction, where sound waves travel through the ear canal to vibrate the eardrum, bone conduction allows sound to be perceived by vibrating the skull. This is used both for **hearing** (bone conduction headphones) and **recording** (bone conduction microphones).

## Transmission Paths

1. **Inner Ear Path**: Direct vibration of the cochlea through the skull.
2. **Ear Canal Radiation**: Vibrations from the skull and soft tissues radiate sound into the ear canal, which then travels to the eardrum as standard air conduction. This path is highly significant for hearing one's own voice.

## Applications in ANC and Wearables

### 1. Ear Canal Occlusion Effect
When the ear canal is blocked (occluded) by a finger or an earplug, bone-conducted sound at low frequencies (< 1 kHz) is amplified by **5–20 dB**. This is because the sound radiated into the ear canal cannot escape and is "trapped" (Fukumoto 2025).

### 2. Private Voice Input (Whisphone)
The **Whisphone** project leverages the occlusion effect + bone conduction to capture whispering sounds from within the ear canal using an internal MEMS microphone. This allows for private AI interaction in noisy environments (Fukumoto 2025).

### 3. Multi-Modal Speech Enhancement (VibOmni)
The **VibOmni** system (He et al. 2025) leverages IMU-captured bone-conducted vibrations as a noise-robust auxiliary modality for earable speech enhancement. It uses a two-branch encoder-decoder DPRNN to fuse audio and vibration features, with a novel Bone Conduction Function (BCF) data augmentation technique that reduces paired data requirements by >72×. The system achieves up to 21% PESQ improvement and ~40% WER reduction on real-world data.

### 4. Voice Activity Detection (OVAD)
Bone conduction sensors (accelerometers) in headphones can reliably detect when the wearer is speaking (Own Voice Activity Detection) because they are immune to external airborne noise. This is used to automatically switch to [[concepts/transparency-mode|Transparency Mode]] (Masilamani 2024).

### 5. Sensor-Failure Robustness
A practical concern with wearable BC sensors is intermittent invalidity (loose contact, jaw movement, body motion). Liu, Chen & Yin (2025) introduce a **Special Training** strategy — randomly disabling either the BC or AC channel during training (p = 0.2) — combined with a dual-channel mask architecture, achieving graceful degradation when one sensor fails. See [[concepts/sensor-failure-robust-fusion|Sensor-Failure Robust Multi-Modal Fusion]].

### 6. Ear Canal Deformation and In-Ear Speech Quality
In-ear microphones capture bone-conducted speech through the sealed ear canal. However, [[concepts/ear-canal-deformation|Ear Canal Deformation (ECD)]] induced by articulatory gestures alters air pressure inside the sealed cavity, degrading in-ear speech quality via a stuck-at-low microphone fault. Han et al. (2026) address this with [[concepts/quality-aware-speech-enhancement|Quality-Aware Speech Enhancement (QuaSE)]], which dynamically weights in-ear features based on self-assessed quality before fusion with airborne speech.

## Related Concepts

- [[concepts/ear-canal-occlusion-effect|Ear Canal Occlusion Effect]]
- [[concepts/ear-canal-deformation|Ear Canal Deformation]]
- [[concepts/quality-aware-speech-enhancement|Quality-Aware Speech Enhancement]]
- [[concepts/voice-activity-detection|Voice Activity Detection]]
- [[concepts/bcs-guided-speech-enhancement|BCS-Guided Speech Enhancement]]
- [[concepts/transparency-mode|Transparency Mode]]
- [[concepts/complex-spectral-mapping|Complex Spectral Mapping]]
- [[sources/fukumoto-2025-whisphone-paper-reading-note|Whisphone]]

## Related Sources

- [[sources/zhang-2022-bone-conducted-speech-dissertation|Zhang 2022: Bone-Conducted Speech Dissertation]]
- [[sources/wang-2022-fusing-bc-ac-complex-domain-se|Wang, Zhang & Wang 2022: Fusing BC and AC for Complex-Domain SE]]
- [[sources/liu-2025-robust-fusion-bc-ac-attention|Liu, Chen & Yin 2025: Robust BC/AC Fusion with ATFA]]
- [[sources/fukumoto-2025-whisphone-paper-reading-note|Fukumoto 2025: Whisphone Paper Reading Note]]
- [[sources/masilamani-2024-headphone-conversation-detect-paper-reading-note|Masilamani 2024: Headphone Conversation Detect]]
- [[sources/han-2026-quality-aware-earable-se|Han et al. 2026: QuaSE — Quality-Aware Earable Dual-Microphone SE]]
