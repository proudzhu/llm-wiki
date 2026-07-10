---
type: concept
created: 2026-07-10
updated: 2026-07-10
sources:
  - raw/papers/ostergaard-2026-own-voice-cancellation/full-text.md
tags:
  - speech-enhancement
  - source-separation
  - target-speaker-extraction
  - far-field
  - low-latency
  - streaming
---

# Own-Voice Cancellation (OVC)

**Own-Voice Cancellation (OVC)** is the task of removing a target (enrolled) speaker from a noisy multi-speaker mixture while preserving any remaining speech. It is the complement of [[concepts/target-speaker-extraction|target speaker extraction (TSE)]]: where TSE keeps only the enrolled speaker, OVC removes only the enrolled speaker.

## Problem Formulation

Given an input mixture containing a target speaker $s$ (the own-voice), other speakers $i$, and noise:

$$\mathbf{y} = \mathbf{x}^{s} + \sum_{i \neq s} \mathbf{x}^{i} + \mathbf{n}$$

OVC aims to recover:

$$\bar{\mathbf{y}} = \sum_{i \neq s} \mathbf{x}^{i}$$

The network is conditioned on a short enrollment utterance from the target speaker (as in TSE), but produces the mixture *minus* that speaker.

## Motivation: Latency-Induced Own-Voice Artifacts

When a far-field device (e.g., a table-top microphone) captures, enhances, and streams audio back to the user, the acoustic round-trip time easily exceeds 10 ms. The user's own voice arrives with a noticeable delay, producing perceptible echo-like artifacts. Key perceptual thresholds from the hearing-aid literature:

| Delay | Effect |
|-------|--------|
| 4–10 ms | Perceptible disturbances |
| 10–15 ms | Increasingly disturbing |
| > 15–20 ms | Unacceptable to most listeners |

OVC addresses this by treating the user's own voice as an unwanted signal to be suppressed before streaming, using only a short enrollment utterance as reference.

## Relation to Other Tasks

| Task | Goal | Reference signal |
|------|------|------------------|
| **OVC** | Remove enrolled speaker | Enrollment utterance |
| [[concepts/target-speaker-extraction\|TSE]] | Extract enrolled speaker | Enrollment utterance |
| Speech separation | Separate all speakers | None (blind) |
| [[concepts/personalized-speech-enhancement\|PSE]] | Enhance enrolled speaker | Enrollment utterance |
| Acoustic echo cancellation | Remove playback signal | Far-end reference signal |

OVC can be viewed as a special case of speech separation where the source identifiability problem is solved by directly informing the network which speaker to remove. Unlike acoustic echo cancellation, OVC does not require access to the playback/reference signal — only a short enrollment utterance.

## Training with Speaker Dropout

Following "Listen only to me!" (Delcroix 2022), the network is trained with independent speaker dropout:

- Other speaker dropped with probability $p_o$ — target output is silence
- Enrolled speaker dropped with probability $p_e$ — target is the denoised other speaker

This enables the model to handle cases where only the own-voice is present (output silence) or only background noise + other speakers (denoise).

## Loss Function

Negative thresholded SDR loss extended to handle silence:

$$\mathbf{L}_{\mathrm{SDR}}(\hat{\mathbf{x}}, \mathbf{x}, \mathbf{y}) = \begin{cases} \mathcal{L}^{\text{active}}(\hat{\mathbf{x}}, \mathbf{x}), & \text{if } \mathbf{x} \neq \mathbf{0}, \\ \mathcal{L}^{\text{inactive}}(\hat{\mathbf{x}}, \mathbf{y}), & \text{if } \mathbf{x} = \mathbf{0}, \end{cases}$$

with soft thresholds $\tau$ preventing the model from over-optimizing already-well-separated mixtures.

## Key Architectures

| Architecture | Type | Latency | Notes |
|--------------|------|---------|-------|
| [[concepts/td-speakerbeam\|TD-SpeakerBeam]] | ConvTasNet-based | 2 ms | Baseline |
| [[concepts/mamba-mingru\|Mamba-MinGRU]] | Linear RNN | 2 ms | Compute-efficient, matches baseline |

## Related Concepts

- [[concepts/target-speaker-extraction|Target Speaker Extraction (TSE)]]
- [[concepts/mamba-mingru|Mamba-MinGRU]]
- [[concepts/td-speakerbeam|TD-SpeakerBeam]]
- [[concepts/speaker-embedding|Speaker Embedding]]
- [[concepts/personalized-speech-enhancement|Personalized Speech Enhancement (PSE)]]
- [[concepts/time-domain-speech-enhancement|Time-Domain Speech Enhancement]]

## Related Sources

- [[sources/ostergaard-2026-own-voice-cancellation|Østergaard et al. 2026: Don't Listen to Me — Own-Voice Cancellation]]
