---
type: concept
created: 2026-04-26
updated: 2026-04-26
sources:
tags:
  - active-noise-control
  - robust-control
  - uncertainty-modeling
---

# Elliptic Uncertainty Model

The **elliptic uncertainty model** represents plant variations as an ellipse in the complex plane at each frequency bin. It captures elongated distributions (e.g., variations primarily along one axis) with only four parameters, offering a good balance between modeling accuracy and simplicity.

## Definition

$$\Pi_\mu^{(E)} = \left\{ G \in \mathbb{C} : \left(\frac{X_\mu}{R_{x,\mu}}\right)^2 + \left(\frac{Y_\mu}{R_{y,\mu}}\right)^2 \leq 1 \right\}$$

with rotated coordinates:

$$X_\mu = \cos(\theta_\mu) \Re(\Delta G_\mu) + \sin(\theta_\mu) \Im(\Delta G_\mu)$$
$$Y_\mu = \sin(\theta_\mu) \Re(\Delta G_\mu) - \cos(\theta_\mu) \Im(\Delta G_\mu)$$

where $\Delta G_\mu = G - G_\mu^{(0)}$.

Parameters:
- $G_\mu^{(0)}$: ellipse center
- $R_{x,\mu}$: semi-major axis
- $R_{y,\mu}$: semi-minor axis
- $\theta_\mu$: angle between $R_{x,\mu}$ and the real axis

Obtained from the **smallest enclosing ellipse** (Löwner-John ellipsoid) via Welzl's algorithm or convex optimization.

## Special Case

When $R_{x,\mu} = R_{y,\mu}$, the ellipse degenerates to the norm-bounded (disk) model. The disk is always a special case of the ellipse.

## Robust Stability Constraint

When the controller multiplies the uncertainty set by $K_\mu$, the ellipse transforms:

$$R_{x,\mu}' = |K_\mu| R_{x,\mu}, \quad R_{y,\mu}' = |K_\mu| R_{y,\mu}, \quad \theta_\mu' = \theta_\mu + \angle K_\mu$$

The constraint function is:

$$C_\mu^{(E)}(q) = |Q_\mu(q)| - \frac{X_\mu'^2(q)}{R_{x,\mu}^2} - \frac{Y_\mu'^2(q)}{R_{y,\mu}^2}$$

This is **non-convex** in $q$ because $X_\mu'^2$ and $Y_\mu'^2$ are subtracted.

## Performance

In Hilgemann et al. (2024):
- **Objective**: $J^{(E)}(q) = 0.56$ (vs. 1.11 for disk, 0.54 for convex hull)
- Significant improvement over disk model for **over-ear** headphones
- Did **not** improve over multi-disk for **in-ear** headphones — the uncertainty shape for in-ear devices is different

## When the Elliptic Model Helps

The elliptic model is most beneficial when:
- Observations cluster in an elongated shape (e.g., primarily along the imaginary axis at low frequencies)
- The aspect ratio $R_{x,\mu}/R_{y,\mu}$ is significantly different from 1
- At mid-frequencies (~2.8 kHz) where variations follow a line at ~30° angle

It is less beneficial when:
- Variations are quasi-circular (high frequencies ~4.6 kHz) — the disk model is already adequate
- The distribution is irregular and non-elliptical — the [[concepts/convex-hull-uncertainty-model|Convex Hull Uncertainty Model]] is better

## Related Concepts

- [[concepts/uncertainty-modeling-for-anc|Uncertainty Modeling for ANC]]
- [[concepts/convex-hull-uncertainty-model|Convex Hull Uncertainty Model]]
- [[concepts/robust-stability-constraint|Robust Stability Constraint]]
- [[concepts/feedback-anc|Feedback ANC]]
- [[concepts/internal-model-control|Internal Model Control]]

## Related Sources

- [[sources/hilgemann-2024-data-driven-uncertainty-anc|Hilgemann 2024: Data-Driven Uncertainty Modeling for Robust Feedback ANC]]
