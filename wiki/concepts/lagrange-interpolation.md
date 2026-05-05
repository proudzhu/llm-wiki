---
type: concept
created: 2026-05-02
updated: 2026-05-02
sources:
  - raw/articles/eli-2026-lagrange-interpolation/full-text.md
tags:
  - numerical-methods
  - linear-algebra
  - interpolation
  - polynomial
---

# Lagrange Interpolation

**Lagrange Interpolation** is a method for finding the unique polynomial of degree at most $n$ that passes through $n+1$ distinct data points. It constructs the interpolating polynomial as a linear combination of Lagrange basis functions.

## Overview

Given $n+1$ distinct points $(x_0, y_0), \ldots, (x_n, y_n)$, the Lagrange interpolating polynomial is:

$$P(x) = \sum_{i=0}^{n} y_i \, \ell_i(x)$$

where $\ell_i(x)$ are the **Lagrange basis functions**:

$$\ell_i(x) = \prod_{\substack{j=0 \\ j \neq i}}^{n} \frac{x - x_j}{x_i - x_j}$$

Each $\ell_i(x)$ equals 1 at $x_i$ and 0 at all other nodes $x_j$ ($j \neq i$).

## Key Properties

### Existence and Uniqueness

The **Polynomial Interpolation Theorem** states: for any $n+1$ data points with distinct $x_i$, there exists a unique polynomial of degree at most $n$ that interpolates these points.

- **Existence**: The Lagrange construction explicitly produces such a polynomial
- **Uniqueness**: If two polynomials $P$ and $Q$ of degree $\leq n$ both interpolate the same $n+1$ points, then $P - Q$ has $n+1$ roots but degree $\leq n$, so $P - Q = 0$ (by the Fundamental Theorem of Algebra)

### Lagrange Basis as a Vector Space Basis

The set $\{\ell_0, \ell_1, \ldots, \ell_n\}$ forms a basis for $P_n(\mathbb{R})$ (the vector space of real polynomials of degree $\leq n$):

- **Linear independence**: $\sum c_i \ell_i = 0$ evaluated at $x_j$ gives $c_j = 0$
- **Span**: Any polynomial $p \in P_n$ can be expressed as $\sum p(x_i) \ell_i$

### Interpolation Matrix

Using the Lagrange basis, the interpolation system becomes trivial — the matrix is the identity:

$$\begin{bmatrix} 1 & 0 & \cdots & 0 \\ 0 & 1 & \cdots & 0 \\ \vdots & & \ddots & \vdots \\ 0 & 0 & \cdots & 1 \end{bmatrix} \begin{bmatrix} y_0 \\ y_1 \\ \vdots \\ y_n \end{bmatrix} = \begin{bmatrix} y_0 \\ y_1 \\ \vdots \\ y_n \end{bmatrix}$$

This contrasts with the **Vandermonde matrix** obtained when using the monomial basis $\{1, x, x^2, \ldots, x^n\}$, which is invertible but often numerically ill-conditioned.

## Comparison with Other Methods

| Method | Basis | Matrix | Numerical Properties |
|--------|-------|--------|---------------------|
| Vandermonde | $\{1, x, x^2, \ldots\}$ | Vandermonde matrix | Ill-conditioned |
| Lagrange | $\{\ell_0, \ell_1, \ldots\}$ | Identity matrix | Stable but $O(n^2)$ evaluation |
| Newton | Divided differences | Lower triangular | $O(n)$ evaluation, incremental |

## Related Concepts

- [[../concepts/vandermonde-matrix|Vandermonde Matrix]] — alternative basis for polynomial interpolation
- [[../concepts/numerical-stability|Numerical Stability]] — Vandermonde matrix ill-conditioning motivates Lagrange/Newton methods
- [[../concepts/symbolic-computation|Symbolic Computation]] — CAS manipulation of polynomial expressions

## Related Sources

- [[../sources/eli-2026-lagrange-interpolation|Bendersky 2026: Notes on Lagrange Interpolating Polynomials]]
