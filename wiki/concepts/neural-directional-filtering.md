---
type: concept
created: 2026-05-13
updated: 2026-05-13
tags:
  - neural-directional-filtering
  - virtual-directional-microphone
  - spatial-audio
  - deep-learning
---

# Neural Directional Filtering

Neural directional filtering (NDF) is a data-driven approach for reconstructing a virtual directional microphone (VDM) with a desired directivity pattern from a compact microphone array. By using a deep neural network to learn the input-output behavior of an ideal directional microphone, NDF achieves frequency-invariant target directivity patterns on arrays with limited microphones and small apertures.

## Problem Formulation

Given a compact array of $Q$ omnidirectional microphones, NDF estimates a VDM signal:

$$Z_{\mathrm{vdm}}(f,t)=\sum_{n=1}^{N}H_{\mathrm{vdm},n}(f;\Lambda)\,X_{n}(f,t)$$

where $\Lambda(\theta,\phi)$ is the desired directivity pattern, and $H_{\mathrm{vdm},n}(f;\Lambda)$ weights each propagation path by the directivity gain at its incident direction.

## Key Approaches

| Approach | Description | Key Features |
|----------|-------------|--------------|
| FT-JNF | Joint spatial and temporal-spectral nonlinear filtering | Uses BiLSTM + UniLSTM for mask estimation |
| Dual-mask NDF (NDF+) | Extended FT-JNF with two parallel mask branches | Joint coherent/diffuse estimation |
| SHONDC | Steerable high-order neural directional coding | Supports steerable directivity patterns |
| UNDF | NDF with user-defined directivity patterns | Flexible directivity configuration |

## Architecture

The FT-JNF-based NDF architecture processes concatenated real/imaginary STFT coefficients $[B,T,F,2Q]$ through:
1. **Frequency processing**: BiLSTM along frequency dimension
2. **Temporal processing**: UniLSTM along time dimension
3. **Mask estimation**: Linear layer with tanh activation producing complex mask
4. **Signal reconstruction**: Mask applied to reference microphone signal

## Related Concepts

- [[../concepts/virtual-directional-microphone|Virtual Directional Microphone]]
- [[../concepts/directivity-pattern|Directivity Pattern]]
- [[../concepts/fixed-beamformer|Fixed Beamformer]]
- [[../concepts/differential-microphone-array|Differential Microphone Array]]
- [[../concepts/joint-nonlinear-filtering|Joint Nonlinear Filtering]]

## Related Sources

- [[../sources/huang-2026-ndf-joint-neural-directional-filtering|Huang et al. 2026: NDF+]]
