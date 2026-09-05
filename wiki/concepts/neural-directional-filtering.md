---
type: concept
created: 2026-05-13
updated: 2026-09-05
sources:
  - raw/papers/tesch-2023-insights-deep-nonlinear-filters/full-text.md
  - raw/papers/wechsler-2024-neural-directional-filtering/full-text.md
  - raw/papers/huang-2025-steerable-neural-directional-filtering/full-text.md
tags:
  - neural-directional-filtering
  - virtual-directional-microphone
  - spatial-audio
  - deep-learning
---

# Neural Directional Filtering

Neural directional filtering (NDF) is a data-driven approach for reconstructing a virtual directional microphone (VDM) with a desired directivity pattern from a compact microphone array. By using a deep neural network to learn the input-output behavior of an ideal directional microphone, NDF achieves frequency-invariant target directivity patterns on arrays with limited microphones and small apertures.

The concept was introduced and formalized by [[entities/julian-wechsler|Wechsler]] et al. (IWAENC 2024): a DNN estimates a single-channel complex mask from the array signals, applied to a reference microphone to render the VDM signal, replacing the DOA-estimation-and-gain pipeline of parametric directional filtering (and its reliance on W-disjoint orthogonality).

## Founding Study Findings (Wechsler et al. 2024)

- **Training-data composition is decisive**: the training set must contain multi-speaker scenes with speaker positions densely sampling the desired pattern (positions on a circle concentric with the array). Single-speaker training fails to generalize to multi-speaker scenes; training on ≥2 speakers generalizes up to six; beyond three brings no significant gain.
- **Higher-order patterns with fewer microphones**: a 3rd-order DMA pattern (classically a 6-microphone CDMA) was realized with 4 microphones at 18.4 dB mean SDR, versus −5.9 dB for an LS beamformer and 12.7 dB for a parametric baseline.
- **Baseline failure modes**: parametric filtering excels with a single source but degrades with multiple concurrent sources; fixed LS beamforming is limited by white-noise amplification and cannot approximate the 3rd-order pattern with 4 microphones.

## Problem Formulation

Given a compact array of $Q$ omnidirectional microphones, NDF estimates a VDM signal:

$$Z_{\mathrm{vdm}}(f,t)=\sum_{n=1}^{N}H_{\mathrm{vdm},n}(f;\Lambda)\,X_{n}(f,t)$$

where $\Lambda(\theta,\phi)$ is the desired directivity pattern, and $H_{\mathrm{vdm},n}(f;\Lambda)$ weights each propagation path by the directivity gain at its incident direction.

## Key Approaches

| Approach | Description | Key Features |
|----------|-------------|--------------|
| FT-JNF | Joint spatial and temporal-spectral nonlinear filtering | Uses BiLSTM + UniLSTM for mask estimation |
| SNDF | Steerable NDF (Huang et al. 2025) | Steering direction as conditioning input; single model steers to any direction at inference |
| Dual-mask NDF (NDF+) | Extended FT-JNF with two parallel mask branches | Joint coherent/diffuse estimation |
| SHONDC | Steerable high-order neural directional coding | Supports steerable directivity patterns |
| UNDF | NDF with user-defined directivity patterns | Flexible directivity configuration |

## Steerable Extension (SNDF)

[[concepts/steerable-neural-directional-filtering|SNDF]] (Huang et al., Euronoise 2025) removes NDF's restriction to a static, fixed-look-direction pattern per model: the steering direction $\theta_s$ is one-hot encoded and injected as the initial states of the F-BiLSTM, so one trained model renders the learned pattern at any direction — with steering-invariant pattern quality and consistent SDR across directions, and 6th-order patterns learned from only 4 microphones.

## Architecture

The FT-JNF-based NDF architecture processes concatenated real/imaginary STFT coefficients $[B,T,F,2Q]$ through:
1. **Frequency processing**: BiLSTM along frequency dimension
2. **Temporal processing**: UniLSTM along time dimension
3. **Mask estimation**: Linear layer with tanh activation producing complex mask
4. **Signal reconstruction**: Mask applied to reference microphone signal

## Related Concepts

- [[concepts/virtual-directional-microphone|Virtual Directional Microphone]]
- [[concepts/directivity-pattern|Directivity Pattern]]
- [[concepts/fixed-beamformer|Fixed Beamformer]]
- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/joint-nonlinear-filtering|Joint Nonlinear Filtering]]

## Related Sources

- [[sources/wechsler-2024-neural-directional-filtering|Wechsler et al. 2024: Neural Directional Filtering]] — founding paper: formalizes the task, investigates training-data composition, demonstrates 3rd-order patterns with 4 microphones
- [[sources/huang-2025-steerable-neural-directional-filtering|Huang et al. 2025: Steerable Neural Directional Filtering]] — extends NDF to steerable patterns with a single conditioned model
- [[sources/tesch-2023-insights-deep-nonlinear-filters|Tesch & Gerkmann 2023: Insights Into Deep Non-linear Filters for Improved Multi-channel Speech Enhancement]] — origin of the FT-JNF backbone used by NDF [22]
- [[sources/huang-2026-ndf-joint-neural-directional-filtering|Huang et al. 2026: NDF+]]
