---
type: concept
created: 2026-04-26
updated: 2026-04-26
sources:
tags:
  - active-noise-control
  - robust-control
  - control-theory
---

# Robust Stability Constraint

A **robust stability constraint** is a mathematical condition that guarantees a feedback control system remains stable for all plant variations within a specified uncertainty set. In ANC headphone design, these constraints are imposed at each frequency bin during controller optimization.

## Fundamental Principle

For robust stability, the **critical point** ($-1 + 0j$ in the Nyquist plane) must be excluded from the set of open-loop responses $L_\mu = K_\mu \cdot G_\mu$ for all frequency bins $\mu$ and all $G_\mu \in \Pi_\mu$.

This is equivalent to requiring that the critical point lies **outside** the uncertainty set $\Pi_\mu$ after it has been scaled and rotated by $K_\mu$.

## Constraint Function Formulation

The constraint is expressed as a scalar function $C_\mu(q) < 0$ where:
- $C_\mu(q) < 0$: robust stability is satisfied at frequency bin $\mu$
- $C_\mu(q) \geq 0$: the critical point is inside or on the boundary of the open-loop uncertainty set

The derivation follows a common pattern:
1. Take the inequality that defines the inside of the uncertainty model $\Pi_\mu$
2. Replace "≤" with ">" to test if a point is outside
3. Use the critical point as the test point
4. Substitute $K_\mu$ according to the controller structure (e.g., IMC: $K_\mu = Q_\mu / (1 - \hat{G}_\mu Q_\mu)$)

## Key Insight: Multiplication by $K_\mu$ Transforms the Uncertainty Set

The open-loop uncertainty set is obtained by multiplying all elements of $\Pi_\mu$ by $K_\mu$. This linear operation:

$$|L_\mu| = |K_\mu| \cdot |G_\mu|, \quad \angle L_\mu = \angle K_\mu + \angle G_\mu$$

corresponds to **scaling** (by $|K_\mu|$) and **rotation** (by $\angle K_\mu$) of the uncertainty set. This transformation can be expressed in closed form for each model type:

| Model | Transformation |
|:------|:---------------|
| Disk | $R_\mu' = \|K_\mu\| R_\mu$ (scaling only) |
| Ellipse | $R_{x,\mu}' = \|K_\mu\| R_{x,\mu}$, $R_{y,\mu}' = \|K_\mu\| R_{y,\mu}$, $\theta_\mu' = \theta_\mu + \angle K_\mu$ |
| Convex Hull | $\alpha_{l,\mu}' = \alpha_{l,\mu} + \angle K_\mu$, $B_{l,\mu}' = \|K_\mu\| B_{l,\mu}$ |

## Convexity of Constraints

| Uncertainty Model | Constraint Type | Global Optimum? |
|:------------------|:----------------|:----------------|
| Norm-Bounded (Disk) | Convex | Yes |
| Multi-Disk | Convex | Yes |
| Elliptic | Non-convex | No (local) |
| Convex Hull | Non-convex | No (local) |

The non-convexity of the elliptic and convex hull constraints means that gradient-based optimization (e.g., interior-point methods) can only find local optima. Despite this, the local optima significantly outperform the global optima of the more conservative convex models.

## Optimization Problem

$$\min_q J(q) = \frac{1}{N_\Omega} \sum_{\mu=1}^{N_\Omega} |W_{1,\mu} \cdot [1 - G_\mu Q_\mu(q)]|^2$$

subject to $C_\mu(q) < 0$ for $1 \leq \mu \leq N_\Omega$

where $q$ is the impulse response of the IMC feedforward filter $Q(z)$.

## Related Concepts

- [[../concepts/uncertainty-modeling-for-anc|Uncertainty Modeling for ANC]]
- [[../concepts/convex-hull-uncertainty-model|Convex Hull Uncertainty Model]]
- [[../concepts/elliptic-uncertainty-model|Elliptic Uncertainty Model]]
- [[../concepts/feedback-anc|Feedback ANC]]
- [[../concepts/internal-model-control|Internal Model Control]]
- [[../concepts/socp-optimization|SOCP Optimization]]

## Related Sources

- [[../sources/hilgemann-2024-data-driven-uncertainty-anc|Hilgemann 2024: Data-Driven Uncertainty Modeling for Robust Feedback ANC]]
