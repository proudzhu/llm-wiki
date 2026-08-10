---
type: concept
created: 2026-04-10
updated: 2026-08-10
sources:
  - raw/papers/guo-2024-anc-saturation-survey/full-text.md
tags:
- adaptive-algorithms
- signal-processing
- stability
- output-constraint-algorithms
---

# Leaky FxLMS Algorithm

## Overview

The **Leaky Filtered-x LMS** algorithm is a variant of the [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] that introduces a **leakage coefficient** (γ, typically close to 1, e.g., 0.9998) to limit the growth of the adaptive filter coefficients.

## Weight Update Rule

```
w(n+1) = γ · w(n) + μ · e(n) · x_f(n)
```

where γ is the leakage coefficient (0 < γ ≤ 1).

## Why Leaky?

The standard FxLMS algorithm can allow the adaptive filter gain to grow without limit, which may cause the system to become **unstable** — particularly in feedback ANC configurations. The leaky variant:

- **Limits the filter gain**, preventing divergence
- **Improves feedback loop stability**
- Trade-off: introduces **bias** into the convergent control filter, as it does not directly minimize the squared error signal

## When It's Needed

The leaky FxLMS is especially important for the [[simplified-adaptive-feedback-anc|Simplified Adaptive Feedback ANC]] system, where stability is more fragile than in the IMC-based approach. Simulations in Wu et al. (2014) showed that:

- SimpAFB with standard FxLMS → **divergent**
- SimpAFB with leaky FxLMS → **stable**, achieving noise reduction comparable to the IMC-based system

## Use as an Output Constraint Algorithm

Beyond its stability role in feedback ANC, the Leaky FxLMS is one of the foundational [[output-constraint-anc-algorithms|output constraint ANC algorithms]] for mitigating the [[output-saturation-effect|output saturation effect]]. The leakage factor γ acts as a soft penalty on $\mathbf{w}^T\mathbf{w}$, indirectly limiting the output power so the secondary-path amplifier remains in its linear region. Per [[sources/guo-2024-anc-saturation-survey|Guo et al. 2024]]:

- **Scalar Leaky FxLMS**: γ is a scalar. Cost: $3N + L + 1$ multiplications.
- **Extended Leaky FxLMS** (Wu 2018): replaces γ with a matrix $\boldsymbol{\gamma} = \mathbf{C}^T\mathbf{C}$ for more control freedom over which coefficients are penalised. Cost: $2N^2 + 2N + L + 1$ multiplications.
- **OLFxLMS (Optimal Leaky FxLMS)**: sets $\boldsymbol{\gamma} = \Lambda_o \mathbf{R}_x$ so the Extended Leaky algorithm converges to the KKT optimum of the QCQP output-power-constrained ANC problem. Requires an offline inverse-modeling estimate of the secondary-path power gain $G_s$.

The Extended and Optimal variants are part of the broader family surveyed in [[concepts/output-constraint-anc-algorithms|Output Constraint ANC Algorithms]].

## Related Concepts

- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[simplified-adaptive-feedback-anc|Simplified Adaptive Feedback ANC]]
- [[active-noise-control|Active Noise Control]]
- [[concepts/output-saturation-effect|Output Saturation Effect]]
- [[concepts/output-constraint-anc-algorithms|Output Constraint ANC Algorithms]]

## Related Sources

- [[sources/guo-2024-anc-saturation-survey|Guo et al. 2024: ANC Algorithms Overcoming Output Saturation]] — survey covering Leaky, Extended Leaky, and OLFxLMS variants as part of the output constraint family
