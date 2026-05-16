---
type: concept
created: 2026-05-05
updated: 2026-05-05
sources:
  - raw/papers/goetz-2026-blind-direction-dependent-acoustic-parameter-estimation/full-text.md
tags:
  - acoustics
  - room-acoustics
  - spatial-audio
  - parameter-estimation
---

# Direction-Dependent Acoustic Parameters

**Direction-Dependent Acoustic Parameters (DDAPs)** are acoustic quantities that vary with the direction of observation in a reverberant sound field, capturing the anisotropic nature of real-room acoustics.

## Overview

In rooms with non-uniform absorption (e.g., domestic environments with windows, carpets, and furniture), acoustic parameters such as reverberation time and energy decay vary with direction. Traditional blind estimation methods treat these parameters as omnidirectional (single-valued), neglecting this directional dependency. DDAPs provide the spatial resolution necessary for realistic rendering of virtual sound sources in [[auditory-augmented-reality|auditory augmented reality]].

## Key DDAPs

### Direction-Dependent Decay Time T₂₀(θ)

The decay time measured from the directional energy decay curve (EDC) obtained by beamforming towards direction θ:

$$\mathrm{EDC}_{\boldsymbol{\theta}}[n] = 10\log_{10}\left(\frac{\sum_{n'=n}^{N-1} h_{\boldsymbol{\theta}}^2[n']}{\sum_{n'=0}^{N-1} h_{\boldsymbol{\theta}}^2[n']}\right)$$

$\mathrm{T}_{20}(\boldsymbol{\theta})$ is defined as the time interval where $-25 \leq \mathrm{EDC}_{\boldsymbol{\theta}} \leq -5$, extrapolated to 60 dB decay: $\mathrm{T}_{20} = 3 \times (\mathrm{T}_{25} - \mathrm{T}_5)$.

$\mathrm{T}_{20}$ exhibits stronger directional dependence than $\mathrm{T}_{60}$ because the late reverberant tail becomes more diffuse and isotropic over time.

### Directional Acoustic Energy E(θ)

The energy of the directional RIR:

$$E(\boldsymbol{\theta}) = 10\log_{10}\left(\frac{1}{N}\sum_{n=0}^{N-1} h_{\boldsymbol{\theta}}^2[n]\right)$$

## Spherical Harmonic Representation

DDAPs can be represented compactly in the [[spherical-harmonic-transform|spherical harmonic]] domain:

$$\Gamma(\boldsymbol{\theta}) = \sum_{l=0}^{L} \sum_{m=-l}^{l} \Gamma_{lm} Y_{lm}(\boldsymbol{\theta})$$

where $\Gamma_{lm}$ are the spherical harmonic coefficients and $L$ controls the spatial resolution. This representation:
- Yields a continuous function evaluable at arbitrary angles
- Provides convenient control over spatial resolution via $L$
- Naturally includes the omnidirectional (zero-order) parameter as $\Gamma_{00}$

## Estimation Challenges

- **Compact arrays**: Limited spatial resolution and directional ambiguities from few microphones in irregular layouts
- **Blind estimation**: Must work from reverberant speech without controlled measurements
- **Head rotation**: Natural head movements can be exploited to aggregate spatial information across multiple orientations (Görtz et al. 2026)

## Related Concepts

- [[spherical-harmonic-transform|Spherical Harmonic Transform]] — mathematical framework for DDAP representation
- [[auditory-augmented-reality|Auditory Augmented Reality]] — primary application domain
- [[beamforming|Beamforming]] — max-rE beamformer used for directional RIR extraction
- [[direction-of-arrival-estimation|Direction-of-Arrival Estimation]] — related spatial estimation task
- [[spatial-coherence|Spatial Coherence]] — multi-channel signal correlation in sound fields

## Related Sources

- [[sources/goetz-2026-blind-direction-dependent-acoustic-parameter-estimation|Görtz et al. 2026: Blind DDAP Estimation Using Smart Glasses]]
