---
type: concept
created: 2026-05-03
updated: 2026-09-03
sources:
  - raw/papers/xu-2026-drifting-models-speech-enhancement/full-text.md
  - raw/papers/shetu-2026-generative-discriminative-comparison/full-text.md
tags:
  - generative-models
  - speech-enhancement
  - one-step-inference
---

# One-Step Generative Models

**One-step generative models** produce outputs in a single function evaluation (1 NFE), eliminating the iterative sampling required by standard diffusion models. This is critical for real-time applications such as speech enhancement where latency is a constraint.

## Overview

Standard diffusion models require 10–100 reverse-time steps to generate high-quality samples. One-step methods aim to achieve comparable quality with a single forward pass through the generator network.

## Approaches to One-Step Generation

### Distillation Methods
Train a student model to mimic the output of a multi-step teacher:
- **Consistency Models**: Enforce self-consistency along the probability flow ODE — any point on the same trajectory maps to the same endpoint
- **ROSE-CD**: Consistency distillation applied to speech enhancement
- **SBCTM**: Schrödinger bridge combined with consistency training

### Native One-Step Methods
Designed for one-step inference from the outset, without requiring a multi-step teacher:
- **GANs**: Single-step generation via adversarial training, but suffer from training instability and mode collapse
- **[[drifting-models|Drifting Models]]**: Achieve one-step inference by evolving the pushforward distribution to equilibrium — no trajectory, no distillation required

### Flow-Based Methods (Few-Step)
Reduce steps by straightening the generative trajectory:
- **Rectified Flow**: Straightens ODE paths for fewer discretization steps
- **MeanFlow**: Learns a mean velocity field for efficient probability transport

## Empirical Validation for SE (Shetu 2026)

[[sources/shetu-2026-generative-discriminative-comparison|Shetu, Habets & Brendel 2026]] provide controlled evidence that one-step generation is not just a latency convenience but a *quality-neutral or superior* choice for speech enhancement: the NCSN++ backbone trained with a GAN objective (single NFE) beats the same backbone trained as an iterative diffusion model on PESQ/SI-SDR/FwSegSNR under matched and mismatched low-SNR conditions, at 60–100× lower GMACs, with faster convergence (~250k vs ~400k steps) and far better data efficiency (peak quality at 50 h vs ≥200 h of training data). The consistency-model route to one-step inference (SEBridge) still lags its GAN counterpart, and few-step flow matching (FlowSE) retains the costly backbone — the one-step *training objective*, not merely the reduced NFE, drives the gain. Details in [[concepts/generative-vs-discriminative-speech-enhancement|Generative vs. Discriminative Speech Enhancement]].

## Trade-offs

| Method | NFE | Training Complexity | Fidelity | Perceptual Quality |
|--------|-----|-------------------|----------|-------------------|
| GANs | 1 | Unstable | Moderate | Good |
| Consistency Models | 1 | Requires teacher | High | Good |
| Drifting Models | 1 | Self-contained | High | High |
| Flow Matching | 1–4 | Moderate | High | High |
| Diffusion | 10–100 | Stable | Highest | Highest |

## Related Concepts

- [[concepts/drifting-models|Drifting Models]]
- [[concepts/diffusion-models-for-speech|Diffusion Models for Speech Enhancement]]
- [[concepts/generative-vs-discriminative-speech-enhancement|Generative vs. Discriminative Speech Enhancement]]

## Related Sources

- [[sources/xu-2026-drifting-models-speech-enhancement|Xu et al. 2026: Speech Enhancement Based on Drifting Models]]
- [[sources/shetu-2026-generative-discriminative-comparison|Shetu, Habets & Brendel 2026: Generative vs. Discriminative SE]] — empirical validation that one-step GAN training matches or beats iterative diffusion for SE
