---
type: concept
created: 2026-04-10
updated: 2026-04-26
sources:
tags:
- active-noise-control
- control-theory
- signal-processing
---

# Internal Model Control

## Overview

**Internal Model Control (IMC)** is a control structure used in [[active-noise-control|Active Noise Control]] feedback systems to regenerate a reference signal when no physical reference sensor is available. It is the foundation for adaptive feedback ANC systems.

## How IMC Works in ANC

In an IMC-based feedback ANC system, the reference signal is **synthesized** from:

```
X(z) = E(z) - Ŝ(z) · Y(z)        (Wu 2014 convention)
```

Where:
- **E(z)** is the error signal from the error sensor
- **Y(z)** is the secondary (anti-noise) signal
- **Ŝ(z)** is the estimated secondary path response

This effectively estimates the primary noise by subtracting the contribution of the secondary signal from the error signal.

> **Sign convention note**: Different sources use different sign conventions. Wu (2014) uses `X(z) = E(z) - Ŝ(z)·Y(z)` (with `E(z) = D(z) + S(z)·Y(z)`), while Kuo & Morgan (1999) use `x̂(n) = e(n) + ŝ(n) * y(n)` (with `e(n) = d(n) - s(n) * y(n)`). The sign difference arises from whether the acoustic summing junction is defined as `d + s*y` or `d - s*y`. Both are internally consistent — the key is that the secondary contribution is **subtracted from the error** to recover the primary noise estimate.

## Advantages

- Transforms a feedback system into an equivalent **feedforward configuration**, allowing the [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] update rule to be applied within the IMC structure (mathematically)
- Stability depends on the complementary sensitivity function, which is simpler to analyze than non-adaptive system robustness
- Can be interpreted as an **adaptive predictor** of the primary noise; performance depends on noise predictability

## Disadvantages

- **High computational load**: Filtering the secondary signal through Ŝ(z) requires a convolution operation. When Ŝ(z) is an FIR filter with hundreds or thousands of coefficients, this is expensive — especially for multi-channel ANC
- **Cannot directly use commercial feedforward FxLMS controllers**: Off-the-shelf feedforward ANC hardware expects a physical reference microphone input. IMC requires the reference signal to be synthesized via `X(z) = E(z) - Ŝ(z)·Y(z)`, which needs custom hardware/software modifications that standard controllers don't support

## IMC for Fixed Controller Optimization (Hilgemann 2024)

Beyond adaptive ANC, the IMC structure is also used for **optimizing fixed feedback controllers**. The controller $K(z)$ is parameterized as:

$$K(z) = \frac{Q(z)}{1 - \hat{G}(z) Q(z)}$$

where $Q(z)$ is an FIR filter (FIR-Q parameterization). The optimization minimizes a frequency-weighted sensitivity objective:

$$J(q) = \frac{1}{N_\Omega} \sum_{\mu=1}^{N_\Omega} |W_{1,\mu} \cdot [1 - G_\mu Q_\mu(q)]|^2$$

subject to [[robust-stability-constraint|robust stability constraints]] derived from [[uncertainty-modeling-for-anc|uncertainty models]]. The IMC structure guarantees nominal stability for any $Q(z)$, simplifying the optimization to focus on performance and robust stability.

## Simplification: [[simplified-adaptive-feedback-anc|Simplified Adaptive Feedback ANC]]

The SimpAFB system eliminates the IMC's convolution step by using the error signal directly as the reference signal: `X_sa(z) = E(z)`. This trades a small amount of noise reduction performance for significantly lower computation and easier implementation.

## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[simplified-adaptive-feedback-anc|Simplified Adaptive Feedback ANC]]
- [[uncertainty-modeling-for-anc|Uncertainty Modeling for ANC]]
- [[robust-stability-constraint|Robust Stability Constraint]]

## Related Sources

- [[sources/wu-2014-simplified-adaptive-feedback-anc|Wu 2014: Simplified Adaptive Feedback ANC]] — Compares IMC-based system with the proposed simplified approach
- [[sources/hilgemann-2024-data-driven-uncertainty-anc|Hilgemann 2024: Data-Driven Uncertainty Modeling for Robust Feedback ANC]] — IMC-based fixed controller optimization with data-driven uncertainty models
