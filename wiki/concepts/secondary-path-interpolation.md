---
type: concept
created: 2026-05-06
updated: 2026-05-06
sources:
  - raw/papers/holzmuller-2026-dtw-secondary-path-anc/full-text.md
tags:
  - active-noise-control
  - secondary-path
  - interpolation
  - spatial-audio
---

# Secondary Path Interpolation

**Secondary Path Interpolation** is the process of estimating the [[../concepts/secondary-path-modeling|secondary path]] at unmeasured positions by interpolating between pre-recorded impulse responses at known measurement positions. This is essential for local [[../concepts/active-noise-control|ANC]] systems with moving listeners, where the secondary path changes as the point of cancellation moves.

## Problem Statement

In a local ANC system, the secondary path $\hat{\mathbf{g}}(\Psi)$ is measured at $N_\Psi$ discrete positions $\underline{\Psi}$. For a listener at an intermediate position $\Psi_{\text{int}}[n]$, the secondary path must be estimated from the pre-recorded database. The key challenge is that adjacent impulse responses exhibit different propagation delays and reflection patterns, making direct time-domain interpolation problematic.

## Interpolation Methods

### Nearest-Neighbor (NN)

Select the secondary path from the closest measurement position:

$$\tilde{\mathbf{g}}_{\text{NN}}[n] = \hat{\mathbf{g}}(\Psi_{\text{NN}}[n])$$

Simple but introduces discontinuities and high system mismatch at intermediate positions.

### Linear Interpolation (LI)

Blend coefficients from adjacent positions with factor $\alpha$:

$$\tilde{\mathbf{g}}_{\text{LI}}[n] = (1 - \alpha[n])\hat{\mathbf{g}}(\Psi_-) + \alpha[n]\hat{\mathbf{g}}(\Psi_+)$$

Produces pre-echo effects and temporal smearing because phase differences between positions are not accounted for.

### Global Time Alignment (GA)

Estimate a global time offset via cross-correlation before linear interpolation. Compensates for bulk delay differences but cannot handle nonlinear time variations such as different reflection patterns.

### DTW-Based Interpolation

Uses [[../concepts/dynamic-time-warping|Dynamic Time Warping]] to align impulse responses sample-by-sample before interpolation, then de-warps the result via cubic spline interpolation. Achieves the lowest system mismatch, especially for coarse measurement grids.

## Performance Comparison

System mismatch (dB) for lateral translation with 15 cm spacing (Holzmüller & Sontacchi 2026):

| Method | SM (dB) | Stable Freq. Range |
|--------|---------|-------------------|
| NN | 2.49 | ~1.2 kHz |
| LI | 1.78 | ~1.1 kHz |
| GA | −9.85 | ~7.7 kHz |
| DTW | −17.65 | ~7.8 kHz |

DTW-based interpolation reduces the required number of measurement positions substantially while extending the controlled frequency bandwidth.

## Relationship to Spatial Audio

The interpolation problem is analogous to HRIR/BRIR interpolation in spatial audio, where similar phase alignment challenges exist. DTW has been successfully applied in both domains, though ANC requires higher phase accuracy throughout the controlled frequency range for stability, while auralization primarily requires magnitude accuracy at high frequencies.

## Related Concepts

- [[../concepts/dynamic-time-warping|Dynamic Time Warping]]
- [[../concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[../concepts/offline-secondary-path-modeling|Offline Secondary-Path Modeling]]
- [[../concepts/active-noise-control|Active Noise Control]]
- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]

## Related Sources

- [[../sources/holzmuller-2026-dtw-secondary-path-anc|Holzmüller & Sontacchi 2026: DTW for Secondary Path Interpolation in ANC]]
