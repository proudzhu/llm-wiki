---
type: source
created: 2026-04-25
updated: 2026-04-25
sources:
  - zotero://select/items/0_UCQRBZUX
tags:
  - kalman-filter
  - state-estimation
  - extended-kalman-filter
  - control-theory
---

# Welch & Bishop 2006: Introduction to the Kalman Filter

**Authors**: [[entities/greg-welch|Greg Welch]], [[entities/gary-bishop|Gary Bishop]]
**Institution**: University of North Carolina at Chapel Hill, Department of Computer Science
**Year**: 2006 (original TR 95-041, first published 1995, updated 2006)
**Type**: Technical Report / Tutorial
**Zotero**: [UCQRBZUX](zotero://select/items/0_UCQRBZUX)

## Summary

This seminal tutorial provides a practical introduction to the discrete Kalman filter and the Extended Kalman Filter (EKF). It presents the complete mathematical derivation, the predictor-corrector algorithm structure, filter tuning guidelines, and a worked numerical example estimating a random constant. The paper is widely cited as the standard accessible reference for understanding Kalman filtering from first principles.

## The Discrete Kalman Filter

### Process Model

The Kalman filter estimates the state $x \in \mathbb{R}^n$ of a discrete-time controlled process governed by the linear stochastic difference equation:

$$x_k = A x_{k-1} + B u_{k-1} + w_{k-1} \tag{1.1}$$

with a measurement $z \in \mathbb{R}^m$:

$$z_k = H x_k + v_k \tag{1.2}$$

where:
- $A$ (n×n): state transition matrix relating previous state to current state
- $B$ (n×l): control input matrix relating input $u$ to state
- $H$ (m×n): measurement matrix relating state to measurement
- $w_k \sim N(0, Q)$: process noise
- $v_k \sim N(0, R)$: measurement noise

### The Kalman Gain

The gain $K_k$ minimizes the a posteriori error covariance:

$$K_k = \bar{P}_k H^T (H \bar{P}_k H^T + R)^{-1} = \frac{\bar{P}_k H^T}{H \bar{P}_k H^T + R} \tag{1.8}$$

Key intuition:
- As $R \to 0$: $K_k \to H^{-1}$ — trust measurements more
- As $\bar{P}_k \to 0$: $K_k \to 0$ — trust predictions more

### Predictor-Corrector Algorithm

| Phase | Equation | Description |
|-------|----------|-------------|
| **Time Update (Predict)** | $\hat{x}_k^- = A \hat{x}_{k-1} + B u_{k-1}$ | Project state ahead |
| | $\bar{P}_k = A P_{k-1} A^T + Q$ | Project error covariance ahead |
| **Measurement Update (Correct)** | $K_k = \bar{P}_k H^T (H \bar{P}_k H^T + R)^{-1}$ | Compute Kalman gain |
| | $\hat{x}_k = \hat{x}_k^- + K_k(z_k - H\hat{x}_k^-)$ | Update estimate with measurement |
| | $P_k = (I - K_k H)\bar{P}_k$ | Update error covariance |

The residual $(z_k - H\hat{x}_k^-)$ is the **innovation** — the discrepancy between predicted and actual measurement. Zero residual means perfect prediction.

### Probabilistic Interpretation

The filter maintains the first two moments of the state distribution:

$$p(x_k | z_k) \sim N(\hat{x}_k, P_k)$$

The a posteriori estimate reflects the mean; the error covariance reflects the variance.

## Filter Parameters and Tuning

| Parameter | Typical Determination | Notes |
|-----------|----------------------|-------|
| $R$ (measurement noise) | Measured off-line from sensor data | Generally practical — can sample measurements to determine variance |
| $Q$ (process noise) | Often difficult to determine directly | Sometimes "injected" uncertainty compensates for poor process model |
| $P_0$ (initial covariance) | Any $P_0 \neq 0$ — filter converges | Choice not critical; filter eventually converges |
| $\hat{x}_0$ (initial state) | Best guess or zero | With $P_0 \neq 0$, filter will converge |

**Steady-state behavior**: When $Q$ and $R$ are constant, both $P_k$ and $K_k$ stabilize quickly and remain constant. These can be pre-computed off-line.

**Dynamic tuning**: $Q_k$ can be adjusted during operation — increase when dynamics change rapidly, decrease when motion is slow.

## The Extended Kalman Filter (EKF)

### Nonlinear Process Model

For nonlinear systems:

$$x_k = f(x_{k-1}, u_{k-1}, w_{k-1}) \tag{2.1}$$
$$z_k = h(x_k, v_k) \tag{2.2}$$

### Linearization via Jacobians

Approximate state and measurement without noise:

$$\tilde{x}_k = f(\hat{x}_{k-1}, u_{k-1}, 0) \tag{2.3}$$
$$\tilde{z}_k = h(\tilde{x}_k, 0) \tag{2.4}$$

Linearize around the estimate using Jacobian matrices:

| Jacobian | Definition |
|----------|------------|
| $A_{k}[i,j] = \frac{\partial f[i]}{\partial x[j]}(\hat{x}_{k-1}, u_{k-1}, 0)$ | Process w.r.t. state |
| $W_{k}[i,j] = \frac{\partial f[i]}{\partial w[j]}(\hat{x}_{k-1}, u_{k-1}, 0)$ | Process w.r.t. noise |
| $H_{k}[i,j] = \frac{\partial h[i]}{\partial x[j]}(\tilde{x}_k, 0)$ | Measurement w.r.t. state |
| $V_{k}[i,j] = \frac{\partial h[i]}{\partial v[j]}(\tilde{x}_k, 0)$ | Measurement w.r.t. noise |

### EKF Algorithm

| Phase | Equation | Description |
|-------|----------|-------------|
| **Time Update** | $\hat{x}_k^- = f(\hat{x}_{k-1}, u_{k-1}, 0)$ | Project state ahead |
| | $\bar{P}_k = A_k P_{k-1} A_k^T + W_k Q_{k-1} W_k^T$ | Project covariance with Jacobians |
| **Measurement Update** | $K_k = \bar{P}_k H_k^T (H_k \bar{P}_k H_k^T + V_k R_k V_k^T)^{-1}$ | Compute gain with Jacobians |
| | $\hat{x}_k = \hat{x}_k^- + K_k(z_k - h(\hat{x}_k^-, 0))$ | Update with nonlinear measurement |
| | $P_k = (I - K_k H_k)\bar{P}_k$ | Update covariance |

### EKF Fundamental Limitation

The EKF linearizes around the current estimate, but **nonlinear transformations of Gaussian distributions are no longer Gaussian**. The EKF is an ad hoc estimator that only approximates Bayes' optimality via linearization. This motivates the **Unscented Kalman Filter (UKF)** by Julier and Uhlmann, which preserves normal distributions through nonlinear transformations.

## Worked Example: Estimating a Random Constant

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| State $x$ | Scalar constant (voltage) | $A=1$, $B=0$, $H=1$ |
| True value | $x = -0.37727$ | Randomly chosen |
| $Q$ | $10^{-5}$ | Small but nonzero for tuning flexibility |
| $R$ | $0.01$ (= $0.1^2$) | 0.1V RMS measurement noise |
| $\hat{x}_0$ | 0 | Standard normal prior |
| $P_0$ | 1 | Nonzero to allow convergence |

### Simulation Results

| Simulation | $R$ | Behavior |
|:-----------|:----|:---------|
| 1 (nominal) | 0.01 | Balanced: estimate converges smoothly to true value |
| 2 (large $R$) | 1.0 | Slower to trust measurements; smoother but sluggish |
| 3 (small $R$) | 0.0001 | Quick to trust measurements; noisier estimate |

The error covariance $P_k$ converges from initial $P_0 = 1$ to approximately $0.0002$ by iteration 50, demonstrating filter convergence regardless of initial choice.

## Key Contributions

1. **Accessible presentation** of the discrete Kalman filter equations with clear predictor-corrector structure
2. **Physical intuition** for the Kalman gain — how $R$ and $P_k$ control trust between measurements and predictions
3. **Complete EKF derivation** from linearization of nonlinear systems via Jacobians
4. **Practical tuning guidance** — how to choose $Q$, $R$, $P_0$, and dynamic adjustment strategies
5. **Numerical example** with three simulations demonstrating the effect of varying $R$

## Related Concepts

- [[kalman-filter|Kalman Filter]] — the main concept page
- [[extended-kalman-filter|Extended Kalman Filter]]
- [[state-space-model|State-Space Model]]
- [[adaptive-filtering|Adaptive Filtering]]
- [[wiener-filter|Wiener Filter]]
- [[model-predictive-control|Model Predictive Control]]

## Related Entities

- [[entities/greg-welch|Greg Welch]]
- [[entities/gary-bishop|Gary Bishop]]

## Related Sources
