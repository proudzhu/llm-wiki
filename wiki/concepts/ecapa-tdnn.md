---
type: concept
created: 2026-06-19
updated: 2026-06-19
tags:
  - speaker-recognition
  - neural-network-architecture
---

# ECAPA-TDNN

ECAPA-TDNN (Emphasized Channel Attention, Propagation and Aggregation in Time Delay Neural Network) is a state-of-the-art speaker embedding extractor architecture. It uses 1D convolutional layers with channel attention, squeeze-and-excitation blocks, and multi-layer feature aggregation. In G-MaP-SE, a frozen ECAPA-TDNN is used as the feature extractor to produce 192-dimensional speaker embeddings.

## Related Concepts

- [[concepts/speaker-embedding|Speaker Embedding]]
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/zhu-2026-g-map-se-guided-speech-enhancement|G-MaP-SE: Guided Speech Enhancement via GMM-Based Prior Matching (Interspeech 2026)]]