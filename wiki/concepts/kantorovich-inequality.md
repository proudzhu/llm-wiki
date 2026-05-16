---
type: concept
created: 2026-05-07
updated: 2026-05-07
tags:
  - mathematics
  - inequality
  - beamforming
  - robustness
---

# Kantorovich Inequality

**Category**: Mathematical Inequality / Beamforming Robustness

## Definition

For any Hermitian positive-definite matrix $\mathbf{R}$ with condition number $\kappa = \lambda_{\max}/\lambda_{\min}$, and for any non-zero vector $\mathbf{x}$, the Kantorovich inequality states:

$$\frac{(\mathbf{x}^H \mathbf{x})^2}{(\mathbf{x}^H \mathbf{R} \mathbf{x})(\mathbf{x}^H \mathbf{R}^{-1} \mathbf{x})} \geq \frac{4\kappa}{(\kappa+1)^2}$$

This inequality provides a bound on the efficiency of the preconditioned conjugate gradient method and relates the Rayleigh quotient to the condition number.

## Application to Beamforming (Mittal et al. 2026)

Mittal et al. (2026) apply the Kantorovich inequality to beamforming by setting $\mathbf{R} = \mathbf{R}_y$ (the spatial correlation matrix) and $\mathbf{x} = \mathbf{R}_y^{-1/2}\mathbf{d}$ (where $\mathbf{d}$ is the steering vector). This yields:

$$\frac{W}{M} \geq \frac{4\kappa}{(\kappa+1)^2}$$

where $W$ is the White Noise Gain and $M$ is the number of microphones.

### Derivation Steps

1. $\mathbf{x}^H \mathbf{x} = \mathbf{d}^H \mathbf{R}_y^{-1} \mathbf{d}$
2. $\mathbf{x}^H \mathbf{R}_y \mathbf{x} = \mathbf{d}^H \mathbf{d} = M$
3. $\mathbf{x}^H \mathbf{R}_y^{-1} \mathbf{x} = \mathbf{d}^H \mathbf{R}_y^{-2} \mathbf{d}$
4. Recognizing $W = \frac{(\mathbf{d}^H \mathbf{R}_y^{-1} \mathbf{d})^2}{\mathbf{d}^H \mathbf{R}_y^{-2} \mathbf{d}}$

### Key Result

Setting $A_G = M/W_{\min}$, the maximum allowable condition number is:

$$\kappa_{\max} = (2A_G - 1) + 2\sqrt{A_G(A_G - 1)}$$

This provides a deterministic mapping from desired WNG to required condition number bound, enabling principled adaptive diagonal loading.

## Historical Context

Introduced by Leonid Kantorovich in 1948 (Functional Analysis and Applied Mathematics, Uspekhi Mat Nauk).

## Related Concepts

- [[diagonal-loading|Diagonal Loading]]
- [[white-noise-gain|White Noise Gain]]
- [[condition-number|Condition Number]]
- [[mpdr-beamformer|MPDR Beamformer]]

## Related Sources

- [[sources/mittal-2026-adaptive-diagonal-loading-beamforming|Mittal et al. 2026: Adaptive Diagonal Loading for Norm Constrained Beamforming]]
