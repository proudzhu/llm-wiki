---
type: concept
created: 2026-07-12
updated: 2026-07-12
sources:
  - raw/papers/stewart-1993-early-history-svd/full-text.md
tags:
  - linear-algebra
  - matrix-decomposition
  - numerical-analysis
  - matrix-computations
---

# Singular Value Decomposition

The **singular value decomposition (SVD)** is a factorization of a real or complex matrix into the product of two orthogonal (or unitary) matrices and a diagonal matrix of nonnegative real numbers. It is one of the most useful tools in numerical linear algebra, with applications in data compression, principal component analysis, signal processing, statistics, and psychometrics.

## Definition

For a real $m \times n$ matrix $\mathbf{A}$, the (full) SVD is

$$\mathbf{A} = \mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^{\mathrm{T}},$$

where:

- $\mathbf{U} \in \mathbb{R}^{m \times m}$ is orthogonal ($\mathbf{U}^{\mathrm{T}}\mathbf{U} = \mathbf{I}$),
- $\mathbf{V} \in \mathbb{R}^{n \times n}$ is orthogonal ($\mathbf{V}^{\mathrm{T}}\mathbf{V} = \mathbf{I}$),
- $\boldsymbol{\Sigma} \in \mathbb{R}^{m \times n}$ is diagonal, with entries $\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_{\min(m,n)} \geq 0$.

The $\sigma_i$ are the **singular values**, the columns of $\mathbf{U}$ are the **left singular vectors**, and the columns of $\mathbf{V}$ are the **right singular vectors**. The singular values are the square roots of the eigenvalues of $\mathbf{A}^{\mathrm{T}}\mathbf{A}$ (equivalently $\mathbf{A}\mathbf{A}^{\mathrm{T}}$).

## Key Properties

- **Existence**: Every matrix has an SVD. This was first established by [[entities/eugenio-beltrami|Beltrami]] (1873) and [[entities/camille-jordan|Jordan]] (1874) for square nonsingular real matrices, and extended to general and complex matrices by Autonne (1913) and Eckart & Young (1939).
- **Best rank-$k$ approximation** ([[concepts/eckart-young-theorem|Eckart–Young theorem]]): The truncated SVD $\mathbf{A}_k = \sum_{i=1}^k \sigma_i \mathbf{u}_i \mathbf{v}_i^{\mathrm{T}}$ is the best rank-$k$ approximation to $\mathbf{A}$ in any unitarily invariant norm, with $\|\mathbf{A} - \mathbf{A}_k\|_2 = \sigma_{k+1}$ and $\|\mathbf{A} - \mathbf{A}_k\|_F^2 = \sum_{i=k+1}^r \sigma_i^2$.
- **Perturbation stability** ([[entities/hermann-weyl|Weyl]] 1912): $|\tilde{\sigma}_i - \sigma_i| \leq \|\mathbf{E}\|_2$ — singular values are perfectly conditioned under additive perturbation, bounded by the [[concepts/spectral-norm|spectral norm]] of the perturbation.
- **Relation to fundamental subspaces**: The first $r$ columns of $\mathbf{U}$ span the column space of $\mathbf{A}$; the last $m-r$ span the left null space. The first $r$ columns of $\mathbf{V}$ span the row space; the last $n-r$ span the null space.

## Early History

The SVD was discovered independently at least three times between 1873 and 1907, in two parallel traditions (linear algebra and integral equations). The full history is surveyed in [[sources/stewart-1993-early-history-svd|Stewart 1993]]:

| Year | Discoverer | Tradition | Key innovation |
|------|------------|-----------|----------------|
| 1873 | [[entities/eugenio-beltrami|Beltrami]] | Bilinear forms | First publication; characteristic equation of $\mathbf{A}\mathbf{A}^{\mathrm{T}}$ |
| 1874 | [[entities/camille-jordan|Jordan]] | Bilinear forms | Variational derivation; **deflation**; block matrix $\left(\begin{smallmatrix}\mathbf{0} & \mathbf{A} \\ \mathbf{A}^{\mathrm{T}} & \mathbf{0}\end{smallmatrix}\right)$ |
| 1889 | [[entities/james-joseph-sylvester|Sylvester]] | Bilinear forms | Independent rediscovery; minors rule; infinitesimal iteration |
| 1907 | [[entities/erhard-schmidt|Schmidt]] | Integral equations | Function-space generalization; **approximation theorem** |
| 1912 | [[entities/hermann-weyl|Weyl]] | Integral equations | **Perturbation theory**; Weyl's inequality; spectral-norm bound |

## Modern Computational Algorithms

- **Golub–Kahan (1965)**: Bidiagonalization via Householder reflections, followed by a variant of the QR algorithm.
- **Golub–Reinsch (1970)**: The standard practical algorithm, widely implemented in LAPACK.
- **Demmel–Kahan (1990)**: Accurate one-sided Jacobi SVD for bidiagonal matrices, especially for small singular values.

## Applications

- **Principal component analysis (PCA)**: Hotelling (1933) — the SVD of a centered data matrix gives the principal components.
- **Low-rank approximation / compression**: Truncated SVD for image compression, denoising, and latent semantic analysis.
- **Pseudoinverse**: $\mathbf{A}^+ = \mathbf{V}\boldsymbol{\Sigma}^+\mathbf{U}^{\mathrm{T}}$ (Moore 1920, Penrose 1955) — the minimum-norm least-squares solution to $\mathbf{A}\mathbf{x} = \mathbf{b}$.
- **Total least squares**: SVD of the augmented data matrix.
- **Signal processing and statistics**: Subspace methods, canonical correlations (Hotelling 1936).

## Related Concepts

- [[concepts/eckart-young-theorem|Eckart–Young Theorem]] — the best low-rank approximation property
- [[concepts/spectral-norm|Spectral Norm]] — the unitarily invariant norm arising in perturbation bounds

## References

- Stewart, G. W. *On the Early History of the Singular Value Decomposition*. SIAM Review, 35(4):551–566, 1993. [doi:10.1137/1035134](https://doi.org/10.1137/1035134)
- Golub, G. H. & Van Loan, C. F. *Matrix Computations*, 4th ed. Johns Hopkins, 2013.
