---
type: source
created: 2026-09-18
updated: 2026-09-18
sources:
  - raw/articles/wikipedia-kronecker-product.md
  - https://en.wikipedia.org/wiki/Kronecker_product
tags:
  - linear-algebra
  - matrix-operations
  - kronecker-product
  - tensor-product
  - mathematics
---

# Wikipedia: Kronecker Product

**Type**: Encyclopedia article (Wikipedia)
**Retrieved**: 2026-09-18
**URL**: [en.wikipedia.org/wiki/Kronecker_product](https://en.wikipedia.org/wiki/Kronecker_product)
**License**: CC BY-SA 4.0

---

## Summary

An encyclopedia reference for the Kronecker product $\mathbf{A} \otimes \mathbf{B}$ — a specialization of the tensor product to matrices that produces a block matrix of size $pm \times qn$ from an $m \times n$ matrix $\mathbf{A}$ and a $p \times q$ matrix $\mathbf{B}$. The article catalogues the algebraic identities (mixed-product, inverse, transpose, determinant, spectrum, rank), the "vec trick" for matrix equations, related products (Tracy–Singh, Khatri–Rao, face-splitting), and applications including the nearest-Kronecker-product approximation.

---

## Definition

For $\mathbf{A} = [a_{ij}] \in \mathbb{C}^{m \times n}$ and $\mathbf{B} \in \mathbb{C}^{p \times q}$, the Kronecker product is the $pm \times qn$ block matrix

$$\mathbf{A}\otimes\mathbf{B} = \begin{bmatrix}
  a_{11} \mathbf{B} & \cdots & a_{1n}\mathbf{B} \\
  \vdots & \ddots & \vdots \\
  a_{m1} \mathbf{B} & \cdots & a_{mn} \mathbf{B}
\end{bmatrix},$$

with elementwise indexing (0-based) $(A \otimes B)_{pr+v,\,qs+w} = a_{rs} b_{vw}$.

- It is a **specialization of the tensor product** from vectors to matrices, giving the matrix of the tensor-product linear map in a standard basis.
- Named after Leopold Kronecker (1823–1891), though the operation was described earlier by Johann Georg Zehfuss (1858); hence the alternative names *Zehfuss product* / *Zehfuss matrix*.
- The operation is **bilinear and associative**, but **not commutative** — $\mathbf{A} \otimes \mathbf{B}$ and $\mathbf{B} \otimes \mathbf{A}$ are permutation-equivalent (related by the commutation/perfect-shuffle matrix).

## Key Algebraic Properties

| Property | Identity |
|---|---|
| Mixed-product | $(\mathbf{A} \otimes \mathbf{B})(\mathbf{C} \otimes \mathbf{D}) = (\mathbf{AC}) \otimes (\mathbf{BD})$ |
| Inverse | $(\mathbf{A} \otimes \mathbf{B})^{-1} = \mathbf{A}^{-1} \otimes \mathbf{B}^{-1}$ (also for Moore–Penrose pseudoinverse) |
| Transpose | $(\mathbf{A}\otimes \mathbf{B})^\textsf{T} = \mathbf{A}^\textsf{T} \otimes \mathbf{B}^\textsf{T}$ (likewise conjugate transpose) |
| Hadamard | $(\mathbf{A} \otimes \mathbf{B}) \circ (\mathbf{C} \otimes \mathbf{D}) = (\mathbf{A} \circ \mathbf{C}) \otimes (\mathbf{B} \circ \mathbf{D})$ |
| Determinant | $\lvert \mathbf{A} \otimes \mathbf{B} \rvert = \lvert \mathbf{A} \rvert^m \lvert \mathbf{B} \rvert^n$ |
| Spectrum | Eigenvalues are $\lambda_i \mu_j$ (all pairwise products); hence $\operatorname{tr}(\mathbf{A}\otimes\mathbf{B}) = \operatorname{tr}\mathbf{A}\,\operatorname{tr}\mathbf{B}$ |
| Singular values | $\sigma_{\mathbf{A},i}\sigma_{\mathbf{B},j}$; hence $\operatorname{rank}(\mathbf{A}\otimes\mathbf{B}) = \operatorname{rank}\mathbf{A}\,\operatorname{rank}\mathbf{B}$ |
| Kronecker sum | $\mathbf{A}\,\overline{\oplus}\,\mathbf{B} = \mathbf{A} \otimes \mathbf{I}_m + \mathbf{I}_n \otimes \mathbf{B}$, with $\exp(\mathbf{N}\,\overline{\oplus}\,\mathbf{M}) = \exp(\mathbf{N}) \otimes \exp(\mathbf{M})$ |
| Outer product | $y \otimes x = \operatorname{vec}(xy^T)$ |

The mixed-product property implies that the category of matrices over a field is a **monoidal category**, with the Kronecker product as the monoidal (tensor) product.

## Matrix Equations and the "vec trick"

The Kronecker product linearizes the Sylvester-type matrix equation $\mathbf{AXB} = \mathbf{C}$:

$$\left(\mathbf{B}^\textsf{T} \otimes \mathbf{A}\right) \operatorname{vec}(\mathbf{X}) = \operatorname{vec}(\mathbf{C}),$$

which has a unique solution iff $\mathbf{A}$ and $\mathbf{B}$ are both invertible.

### Applications

- **Lyapunov equation** and matrix-normal distribution as special cases of multivariate normal.
- **2-D image processing** in matrix-vector form.
- **Fast structured multiplication**: factoring a matrix as a Kronecker product (applied recursively) underlies the radix-2 FFT and the Fast Walsh–Hadamard transform.
- **Nearest Kronecker product**: splitting a known matrix into the Kronecker product of two smaller matrices can be solved exactly via the SVD (Van Loan & Pitsianis 1992); the multi-factor version is harder and is treated as a tensor-decomposition problem.
- **Hand–eye calibration** in robotics, combined with least squares.

## Related Matrix Operations

- **Tracy–Singh product** — the pairwise Kronecker product for each pair of partitions of two partitioned matrices.
- **Khatri–Rao product** — block Kronecker and column-wise variants.
- **Face-splitting product** — with mixed-product properties linking it to the Kronecker and Hadamard products, used in radar and tensor-sketch/convolution results.

## Relevance to This Wiki

The Kronecker product is the algebraic foundation of [[concepts/kronecker-product-beamforming|Kronecker product beamforming]]: representing a length-$M$ filter as a sum of Kronecker products of short subfilters reduces the parameter count from $M = \prod_n L_n$ to $\sum_n L_n$ and shrinks the matrix inversions in the design from $M \times M$ to $L_n \times L_n$. The two-factor case ($\mathbf{h} = \mathbf{h}_1 \otimes \mathbf{h}_2$) underlies the differential Kronecker product beamformer (Cohen, Benesty & Chen 2019), and the N-way, rank-$P$ generalization underlies the low-rank robust superdirective beamformer (Zhu et al. 2025). The factors of the **nearest-Kronecker-product problem** (solved by SVD) recur in adaptive-filtering and multichannel active-noise-control parameter reduction.

---

## Related Concepts

- [[concepts/kronecker-product|Kronecker Product]] — the general mathematical concept
- [[concepts/kronecker-product-beamforming|Kronecker Product Beamforming]]
- [[concepts/singular-value-decomposition|Singular Value Decomposition]] — solves the nearest-Kronecker-product problem
- [[concepts/subband-adaptive-filter|Subband Adaptive Filter]] — applications of nearest Kronecker product decomposition

## Related Sources

- [[sources/cohen-2019-differential-kronecker-beamforming|Cohen, Benesty & Chen 2019: Differential Kronecker Product Beamforming]]
- [[sources/wang-2021-kronecker-adaptive-beamforming|Wang et al. 2021: Kronecker Product Adaptive Beamforming for Microphone Arrays]]
- [[sources/zhu-2025-kronecker-superdirective-beamforming|Zhu et al. 2025: Low-Rank Robust Superdirective Beamforming Using Multidimensional Kronecker Products]]