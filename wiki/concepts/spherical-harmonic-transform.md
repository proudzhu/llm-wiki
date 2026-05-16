---
type: concept
created: 2026-05-05
updated: 2026-05-05
sources:
  - raw/papers/goetz-2026-blind-direction-dependent-acoustic-parameter-estimation/full-text.md
tags:
  - mathematics
  - acoustics
  - spatial-audio
  - spherical-harmonics
---

# Spherical Harmonic Transform

The **Spherical Harmonic Transform (SHT)** decomposes functions defined on the sphere into spherical harmonic coefficients, providing a frequency-domain representation for spatial signals.

## Overview

Spherical harmonics form a complete orthonormal basis for functions on the sphere $\mathbb{S}^2$. The SHT is the spherical analogue of the Fourier transform, enabling compact representation and efficient manipulation of spatial acoustic data.

## Real-Valued Spherical Harmonics

Real-valued spherical harmonics of order $l$ and degree $m$:

$$Y_{lm}(\vartheta, \phi) = N_{l|m|} P_{l|m|}(\cos\vartheta) \begin{cases} \sqrt{2}\sin(|m|\phi), & m < 0 \\ 1, & m = 0 \\ \sqrt{2}\cos(m\phi), & m > 0 \end{cases}$$

where $P_{lm}$ is the associated Legendre polynomial and $N_{lm} = (-1)^{|m|}\sqrt{(2l+1)(l-m)!/4\pi(l+m)!}$ is the normalization factor.

## Forward Transform

The SHT of a function $f(\vartheta, \phi)$:

$$\mathrm{SHT}_L(f(\vartheta, \phi)) = \int_0^{2\pi}\int_0^{\pi} f(\vartheta, \phi) Y_{lm}^*(\vartheta, \phi) \sin\vartheta\, d\vartheta\, d\phi$$

for $0 \leq l \leq L$, $-l \leq m \leq l$, where $L$ is the maximum SH order and $(\cdot)^*$ denotes complex conjugate.

## Inverse Transform

Reconstruction from spherical harmonic coefficients $f_{lm}$:

$$\mathrm{iSHT}_L(f_{lm}) = \sum_{l=0}^{L}\sum_{m=-l}^{l} f_{lm} Y_{lm}(\vartheta, \phi)$$

## Applications in Acoustics

- **[[direction-dependent-acoustic-parameters|DDAP estimation]]**: Acoustic parameters represented as SH coefficients for compact, continuous spatial description
- **Beamforming**: SH-domain beamformers (e.g., max-rE) apply modal weights $w_l$ to SH coefficients
- **Room impulse response modeling**: Spatial RIRs represented as $\mathbf{h}_{lm}[n] \in \mathbb{R}^{(L+1)^2}$
- **Spatial audio rendering**: SH representation enables evaluation at arbitrary directions

## Key Properties

| Property | Description |
|----------|-------------|
| Orthonormality | $\int Y_{lm} Y_{l'm'}^* d\Omega = \delta_{ll'}\delta_{mm'}$ |
| Number of coefficients | $(L+1)^2$ for maximum order $L$ |
| Spatial resolution | Increases with $L$; $L=1$ captures dipole patterns, $L=4$ captures fine spatial detail |
| Rotation equivariance | SH coefficients rotate cleanly under SO(3) transformations |

## Related Concepts

- [[direction-dependent-acoustic-parameters|Direction-Dependent Acoustic Parameters]] — estimated in SH domain
- [[beamforming|Beamforming]] — SH-domain beamformers
- [[direction-of-arrival-estimation|Direction-of-Arrival Estimation]] — spatial estimation on the sphere

## Related Sources

- [[sources/goetz-2026-blind-direction-dependent-acoustic-parameter-estimation|Görtz et al. 2026: Blind DDAP Estimation Using Smart Glasses]]
