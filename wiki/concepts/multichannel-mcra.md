---
type: concept
created: 2026-08-16
updated: 2026-08-16
sources:
  - raw/papers/taseska-2018-informed-spatial-filters/full-text.md
tags:
  - noise-estimation
  - speech-enhancement
  - statistical-model
  - spp
  - recursive-averaging
  - mcra
---

# Multichannel MCRA

**Multichannel MCRA** (Minima-Controlled Recursive Averaging) extends single-channel MCRA to estimate the noise Power Spectral Density (PSD) *matrix* $\boldsymbol{\Phi}_{\mathbf{v}}(t,k)$ from multi-microphone signals using a Speech Presence Probability (SPP)-controlled recursive averager. The noise PSD matrix is updated only at TF bins where speech is likely absent, with the averaging controlled by the a posteriori SPP. Taseska & Habets (IEEE/ACM TASLP 2017) showed that an **ML formulation** of the multichannel noise-PSD/SPP estimation problem yields the same structure as multichannel MCRA, with a specific a priori Speech Absence Probability (SAP) and a specific recursive averaging parameter.

## ML Formulation

The ML solution for the noise PSD matrix and SPP results in a recursive update structurally identical to MCRA:

$$
\hat{\boldsymbol{\Phi}}_{\mathbf{v}}(t,k) = \alpha_v(t,k)\,\hat{\boldsymbol{\Phi}}_{\mathbf{v}}(t-1,k) + (1-\alpha_v(t,k))\,\mathbf{y}(t,k)\mathbf{y}^{\mathrm{H}}(t,k),
$$

where the averaging parameter $\alpha_v$ and the a priori SAP are *given by the ML solution*. However, the pure-ML solution is **not adequate in non-stationary environments**: without additional control, changes in the noise properties are falsely detected as speech onsets, corrupting the noise PSD matrix estimate.

## CDR-Based a Priori SAP

The key contribution: a **CDR-based a priori SAP** estimator that exploits the spatial coherence difference between desired speech (coherent across the array) and background noise (approximately diffuse). The [[concepts/coherent-to-diffuse-power-ratio|Coherent-to-Diffuse Ratio (CDR)]] is mapped to an a priori SAP via a sigmoid-like function, providing robust control that distinguishes noise-property changes from speech onsets. This is more robust than single-channel and multichannel SNR-based a priori SAPs (SC-Cohen, MC-Souden).

## Relation to ISFs

The estimated $\boldsymbol{\Phi}_{\mathbf{v}}$ and SPP drive [[concepts/informed-spatial-filter|informed MVDR and MWF filters]] for blind speech extraction. The SPP also serves as the PMWF trade-off parameter, balancing noise reduction against speech distortion.

## Related Concepts

- [[concepts/informed-spatial-filter|Informed Spatial Filter (ISF)]]
- [[concepts/coherent-to-diffuse-power-ratio|Coherent-to-Diffuse Power Ratio (CDR)]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/multi-channel-wiener-filter|Multichannel Wiener Filter]]
- [[concepts/voice-activity-detection|Voice Activity Detection]]
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/taseska-2018-informed-spatial-filters|Taseska 2018: Informed Spatial Filters for Speech Enhancement]] (Chapter 3)
