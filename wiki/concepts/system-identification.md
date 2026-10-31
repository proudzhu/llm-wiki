---
type: concept
created: 2026-04-12
updated: 2026-10-31
sources:
  - raw/papers/jiang-2025-ai-driven-avnc-review/full-text.md
  - raw/papers/kuo-2006-anc-headphones/full-text.txt
  - in active noise and vibration control.md
  - control in active noise control systems.md
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
5. **Low-Rank Kronecker Decomposition**: modeling a long impulse response ($L = L_1 L_2$ taps) as a sum of $P$ Kronecker products of two short filters, identified online with the [[concepts/rls-nkp|RLS-NKP]] algorithm — lower complexity and markedly faster tracking for long echo paths, since two short filters adapt instead of one long one.
6. **Musical excitation**: replacing white noise/chirp with spectrally dense music for adaptive identification — [[sources/kuo-2006-anc-headphones|Kuo, Mitra & Gan 2006]] show a 65-tap FIR model of the headphone secondary path identified with "O Fortuna" frames (near-flat 0–4 kHz) matches white-noise and chirp-identified models, removing the annoyance of audible calibration noise.

## Challenges in ANC

- **Time-Varying Paths**: In headphones, the secondary path changes every time the user moves the ear cup, requiring **Online Secondary-Path Modeling**.
- **Acoustic Feedback**: Identifying the secondary path while the system is operating can be difficult due to the coupling between the loudspeaker and microphones.
- **Complexity-Accuracy Trade-off**: Higher-order models provide better performance but increase computational load and may lead to numerical instability in real-time control (Wills 2008).

## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[active-vibration-control|Active Vibration Control]]
- [[secondary-path-modeling|Secondary Path Modeling]]
- [[deep-secondary-path-estimation|Deep Secondary Path Estimation]]
- [[state-space-model|State-Space Model]]
- [[model-predictive-control|Model Predictive Control]]

## Related Sources

- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]]
- [[sources/liang-2026-delayed-mpc-anc-paper-reading-note|Liang 2026: Delayed MPC for ANC Paper Reading Note]]
- [[sources/wills-2008-mpc-constraint-handling-anc-avc|Wills 2008: MPC Constraint Handling in ANC/AVC]]
- [[sources/jiang-2025-ai-driven-avnc-review|Jiang et al. 2025: AI-Driven AVNC Review]]
- [[sources/elisei-iliescu-2019-low-rank-rls|Elisei-Iliescu et al. 2019: Recursive Least-Squares Algorithms for the Identification of Low-Rank Systems]] — low-rank Kronecker decomposition method (RLS-NKP) for long echo paths
- [[sources/kuo-2006-anc-headphones|Kuo, Mitra & Gan 2006: Active Noise Control System for Headphone Applications]] — music-based adaptive identification of the headphone secondary path
