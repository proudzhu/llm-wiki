---
type: concept
created: 2026-05-13
updated: 2026-05-13
tags:
  - room-acoustics
  - spatial-audio
  - acoustic-transfer-function
---

# Room Transfer Function

A room transfer function (RTF) describes the acoustic propagation characteristics between a sound source and a receiver (microphone) in an enclosed space. It captures direct sound, early reflections, and late reverberation.

## Mathematical Definition

Under the multiplicative transfer function approximation, the received signal at microphone $q$ from source $n$ is:

$$X_{q,n}(f,t)=H_{q,n}(f)X_{n}(f,t)$$

where $H_{q,n}(f)$ is the RTF and $X_n(f,t)$ is the source signal.

## Components

The RTF can be decomposed into:
- **Direct path**: Line-of-sight propagation
- **Early reflections**: Discrete reflections from surfaces
- **Late reverberation**: Dense, diffuse reverberant tail

## Room Impulse Response

The room impulse response (RIR) is the time-domain counterpart of the RTF. The RTF is the Fourier transform of the RIR.

## Related Concepts

- [[concepts/room-impulse-response|Room Impulse Response]]
- [[concepts/virtual-directional-microphone|Virtual Directional Microphone]]
- [[concepts/diffuse-sound-extraction|Diffuse Sound Extraction]]

## Related Sources

- [[sources/huang-2026-ndf-joint-neural-directional-filtering|Huang et al. 2026: NDF+]]
