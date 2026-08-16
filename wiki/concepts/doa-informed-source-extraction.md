---
type: concept
created: 2026-08-16
updated: 2026-08-16
sources:
  - raw/papers/taseska-2018-informed-spatial-filters/full-text.md
tags:
  - spatial-filter
  - speech-enhancement
  - doa
  - signal-detection
  - interference-reduction
---

# DOA-Informed Source Extraction

**DOA-informed source extraction** is a semi-blind multi-microphone speech enhancement framework where the Direction-of-Arrival (DOA) of the desired source (w.r.t. the array) is approximately known, while the number and locations of interferers are unknown and possibly time-varying. A **narrowband DOA model-based detector** discriminates desired from undesired speech at each TF bin, and the detector output drives [[concepts/informed-spatial-filter|informed spatial filter]] estimation. It was developed by Taseska & Habets (EURASIP J. Adv. Signal Process. 2017) to handle scenarios where the CDR-based detector (which assumes diffuse noise) fails because interferers are *other speakers* with similar coherence to the desired source.

## Signal Model

$$
\mathbf{y}(t,k) = \mathbf{s}(t,k) + \mathbf{i}(t,k) + \mathbf{v}(t,k),
$$

with desired speech $\mathbf{s}$, interfering speech $\mathbf{i}$, and noise $\mathbf{v}$. The undesired-signal PSD matrix is $\boldsymbol{\Phi}_{\mathbf{u}} = \boldsymbol{\Phi}_{\mathbf{i}} + \boldsymbol{\Phi}_{\mathbf{v}}$. Three per-bin hypotheses:

$$
\mathcal{H}_s: \mathbf{y}\approx\mathbf{s}+\mathbf{v}, \quad \mathcal{H}_i: \mathbf{y}\approx\mathbf{i}+\mathbf{v}, \quad \mathcal{H}_v: \mathbf{y}\approx\mathbf{v}.
$$

## DOA Model-Based Detector

Narrowband DOA estimates $\hat{\theta}_{tk}$ are computed from inter-microphone phase differences. The likelihoods are:

- **Under $\mathcal{H}_s$** (desired dominant): a **von Mises distribution** centred at the known desired DOA $\theta_s$, with concentration $\kappa$ reflecting estimation uncertainty.
- **Under $\mathcal{H}_i$** (interferer dominant): a **notched distribution** that suppresses the region around $\theta_s$, modelling that an interferer is unlikely to share the desired DOA.
- **Under $\mathcal{H}_v$** (noise dominant): the Gaussian signal model from [[concepts/multichannel-mcra|multichannel MCRA]] detects noise-dominated bins, and the [[concepts/coherent-to-diffuse-power-ratio|CDR]] controls model parameters.

The spectral information (signal energy) and CDR are used to control the detector parameters, making it robust to non-stationary interferers.

## Filter Design

The desired RTF vector $\mathbf{g}$ and the undesired PSD matrix $\boldsymbol{\Phi}_{\mathbf{u}}$ are estimated using the detector output, then substituted into the informed MVDR filter. The framework can also be implemented as an [[concepts/informed-gsc|informed GSC]].

## Advantages over Alternatives

- **vs. DSB / fixed MVDR**: better interference reduction and adaptability to changing conditions.
- **vs. MPDR**: avoids severe speech distortion from anechoic-RTF mismatch, because the RTF is *estimated from data* rather than modelled anechoically.
- **vs. Robust Adaptive Beamformers**: maintains low signal distortion *without* sacrificing interference reduction, as the propagation vectors and PSD matrices are data-estimated.

## Related Concepts

- [[concepts/informed-spatial-filter|Informed Spatial Filter (ISF)]]
- [[concepts/informed-gsc|Informed GSC]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/mpdr-beamformer|MPDR Beamformer]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/coherent-to-diffuse-power-ratio|Coherent-to-Diffuse Power Ratio (CDR)]]
- [[concepts/relative-transfer-function|Relative Transfer Function (RTF)]]
- [[concepts/robust-minimum-variance-beamforming|Robust Minimum Variance Beamforming]]

## Related Sources

- [[sources/taseska-2018-informed-spatial-filters|Taseska 2018: Informed Spatial Filters for Speech Enhancement]] (Chapter 4)
