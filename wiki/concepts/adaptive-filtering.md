---
type: concept
created: 2026-04-18
updated: 2026-05-03
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

## Related Concepts
- [[active-noise-control|Active Noise Control]]
- [[momentum-lms|Momentum LMS]]
- [[kalman-filter|Kalman Filter]]
- [[extended-kalman-filter|Extended Kalman Filter]]
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[wiener-filter|Wiener Filter]]

## Related Sources

- [[../sources/welch-2006-kalman-filter-intro|Welch & Bishop 2006: Introduction to the Kalman Filter]]
