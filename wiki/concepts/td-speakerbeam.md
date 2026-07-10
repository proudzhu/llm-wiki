---
type: concept
created: 2026-07-10
updated: 2026-07-10
sources:
  - raw/papers/ostergaard-2026-own-voice-cancellation/full-text.md
tags:
  - neural-network
  - speech-enhancement
  - target-speaker-extraction
  - time-domain
  - speaker-conditioning
---

# TD-SpeakerBeam

**TD-SpeakerBeam** (Time-Domain SpeakerBeam) is a target speaker extraction model that conditions a time-domain TasNet-style masking network on a short enrollment utterance to identify and extract (or cancel) a specific speaker. Introduced by Delcroix et al. (ICASSP 2020), it serves as the standard baseline for enrollment-conditioned speech extraction and [[concepts/own-voice-cancellation|own-voice cancellation]] tasks.

## Architecture

TD-SpeakerBeam consists of two networks that do **not** share parameters:

1. **Main network** — a ConvTasNet-style encoder–masking–decoder pipeline operating on the input mixture waveform
2. **Auxiliary network** — a ConvTasNet encoder that processes the enrollment utterance and produces a [[concepts/speaker-embedding|speaker embedding]]

The speaker embedding is applied to the main network via an **adaptation layer** using element-wise multiplication with intermediate representations. When the main network uses skip connections, the auxiliary network outputs one embedding for the skip path and one for the residual path.

## Hyperparameters

Standard configuration (as used in the OVC benchmark):

| Parameter | Symbol | Value |
|-----------|--------|-------|
| Encoder dimension | $N$ | 256 |
| Kernel size | $L$ | 32 (2 ms at 16 kHz) |
| Bottleneck channels | $B$ | 256 |
| Hidden channels | $H$ | 512 |
| Kernel size in bottleneck | $P$ | 3 |
| Number of repeats | $X$ | 8 |
| Number of residual blocks | $R$ | 4 |

The kernel size $L = 32$ corresponds to **2 ms algorithmic latency** at 16 kHz.

## Use as Baseline

TD-SpeakerBeam is the baseline for [[concepts/own-voice-cancellation|OVC]], achieving:

- **Non-causal OVC**: 13.42 dB SDR (F), 14.78 dB SDR (D)
- **Causal OVC**: 11.13 dB SDR (F), 12.09 dB SDR (D)
- **Compute**: 4.97 GMAC/s (main), 1.67 GMAC/s (auxiliary)

The [[concepts/mamba-mingru|Mamba-MinGRU]] architecture matches this performance at ~15× lower main-network compute.

## Related Concepts

- [[concepts/target-speaker-extraction|Target Speaker Extraction (TSE)]]
- [[concepts/own-voice-cancellation|Own-Voice Cancellation (OVC)]]
- [[concepts/mamba-mingru|Mamba-MinGRU]]
- [[concepts/speaker-embedding|Speaker Embedding]]
- [[concepts/time-domain-speech-enhancement|Time-Domain Speech Enhancement]]

## Related Sources

- [[sources/ostergaard-2026-own-voice-cancellation|Østergaard et al. 2026: Don't Listen to Me — Own-Voice Cancellation]]
