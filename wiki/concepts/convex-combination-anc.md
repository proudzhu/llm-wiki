---
type: concept
created: 2026-05-17
updated: 2026-05-17
tags:
  - active-noise-control
  - adaptive-filtering
  - convex-optimization
---

# Convex Combination ANC

## Overview

**Convex Combination ANC** uses a bank of two (or more) adaptive filters with different step sizes, combined via a mixing parameter, to achieve both fast convergence and low steady-state error — avoiding the trade-off inherent in fixed-step-size algorithms.

## Motivation

In [[concepts/filtered-x-lms-algorithm|FxLMS]] and related algorithms, the step size $\mu$ controls the convergence-speed / steady-state-error trade-off:
- Large $\mu$ → fast convergence → high residual noise
- Small $\mu$ → slow convergence → low residual noise

Convex combination runs both filters simultaneously and blends their outputs.

## Structure

Two adaptive filters operate in parallel:
- **Fast filter** ($\boldsymbol{w}_1$, large $\mu$, fast convergence, high noise residue)
- **Slow filter** ($\boldsymbol{w}_2$, small $\mu$, slow convergence, low noise residue)

Outputs are combined via mixing parameter $\lambda(n) \in [0, 1]$:

$$e(n) = \lambda(n) e_1(n) + [1-\lambda(n)] e_2(n)$$
$$y(n) = \lambda(n) y_1(n) + [1-\lambda(n)] y_2(n)$$

The mixing parameter is adapted via a sigmoid function $\lambda(n) = 1/(1+e^{-\varrho(n)})$, where $\varrho(n)$ is an internal parameter.

## Extensions

- **Multi-channel**: Applied to single and multi-channel ANC systems
- **Impulsive noise**: Convex combination of modified FxLMP algorithms for robust impulsive noise control
- **Nonlinear**: Convex combination of nonlinear adaptive filters (Part II)

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]

## Related Sources

- [[sources/lu-2021-survey-active-noise-control-linear|Lu et al. 2021: Survey on ANC — Part I: Linear Systems]]
