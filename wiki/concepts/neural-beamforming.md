---
type: concept
created: 2026-05-20
updated: 2026-07-09
tags:
  - beamforming
  - deep-learning
  - microphone-array
  - multi-channel
---

# Neural Beamforming

**Neural beamforming** refers to the use of deep neural networks to learn beamforming weights directly from data, as opposed to using predetermined beamformers (e.g., MVDR, NLCMV) that rely on explicit signal models and environmental assumptions. Neural beamformers are trained end-to-end and can adapt to complex, real-world acoustic conditions.

## Motivation

Conventional beamformers (MVDR, NLCMV, etc.) rely on assumptions such as:
- Known microphone geometry and steering vectors
- Stationary noise fields
- Diffuse noise models

These assumptions often fail in practice. Neural beamforming avoids them by learning spatial filtering from data, discovering optimal beam patterns for the target task.

## Approaches

### Beamformer Weight Learning

The predetermined beamformer weights are used as initialization, and the weights are fine-tuned via backpropagation during task training. This is used in the Feng et al. (2025) directional source separation work, where NLCMV weights for 13 steering directions are loaded as a convolutional layer and updated during separation training. The learned beamformers develop strong lateral suppression (~10 dB gain at side directions).

### End-to-End Neural Beamforming

The beamforming operation is embedded as a differentiable layer (e.g., a filter-and-sum layer) within a larger neural network. The network learns to compute optimal filter coefficients from the multi-channel input:

- **FaSNet** (Filter-and-Sum Network): Time-domain filter-and-sum layer that learns beamforming coefficients
- **Neural MVDR**: DNN-estimated signal statistics plugged into the MVDR formula, forming a differentiable beamformer
- **Differentiable robust MVDR**: Closed-form WNG-constrained MVDR solution embedded as a differentiable layer with learnable frequency-dependent WNG thresholds (Deng et al. 2026)
- **BEAMNET**: Fully learned spatial filtering with no explicit signal model

### Integration with Downstream Tasks

Neural beamformers are often trained jointly with downstream models:

- **Speech separation**: Beamforming front-end + separation back-end trained together (Feng et al. 2025)
- **ASR**: Neural beamforming + end-to-end ASR trained jointly
- **Speech enhancement**: Beamforming + enhancement network

## Advantages

- No explicit assumption about microphone geometry
- Adapts to real-world noise conditions
- Can combine spatial and spectral processing in one network
- Joint training with downstream tasks optimizes for the final metric

## Related Sources

- [[sources/feng-2025-directional-source-separation-smart-glasses|Feng et al. 2025: Directional Source Separation for Smart Glasses]]
- [[sources/deng-2026-joint-covariance-wng-mvdr|Deng et al. 2026: Joint Covariance and WNG Learning for Robust MVDR]]
