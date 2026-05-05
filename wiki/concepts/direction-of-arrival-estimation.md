---
type: concept
created: 2026-04-30
updated: 2026-05-05
sources:
  - raw/papers/wang-2026-predictive-dsfanc-crnn/full-text.md
  - raw/papers/wang-2026-directional-sfanc-reverberant/full-text.md
  - raw/papers/zhang-2014-causality-feedforward-anc-headset/full-text.md
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

- **Classical methods**: Beamforming-based scanning (delay-and-sum), MVDR spatial spectrum, MUSIC, ESPRIT
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

## Key Considerations

- **Discretization**: DoA is typically discretized into a grid (e.g., 36 angles at 10° resolution) for classification-based estimation
- **Temporal context**: Multi-frame input captures source trajectory dynamics, essential for prediction
- **Far-field assumption**: Small array apertures allow far-field modeling (plane wave assumption)
- **Robustness**: Must generalize to unseen noise types, rooms, and reverberation conditions

## Related Concepts

- [[../concepts/selective-fixed-filter-anc|Selective Fixed-Filter ANC]] — DoA drives filter selection in D-SFANC/PD-SFANC
- [[../concepts/moving-source-tracking|Moving Source Tracking]] — temporal DoA evolution for moving sources
- [[../concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — neural architecture for data-driven DoA estimation
- [[../concepts/active-noise-control|Active Noise Control]] — application domain

## Related Sources

- [[../sources/wang-2026-predictive-dsfanc-crnn|Wang 2026: Predictive Directional SFANC via CRNN]] — CRNN-based next-frame DoA prediction for ANC
- [[../sources/wang-2026-directional-sfanc-reverberant|Wang 2026: Directional SFANC in Reverberant Environments]] — CNN-based multi-task DoA estimation for reverberant conditions
- [[../sources/zhang-2014-causality-feedforward-anc-headset|Zhang 2014: Causality Study on Feedforward ANC Headset]] — foundational work showing direction-dependent causality in feedforward ANC
