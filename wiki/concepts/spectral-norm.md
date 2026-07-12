---
type: concept
created: 2026-07-12
updated: 2026-07-12
sources:
  - raw/papers/stewart-1993-early-history-svd/full-text.md
tags:
  - linear-algebra
  - matrix-norm
  - perturbation-theory
  - numerical-analysis
---

# Spectral Norm

The **spectral norm** (or **2-norm**) of a matrix $\mathbf{A}$ is its largest singular value:

$$\|\mathbf{A}\|_2 = \sigma_1(\mathbf{A}) = \max_{\mathbf{x} \neq \mathbf{0}} \frac{\|\mathbf{A}\mathbf{x}\|_2}{\|\mathbf{x}\|_2}.$$

It is the operator norm induced by the Euclidean vector norm, and is a unitarily invariant norm: $\|\mathbf{U}\mathbf{A}\mathbf{V}\|_2 = \|\mathbf{A}\|_2$ for any orthogonal (or unitary) $\mathbf{U}, \mathbf{V}$.

## Variational Characterization

For a real matrix $\mathbf{A}$, the spectral norm admits the variational form

$$\sigma_1 = \max_{\|\mathbf{u}\|=\|\mathbf{v}\|=1} \mathbf{u}^{\mathrm{T}}\mathbf{A}\mathbf{v} = \sqrt{\lambda_{\max}(\mathbf{A}^{\mathrm{T}}\mathbf{A})},$$

where the maximum is attained by the leading left and right singular vectors. This characterization, used by [[entities/camille-jordan|Jordan]] (1874) and [[entities/hermann-weyl|Weyl]] (1912), is central to the early derivations of the [[concepts/singular-value-decomposition|SVD]].

## Role in Perturbation Theory

Weyl's inequality (1912) gives the fundamental perturbation bound on singular values:

$$|\tilde{\sigma}_i - \sigma_i| \leq \|\mathbf{E}\|_2, \qquad i = 1, \ldots, n,$$

where $\mathbf{E} = \tilde{\mathbf{A}} - \mathbf{A}$ is the perturbation. The spectral norm of $\mathbf{E}$ thus bounds the worst-case change in any singular value. This is a stronger statement than might first appear: singular values are **perfectly conditioned** — each $\sigma_i$ has condition number 1 with respect to additive perturbations, regardless of whether $\sigma_i$ is large or small.

The spectral norm also governs the **best rank-$k$ approximation error** ([[concepts/eckart-young-theorem|Eckart–Young theorem]]):

$$\min_{\mathrm{rank}(\mathbf{B}) \leq k} \|\mathbf{A} - \mathbf{B}\|_2 = \sigma_{k+1}(\mathbf{A}).$$

## Related Norms

- **Frobenius norm**: $\|\mathbf{A}\|_F = \sqrt{\sum_i \sigma_i^2}$. Also unitarily invariant, but aggregates all singular values rather than only the largest.
- The spectral and Frobenius norms are the two most commonly used unitarily invariant norms, related by $\|\mathbf{A}\|_2 \leq \|\mathbf{A}\|_F \leq \sqrt{r}\,\|\mathbf{A}\|_2$ where $r = \mathrm{rank}(\mathbf{A})$.

## References

- Weyl, H. *Das asymptotische Verteilungsgesetz der Eigenwerte linearer partieller Differentialgleichungen*. Math. Ann., 71:441–479, 1912.
- Stewart, G. W. *On the Early History of the Singular Value Decomposition*. SIAM Review, 35(4):551–566, 1993.
