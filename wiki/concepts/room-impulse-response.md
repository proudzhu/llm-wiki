---
type: concept
created: 2026-05-13
updated: 2026-05-13
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

## Related Concepts

- [[../concepts/room-transfer-function|Room Transfer Function]]
- [[../concepts/image-source-method|Image Source Method]]
- [[../concepts/diffuse-sound-extraction|Diffuse Sound Extraction]]

## Related Sources

- [[../sources/huang-2026-ndf-joint-neural-directional-filtering|Huang et al. 2026: NDF+]]
