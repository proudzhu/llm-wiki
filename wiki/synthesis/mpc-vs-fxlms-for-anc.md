---
type: synthesis
created: 2026-04-12
updated: 2026-04-19
sources:
tags:
- constraint-handling
- model-predictive-control
- quadratic-programming
- real-time
- state-space
---

# MPC vs Traditional ANC: Two Paths to Optimal Control

> Cross-source synthesis connecting [[../sources/wills-2008-mpc-constraint-handling-anc-avc|Wills 2008: MPC Constraint Handling in ANC/AVC]] (DSP implementation) and [[../sources/liang-2026-delayed-mpc-anc-paper-reading-note|Liang 2026: Delayed MPC for ANC Paper Reading Note]] (closed-form solution).

---

## The Fundamental Difference

Traditional ANC ([[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]) and [[../concepts/model-predictive-control|Model Predictive Control]] (MPC) solve the same problem — generate anti-noise to cancel unwanted sound — but with **fundamentally different philosophies**:

| Aspect | FxLMS | MPC |
|--------|-------|-----|
| **Optimization** | Per-sample gradient descent | Batch optimization over prediction horizon |
| **Constraints** | Cannot handle them | Explicitly handles actuator saturation, stability |
| **Solution** | Iterative (one step at a time) | Closed-form or QP (all future steps) |
| **Computational cost** | $O(L)$ per sample | $O(N_{state}^2 \cdot N_p)$ per control interval |
| **Theoretical foundation** | Stochastic approximation | Optimal control theory |
| **Tuning parameters** | $\mu$ (step size) | $Q, R$ (weights), $N_p$ (prediction horizon) |

---

## MPC for ANC: The Control Problem

Both [[../sources/wills-2008-mpc-constraint-handling-anc-avc|Wills 2008: MPC Constraint Handling in ANC/AVC]] and [[../sources/liang-2026-delayed-mpc-anc-paper-reading-note|Liang 2026: Delayed MPC for ANC Paper Reading Note]] formulate ANC as:

$$\min_u \sum_{k=0}^{N_p-1} \left( x(k)^T Q x(k) + u(k)^T R u(k) \right)$$

subject to:
- **System dynamics**: $x(k+1) = A x(k) + B u(k - d)$
- **Actuator constraints**: $|u(k)| \leq u_{\max}$ (speaker saturation)
- **Rate constraints**: $|\Delta u(k)| \leq \Delta u_{\max}$ (speaker slew rate)

Where $d$ is the system delay (typically 1-5 samples in ANC).

---

## Wills 2008: Online QP Solver on DSP

### Approach

[[../sources/wills-2008-mpc-constraint-handling-anc-avc|Wills 2008: MPC Constraint Handling in ANC/AVC]] uses a **numerical QP solver** running online at each control step:

1. At each sample, formulate the MPC problem as a Quadratic Program
2. Solve the QP using an active-set method
3. Apply the first control input
4. Repeat at next sample

### DSP Implementation

| Parameter | Value |
|-----------|-------|
| DSP | Analog Devices ADSP-21262 (SHARC) |
| Model order | 18 states |
| Sampling rate | 5 kHz |
| QP solve time | < 150 μs |
| Control interval | 200 μs |

### Key Findings

1. **MPC outperforms saturated LQG** when actuator constraints are active (by 3-5 dB)
2. **Constraint handling is the primary benefit** — without constraints, MPC ≈ LQG
3. **Computationally feasible** on 2008-era DSP with 150 μs solve time
4. **The main limitation**: QP solve time grows cubically with model order

---

## Liang 2026: Analytical Closed-Form Solution

### Approach

[[../sources/liang-2026-delayed-mpc-anc-paper-reading-note|Liang 2026: Delayed MPC for ANC Paper Reading Note]] derives an **analytical closed-form solution** for MPC with input delay:

$$u^* = -(R + B^T P B)^{-1} B^T P A x$$

where $P$ is the solution to the discrete-time Riccati equation.

This eliminates the need for online QP solving entirely.

### Key Innovation: Delay Compensation

The key contribution is handling the **system delay** $d$ in the ANC loop:
- The control input $u(k-d)$ affects the system $d$ steps later
- Standard MPC assumes instantaneous input
- Liang et al. derive a modified Riccati equation that accounts for delay

### Performance

| Metric | Wills 2008 (QP) | Liang 2026 (Closed-form) |
|--------|----------------|-------------------------|
| Computation per step | 150 μs (active-set QP) | < 10 μs (matrix multiply) |
| Noise reduction | ~12 dB | ~14 dB |
| Constraint handling | Yes (hard constraints) | Yes (via Riccati modification) |
| Model order limit | ~20 states (DSP-limited) | No practical limit |
| Implementation | Complex QP solver | Simple matrix operations |

---

## Why MPC Matters for ANC

### 1. Explicit Constraint Handling

This is the **killer feature** of MPC for ANC. Speaker saturation causes:
- **Wind-up**: The integrator in the controller accumulates error during saturation
- **Instability**: When the speaker recovers, the accumulated error causes overshoot
- **Distortion**: Clipped anti-noise signals are harmonically distorted

MPC **predicts** saturation before it happens and adjusts the control input proactively.

### 2. Multi-Objective Optimization

MPC can simultaneously optimize for:
- Noise reduction (primary objective)
- Control effort (secondary objective, via $R$ weight)
- Actuator wear (rate constraints)
- Stability margins (terminal constraints)

### 3. Systematic Delay Compensation

Unlike FxLMS which implicitly handles delay through the filtered reference signal, MPC explicitly models the delay in its state-space formulation, leading to more accurate compensation.

---

## When to Use MPC vs FxLMS

| Scenario | Recommended | Why |
|----------|-------------|-----|
| Simple single-channel ANC | FxLMS | Lower complexity, well-understood |
| Actuator saturation is a problem | MPC | Explicit constraint handling |
| Multi-channel ANC with cross-coupling | MPC | Naturally handles MIMO systems |
| Ultra-low latency (< 1 ms) | FxLMS | QP solve time adds latency |
| Variable acoustic conditions | MPC | Model-based adaptation |
| DSP-constrained embedded system | Liang 2026 closed-form | < 10 μs computation |

---

## Related Concepts

- [[../concepts/model-predictive-control|Model Predictive Control]]
- [[../concepts/quadratic-programming|Quadratic Programming]]
- [[../concepts/state-space-model|State-Space Model]]
- [[../concepts/system-identification|System Identification]]
- [[../concepts/kalman-filter|Kalman Filter]]
- [[../concepts/active-vibration-control|Active Vibration Control]]
- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[../concepts/active-noise-control|Active Noise Control]]

## Related Sources

- [[../sources/wills-2008-mpc-constraint-handling-anc-avc|Wills 2008: MPC Constraint Handling in ANC/AVC]]
- [[../sources/liang-2026-delayed-mpc-anc-paper-reading-note|Liang 2026: Delayed MPC for ANC Paper Reading Note]]
- [[../sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]]
