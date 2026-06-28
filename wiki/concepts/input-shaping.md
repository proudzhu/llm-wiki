---
type: concept
created: 2026-06-28
updated: 2026-06-28
sources:
  - raw/papers/jiang-2025-ai-driven-avnc-review/full-text.md
tags:
  - control-theory
  - vibration-control
  - feedforward-control
  - flexible-structures
---

# Input Shaping

**Input Shaping (IS)** is a feedforward control technique that modifies the command input to a flexible system by convolving it with a sequence of impulses, designed to cancel residual vibrations at the system's natural frequencies.

## Overview

First systematized by Singer and Seering (1990), input shaping generates a command signal that excites the system's modes in such a way that the residual vibrations from each impulse cancel each other out. The technique is particularly effective for underdamped flexible structures where overshoot and residual vibration must be minimized (e.g., cranes, robot arms, spacecraft solar panels).

## Core Principle

The shaped input is a convolution of the original command with a sequence of impulses:

$$u_{shaped}(t) = \sum_{i=1}^{n} A_i \delta(t - t_i) * u_{cmd}(t)$$

where $A_i$ and $t_i$ are the amplitudes and time locations of the impulses, chosen such that the residual vibration amplitude is zero (or minimized) at the system's natural frequencies.

## AI-Enhanced Input Shaping

Traditional input shaping requires accurate knowledge of modal frequencies and damping ratios. AI methods address this limitation:

| Method | AI Role | Advantage | Limitation |
|--------|---------|-----------|------------|
| **ANN-based IS** | DNN maps frequency response to shaper parameters | 50%+ residual amplitude reduction at 40% frequency mismatch | Requires training data covering expected frequency range |
| **RL-based IS** | RL searches policy space for optimal impulse timing | No gradient model needed; adapts to nonlinear constraints | Low sample efficiency; exploration risk on hardware |
| **PINN-based IS** | Physics constraints embedded in loss | Extrapolation robustness; physical consistency | Sensitive to prior model accuracy and loss weight tuning |

## Key Challenges

- **Modal parameter sensitivity**: Shaper design heavily relies on accurate modal frequencies and damping. Environmental drift causes pulse mismatch.
- **Online adaptability**: Pre-tuned pulse sequences fail under varying loads or sudden changes in joint flexibility.
- **Delay trade-off**: Robust shapers extend pulse sequences to improve tolerance, but this introduces additional command delay.

## Related Concepts

- [[concepts/active-vibration-control|Active Vibration Control]]
- [[concepts/physics-informed-neural-network|Physics-Informed Neural Network]]
- [[concepts/reinforcement-learning-for-control|Reinforcement Learning for Control]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]

## Related Sources

- [[sources/jiang-2025-ai-driven-avnc-review|Jiang et al. 2025: AI-Driven AVNC Review]]
