---
type: concept
created: 2026-05-03
updated: 2026-05-03
sources:
  - raw/papers/xu-2026-drifting-models-speech-enhancement/full-text.md
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

## Related Sources

- [[sources/xu-2026-drifting-models-speech-enhancement|Xu et al. 2026: Speech Enhancement Based on Drifting Models]]
