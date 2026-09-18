---
type: concept
created: 2026-09-18
updated: 2026-09-18
sources:
  - raw/articles/wikipedia-kronecker-product.md
tags:
  - linear-algebra
  - matrix-operations
  - kronecker-product
  - tensor-product
  - structured-matrices
---

# Kronecker Product

**Category**: Linear Algebra / Matrix Operations

## Definition

The **Kronecker product** $\mathbf{A} \otimes \mathbf{B}$ is a matrix operation on an $m \times n$ matrix $\mathbf{A}$ and a $p \times q$ matrix $\mathbf{B}$ producing the $pm \times qn$ block matrix

$$\mathbf{A}\otimes\mathbf{B} = \begin{bmatrix}
  a_{11} \mathbf{B} & \cdots & a_{1n}\mathbf{B} \\
  \vdots & \ddots & \vdots \\
  a_{m1} \mathbf{B} & \cdots & a_{mn} \mathbf{B}
\end{bmatrix}, \qquad (A\otimes B)_{pr+v,\,qs+w} = a_{rs} b_{vw}.$$

It is the matrix representation of the abstract **tensor product** of linear maps, and it is a genuine operation on matrices distinct from ordinary matrix multiplication. It is named after Leopold Kronecker, though the operation was described earlier by Johann Georg Zehfuss (1858) — hence the alternative names *Zehfuss product* / *Zehfuss matrix*.

## Core Algebraic Identities

- **Bilinear, associative, not commutative.** $\mathbf{A} \otimes \mathbf{B} \neq \mathbf{B} \otimes \mathbf{A}$ in general, but the two are permutation-equivalent via the commutation (perfect-shuffle) matrix.
- **Mixed-product.** $(\mathbf{A} \otimes \mathbf{B})(\mathbf{C} \otimes \mathbf{D}) = (\mathbf{AC}) \otimes (\mathbf{BD})$ — this is what makes the Kronecker product the monoidal product of the category of matrices.
- **Inverse / pseudoinverse.** $(\mathbf{A} \otimes \mathbf{B})^{-1} = \mathbf{A}^{-1} \otimes \mathbf{B}^{-1}$; $\mathbf{A} \otimes \mathbf{B}$ is invertible iff both factors are.
- **Transpose.** $(\mathbf{A}\otimes \mathbf{B})^\textsf{T} = \mathbf{A}^\textsf{T} \otimes \mathbf{B}^\textsf{T}$ (analogously for conjugate transpose).
- **Hadamard / element-wise.** $(\mathbf{A} \otimes \mathbf{B}) \circ (\mathbf{C} \otimes \mathbf{D}) = (\mathbf{A} \circ \mathbf{C}) \otimes (\mathbf{B} \circ \mathbf{D})$.
- **Determinant / trace.** $\lvert \mathbf{A} \otimes \mathbf{B} \rvert = \lvert \mathbf{A} \rvert^m \lvert \mathbf{B} \rvert^n$ and $\operatorname{tr}(\mathbf{A}\otimes\mathbf{B}) = \operatorname{tr}\mathbf{A}\,\operatorname{tr}\mathbf{B}$.
- **Spectrum and rank.** Eigenvalues are all products $\lambda_i \mu_j$; singular values are all products $\sigma_{\mathbf{A},i}\sigma_{\mathbf{B},j}$, so $\operatorname{rank}(\mathbf{A}\otimes\mathbf{B}) = \operatorname{rank}\mathbf{A}\,\operatorname{rank}\mathbf{B}$.
- **Kronecker sum.** $\mathbf{A}\,\overline{\oplus}\,\mathbf{B} = \mathbf{A} \otimes \mathbf{I}_m + \mathbf{I}_n \otimes \mathbf{B}$, with $\exp(\mathbf{N}\,\overline{\oplus}\,\mathbf{M}) = \exp(\mathbf{N}) \otimes \exp(\mathbf{M})$ (used for ensembles of non-interacting systems).

## Linearization of Matrix Equations

