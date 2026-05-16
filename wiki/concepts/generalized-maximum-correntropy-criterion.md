---
type: concept
created: 2026-04-12
updated: 2026-04-17
sources:
  for active noise control.md
tags:
- optimization
- robust-control
- signal-processing
---

# Generalized Maximum Correntropy Criterion

**Generalized Maximum Correntropy Criterion (GMCC)** is an optimization framework that generalizes the [[maximum-correntropy-criterion|Maximum Correntropy Criterion]] (MCC) by using a **[[generalized-gaussian-distribution|Generalized Gaussian Distribution]] (GGD)** kernel.

## Overview

Proposed by Chen et al. (2016), GMCC provides a more flexible robust filtering framework than standard MCC. By adjusting the kernel's shape parameter $\alpha$, the algorithm can be tailored to the specific statistics of non-Gaussian noise (e.g., impulsive noise).

## Mathematical Formulation

The GMCC objective is to maximize the generalized correntropy:
$$ J_{GMCC} = E\left[\gamma_{\alpha, \beta} \exp(-\lambda |e(n)|^\alpha)\right] $$
Where $e(n)$ is the error.

### Gradient Descent Algorithm
The resulting weight update rule for an adaptive filter is:
$$ w(n+1) = w(n) + \mu \exp(-\lambda |e(n)|^\alpha) |e(n)|^{\alpha-1} \text{sign}(e(n)) x(n) $$
This can be viewed as an **Adaptive Filter with a Variable Step Size**, where the step size decays exponentially for large errors.

## Advantages

1. **Robustness to Impulsive Noise**: Like MCC, GMCC suppresses large outliers. However, the $\alpha$ parameter allows for finer control over the suppression behavior.
2. **Zero Probability of Divergence (POD)**: The algorithm is theoretically guaranteed to remain stable even under extreme impulsive noise spikes because the update vanishes as the error grows.
3. **Versatility**: GMCC encompasses several standard algorithms as limiting cases, including LMS ($\alpha=2, \lambda \to 0$) and the Sign Algorithm ($\alpha=1$).

## Advanced Variations in ANC

In [[active-noise-control|Active Noise Control]], several advanced versions of GMCC have been developed to handle complex noise (Zhu 2020):
- **FxGMCC**: The Filtered-x version of GMCC.
- **IFxGMCC**: Uses a continuous mixed $L_p$ norm to eliminate the need for manual tuning of $\alpha$.
- **C-IFxGMCC**: A **convex combination** of two IFxGMCC filters (one with a large step size for fast convergence, one with a small step size for low steady-state error).

## Related Concepts

- [[generalized-correntropy|Generalized Correntropy]]
- [[maximum-correntropy-criterion|Maximum Correntropy Criterion]]
- [[generalized-gaussian-distribution|Generalized Gaussian Distribution]]
- [[impulsive-noise|Impulsive Noise]]
- [[robust-adaptive-filtering|Robust Adaptive Filtering]]
- [[active-noise-control|Active Noise Control]]

## Related Sources

- [[sources/chen-2016-generalized-correntropy-robust-adaptive-filtering|Chen 2016: Generalized Correntropy for Robust Adaptive Filtering]]
- [[sources/zhu-2020-robust-gmcc-anc-paper-reading-note|Zhu 2020: Robust GMCC for ANC Paper Reading Note]]
