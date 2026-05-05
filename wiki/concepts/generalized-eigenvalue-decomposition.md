---
type: concept
created: 2026-04-29
updated: 2026-04-29
tags:
  - linear-algebra
  - eigenvalue-problem
  - speech-enhancement
---

# Generalized Eigenvalue Decomposition

**Generalized Eigenvalue Decomposition (GEVD)** solves the generalized eigenvalue problem for two matrices, commonly used in multi-channel speech enhancement for joint diagonalization.

## Formulation

Given two matrices $A$ and $B$, GEVD finds $B$ and $\Lambda$ such that:

$$B^H A B = \Lambda, \quad B^H B B = I$$

In speech enhancement, $A = \Phi_x$ (speech SCM) and $B = \Phi_n$ (noise SCM).

## Application in VSLF

The VSLF framework uses GEVD to jointly diagonalize speech and noise SCMs:

$$B^H \Phi_x B = \Lambda, \quad B^H \Phi_n B = I_M$$

The generalized eigenvalues $\Lambda$ (ordered decreasingly) determine the span dimension $Q$ and filter weights.

## Related Concepts

- [[../concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[../concepts/variable-span-linear-filter|Variable Span Linear Filter]]
- [[../concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Related Sources

- [[../sources/oviste-2026-neural-vslf-speech-enhancement|Oviste 2026: Neural VSLF for Speech Enhancement]]
