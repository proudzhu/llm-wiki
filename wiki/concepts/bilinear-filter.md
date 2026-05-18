---
type: concept
created: 2026-05-18
updated: 2026-05-18
sources:
aliases:
- Bilinear ANC
tags:
- nonlinear-systems
- adaptive-filtering
- recursive-filter
---

# Bilinear Filter

## Overview

The **bilinear filter** is a recursive nonlinear structure that combines past inputs and past outputs through a cross-product term. In [[nonlinear-active-noise-control|NLANC]] it is preferred when the system features strong saturation nonlinearity, because it captures such effects with a much shorter filter length than [[volterra-filter|Volterra]] or [[flann-filter|FLANN]] alternatives.

## Input-Output Relation

For memory length $N_1$:

$$
y(n) = \sum_{i=0}^{N_1} a_i(n)\,x(n{-}i) + \sum_{t=1}^{N_1} b_t(n)\,y(n{-}t) + \sum_{i=0}^{N_1}\sum_{t=1}^{N_1} c_{i,t}(n)\,x(n{-}i)\,y(n{-}t)
$$

with three coefficient sets:
- $a_i(n)$ : feed-forward, $N_1+1$ elements
- $b_t(n)$ : feedback, $N_1$ elements
- $c_{i,t}(n)$ : cross-products, $N_1(N_1+1)$ elements

Total $N_c = N_1^2 + 3N_1 + 1$ — quadratic in memory, but typically with a much smaller $N_1$ than the equivalent Volterra/FLANN.

## Variants for ANC

| Variant | Innovation |
|:--------|:-----------|
| **Diagonal-channel bilinear** | Restricts cross-term updates to the diagonal channel for tractability |
| **Trigonometric FLANN-bilinear** | FLANN expands the input, then bilinear filter adapts coefficients |
| **Reweighted bilinear FxLMS** | Reweights coefficients for nonlinear secondary paths |
| **Leaky bilinear FeLMS + PU** | Leaky filtered-error LMS with partial-update for stability and complexity reduction |

## When to Use

Bilinear filters are most effective when:
- The secondary path or actuator exhibits **saturation** behaviour.
- A short filter length is mandated by latency or cost constraints.
- The system does not require a true universal approximator.

## Limitations

- Recursive structure complicates stability analysis (need bounded-input bounded-output conditions).
- Cross-product term can amplify input noise.
- Less interpretable than Hammerstein/Wiener cascades.

## Related Concepts

- [[nonlinear-active-noise-control|Nonlinear ANC]]
- [[volterra-filter|Volterra Filter]]
- [[flann-filter|FLANN Filter]]
- [[adaptive-filtering|Adaptive Filtering]]
- [[filtered-x-lms-algorithm|Filtered-x LMS]]

## Related Sources

- [[../sources/lu-2021-anc-survey-nonlinear|Lu et al. 2021: Survey on ANC — Part II (Nonlinear)]]