The Kronecker product converts matrix equations into linear systems in vectorized unknowns — the **"vec trick"**:

$$\left(\mathbf{B}^\textsf{T} \otimes \mathbf{A}\right) \operatorname{vec}(\mathbf{X}) = \operatorname{vec}(\mathbf{AXB}) = \operatorname{vec}(\mathbf{C}).$$

Therefore $\mathbf{AXB} = \mathbf{C}$ has a unique solution iff $\mathbf{A}$ and $\mathbf{B}$ are invertible. This underlies the Lyapunov equation, matrix-normal distributions, and 2-D image-processing operators in matrix-vector form.

## Nearest Kronecker Product

A matrix given only numerically rarely factorizes exactly. Finding $\mathbf{A}, \mathbf{B}$ minimizing $\lVert \mathbf{M} - \mathbf{A} \otimes \mathbf{B} \rVert$ is the **nearest Kronecker product** problem, solvable exactly via the [[concepts/singular-value-decomposition|SVD]] (Van Loan & Pitsianis 1992); see the dedicated page [[concepts/nearest-kronecker-product|Nearest Kronecker Product]] for the solution, its rank-$P$ generalization, and its signal-processing applications. Optimally splitting into **more than two** factors is harder and is treated as a tensor-decomposition problem — the setting that reappears as the rank-$P$, N-way decompositions in Kronecker product beamforming.

## Role in This Wiki

Kronecker products are the algebraic backbone of **structured, low-rank filter representations**:

- [[concepts/kronecker-product-beamforming|Kronecker Product Beamforming]] — a length-$M$ filter is written as a sum of $P$ Kronecker products of $N$ short filters ($M = \prod_n L_n$), cutting the parameter count from $M$ to $\sum_n L_n$ and the matrix-inversion dimension from $M$ to $L_n$, while the low-rank structure often *improves* robustness.
- In [[concepts/differential-microphone-array|differential microphone arrays]], the two-factor case $\mathbf{h} = \mathbf{h}_1 \otimes \mathbf{h}_2$ corresponds to two virtual ULAs ($M = M_1 M_2$), where the beampattern and [[concepts/white-noise-gain|WNG]] factorize but the directivity factor and front-to-back ratio do not.
- The SVD-based nearest-Kronecker-product decomposition also appears in adaptive filtering — most prominently the [[concepts/rls-nkp|RLS-NKP]] family of low-rank recursive least-squares algorithms for echo-path identification — and in parameter reduction for multichannel active noise control controllers.

## Related Operations

The **Tracy–Singh product** (pairwise Kronecker products over blocks of partitioned matrices), the **Khatri–Rao product** (block and column-wise variants), and the **face-splitting product** are variants that share mixed-product identities with the Kronecker and Hadamard products.

## Related Concepts

- [[concepts/kronecker-product-beamforming|Kronecker Product Beamforming]]
- [[concepts/singular-value-decomposition|Singular Value Decomposition]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/subband-adaptive-filter|Subband Adaptive Filter]]
- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/white-noise-gain|White Noise Gain]]

## Related Sources

- [[sources/wikipedia-kronecker-product|Wikipedia: Kronecker Product]] — general mathematical reference
- [[sources/cohen-2019-differential-kronecker-beamforming|Cohen, Benesty & Chen 2019: Differential Kronecker Product Beamforming]]
- [[sources/wang-2021-kronecker-adaptive-beamforming|Wang et al. 2021: Kronecker Product Adaptive Beamforming for Microphone Arrays]]
- [[sources/zhu-2025-kronecker-superdirective-beamforming|Zhu et al. 2025: Low-Rank Robust Superdirective Beamforming Using Multidimensional Kronecker Products]]
- [[sources/elisei-iliescu-2019-low-rank-rls|Elisei-Iliescu et al. 2019: Recursive Least-Squares Algorithms for the Identification of Low-Rank Systems]] — rank-$P$ NKP decomposition as the foundation of low-rank adaptive identification