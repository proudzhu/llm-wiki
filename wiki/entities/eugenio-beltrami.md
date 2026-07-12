---
type: entity
created: 2026-07-12
updated: 2026-07-12
sources:
  - raw/papers/stewart-1993-early-history-svd/full-text.md
tags:
  - mathematician
  - linear-algebra
  - differential-geometry
  - history-of-mathematics
---

# Eugenio Beltrami

**Eugenio Beltrami** (1835–1899) was an Italian mathematician known for his work in differential geometry and linear algebra. He is the **first publisher of the singular value decomposition** (1873), which he derived independently of any predecessors.

## Contributions

- **Singular value decomposition (1873)**: In *Sulle funzioni bilineari* (Giornale di Matematiche), Beltrami showed that a bilinear form $\mathbf{x}^{\mathrm{T}}\mathbf{A}\mathbf{y}$ can be diagonalized by orthogonal substitutions $\mathbf{x} = \mathbf{U}\boldsymbol{\xi}$, $\mathbf{y} = \mathbf{V}\boldsymbol{\eta}$, yielding $\boldsymbol{\Sigma} = \mathbf{U}^{\mathrm{T}}\mathbf{A}\mathbf{V}$. He derived the characteristic equations $\mathbf{U}^{\mathrm{T}}(\mathbf{A}\mathbf{A}^{\mathrm{T}}) = \boldsymbol{\Sigma}^2\mathbf{U}^{\mathrm{T}}$ and $(\mathbf{A}^{\mathrm{T}}\mathbf{A})\mathbf{V} = \mathbf{V}\boldsymbol{\Sigma}^2$, and gave an algorithm based on the characteristic polynomial of $\mathbf{A}\mathbf{A}^{\mathrm{T}}$.
  - **Limitations**: The derivation assumed nonsingular $\mathbf{A}$ with distinct singular values, and contained a circularity in the argument for positivity of $\sigma_i^2$.
- **Differential geometry**: Known for interpreting non-Euclidean (Lobachevskian/Bolyai) geometry on a surface of constant negative curvature (the pseudosphere, 1868).

## Historical Note

As Stewart notes in [[sources/stewart-1993-early-history-svd|the survey]], Beltrami's exposition was aimed at students, and "a certain slackness in the exposition suggests that he had not thought the problem through" — yet he remains the first to publish the SVD.

## References

- Beltrami, E. *Sulle funzioni bilineari*. Giornale di Matematiche, 11:98–106, 1873.
- Stewart, G. W. *On the Early History of the Singular Value Decomposition*. SIAM Review, 35(4):551–566, 1993.
