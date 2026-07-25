---
type: concept
created: 2026-07-25
updated: 2026-07-25
sources:
  - raw/papers/huang-2026-lightweight-speech-enhancement-guided-target-speech-extraction/full-text.md
tags:
  - target-speech-extraction
  - data-augmentation
  - training-strategy
  - speech-distortion
---

# Distortion-aware Training

**Distortion-aware training** is a data-augmentation strategy for target speech extraction (TSE) in which the mildly distorted output of a speech-enhancement front-end is used as an additional training input alongside the original noisy mixture, so that the model is explicitly exposed to distorted speech and learns to be robust against it. It was introduced by Huang et al. (2026) as the D-LGTSE extension of LGTSE.

## Motivation

In multi-speaker TSE the extracted target speech often contains residual distortions. A TSE backbone trained only on clean-target/noisy-input pairs may fail when its input is itself a distorted signal (e.g., the output of an imperfect denoiser). Rather than treating the denoiser's residual distortion as a defect, D-LGTSE reframes it as a **free source of acoustic variability** for training: because the [[concepts/gtcrn|GTCRN]]-denoised spectrum $\mathbf{Y}_d$ is not perfectly clean but mildly distorted, it serves as a realistic distortion sample that can augment the training distribution.

## Three Data-Usage Strategies

D-LGTSE investigates three ways of incorporating the distorted denoised output $\mathbf{Y}_d$ during training:

### 1. Distortion-aware Concatenation

Concatenate the original noisy spectrum $\mathbf{Y}$, the denoised spectrum $\mathbf{Y}_d$, and the [[concepts/noise-agnostic-enrollment-guidance|noise-agnostic guidance]] $\mathbf{E}_{Y_d}$ along the channel dimension. The fused representation is fed into the backbone in a single forward pass. This lets the backbone jointly process noisy and mildly distorted speech at inference time.

### 2. On-the-fly

Enlarge each mini-batch $\mathcal{B}$ by including both the original noisy and the on-the-fly denoised spectrums:

$$
\mathcal{B} = \{(\mathbf{Y}_i, \mathbf{E}_{Y_d}^i), \mathbf{Y}_{\text{target}}^i\}_{i=1}^N \cup \{(\mathbf{Y}_d^i, \mathbf{E}_{Y_d}^i), \mathbf{Y}_{\text{target}}^i\}_{i=1}^N
$$

where $N$ is the original mini-batch size and $\mathbf{Y}_{\text{target}}^i$ is the clean target (ground-truth) for the $i$-th sample. This lets the model process noisy and mildly distorted speech in parallel within each batch.

### 3. Offline

Pre-process the entire noisy dataset $\mathcal{D}$ to obtain a denoised dataset $\mathcal{D}_d$, then merge and shuffle:

$$
\mathcal{D}_{\text{mix}} = \mathrm{shuffle}(\mathcal{D} \cup \mathcal{D}_d)
$$

The shuffle operation encourages generalization by exposing the model to diverse noisy–denoised pairings. Compared with distortion-aware concatenation, this offline strategy reduces both training computation cost and inference latency.

## Why Offline Wins

| Strategy | SI-SDR (dB) | PESQ | STOI (%) |
|:---------|:-----------:|:----:|:--------:|
| Concatenation | 7.96 | 2.24 | 81.37 |
| On-the-fly | 8.10 | 2.28 | 81.80 |
| **Offline** | **8.32** | **2.30** | **82.28** |

The offline strategy wins because it **persists the distortion signal throughout training**. In the concatenation and on-the-fly mechanisms, the denoiser is unfrozen during joint fine-tuning and becomes increasingly effective, which reduces the residual distortion in $\mathbf{Y}_d$ over training — limiting the model's exposure to challenging distorted conditions. The offline strategy, by contrast, stores the distorted speech in advance (computed from the pretrained, frozen GTCRN), so the distortion distribution is preserved across the whole training run and the robustness benefit is retained.

## Relation to Two-stage Training

Distortion-aware training is combined with a two-stage schedule: (1) pretrain GTCRN for SE and pretrain the backbone for TSE using GTCRN's denoised output; (2) unfreeze GTCRN and jointly fine-tune the whole system end-to-end. The joint loss combines denoising and TSE objectives:

$$
\mathcal{L} = -\mathrm{SI\text{-}SDR}(\mathbf{y}_d, \mathbf{y}_{\text{clean}}) - \mathrm{SI\text{-}SDR}(\hat{\mathbf{y}}_{\text{target}}, \mathbf{y}_{\text{target}})
$$

Without joint fine-tuning, simple stacking of separately pretrained modules (SI-SDR 7.60 dB) or a frozen-GTCRN backbone (8.02 dB) underperform the two-stage joint scheme (8.32 dB).

## Related Concepts

- [[concepts/noise-agnostic-enrollment-guidance|Noise-agnostic Enrollment Guidance]]
- [[concepts/target-speaker-extraction|Target Speaker Extraction (TSE)]]
- [[concepts/sef-pnet|SEF-PNet]]
- [[concepts/gtcrn|GTCRN]]

## Related Sources

- [[sources/huang-2026-lightweight-speech-enhancement-guided-target-speech-extraction|Huang et al. 2026: Lightweight Speech Enhancement Guided Target Speech Extraction in Noisy Multi-Speaker Scenarios]]
