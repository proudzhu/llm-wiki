---
type: concept
created: 2026-04-10
updated: 2026-04-10
sources:
tags:
- adaptive-algorithms
- signal-processing
- stability
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

## Related Concepts

- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[simplified-adaptive-feedback-anc|Simplified Adaptive Feedback ANC]]
- [[active-noise-control|Active Noise Control]]

## Related Sources
