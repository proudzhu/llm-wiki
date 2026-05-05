---
type: concept
created: 2026-05-04
updated: 2026-05-04
sources:
  - raw/papers/yang-2026-transformer-e2e-cfg-anc/full-text.md
tags:
  - active-noise-control
  - deep-learning
  - differentiable-programming
  - unsupervised-learning
---

# End-to-End Differentiable ANC

**End-to-End Differentiable ANC** is a training paradigm where the neural network co-processor and the physical ANC forward path are integrated into a single differentiable computational graph, enabling gradient-based optimization directly from the residual noise objective without labeled target filters.

## Overview

Traditional neural-network-based ANC methods train the co-processor in a supervised manner, requiring labeled target filters or noise profiles. End-to-end differentiable ANC eliminates this requirement by making the entire signal path — from reference signal through control filter generation to residual error — differentiable.

The key insight is that the mapping from input frame to residual error is fully differentiable:

$$\mathbf{x}_f \rightarrow \mathbf{w} \rightarrow y(n) \rightarrow e(n) \rightarrow \mathcal{L}$$

Since each step is a differentiable operation (neural network inference, linear convolution, subtraction), the network parameters can be updated by backpropagation:

$$\theta \leftarrow \theta - \eta \nabla_\theta \mathcal{L}$$

## Training Objective

The unsupervised loss is defined directly from the residual error after cancellation:

$$\mathcal{L} = \frac{1}{T} \sum_{n=0}^{T-1} \alpha_n e^2(n)$$

where $e(n) = d(n) - \sum_{k=0}^{N-1} w_k x'(n-k)$ is the residual error, $x'(n) = x(n) * \hat{s}(n)$ is the filtered reference signal, and $\alpha_n$ is an optional weighting coefficient (e.g., forgetting-factor scheme with $\lambda = 0.999$).

## Key Properties

- **No labeled data required**: The training signal is the residual noise itself, which is always available during ANC operation
- **Physically aligned objective**: Minimizing residual error is exactly the goal of ANC, so the network is optimized for the true physical objective
- **Differentiable secondary path**: The estimated secondary-path impulse response $\hat{s}(n)$ is incorporated as a fixed linear layer in the computational graph
- **Frame-wise training, sample-wise inference**: The co-processor operates at frame rate during both training and inference, while the ANC controller operates at sampling rate

## Applications

### Unsupervised GFANC (Luo et al. 2024, ICASSP)
CNN co-processor generates combination weights for sub-filter recombination within a differentiable ANC system.

### E2E-CFG (Yang et al. 2026)
Transformer co-processor directly generates full control-filter coefficients within a differentiable ANC system, removing the decomposition-recombination stage.

## Related Concepts

- [[../concepts/generative-fixed-filter-anc|Generative Fixed-Filter ANC]] — GFANC methods using this training paradigm
- [[../concepts/active-noise-control|Active Noise Control]] — parent domain
- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — traditional adaptive alternative

## Related Sources

- [[../sources/yang-2026-transformer-e2e-cfg-anc|Yang 2026: Transformer-based E2E-CFG for ANC]] — direct filter generation in differentiable ANC
- [[../sources/luo-2026-hybrid-gfanc-fxnlms|Luo 2026: Hybrid GFANC-FxNLMS]] — unsupervised GFANC with differentiable training
