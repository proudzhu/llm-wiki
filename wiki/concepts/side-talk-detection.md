---
type: concept
created: 2026-08-22
updated: 2026-08-22
sources:
  - raw/papers/yang-2025-mc-differential-asr-smart-glasses/full-text.md
tags:
  - voice-activity-detection
  - speech-recognition
  - smart-glasses
  - privacy-preserving
---

# Side-Talk Detection (STD)

**Side-Talk Detection (STD)** is a [[concepts/voice-activity-detection|voice activity detection]]-adjacent task introduced for [[concepts/wearer-speech-recognition|wearer speech recognition (WSR)]] on smart glasses. The STD task is to distinguish, at the audio sample level, between (i) speech from the **wearer** of the device, (ii) speech from a **bystander** (side-talk), and (iii) **non-speech** segments — **without modeling speaker identity**.

## Why STD instead of speaker diarization?

Standard speaker diarization solves "who spoke when" by clustering speaker embeddings, which requires knowing (or enrolling) the speaker's identity. On an always-on wearable, this raises privacy concerns: the device should not store or use the wearer's (or bystanders') speaker identity. STD sidesteps the issue by exploiting a **structural prior** — the device is worn by the wearer — so the role (wearer/bystander) is determined by the relative position of the source to the device, not by speaker identity.

## Distinctive Formulation

The streaming STD model of [[entities/yang-liu|Yang Liu]] et al. (MMW, ASRU 2025; and adopted as a frontend in [[sources/yang-2025-mc-differential-asr-smart-glasses|Yang et al. 2025]]) is a lightweight (~2M parameter) [[concepts/film-layer|temporal convolutional network (TCN)]] that produces sample-level logits over the three classes. In the differential ASR system, the logits are downsampled via two Conv2D layers (kernels [20,1], strides [10,1] and [16,1], intermediate channels = 3) into a 5-dimensional **STD embedding** that is concatenated with log-Mel features of the beamformer and microphone-selection outputs and fed to an RNN-T ASR backbone.

The STD model is trained on **real non-user data** (not the wearer) so it does not require per-user enrollment. It runs in streaming mode at the audio sample level — no future-context lookahead — so the additional latency to the ASR pipeline is negligible.

## Role in Differential ASR

In Yang et al. 2025's differential ASR, the STD embedding is the third frontend channel (alongside beamformer ch-x and microphone-selection ch-0). It provides a **complementary cue**: while ch-x and ch-0 carry acoustic features of the mixed signal, the STD embedding carries a coarse semantic role label (wearer/bystander/non-speech). This complementary view lets the ASR model down-weight bystander-corrupted frames even when the beamformer fails to fully suppress them.

## Related Concepts

- [[concepts/voice-activity-detection|Voice Activity Detection (VAD)]]
- [[concepts/differential-asr|Differential ASR]]
- [[concepts/wearer-speech-recognition|Wearer Speech Recognition (WSR)]]
- [[concepts/target-speaker-vad|TS-VAD]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Related Sources

- [[sources/yang-2025-mc-differential-asr-smart-glasses|Yang et al. 2025: Multi-Channel Differential ASR for Smart Glasses]]
