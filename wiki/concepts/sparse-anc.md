---
type: concept
created: 2026-05-17
updated: 2026-05-17
tags:
  - active-noise-control
  - adaptive-filtering
  - sparsity
---

# Sparse ANC

## Overview

**Sparse ANC** algorithms exploit sparsity in [[concepts/active-noise-control|Active Noise Control]] systems to improve convergence speed and reduce computational complexity. Sparsity can exist in the primary path, secondary path, or the noise source itself.

## Types of Sparsity

1. **Path sparsity**: The impulse response of the primary or secondary path has many near-zero coefficients
2. **Source sparsity**: The noise source is sparsely distributed in space or frequency

## Key Algorithms

### FxIPNLMS (Filtered-x Improved Proportionate NLMS)

The **Improved Proportionate NLMS** assigns larger step sizes to larger filter coefficients, accelerating convergence for sparse paths. Compatible with convex combination schemes for Gaussian noise.

### Zero-Attracting (ZA) and Reweighted ZA Strategies

Add sparsity-promoting penalties to the FxLMS cost function:
- **ZA-FxLMS**: $L_1$ regularization encourages zero coefficients
- **RZA-FxLMS**: Reweighted zero-attracting for stronger sparsity induction

Applied to both path-sparse and source-sparse scenarios.

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/convex-combination-anc|Convex Combination ANC]]

## Related Sources

- [[sources/lu-2021-survey-active-noise-control-linear|Lu et al. 2021: Survey on ANC — Part I: Linear Systems]]
