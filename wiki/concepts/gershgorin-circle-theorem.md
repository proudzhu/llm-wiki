---
type: concept
created: 2026-05-07
updated: 2026-05-07
tags:
  - mathematics
  - linear-algebra
  - eigenvalue-bounds
  - beamforming
---

# Gershgorin Circle Theorem

**Category**: Linear Algebra / Eigenvalue Bounds

## Definition

For any square matrix $\mathbf{A} \in \mathbb{C}^{n \times n}$, every eigenvalue $\lambda$ lies within at least one Gershgorin disc $D(a_{ii}, R_i)$, where:

$$R_i = \sum_{j \neq i} |a_{ij}|$$

That is, the disc is centered at the diagonal element $a_{ii}$ with radius equal to the sum of absolute off-diagonal elements in that row.

## Application to Beamforming (Mittal et al. 2026)

Mittal et al. (2026) use the Gershgorin Circle Theorem to bound the extreme eigenvalues of the sample SCM without performing a full eigenvalue decomposition. This provides an $\mathcal{O}(M^2)$ alternative to $\mathcal{O}(M^3)$ exact EVD:

$$\lambda_{\max} \leq \max_m \left(\hat{R}_{m,m} + R_m\right)$$

$$\lambda_{\min} \geq \max\left(0, \min_m \left(\hat{R}_{m,m} - R_m\right)\right)$$

where $R_m = \sum_{j \neq m} |\hat{R}_{m,j}|$ for the sample SCM $\hat{\mathbf{R}}_y$.

### Basis Dependence

The Gershgorin bounds are basis-dependent. In the GSC formulation, the unitary blocking matrix $\mathbf{B}$ alters the distribution of matrix energy between diagonal and off-diagonal elements, yielding different loading estimates compared to the direct MPDR domain.

## Performance

- **Near-EVD performance**: Achieves nearly identical output SINR to Exact EVD
- **Moderate complexity**: $\mathcal{O}(M^2)$ vs. $\mathcal{O}(M^3)$ for EVD
- **Best trade-off**: Recommended for practical large-array implementations

## Related Concepts

- [[diagonal-loading|Diagonal Loading]]
- [[condition-number|Condition Number]]
- [[gsc-beamformer|Generalized Sidelobe Canceller]]
- [[mpdr-beamformer|MPDR Beamformer]]

## Related Sources

- [[sources/mittal-2026-adaptive-diagonal-loading-beamforming|Mittal et al. 2026: Adaptive Diagonal Loading for Norm Constrained Beamforming]]
