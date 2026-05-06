---
type: concept
created: 2026-04-10
updated: 2026-04-10
sources:
tags:
- adaptive-algorithms
- lms
- signal-processing
---

# Filtered-x LMS Algorithm

## Overview

The **Filtered-x Least Mean Square (FxLMS)** algorithm is the most widely used adaptive algorithm in [[active-noise-control|Active Noise Control]] systems. It is a variant of the standard LMS algorithm that accounts for the **secondary path** between the controller output and the error sensor.

## Why "Filtered-x"?

In standard LMS, the weight update is:

```
w(n+1) = w(n) + μ · e(n) · x(n)
```

In ANC, the error signal is affected by the secondary path S(z). The FxLMS algorithm accounts for this by filtering the reference signal x(n) through an **estimate of the secondary path** Ŝ(z) before using it in the weight update:

```
x_f(n) = Ŝ(z) * x(n)    (convolution)
w(n+1) = w(n) + μ · e(n) · x_f(n)
```

## Key Parameters

| Parameter | Description |
|-----------|-------------|
| **μ (step size)** | Controls convergence speed and stability; larger = faster but less stable |
| **Ŝ(z)** | Estimated secondary path response (typically an FIR filter with hundreds or thousands of coefficients) |
| **Filter length** | Number of taps in the adaptive filter; more taps = better performance but higher computation |

## Computational Burden

The FxLMS algorithm requires a **convolution operation** to filter the reference signal through Ŝ(z). When Ŝ(z) has hundreds or thousands of coefficients, this becomes a heavy burden for real-time controllers — especially in multi-channel ANC systems. This computational burden motivated the [[simplified-adaptive-feedback-anc|Simplified Adaptive Feedback ANC]] approach.

## Stability Condition

For stability, the phase difference between the true secondary path and its estimation must be within π/2 radians:

```
|∠S(e^jω) - ∠Ŝ(e^jω)| < π/2,  ∀ω
```

For MIMO systems, a sufficient stability criterion is:

$$\Re\left\{\text{eig}\left[\hat{\mathbf{G}}^H(\omega)\mathbf{G}(\omega)\right]\right\} > 0 \quad \forall\omega$$

where $\mathbf{G}(\omega)$ and $\hat{\mathbf{G}}(\omega)$ are the Fourier transforms of the actual and estimated secondary paths. This underlines the need for accurate secondary path estimates — approaches like [[secondary-path-interpolation|Secondary Path Interpolation]] via [[dynamic-time-warping|DTW]] can extend the stable frequency range by improving phase accuracy of interpolated paths.

## Variants

- [[leaky-fxlms-algorithm|Leaky FxLMS Algorithm]] — Adds a leakage coefficient to limit filter gain, improving stability
- Normalized FxLMS — Adapts step size based on reference signal power

## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[leaky-fxlms-algorithm|Leaky FxLMS Algorithm]]
- [[simplified-adaptive-feedback-anc|Simplified Adaptive Feedback ANC]]

## Related Sources
