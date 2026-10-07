---
type: concept
created: 2026-10-07
updated: 2026-10-07
sources:
  - raw/papers/itzhak-2025-stft-roi-beamforming/full-text.md
tags:
  - beamforming
  - microphone-arrays
  - performance-measures
---

# Directivity Factor (DF)

## Definition

The **directivity factor** quantifies a beamformer's ability to attenuate a spatially **diffuse noise field**. It is defined as the array gain when the noise is spherically isotropic, i.e. the ratio of the (squared) response in the look direction to the noise power integrated over all directions:

$$
\mathcal{D}[\mathbf{h}] = \frac{|\mathbf{h}^H \mathbf{d}|^2}{\mathbf{h}^H \boldsymbol{\Gamma}_0 \mathbf{h}}
$$

where $\boldsymbol{\Gamma}_0(k) = \frac{1}{4\pi} \int_0^\pi \int_0^{2\pi} \mathbf{d}(k,\theta,\phi)\, \mathbf{d}^H(k,\theta,\phi) \sin\theta\, \mathrm{d}\phi\, \mathrm{d}\theta$ is the pseudo-correlation matrix of the diffuse noise field. Equivalently, the DF is $4\pi$ times the ratio of the power beampattern in the look direction to the beampattern averaged over the sphere. The maximum DF for an $M$-element array is $M$ (0 dB $\cdot 10\log_{10} M$).

Maximizing DF is the goal of [[concepts/superdirective-beamforming|superdirective beamforming]]; DF is the standard directivity metric for [[concepts/differential-microphone-array|differential microphone arrays]] and appears across fixed and adaptive array design as the counterpart of [[concepts/white-noise-gain|WNG]] in the fundamental **directivity-vs-robustness tradeoff** — pushing DF up (especially at low frequencies with compact arrays) drives WNG strongly negative.

## ROI-Generalized Directivity Factor

[[sources/itzhak-2025-stft-roi-beamforming|Itzhak & Cohen 2025]] generalize the DF to a **region-of-interest** (ROI) $\Omega$: rather than evaluating the response at a single look direction, the numerator averages the power beampattern over all directions in the ROI:

$$
\mathcal{D}_\Omega[\mathbf{h}] = \frac{\mathbf{h}^H \boldsymbol{\Gamma}_{\mathbf{d},\Omega}\, \mathbf{h}}{\mathbf{h}^H \boldsymbol{\Gamma}_0\, \mathbf{h}}
$$

where $\boldsymbol{\Gamma}_{\mathbf{d},\Omega}$ is the ROI average of the steering outer product. Subband and broadband variants are defined, and the classical DF is recovered when the ROI shrinks to a single DOA. This generalized DF is maximized by the paper's **LD-MDF** (least-distortion maximum-DF) beamformer, subject to an ROI-distortion constraint; the number of retained generalized eigenvectors $K$ trades DF against average distortion over the ROI (decreasing $K$ raises DF but attenuates signals near the ROI edges).

## Related Concepts

- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/superdirective-beamforming|Superdirective Beamforming]]
- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/roi-beamforming|Region-of-Interest Beamforming]]
- [[concepts/beamforming|Beamforming]]

## Related Sources

- [[sources/itzhak-2025-stft-roi-beamforming|Itzhak & Cohen 2025: STFT-Domain Least-Distortion Region-of-Interest Beamforming]] — ROI-generalized subband/broadband DF and the LD-MDF beamformer that maximizes it
