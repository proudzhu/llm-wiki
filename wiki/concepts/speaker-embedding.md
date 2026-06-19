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

## Related Concepts

- [[concepts/ecapa-tdnn|ECAPA-TDNN]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/prior-matching|Prior Matching]]
- [[concepts/personalized-speech-enhancement|Personalized Speech Enhancement (PSE)]]

## Related Sources

- [[sources/zhu-2026-g-map-se-guided-speech-enhancement|G-MaP-SE: Guided Speech Enhancement via GMM-Based Prior Matching (Interspeech 2026)]]