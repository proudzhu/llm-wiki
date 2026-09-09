---
type: concept
created: 2026-04-30
updated: 2026-09-09
sources:
  - raw/papers/wang-2026-predictive-dsfanc-crnn/full-text.md
  - raw/papers/wang-2026-directional-sfanc-reverberant/full-text.md
  - raw/papers/zhang-2014-causality-feedforward-anc-headset/full-text.md
  - raw/papers/kim-2014-doa-based-snr-estimation/full-text.txt
  - raw/papers/grumiaux-2022-ssl-deep-learning-survey/full-text.txt
  - raw/papers/tervo-2009-sound-intensity-direction/full-text.md
tags:
  - signal-processing
  - array-processing
  - sound-source-localization
  - active-noise-control
---

# Direction-of-Arrival Estimation

**Direction-of-Arrival (DoA) Estimation** is the process of determining the direction from which a propagating signal arrives at a sensor array. In ANC, DoA information enables spatially-aware filter selection.

## Overview

DoA estimation exploits the spatial diversity of microphone arrays to determine the azimuth and/or elevation of sound sources. Common approaches include:

- **Classical methods**: Beamforming-based scanning (delay-and-sum), MVDR spatial spectrum, MUSIC, ESPRIT, and [[concepts/intensity-vector-doa-estimation|intensity-vector methods]] that read direction off the physical energy flow measured by a compact [[concepts/sound-intensity-vector|sound intensity]] probe
- **Data-driven methods**: Neural networks (CNN, CRNN) trained to classify or regress DoA from multichannel spectrograms

## DoA for ANC

In the context of ANC, DoA estimation serves as the spatial information input for Directional SFANC (D-SFANC) methods. The motivation for direction-aware ANC comes from Zhang & Qiu (2014), who demonstrated that a typical feedforward ANC headset is causal at 0° (frontal) but non-causal at 90° (lateral), causing significant performance degradation that depends on the noise arrival direction.

- **D-SFANC**: Uses current-frame DoA to select the appropriate pre-trained control filter
- **PD-SFANC** (Wang et al. 2026): Uses a CRNN to **predict** the next-frame DoA from multi-frame context, enabling proactive filter selection

### CNN-Based DoA in Reverberant Environments (Wang et al. 2026)

A lightweight CNN trained via multi-task learning simultaneously estimates azimuth and elevation from a single frame of $J$-channel STFT spectrograms. The CNN uses magnitude + phase features, three convolutional modules with group normalization, and two separate FC heads for azimuth and elevation classification.

$$(\hat{\mathbf{p}}_{\text{azim}}, \hat{\mathbf{p}}_{\text{elev}}) = CNN(\mathbf{R}; \Theta^*)$$

Achieves ~96% azimuth and ~91% elevation accuracy on unseen noise types and rooms with only 0.03M parameters and 7.83 ms CPU runtime. Demonstrates robustness to reverberation (RT60 up to 0.9 s) and varying SNR.

### CRNN-Based DoA Prediction (Wang et al. 2026)

Input: $K$ consecutive frames of $J$-channel STFT (magnitude + phase) → $\mathbf{R} \in \mathbb{R}^{2J \times F \times TK}$

