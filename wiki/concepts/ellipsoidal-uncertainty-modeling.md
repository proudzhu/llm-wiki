---
type: concept
created: 2026-06-21
updated: 2026-06-21
sources:
  - raw/papers/lorenz-2005-robust-minimum-variance-beamforming/full-text.md
tags:
  - beamforming
  - robust-beamforming
  - ellipsoidal-calculus
  - uncertainty-modeling
  - convex-optimization
  - array-signal-processing
---

# Ellipsoidal Uncertainty Modeling

**Ellipsoidal Uncertainty Modeling** is the practice of representing a set of possible values of an uncertain vector (such as an array manifold response) as an ellipsoid, and then propagating that ellipsoid through signal-path operations to obtain an aggregate uncertainty description suitable for robust optimization. It is the geometric foundation of the [[concepts/robust-minimum-variance-beamforming|Robust Minimum Variance Beamformer]].

## Ellipsoid Parameterization

An ellipsoid in $\mathbb{R}^n$ is parameterized by its center $c \in \mathbb{R}^n$ and a symmetric non-negative definite **configuration matrix** $P \in \mathbb{R}^{n \times n}$:

$$\mathcal{E}(c, P) = \left\{P^{1/2} u + c \mid \|u\| \leq 1\right\} = \left\{x \mid (x-c)^T P^{-1} (x-c) \leq 1\right\}$$

The first form is preferred when $P$ is degenerate or poorly conditioned; the second allows quick point-in-ellipsoid tests. For complex array responses $a \in \mathbb{C}^n$, the direct sum of real and imaginary parts is taken in $\mathbb{R}^{2n}$ — this avoids the unwanted real/imaginary symmetry that a complex ellipsoid in $\mathbb{C}^n$ would impose, yielding a tighter fit.

## Constructing the Ellipsoid from Data

Given $m$ samples $s_1, \ldots, s_m$ of the array response (e.g., measured at slightly different AOAs or across calibration runs), two main approaches are used:

### 1. Sample Mean / Covariance Fit

$$c = \frac{1}{m}\sum_{i=1}^{m} s_i, \quad P = \frac{1}{\alpha m}\sum_{i=1}^{m} (s_i - c)(s_i - c)^T$$

with $\alpha = \sup_i (s_i - c)^T P^{-1} (s_i - c)$ chosen so that *all* samples lie inside the ellipsoid. Simple and fast, but can be loose.

### 2. Minimum-Volume Ellipsoid (MVE / Löwner–John)

The minimum-volume ellipsoid covering the samples is found by solving the convex SDP

$$\min_{F, g} \; \log\det F^{-1} \quad \text{s.t.} \quad \|F s_i - g\| \leq 1, \; i = 1, \ldots, m$$

with $A = F^{-1}$, $c = F^{-1} g$. The MVE is the tightest ellipsoidal cover and is guaranteed to contain all data points (but is *not* robust to outliers). When the samples lie on a low-dimensional affine subspace of dimension $l < 2n$, a rank-preserving affine projection (via the left singular vectors of $[s_2 - s_1, \ldots, s_m - s_1]$) is applied first to avoid numerical ill-conditioning; a minimum of $l + 2$ points are required.

## Propagating Uncertainty: Ellipsoidal Calculus

When the array response is the result of several uncertain components in the signal path (antenna, electronics, gains, phases), each described by its own ellipsoid, the aggregate uncertainty is obtained by **ellipsoidal calculus**:

### Sum of Two Ellipsoids (Minkowski Sum)

If $x \in \mathcal{E}(c_1, P_1)$ and $y \in \mathcal{E}(c_2, P_2)$, then $x + y$ is contained in

$$\mathcal{E}\bigl(c_1 + c_2,\; P(p)\bigr), \quad P(p) = (1 + p^{-1}) P_1 + (1 + p) P_2$$

The **minimum-trace** choice $p^\star = \sqrt{\mathbf{Tr}\,P_1 / \mathbf{Tr}\,P_2}$ can be computed in $\mathcal{O}(n)$ and works with degenerate ellipsoids, making it preferable to the determinant-minimizing choice ($\mathcal{O}(n^3)$).

### Hadamard Product of Two Ellipsoids

For **multiplicative** uncertainties (e.g., unknown per-channel gain/phase), the aggregate array response is the element-wise (Hadamard) product of two ellipsoid-valued vectors. This requires the specialized calculus described in [[concepts/hadamard-product-ellipsoids|Hadamard Product of Ellipsoids]].

## Role in Robust Beamforming

The aggregate ellipsoid $\mathcal{E}$ is plugged directly into the [[concepts/robust-minimum-variance-beamforming|RMVB]] constraint $\mathbf{Re}\,w^* a \geq 1\;\forall a \in \mathcal{E}$, which the Cauchy–Schwarz inequality converts into the second-order cone constraint $\|A^T x\| \leq c^T x - 1$. The quality of the ellipsoidal model directly determines the conservatism of the RMVB: an ellipsoid that is too large sacrifices performance; one that is too small may violate the minimum-gain guarantee.

## Related Concepts

- [[concepts/robust-minimum-variance-beamforming|Robust Minimum Variance Beamforming (RMVB)]]
- [[concepts/hadamard-product-ellipsoids|Hadamard Product of Ellipsoids]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/socp-optimization|SOCP Optimization]]
- [[concepts/diagonal-loading|Diagonal Loading]]

## Related Sources

- [[sources/lorenz-2005-robust-minimum-variance-beamforming|Lorenz & Boyd 2005: Robust Minimum Variance Beamforming]]
