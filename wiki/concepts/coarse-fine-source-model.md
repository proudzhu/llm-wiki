---
type: concept
created: 2026-10-04
updated: 2026-10-04
sources:
  - raw/papers/nakatani-2022-switching-iva/full-text.md
tags:
  - blind-source-separation
  - independent-vector-analysis
  - source-modeling
  - dereverberation
---

# Coarse-Fine Source Model

The **coarse-fine source model** is a hybrid statistical source model used by [[concepts/switching-independent-vector-analysis|swIVA]] and [[concepts/switching-civa|swCIVA]] to reconcile two contradictory requirements in a single maximum-likelihood optimization.

## The contradiction

- **Fine source model** (frequency-dependent, variance $\lambda_{n,t,f}$): essential for optimizing the MCLP filters (WPE dereverberation) and the switching weights, because reverberation and noise influence are frequency-dependent.
- **Coarse source model** (frequency-independent, variance $\lambda_{n,t}$): essential for IVA's core mechanism — modeling each source as a full-band vector with inter-frequency dependency is what solves the frequency permutation problem without post-processing.

## The hybrid

Use each model where it is indispensable:

$$
\lambda_{n,t} = \frac{1}{F}\sum_{f=1}^{F} \lambda_{n,t,f} \quad \text{(coarse, for separation-matrix updates)}
$$

- **Separation matrix $\mathbf{W}$ updates** use the coarse (frequency-independent) model;
- **MCLP filter $\mathbf{G}$, variance $\Lambda$, and switch $\mathbf{B}$ updates** use the fine (frequency-dependent) model.

Empirically, using the fine model for switches and MCLP filters "greatly improved" swIVA/swCIVA performance versus coarse-only configurations; the coarse model must be kept for the separation matrices for permutation-free separation. The idea was first shown effective for CIVA (Nakatani et al. 2021) and extended to the switching weights by the 2022 swIVA/swCIVA paper.

## Related Concepts

- [[concepts/switching-independent-vector-analysis|Switching Independent Vector Analysis]]
- [[concepts/switching-civa|Switching CIVA (swCIVA)]]
- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/weighted-prediction-error|Weighted Prediction Error (WPE)]]

## Related Sources

- [[sources/nakatani-2022-switching-iva|Nakatani et al. 2022: Switching IVA and Its Extension to Blind and Spatially Guided Convolutional Beamforming]]
