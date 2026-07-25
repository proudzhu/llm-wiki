---
type: concept
created: 2026-07-25
updated: 2026-07-25
sources:
  - raw/papers/huang-2026-lightweight-speech-enhancement-guided-target-speech-extraction/full-text.md
tags:
  - target-speech-extraction
  - enrollment-guidance
  - speech-enhancement
  - noise-robustness
---

# Noise-agnostic Enrollment Guidance

**Noise-agnostic enrollment guidance** is a target speech extraction (TSE) technique that denoises the noisy mixture before computing the context-interaction representation between enrollment speech and the mixture, so that the target-speaker guidance signal is free of noise contamination. It was introduced by Huang et al. (2026) in the LGTSE framework to address the failure mode where noise in the mixture corrupts the enrollment-guided representation and misleads the backbone in identifying the target speaker.

## Problem: Noise-contaminated Guidance

In embedding/encoder-free TSE methods such as [[concepts/sef-pnet|SEF-PNet]], the enrollment guidance is obtained by a context-interaction (e.g., softmax-attention) between enrollment $\mathbf{E}$ and noisy mixture $\mathbf{Y}$:

$$
\mathbf{E}_Y = \mathbf{E} \times \mathrm{softmax}\left(\mathbf{E}^{\mathrm{T}} \times \mathbf{Y}\right)
$$

Because the softmax correlation is computed against the noisy $\mathbf{Y}$, the resulting $\mathbf{E}_Y$ inherits noise from the mixture. Under noisy multi-speaker conditions this contamination severely degrades the quality of the guidance and causes target-speech distortion. Prior remedies (e.g., a jointly trained enhancer to reduce enrollment–noise similarity) still leave enrollment speech interacting with noisy mixtures, so the guidance remains noise-contaminated.

## Formulation

LGTSE inserts a lightweight speech-enhancement model (here [[concepts/gtcrn|GTCRN]], 0.05 M params) before the context interaction. The noisy mixture is first denoised:

$$
\mathbf{Y}_d = \mathrm{GTCRN}(\mathbf{Y}), \qquad \mathbf{E}_{Y_d} = \mathbf{E} \times \mathrm{softmax}\left(\mathbf{E}^{\mathrm{T}} \times \mathbf{Y}_d\right)
$$

The guidance $\mathbf{E}_{Y_d}$ is now **noise-agnostic**: the correlation between enrollment and mixture is computed on a denoised feature, so noise no longer leaks into the speaker representation. The concatenated feature $[\mathbf{Y}; \mathbf{E}_{Y_d}]$ is then passed to the TSE backbone (base concatenation). Importantly, the backbone still receives the original noisy $\mathbf{Y}$ for extraction — only the *guidance path* is denoised.

## Why It Works

- Denoising $\mathbf{Y}$ removes the noise components that would otherwise dominate the frame-wise correlation $\mathbf{E}^{\mathrm{T}} \mathbf{Y}$, so the softmax attends to actual target-speaker frames rather than noise frames.
- Because [[concepts/gtcrn|GTCRN]] is ultralightweight (0.05 M params, 0.03 GMACs/s), the overhead on top of the TSE backbone is negligible (~0.8% of SEF-PNet's params).
- Spectrogram visualizations (Fig. 2 of the source paper) confirm that the guidance spectrogram produced from denoised interaction is visibly cleaner than that from direct noisy interaction.

## Relation to Distortion-aware Training

The denoiser output $\mathbf{Y}_d$ is not perfectly clean — it carries mild distortion. [[concepts/distortion-aware-training|D-LGTSE]] exploits this property by using $\mathbf{Y}_d$ as an additional distorted training input, turning the denoiser's imperfection into a data-augmentation asset rather than a liability.

## Empirical Effect

On Libri2Mix (2-speaker + noise), switching from noise-contaminated guidance (SEF-PNet) to noise-agnostic guidance (LGTSE) improves SI-SDR from 7.43 → 7.88 dB, PESQ 2.14 → 2.21, and STOI 80.31% → 81.27% — a +0.45 dB SI-SDR gain from guidance denoising alone, before any distortion-aware training.

## Related Concepts

- [[concepts/target-speaker-extraction|Target Speaker Extraction (TSE)]]
- [[concepts/distortion-aware-training|Distortion-aware Training]]
- [[concepts/sef-pnet|SEF-PNet]]
- [[concepts/gtcrn|GTCRN]]
- [[concepts/personalized-speech-enhancement|Personalized Speech Enhancement]]
- [[concepts/speaker-embedding|Speaker Embedding]]

## Related Sources

- [[sources/huang-2026-lightweight-speech-enhancement-guided-target-speech-extraction|Huang et al. 2026: Lightweight Speech Enhancement Guided Target Speech Extraction in Noisy Multi-Speaker Scenarios]]
