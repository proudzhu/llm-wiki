---
type: source
created: 2026-05-17
updated: 2026-05-17
sources:
  - raw/papers/holzmuller-2025-deep-observation-filter-virtual-sensing-active-noise-control/full-text.md
  - https://www.researchgate.net/publication/392928626
  - zotero://select/items/0_5KW3SUYE
tags:
  - active-noise-control
  - virtual-sensing
  - remote-microphone-technique
  - convolutional-neural-network
  - gcc-phat
  - deep-learning
aliases:
  - 'Holzmuller & Sontacchi 2025: Deep Observation Filter for Virtual Sensing ANC'
---

# Holzmuller & Sontacchi 2025: Deep Observation Filter for Virtual Sensing in Local Active Noise Control

**Authors**: Felix Holzmuller, Alois Sontacchi
**Institution**: Institute of Electronic Music and Acoustics, University of Music and Performing Arts Graz, Austria
**Published**: Forum Acusticum / Euronoise, June 2025
**📎 Zotero**: [zotero://select/items/0_5KW3SUYE](zotero://select/items/0_5KW3SUYE)
**Code**: [GitHub](https://github.com/fholzm/Obs-TasNet) (shared with follow-up work)

## Summary

Proposes a **CNN-based online estimation** of the observation filter in the **Remote Microphone Technique (RMT)** for local active noise control. Unlike traditional RMT requiring pre-computed filter databases and selection logic, a lightweight encoder-decoder CNN (366.94k params, 1.34M ops/inference) takes **GCC-PHAT** features between remote microphones and **virtual microphone coordinates** as input, and outputs FIR filter coefficients for the observation filter. The approach supports **variable virtual microphone positions** and various acoustic scenarios without filter selection. Evaluated on synthetic data in pyroomacoustics, achieving −33.53 dB NMSE with accurate position data.

## Problem Statement

Local ANC requires the error signal at the point of cancellation, but placing sensors there is often infeasible. Virtual sensing via RMT estimates this signal using nearby physical microphones and pre-computed filters. However, conventional RMT requires a large database of pre-computed filters for different acoustic scenarios and virtual positions, plus a filter-selection mechanism during operation — creating a scalability challenge.

## Methodology

### RMT Formulation

The residual noise at the listener's position $$E(z) = D_e(z) + G_e(z)U(z)$$ combines primary disturbances and secondary-path-filtered control signals. Physical remote microphones capture $$\mathbf{M}(z) = \mathbf{D}_m(z) + \mathbf{G}_m(z)U(z)$$. The primary disturbances at remote positions are extracted as $$\hat{\mathbf{D}}_m(z) = \mathbf{M}(z) - \hat{\mathbf{G}}_m(z)U(z)$$, then passed through the observation filter $$\mathbf{O}(z)$$ to estimate the virtual error: $$\hat{D}_e(z) = \mathbf{O}(z)\hat{\mathbf{D}}_m(z)$$. The final virtual error estimate combines this with the filtered control signal: $$\hat{E}(z) = \hat{D}_e(z) + \hat{G}_e(z)U(z)$$.

### Neural Observation Filter

- **Input features**: GCC-PHAT between all unique remote microphone pairs (6 pairs for 4 mics, 29 values each) + 3D Cartesian coordinates of the virtual microphone
- **GCC-PHAT**: $$r_{x_1x_2}[k] \xleftarrow{\mathrm{IDFT}} \frac{1}{|S_{x_1x_2}(f)|} S_{x_1x_2}(f)$$, with exponentially weighted moving average CSD estimation
- **Architecture**: Encoder-decoder CNN with 4 encoder stages (Conv1d, leaky ReLU), bottleneck with concatenated position coordinates (2 linear layers), and 4 decoder stages (ConvT1d), outputting 4 × 65 FIR coefficients
- **Asynchronous operation**: Coefficients updated every 500ms (2 inferences/sec) on an external co-processor/NPU, while filtering runs on low-latency hardware
- **Training**: MSE loss in time domain on primary disturbance prediction, Adam optimizer, 1000 epochs, 16h on RTX 3080

### Training Dataset

- 50,000 synthetic scenes in pyroomacoustics
- 4 remote microphones in tetrahedral arrangement (28.3 cm aperture)
- Virtual microphone within ±5 cm of center
- Single primary source at 1 m distance, colored broadband noise (1/f^β, β ∈ [0,2])
- 16 kHz sample rate, 10s per scene, 80/20 train/validation split
- FIR filter length: 65 taps, overlap-save with 128-sample segments, 64-sample step

## Key Results

| Condition | Mean NMSE | SD |
|-----------|-----------|-----|
| With position data (train+val) | −33.53 dB | 9.90 dB |
| Position at validation only | −17.67 dB | 14.35 dB |
| No position data | −13.42 dB | 12.24 dB |

- Virtual microphone distance from center: −35.02 dB at <1 cm → −32.06 dB at 4-5 cm (~0.5-1 dB degradation/cm)
- Primary source direction: no statistically significant difference (p = 0.762)
- Best low-frequency performance, with spectral tilt matching training noise distribution

## Key Contributions

1. First CNN-based online estimation of RMT observation filter with variable virtual microphone position
2. GCC-PHAT input features enable asynchronous computation on external (co-)processors
3. Eliminates the need for pre-computed filter databases and selection logic
4. Position coordinate conditioning significantly improves estimation accuracy (20 dB NMSE gain)
5. Lightweight architecture (366.94k params) suitable for embedded deployment

## Related Concepts

- [[concepts/remote-microphone-technique|Remote Microphone Technique]]
- [[concepts/virtual-sensing|Virtual Sensing]]
- [[concepts/neural-observation-filter|Neural Observation Filter]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/neural-networks|Neural Networks]]

## Related Entities

- [[entities/felix-holzmueller|Felix Holzmüller]]
- [[entities/alois-sontacchi|Alois Sontacchi]]

## Related Sources

- [[sources/holzmueller-2026-obs-tasnet-virtual-sensing|Holzmüller 2026: Obs-TasNet for Virtual Sensing]] — Follow-up work using Conv-TasNet architecture
- [[sources/holzmuller-2026-dtw-secondary-path-anc|Holzmüller & Sontacchi 2026: DTW for Secondary Path Interpolation in ANC]]
- [[sources/a-review-of-virtual-sensing-algorithms-for-active-|Moreau 2008: Review of Virtual Sensing Algorithms for ANC]]
