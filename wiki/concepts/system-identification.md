---
type: concept
created: 2026-04-12
updated: 2026-04-17
sources:
  in active noise and vibration control.md
  control in active noise control systems.md
tags:
- control-theory
- signal-processing
---

# System Identification

**System Identification** is the process of building mathematical models of dynamic systems from measured input and output data.

## Overview

In [[active-noise-control|Active Noise Control]] and [[active-vibration-control|Active Vibration Control]], system identification is crucial for characterizing the **Primary Path** and **Secondary Path**. These models are used by adaptive algorithms (like FxLMS) and modern control strategies (like MPC).

## Common Identification Methods

1. **Adaptive LMS/RLS**: Used for online identification where the model parameters are updated continuously.
2. **Transfer Function Fitting**: Measuring the frequency response and fitting a rational function (poles and zeros).
3. **Vector Fitting**: A robust iterative algorithm for fitting high-order state-space models to frequency domain data. Used in Liang (2026) to generate 15th-order models for ANC.
4. **Subspace Identification**: Algorithms like N4SID that estimate state-space matrices directly from time-series data.

## Challenges in ANC

- **Time-Varying Paths**: In headphones, the secondary path changes every time the user moves the ear cup, requiring **Online Secondary-Path Modeling**.
- **Acoustic Feedback**: Identifying the secondary path while the system is operating can be difficult due to the coupling between the loudspeaker and microphones.
- **Complexity-Accuracy Trade-off**: Higher-order models provide better performance but increase computational load and may lead to numerical instability in real-time control (Wills 2008).

## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[secondary-path-modeling|Secondary Path Modeling]]
- [[state-space-model|State-Space Model]]
- [[model-predictive-control|Model Predictive Control]]
- [[active-vibration-control|Active Vibration Control]]

## Related Sources

- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]]
- [[sources/liang-2026-delayed-mpc-anc-paper-reading-note|Liang 2026: Delayed MPC for ANC Paper Reading Note]]
- [[sources/wills-2008-mpc-constraint-handling-anc-avc|Wills 2008: MPC Constraint Handling in ANC/AVC]]
