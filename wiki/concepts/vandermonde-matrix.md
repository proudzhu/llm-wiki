---
type: concept
created: 2026-05-02
updated: 2026-05-02
sources:
  - raw/articles/eli-2026-lagrange-interpolation/full-text.md
tags:
  - linear-algebra
  - numerical-methods
  - interpolation
  - determinant
---

# Vandermonde Matrix

A **Vandermonde matrix** is a matrix with the geometric progression structure:

$$V = \begin{bmatrix} 1 & x_0 & x_0^2 & \cdots & x_0^n \\ 1 & x_1 & x_1^2 & \cdots & x_1^n \\ \vdots & & & & \vdots \\ 1 & x_n & x_n^2 & \cdots & x_n^n \end{bmatrix}$$

## Key Properties

### Determinant

The determinant of an $n \times n$ Vandermonde matrix is:

$$\det(V) = \prod_{0 \leq i < j \leq n} (x_j - x_i)$$

When all $x_i$ are distinct, $\det(V) \neq 0$, so $V$ is invertible.

**Proof sketch**: Subtract $x_0$ times the previous column from each column (starting from the right) to zero out the first row after the first element. Factor out $(x_i - x_0)$ from each row, reducing to a smaller Vandermonde matrix. Proceed by induction.

### Invertibility and Interpolation

The Vandermonde matrix arises naturally in polynomial interpolation using the monomial basis. The system $V\mathbf{a} = \mathbf{y}$ has a unique solution when $x_i$ are distinct, confirming the existence and uniqueness of the interpolating polynomial.

### Numerical Conditioning

Despite being theoretically invertible, the Vandermonde matrix is often **numerically ill-conditioned**, especially for large $n$ or closely spaced nodes. This motivates the use of alternative bases (Lagrange, Newton) for practical computation.

## Related Concepts

- [[../concepts/lagrange-interpolation|Lagrange Interpolation]] — alternative basis yielding identity matrix instead of Vandermonde
- [[../concepts/numerical-stability|Numerical Stability]] — Vandermonde ill-conditioning as a practical concern

## Related Sources

- [[../sources/eli-2026-lagrange-interpolation|Bendersky 2026: Notes on Lagrange Interpolating Polynomials]]
