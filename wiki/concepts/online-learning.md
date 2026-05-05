---
type: concept
created: 2026-05-03
updated: 2026-05-03
sources:
  - raw/papers/jin-2026-momentum-lms-nonstationarity/full-text.md
tags:
  - machine-learning
  - online-learning
  - adaptive-algorithms
  - streaming-data
---

# Online Learning

**Online Learning** is a paradigm where models are updated incrementally as each data sample arrives, eliminating the need to store or revisit past data. This enables single-pass processing over potentially unbounded data streams with computational and memory complexity independent of the stream length.

## Overview

In contrast to the offline-training–online-generalization paradigm, online learning processes each sample exactly once and updates model parameters on the fly. This is essential for applications driven by streaming data such as recommendation systems, credit scoring, sensor networks, and reinforcement learning.

## Key Algorithms

| Algorithm | Type | Key Feature |
|-----------|------|-------------|
| Perceptron | Linear classification | Foundational online method |
| Projected Online Gradient Descent | Convex optimization | Regret guarantees |
| Ader | Nonstationary convex | Meta-algorithm with multiple experts |
| LMS / NLMS | Adaptive filtering | Low complexity, real-time |
| [[momentum-lms|MLMS]] | Adaptive filtering with momentum | Faster tracking in nonstationary settings |
| RLS | Recursive least squares | Fast convergence, higher complexity |

## Nonstationarity Challenge

A fundamental challenge in online learning is that data distributions may drift over time and system parameters may evolve. This violates the classical i.i.d. assumption and necessitates algorithms that can:

1. **Track time-varying parameters** without expensive retraining
2. **Balance tracking speed vs. noise sensitivity** (the tracking–noise tradeoff)
3. **Maintain stability** under general data conditions (not just stationary/independent)

## Regret Analysis

Regret measures the cumulative loss of an online algorithm relative to a benchmark:

- **Static regret**: Comparison against the best fixed parameter
- **Dynamic regret**: Comparison against a sequence of time-varying optimal parameters

For [[momentum-lms|MLMS]] in time-varying linear systems, the averaged prediction regret approaches the irreducible noise floor $\sigma_v^2$ as the step-size $\mu \to 0$ when parameters are constant.

## Related Concepts

- [[../concepts/momentum-lms|Momentum LMS]]
- [[../concepts/adaptive-filtering|Adaptive Filtering]]
- [[../concepts/variable-step-size-lms|Variable Step Size LMS]]

## Related Sources

- [[../sources/jin-2026-momentum-lms-nonstationarity|Jin, Zheng & Guo 2026: Momentum LMS Theory beyond Stationarity]]
