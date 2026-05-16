---
type: concept
created: 2026-04-29
updated: 2026-04-30
tags:
  - speech-enhancement
  - multi-channel
  - array-processing
---

# Multi-Channel Speech Enhancement

**Multi-Channel Speech Enhancement (MCSE)** uses multiple microphones to improve speech quality and intelligibility by exploiting spatial information.

## Categories

| Category | Examples | Characteristics |
|:---------|:---------|:----------------|
| Linear filtering (probabilistic) | MWF, MVDR, GEV beamformer | Interpretable, controllable tradeoff |
| End-to-end data-driven | Neural network-based | Black box, implicit tradeoff |
| Hybrid methods | DNN-guided linear filters | Combines interpretability with data-driven estimation |

## Key Techniques

- **Beamforming**: Spatial filtering to enhance signals from target direction
- **Multi-Channel Wiener Filter (MWF)**: Optimal linear filter minimizing MSE
- **MVDR Beamformer**: Minimum Variance Distortionless Response
- **GEV Beamformer**: Generalized Eigenvalue Decomposition-based beamformer
- **Variable Span Linear Filter (VSLF)**: Generalized framework with controllable tradeoff
- **SCM Reconstruction-Based MWF (R-MWF)**: Reconstructs SCM from variance ratios and predefined coherence matrices; lightweight online algorithm

## Related Concepts

- [[concepts/beamforming|Beamforming]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/variable-span-linear-filter|Variable Span Linear Filter]]
- [[concepts/virtual-microphone-estimation|Virtual Microphone Estimation]]
- [[concepts/spatial-audio-representation-learning|Spatial Audio Representation Learning]]

## Related Sources

- [[sources/oviste-2026-neural-vslf-speech-enhancement|Oviste 2026: Neural VSLF for Speech Enhancement]]
- [[sources/liu-2026-scm-reconstruction-speech-enhancement|Liu 2026: SCM Reconstruction for Speech Enhancement]]
- [[sources/lee-2026-spatial-magnifier-spatial-upsampling|Lee et al. 2026: Spatial-Magnifier]]
