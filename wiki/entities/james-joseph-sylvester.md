---
type: entity
created: 2026-07-12
updated: 2026-07-12
sources:
  - raw/papers/stewart-1993-early-history-svd/full-text.md
tags:
  - mathematician
  - linear-algebra
  - matrix-theory
  - history-of-mathematics
---

# James Joseph Sylvester

**James Joseph Sylvester** (1814–1897) was a British mathematician who coined much of the modern vocabulary of matrix theory, including the word "matrix" itself. He **independently discovered the singular value decomposition** in 1889, in ignorance of [[entities/eugenio-beltrami|Beltrami]] and [[entities/camille-jordan|Jordan]].

## Contributions

- **Singular value decomposition (1889)**: In a footnote in the *Messenger of Mathematics*, a *Comptes Rendus* note, and a full paper [58], Sylvester presented two methods:
  - **The rule**: Form $M = \mathbf{x}^{\mathrm{T}}\mathbf{A}\mathbf{A}^{\mathrm{T}}\mathbf{x} = \sum \lambda_i \xi_i^2$; then $B = \mathbf{x}^{\mathrm{T}}\mathbf{A}\mathbf{y} = \sum \sigma_i \xi_i \eta_i$ with $\sigma_i^2 = \lambda_i$. The substitution coefficients come from order-$(n{-}1)$ minors of $\mathbf{M} - \sigma^2\mathbf{I}$, normalized. This only works for simple singular values.
  - **Infinitesimal iteration**: An inductive procedure using "infinitesimal orthogonal substitutions" — infinitesimal rotations that zero out off-diagonal elements while preserving previously introduced zeros. Stewart notes that this anticipates modern continuous-transformation algorithms defined by differential equations, though Sylvester did not give enough detail to write down such equations.
- **Matrix terminology**: Coined "matrix," "minor," "discriminant," "Jacobian" (with Jacobi), and many other terms.
- **Sylvester's law of inertia**: The classification of quadratic forms by signature.
- **Combinatorics and number theory**: Contributions to partition theory and invariant theory.

## Historical Note

Stewart observes in [[sources/stewart-1993-early-history-svd|the survey]] that Sylvester's style is "opaque" and that he "pontificates without proving." He was also unaware of Jacobi's 1846 iterative diagonalization algorithm for symmetric matrices; the generalization of Jacobi's method to the SVD is due to Kogbetliantz (1955).

## References

- Sylvester, J. J. Notes on a footnote. *Messenger of Mathematics*, 19:87–90, 1890 (footnote [57]).
- Sylvester, J. J. Sur la réduction d'une fonction linéaire et bilinéaire. *Comptes Rendus*, 108:651–653, 1889 (note [59]).
- Sylvester, J. J. On the reduction of a bilinear quantic to its canonical form. *Messenger of Mathematics*, 19:1–4, 1889 (paper [58]).
- Stewart, G. W. *On the Early History of the Singular Value Decomposition*. SIAM Review, 35(4):551–566, 1993.
