---
type: concept
created: 2026-05-13
updated: 2026-05-13
tags:
  - control-theory
  - optimization
  - robust-control
---

# Q-Parameterization

**Q-parameterization** (also known as Youla parameterization) is a control theory technique that parameterizes all stabilizing controllers for a given plant using a stable free parameter $Q$. In the context of feedback ANC, it reformulates the controller design as an optimization over the Q-parameter.

## Key Formulations

The feedback control filter is expressed as:

$$C = \frac{Q}{1 - Q P_0}$$

where $Q$ is the optimization variable and $P_0$ is the nominal plant model. The optimization minimizes the sensitivity function subject to stability and performance constraints.

## Applications in ANC

- **Constrained optimization**: The Q-parameter is found via sequential quadratic programming, minimizing error signal variance while satisfying robustness constraints
- **Frequency warping integration**: Q-parameterization can be applied in the warped frequency domain for improved low-frequency performance
- **Laguerre-basis integration**: $Q$ can be parameterized as a [[concepts/laguerre-filter|Laguerre filter]] network — since the Laguerre frequency response is affine in the coefficient vector, the convexity of the constrained program is preserved, and an order-17 Laguerre $Q$ matches order-255 FIR performance ([[sources/klatt-2025-laguerre-feedback-anc|Klatt & Martin 2025]])

## Related Concepts

- [[concepts/feedback-anc|Feedback ANC]]
- [[concepts/sensitivity-function|Sensitivity Function]]
- [[concepts/robust-control|Robust Control]]

## Related Sources

- [[sources/seo-2016-feedback-anc-constrained-optimization|Seo et al. 2016: Feedback ANC via Constrained Optimization]]
- [[sources/klatt-2025-laguerre-feedback-anc|Klatt & Martin 2025: Laguerre Filter-based Robust Feedback Active Noise Control]]
