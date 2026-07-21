---
type: concept
created: 2026-04-29
updated: 2026-07-21
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
- **Joint AEC+NS+DR (DeepVQE)**: Unified model with cross-attention alignment and complex convolving mask for simultaneous echo/noise/reverb removal
- **Quality-Aware Dual-Microphone SE (QuaSE)**: Dynamically fuses quality-varying in-ear speech with noisy airborne speech via self-supervised quality assessment; addresses [[concepts/ear-canal-deformation|ECD]]-induced modality imbalance in earables
- **[[concepts/output-based-speech-enhancement|Output-based SE]]**: Configures the system by evaluating SI/SQ of candidate outputs (rather than extracting input features from noisy signals); demonstrated by Apostolidis et al. (2026) via GP-selected [[concepts/mpdr-beamformer|MPDR]] beamforming

## Related Concepts

- [[concepts/beamforming|Beamforming]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/variable-span-linear-filter|Variable Span Linear Filter]]
- [[concepts/virtual-microphone-estimation|Virtual Microphone Estimation]]
- [[concepts/spatial-audio-representation-learning|Spatial Audio Representation Learning]]
- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]]
- [[concepts/complex-convolving-mask|Complex Convolving Mask]]
- [[concepts/quality-aware-speech-enhancement|Quality-Aware Speech Enhancement]]
- [[concepts/ear-canal-deformation|Ear Canal Deformation]]
- [[concepts/output-based-speech-enhancement|Output-based Speech Enhancement]]
- [[concepts/glimpse-proportion|Glimpse Proportion]]
- [[concepts/mpdr-beamformer|MPDR Beamformer]]

## Related Sources

- [[sources/oviste-2026-neural-vslf-speech-enhancement|Oviste 2026: Neural VSLF for Speech Enhancement]]
- [[sources/liu-2026-scm-reconstruction-speech-enhancement|Liu 2026: SCM Reconstruction for Speech Enhancement]]
- [[sources/zaidel-2026-linearly-constrained-deep-beamformer|Zaidel et al. 2026: Linearly Constrained Deep Beamformer]]
- [[sources/lee-2026-spatial-magnifier-spatial-upsampling|Lee et al. 2026: Spatial-Magnifier]]
- [[sources/indenbom-2023-deepvqe|Indenbom et al. 2023: DeepVQE]]
- [[sources/han-2026-quality-aware-earable-se|Han et al. 2026: QuaSE — Quality-Aware Earable Dual-Microphone SE]]
- [[sources/apostolidis-2026-listen-first-output-based-multi-microphone|Apostolidis et al. 2026: Listen first — output-based multi-microphone speech enhancement]]
