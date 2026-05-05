---
type: concept
created: 2026-05-03
updated: 2026-05-03
sources:
  - raw/papers/xu-2026-drifting-models-speech-enhancement/full-text.md
tags:
  - speech-enhancement
  - generative-models
  - diffusion-models
---

# Diffusion Models for Speech Enhancement

**Diffusion models for speech enhancement** apply score-based generative modeling to the denoising problem, defining a forward process that gradually corrupts clean speech into noise and a reverse process that recovers clean speech from noisy observations.

## Overview

Score-based diffusion models have established state-of-the-art performance in speech enhancement by modeling the gradient of the log-density of the clean speech distribution. The reverse dynamics can be formulated as either a Stochastic Differential Equation (SDE) or a deterministic Probability Flow ODE (PF-ODE) sharing the same marginal densities.

However, their inference is inherently iterative — numerically integrating the reverse-time trajectories requires 10–100 discretization steps, resulting in a high Number of Function Evaluations (NFE) that creates a latency bottleneck for real-time applications.

## Acceleration Strategies

### Trajectory Compression
- **Hybrid approaches**: Combine predictive models with a small number of diffusion refinement steps (e.g., Storm, Trachu et al.)
- **Diffusion-GAN hybrids**: Further reduce steps via adversarial training
- **Consistency Models**: Enforce self-consistency along the PF-ODE to distill a multi-step sampler into a single-step mapping (ROSE-CD, SBCTM)

### Trajectory Linearization
- **Flow Matching**: Learn a vector field that defines a probability path from noise to data
- **Rectified Flow**: Explicitly straightens the transport path to minimize ODE curvature
- **MeanFlow**: Learns a continuous mean velocity field to model probability paths

### Beyond Trajectories
- **[[drifting-models|Drifting Models]]**: Reformulate generation as a distributional equilibrium problem, achieving native one-step inference without any trajectory (DriftSE)

## Representative Methods on VoiceBank-DEMAND

| Method | NFE | PESQ | SI-SDR | Approach |
|--------|-----|------|--------|----------|
| SGMSE+ | 30 | 2.90 | 16.90 | Score-based diffusion |
| ROSE-CD | 1 | 3.49 | 17.80 | Consistency distillation |
| SBCTM | 1 | 3.56 | 12.70 | Schrödinger bridge + consistency |
| MeanFlowSE | 1 | 2.81 | 19.97 | Mean flow |
| DriftSE | 1 | 3.15 | 16.10 | Drifting models (equilibrium) |

## Related Concepts

- [[../concepts/drifting-models|Drifting Models]]
- [[../concepts/one-step-generative-models|One-Step Generative Models]]
- [[../concepts/self-supervised-speech-representation|Self-Supervised Speech Representation]]

## Related Sources

- [[../sources/xu-2026-drifting-models-speech-enhancement|Xu et al. 2026: Speech Enhancement Based on Drifting Models]]
