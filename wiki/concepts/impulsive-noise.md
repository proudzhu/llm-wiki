---
type: concept
created: 2026-04-12
updated: 2026-04-17
sources:
  for active noise control.md
tags:
- active-noise-control
- robust-control
- signal-processing
---

# Impulsive Noise

**Impulsive Noise** is a type of non-Gaussian noise characterized by short-duration, high-amplitude bursts or "spikes" that deviate significantly from the background signal.

## Overview

In statistical signal processing, impulsive noise is often modeled using heavy-tailed distributions such as the **$\alpha$-Stable Distribution** or the **Generalized Gaussian Distribution (GGD)** with a shape parameter $p < 2$. Examples in the real world include:
- Acoustic "pops" and clicks in audio.
- Engine ignition noise.
- Electrical switching transients.
- Traction substation noise in railways (Zhu 2020).

## Impact on Adaptive Filtering

The standard [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] (FxLMS) is based on the **Minimum Mean Square Error (MMSE)** criterion, which assumes Gaussian noise. When impulsive noise is present:
1. **Stability Issues**: Large error spikes result in massive weight updates, causing the algorithm to diverge.
2. **Performance Degradation**: The $L_2$ norm (squaring the error) over-weights large outliers, biasing the solution.

## Robust Solutions

To handle impulsive noise, the quadratic cost function must be replaced with a **robust cost function** that suppresses large errors.

### 1. Maximum Correntropy Criterion (MCC)
Uses a Gaussian kernel to measure similarity. The "score function" (gradient) of MCC decays exponentially for large errors, effectively "ignoring" outliers.
$$ f(e) = \exp\left(-\frac{e^2}{2\sigma^2}\right) e $$

### 2. Generalized Maximum Correntropy Criterion (GMCC)
Uses a **GGD kernel** with a shape parameter $p$. This provides more flexibility than standard MCC and can be tuned to the specific "heaviness" of the noise tails (Chen 2016).
- **IFxGMCC**: An improved version that uses a continuous mixed $L_p$ norm to avoid manual tuning of the $p$ parameter (Zhu 2020).

### 3. FxLMP (Filtered-x Least Mean P-power)
Uses the $L_p$ norm ($p < 2$) instead of $L_2$. While more robust than LMS, it can still diverge if $p$ is not chosen correctly for the noise type.

### 4. Nonlinear Clipping/Saturation
Simple methods that "clip" the error signal or the reference signal before adaptation. While easy to implement, they introduce harmonic distortion and may not be optimal.

## Comparison of Robustness

| Algorithm | Error Norm | Large Error Behavior | Stability under Impulses |
|-----------|------------|---------------------|--------------------------|
| **FxLMS** | $L_2$ (Quadratic) | Linear growth | Poor |
| **FxLMP** | $L_p$ (Power) | Power-law growth | Fair |
| **FxMCC** | Gaussian Kernel | **Exponential decay to zero** | Good |
| **FxGMCC**| GGD Kernel | **Exponential decay to zero** | Excellent |

## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[generalized-gaussian-distribution|Generalized Gaussian Distribution]]
- [[maximum-correntropy-criterion|Maximum Correntropy Criterion]]
- [[generalized-maximum-correntropy-criterion|Generalized Maximum Correntropy Criterion]]
- [[robust-adaptive-filtering|Robust Adaptive Filtering]]
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]

## Related Sources

- [[sources/chen-2016-generalized-correntropy-robust-adaptive-filtering|Chen 2016: Generalized Correntropy for Robust Adaptive Filtering]]
- [[sources/zhu-2020-robust-gmcc-anc-paper-reading-note|Zhu 2020: Robust GMCC for ANC Paper Reading Note]]
- [[sources/lu-2021-survey-active-noise-control-linear|Lu et al. 2021: Survey on ANC — Part I: Linear Systems]]
