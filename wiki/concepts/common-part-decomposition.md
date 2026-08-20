---
type: concept
created: 2026-08-20
updated: 2026-08-20
sources:
  - raw/papers/schepker-2016-sdp-minmax-acoustic-feedback/full-text.md
tags:
  - acoustic-feedback-cancellation
  - hearing-aids
  - system-identification
  - pole-zero-filters
aliases:
  - common part modeling
  - feedback path decomposition
---

# Common Part Decomposition

**Common part decomposition** is a modeling technique for acoustic feedback paths in hearing aids that reduces the number of adaptive parameters by decomposing each acoustic transfer function (ATF) $H_m(z)$ into the convolution of a time-invariant **common part** $\hat{H}^c(z)$ and a time-varying **variable part** $\hat{H}_m^v(z)$:

$$\hat{H}_m(z) = \hat{H}^c(z) \cdot \hat{H}_m^v(z) = \frac{B^c(z)}{A^c(z)} \cdot B_m^v(z)$$

The common part accounts for components shared across a set of feedback paths (e.g., transducer characteristics, individual ear characteristics), while the variable part tracks fast changes (e.g., a moving telephone or hand). The common part is typically modeled as a pole-zero filter ($N_p^c$ poles, $N_z^c$ zeros), and the variable part as an all-zero filter ($N_z^v$ zeros) to enable stable adaptive filtering.

## Motivation

The convergence speed and computational complexity of [[concepts/adaptive-feedback-cancellation|adaptive feedback cancellation (AFC)]] algorithms depend on the number of adaptive parameters. By extracting a time-invariant common part from a set of measured feedback paths (e.g., multi-microphone hearing aid or multiple measurements), only the lower-order variable part needs to be adapted online, reducing the adaptive filter length and improving convergence.

## Estimation Approaches

The parameters of the common and variable parts are estimated from a set of measured ATFs using two main approaches:

1. **Least-squares (LS) optimization** (Schepker & Doclo 2014): Minimizes the overall misalignment between true and estimated feedback paths using the iterative Steiglitz-McBride method with alternating least-squares. Yields good misalignment but may limit the [[concepts/maximum-stable-gain|MSG]].

2. **[[concepts/min-max-common-part-estimation|Min-max optimization]]** (Schepker & Doclo 2016): Directly maximizes the MSG by minimizing the maximum output-error across all frequencies and paths, formulated as a semidefinite program with Lyapunov stability constraints. Yields 2–5 dB MSG improvement over LS at the cost of increased misalignment.

## Robustness

The common part estimated from a limited set of measured feedback paths (e.g., free-field conditions) generalizes to unseen feedback paths (telephone receiver, repositioned hearing aid), enabling MSG improvements and variable-part parameter reduction even for unknown conditions not included in the optimization.

## Related Concepts

- [[concepts/min-max-common-part-estimation|Min-max Common Part Estimation]] — the SDP-based optimization approach for estimating the common part
- [[concepts/adaptive-feedback-cancellation|Adaptive Feedback Cancellation (AFC)]] — the application context
- [[concepts/maximum-stable-gain|Maximum Stable Gain]] — the performance metric optimized by the min-max approach
- [[concepts/prediction-error-method|Prediction Error Method]] — used with common part decomposition in AFC simulations
- [[concepts/hearing-aid-feedback-cancellation|Hearing Aid Feedback Cancellation]] — the application domain

## Related Sources

- [[sources/schepker-2016-sdp-minmax-acoustic-feedback|Schepker & Doclo 2016: SDP Min-max Common Part Estimation]] — proposes the min-max SDP optimization with Lyapunov stability constraint
