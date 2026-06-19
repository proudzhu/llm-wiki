---
type: concept
created: 2026-06-19
updated: 2026-06-19
tags:
  - speech-enhancement
  - neural-network-architecture
---

# MP-SENet

MP-SENet is a time-frequency domain speech enhancement model that serves as the backbone for G-MaP-SE. It uses a magnitude-phase estimation framework with TF blocks and attention mechanisms. The model processes STFT spectrograms and estimates both magnitude and phase components.

## Key Formulations

- $Architecture: Encoder + TF blocks with multi-head attention + Decoder$
- $Loss: Multi-component including PESQ-based GAN loss, STFT consistency, magnitude, complex-spectrum, phase, and time-domain losses$

## Related Concepts

- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/prior-matching|Prior Matching]]

## Related Sources

- [[sources/zhu-2026-g-map-se-guided-speech-enhancement|G-MaP-SE: Guided Speech Enhancement via GMM-Based Prior Matching (Interspeech 2026)]]