---
type: concept
created: 2026-04-12
updated: 2026-08-01
sources:
  in active noise and vibration control.md
  control in active noise control systems.md
tags:
- control-theory
- mathematics
- deep-learning
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

## Deep-Learning State-Space Models

A separate subfamily of state-space models has emerged in deep learning, where the continuous-time SSM equations above are used as a **trainable neural-network layer** rather than as a model of a physical plant. The discretized convolution form $y = \overline{K} * u$ makes the layer trainable on long sequences via FFT, with theoretically infinite receptive field. Notable variants in this wiki:

- **[[concepts/s4nd|S4ND]]** (Nguyen et al., NeurIPS 2022) — multidimensional PDE extension of the S4 structured SSM, with independent SSMs along each input axis. Used as the global-feature branch of the [[concepts/sic-block|SIC block]] in [[concepts/sicrn|SICRN]] for monaural speech enhancement.
- **[[concepts/mamba-mingru|Mamba-MinGRU]]** (Østergaard et al. 2026) — selective state-space model (Mamba) + MinGRU linear recurrence for time-domain own-voice cancellation at 2 ms latency.

These deep-learning SSMs share the underlying state-space mathematics with the control-theoretic SSMs above, but are used as learnable sequence-modeling layers rather than as identified plant models.

## Related Concepts

- [[model-predictive-control|Model Predictive Control]]
- [[system-identification|System Identification]]
- [[kalman-filter|Kalman Filter]]
- [[active-noise-control|Active Noise Control]]
- [[active-vibration-control|Active Vibration Control]]
- [[kalman-filter|Kalman Filter]]
- [[extended-kalman-filter|Extended Kalman Filter]]
- [[s4nd|S4ND]] — multidimensional deep-learning SSM (speech enhancement)
- [[mamba-mingru|Mamba-MinGRU]] — selective SSM + MinGRU (own-voice cancellation)

## Related Sources

- [[sources/welch-2006-kalman-filter-intro|Welch & Bishop 2006: Introduction to the Kalman Filter]]
- [[sources/wills-2008-mpc-constraint-handling-anc-avc|Wills 2008: MPC Constraint Handling in ANC/AVC]]
- [[sources/liang-2026-delayed-mpc-anc-paper-reading-note|Liang 2026: Delayed MPC for ANC Paper Reading Note]]
- [[sources/zhao-2024-sicrn|Zhao, He & Zhang 2024: SICRN]] — applies S4ND (multidimensional deep-learning SSM) to monaural speech enhancement
