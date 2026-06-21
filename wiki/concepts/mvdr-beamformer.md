---
type: concept
created: 2026-04-29
updated: 2026-06-21
sources:
  - raw/papers/lorenz-2005-robust-minimum-variance-beamforming/full-text.md
tags:
  - beamforming
  - speech-enhancement
  - array-processing
---

# MVDR Beamformer

The **Minimum Variance Distortionless Response (MVDR)** beamformer minimizes output noise power while maintaining unity gain in the target direction. Also known as **Capon's method** (Capon 1969).

## Formulation

$$h_{\text{MVDR}} = \frac{\Phi_n^{-1} a}{a^H \Phi_n^{-1} a}$$

where $a$ is the steering vector for the target direction and $\Phi_n$ is the noise spatial covariance matrix. When the sample covariance $R_y$ is used in place of $\Phi_n$ (so that the minimized power includes the desired signal), the solution is

$$w_{\text{mv}} = \frac{R_y^{-1} a(\theta)}{a(\theta)^* R_y^{-1} a(\theta)}$$

## Sensitivity to Array-Manifold Mismatch

Capon's MVB assumes the array manifold $a(\theta)$ is known exactly. In practice, imprecise knowledge of the angle of arrival or array calibration errors cause the SINR to degrade **catastrophically** for modest differences between the assumed and actual array response. Classical remedies include [[concepts/diagonal-loading|diagonal loading]] and eigenvalue thresholding, but these require heuristic parameter choice and ignore *anisotropic* knowledge of manifold variation. The [[concepts/robust-minimum-variance-beamforming|Robust MVB (RMVB)]] of Lorenz & Boyd (2005) addresses this by enforcing the unity-gain constraint over an entire [[concepts/ellipsoidal-uncertainty-modeling|uncertainty ellipsoid]] of possible array responses, formulated as a [[concepts/socp-optimization|second-order cone program]].

## Relationship to LCMV

The MVDR is a special case of the [[concepts/lcmv-beamformer|LCMV beamformer]] with a single distortionless constraint.

## Relationship to VSLF

The MVDR is a special case of the [[concepts/variable-span-linear-filter|Variable Span Linear Filter]] with $\mu=0$ and $Q=P$ (true rank of $\Phi_x$).

## Related Concepts

- [[concepts/beamforming|Beamforming]]
- [[concepts/robust-minimum-variance-beamforming|Robust Minimum Variance Beamforming (RMVB)]]
- [[concepts/ellipsoidal-uncertainty-modeling|Ellipsoidal Uncertainty Modeling]]
- [[concepts/mpdr-beamformer|MPDR Beamformer]]
- [[concepts/lcmv-beamformer|LCMV Beamformer]]
- [[concepts/gsc-beamformer|Generalized Sidelobe Canceller]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/variable-span-linear-filter|Variable Span Linear Filter]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/diagonal-loading|Diagonal Loading]]
- [[concepts/white-noise-gain|White Noise Gain]]

## Related Sources

- [[sources/lorenz-2005-robust-minimum-variance-beamforming|Lorenz & Boyd 2005: Robust Minimum Variance Beamforming]]
- [[sources/oviste-2026-neural-vslf-speech-enhancement|Oviste 2026: Neural VSLF for Speech Enhancement]]
- [[sources/mittal-2026-adaptive-diagonal-loading-beamforming|Mittal et al. 2026: Adaptive Diagonal Loading for Norm Constrained Beamforming]]
- [[sources/lee-2026-spatial-magnifier-spatial-upsampling|Lee et al. 2026: Spatial-Magnifier]]
