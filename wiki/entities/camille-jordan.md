---
type: entity
created: 2026-07-12
updated: 2026-07-12
sources:
  - raw/papers/stewart-1993-early-history-svd/full-text.md
tags:
  - mathematician
  - linear-algebra
  - group-theory
  - history-of-mathematics
---

# Camille Jordan

**Camille Jordan** (1838–1921) was a French mathematician, a leading figure in group theory and linear algebra. He is the **codiscoverer of the singular value decomposition** (1874), publishing his derivation a year after [[entities/eugenio-beltrami|Beltrami]].

## Contributions

- **Singular value decomposition (1874)**: In *Mémoire sur les formes bilinéaires* (J. Math. Pures Appl.), Jordan derived the SVD variationally by maximizing $\mathbf{x}^{\mathrm{T}}\mathbf{A}\mathbf{y}$ subject to $\|\mathbf{x}\|^2 = \|\mathbf{y}\|^2 = 1$. His Lagrange-multiplier derivation is more complete than Beltrami's and elegantly handles degeneracies.
- **Deflation technique**: Jordan introduced a deflation method that uses a partial solution (the largest singular triplet) to reduce the problem to one of smaller size. By extending the singular vectors to orthogonal matrices and observing the resulting block-diagonal structure, he could inductively construct the full SVD. As Stewart notes in [[sources/stewart-1993-early-history-svd|the survey]], this technique "apparently lay fallow until Schur (1917) used it to establish his triangular form."
- **Block matrix**: Jordan used the symmetric block matrix $\left(\begin{smallmatrix} \mathbf{0} & \mathbf{A} \\ \mathbf{A}^{\mathrm{T}} & \mathbf{0} \end{smallmatrix}\right)$, which is still widely used today (popularized by Wielandt and Lanczos in 1958).
- **Jordan canonical form**: His work on canonical forms for matrices and linear transformations.
- **Jordan curve theorem**: The theorem that a simple closed curve separates the plane into two components.

## References

- Jordan, C. *Mémoire sur les formes bilinéaires*. J. Math. Pures Appl., 19:35–54, 1874.
- Stewart, G. W. *On the Early History of the Singular Value Decomposition*. SIAM Review, 35(4):551–566, 1993.
