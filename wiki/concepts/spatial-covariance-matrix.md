---
type: concept
created: 2026-04-29
updated: 2026-04-30
tags:
  - array-processing
  - spatial-statistics
  - speech-enhancement
---

# Spatial Covariance Matrix

The **Spatial Covariance Matrix (SCM)** captures the second-order statistics of multi-channel signals across microphone arrays.

## Definition

For a multi-channel signal $x \in \mathbb{C}^M$:

$$\Phi_x = \mathbb{E}[xx^H]$$

## Role in Speech Enhancement

- **Clean-speech SCM** ($\Phi_x$): Characterizes spatial properties of target speech
- **Noise SCM** ($\Phi_n$): Characterizes spatial properties of interference/noise
- Used in MWF, MVDR, GEV beamformer, and VSLF weight computation

## Estimation

SCMs can be estimated via:
- Sample covariance from noise-only periods
- DNN-based prediction (e.g., HVSF architecture)
- Voice activity detection-guided updates

## SCM Reconstruction via Normalized Decomposition

Liu et al. (2026) propose decomposing the **normalized** SCM as a linear combination of predefined coherence matrices:

$$\Gamma_y = \sum_{i=1}^{I} \psi_i \Gamma_i + \psi_R \Gamma_d + \psi_V I_M$$

where $\psi_i, \psi_R, \psi_V$ are **variance ratios** (non-negative, sum to 1), $\Gamma_i$ are source coherence matrices (from RTF or DOA), $\Gamma_d$ is the diffuse-field coherence matrix, and $I_M$ is the identity matrix. The variance ratios are estimated via a lightweight multiplicative update algorithm with KL-divergence regularization, achieving $\mathcal{O}(M^2(I+2))$ complexity.

### Key Insight

Normalization by trace transforms the SCM estimation problem from estimating absolute variances to estimating **relative variance ratios** — a simpler constrained optimization with non-negativity and unity-sum constraints, solvable by multiplicative updates.

## Related Concepts

- [[../concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[../concepts/beamforming|Beamforming]]
- [[../concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[../concepts/mvdr-beamformer|MVDR Beamformer]]
- [[../concepts/variable-span-linear-filter|Variable Span Linear Filter]]
- [[../concepts/spatial-coherence|Spatial Coherence]]
- [[../concepts/variance-ratio-estimation|Variance Ratio Estimation]]

## Related Sources

- [[../sources/oviste-2026-neural-vslf-speech-enhancement|Oviste 2026: Neural VSLF for Speech Enhancement]]
- [[../sources/liu-2026-scm-reconstruction-speech-enhancement|Liu 2026: SCM Reconstruction for Speech Enhancement]]
