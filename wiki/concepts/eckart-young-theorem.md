---
type: concept
created: 2026-07-12
updated: 2026-07-12
sources:
  - raw/papers/stewart-1993-early-history-svd/full-text.md
tags:
  - linear-algebra
  - approximation-theory
  - matrix-decomposition
  - low-rank-approximation
---

# Eckart–Young Theorem

The **Eckart–Young theorem** (also called the **Eckart–Young–Mirsky theorem**) states that the best rank-$k$ approximation to a matrix, in the Frobenius norm or the [[concepts/spectral-norm|spectral norm]], is given by truncating the [[concepts/singular-value-decomposition|singular value decomposition]] after $k$ terms. It is "the fundamental theorem of the singular value decomposition" (Stewart 1993).

## Statement

Let $\mathbf{A} \in \mathbb{R}^{m \times n}$ have SVD $\mathbf{A} = \mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^{\mathrm{T}}$ with singular values $\sigma_1 \geq \sigma_2 \geq \cdots \geq 0$. For any $k < \mathrm{rank}(\mathbf{A})$, the truncated SVD

$$\mathbf{A}_k = \sum_{i=1}^k \sigma_i \mathbf{u}_i \mathbf{v}_i^{\mathrm{T}}$$

is the unique minimizer of $\|\mathbf{A} - \mathbf{B}\|$ over all matrices $\mathbf{B}$ of rank at most $k$. The minimum errors are:

- **Frobenius norm**: $\|\mathbf{A} - \mathbf{A}_k\|_F^2 = \sum_{i=k+1}^r \sigma_i^2$
- **Spectral norm**: $\|\mathbf{A} - \mathbf{A}_k\|_2 = \sigma_{k+1}$

Mirsky (1960) generalized the result: the truncated SVD is optimal in **any** unitarily invariant norm.

## History

The theorem was first proved by [[entities/erhard-schmidt|Erhard Schmidt]] in 1907, in the context of integral equations with unsymmetric kernels (*Zur Theorie der linearen und nichtlinearen Integralgleichungen*, Math. Ann., 63:433–476, 1907). Schmidt's proof shows that for any orthonormal set $\{\mathbf{x}_1, \ldots, \mathbf{x}_k\}$,

$$\sum_{i=1}^k \|\mathbf{A}\mathbf{x}_i\|^2 \leq \sum_{i=1}^k \sigma_i^2,$$

via a clever partition of $\mathbf{V} = (\mathbf{V}_1 \; \mathbf{V}_2)$ and bounding each term using the structure of $\boldsymbol{\Sigma}$.

[[entities/hermann-weyl|Hermann Weyl]] (1912) gave an elegant alternative proof as a corollary of his perturbation theory: his core lemma $\sigma_1(\mathbf{A} - \mathbf{B}_k) \geq \sigma_{k+1}(\mathbf{A})$ immediately yields the spectral-norm bound, and summing gives the Frobenius bound.

Carl Eckart and Gale Young rediscovered the theorem for finite-dimensional matrices in 1936 and 1939, giving the theorem its common name. Leonid Mirsky extended it to all unitarily invariant norms in 1960.

## Significance

The theorem transforms the SVD from a mere factorization into the definitive tool for:

- **Low-rank approximation**: Optimal compression of matrices (images, data, neural network weights).
- **Principal component analysis**: The connection between SVD and PCA is a direct consequence.
- **Denoising**: Truncating small singular values suppresses noise under the assumption that signal energy is concentrated in large singular values.
- **Numerical rank determination**: The spectral-norm gap $\sigma_{k+1}$ quantifies how close $\mathbf{A}$ is to a rank-$k$ matrix.

## References

- Schmidt, E. *Zur Theorie der linearen und nichtlinearen Integralgleichungen*. Math. Ann., 63:433–476, 1907.
- Eckart, C. & Young, G. The approximation of one matrix by another of lower rank. *Psychometrika*, 1:211–218, 1936.
- Mirsky, L. Symmetric gauge functions and unitarily invariant norms. *Quart. J. Math. Oxford*, 11:50–59, 1960.
- Stewart, G. W. *On the Early History of the Singular Value Decomposition*. SIAM Review, 35(4):551–566, 1993.
