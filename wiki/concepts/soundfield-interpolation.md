---
type: concept
created: 2026-06-25
updated: 2026-06-25
tags:
  - acoustics
  - signal-processing
  - soundfield-reproduction
  - interpolation
---

# Soundfield Interpolation

## Overview

**Soundfield Interpolation** is the task of estimating the acoustic pressure (soundfield) at unmeasured spatial positions from measurements at a limited set of known positions. It is a core component of [[virtual-sensing|Virtual Sensing]], [[active-noise-control|Active Noise Control]], spatial audio, and acoustic holography.

## Problem Statement

Given pressure measurements $p(\mathbf{r}_q, n)$ at $Q$ monitoring positions $\{\mathbf{r}_q\}_{q=1}^Q$, estimate the pressure $\hat{p}(\mathbf{r}_v, n)$ at $V$ virtual positions $\{\mathbf{r}_v\}_{v=1}^V$.

## Methods

### Spherical Harmonics Decomposition

Sound pressure on a sphere is decomposed onto SH basis functions. Requires $Q > (U+1)^2$ microphones to accurately estimate SH coefficients up to order $U$.

### Physics-Informed Neural Network (PINN)

A [[physics-informed-neural-network|PINN]] takes space-time coordinates as inputs and outputs pressure. Trained on a combined loss: data MSE at monitoring positions plus PDE residual enforcing the acoustic wave equation at collocation points. Enables interpolation with fewer microphones than SH methods.

### Comparison

| Method | Prior Knowledge | Mic. Requirement | Performance |
|--------|-----------------|------------------|-------------|
| Spherical Harmonics | Array geometry, free-field | $Q > (U+1)^2$ | Limited by SH order |
| PINN | Wave equation, collocation points | $Q$ can be small | ~8 dB better than SH with $Q=8$ |
| RMT | Acoustic path model | Any | Depends on training quality |

## Related Concepts

- [[physics-informed-neural-network|Physics-Informed Neural Network]]
- [[virtual-sensing|Virtual Sensing]]
- [[active-noise-control|Active Noise Control]]
- [[spherical-harmonic-transform|Spherical Harmonic Transform]]
- [[remote-microphone-technique|Remote Microphone Technique]]
