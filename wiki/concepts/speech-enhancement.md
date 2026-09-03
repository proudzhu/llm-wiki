---
type: concept
created: 2026-06-19
updated: 2026-09-03
sources:
  - raw/papers/chao-2024-mamba-speech-enhancement/full-text.md
  - raw/papers/tashev-2008-sound-capture-spatial-filter/full-text.md
  - raw/papers/shetu-2026-generative-discriminative-comparison/full-text.md
  - raw/papers/li-2020-residual-noise-control/full-text.md
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
- Low-complexity enhancement for embedded devices (e.g., [[concepts/ulcnet|ULCNet]])
- Low-power spiking enhancement — SNN-based SE for neuromorphic/edge deployment (e.g., [[concepts/sse-net|SSE-Net]])
- State-space-model-based enhancement — Mamba / S4ND / S4 as the core sequence model (e.g., [[concepts/semamba|SEMamba]], [[concepts/sicrn|SICRN]])
- Training-paradigm choice — generative (GAN / diffusion / flow / consistency) vs. discriminative training, with quantified robustness, complexity, and hallucination trade-offs (see [[concepts/generative-vs-discriminative-speech-enhancement|Generative vs. Discriminative Speech Enhancement]])
- Loss-function design with residual noise control — training-time trade-off between speech distortion and natural residual noise, generalizing MSE/components loss into a parameterized family (e.g., [[concepts/generalized-loss-function|Generalized Loss Function]])

## Related Concepts

- [[concepts/gaussian-mixture-model|Gaussian Mixture Model (GMM)]]
- [[concepts/speaker-embedding|Speaker Embedding]]
- [[concepts/prior-matching|Prior Matching]]
- [[concepts/personalized-speech-enhancement|Personalized Speech Enhancement (PSE)]]
- [[concepts/mp-senet|MP-SENet]]
- [[concepts/semamba|SEMamba]] — first Mamba-based SE; SOTA PESQ 3.69 on VoiceBank-DEMAND
- [[concepts/mamba|Mamba]] — selective SSM core block used by SEMamba
- [[concepts/perceptual-contrast-stretching|Perceptual Contrast Stretching (PCS)]] — post-processing that boosts SE PESQ
- [[concepts/ecapa-tdnn|ECAPA-TDNN]]
- [[concepts/ulcnet|ULCNet]]
- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]]
- [[concepts/generative-vs-discriminative-speech-enhancement|Generative vs. Discriminative Speech Enhancement]]
- [[concepts/speech-enhancement-hallucination|Speech Enhancement Hallucination]]
- [[concepts/diffusion-models-for-speech|Diffusion Models for Speech Enhancement]]
- [[concepts/generalized-loss-function|Generalized Loss Function]]

## Related Sources

- [[sources/zhu-2026-g-map-se-guided-speech-enhancement|G-MaP-SE: Guided Speech Enhancement via GMM-Based Prior Matching (Interspeech 2026)]]
- [[sources/shetu-2024-hybrid-low-complexity-aenr|Shetu et al. 2024: Hybrid Low-Complexity AENR]]
- [[sources/liu-2026-sse-net|Liu et al. 2026: SSE-Net]] — spike-native SNN-based monaural speech enhancement (SOTA among SNN-SE, power proxy 19.70 M Ops/s)
- [[sources/chao-2024-mamba-speech-enhancement|Chao et al. 2024: An Investigation of Incorporating Mamba for Speech Enhancement]] — first Mamba-based SE; SOTA PESQ 3.69 on VoiceBank-DEMAND
- [[sources/tashev-2008-sound-capture-spatial-filter|Tashev et al. 2008: Sound Capture System and Spatial Filter for Small Devices]] — classical statistical-model multi-channel SE for small devices (10.43 dB SNR / 0.39 PESQ-MOS on a 9.6 mm back-to-back array)
- [[sources/shetu-2026-generative-discriminative-comparison|Shetu, Habets & Brendel 2026: Generative vs. Discriminative SE]] — 14-model controlled comparison of generative and discriminative training paradigms
- [[sources/li-2020-residual-noise-control|Li, Peng, Zheng & Li 2020: Supervised Speech Enhancement with Residual Noise Control]] — generalized loss function embedding residual noise control in training