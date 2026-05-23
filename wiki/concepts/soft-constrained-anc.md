---
type: concept
created: 2026-05-23
updated: 2026-05-23
tags:
  - active-noise-control
  - optimization
  - speech-preserving-anc
  - spatially-selective-anc
---

# Soft-Constrained ANC

**Soft-constrained ANC** designs a control filter $\mathbf{w}$ by minimising a single scalar cost that **adds a weighted penalty term** for a secondary objective, instead of imposing it as a hard equality or inequality constraint. The trade-off between competing objectives is governed by a positive scalar $\beta$.

## General Form

A soft-constrained ANC objective typically reads

$$\min_{\mathbf{w}} \;\; \underbrace{\mathbb{E}\{e^2(n)\}}_{\text{noise reduction}} + \underbrace{\mathbf{w}^T \mathbf{B} \mathbf{w}}_{\text{regularisation}} + \beta \cdot \underbrace{\mathcal{D}(\mathbf{w})}_{\text{secondary-objective penalty}},$$

where $e(n)$ is the inner-error microphone signal, $\mathbf{B}$ is a (block-)diagonal regularisation matrix, $\mathcal{D}(\mathbf{w})$ encodes the secondary objective (e.g., distortion of a desired signal, speech preservation), and $\beta \geq 0$ is the trade-off parameter.

When $\mathcal{D}(\mathbf{w})$ is a quadratic form, the cost is convex in $\mathbf{w}$ and admits a closed-form solution.

## Why Soft Instead of Hard Constraints?

| Aspect | Hard constraint | Soft constraint |
|:-------|:----------------|:----------------|
| Feasibility | Can become infeasible under model error | Always has a solution |
| Tuning | Threshold must be chosen | Trade-off parameter must be chosen |
| Sensitivity | Solution lies on constraint boundary | Solution lies in interior — smoother behaviour |
| Closed form | Often requires QP/SOCP | Often a regularised normal-equation solve |

Soft formulations are particularly attractive when the "constraint" is a quality metric (speech distortion, acoustic transparency) rather than a stability or safety condition.

## Examples in ANC

- **Spatially selective ANC** ([[concepts/spatially-selective-anc|SSANC]]) — penalty term measures the deviation between the achieved post-filter response from the desired direction and a target delayed-impulse template using **relative impulse responses (ReIRs)**:

  $$\mathcal{D}(\mathbf{w}) = \| \mathbf{H}(\mathbf{q} + \mathbf{Gw}) - \boldsymbol{\delta}_\Delta \|^2.$$

- **Constrained-output ANC** — penalty term restricts the actuator power $\| \mathbf{w} \|^2$ as part of the cost rather than as a hard upper bound.

- **Robust soft-constrained ANC** — averages the soft cost over a set of $J$ secondary path estimates $\{\mathbf{G}_j\}$ to obtain a single robust control filter ([[sources/xiao-2026-robust-spatially-selective-anc|Xiao 2026]]).

## Choice of $\beta$

The trade-off parameter $\beta$ has a clear operational meaning:

- $\beta \to 0$: pure noise-reduction design — secondary objective ignored.
- $\beta \to \infty$: secondary objective dominates — noise reduction collapses.
- Practical values are chosen by sweeping $\beta$ on a logarithmic grid and inspecting Pareto fronts of the competing metrics (e.g., NR vs. PESQ, NR vs. spectral distortion).

## Relation to Regularisation

The regularisation term $\mathbf{w}^T \mathbf{B} \mathbf{w}$ is itself a soft constraint on the filter norm — preventing ill-conditioned solutions and limiting actuator effort. Splitting feedforward and feedback regularisation weights ($\eta_{FF}$ vs. $\eta_{FB}$) is a common practical refinement.

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/spatially-selective-anc|Spatially Selective ANC]]
- [[concepts/speech-preserving-anc|Speech-Preserving ANC]]
- [[concepts/uncertainty-modeling-for-anc|Uncertainty Modeling for ANC]]
- [[concepts/robust-adaptive-filtering|Robust Adaptive Filtering]]

## Related Sources

- [[sources/xiao-2026-robust-spatially-selective-anc|Xiao 2026: Robust Soft-Constrained SSANC for Hearables]]
