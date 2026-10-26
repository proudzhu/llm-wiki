---
type: concept
created: 2026-10-26
updated: 2026-10-26
sources:
  - raw/papers/huang-2026-undf-configurable-directivity/full-text.md
tags:
  - neural-directional-filtering
  - directivity-pattern
  - conditioning
  - deep-learning
  - spatial-audio
---

# UNDF

**UNDF** (neural directional filtering with user-defined directivity patterns) extends [[concepts/neural-directional-filtering|neural directional filtering]] so that the *directivity pattern itself* — not just the steering direction — is a user-configurable input at inference. Introduced by Huang, Chetupalli & Habets (arXiv 2510.20253), UNDF conditions a DNN on a sampled pattern vector $\Lambda(\theta)$ ($L=72$ angles over $[0,2\pi]$, assumed frequency-invariant), allowing the target spatial response to be changed arbitrarily — even frame by frame — after training.

The progression of the NDF family's inference-time configurability:

| Model | Pattern shape | Steering direction | Gain scaling |
|-------|---------------|--------------------| ------------ |
| NDF (Wechsler et al. 2024) | fixed at training | fixed at training | fixed |
| SNDF (Huang et al. 2025) | fixed at training | free (one-hot conditioning) | fixed |
| UNDF (this) | **user-defined** | **user-defined** | **user-defined** |
| FiLM-JNF steering (journal paper) | fixed shape per model | free (continuous sinusoidal embedding) | fixed |

## Signal Model

The target is the per-source weighted mixture at the reference microphone, with a possibly time-varying user pattern $\Lambda_t$:

$$
Z[f,t]=\sum_{n=1}^{N}\Lambda_{t}(\theta_{n})\,X_{1,n}[f,t],
$$

i.e., spatial *recording* with a desired weighting of the scene rather than extraction of a single source.

## Conditioning Mechanisms

- **PV-JNF**: the pattern vector feeds a linear layer whose output initializes the F-BiLSTM states (adapted from the [[concepts/spatially-selective-nonlinear-filter|SSF]] one-hot conditioning). Works for training-set patterns but fails to generalize: unseen steering directions cause bias, unseen orders collapse (10.4 dB SDR on a 3rd-order pattern), and scaled patterns are badly approximated (8.1 dB).
- **FiLM-JNF** ([[concepts/film-jnf|FiLM-JNF]]): the pattern vector is mapped by two linear layers to per-feature affine parameters $\boldsymbol{\alpha},\boldsymbol{\beta}\in\mathbb{R}^{512}$; the FiLM layer applies $\mathbf{y}=\boldsymbol{\alpha}\odot\mathbf{x}+\boldsymbol{\beta}$ between the F-BiLSTM and T-UniLSTM, shared across time and frequency. This provides **compositional generalization over the pattern space**: unseen higher orders (17.3 vs 10.4 dB), unseen scaling (19.5 vs 8.1 dB), unseen steering (24.3 vs 20.9 dB) — up to 11 dB better than PV-JNF.

Both variants output a complex mask applied to the reference microphone, and both are causal with per-frame conditioning, so **time-varying patterns** take effect immediately in the output.

## Training Recipes

| Recipe | Patterns | Effect |
|--------|----------|--------|
| A | 60 first-order patterns ($\mu\in\{0,\ldots,0.9\}$, $\theta_s\in\{0°,\ldots,300°\}$) | finite set; used to compare conditioning mechanisms |
| B− | one random DMA pattern ($C=1$) | broader coverage alone |
| B | linear combination of $C=4$ random DMA patterns (orders $J\in[1,11]$) | combinations drive multi-scaled approximation (19.8 vs 13.0 dB) |
| B+ | B + rectangular pattern mixes (⅓ each: DMA-combination / rectangular-combination / mixed) | rectangular mixing enables **irregular shapes** (20.4 vs 14.8 dB) |

## Key Findings

- FiLM conditioning beats initial-state conditioning on every unseen-pattern dimension (steering, order, scaling); on seen patterns they are comparable.
- Recipe B outperforms oracle-DOA parametric filtering on all tested patterns (26.3–26.8 vs ≤ 21.4 dB SDR).
- The Recipe B+ model's narrowband patterns are frequency-invariant.
- A speech-trained, anechoic-trained model generalizes to non-speech (music) sources and light reverberation (RT60 = 0.15 s), and follows per-period pattern changes in a time-varying demonstration scene.
- The pattern-space generalization of FiLM-JNF is what the comprehensive [[sources/huang-2026-neural-directional-filtering|journal-style NDF paper]] reuses for continuous steering (a single-angle pattern as a special case), and what [[concepts/film-osn|FiLM-OSN]] adopts for low-latency hearing-aid NDF with a 72-dimensional pattern vector.

## Related Concepts

- [[concepts/neural-directional-filtering|Neural Directional Filtering]]
- [[concepts/steerable-neural-directional-filtering|Steerable Neural Directional Filtering]]
- [[concepts/film-jnf|FiLM-JNF]]
- [[concepts/film-layer|FiLM Layer]]
- [[concepts/joint-nonlinear-filtering|Joint Nonlinear Filtering]]
- [[concepts/directivity-pattern|Directivity Pattern]]
- [[concepts/virtual-directional-microphone|Virtual Directional Microphone]]

## Related Sources

- [[sources/huang-2026-undf-configurable-directivity|Huang, Chetupalli & Habets 2026: UNDF — Configurable Directivity Pattern at Inference]] — the introducing paper
- [[sources/huang-2026-neural-directional-filtering|Huang et al. 2026: Neural Directional Filtering with a Compact Microphone Array]] — companion journal-style treatment using FiLM-JNF for continuous steering
- [[sources/uphaus-2026-directivity-low-latency|Uphaus et al. 2026: Directivity-Conditioned Low-Latency Neural Filtering]] — FiLM-pattern conditioning carried to the 10 ms-latency hearing-aid setting
