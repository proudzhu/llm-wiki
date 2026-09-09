---
type: concept
created: 2026-04-25
updated: 2026-09-09
sources:
  - raw/papers/grumiaux-2022-ssl-deep-learning-survey/full-text.txt
tags:
  - acoustics
  - room-simulation
  - signal-processing
---

# Image Source Method

The **Image Source Method (ISM)** is a classical algorithm for simulating room acoustics by computing Room Impulse Responses (RIRs) in rectangular enclosures. Originally proposed by Allen and Berkley (1979), it remains the standard approach for generating high-fidelity acoustic simulations used in [[active-noise-control|ANC]] research and other audio applications.

## Core Principle

ISM models wall reflections by placing virtual "image sources" — mirror images of the original sound source with respect to each wall surface. Each image source represents a specific reflection path, and the combined contributions of all image sources (up to a chosen reflection order) produce the room impulse response.

For a rectangular room, the method is exact for first-order reflections and can be extended to arbitrary order by considering images of images.

## Modern Implementation: pyroomacoustics

Scheibler et al. (2018) developed **pyroomacoustics**, a Python library that efficiently implements ISM with configurable parameters:

- Room dimensions and geometry
- Wall absorption coefficients (frequency-dependent)
- Microphone and source positions
- Maximum reflection order
- Reverberation time ($RT_{60}$) targeting

## Key Parameters for ANC Simulation

From Dai 2026's configuration:

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Room size | 4m × 3m × 2.5m | Small office / vehicle interior |
| $RT_{60}$ | 0.3s | Moderate acoustic treatment (carpeted room) |
| Sampling rate | 16 kHz | Matches speech/NOISEX-92 datasets |
| RIR length | 512 points | Truncated for filter design |
| Secondary source distance | 5 cm from error mic | Near-field (ANC headrest scenario) |

## ISM as the Standard Training-Data Generator for DL-based SSL (Grumiaux et al. 2022)

The Grumiaux et al. 2022 survey identifies ISM-based simulators as the workhorses for generating the synthetic RIRs used to train deep-learning [[concepts/sound-source-localization|sound source localization]] systems — they offer the best trade-off between simulation fidelity (especially for the RIR "head": direct path + early reflections) and computational complexity. Widely used implementations include Habets' RIR generator, Roomsim/Roomsimove, the SMIR generator (spherical arrays), pyroomacoustics, and GPU-accelerated ISM (Diaz-Guerra et al. 2021) for moving sources. Extensions that improve SSL training data: ISM with a diffuse-reverberation model (Lehmann & Johansson), directional sources and scattering (Gelderblom et al. 2021 — best SSL performance in their comparison), and a low-complexity direct-path/late-reverb statistical hybrid (Hübner et al. 2021) matching ISM-trained accuracy at lower cost. Geometric-acoustics simulators still cannot capture wave phenomena such as diffraction.

- **Beyond ideal models**: Simple low-pass filter simulations of acoustic paths fail to capture the multi-path propagation, frequency-selective attenuation, and phase delay that characterize real rooms
- **Reverberation effects**: Reverberation reduces maximum noise reduction and creates frequency-dependent convergence speed differences (Lu & Clarkson 1993)
- **Robustness validation**: Testing ANC algorithms under realistic reverberant conditions is essential for practical deployment

## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[speech-preserving-anc|Speech-Preserving ANC]]

## Related Sources

- [[sources/dai-2026-speech-preserving-deep-anc|Dai 2026: Speech-Preserving Deep ANC]]
