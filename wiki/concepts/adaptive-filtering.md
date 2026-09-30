---
type: concept
created: 2026-04-18
updated: 2026-09-30
sources:
- raw/papers/hoshuyama-1999-robust-adaptive-beamformer-ccaf/full-text.md
tags:
- signal-processing
- adaptive-filtering
---

# Adaptive Filtering

Adaptive filtering algorithms adjust their parameters in real-time to minimize an error signal. Unlike fixed filters, adaptive filters can track time-varying systems and non-stationary signals.

## Key Algorithms

| Algorithm | Type | Key Feature |
|-----------|------|-------------|
| LMS | Gradient descent | Simple, low complexity |
| [[momentum-lms\|Momentum LMS]] | LMS + momentum | Faster convergence, $\beta = 1/(1-\alpha)$ rate multiplier |
| FxLMS | Modified LMS for ANC | Compensates for secondary path |
| RLS | Recursive least squares | Fast convergence, high complexity |
| [[concepts/rls-nkp\|RLS-NKP]] | Low-rank RLS | Nearest Kronecker product decomposition: two coupled short filters, faster tracking of long echo paths |
| [[kalman-filter\|Kalman Filter]] | Optimal recursive estimator | Minimum MSE, requires state-space model |
| [[extended-kalman-filter\|EKF]] | Nonlinear Kalman | Handles nonlinear dynamics via Jacobians |

## Relationship to Kalman Filtering

The Kalman filter can be viewed as an adaptive filter with an optimal (minimum MSE) gain that adapts based on the relative uncertainties of the process model and measurements. Unlike LMS/FxLMS which use fixed step sizes, the Kalman gain automatically adjusts based on the error covariance. The [[kalman-filter|Kalman Filter]] is recursive like LMS but optimal in the MSE sense, making it a theoretically superior adaptive filter when the state-space model is known.

## Neural Counterpart: Adaptive Convolution

[[concepts/adaptive-convolution|Adaptive convolution]] (Wang et al. 2025) is the neural-network analogue of classical adaptive filtering for streaming speech enhancement: instead of updating filter coefficients via an LMS/RLS recursion on an error signal, it generates per-frame convolution kernels by aggregating a small bank of learned candidate kernels with input-dependent attention weights. The conceptual parallel — adjusting filter coefficients in real time based on the statistical characteristics of the input signal — is made explicit in the paper. Ablation reveals that candidate-kernel selection correlates strongly with signal characteristics (speaker pitch, speech vs. noise activity), mirroring how classical adaptive filters tune their coefficients to input statistics.

## Constrained Adaptation

A third robustness strategy — distinct from robust cost functions and from variable step size/regularization — constrains the *coefficient vector itself*. All variants are motivated by the same failure: an unconstrained adaptive canceller will grow large, finely tuned coefficients to cancel a weak but correlated component of a signal it is not supposed to cancel (in a [[concepts/gsc-beamformer|GSC]] blocking matrix, that signal is the target).

| Variant | Constraint | Typical use |
|:--------|:-----------|:------------|
| Leakage | $w(n+1) = (1-\gamma)w(n) + \mu e(n)x(n)$ | Generic misadjustment control |
| Noise injection | Add a small uncorrelated signal to the reference | Deter over-fitting to weak correlated components |
| [[concepts/norm-constrained-adaptive-filter\|Norm constraint]] | Rescale the tap vector when $\lVert W \rVert^2 > K$ | Canceller in a robust GSC |
| [[concepts/coefficient-constrained-adaptive-filter\|Per-coefficient box]] | Clamp every tap to its own $[\psi_n, \phi_n]$ | Adaptive blocking matrix with a specified target-DOA tolerance |

The per-coefficient box is the most expressive of the three: because the interval is chosen per tap index, the constraint can be *shaped* to the set of solutions a specified class of target signals requires. That is how [[sources/hoshuyama-1999-robust-adaptive-beamformer-ccaf|Hoshuyama, Sugiyama & Hirano 1999]] turn the maximum allowable [[concepts/steering-vector-error|steering-vector error]] into an explicit design parameter — their constraint region is the envelope of the optimal target-minimizing coefficient vectors over a chosen DOA sector. A scalar norm bound cannot make that distinction, which is exactly why it must trade interference reduction for robustness.

## Related Concepts
- [[concepts/coefficient-constrained-adaptive-filter|Coefficient-Constrained Adaptive Filter (CCAF)]]
- [[concepts/norm-constrained-adaptive-filter|Norm-Constrained Adaptive Filter (NCAF)]]
- [[concepts/gsc-beamformer|Generalized Sidelobe Canceller (GSC)]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/momentum-lms|Momentum LMS]]
- [[concepts/kalman-filter|Kalman Filter]]
- [[concepts/extended-kalman-filter|Extended Kalman Filter]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/wiener-filter|Wiener Filter]]
- [[concepts/adaptive-convolution|Adaptive Convolution]]

## Related Sources

- [[sources/hoshuyama-1999-robust-adaptive-beamformer-ccaf|Hoshuyama, Sugiyama & Hirano 1999: A Robust Adaptive Beamformer with a Blocking Matrix Using Constrained Adaptive Filters]] — per-coefficient box constraints on adaptive-filter taps, shaped to bound target-DOA tracking
- [[sources/welch-2006-kalman-filter-intro|Welch & Bishop 2006: Introduction to the Kalman Filter]]
- [[sources/fujii-2006-simultaneous-equations-anc|Fujii et al. 2006: Verification of Simultaneous Equations Method]] — Frequency-domain adaptive algorithm for overall path identification in ANC
- [[sources/elisei-iliescu-2019-low-rank-rls|Elisei-Iliescu et al. 2019: Recursive Least-Squares Algorithms for the Identification of Low-Rank Systems]] — introduces RLS-NKP: low-rank RLS via nearest Kronecker product decomposition
