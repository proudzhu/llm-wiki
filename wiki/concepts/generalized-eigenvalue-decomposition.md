---
type: concept
created: 2026-04-29
updated: 2026-09-19
sources:
  - raw/papers/scheibler-2020-fast-independent-vector-extraction/full-text.md
  - raw/papers/xiang-2024-multichannel-cdr-estimation/full-text.md
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

## Application in FIVE

[[concepts/fast-independent-vector-extraction|FIVE]] applies GEVD iteratively for blind source extraction: each iteration computes the maximum-SINR beamformer as the generalized eigenvector of the pair (sample covariance $\boldsymbol{C}_f$, reweighted background covariance $\boldsymbol{V}_f$). After one-time pre-whitening $\boldsymbol{C}_f = \boldsymbol{Q}_f^{\mathsf{H}}\boldsymbol{Q}_f$, this reduces to a standard eigenvalue decomposition of the whitened covariance $\widetilde{\boldsymbol{V}}_f = \boldsymbol{Q}_f^{-\mathsf{H}}\boldsymbol{V}_f\boldsymbol{Q}_f^{-1}$, taking the *smallest* eigenvector — the closed-form global minimum of the auxiliary function.

## Application in Multichannel CDR Estimation

Xiang et al. 2024 estimate the array manifold vector for [[concepts/multichannel-cdr-estimation|multichannel CDR estimation]] by jointly diagonalizing the observation and diffuse-noise pseudo-coherence matrices: $\boldsymbol{\Gamma}_{\mathrm{dn}} = \mathbf{U}\mathbf{U}^{\mathrm{H}}$ and $\boldsymbol{\Gamma}_{\mathbf{y}} = \mathbf{U}\boldsymbol{\Lambda}\mathbf{U}^{\mathrm{H}}$, where the columns of $\mathbf{U}$ are the eigenvectors of $\boldsymbol{\Gamma}_{\mathrm{dn}}^{-1}\boldsymbol{\Gamma}_{\mathbf{y}}$ and $\lambda_1 \geq \cdots \geq \lambda_M$ its eigenvalues. The principal eigenvector, scaled as $\widehat{\mathbf{d}} = \frac{\sqrt{M}}{\|\mathbf{u}_1\|_2}\mathbf{u}_1$, serves as the manifold-vector estimate, yielding a DOA-free closed-form coherent-to-diffuse power ratio.

## Related Concepts

- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/variable-span-linear-filter|Variable Span Linear Filter]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/fast-independent-vector-extraction|Fast Independent Vector Extraction]]
- [[concepts/condition-number|Condition Number]]
- [[concepts/diagonal-loading|Diagonal Loading]]

## Related Sources

- [[sources/oviste-2026-neural-vslf-speech-enhancement|Oviste 2026: Neural VSLF for Speech Enhancement]]
- [[sources/mittal-2026-adaptive-diagonal-loading-beamforming|Mittal et al. 2026: Adaptive Diagonal Loading for Norm Constrained Beamforming]]
- [[sources/scheibler-2020-fast-independent-vector-extraction|Scheibler & Ono 2020: Fast Independent Vector Extraction]]
- [[sources/xiang-2024-multichannel-cdr-estimation|Xiang, Lei, Pan, Chen & Benesty 2024: On Multichannel Coherent-to-Diffuse Power Ratio Estimation]] — joint diagonalization for array manifold estimation in multichannel CDR estimation
