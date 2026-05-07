---
type: concept
created: 2026-04-12
updated: 2026-04-28
sources:
  - raw/papers/frank-2026-low-latency-roi-beamforming/full-text.txt
tags:
- acoustics
- antenna-theory
- signal-processing
---

# Beamforming

**Beamforming** (or spatial filtering) is a signal processing technique used in sensor arrays for directional signal transmission or reception.

## Overview

In the context of microphones, beamforming combines signals from multiple microphones so that sounds from a specific direction (the "beam") are amplified through constructive interference, while sounds from other directions are attenuated through destructive interference.

## Beamforming in Headphones

Modern ANC headphones use beamforming for several critical tasks:
1. **Clear Voice Pickup**: Focusing on the user's mouth during phone calls to suppress background noise.
2. **Conversation Focusing**: In **[[transparency-mode|Transparency Mode]]**, beamforming can focus on a person speaking in front of the user (Target Voice Activity Detection - TVAD).
3. **Adaptive Aperture**: Advanced systems can dynamically adjust the width and angle of the beam based on the user's head movement (measured via IMU) and the detected location of the speaker (Masilamani 2024).

## Common Beamforming Techniques

- **Delay-and-Sum**: The simplest form, where signals are shifted in time and added.
- **[[mpdr-beamformer|MPDR (Minimum Power Distortionless Response)]]**: Minimizes total output power while maintaining a constant gain in the target direction.
- **[[mvdr-beamformer|MVDR (Minimum Variance Distortionless Response)]]**: Minimizes interference-plus-noise power while maintaining a constant gain in the target direction.
- **[[gsc-beamformer|GSC (Generalized Sidelobe Canceller)]]**: A structure that splits the beamformer into a fixed path and an adaptive interference-cancellation path.
- **Neural Beamforming**: Using deep learning models (e.g., U-Nets or LSTMs) to perform spatial filtering in complex, multi-path environments.

## Robustness and Diagonal Loading

Adaptive beamformers are vulnerable to snapshot deficiency — when the number of available frames $L$ is less than or comparable to the number of microphones $M$, the sample [[spatial-covariance-matrix|spatial correlation matrix]] becomes ill-conditioned. This causes the [[white-noise-gain|White Noise Gain]] (WNG) to collapse and leads to severe target signal cancellation.

**[[diagonal-loading|Diagonal Loading]]** is the classical remedy: adding a scaled identity matrix $\mu\mathbf{I}$ to the SCM before inversion bounds the [[condition-number|condition number]] and stabilizes the weight vector. Mittal et al. (2026) propose an adaptive diagonal loading method using the [[kantorovich-inequality|Kantorovich inequality]] to deterministically guarantee WNG stays within specified bounds, with three scalable estimation modes (Trace, Gershgorin, Exact EVD).

## Dynamic Aperture Adjustment (Patent US20240363094A1)

Masilamani (2024) proposes a system that adjusts the beamforming aperture based on the user's head orientation:
- **Focused Beam**: When the user looks directly at a speaker, the beam narrows (< 180°) to maximize clarity.
- **Wide Beam**: When the user looks away, the beam expands immediately to maintain environmental awareness.

## Region-of-Interest (ROI) Beamforming for Wearables

Frank & Cohen (2026) developed a unified formulation for **least-distortion maximum-gain (LDMG) ROI beamformers** for smart glasses, comparing time-domain and STFT-domain implementations:

- **ROI beamforming** preserves signals from a spatial region rather than a single DOA, accommodating head motion and DOA uncertainty
- **Time-domain implementation** delivers 2x lower algorithmic latency (Ly/2 vs Ly samples) and higher performance across all metrics (DF, WNG, own-voice suppression)
- **Trade-off**: Time-domain requires M Ly² real multiplications vs O(M Ly log₂ Ly) for STFT-domain
- **Conclusion**: When low latency is critical and modest additional on-device computing power is available, time-domain ROI beamforming is preferred for smart-glasses front ends

See [[roi-beamforming|Region-of-Interest Beamforming]] for details.

## Maximum Radial Energy (max-rE) Beamformer

The $\max\text{-}\mathbf{r}_E$ beamformer maximizes the radial energy efficiency of a spherical microphone array by applying optimized modal weights $w_l$ to spherical harmonic coefficients. Used by Görtz et al. (2026) for computing directional RIRs in [[direction-dependent-acoustic-parameters|DDAP]] ground truth generation:

$$h_{\boldsymbol{\theta}_j}[n] = \sum_{l=0}^{L} \sum_{m=-l}^{l} w_l Y_{lm}(\boldsymbol{\theta}_j) \mathbf{h}_{lm}^{(\circ)}[n]$$

The beamformer's directivity increases with SH order $L$, but higher orders require more microphones and are susceptible to spatial aliasing at high frequencies.

## Related Concepts

- [[transparency-mode|Transparency Mode]]
- [[voice-activity-detection|Voice Activity Detection]]
- [[active-noise-control|Active Noise Control]]
- [[roi-beamforming|Region-of-Interest Beamforming]]
- [[mpdr-beamformer|MPDR Beamformer]]
- [[mvdr-beamformer|MVDR Beamformer]]
- [[gsc-beamformer|Generalized Sidelobe Canceller]]
- [[diagonal-loading|Diagonal Loading]]
- [[white-noise-gain|White Noise Gain]]
- [[kantorovich-inequality|Kantorovich Inequality]]
- [[condition-number|Condition Number]]

## Related Sources

- [[../sources/masilamani-2024-headphone-conversation-detect-paper-reading-note|Masilamani 2024: Headphone Conversation Detect]]
- [[../sources/frank-2026-low-latency-roi-beamforming|Frank & Cohen 2026: Low-latency Audio Front-end ROI Beamforming for Smart Glasses]]
- [[../sources/mittal-2026-adaptive-diagonal-loading-beamforming|Mittal et al. 2026: Adaptive Diagonal Loading for Norm Constrained Beamforming]]
