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

## Applications in Lightweight AEC (EchoFree)

[[sources/li-2025-echofree-neural-aec|EchoFree (Li et al. 2025)]] uses a frozen WavLM-Large as a multi-layer embedding extractor for a two-stage training strategy on a 278K-parameter AEC post filter:

- **Stage 1** — train with **SSL loss only**: MSE between WavLM embeddings of estimated and ground-truth signals, averaged over all $L$ layers. Provides coarse spectral learning without requiring a perceptual gain target.
- **Stage 2** — fine-tune with a weighted combination of [[concepts/bark-scale-spectral-features|Bark-scale]] gain loss (fourth-order + second-order + cross-entropy) and SSL loss. SSL acts as a regularizer preserving representation fidelity while the model is fine-tuned toward better Bark gain prediction.

Ablation shows SSL-only training beats conventional gain-loss training on double-talk EchoMOS (3.91 vs 3.74), confirming that SSL embeddings carry information useful for residual echo suppression beyond what a simple gain target provides. The two-stage combination achieves the best overall trade-off across the four AECMOS sub-metrics.

## Related Concepts

- [[concepts/drifting-models|Drifting Models]]
- [[concepts/diffusion-models-for-speech|Diffusion Models for Speech Enhancement]]
- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]]
- [[concepts/bark-scale-spectral-features|Bark-Scale Spectral Features]]
- [[concepts/u-net-post-filter|U-Net Post Filter]]

## Related Sources

- [[sources/xu-2026-drifting-models-speech-enhancement|Xu et al. 2026: Speech Enhancement Based on Drifting Models]]
- [[sources/li-2025-echofree-neural-aec|Li et al. 2025: EchoFree]]
