---
type: concept
created: 2026-06-19
updated: 2026-06-19
tags:
  - speaker-recognition
  - representation-learning
---

# Speaker Embedding

A speaker embedding is a fixed-dimensional vector representation extracted from a speech utterance that captures speaker-specific characteristics. Speaker embeddings are used for speaker verification, diarization, and as conditioning features in personalized speech enhancement. Common extractors include x-vectors and ECAPA-TDNN.

## Key Formulations

- $Typically 128-512 dimensional vectors$
- $Often $\ell_2$-normalized to project onto the unit hypersphere$
- $Extracted from a frozen pretrained speaker recognition model$

## Auxiliary Encoder Architectures

In enrollment-conditioned tasks ([[concepts/target-speaker-extraction|TSE]], [[concepts/own-voice-cancellation|OVC]]), the speaker embedding is produced by an **auxiliary network** (auxiliary encoder). Two families are commonly used:

| Auxiliary type | Architecture | Compute | Notes |
|----------------|--------------|---------|-------|
| ConvTasNet-based | Temporal convolutional network | ~1.67 GMAC/s | Standard in [[concepts/td-speakerbeam|TD-SpeakerBeam]] |
| Linear RNN-based | Bidirectional [[concepts/mingru|MinGRU]] / Mamba blocks | ~0.26 GMAC/s | Better SDR on full-mixture condition at ~6× lower compute |

Østergaard et al. (2026) showed that linear RNN auxiliary encoders provide better speaker representations than ConvTasNet-based ones for speaker conditioning in OVC, while substantially reducing compute.

## Related Concepts

- [[concepts/ecapa-tdnn|ECAPA-TDNN]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/prior-matching|Prior Matching]]
- [[concepts/personalized-speech-enhancement|Personalized Speech Enhancement (PSE)]]
- [[concepts/own-voice-cancellation|Own-Voice Cancellation (OVC)]]
- [[concepts/td-speakerbeam|TD-SpeakerBeam]]
- [[concepts/mamba-mingru|Mamba-MinGRU]]

## Related Sources

- [[sources/ostergaard-2026-own-voice-cancellation|Østergaard et al. 2026: Don't Listen to Me — Own-Voice Cancellation]]
- [[sources/zhu-2026-g-map-se-guided-speech-enhancement|G-MaP-SE: Guided Speech Enhancement via GMM-Based Prior Matching (Interspeech 2026)]]