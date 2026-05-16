---
type: concept
created: 2026-04-12
updated: 2026-04-25
sources:
  Controllers.md
tags:
- mathematics
- signal-processing
---

# Wiener Filter

The **Wiener Filter** is an optimal linear filter used to produce an estimate of a desired random process by linear time-invariant (LTI) filtering of an observed noisy process.

## Overview

The Wiener filter minimizes the **Mean Square Error (MSE)** between the filter output and the desired signal. It assumes that the signal and noise are stationary random processes with known spectral characteristics or auto-correlation and cross-correlation functions.

## Optimal Solution

For a discrete-time FIR filter of length $N$, the optimal weights $w_{opt}$ are given by the **Wiener-Hopf Equation**:
$$ w_{opt} = R^{-1} P $$
Where:
- **$R$**: Auto-correlation matrix of the input signal.
- **$P$**: Cross-correlation vector between the input and the desired signal.

## Role in ANC

In **[[active-noise-control|Active Noise Control]]**, the Wiener filter represents the theoretical optimal controller for a given acoustic path.
- **Feedforward ANC**: The optimal $W(z) = P(z)/S(z)$, which is a Wiener filter that models the primary path while compensating for the secondary path.
- **Feedback ANC**: The optimal controller for minimizing the variance of the error signal can be derived as a Wiener filter using the **Internal Model Control (IMC)** structure (Pawelczyk 1997).

## Limitations

- **Stationarity**: The standard Wiener filter assumes the signals are stationary. In real-world ANC, signals are often non-stationary, necessitating **Adaptive Filters** (like LMS or RLS) that iteratively converge toward the Wiener solution.
- **Causality**: The optimal Wiener solution may be non-causal (requiring future information). In practical systems, a causal approximation must be used, which may have lower performance.

## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[feedback-anc|Feedback ANC]]
- [[internal-model-control|Internal Model Control]]
- [[minimum-variance-control|Minimum Variance Control]]
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[kalman-filter|Kalman Filter]]

## Related Sources

- [[sources/welch-2006-kalman-filter-intro|Welch & Bishop 2006: Introduction to the Kalman Filter]]
- [[sources/pawelczyk-1997-anc-feedback-fixed-adaptive|Pawelczyk 1997: ANC Feedback Fixed/Adaptive]]
- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]]
