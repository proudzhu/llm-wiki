---
type: concept
created: 2026-05-12
updated: 2026-05-12
tags:
  - speech-enhancement
  - virtual-microphone
  - array-processing
  - spatial-upsampling
---

# Virtual Microphone Estimation

**Virtual Microphone Estimation (VME)** is the task of estimating signals at microphone positions that are not physically present, using signals from a limited set of real microphones. A Virtual Microphone (VM) is defined as a captured signal available during training but absent during inference.

## Problem Definition

Given real microphone (RM) signals $\mathbf{r} \in \mathbb{R}^{M_r \times N}$, estimate virtual microphone signals $\hat{\mathbf{v}} \in \mathbb{R}^{M_v \times N}$:

$$\hat{\mathbf{v}} = \text{Neural-VME}(\mathbf{r})$$

The augmented signal $\bar{\mathbf{y}} = [\mathbf{r}, \hat{\mathbf{v}}]$ increases the effective array size from $M_r$ to $M = M_r + M_v$, boosting spatial diversity for downstream processing.

## Approaches

| Method | Architecture | Key Feature | Params |
|:-------|:-------------|:------------|:-------|
| MC Conv-TasNet (STL) | Conv-TasNet | Single-task learning | 13.0M |
| MC Conv-TasNet (MTL) | Conv-TasNet | Multi-task learning (VME + BF) | 13.0M |
| SpatialNet-VME | SpatialNet | Reuse SE architecture for VME | 1.2M |
| Spatial-Magnifier | GAN + DBPN | Specialized for spatial upsampling | 1.2M |

## Applications

- **VM-BF (Virtual Microphone-Based Beamforming)**: Augmented signal used to compute SCMs for adaptive beamforming (MCWF, MVDR)
- **VM-SE (Virtual Microphone-Based Speech Enhancement)**: VM signals/features condition end-to-end MC-SE models directly
- **Universal Acoustic Vision**: Increase ambisonic order via super-resolution architectures

## Key Insight

The primary advantage of Neural-VME lies in **decoupling spatial representation learning from spectral enhancement**. Estimating VM signals forces the system to learn robust spatial representations that directly benefit downstream MC-SE performance, rather than simply interpolating waveforms.

## Related Concepts

- [[concepts/spatial-audio-representation-learning|Spatial Audio Representation Learning]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/remote-microphone-technique|Remote Microphone Technique]]

## Related Sources

- [[sources/lee-2026-spatial-magnifier-spatial-upsampling|Lee et al. 2026: Spatial-Magnifier]]
- [[sources/farmani-2026-virtual-mic-beamforming-hearing-aid|Farmani 2026: VM Beamforming for Hearing Aids]]
