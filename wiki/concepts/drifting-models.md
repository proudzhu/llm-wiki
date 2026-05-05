---
type: concept
created: 2026-05-03
updated: 2026-05-03
sources:
  - raw/papers/xu-2026-drifting-models-speech-enhancement/full-text.md
tags:
  - generative-models
  - speech-enhancement
  - distribution-matching
  - one-step-inference
---

# Drifting Models

**Drifting Models** are a generative modeling paradigm that reformulates generation as a distributional equilibrium problem, achieving native one-step inference by evolving the pushforward distribution of a mapping function to match the target data distribution.

## Overview

Unlike diffusion models (which require iterative reverse-time sampling) or flow matching (which requires ODE discretization), Drifting Models directly learn a mapping $f_\theta$ whose pushforward distribution $q_\theta = (f_\theta)_\# p_\epsilon$ converges to the data distribution $p_{\text{data}}$ at equilibrium. The key mechanism is the **Drifting Field** — a learned correction vector that guides generated samples toward high-density regions of the target distribution.

Originally proposed by Deng et al. (2026) for large-scale image generation (FID 1.54 on ImageNet), the framework was adapted for speech enhancement by Xu et al. (2026) as DriftSE.

## Core Formulation

### Pushforward and Equilibrium

Given source distribution $p_\epsilon$ (e.g., standard Gaussian) and mapping $f_\theta$:

$$\mathbf{x} = f_\theta(\epsilon), \quad \epsilon \sim p_\epsilon$$

The pushforward distribution $q_\theta = (f_\theta)_\# p_\epsilon$ is driven toward $p_{\text{data}}$ until equilibrium:

$$q_\theta = p_{\text{data}} \quad \Longrightarrow \quad \mathbf{V}_{p,q}(\mathbf{x}) = \mathbf{0}, \; \forall \mathbf{x}$$

### Drifting Field

Inspired by mean-shift theory, the Drifting Field decomposes into attraction and repulsion:

$$\mathbf{V}_{p,q}(\mathbf{x}) = \mathbf{V}_p^+(\mathbf{x}) - \mathbf{V}_q^-(\mathbf{x})$$

which unifies into a single expectation:

$$\mathbf{V}_{p,q}(\mathbf{x}) = \frac{1}{Z_p Z_q} \mathbb{E}_{p,q}\left[k(\mathbf{x}, \mathbf{y}^+) k(\mathbf{x}, \mathbf{y}^-)(\mathbf{y}^+ - \mathbf{y}^-)\right]$$

where $\mathbf{y}^+ \sim p_{\text{data}}$ (positives), $\mathbf{y}^- \sim q_\theta$ (negatives), and $k_\tau(\mathbf{x}, \mathbf{y}) = \exp(-\|\mathbf{x} - \mathbf{y}\|_2 / \tau)$ is the exponential similarity kernel with temperature $\tau$.

### Training Objective

$$\mathcal{L}_{\text{drift}} = \mathbb{E}_\epsilon\left[\left\|\phi(\mathbf{x}) - \text{sg}\left(\phi(\mathbf{x}) + \mathbf{V}(\phi(\mathbf{x}))\right)\right\|_2^2\right]$$

where $\phi(\cdot)$ is a feature extractor and $\text{sg}(\cdot)$ is stop-gradient.

## Key Properties

1. **Native one-step inference**: No iterative sampling or trajectory discretization required (1 NFE)
2. **Unpaired training**: By matching distributions rather than paired samples, the framework can train without noisy-clean audio pairs
3. **Latent space operation**: The drifting field is computed in a semantic latent space (e.g., SSL features) for perceptually meaningful corrections
4. **Multi-layer supervision**: Aggregating drift across multiple encoder layers captures both low-level acoustic and high-level semantic structure

## Comparison with Related Paradigms

| Approach | Inference | Trajectory | Unpaired Training |
|----------|-----------|------------|-------------------|
| Diffusion Models | Iterative (10–100 NFE) | Reverse-time SDE/ODE | No |
| Consistency Models | 1-step (distilled) | Self-consistency along PF-ODE | No |
| Flow Matching | Iterative (few steps) | Straightened ODE | No |
| **Drifting Models** | **1-step (native)** | **None (equilibrium)** | **Yes** |

## Related Concepts

- [[../concepts/diffusion-models-for-speech|Diffusion Models for Speech Enhancement]]
- [[../concepts/one-step-generative-models|One-Step Generative Models]]
- [[../concepts/self-supervised-speech-representation|Self-Supervised Speech Representation]]

## Related Sources

- [[../sources/xu-2026-drifting-models-speech-enhancement|Xu et al. 2026: Speech Enhancement Based on Drifting Models]]
