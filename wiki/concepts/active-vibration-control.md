---
type: concept
created: 2026-04-12
updated: 2026-04-17
sources:
  - raw/papers/jiang-2025-ai-driven-avnc-review/full-text.md
  - in active noise and vibration control.md
tags:
- active-vibration-control
- control-theory
- structural-dynamics
---

# Active Vibration Control

**Active Vibration Control (AVC)** is the application of active control techniques to reduce the undesirable vibrations of structures, such as beams, plates, or bridges, using sensors and actuators.

## Overview

AVC is conceptually similar to [[active-noise-control|Active Noise Control]], but while ANC deals with acoustic pressure waves in fluids (like air), AVC deals with structural vibrations (displacement, velocity, or acceleration) in solids. It is particularly effective for suppressing resonant modes in flexible structures where passive damping (adding mass or stiffness) is weight-prohibitive.

## Core Components

1. **Sensors**: Typically accelerometers, strain gauges, or piezoelectric sensors that measure the structural deformation or movement.
2. **Actuators**: Piezoelectric ceramic patches (PZT), electromagnetic shakers, or active engine mounts that apply counter-forces or moments to the structure.
3. **Controller**: Implements algorithms like [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]], [[model-predictive-control|Model Predictive Control]], or $H_\infty$ to generate the anti-vibration signals.

## Technical Challenges

### 1. Actuator Saturation
In AVC, actuators (especially piezoelectric patches) have strict physical limits such as maximum voltage, displacement, or depolarization voltage. Traditional controllers like LQG or FXLMS may become unstable or lose performance when these limits are hit. [[model-predictive-control|Model Predictive Control]] is often used to explicitly handle these constraints (Wills 2008).

### 2. High-Order Modal Dynamics
Structures have many resonant modes. A controller designed for low-frequency modes might accidentally excite unmodeled high-frequency modes (spillover effect). This requires:
- Accurate [[system-identification|System Identification]].
- Low-pass filtering of control signals.
- Robust control design.

### 3. Sensor/Actuator Placement
The effectiveness of AVC depends heavily on placing sensors and actuators at points of maximum strain or displacement for the target modes (e.g., anti-nodes).

## Comparison with ANC

| Feature | ANC | AVC |
|---------|-----|-----|
| **Medium** | Air / Water | Solids (Beams, Plates) |
| **Primary Goal** | Sound Pressure Level (SPL) reduction | Displacement / Acceleration reduction |
| **Actuators** | Loudspeakers | Piezoelectric patches, Shakers |
| **Complexity** | Multi-path propagation | Modal coupling |

## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[input-shaping|Input Shaping]]
- [[reinforcement-learning-for-control|Reinforcement Learning for Control]]
- [[safe-reinforcement-learning|Safe Reinforcement Learning]]
- [[model-predictive-control|Model Predictive Control]]
- [[quadratic-programming|Quadratic Programming]]
- [[system-identification|System Identification]]
- [[state-space-model|State-Space Model]]
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]

## Related Sources

- [[sources/wills-2008-mpc-constraint-handling-anc-avc|Wills 2008: MPC Constraint Handling in ANC/AVC]]
- [[sources/liang-2026-delayed-mpc-anc-paper-reading-note|Liang 2026: Delayed MPC for ANC Paper Reading Note]]
- [[sources/jiang-2025-ai-driven-avnc-review|Jiang et al. 2025: AI-Driven AVNC Review]]
