---
type: concept
created: 2026-04-18
updated: 2026-07-22
sources:
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
| [[kalman-filter\|Kalman Filter]] | Optimal recursive estimator | Minimum MSE, requires state-space model |
| [[extended-kalman-filter\|EKF]] | Nonlinear Kalman | Handles nonlinear dynamics via Jacobians |

## Relationship to Kalman Filtering

The Kalman filter can be viewed as an adaptive filter with an optimal (minimum MSE) gain that adapts based on the relative uncertainties of the process model and measurements. Unlike LMS/FxLMS which use fixed step sizes, the Kalman gain automatically adjusts based on the error covariance. The [[kalman-filter|Kalman Filter]] is recursive like LMS but optimal in the MSE sense, making it a theoretically superior adaptive filter when the state-space model is known.

## Neural Counterpart: Adaptive Convolution

[[concepts/adaptive-convolution|Adaptive convolution]] (Wang et al. 2025) is the neural-network analogue of classical adaptive filtering for streaming speech enhancement: instead of updating filter coefficients via an LMS/RLS recursion on an error signal, it generates per-frame convolution kernels by aggregating a small bank of learned candidate kernels with input-dependent attention weights. The conceptual parallel — adjusting filter coefficients in real time based on the statistical characteristics of the input signal — is made explicit in the paper. Ablation reveals that candidate-kernel selection correlates strongly with signal characteristics (speaker pitch, speech vs. noise activity), mirroring how classical adaptive filters tune their coefficients to input statistics.

## Related Concepts
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/momentum-lms|Momentum LMS]]
- [[concepts/kalman-filter|Kalman Filter]]
- [[concepts/extended-kalman-filter|Extended Kalman Filter]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/wiener-filter|Wiener Filter]]
- [[concepts/adaptive-convolution|Adaptive Convolution]]

## Related Sources

- [[sources/welch-2006-kalman-filter-intro|Welch & Bishop 2006: Introduction to the Kalman Filter]]
- [[sources/fujii-2006-simultaneous-equations-anc|Fujii et al. 2006: Verification of Simultaneous Equations Method]] — Frequency-domain adaptive algorithm for overall path identification in ANC
