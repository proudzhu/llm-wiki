---
type: concept
created: 2026-04-25
updated: 2026-04-25
sources:
tags:
  - control-theory
  - state-estimation
  - nonlinear-filtering
---

# Extended Kalman Filter

The **Extended Kalman Filter (EKF)** is a nonlinear extension of the [[kalman-filter|Kalman Filter]] that linearizes the process and measurement models around the current estimate using Jacobian matrices.

## Why the EKF Is Needed

The standard Kalman filter assumes linear dynamics and linear measurement models. Many real-world systems are nonlinear:

$$x_k = f(x_{k-1}, u_{k-1}, w_{k-1})$$
$$z_k = h(x_k, v_k)$$

The EKF handles these by locally linearizing $f$ and $h$ at each time step.

## How It Works

### 1. Linearization via Jacobians

At each step, compute four Jacobian matrices:

| Jacobian | Definition | Meaning |
|----------|------------|---------|
| $A_k$ | $\frac{\partial f}{\partial x}\big\|_{\hat{x}_{k-1}}$ | How state evolves near current estimate |
| $W_k$ | $\frac{\partial f}{\partial w}\big\|_{\hat{x}_{k-1}}$ | How process noise enters the dynamics |
| $H_k$ | $\frac{\partial h}{\partial x}\big\|_{\tilde{x}_k}$ | How measurement relates to state |
| $V_k$ | $\frac{\partial h}{\partial v}\big\|_{\tilde{x}_k}$ | How measurement noise enters |

### 2. EKF Algorithm

| Phase | Equation |
|-------|----------|
| **Predict state** | $\hat{x}_k^- = f(\hat{x}_{k-1}, u_{k-1}, 0)$ |
| **Predict covariance** | $\bar{P}_k = A_k P_{k-1} A_k^T + W_k Q_{k-1} W_k^T$ |
| **Kalman gain** | $K_k = \bar{P}_k H_k^T (H_k \bar{P}_k H_k^T + V_k R_k V_k^T)^{-1}$ |
| **Update state** | $\hat{x}_k = \hat{x}_k^- + K_k(z_k - h(\hat{x}_k^-, 0))$ |
| **Update covariance** | $P_k = (I - K_k H_k)\bar{P}_k$ |

### 3. Key Difference from Linear Kalman Filter

- Jacobians $A_k$, $W_k$, $H_k$, $V_k$ must be **recomputed at every time step** (they depend on the current state estimate)
- The nonlinear functions $f$ and $h$ are used directly in the state prediction and measurement prediction
- The covariance update uses the linearized Jacobians, not the original nonlinear functions

## Fundamental Limitation

**Nonlinear transformations of Gaussian distributions are no longer Gaussian.** The EKF linearizes around the current mean and covariance, but this is only an approximation. The resulting state distribution is not truly Gaussian — the EKF is an ad hoc estimator that approximates Bayes' optimality.

This limitation motivates alternatives:
- **Unscented Kalman Filter (UKF)**: Uses sigma points to propagate distributions through nonlinear transformations without linearization (Julier & Uhlmann, 1996)
- **Particle Filters**: Monte Carlo approach for highly nonlinear systems

## Applications

- **Navigation**: GPS/INS integration, spacecraft attitude estimation
- **Robotics**: SLAM (Simultaneous Localization and Mapping)
- **[[active-noise-control|ANC]]**: Estimating time-varying acoustic paths
- **Computer vision**: Tracking and pose estimation

## Related Concepts

- [[kalman-filter|Kalman Filter]]
- [[state-space-model|State-Space Model]]
- [[adaptive-filtering|Adaptive Filtering]]
- [[model-predictive-control|Model Predictive Control]]

## Related Sources

- [[sources/welch-2006-kalman-filter-intro|Welch & Bishop 2006: Introduction to the Kalman Filter]]
