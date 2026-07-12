---
type: entity
created: 2026-07-12
updated: 2026-07-12
sources:
  - raw/papers/stewart-1993-early-history-svd/full-text.md
tags:
  - mathematician
  - integral-equations
  - functional-analysis
  - approximation-theory
  - history-of-mathematics
---

# Erhard Schmidt

**Erhard Schmidt** (1876–1959) was a German mathematician, a student of **David Hilbert** at Göttingen. His 1907 work on integral equations **elevated the [[concepts/singular-value-decomposition|singular value decomposition]] from a mathematical curiosity to a fundamental computational tool** by proving the best rank-$k$ approximation theorem.

## Contributions

- **SVD for integral equations (1907)**: In *Zur Theorie der linearen und nichtlinearen Integralgleichungen* (Math. Ann., 1907), Schmidt generalized the SVD to infinite-dimensional function spaces. For an unsymmetric kernel $A(s,t)$, he defined adjoint eigenfunction pairs $(u_i(s), v_i(t))$ satisfying the integral equations, constructed them via the symmetric kernels $\bar{A}$ and $\underline{A}$, and established the bilinear-form expansion that "corresponds to the canonical decomposition of a bilinear form."
- **The approximation theorem** ([[concepts/eckart-young-theorem|Eckart–Young theorem]]): Schmidt's crowning contribution is the proof that the best rank-$k$ approximation to $\mathbf{A}$ in the Frobenius norm is $\mathbf{A}_k = \sum_{i=1}^k \sigma_i \mathbf{u}_i \mathbf{v}_i^{\mathrm{T}}$, with $\|\mathbf{A} - \mathbf{A}_k\|^2 = \sum_{i=k+1}^n \sigma_i^2$. Stewart calls this "the fundamental theorem of the singular value decomposition."
  - The proof uses a clever partition of $\mathbf{V} = (\mathbf{V}_1 \; \mathbf{V}_2)$ and shows $\sum_{i=1}^k \|\mathbf{A}\mathbf{x}_i\|^2 \leq \sum_{i=1}^k \sigma_i^2$ for any orthonormal set $\{\mathbf{x}_1, \ldots, \mathbf{x}_k\}$.
- **Gram–Schmidt orthogonalization**: Schmidt's name is attached to the Gram–Schmidt process for orthogonalizing a sequence of vectors.
- **Functional analysis**: Foundational contributions to the theory of Hilbert spaces and integral equations.

## Historical Note

As Stewart notes in [[sources/stewart-1993-early-history-svd|the survey]], the approximation theorem is often misattributed to Eckart and Young (1936, 1939), who rediscovered it nearly three decades later. Unlike his linear-algebra predecessors (Beltrami, Jordan, Sylvester), Schmidt approached the SVD from the theory of integral equations — a parallel tradition.

## References

- Schmidt, E. *Zur Theorie der linearen und nichtlinearen Integralgleichungen*. Math. Ann., 63:433–476, 1907.
- Stewart, G. W. *On the Early History of the Singular Value Decomposition*. SIAM Review, 35(4):551–566, 1993.
