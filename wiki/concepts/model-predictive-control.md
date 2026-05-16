---
type: concept
created: 2026-04-12
updated: 2026-04-17
sources:
  in active noise and vibration control.md
  control in active noise control systems.md
tags:
- control-theory
- model-predictive-control
- optimization
---

# Model Predictive Control

**Model Predictive Control (MPC)** is an advanced method of process control that relies on dynamic models of the system to predict its future behavior and solve an optimization problem at each sampling time.

## Overview

MPC uses a **sliding window** (receding horizon) approach. At each time step $k$:
1. The current state of the system is measured or estimated.
2. An optimization problem is solved over a future time horizon of $N$ steps to find an optimal control sequence.
3. Only the **first step** of this sequence is applied to the system.
4. The process repeats at the next time step $k+1$.

## Core Elements

- **Internal Model**: Typically a linear state-space model or an IIR filter that represents the system's dynamics.
- **Cost Function**: Usually a quadratic function that penalizes the tracking error and control effort.
- **Constraints**: Physical limits on actuators (e.g., maximum voltage) or safety limits on states are explicitly included in the optimization.

## MPC in ANC/AVC

In [[active-noise-control|Active Noise Control]] and [[active-vibration-control|Active Vibration Control]], MPC is emerging as an alternative to the standard [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] because:
1. **Constraint Handling**: Unlike FXLMS, MPC can prevent actuator saturation, ensuring stability and performance when physical limits are reached (Wills 2008).
2. **Preview Capability**: If the primary noise (disturbance) can be measured upstream, MPC can use this "preview" to pre-emptively generate anti-noise.
3. **Optimality**: MPC can be designed to match the performance of LQG controllers but with added robustness to constraints.

## Implementation Approaches

### 1. Online Quadratic Programming (QP)
The most common form, where a [[quadratic-programming|Quadratic Programming]] problem is solved at every sampling interval. This was historically too slow for high-frequency ANC (kHz range) but has been demonstrated on modern DSPs with optimized solvers (Wills 2008).

### 2. Analytical Closed-Form (Delayed MPC)
Proposed by Liang (2026), this method exploits the propagation delay in the primary path as a "free" preview window. When the prediction horizon is shorter than this delay, the MPC problem can be solved analytically without an iterative QP solver, making it computationally competitive with FXLMS.

## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[active-vibration-control|Active Vibration Control]]
- [[quadratic-programming|Quadratic Programming]]
- [[state-space-model|State-Space Model]]
- [[system-identification|System Identification]]
- [[kalman-filter|Kalman Filter]]
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]

## Related Sources

- [[sources/wills-2008-mpc-constraint-handling-anc-avc|Wills 2008: MPC Constraint Handling in ANC/AVC]]
- [[sources/liang-2026-delayed-mpc-anc-paper-reading-note|Liang 2026: Delayed MPC for ANC Paper Reading Note]]
