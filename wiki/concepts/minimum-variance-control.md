---
type: concept
created: 2026-04-12
updated: 2026-04-17
sources:
  Controllers.md
tags:
- control-theory
- mathematics
---

# Minimum Variance Control

**Minimum Variance Control (MVC)** is an optimal control strategy designed to minimize the variance (power) of the system output.

## Overview

MVC is a fundamental concept in stochastic control. In the context of [[active-noise-control|Active Noise Control]], MVC is used to design the optimal fixed controller for **[[feedback-anc|Feedback ANC]]** systems. The goal is to minimize the expected value of the square of the residual error:
$$ J = E[e^2(n)] $$

## Mechanism

For a system with a pure propagation delay of $k$ samples, the current control action $u(n)$ can only influence the output $y(n+k)$ after $k$ steps. Therefore, the best the controller can do is to perfectly cancel the **predictable part** of the disturbance over the $k$-step horizon. The residual error will then be the unpredictable part (the "innovation" sequence).

## Applications in ANC

1. **Optimal Feedback Design**: For [[feedback-anc|Feedback ANC]] in active headphones or hearing aids, MVC provides the benchmark for the maximum achievable noise reduction.
2. **Internal Model Control (IMC)**: It can be shown that the IMC structure and the standard feedback structure are equivalent to MVC when the system model is perfect (Pawelczyk 1997).
3. **WMVC (Weighted MVC)**: In practice, pure MVC may lead to excessive control effort or instability (especially with non-minimum phase plants). **Weighted MVC** adds a penalty term for the control signal to the cost function, providing a trade-off between noise reduction and stability.

## Performance Limits

The maximum noise reduction achievable by MVC is determined by the **predictability** of the noise and the **delay** in the secondary path. 
- If the noise is white (unpredictable), MVC provides **0 dB** reduction.
- If the delay increases, performance drops significantly because more of the disturbance becomes "unpredictable" over the longer horizon.

## Related Concepts

- [[feedback-anc|Feedback ANC]]
- [[internal-model-control|Internal Model Control]]
- [[wiener-filter|Wiener Filter]]
- [[active-noise-control|Active Noise Control]]

## Related Sources

- [[../sources/pawelczyk-1997-anc-feedback-fixed-adaptive|Pawelczyk 1997: ANC Feedback Fixed/Adaptive]]
- [[../sources/benois-2020-hybrid-pseudo-cascaded-anc-headphones|Benois 2020: Hybrid and Pseudo-Cascaded ANC for Headphones]]
