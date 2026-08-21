---
type: concept
created: 2026-08-22
updated: 2026-08-22
sources:
  - raw/papers/yang-2025-mc-differential-asr-smart-glasses/full-text.md
  - raw/papers/lin-2024-agadir-array-geometry-agnostic-speech-recognition/full-text.md
  - raw/papers/feng-2025-directional-source-separation-smart-glasses/full-text.md
tags:
  - speech-recognition
  - smart-glasses
  - wearable
  - asr
---

# Wearer Speech Recognition (WSR)

**Wearer Speech Recognition (WSR)** is the task of transcribing the speech of the **wearer** of a wearable device (smart glasses, earables, headsets) from multi-channel microphone signals captured by the device's on-body array. It contrasts with general far-field ASR and conversational ASR in that the target speaker is fixed by the device geometry: the wearer's mouth is at a known relative position to the array.

## Why WSR is Hard

Smart-glasses microphones operate in **open-field conditions**, unlike close-talk headset microphones. The wearer is not close-miked, and the array is small (5 mics on a typical pair of Ray-Ban Meta smart glasses). Bystander side-talk is the dominant failure mode: in real conversations, unrelated speech from a third party corrupts the wearer transcription and propagates errors into downstream tasks (natural language understanding, assistant responses). Compounding this:

- The array is small and on a curved frame — array geometry changes across prototypes (motivating [[concepts/nlcmv-beamforming|geometry-agnostic]] training, see [[sources/lin-2024-agadir-array-geometry-agnostic-speech-recognition|AGADIR]]).
- Privacy constraints discourage modeling speaker identity (the device should not store the wearer's voiceprint).
- Latency must be kept low for real-time interaction (~120 ms in Yang et al. 2025).

## Approaches Surveyed

| Approach | Reference | Key idea |
|----------|-----------|----------|
| Multi-direction NLCMV beamforming + RNN-T | [[sources/lin-2024-agadir-array-geometry-agnostic-speech-recognition\|Lin et al. 2024 (AGADIR)]] | $K+1$ fixed beamformers (one per steering direction); ASR picks up wearer + bystander via serialized output training |
| Directional source separation + ASR | [[sources/feng-2025-directional-source-separation-smart-glasses\|Feng et al. 2025]] | Neural source separation as frontend to ASR |
| [[concepts/differential-asr\|Differential ASR]] | [[sources/yang-2025-mc-differential-asr-smart-glasses\|Yang et al. 2025]] | Multiple complementary frontends (beamformer + close-mic + STD embedding) fused into a streaming RNN-T |
| Multi-microphone Whisper (MMW) with side-talk rejection | Yang Liu et al. 2025 (ref [23] in Yang 2025) | Whisper LLM robust to side-talk via multi-mic |

## Evaluation Methodology

Yang et al. 2025 introduced a **HATS (head and torso simulator)** real-recorded evaluation: 72 bystander locations = 8 angles × 3 heights × 3 distances, with both wearer-first and bystander-first speaker order. This enables **angle-resolved** failure analysis (e.g., 270°/315°/0° wearer-bystander and 225° bystander-wearer at 50% overlap are hardest).

## Related Concepts

- [[concepts/beamforming|Beamforming]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/nlcmv-beamforming|NLCMV Beamforming]]
- [[concepts/differential-asr|Differential ASR]]
- [[concepts/side-talk-detection|Side-Talk Detection (STD)]]
- [[concepts/roi-beamforming|Region-of-Interest Beamforming]]
- [[concepts/target-speaker-asr|Target Speaker ASR]]

## Related Sources

- [[sources/lin-2024-agadir-array-geometry-agnostic-speech-recognition|Lin et al. 2024: AGADIR]]
- [[sources/feng-2025-directional-source-separation-smart-glasses|Feng et al. 2025: Directional Source Separation for Smart Glasses]]
- [[sources/yang-2025-mc-differential-asr-smart-glasses|Yang et al. 2025: Multi-Channel Differential ASR for Smart Glasses]]
