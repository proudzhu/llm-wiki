---
type: concept
created: 2026-05-13
updated: 2026-09-09
sources:
  - raw/papers/grumiaux-2022-ssl-deep-learning-survey/full-text.txt
tags:
  - room-acoustics
  - spatial-audio
  - acoustic-simulation
---

# Room Impulse Response

A room impulse response (RIR) characterizes the acoustic response of an enclosed space to an impulsive sound source. It captures all propagation paths including direct sound, early reflections, and late reverberation.

## Components

- **Direct path**: First arrival, line-of-sight propagation
- **Early reflections**: Discrete reflections from walls, floor, ceiling (typically first 50-80 ms)
- **Late reverberation**: Dense, exponentially decaying reverberant tail

## Key Parameters

| Parameter | Description |
|-----------|-------------|
| RT60 | Time for sound energy to decay by 60 dB |
| DRR | Direct-to-reverberant ratio |
| EDT | Early decay time |

## Simulation Methods

- **Image source method**: Geometric approach for early reflections
- **Monte Carlo RIR**: Statistical simulation with random room configurations
- **Wave-based methods**: Numerical solution of wave equation (accurate but computationally expensive)

## RIRs as Training Data for DL-based SSL (Grumiaux et al. 2022)

The relative source-to-array position is implicitly encoded in the multichannel RIR, which is why simulated RIRs are the dominant source of training data for deep-learning [[concepts/sound-source-localization|sound source localization]]: dry source signals are convolved with simulated RIRs spanning many source/microphone positions, room dimensions, and reverberation times. The survey notes that training on speech signals (or speech+noise+event mixtures) yields better localization than noise-based training, even when the noise is GAN-simulated (Vargas et al. 2021). A key limitation: "shoebox" simulations with unrealistically placed arrays (e.g., floating in mid-air) contribute to the well-known performance drop when testing DNNs on real-world signals.

## Related Concepts

- [[concepts/room-transfer-function|Room Transfer Function]]
- [[concepts/image-source-method|Image Source Method]]
- [[concepts/diffuse-sound-extraction|Diffuse Sound Extraction]]

## Related Sources

- [[sources/huang-2026-ndf-joint-neural-directional-filtering|Huang et al. 2026: NDF+]]
