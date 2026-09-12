---
type: concept
created: 2026-04-18
updated: 2026-09-12
sources:
  - raw/papers/zhang-2021-adl-mvdr/full-text.md
tags:
  - numerical-methods
  - linear-algebra
  - deep-learning
  - beamforming
---

# Numerical Stability

**Numerical stability** concerns the behavior of an algorithm under finite-precision arithmetic — whether small perturbations (rounding error, ill-conditioned inputs) are amplified or damped. In signal processing systems that mix closed-form matrix operations with neural networks, numerical instability can silently corrupt training.

## Matrix Inversion in Jointly Trained Beamformers

The MVDR beamformer solution requires inverting the noise covariance matrix $\mathbf{\Phi}_{\text{NN}}$ and extracting the principal eigenvector (PCA) of the speech covariance matrix. When these closed-form operations are embedded in an end-to-end trainable system, they are **sometimes numerically unstable** — the classical remedies are [[concepts/diagonal-loading|diagonal loading]] (adding $\epsilon\mathbf{I}$ before inversion) and eigenvalue thresholding, both requiring heuristic parameter choices.

[[sources/zhang-2021-adl-mvdr|Zhang et al. 2021]]'s [[concepts/adl-mvdr|ADL-MVDR]] takes a different route: the matrix inversion and PCA are replaced by two GRU networks trained end-to-end with the front-end filter estimator. This eliminates the unstable closed-form operations entirely — no diagonal loading needed — while the RNNs recursively accumulate the statistics over frames, exploiting the classical result that RNNs can solve matrix inversion in real time (Wang 1993; Zhang & Ge 2005).

## Related Concepts

- [[concepts/diagonal-loading|Diagonal Loading]]
- [[concepts/condition-number|Condition Number]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/adl-mvdr|ADL-MVDR]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/active-noise-control|Active Noise Control]]

## Related Sources

- [[sources/zhang-2021-adl-mvdr|Zhang et al. 2021: ADL-MVDR]] — GRU replacement of matrix inversion and PCA resolves joint-training instability inside the MVDR solution
