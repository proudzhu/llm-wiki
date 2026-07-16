---
type: concept
created: 2026-04-12
updated: 2026-05-15
sources:
  in active noise and vibration control.md
  - raw/papers/zhang-2024-neural-kalman-howling/full-text.txt
  - raw/papers/zhang-2023-hybrid-ahs/full-text.txt
tags:
- control-theory
- mathematics
- signal-processing
---

# Kalman Filter

The **Kalman Filter** is a recursive, optimal estimation algorithm that provides the minimum mean-square error estimate of the internal state of a linear dynamical system from a series of noisy measurements. Published by R.E. Kalman in 1960, it has become one of the most widely used algorithms in estimation and control.

## Core Algorithm

The filter operates in a **predictor-corrector** cycle:

### 1. Time Update (Predict)

Project the state and error covariance forward:

$$\hat{x}_k^- = A\hat{x}_{k-1} + Bu_{k-1}$$
$$\bar{P}_k = AP_{k-1}A^T + Q$$

### 2. Measurement Update (Correct)

Incorporate the new measurement $z_k$:

$$K_k = \bar{P}_k H^T(H\bar{P}_k H^T + R)^{-1}$$
$$\hat{x}_k = \hat{x}_k^- + K_k(z_k - H\hat{x}_k^-)$$
$$P_k = (I - K_k H)\bar{P}_k$$

### Kalman Gain Intuition

The gain $K_k$ balances trust between prediction and measurement:

| Condition | Gain Behavior | Interpretation |
|-----------|---------------|----------------|
| $R \to 0$ | $K_k \to H^{-1}$ | Trust measurements more |
| $\bar{P}_k \to 0$ | $K_k \to 0$ | Trust predictions more |

The **residual** (or innovation) $z_k - H\hat{x}_k^-$ measures the discrepancy between predicted and actual measurement. Zero residual means perfect prediction.

### Probabilistic Interpretation

The filter maintains the first two moments of the state distribution:

$$p(x_k | z_k) \sim N(\hat{x}_k, P_k)$$

## Filter Tuning

| Parameter | How to Determine | Notes |
|-----------|-----------------|-------|
| $R$ | Measure off-line from sensor data | Generally practical |
| $Q$ | Often difficult; sometimes "injected" uncertainty | Compensates for model errors |
| $P_0$ | Any $P_0 \neq 0$ | Filter converges regardless |
| $\hat{x}_0$ | Best guess or zero | With $P_0 \neq 0$, converges |

When $Q$ and $R$ are constant, $P_k$ and $K_k$ stabilize to steady-state values that can be pre-computed.

## Recursive Advantage

Unlike the [[wiener-filter|Wiener Filter]] which operates on all data at once, the Kalman filter recursively conditions each estimate on all past measurements. This makes it far more practical for real-time implementation.

## Role in ANC/AVC

In modern control systems like **[[model-predictive-control|Model Predictive Control]]**, the Kalman filter is used to estimate the full state vector $x(k)$ of the system from a limited number of sensors (Wills 2008).

For ANC, a Kalman filter can be used to:
- Estimate the disturbance signal (primary noise) even when it is buried in sensor noise
- Provide a robust "innovation" signal ($e(k)$) that represents the unpredictable part of the noise
- Track time-varying parameters in the acoustic environment

## Advanced Variations

- **[[extended-kalman-filter|Extended Kalman Filter (EKF)]]**: For nonlinear systems — linearizes via Jacobians at each step. Fundamental limitation: nonlinear transforms of Gaussians are not Gaussian.
- **Unscented Kalman Filter (UKF)**: Handles nonlinearities more accurately than EKF using sigma points (Julier & Uhlmann, 1996)
- **MCC-KF**: A robust Kalman filter that replaces the standard MSE update with the **[[maximum-correntropy-criterion|Maximum Correntropy Criterion]]**, making it immune to impulsive noise in the measurements
- [[frequency-domain-kalman-filter|Frequency-Domain Kalman Filter (FDKF)]]: Operates in the frequency domain for acoustic echo/howling suppression; per-frequency-bin state updates
- **Partitioned-block-frequency-domain adaptive KF**: Diagonalized variant used in acoustic echo controllers; serves as the first stage in hybrid AENR systems (e.g., Shetu et al. 2024)

## Related Concepts

- [[extended-kalman-filter|Extended Kalman Filter]]
- [[state-space-model|State-Space Model]]
- [[model-predictive-control|Model Predictive Control]]
- [[maximum-correntropy-criterion|Maximum Correntropy Criterion]]
- [[active-vibration-control|Active Vibration Control]]
- [[wiener-filter|Wiener Filter]]
- [[adaptive-filtering|Adaptive Filtering]]
- [[acoustic-howling-suppression|Acoustic Howling Suppression]]
- [[frequency-domain-kalman-filter|Frequency-Domain Kalman Filter]]

## Related Sources

- [[sources/welch-2006-kalman-filter-intro|Welch & Bishop 2006: Introduction to the Kalman Filter]]
- [[sources/wills-2008-mpc-constraint-handling-anc-avc|Wills 2008: MPC Constraint Handling in ANC/AVC]]
- [[sources/zhang-2023-hybrid-ahs|Zhang 2023: Hybrid AHS]]
- [[sources/zhang-2024-neural-kalman-howling|Zhang 2024: Neural Network Augmented Kalman Filter for AHS]]
