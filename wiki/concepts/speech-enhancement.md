---
type: concept
created: 2026-06-19
updated: 2026-06-19
tags:
  - speech-processing
  - audio-enhancement
---

# Speech Enhancement

Speech enhancement (SE) is the task of improving the perceptual quality and intelligibility of speech signals degraded by additive noise, reverberation, or other distortions. Modern deep learning approaches operate in either the time domain or time-frequency (TF) domain, leveraging architectures such as convolutional neural networks, recurrent networks, transformers, and diffusion models.

## Key Formulations

- $Given clean speech $x \in \mathbb{R}^T$, noisy observation $y$, and additive noise $n$: $y = x + n$$
- $SE systems estimate $\hat{x}$ from $y$$
- $Common approaches include spectral mapping, masking (e.g., complex ratio mask), and time-domain wave-to-wave regression$

## Sub-areas

- Personalized speech enhancement (conditioning on speaker embeddings)
- Multi-channel speech enhancement (beamforming, spatial filtering)
- Bone-conduction speech enhancement
- Real-time low-latency enhancement

## Related Concepts

- [[concepts/gaussian-mixture-model|Gaussian Mixture Model (GMM)]]
- [[concepts/speaker-embedding|Speaker Embedding]]
- [[concepts/prior-matching|Prior Matching]]
- [[concepts/personalized-speech-enhancement|Personalized Speech Enhancement (PSE)]]
- [[concepts/mp-senet|MP-SENet]]
- [[concepts/ecapa-tdnn|ECAPA-TDNN]]

## Related Sources

- [[sources/zhu-2026-g-map-se-guided-speech-enhancement|G-MaP-SE: Guided Speech Enhancement via GMM-Based Prior Matching (Interspeech 2026)]]