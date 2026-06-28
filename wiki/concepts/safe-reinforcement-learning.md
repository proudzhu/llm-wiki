---
type: concept
created: 2026-06-28
updated: 2026-06-28
sources:
  - raw/papers/jiang-2025-ai-driven-avnc-review/full-text.md
tags:
  - machine-learning
  - reinforcement-learning
  - safety-critical
  - control-systems
---

# Safe Reinforcement Learning

**Safe Reinforcement Learning (Safe-RL)** extends standard RL by incorporating hard constraints, risk metrics, and formal safety guarantees into policy optimization, enabling deployment in safety-critical engineering applications.

## Overview

Standard RL agents explore freely, which is unacceptable in physical control systems where exploration can cause actuator saturation, structural damage, or instability. Safe-RL integrates safety constraints directly into the learning framework, providing an executable safety assurance layer and formal stability proofs.

## Key Mechanisms

### 1. Constrained MDP (CMDP)
Extends the standard MDP with a cost function $C(s,a)$ and constraint:
$$\mathbb{E}\left[\sum_{t=0}^{T} \gamma^t C(s_t, a_t)\right] \leq d$$
where $d$ is the maximum allowable cumulative cost. The agent maximizes reward subject to this constraint.

### 2. Lyapunov Constraints
Neural Lyapunov functions $V(s)$ provide formal stability proofs by verifying:
$$V(s) > 0, \quad \nabla V(s)^T f(s, \pi(s)) < 0$$
This ensures the closed-loop system converges to a stable equilibrium. However, it requires stringent constraints on network structure, limiting model expressiveness.

### 3. Control Barrier Functions (CBF)
CBFs enforce safety sets as invariant constraints:
$$\sup_{a} \nabla B(s)^T f(s, a) \geq -\alpha(B(s))$$
where $B(s)$ is a barrier function defining the safe set. This ensures the system state remains within safe boundaries.

### 4. Conservative Fallback
A supervisor monitors the running reward at each step. Once performance degradation exceeds a threshold set by a conservative baseline controller, the system reverts to the baseline. This provides a practical safety net during policy exploration.

## Applications in AVNC

- **RL-PID**: PID gains parameterized as DPG agent actions; supervisor reverts to baseline PID when reward degrades.
- **DCDDPG-GESO**: Dual critics take min-Q to suppress overestimation; experience replay and soft updates stabilize training.
- **SAC for chatter suppression**: Soft actor-critic drives piezoelectric actuators for milling vibration control.

## Challenges

- **Stability validation**: Neural Lyapunov learning certificates are difficult to verify for complex systems with large state spaces.
- **Formal verification**: Solvers (SOS, MIP, SMT) are too expensive for real-time control.
- **Uncertainty quantification**: Bayesian deep learning can estimate epistemic uncertainty but adds significant computational burden to the control loop.
- **Domain-specific evaluation criteria**: Most XAI studies rely on anecdotal evidence rather than stable quantitative metrics.

## Related Concepts

- [[concepts/reinforcement-learning-for-control|Reinforcement Learning for Control]]
- [[concepts/active-vibration-control|Active Vibration Control]]
- [[concepts/robust-control|Robust Control]]
- [[concepts/model-predictive-control|Model Predictive Control]]

## Related Sources

- [[sources/jiang-2025-ai-driven-avnc-review|Jiang et al. 2025: AI-Driven AVNC Review]]
