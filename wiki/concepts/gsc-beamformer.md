---
type: concept
created: 2026-05-07
updated: 2026-08-30
sources:
  - raw/papers/taseska-2018-informed-spatial-filters/full-text.md
  - raw/papers/yan-2014-dual-mic-bt-noise-reduction/full-text.md
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

## Informed GSC (Taseska, Varzandeh & Habets 2016)

Taseska et al. develop the [[concepts/informed-gsc|informed GSC]], where the FBF, BM, and NC are adapted *per TF bin* under the control of a narrowband signal detector (the DOA model-based detector). The signal-cancellation problem of standard GSCs is alleviated by updating the NC **only when the desired signal is absent** — i.e., using the undesired-signal PSD matrix $\boldsymbol{\Phi}_{\mathbf{u}}$ rather than the microphone PSD matrix $\boldsymbol{\Phi}_{\mathbf{y}}$ in the NC computation. The BM uses the RTF-based form (Gannot et al.) rather than the anechoic Griffiths-Jim form, with the RTF estimated online via the detector. An RLS-based recursive NC implementation avoids per-bin matrix inversion, matching the closed-form informed MVDR's performance without notable loss — validating the GSC as an efficient practical alternative in highly non-stationary scenarios.

## ATF-GSC for Bluetooth Headsets (Yan, Qiu & Lu 2014)

[[sources/yan-2014-dual-mic-bt-noise-reduction|Yan et al. 2014]] instantiate the RTF-form GSC on a two-microphone Bluetooth headset (3–4 cm baseline, mouth 3–4 cm from the reference mic — near-field, quasi-fixed geometry), with beamforming matrix $A = [1, W_s]$ and blocking matrix $B = [1, -W_s]$ built from the single RTF $W_s$. Two findings generalize: (i) a blocking matrix **pre-modeled in a quiet factory environment** is robust to wearing-angle mismatch (0°/45°/90°) and inter-user variation, because the near-field path is dominated by geometry — unlike noise-environment adaptive RTF estimation (Cohen 2004), which suffers large modeling errors at low SNR; (ii) under mismatch, speech leaks into the noise reference, equivalent to operating at $\beta = 1$ on the [[concepts/speech-distortion-constrained-noise-reduction|SD-constrained optimal filter]] curve — GSC trades some noise reduction for much lower speech distortion than coherence-function post-filters. See [[concepts/atf-gsc|ATF-GSC]].

## Related Concepts

- [[mpdr-beamformer|MPDR Beamformer]]
- [[mvdr-beamformer|MVDR Beamformer]]
- [[diagonal-loading|Diagonal Loading]]
- [[white-noise-gain|White Noise Gain]]
- [[gershgorin-circle-theorem|Gershgorin Circle Theorem]]
- [[beamforming|Beamforming]]
- [[concepts/informed-spatial-filter|Informed Spatial Filter (ISF)]] — paradigm unifying the informed GSC (Taseska & Habets 2018)
- [[concepts/informed-gsc|Informed GSC]] — bin-wise detector-controlled GSC with RLS noise canceller

## Related Sources

- [[sources/taseska-2018-informed-spatial-filters|Taseska 2018: Informed Spatial Filters for Speech Enhancement]] — informed GSC with bin-wise detector-controlled FBF/BM/NC and RLS noise canceller (Ch 5)
- [[sources/mittal-2026-adaptive-diagonal-loading-beamforming|Mittal et al. 2026: Adaptive Diagonal Loading for Norm Constrained Beamforming]]
- [[sources/zaidel-2026-linearly-constrained-deep-beamformer|Zaidel et al. 2026: Linearly Constrained Deep Beamformer]]
