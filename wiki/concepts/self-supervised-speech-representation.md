---
type: concept
created: 2026-05-03
updated: 2026-05-03
sources:
  - raw/papers/xu-2026-drifting-models-speech-enhancement/full-text.md
tags:
  - speech-processing
  - self-supervised-learning
  - representation-learning
---

# Self-Supervised Speech Representation

**Self-supervised speech representations** are learned features extracted from speech audio using models pre-trained on large unlabeled corpora via self-supervised objectives, capturing hierarchical acoustic and linguistic structures.

## Overview

Self-supervised learning (SSL) models for speech — such as HuBERT, WavLM, and DistilHuBERT — learn rich representations by solving pretext tasks on unlabeled audio. These models exhibit a well-documented **layer hierarchy**:

- **Shallow layers**: Capture low-level acoustic structure (spectral patterns, pitch)
- **Middle layers**: Encode phonetic and segmental information
- **Deep layers**: Represent semantic and linguistic content

This hierarchical structure makes SSL features valuable for downstream tasks where Euclidean distances on raw spectrograms are suboptimal.

## Key Models

| Model | Parameters | Dimensions | Training Objective |
|-------|-----------|------------|-------------------|
| HuBERT-Large | 300M | 1024-d | Masked prediction of clustered features |
| WavLM-Large | 317M | 1024-d | Masked speech prediction + denoising |
| DistilHuBERT | ~75M | 768-d | Knowledge distillation from HuBERT |

## Applications in Generative Speech Enhancement

In [[drifting-models|Drifting Models]] for speech enhancement (DriftSE), SSL encoders serve as frozen feature extractors for computing the drifting field in a perceptually meaningful latent space:

- **Multi-layer supervision**: Drift is computed and aggregated across multiple encoder layers to capture both fine acoustic detail and high-level semantic structure
- **Frame-wise operation**: SSL features provide frame-level representations (typically 20ms hop, 25ms receptive field) suitable for temporal processing
- **DistilHuBERT advantage**: Despite being smaller (768-d vs 1024-d), DistilHuBERT with multi-layer supervision achieves competitive or better SI-SDR while maintaining similar perceptual quality

## Related Concepts

- [[../concepts/drifting-models|Drifting Models]]
- [[../concepts/diffusion-models-for-speech|Diffusion Models for Speech Enhancement]]

## Related Sources

- [[../sources/xu-2026-drifting-models-speech-enhancement|Xu et al. 2026: Speech Enhancement Based on Drifting Models]]
