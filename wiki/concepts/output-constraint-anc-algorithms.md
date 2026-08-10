---
type: concept
created: 2026-08-10
updated: 2026-08-10
sources:
  - raw/papers/guo-2024-anc-saturation-survey/full-text.md
tags:
  - active-noise-control
  - adaptive-filtering
  - fxlms
  - output-constraint-algorithms
  - optimization
---

# Output Constraint ANC Algorithms

## Overview

**Output constraint ANC algorithms** are a family of [[filtered-x-lms-algorithm|FxLMS]] variants that mitigate the [[output-saturation-effect|output saturation effect]] by **limiting the output power** of the control filter so the secondary-path amplifier remains in its linear region. They are one of the two complementary families of saturation-mitigation algorithms distinguished by [[sources/guo-2024-anc-saturation-survey|Guo et al. 2024]], the other being [[nonlinear-active-noise-control|nonlinear adaptive algorithms]].

Output constraint algorithms are the practical default for severe saturation: they preserve adaptive-filter stability at the cost of not fully cancelling the disturbance, while nonlinear adaptive algorithms diverge under the same conditions.

## Unified Optimisation Framework

The survey formulates output-constrained ANC as a **quadratically constrained quadratic program** (QCQP):

$$\min_\mathbf{w} J(\mathbf{w}) = \mathbb{E}\!\left[\left|d(n) - \textstyle\sum_l s_l \mathbf{w}^T(n{-}l)\mathbf{x}(n{-}l)\right|^2\right] \quad \text{s.t.}\ \ g(\mathbf{w}) = \mathbb{E}[|\mathbf{w}^T(n)\mathbf{x}(n)|^2] \le \rho^2,$$

whose KKT solution is

$$\mathbf{w}_o = (\lambda_o \mathbf{R}_x + \mathbf{R}_{x'})^{-1} \mathbf{P}_{dx'},$$

with the Lagrange factor $\lambda_o$ vanishing when the constraint is inactive. All surveyed output constraint algorithms are recursive approximations of this same optimum; they differ in the choice of leakage matrix or penalty factor used to realise $\lambda_o$ online.

## Algorithm Family

| Algorithm | Mechanism | Constraint type | Complexity (multiplications) |
|:----------|:----------|:----------------|:------------------------------|
| **2-GD FxLMS** (Shi 2019) | Two gradient directions: standard FxLMS update when $|y(n)| \le C$, weight-reduction update otherwise | Amplitude | $2N + L + 1$ (matches FxLMS) |
| **Re-scaling FxLMS** (Qiu & Hansen 2001) | Rescales $\mathbf{w}(n{+}1)$ and $y(n{+}1)$ by $C/|y(n{+}1)|$ when threshold exceeded | Amplitude | $3N + L + 2$ |
| **[[leaky-fxlms-algorithm\|Leaky FxLMS]]** | Scalar leakage factor $\lambda$ penalises $\mathbf{w}^T\mathbf{w}$ in the cost function | Power (scalar) | $3N + L + 1$ |
| **Extended Leaky FxLMS** (Wu 2018) | Matrix leakage $\boldsymbol{\gamma} = \mathbf{C}^T\mathbf{C}$ for more control freedom | Power (matrix) | $2N^2 + 2N + L + 1$ |
| **MOV FxLMS** (Shi 2021) | Penalty on output variance $\alpha\,\mathbb{E}[y^2(n)]$ added to MSE cost | Power | $3N + L + 1$ (basic); $4N + L + 7$ (optimal) |
| **OLFxLMS** (Optimal Leaky) | Sets $\boldsymbol{\gamma} = \Lambda_o \mathbf{R}_x$ so extended Leaky converges to the QCQP optimum; estimates $G_s$ via inverse modeling | Optimal power | $2N^2 + 2N + L$ |
| **Optimal MOV FxLMS** | Sets $\alpha = \Lambda_o$ so MOV converges to the QCQP optimum | Optimal power | $4N + L + 7$ |
| **MOV-Modified FxLMS** (Lai 2023) | Online estimation of $G_s \approx \sigma_{x'}^2/\sigma_x^2$ via moving filter; variable penalty $\alpha(n)$ | Optimal power (online) | $4N + L + K + 7$ |

$N$ = control filter length, $L$ = secondary-path length, $K$ = moving filter length.

## Convergence to the QCQP Optimum

OLFxLMS and Optimal MOV FxLMS are the two algorithms that explicitly converge to the QCQP optimum, by setting their leakage matrix / penalty factor equal to the optimal Lagrange factor times the input autocorrelation matrix:

- OLFxLMS: $\boldsymbol{\gamma} = \Lambda_o \mathbf{R}_x$
- Optimal MOV FxLMS: $\alpha = \Lambda_o$

Both require an estimate of the secondary-path power gain $G_s$, traditionally obtained offline via inverse modeling of the secondary path. **MOV-Modified FxLMS** removes this bottleneck by estimating $G_s$ online as the ratio $\sigma_{x'}^2 / \sigma_x^2$ via a moving-average filter, allowing the algorithm to track time-varying noise and acoustic environments while still converging to the constrained optimum.

## Complexity and Practicality

Compared with the [[nonlinear-active-noise-control|nonlinear adaptive]] family:

- **Linear complexity in $N$** for most variants (2-GD, Leaky, Re-scaling, MOV, MOV-Modified). Only the optimal-leaky variants (OLFxLMS, Extended Leaky) go quadratic in $N$ due to the matrix leakage.
- **Real-time feasibility**: Implementable on standard DSPs; MOV-Modified supports online penalty tuning for dynamic environments.
- **Stability under severe saturation**: Preserved by design — the constraint forces the amplifier into its linear region, preventing the filter divergence that unconstrained algorithms exhibit.

## When to Use

Output constraint algorithms are required whenever the disturbance level pushes the amplifier into its **severe saturation** region, i.e. when the fundamental component cannot be fully attenuated. Under **mild saturation** (only harmonics remain), [[nonlinear-active-noise-control|nonlinear adaptive algorithms]] are advantageous because their pre-distortion strategy can cancel the harmonics that output constraint leaves behind.

## Related Concepts

- [[concepts/output-saturation-effect|Output Saturation Effect]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/leaky-fxlms-algorithm|Leaky FxLMS Algorithm]]
- [[concepts/nonlinear-active-noise-control|Nonlinear Active Noise Control]]
- [[concepts/quadratic-programming|Quadratic Programming]] — QCQP formulation
- [[concepts/secondary-path-modeling|Secondary Path Modeling]] — inverse modeling for power-gain estimation
- [[concepts/minimum-variance-control|Minimum Variance Control]] — related but distinct (output-variance vs. output-power constraint)

## Related Sources

- [[sources/guo-2024-anc-saturation-survey|Guo et al. 2024: ANC Algorithms Overcoming Output Saturation]]
