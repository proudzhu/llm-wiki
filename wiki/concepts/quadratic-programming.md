---
type: concept
created: 2026-04-12
updated: 2026-04-17
sources:
  in active noise and vibration control.md
tags:
- mathematics
- optimization
---

# Quadratic Programming

**Quadratic Programming (QP)** is a type of mathematical optimization problem where a quadratic objective function is minimized subject to linear constraints on the variables.

## Problem Formulation

A standard QP problem can be expressed as:
$$ \min_{z} \frac{1}{2} z^T H z + f^T z $$
Subject to:
- $G z \leq W$ (Inequality constraints)
- $A z = b$ (Equality constraints)
- $l \leq z \leq u$ (Simple bounds)

Where $H$ is a symmetric positive definite matrix (for convex QP), $z$ is the vector of decision variables, and $H, f, G, W, A, b$ are problem data.

## Role in Model Predictive Control

In [[model-predictive-control|Model Predictive Control]], the control problem at each time step is formulated as a QP. The variables $z$ represent the future sequence of control actions. The quadratic objective function represents the trade-off between tracking error and control energy, while the constraints represent the physical limits of the actuators (e.g., maximum voltage).

## Solvers for Real-Time DSP

Solving a QP at every sampling period (e.g., every 200 $\mu$s for a 5 kHz ANC system) requires highly efficient algorithms. Common real-time solvers include:

1. **Active-Set Methods**: (e.g., Goldfarb-Idnani) Starts with an unconstrained solution and iteratively adds active constraints until the optimal solution is found. Effective when the number of constraints is small and "warm-starting" (using the previous solution) is possible (Wills 2008).
2. **Interior-Point Methods**: Suitable for large-scale problems with many constraints, but often have higher fixed computational costs per iteration.
3. **Explicit MPC (Lookup Tables)**: Pre-calculates the QP solutions for all possible states and stores them in a lookup table. However, this suffers from the "curse of dimensionality" and requires massive memory for high-order systems.

## Related Concepts

- [[model-predictive-control|Model Predictive Control]]
- [[active-vibration-control|Active Vibration Control]]
- [[active-noise-control|Active Noise Control]]

## Related Sources

- [[../sources/wills-2008-mpc-constraint-handling-anc-avc|Wills 2008: MPC Constraint Handling in ANC/AVC]]
