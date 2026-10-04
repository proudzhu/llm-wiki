---
type: concept
created: 2026-10-04
updated: 2026-10-04
sources:
  - raw/papers/scheibler-2021-log-quadratically-penalized-iva/full-text.md
tags:
  - optimization-algorithms
  - numerical-algorithms
  - blind-source-separation
  - independent-vector-analysis
---

# Log-Quadratically Penalized Quadratic Minimization (LQPQM)

**LQPQM** is a class of non-convex optimization problems introduced and solved by [[entities/robin-scheibler|Robin Scheibler]] (IEEE TSP 2021): minimize a quadratic form *minus* the logarithm of another quadratic form (plus offset). Despite non-convexity — the log term pinches the quadratic bowl upward and can create up to $2d+1$ stationary points in $d$ dimensions — its **global minimum can be computed efficiently**, as the largest zero of a secular equation.

## Key Formulations

### Problem statement

For $\boldsymbol{A},\boldsymbol{C}\in\mathbb{C}^{d\times d}$ Hermitian positive (semi-)definite, $\boldsymbol{b},\boldsymbol{d}\in\mathbb{C}^{d}$, $z\ge 0$:

$$
\min_{\boldsymbol{x}\in\mathbb{C}^{d}}\ (\boldsymbol{x}-\boldsymbol{b})^{\mathsf{H}}\boldsymbol{A}(\boldsymbol{x}-\boldsymbol{b})-\log\left((\boldsymbol{x}-\boldsymbol{d})^{\mathsf{H}}\boldsymbol{C}(\boldsymbol{x}-\boldsymbol{d})+z\right)
$$

A Cholesky factor $\boldsymbol{G}$ of $\boldsymbol{A}$ (with $\boldsymbol{U}=\boldsymbol{G}^{-\mathsf{H}}\boldsymbol{C}\boldsymbol{G}^{-1}$, $\boldsymbol{v}=\boldsymbol{G}(\boldsymbol{b}-\boldsymbol{d})$) reduces it to the canonical form

$$
\min_{\boldsymbol{y}\in\mathbb{C}^{d}}\ \boldsymbol{y}^{\mathsf{H}}\boldsymbol{y}-\log\left((\boldsymbol{y}+\boldsymbol{v})^{\mathsf{H}}\boldsymbol{U}(\boldsymbol{y}+\boldsymbol{v})+z\right)
$$

### Solution via a secular equation

Let $\boldsymbol{U}=\boldsymbol{\Sigma}\boldsymbol{\Phi}\boldsymbol{\Sigma}^{\mathsf{H}}$ be the eigendecomposition with eigenvalues $\varphi_1\le\ldots\le\varphi_d$, and $\tilde{\boldsymbol{v}}=\boldsymbol{\Sigma}^{\mathsf{H}}\boldsymbol{v}$.

- **Special case $\boldsymbol{v}=0$**: the solution follows from the eigendecomposition alone — $\boldsymbol{y}^{\star}=0$ if $z\ge\varphi_d$, otherwise the top eigenvector scaled by $\sqrt{(\varphi_d-z)/(\boldsymbol{\sigma}_d^{\mathsf{H}}\boldsymbol{U}\boldsymbol{\sigma}_d)}$.
- **General case $\boldsymbol{v}\neq 0$**: every stationary point is of the form
$$
\boldsymbol{y}(\lambda)=(\lambda\boldsymbol{I}-\boldsymbol{U})^{-1}\boldsymbol{U}\boldsymbol{v}
$$
where $\lambda$ is a zero of the **secular equation**
$$
f(\lambda)=\lambda^{2}\sum_{m\in\mathcal{S}}\frac{\varphi_{m}|\tilde{v}_{m}|^{2}}{(\lambda-\varphi_{m})^{2}}-\lambda+z,
\qquad
\mathcal{S}=\{m:\varphi_m|\tilde v_m|^2\neq 0\}
$$

The objective along the stationary branch,

$$
g(\lambda)=1-\sum_{m\in\mathcal{S}}\frac{\varphi_{m}|\tilde{v}_{m}|^{2}}{\lambda-\varphi_{m}}-\frac{z}{\lambda}-\log\lambda,
$$

satisfies $g'(\lambda)=f(\lambda)/\lambda^{2}$: the objective **decreases for increasing roots**, so the global minimum is the **largest zero** of $f$. That zero is the unique root in $(\max(\varphi_{\max},z),+\infty)$, an interval where $f$ is strictly decreasing — so Newton-Raphson converges reliably.

### Root-finding recipe

1. **Initialization**: retain only the dominant $(\varphi_{\max},\tilde v_{\max})$ term and clear denominators to get a cubic polynomial; its largest real root is a safe, accurate start.
2. **Stabilization**: solve in scaled variables $\hat f(\mu)=f(\varphi_{\max}\mu)/\varphi_{\max}$ to avoid overflow of $(\lambda-\varphi_m)^{-2}$; fall back to bisection-style halving when a Newton step lands below $\varphi_{\max}$.

## Why It Matters

- **Origin**: LQPQM arises as the exact subproblem of the [[concepts/iterative-projection-with-adjustment|IPA]] update for [[concepts/independent-vector-analysis|AuxIVA]], where the adjustment vector $\boldsymbol{q}$ of the other sources' demixing filters must minimize a quadratic surrogate with a log-determinant penalty.
- **Connections**: the secular-equation structure is reminiscent of modified eigenvalue problems (Golub 1973), generalized trust-region subproblems, and applications in robust beamforming, multi-lateration, and DOA estimation — but the LQPQM itself had reportedly not been solved before 2021.
- **Speculated uses beyond BSS** (per the original paper): barrier-function interior-point methods, and information-theoretic capacity maximization subject to quadratic penalties or constraints.

## Related Concepts

- [[concepts/iterative-projection-with-adjustment|Iterative Projection with Adjustment (IPA)]] — the AuxIVA update that LQPQM solves
- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/generalized-eigenvalue-decomposition|Generalized Eigenvalue Decomposition]] — the $\boldsymbol{v}=0$ special case and the underlying eigenstructure
- [[concepts/quadratic-programming|Quadratic Programming]] — convex sibling without the log penalty

## Related Sources

- [[sources/scheibler-2021-log-quadratically-penalized-iva|Scheibler 2021: Independent Vector Analysis via Log-Quadratically Penalized Quadratic Minimization]] — introduces and solves the problem
