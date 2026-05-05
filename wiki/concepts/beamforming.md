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
- **MVDR (Minimum Variance Distortionless Response)**: An adaptive beamformer that minimizes total output power while maintaining a constant gain in the target direction.
- **GSC (Generalized Sidelobe Canceller)**: A structure that splits the beamformer into a fixed path and an adaptive interference-cancellation path.
- **Neural Beamforming**: Using deep learning models (e.g., U-Nets or LSTMs) to perform spatial filtering in complex, multi-path environments.

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

## Related Concepts

- [[transparency-mode|Transparency Mode]]
- [[voice-activity-detection|Voice Activity Detection]]
- [[active-noise-control|Active Noise Control]]
- [[roi-beamforming|Region-of-Interest Beamforming]]

## Related Sources

- [[../sources/masilamani-2024-headphone-conversation-detect-paper-reading-note|Masilamani 2024: Headphone Conversation Detect]]
- [[../sources/frank-2026-low-latency-roi-beamforming|Frank & Cohen 2026: Low-latency Audio Front-end ROI Beamforming for Smart Glasses]]
