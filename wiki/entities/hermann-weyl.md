---
type: entity
created: 2026-07-12
updated: 2026-07-12
sources:
  - raw/papers/stewart-1993-early-history-svd/full-text.md
tags:
  - mathematician
  - perturbation-theory
  - spectral-theory
  - mathematical-physics
  - history-of-mathematics
---

# Hermann Weyl

**Hermann Weyl** (1885–1955) was a German mathematician and mathematical physicist, one of the most influential mathematicians of the 20th century. His 1912 contribution to [[concepts/singular-value-decomposition|SVD]] theory provided an elegant **perturbation theory for singular values** and an alternative proof of the approximation theorem.

## Contributions

- **Perturbation theory for singular values (1912)**: In *Das asymptotische Verteilungsgesetz der Eigenwerte linearer partieller Differentialgleichungen* (Math. Ann., 1912), Weyl developed a general perturbation theory. His core lemma states that for any rank-$k$ matrix $\mathbf{B}_k$,
  $$\sigma_1(\mathbf{A} - \mathbf{B}_k) \geq \sigma_{k+1}(\mathbf{A}).$$
- **Weyl's inequality**: For $\mathbf{A} = \mathbf{A}' + \mathbf{A}''$ with singular values in descending order,
  $$\sigma_{i+j-1} \leq \sigma_i' + \sigma_j''. \tag{6.3}$$
  The proof first establishes the $i=j=1$ case via the variational characterization $\sigma_1 = \mathbf{u}_1^{\mathrm{T}}\mathbf{A}\mathbf{v}_1$, then uses the core lemma with best rank-$(i{-}1)$ and rank-$(j{-}1)$ approximations.
- **Approximation theorem (corollary)**: Setting $\mathbf{A}' = \mathbf{A} - \mathbf{B}_k$ and $\mathbf{A}'' = \mathbf{B}_k$ with $\mathrm{rank}(\mathbf{B}_k) = k$ yields $\sigma_i(\mathbf{A} - \mathbf{B}_k) \geq \sigma_{k+i}$, hence
  $$\|\mathbf{A} - \mathbf{B}_k\|^2 \geq \sigma_{k+1}^2 + \cdots + \sigma_n^2,$$
  equivalent to [[entities/erhard-schmidt|Schmidt]]'s result but obtained more elegantly.
- **Spectral-norm perturbation bound**: With $\mathbf{A}' = \mathbf{A}$ and $\mathbf{A}'' = \mathbf{E}$,
  $$|\tilde{\sigma}_i - \sigma_i| \leq \|\mathbf{E}\|_2, \qquad i = 1, \ldots, n,$$
  bounding the maximum change in any singular value by the [[concepts/spectral-norm|spectral norm]] of the perturbation.
- **Weyl's asymptotic law**: Distribution of eigenvalues of the Laplacian on compact domains — the original topic of the 1912 paper.
- **Representation theory, gauge theory, foundations of quantum mechanics**: Foundational contributions across mathematical physics.

## Historical Note

Weyl's paper primarily treated symmetric kernels; he noted in a footnote that his proof extends to the unsymmetric case. As Stewart notes in [[sources/stewart-1993-early-history-svd|the survey]], Weyl's variational approach is "remarkable for its simplicity and elegance" — the approximation theorem falls out as a corollary of the more general perturbation theory.

## References

- Weyl, H. *Das asymptotische Verteilungsgesetz der Eigenwerte linearer partieller Differentialgleichungen*. Math. Ann., 71:441–479, 1912.
- Stewart, G. W. *On the Early History of the Singular Value Decomposition*. SIAM Review, 35(4):551–566, 1993.
