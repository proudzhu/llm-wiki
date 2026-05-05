---
type: concept
created: 2026-04-12
updated: 2026-04-25
sources:
  in active noise and vibration control.md
  control in active noise control systems.md
tags:
- control-theory
- mathematics
---

# State-Space Model

A **State-Space Model** is a mathematical representation of a physical system as a set of input, output, and state variables related by first-order differential or difference equations.

## Mathematical Formulation

In discrete-time, a linear time-invariant (LTI) state-space model is defined by:
$$ x(k+1) = A x(k) + B u(k) + K e(k) $$
$$ y(k) = C x(k) + D u(k) + e(k) $$

Where:
- **$x(k)$**: State vector (represents the "memory" of the system).
- **$u(k)$**: Input vector (control signal).
- **$y(k)$**: Output vector (measured signal).
- **$e(k)$**: Innovation/Noise term.
- **$A, B, C, D$**: System matrices that define the dynamics.

## Role in ANC/AVC

In modern [[active-noise-control|Active Noise Control]] and [[active-vibration-control|Active Vibration Control]], state-space models are increasingly preferred over transfer functions because:
1. **Multi-Variable Support**: They naturally handle Multiple-Input Multiple-Output (MIMO) systems (e.g., multi-channel ANC).
2. **Modern Control Theory**: They are the foundation for optimal control methods like LQG (Linear Quadratic Gaussian) and **[[model-predictive-control|Model Predictive Control]]**.
3. **Internal Dynamics**: They provide access to the internal "states" of the system, which can be estimated using a **[[kalman-filter|Kalman Filter]]**.

## Model Extraction

For ANC systems, state-space models are typically obtained via **[[system-identification|System Identification]]**. Methods like **Vector Fitting** (Liang 2026) are used to fit a high-order state-space representation (e.g., 15th to 30th order) to the measured frequency response of the primary and secondary paths.

## Related Concepts

- [[model-predictive-control|Model Predictive Control]]
- [[system-identification|System Identification]]
- [[kalman-filter|Kalman Filter]]
- [[active-noise-control|Active Noise Control]]
- [[active-vibration-control|Active Vibration Control]]
- [[kalman-filter|Kalman Filter]]
- [[extended-kalman-filter|Extended Kalman Filter]]

## Related Sources

- [[../sources/welch-2006-kalman-filter-intro|Welch & Bishop 2006: Introduction to the Kalman Filter]]
- [[../sources/wills-2008-mpc-constraint-handling-anc-avc|Wills 2008: MPC Constraint Handling in ANC/AVC]]
- [[../sources/liang-2026-delayed-mpc-anc-paper-reading-note|Liang 2026: Delayed MPC for ANC Paper Reading Note]]
