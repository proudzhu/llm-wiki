---
type: source
created: 2026-05-02
updated: 2026-05-02
sources:
  - raw/articles/eli-2026-lagrange-interpolation/full-text.md
  - https://eli.thegreenplace.net/2026/notes-on-lagrange-interpolating-polynomials/
tags:
  - numerical-methods
  - interpolation
  - linear-algebra
  - polynomial
---

# Bendersky 2026: Notes on Lagrange Interpolating Polynomials

**Author**: [[../entities/eli-bendersky|Eli Bendersky]]
**Published**: 2026
**Type**: Blog post
**URL**: [eli.thegreenplace.net](https://eli.thegreenplace.net/2026/notes-on-lagrange-interpolating-polynomials/)

---

## Summary

A tutorial on polynomial interpolation via Lagrange basis functions. Derives the Lagrange interpolating polynomial from first principles, proves existence and uniqueness of the interpolating polynomial, shows that Lagrange basis functions form a vector space basis for $P_n(\mathbb{R})$, and derives the Vandermonde determinant formula.

---

## Polynomial Interpolation Problem

Given $n+1$ distinct points $(x_0, y_0), \ldots, (x_n, y_n)$, find a polynomial $P(x)$ of degree at most $n$ such that $P(x_i) = y_i$ for all $i$.

## Existence via Linear Algebra

Assigning all points into the generic polynomial $P(x) = a_0 + a_1 x + \cdots + a_n x^n$ yields the linear system:

$$\begin{bmatrix} 1 & x_0 & \cdots & x_0^n \\ 1 & x_1 & \cdots & x_1^n \\ \vdots & & & \vdots \\ 1 & x_n & \cdots & x_n^n \end{bmatrix} \begin{bmatrix} a_0 \\ a_1 \\ \vdots \\ a_n \end{bmatrix} = \begin{bmatrix} y_0 \\ y_1 \\ \vdots \\ y_n \end{bmatrix}$$

The coefficient matrix is the **Vandermonde matrix**, which is invertible when $x_i$ are distinct. However, it is often numerically ill-conditioned, motivating alternative methods.

## Lagrange Basis Construction

Define the **Lagrange basis functions**:

$$\ell_i(x) = \prod_{\substack{j=0 \\ j \neq i}}^{n} \frac{x - x_j}{x_i - x_j}$$

Each $\ell_i(x) = 1$ at $x_i$ and $0$ at all other $x_j$. The interpolating polynomial is then:

$$P(x) = \sum_{i=0}^{n} y_i \, \ell_i(x)$$

![Normalized Lagrange basis functions](raw/articles/eli-2026-lagrange-interpolation/figures/lagrange-basis-normalized.png)
*Figure: Normalized Lagrange basis functions $\ell_0, \ell_1, \ell_2$ for points $\{(1,1), (2,4), (3,9)\}$. Each is 1 at its node and 0 at all others.*

## Polynomial Interpolation Theorem

**For any $n+1$ data points with distinct $x_i$, there exists a unique polynomial of degree at most $n$ that interpolates these points.**

- **Existence**: Lagrange construction explicitly produces such a polynomial
- **Degree**: Each $\ell_i$ has degree $n$, so $P$ has degree at most $n$
- **Uniqueness**: If $Q$ is another such polynomial, then $P - Q$ has $n+1$ roots but degree $\leq n$, so $P - Q = 0$

## Lagrange Basis as Vector Space Basis

The set $\{\ell_0, \ell_1, \ldots, \ell_n\}$ is a basis for $P_n(\mathbb{R})$:

- **Linear independence**: $\sum c_i \ell_i = 0$ evaluated at $x_j$ gives $c_j = 0$
- **Span**: Any $p \in P_n$ can be expressed as $\sum p(x_i) \ell_i$

## Interpolation Matrix in Lagrange Basis

Using the Lagrange basis, the interpolation system becomes the identity matrix:

$$I \cdot \mathbf{y} = \mathbf{y}$$

This trivially shows that $a_i = y_i$, contrasting with the ill-conditioned Vandermonde matrix.

## Vandermonde Determinant

$$\det(V) = \prod_{0 \leq i < j \leq n} (x_j - x_i)$$

Proof by induction: subtract $x_0$ times the previous column from each column, factor out $(x_i - x_0)$ from each row, and reduce to a smaller Vandermonde matrix.

## Key Contributions

1. **Derives Lagrange basis from first principles**: starts from the product function and normalizes
2. **Proves uniqueness via contradiction**: $n+1$ roots in a degree-$n$ polynomial
3. **Shows Lagrange basis is a true vector space basis**: linear independence + span for $P_n(\mathbb{R})$
4. **Derives Vandermonde determinant formula**: by induction using column operations

---

## Related Concepts

- [[../concepts/lagrange-interpolation|Lagrange Interpolation]]
- [[../concepts/vandermonde-matrix|Vandermonde Matrix]]
- [[../concepts/numerical-stability|Numerical Stability]]
- [[../concepts/symbolic-computation|Symbolic Computation]]
