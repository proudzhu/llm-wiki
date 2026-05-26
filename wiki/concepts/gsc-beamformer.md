---
type: concept
created: 2026-05-07
updated: 2026-05-07
tags:
  - beamforming
  - adaptive-filtering
  - microphone-arrays
---

# Generalized Sidelobe Canceller (GSC)

**Category**: Adaptive Beamforming Architecture

## Definition

The Generalized Sidelobe Canceller (GSC) is an alternative formulation of the [[concepts/lcmv-beamformer|linearly constrained minimum variance (LCMV) beamformer]] that orthogonalizes the distortionless constraint and the adaptive noise cancellation components:

$$\mathbf{w}_{gsc} = \mathbf{w}_q - \mathbf{B}\mathbf{w}_a$$

where:
- $\mathbf{w}_q = \mathbf{d}/M$: Fixed quiescent weight vector satisfying the target constraint
- $\mathbf{B} \in \mathbb{C}^{M \times (M-1)}$: Blocking matrix such that $\mathbf{B}^H \mathbf{d} = \mathbf{0}$ and $\mathbf{B}^H \mathbf{B} = \mathbf{I}$
- $\mathbf{w}_a \in \mathbb{C}^{(M-1) \times 1}$: Adaptive noise cancellation weight vector

## Adaptive Weight Computation

The noise cancellation weights are computed as:

$$\mathbf{w}_a = \mathbf{R}_n^{-1} \mathbf{r}_{qn}$$

where:
- $\mathbf{R}_n = \mathbf{B}^H \hat{\mathbf{R}}_y \mathbf{B}$: Noise correlation matrix in the blocking subspace
- $\mathbf{r}_{qn} = \mathbf{B}^H \hat{\mathbf{R}}_y \mathbf{w}_q$: Cross-correlation vector

## WNG-Constrained GSC (Mittal et al. 2026)

Mittal et al. (2026) show that their adaptive diagonal loading method is structurally agnostic. In the GSC framework, the loading is applied to the noise correlation matrix:

$$\mathbf{w}_a = (\mathbf{R}_n + \mu[i]\mathbf{I})^{-1} \mathbf{r}_{qn}$$

### Unitary Transformation Equivalence

Define $\mathbf{T} = [\sqrt{M}\mathbf{w}_q, \mathbf{B}]$. Since $\mathbf{T}^H \mathbf{T} = \mathbf{I}$, the transformed matrix $\tilde{\mathbf{R}} = \mathbf{T}^H \hat{\mathbf{R}}_y \mathbf{T}$ shares the exact same eigenvalues as $\hat{\mathbf{R}}_y$. This can be constructed from tracked GSC components:

$$\tilde{\mathbf{R}} = \begin{bmatrix} M p_q & \sqrt{M} \mathbf{r}_{qn}^H \\ \sqrt{M} \mathbf{r}_{qn} & \mathbf{R}_n \end{bmatrix}$$

### Mode Invariance

- **EVD and Trace modes**: Perfectly invariant between MPDR and GSC (identical weights and performance)
- **Gershgorin mode**: Basis-dependent — the blocking matrix $\mathbf{B}$ alters the distribution between diagonal and off-diagonal elements, yielding different loading estimates

## Related Concepts

- [[mpdr-beamformer|MPDR Beamformer]]
- [[mvdr-beamformer|MVDR Beamformer]]
- [[diagonal-loading|Diagonal Loading]]
- [[white-noise-gain|White Noise Gain]]
- [[gershgorin-circle-theorem|Gershgorin Circle Theorem]]
- [[beamforming|Beamforming]]

## Related Sources

- [[sources/mittal-2026-adaptive-diagonal-loading-beamforming|Mittal et al. 2026: Adaptive Diagonal Loading for Norm Constrained Beamforming]]
- [[sources/zaidel-2026-linearly-constrained-deep-beamformer|Zaidel et al. 2026: Linearly Constrained Deep Beamformer]]
