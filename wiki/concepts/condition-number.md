---
type: concept
created: 2026-05-07
updated: 2026-05-07
tags:
  - mathematics
  - linear-algebra
  - beamforming
  - robustness
---

# Condition Number

**Category**: Linear Algebra / Matrix Analysis

## Definition

For a matrix $\mathbf{A}$, the condition number $\kappa(\mathbf{A})$ quantifies how sensitive the solution of a linear system $\mathbf{A}\mathbf{x} = \mathbf{b}$ is to perturbations in $\mathbf{b}$. For the spectral norm (2-norm):

$$\kappa(\mathbf{A}) = \frac{\sigma_{\max}(\mathbf{A})}{\sigma_{\min}(\mathbf{A})}$$

For Hermitian positive-definite matrices (such as spatial correlation matrices):

$$\kappa(\mathbf{A}) = \frac{\lambda_{\max}}{\lambda_{\min}}$$

where $\lambda_{\max}$ and $\lambda_{\min}$ are the maximum and minimum eigenvalues.

## Interpretation

- **$\kappa \approx 1$**: Well-conditioned; small input perturbations cause small output perturbations
- **$\kappa \gg 1$**: Ill-conditioned; small input perturbations cause large output perturbations
- **$\kappa \to \infty$**: Singular (rank-deficient); inversion is impossible

## Relevance to Beamforming

In adaptive beamforming, the sample SCM $\hat{\mathbf{R}}_y$ becomes ill-conditioned under snapshot deficiency ($L < M$ or $L \approx M$). This causes:

1. The inverse $\hat{\mathbf{R}}_y^{-1}$ to amplify minor estimation errors
2. The weight vector norm $\|\mathbf{w}\|^2$ to spike
3. WNG collapse and target signal cancellation

## Condition Number Control via Diagonal Loading

Diagonal loading shifts all eigenvalues by $\mu$:

$$\kappa_{loaded} = \frac{\lambda_{\max} + \mu}{\lambda_{\min} + \mu}$$

As $\mu \to \infty$, $\kappa_{loaded} \to 1$ (perfectly conditioned, but no adaptive nulling).

### Kantorovich-Bounded $\kappa_{\max}$ (Mittal et al. 2026)

Mittal et al. (2026) derive the maximum allowable condition number from the desired WNG bound:

$$\kappa_{\max} = (2A_G - 1) + 2\sqrt{A_G(A_G - 1)}$$

where $A_G = M/W_{\min}$. This enables principled selection of the diagonal loading parameter.

## Related Concepts

- [[diagonal-loading|Diagonal Loading]]
- [[kantorovich-inequality|Kantorovich Inequality]]
- [[white-noise-gain|White Noise Gain]]
- [[gershgorin-circle-theorem|Gershgorin Circle Theorem]]
- [[generalized-eigenvalue-decomposition|Generalized Eigenvalue Decomposition]]

## Related Sources

- [[sources/mittal-2026-adaptive-diagonal-loading-beamforming|Mittal et al. 2026: Adaptive Diagonal Loading for Norm Constrained Beamforming]]