$$\mathbf{z} = \text{Avg}[\text{CNN}(\mathbf{R})] \in \mathbb{R}^{T' \times 64}$$
$$\mathbf{h}_t = \text{GRU}(\mathbf{z}_t, \mathbf{h}_{t-1}) \in \mathbb{R}^{64}$$
$$\hat{\mathbf{p}} = \text{Softmax}[\text{FC}(\mathbf{h}_{T'})] \in \mathbb{R}^{V}$$

The CRNN achieves >90% DoA classification accuracy at SNR ≥ 20 dB with only 0.05M parameters.

## DOA as a Cue for SNR Estimation (Kim & Kim 2014)

Beyond localization and filter selection, DOA information can serve directly as an **SNR cue** for speech enhancement. Kim & Kim (2014) assume the target DOA (TDOA) is known a priori for a dual-microphone array, time-align the channels accordingly, and convert the residual phase difference into a [[concepts/target-to-non-target-directional-signal-ratio|TNR]] and then a [[concepts/doa-based-snr-estimation|DOA-based SNR]] for a Wiener-filter speech enhancer. Their DOA-error analysis shows the enhancement performance is best near zero target-DOA error and degrades outside a small window — but since GCC/SRP-PHAT localization is reliable within that window, the cue is practical. A super-directive beamformer's broadside dual-microphone directivity is by contrast nearly DOA-error-invariant. The approach fails when target and interference share a DOA, the fundamental ambiguity of DOA cues.

## Key Considerations

- **Discretization**: DoA is typically discretized into a grid (e.g., 36 angles at 10° resolution) for classification-based estimation
- **Temporal context**: Multi-frame input captures source trajectory dynamics, essential for prediction
- **Far-field assumption**: Small array apertures allow far-field modeling (plane wave assumption)
- **Robustness**: Must generalize to unseen noise types, rooms, and reverberation conditions

## DoA Estimation in the DL-based SSL Landscape (Grumiaux et al. 2022)

The Grumiaux et al. 2022 survey treats "DoA estimation" and sound source localization as interchangeable (azimuth/elevation without distance) and organizes 156 DL-based systems by output strategy:

- **Classification**: space discretized into zones; softmax (single-source) or sigmoid (multi-source) output forms a *spatial pseudo-spectrum* whose peaks are DoA estimates; grids range from coarse azimuth classes to quasi-uniform 429/432-class spherical grids.
- **Regression**: continuous Cartesian/spherical coordinates, increasingly via the [[concepts/activity-coupled-cartesian-doa|ACCDOA]] representation that couples event activity with Cartesian DoA.
- **Non-direct**: the DNN outputs TF masks, denoised features, or likelihood surfaces consumed by a conventional estimator.

The survey reports representative gains of DL over conventional DoA methods: a CNN doubled DoA classification accuracy vs SRP-PHAT at low SNR (Chakrabarty & Habets 2017a), and a CRNN halved the average angular error of MUSIC in reverberant conditions (Adavanne et al. 2018).

## Intensity-Vector DoA (Tervo 2009)

Before the DL era, [[sources/tervo-2009-sound-intensity-direction|Tervo (EUSIPCO 2009)]] provided one of the few systematic comparisons of conventional [[concepts/intensity-vector-doa-estimation|intensity-vector DoA estimators]] on real concert-hall data (RT ≈ 2.1 s, SNR 0–40 dB). Fitting two-component wrapped mixture distributions (von Mises / wrapped Gaussian) to the per-frame azimuth histogram of [[concepts/sound-intensity-vector|sound intensity vectors]] outperformed simple circular averaging, and von Mises mixtures were the most noise-robust of the five methods tested; energy-weighted averaging (MCA) was clearly worst, showing that radial-magnitude weighting lets reverberation- and noise-dominated bins dominate the estimate. All methods stayed under 4° circular bias, but anomaly rates remained high at low SNR — quantifying the "degrade quickly under reflections" behavior that the Grumiaux survey attributes to classical intensity methods.

## Related Concepts

- [[concepts/selective-fixed-filter-anc|Selective Fixed-Filter ANC]] — DoA drives filter selection in D-SFANC/PD-SFANC
- [[concepts/moving-source-tracking|Moving Source Tracking]] — temporal DoA evolution for moving sources
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — neural architecture for data-driven DoA estimation
- [[concepts/active-noise-control|Active Noise Control]] — application domain
- [[concepts/doa-based-snr-estimation|DOA-Based SNR Estimation]] — DOA as a cue for SNR rather than filter selection
- [[concepts/sound-intensity-vector|Sound Intensity Vector]] — the physical energy-flow quantity measured by p–p probes and B-format arrays
- [[concepts/intensity-vector-doa-estimation|Intensity-Vector DOA Estimation]] — averaging vs. mixture-model estimators on intensity-vector azimuths

## Related Sources

- [[sources/wang-2026-predictive-dsfanc-crnn|Wang 2026: Predictive Directional SFANC via CRNN]] — CRNN-based next-frame DoA prediction for ANC
- [[sources/wang-2026-directional-sfanc-reverberant|Wang 2026: Directional SFANC in Reverberant Environments]] — CNN-based multi-task DoA estimation for reverberant conditions
- [[sources/zhang-2014-causality-feedforward-anc-headset|Zhang 2014: Causality Study on Feedforward ANC Headset]] — foundational work showing direction-dependent causality in feedforward ANC
- [[sources/goetz-2026-blind-direction-dependent-acoustic-parameter-estimation|Görtz et al. 2026: Blind DDAP Estimation Using Smart Glasses]] — head rotation exploited for direction-dependent parameter estimation
- [[sources/tervo-2009-sound-intensity-direction|Tervo 2009: Direction Estimation Based on Sound Intensity Vectors]] — conventional intensity-vector DoA estimators compared on real concert-hall data
