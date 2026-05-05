---
type: concept
created: 2026-05-04
updated: 2026-05-04
sources:
  - raw/papers/yang-2026-transformer-e2e-cfg-anc/full-text.md
  - raw/papers/luo-2026-hybrid-gfanc-fxnlms/full-text.md
tags:
  - active-noise-control
  - fixed-filter-anc
  - deep-learning
  - generative-model
---

# Generative Fixed-Filter ANC

**Generative Fixed-Filter ANC (GFANC)** is an ANC strategy that uses a neural network co-processor to generate custom control filters in real time, rather than selecting from a pre-trained discrete library as in [[selective-fixed-filter-anc|SFANC]]. The generated filter is a combination of sub-control filters weighted by the co-processor's output.

## Overview

SFANC selects one filter from a discrete library, which may be insufficient when the incoming noise differs substantially from the design conditions. GFANC addresses this by generating a more suitable control filter through **sub-filter decomposition and recombination**:

1. A wideband pre-trained control filter is partitioned into $M$ sub-filters (e.g., via uniform frequency-domain partitioning)
2. A CNN co-processor processes the reference signal and predicts $M$ combination weights
3. The final control filter is the weighted sum of sub-filters: $\mathbf{w} = \sum_{m=1}^{M} g_m \mathbf{w}_m$

This enables finer-grained adaptation than discrete selection while maintaining the instant-response advantage of fixed-filter ANC.

## Evolution of GFANC

### Supervised GFANC (Luo et al. 2024)
The original GFANC framework trains the co-processor in a **supervised** manner, requiring labeled target filters. Temporal smoothing via Bayesian or Kalman filtering enhances robustness under dynamic noise conditions.

### Unsupervised GFANC (Luo et al. 2024, ICASSP)
Integrates the co-processor and real-time controller into a **differentiable ANC system**. The accumulated squared error serves directly as the training objective, eliminating the need for labeled data while remaining aligned with the physical objective of noise cancellation.

### End-to-End CFG (E2E-CFG) (Yang et al. 2026)
Replaces the decomposition-recombination paradigm with **direct control-filter generation**. A Transformer-based co-processor outputs the full $N$-dimensional filter coefficient vector, removing dependence on intermediate sub-filter representations. Trained unsupervised using the same differentiable ANC framework.

## Comparison: SFANC vs. GFANC vs. E2E-CFG

| Aspect | SFANC | GFANC | E2E-CFG |
|--------|-------|-------|---------|
| Filter source | Pre-trained library | Generated from sub-filters | Directly generated |
| Output | Index selection | $M$ combination weights | $N$ filter coefficients |
| Adaptation granularity | Discrete | Continuous (weighted sum) | Continuous (full filter) |
| Error accumulation | No | Yes (through recombination) | No |
| Training | Classification | Supervised / Unsupervised | Unsupervised |
| Co-processor | CNN classifier | CNN weight predictor | Transformer filter generator |

## Key Formulations

### Sub-filter recombination (GFANC)
$$\mathbf{w} = \sum_{m=1}^{M} g_m \mathbf{w}_m, \quad g_m = \sigma(\text{CNN}(\mathbf{x}_f))_m$$

### Direct filter generation (E2E-CFG)
$$\mathbf{w} = \mathcal{F}_\theta(\mathbf{x}_f) \in \mathbb{R}^N$$

### Unsupervised training objective
$$\mathcal{L} = \frac{1}{T} \sum_{n=0}^{T-1} \alpha_n e^2(n)$$

where $\alpha_n$ follows a forgetting-factor scheme ($\lambda = 0.999$).

## Related Concepts

- [[../concepts/selective-fixed-filter-anc|Selective Fixed-Filter ANC]] — predecessor: discrete filter selection
- [[../concepts/active-noise-control|Active Noise Control]] — parent domain
- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — adaptive alternative
- [[../concepts/end-to-end-differentiable-anc|End-to-End Differentiable ANC]] — training paradigm for unsupervised GFANC and E2E-CFG

## Related Sources

- [[../sources/yang-2026-transformer-e2e-cfg-anc|Yang 2026: Transformer-based E2E-CFG for ANC]] — direct filter generation with Transformer co-processor
- [[../sources/luo-2026-hybrid-gfanc-fxnlms|Luo 2026: Hybrid GFANC-FxNLMS]] — unsupervised GFANC with CNN co-processor and hybrid stabilization
