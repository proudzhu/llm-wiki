---
type: concept
created: 2026-04-12
updated: 2026-04-17
sources:
  for active noise control.md
tags:
- robust-control
- signal-processing
---

# Robust Adaptive Filtering

**Robust Adaptive Filtering** refers to the design of adaptive algorithms that maintain stability and performance in the presence of non-Gaussian disturbances, such as **[[impulsive-noise|Impulsive Noise]]** or outliers.

## Overview

Traditional adaptive filters (like LMS and RLS) are based on minimizing the Mean Square Error (MSE). While optimal for Gaussian noise, they perform poorly when the noise has heavy tails, as the squaring operation in the cost function over-amplifies large outliers. Robust filtering replaces the MSE with cost functions that are less sensitive to large errors.

## Core Approaches

### 1. Robust Cost Functions
Replacing $e^2(n)$ with a function that grows slower than quadratic:
- **Least Mean P-power (LMP)**: Minimizes $|e(n)|^p$ where $1 \leq p < 2$.
- **Logarithmic Cost**: Minimizes $\log(1 + e^2/2\sigma^2)$.
- **[[maximum-correntropy-criterion|Maximum Correntropy Criterion]] (MCC)**: Maximizes a kernel-based similarity measure. The gradient (score function) decays to zero for large errors.

### 2. Signal Pre-processing
Applying nonlinearities to the input or error signals before they reach the adaptation logic:
- **Clipping/Saturation**: Hard-limiting the signal amplitude.
- **Median Filtering**: Removing impulsive spikes using a sliding window median.

### 3. Variable Step Size (VSS)
Automatically reducing the step size $\mu$ when a large error is detected, assuming it's an outlier.

## Comparison of Score Functions

The **score function** $f(e)$ determines the weight update in the form: $w(n+1) = w(n) + \mu f(e) x(n)$.

| Algorithm | Score Function $f(e)$ | Behavior for Large $e$ |
|-----------|----------------------|-----------------------|
| **LMS** | $e$ | Linear growth (unstable) |
| **LMP** | $|e|^{p-1} \text{sign}(e)$ | Power-law growth |
| **MCC** | $\exp(-e^2/2\sigma^2)e$ | **Exponential decay to zero** |
| **GMCC** | $\exp(-\lambda|e|^\alpha)|e|^{\alpha-1} \text{sign}(e)$ | **Exponential decay to zero** |

## Zero Probability of Divergence (POD)

A key goal in robust filtering is achieving **Zero POD**. This means that no matter how large an impulsive spike is, the algorithm is guaranteed not to diverge. Chen et al. (2016) proved that algorithms based on [[generalized-maximum-correntropy-criterion|Generalized Maximum Correntropy Criterion]] (GMCC) can achieve this property because their score functions vanish at infinity.

## Related Concepts

- [[impulsive-noise|Impulsive Noise]]
- [[maximum-correntropy-criterion|Maximum Correntropy Criterion]]
- [[generalized-maximum-correntropy-criterion|Generalized Maximum Correntropy Criterion]]
- [[synthesis/impulsive-noise-control|Robust ANC for Impulsive and Non-Gaussian Noise]]
- [[correntropy|Correntropy]]
- [[information-theoretic-learning|Information Theoretic Learning]]

## Related Sources

- [[sources/chen-2016-generalized-correntropy-robust-adaptive-filtering|Chen 2016: Generalized Correntropy for Robust Adaptive Filtering]]
- [[sources/zhu-2020-robust-gmcc-anc-paper-reading-note|Zhu 2020: Robust GMCC for ANC Paper Reading Note]]
