---
type: concept
created: 2026-04-26
updated: 2026-04-26
sources:
tags:
  - active-noise-control
  - robust-control
  - convex-geometry
  - uncertainty-modeling
---

# Convex Hull Uncertainty Model

The **convex hull uncertainty model** represents plant variations as the smallest convex polyhedral region containing all observed frequency responses. It achieves the minimal model area among contiguous uncertainty models, providing the greatest design freedom for robust controller optimization.

## Definition

At each frequency bin $\mu$, the model is defined as the intersection of $m_\mu$ half-spaces:

$$\Pi_\mu^{(CH)} = \bigcap_{l=1}^{m_\mu} \left\{ G \in \mathbb{C} : A_{0l,\mu} \Re(G) + A_{1l,\mu} \Im(G) + B_{l,\mu} \leq 0 \right\}$$

Parameters:
- $m_\mu$: number of half-spaces (facets of the convex hull)
- $A_{0l,\mu}$, $A_{1l,\mu}$: weights defining the normal direction of each half-space
- $B_{l,\mu}$: offset of each half-space from the origin

Obtained via the **quickhull algorithm** (Barber et al., 1996).

## Key Properties

1. **Minimal area**: Among all convex, contiguous models, the convex hull covers the least area — only ~60% of the norm-bounded disk area on average
2. **Inherent contiguity**: Being a single convex region, it automatically covers transitions between fits (e.g., normal → loose), unlike the tri-rectangle model
3. **Non-convex constraint**: The resulting robust stability constraint is non-convex in the optimization variable $q$, requiring local optima

## Robust Stability Constraint

When the controller multiplies the uncertainty set by $K_\mu$, the convex hull transforms:

$$\alpha_{l,\mu}' = \alpha_{l,\mu} + \angle K_\mu, \quad B_{l,\mu}' = |K_\mu| B_{l,\mu}$$

The constraint that the critical point ($-1$) lies outside the open-loop uncertainty set becomes:

$$C_\mu^{(CH)}(q) = \min\left(V_{1,\mu}(q), \ldots, V_{m_\mu,\mu}(q)\right)$$

where:

$$V_{l,\mu}(q) = \cos(\alpha_{l,\mu}) \Re(W_\mu(q)) - \sin(\alpha_{l,\mu}) \Im(W_\mu(q)) - |Q_\mu(q)| B_{l,\mu}$$

The non-smooth min-function is approximated by:

$$\min(x_1, \ldots, x_m) \approx -\frac{1}{\rho} \log \sum_{l=1}^{m} \exp(-\rho x_l)$$

which approaches the true min as $\rho \to \infty$.

## Performance

In Hilgemann et al. (2024), the convex hull model achieved:
- **Objective**: $J^{(CH)}(q) = 0.54$ (vs. 1.11 for disk)
- **+18 dB improvement** at 300 Hz over the disk model for over-ear headphones
- **No instability** observed across all fit conditions with 21 human wearers

## Comparison with Other Models

| Property | Convex Hull | [[concepts/elliptic-uncertainty-model|Elliptic]] | Multi-Disk | Disk |
|:---------|:-----------|:---------|:-----------|:-----|
| Area | Smallest | Small | Medium | Largest |
| Contiguity | Yes | Yes | Yes | Yes |
| Constraint | Non-convex | Non-convex | Convex | Convex |
| Global optimum | No | No | Yes | Yes |
| Fit transitions | Covered | Covered | Covered | Covered |

## Related Concepts

- [[concepts/uncertainty-modeling-for-anc|Uncertainty Modeling for ANC]]
- [[concepts/elliptic-uncertainty-model|Elliptic Uncertainty Model]]
- [[concepts/robust-stability-constraint|Robust Stability Constraint]]
- [[concepts/feedback-anc|Feedback ANC]]
- [[concepts/internal-model-control|Internal Model Control]]

## Related Sources

- [[sources/hilgemann-2024-data-driven-uncertainty-anc|Hilgemann 2024: Data-Driven Uncertainty Modeling for Robust Feedback ANC]]
