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
  - hadamard-product
  - uncertainty-modeling
  - convex-optimization
---

# Hadamard Product of Ellipsoids

The **Hadamard (element-wise) product of two ellipsoids** is the set of all element-wise products $x \circ y = [x_1 y_1, \ldots, x_n y_n]^T$ where $x$ ranges over one ellipsoid and $y$ over another. It arises in [[concepts/robust-minimum-variance-beamforming|robust beamforming]] when the array output is subject to **multiplicative** uncertainties — for example, when the array manifold $\mathcal{E}_1$ is uncertain and the per-channel electronics gains/phases $\mathcal{E}_2$ are also uncertain, the set of possible received array responses is (to first order) the Hadamard product $\mathcal{E}_1 \circ \mathcal{E}_2$. Lorenz & Boyd (2005) derived novel outer approximations for this product in both the real and complex cases.

## Why It Arises

In a real array, the measured response is the product of the physical array manifold (uncertain due to coupling, AOA error) and the electronics chain (uncertain gains and phases). If each uncertainty is described by an ellipsoid, the combined uncertainty is the *numerical range* of the Hadamard product of the two ellipsoids. Unlike the Minkowski sum, the Hadamard product of two ellipsoids is **not** an ellipsoid, so an outer ellipsoidal approximation is required.

## Key Lemmas

**Lemma 3** (factorization): For any $x, y \in \mathbb{R}^n$,

$$(x \circ y)(x \circ y)^T = (xx^T) \circ (yy^T)$$

**Lemma 4** (containment): If $x \in \mathcal{E}_x = \{Au \mid \|u\| \leq 1\}$ and $y \in \mathcal{E}_y = \{Cv \mid \|v\| \leq 1\}$, then $x \circ y$ is contained in

$$\mathcal{E}_{xy} = \left\{(AA^T \circ CC^T)^{1/2} w \mid \|w\| \leq 1\right\}$$

This follows from Lemma 3 plus the fact that the Hadamard product of two positive-semidefinite matrices is positive semidefinite (Schur product theorem), so the cross terms in the expansion are all PSD and can be dropped to obtain a valid outer bound.

## Real-Case Outer Approximation

For $\mathcal{E}_1 = \{Au + b \mid \|u\| \leq 1\}$ and $\mathcal{E}_2 = \{Cv + d \mid \|v\| \leq 1\}$, expand

$$x \circ y = b \circ d + Au \circ Cv + Au \circ d + b \circ Cv$$

By Lemmas 4–5, the field of values is contained in the **Minkowski sum of three ellipsoids**:

$$\mathcal{S} = \mathcal{E}(b \circ d,\, AA^T \circ CC^T) + \mathcal{E}(0,\, AA^T \circ dd^T) + \mathcal{E}(0,\, bb^T \circ CC^T)$$

Ignoring correlations between the three terms and applying the minimum-trace Minkowski-sum formula yields a single covering ellipsoid $\mathcal{E}(b \circ d, P)$ with

$$P = (1 + p_1^{-1})(1 + p_2^{-1})\, AA^T \circ CC^T + (1 + p_1)(1 + p_2^{-1})\, AA^T \circ dd^T + (1 + p_1)(1 + p_2)\, bb^T \circ CC^T$$

for $p_1, p_2 > 0$ chosen to minimize the trace (preferred) or determinant. The trace metric is numerically more reliable when $b$ or $d$ has very small entries.

## Complex-Case Outer Approximation

Representing complex vectors $\alpha, \beta \in \mathbb{C}^n$ by the direct sum of real/imaginary parts in $\mathbb{R}^{2n}$, the product $\gamma = \alpha \circ \beta$ decomposes as

$$z = F_1 x \circ F_2 y + F_3 x \circ F_4 y$$

where $F_1, \ldots, F_4$ are $2n \times 2n$ reordering matrices (block entries $I_n$ and $0$). Expanding over the ellipsoid parameters yields a sum of **six** ellipsoids, which is then outer-approximated by a single ellipsoid via repeated application of the Minkowski-sum formula.

## Improved Approximation

Two refinements produce a tighter covering ellipsoid:

1. **Givens phase rotation**: A block-diagonal rotation $T$ (with $2\times2$ rotation blocks per complex entry) shifts the phase of each ellipsoid-center component so that its imaginary part vanishes. This zeros one of the six terms in the complex expansion, reducing it to **five** terms. The rotation is invertible and leaves the Hadamard product invariant under $T_x^{-1} T_y^{-1}(\cdot)$.

2. **Ordering selection**: The Hadamard product is commutative, but the outer approximation is *not* symmetric under swapping $\{A, b\} \leftrightarrow \{C, d\}$. Both orderings are evaluated and the one with smaller trace is kept. The selection can be made in $\mathcal{O}(n)$ using the identity

$$\mathbf{Tr}\,\mathcal{E}_0 = \left(\sqrt{\mathbf{Tr}\,\mathcal{E}_1} + \cdots + \sqrt{\mathbf{Tr}\,\mathcal{E}_p}\right)^2$$

without explicitly computing the minimum-trace ellipsoids. The chosen configuration matrix is then transformed back to the original coordinates.

## Role in Robust Beamforming

The Hadamard-product calculus lets a designer combine separate uncertainty ellipsoids for the antenna manifold, the RF electronics, and the baseband chain into a single aggregate array-response ellipsoid. That aggregate ellipsoid is then fed into the [[concepts/robust-minimum-variance-beamforming|RMVB]] constraint, producing a beamformer that is robust to the *combined* multiplicative uncertainty rather than just to AOA error alone.

## Related Concepts

- [[concepts/robust-minimum-variance-beamforming|Robust Minimum Variance Beamforming (RMVB)]]
- [[concepts/ellipsoidal-uncertainty-modeling|Ellipsoidal Uncertainty Modeling]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/socp-optimization|SOCP Optimization]]

## Related Sources

- [[sources/lorenz-2005-robust-minimum-variance-beamforming|Lorenz & Boyd 2005: Robust Minimum Variance Beamforming]]
