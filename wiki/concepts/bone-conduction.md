---
type: concept
created: 2026-04-12
updated: 2026-04-17
sources:
  - wiki/sources/kuang-2024-lightweight-speech-enhancement-bone-air.md
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
Bone conduction sensors (accelerometers) in headphones can reliably detect when the wearer is speaking (Own Voice Activity Detection) because they are immune to external airborne noise. This is used to automatically switch to [[transparency-mode|Transparency Mode]] (Masilamani 2024).

## Related Concepts

- [[ear-canal-occlusion-effect|Ear Canal Occlusion Effect]]
- [[voice-activity-detection|Voice Activity Detection]]
- [[bcs-guided-speech-enhancement|BCS-Guided Speech Enhancement]]
- [[transparency-mode|Transparency Mode]]
- [[../sources/fukumoto-2025-whisphone-paper-reading-note|Whisphone]]

## Related Sources

- [[../sources/zhang-2022-bone-conducted-speech-dissertation|Zhang 2022: Bone-Conducted Speech Dissertation]]

- [[../sources/fukumoto-2025-whisphone-paper-reading-note|Fukumoto 2025: Whisphone Paper Reading Note]]
- [[../sources/masilamani-2024-headphone-conversation-detect-paper-reading-note|Masilamani 2024: Headphone Conversation Detect]]
