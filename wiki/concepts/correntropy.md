---
type: concept
created: 2026-04-12
updated: 2026-04-17
sources:
  for active noise control.md
tags:
- information-theory
- signal-processing
- statistics
---

# Correntropy

**Correntropy** is a non-linear local similarity measure between two random variables, defined in a kernel space.

## Overview

Correntropy generalizes the concept of correlation by using a kernel function (typically a Gaussian kernel). While correlation only captures second-order statistics (linear relationship), correntropy captures all even-order statistics of the difference between variables.

For two random variables $X$ and $Y$, the correntropy is defined as:
$$ V(X,Y) = E[\kappa(X, Y)] $$
Where $\kappa$ is a Mercer kernel. For the standard **Gaussian kernel**:
$$ V_\sigma(X,Y) = E\left[\frac{1}{\sqrt{2\pi}\sigma} \exp\left(-\frac{(X-Y)^2}{2\sigma^2}\right)\right] $$

## Key Properties

1. **Local Measure**: Correntropy is highly sensitive to the values of $X$ and $Y$ when they are close to each other (controlled by the kernel bandwidth $\sigma$). As the difference $|X-Y|$ increases, the correntropy decays exponentially to zero.
2. **Robustness**: Because it ignores large differences (outliers), correntropy-based optimization is inherently robust to impulsive noise and non-Gaussian disturbances.
3. **Relation to Correlation**: If the Gaussian kernel bandwidth $\sigma$ is very large, correntropy approaches the standard correlation (second-order statistic).
4. **Information Theoretic Connection**: Correntropy is related to **Rényi's Quadratic Entropy** of the error, providing a bridge between signal processing and information theory (Information Theoretic Learning).

## Extensions

- **[[generalized-correntropy|Generalized Correntropy]]**: Replaces the Gaussian kernel with a **Generalized Gaussian Distribution (GGD)** kernel, providing a shape parameter $p$ to control the "heaviness" of the error suppression (Chen 2016).

## Applications in ANC

In [[active-noise-control|Active Noise Control]], correntropy is used to develop robust alternatives to the [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] (FxLMS). By maximizing correntropy (the [[maximum-correntropy-criterion|Maximum Correntropy Criterion]]), the system becomes immune to large "spikes" in the error signal caused by impulsive noise.

## Related Concepts

- [[maximum-correntropy-criterion|Maximum Correntropy Criterion]]
- [[generalized-correntropy|Generalized Correntropy]]
- [[information-theoretic-learning|Information Theoretic Learning]]
- [[robust-adaptive-filtering|Robust Adaptive Filtering]]
- [[impulsive-noise|Impulsive Noise]]
- [[active-noise-control|Active Noise Control]]
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]

## Related Sources

- [[sources/chen-2016-generalized-correntropy-robust-adaptive-filtering|Chen 2016: Generalized Correntropy for Robust Adaptive Filtering]]
- [[sources/zhu-2020-robust-gmcc-anc-paper-reading-note|Zhu 2020: Robust GMCC for ANC Paper Reading Note]]
