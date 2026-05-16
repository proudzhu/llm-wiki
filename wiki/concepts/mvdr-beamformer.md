---
type: concept
created: 2026-04-29
updated: 2026-04-29
tags:
  - beamforming
  - speech-enhancement
  - array-processing
---

# MVDR Beamformer

The **Minimum Variance Distortionless Response (MVDR)** beamformer minimizes output noise power while maintaining unity gain in the target direction.

## Formulation

$$h_{\text{MVDR}} = \frac{\Phi_n^{-1} a}{a^H \Phi_n^{-1} a}$$

where $a$ is the steering vector for the target direction and $\Phi_n$ is the noise spatial covariance matrix.

## Relationship to VSLF

The MVDR is a special case of the [[concepts/variable-span-linear-filter|Variable Span Linear Filter]] with $\mu=0$ and $Q=P$ (true rank of $\Phi_x$).

## Related Concepts

- [[concepts/beamforming|Beamforming]]
- [[concepts/mpdr-beamformer|MPDR Beamformer]]
- [[concepts/gsc-beamformer|Generalized Sidelobe Canceller]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/variable-span-linear-filter|Variable Span Linear Filter]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/diagonal-loading|Diagonal Loading]]
- [[concepts/white-noise-gain|White Noise Gain]]

## Related Sources

- [[sources/oviste-2026-neural-vslf-speech-enhancement|Oviste 2026: Neural VSLF for Speech Enhancement]]
- [[sources/mittal-2026-adaptive-diagonal-loading-beamforming|Mittal et al. 2026: Adaptive Diagonal Loading for Norm Constrained Beamforming]]
- [[sources/lee-2026-spatial-magnifier-spatial-upsampling|Lee et al. 2026: Spatial-Magnifier]]
