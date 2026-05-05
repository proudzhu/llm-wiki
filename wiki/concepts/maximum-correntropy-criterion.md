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

# Maximum Correntropy Criterion

**Maximum Correntropy Criterion (MCC)** is an optimization principle that maximizes the correntropy between a desired signal and the output of a system.

## Overview

In adaptive filtering, the MCC is used as a robust alternative to the standard **Minimum Mean Square Error (MMSE)**. While MMSE minimizes the $L_2$ norm of the error, MCC maximizes the average value of a Gaussian kernel applied to the error:
$$ J_{MCC} = E\left[\exp\left(-\frac{e^2(n)}{2\sigma^2}\right)\right] $$

## Why MCC is Robust

The gradient of the MCC cost function (the **score function**) is:
$$ \frac{\partial J_{MCC}}{\partial w} \propto \exp\left(-\frac{e^2(n)}{2\sigma^2}\right) e(n) x(n) $$
When the error $|e(n)|$ is very large (e.g., during an impulsive noise spike), the exponential term $\exp(-e^2/2\sigma^2)$ tends to zero. This effectively "shuts down" the weight update for that sample, preventing the outlier from destabilizing the filter.

## Comparison with LMS

| Feature | LMS (MMSE) | MCC |
|---------|------------|-----|
| **Cost Function** | $E[e^2(n)]$ | $E[\exp(-e^2/2\sigma^2)]$ |
| **Error Weighting** | Linear (Large $e$ → Large update) | **Exponential decay** (Large $e$ → Zero update) |
| **Noise Assumption** | Gaussian | Non-Gaussian / Impulsive |
| **Key Parameter** | Step size $\mu$ | Step size $\mu$ + Kernel bandwidth $\sigma$ |

## Limiting Behaviors

1. **Wiener Solution**: As the kernel bandwidth $\sigma \to \infty$, MCC approaches the standard MMSE/Wiener solution.
2. **MAP Estimator**: As $\sigma \to 0$, the MCC solution approaches the Maximum A Posteriori (MAP) estimate of the system parameters.

## Extensions

- **[[generalized-maximum-correntropy-criterion|Generalized Maximum Correntropy Criterion]] (GMCC)**: Replaces the Gaussian kernel with a Generalized Gaussian Distribution (GGD) kernel to handle a wider variety of noise distributions (Chen 2016, Zhu 2020).
- **FxMCC**: The application of MCC to [[active-noise-control|Active Noise Control]] systems using the Filtered-x structure.

## Related Concepts

- [[correntropy|Correntropy]]
- [[generalized-maximum-correntropy-criterion|Generalized Maximum Correntropy Criterion]]
- [[robust-adaptive-filtering|Robust Adaptive Filtering]]
- [[impulsive-noise|Impulsive Noise]]
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[active-noise-control|Active Noise Control]]

## Related Sources

- [[../sources/chen-2016-generalized-correntropy-robust-adaptive-filtering|Chen 2016: Generalized Correntropy for Robust Adaptive Filtering]]
- [[../sources/zhu-2020-robust-gmcc-anc-paper-reading-note|Zhu 2020: Robust GMCC for ANC Paper Reading Note]]
