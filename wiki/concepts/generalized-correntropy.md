---
type: concept
created: 2026-04-12
updated: 2026-04-17
sources:
  for active noise control.md
tags:
- information-theory
- signal-processing
---

# Generalized Correntropy

**Generalized Correntropy** is an extension of [[correntropy|Correntropy]] that uses the **Generalized Gaussian Distribution (GGD)** as the kernel function instead of a standard Gaussian kernel.

## Overview

Proposed by Chen et al. (2016), generalized correntropy provides a shape parameter $\alpha$ that allows the metric to be tuned for different types of non-Gaussian noise. It is defined as:
$$ V_{\alpha, \beta}(X, Y) = E\left[\gamma_{\alpha, \beta} \exp(-\lambda |X-Y|^\alpha)\right] $$
Where:
- **$\alpha > 0$**: The shape parameter.
- **$\beta > 0$**: The scale (bandwidth) parameter.
- **$\lambda = 1/\beta^\alpha$**: The kernel parameter.
- **$\gamma_{\alpha, \beta}$**: Normalization constant.

## Why "Generalized"?

By adjusting the shape parameter $\alpha$, the kernel can mimic various standard distributions and their corresponding error norms:
- **$\alpha = 2$**: Standard Gaussian kernel (equivalent to standard [[correntropy|Correntropy]]).
- **$\alpha = 1$**: Laplace kernel (related to $L_1$ norm/robust statistics).
- **$\alpha \to \infty$**: Uniform distribution kernel.
- **$\alpha \to 0$**: Related to $L_0$ norm minimization (useful for sparsity).

## Advantages over Standard Correntropy

1. **Flexibility**: The shape parameter $\alpha$ allows the suppression of large errors to be tuned. For example, $\alpha < 2$ results in heavier tails, providing better robustness against extremely large impulsive spikes (Zhu 2020).
2. **Probability of Divergence (POD)**: Algorithms based on generalized correntropy (like GMCC) can be shown to have zero POD, meaning they are theoretically guaranteed not to diverge even under heavy impulsive noise.
3. **Control over Nonlinearity**: The "score function" (gradient) can be specifically designed to match the statistics of the noise environment.

## Applications in ANC

In [[active-noise-control|Active Noise Control]], generalized correntropy leads to the **FxGMCC** algorithm, which is superior to both FxLMS and standard FxMCC in handling complex, non-Gaussian noise sources like traction substations or mixed impulsive/sinusoidal noise.

## Related Concepts

- [[correntropy|Correntropy]]
- [[generalized-maximum-correntropy-criterion|Generalized Maximum Correntropy Criterion]]
- [[generalized-gaussian-distribution|Generalized Gaussian Distribution]]
- [[maximum-correntropy-criterion|Maximum Correntropy Criterion]]
- [[robust-adaptive-filtering|Robust Adaptive Filtering]]
- [[active-noise-control|Active Noise Control]]

## Related Sources

- [[sources/chen-2016-generalized-correntropy-robust-adaptive-filtering|Chen 2016: Generalized Correntropy for Robust Adaptive Filtering]]
- [[sources/zhu-2020-robust-gmcc-anc-paper-reading-note|Zhu 2020: Robust GMCC for ANC Paper Reading Note]]
