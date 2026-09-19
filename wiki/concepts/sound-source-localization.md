---
type: concept
created: 2026-09-09
updated: 2026-09-19
sources:
  - raw/papers/grumiaux-2022-ssl-deep-learning-survey/full-text.txt
  - raw/papers/tervo-2009-sound-intensity-direction/full-text.md
  - raw/papers/pan-2025-data-driven-acoustics/full-text.md
tags:
  - sound-source-localization
  - doa-estimation
  - audio-processing
  - microphone-array
---

# Sound Source Localization (SSL)

Sound source localization is the problem of estimating the position of one or several sound sources relative to a reference position, generally the recording microphone array, based on recorded multichannel acoustic signals. In most practical cases SSL is simplified to estimating the sources' [[concepts/direction-of-arrival-estimation|direction of arrival]] (azimuth and elevation), without estimating the distance to the array — the Grumiaux et al. 2022 survey uses "SSL" and "DoA estimation" interchangeably.

## Problem Basis

Each microphone signal is the source signal convolved with a position-dependent [[concepts/room-impulse-response|room impulse response]] plus noise. The inter-channel differences (delay, amplitude) caused by distinct propagation paths encode the relative source-to-array position; in the STFT domain the acoustic transfer functions carry this spatial information. DNNs are attractive because they can learn to exploit this complex relationship without explicit signal/channel modeling assumptions — at the cost of reduced generality across setups (a model trained for one array geometry degrades on another).

## Conventional vs. DL-based Methods

- **Conventional**: TDoA/GCC-PHAT, SRP-PHAT power maps, sound intensity ([[concepts/sound-intensity-vector|intensity vectors]] — quantitatively compared for a real concert hall by [[sources/tervo-2009-sound-intensity-direction|Tervo 2009]]: mixture-model fitting of the azimuth histogram beats simple circular averaging, but all variants degrade under strong reverberation), subspace methods (MUSIC, ESPRIT), GMM/GMR generative models, Bayesian inference, compressive sensing, ICA. Perform poorly in noisy, reverberant, multi-source conditions; DNN systems have shown large gains (e.g., 2x accuracy over SRP-PHAT at low SNR; 50% angular-error reduction vs. MUSIC).
- **DL-based**: a feature extraction module (or raw waveforms) feeding a DNN (FFNN → CNN → RNN → CRNN → residual → attention → encoder-decoder, in historical order) that outputs a DoA estimate — via classification (spatial pseudo-spectrum) or regression (coordinates, ACCDOA).

## Key Configurations

- **Single-source vs. multi-source**: multi-source SSL with time-overlapping sources is much harder; requires source counting (NoS known or estimated) and TF-domain sparsity to separate contributions.
- **Static vs. moving sources**: most works assume static sources; tracking is an open research direction.
- **Source activity**: real systems must detect source presence (e.g., via [[concepts/voice-activity-detection|VAD]]) rather than assume it.

## Detection-Based Formulation (Pan 2025)

[[sources/pan-2025-data-driven-acoustics|Pan 2025]] formulates source localization as a **signal detection problem over directions**: the label indicates whether a source is active in a given direction. The signal model isolates the direct path, $p_m(t) = h_0 s(t - \tau_m) + \text{reflections}$, so the source angle is encoded in inter-channel time differences $\tau_m - \tau_1 = \delta_{m,1}\cos\theta/c$, which become phase shifts $e^{-\jmath\omega(\tau_m - \tau_1)}$ in the STFT domain. Surveyed loss constructions: softmax + cross-entropy over an angle grid (classification); multi-head sigmoid + BCE (multi-direction presence); MSE regression to a unit Cartesian vector; and the joint detection+localization cost [[concepts/activity-coupled-cartesian-doa|ACCDOA]] ($3 \times L$ label matrix). Typical networks: CNN+FC on spatial spectra; multi-objective networks (source count via softmax + angle via multi-sigmoid, sharing a 10-layer convolutional feature extractor); and a U-Net mapping $T \times K \times 2M$ multichannel spectrograms to per-time-frequency-angle probabilities, whose angle-summed output doubles as a TF mask for direction-based extraction — connecting localization back to [[concepts/tf-mask-estimation|TF mask estimation]].

## Related Concepts

- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/relative-transfer-function|Relative Transfer Function (RTF)]]
- [[concepts/ambisonics|Ambisonics]]
- [[concepts/sel-d|SELD]]
- [[concepts/activity-coupled-cartesian-doa|ACCDOA]]
- [[concepts/room-impulse-response|Room Impulse Response]]

## Related Sources

- [[sources/grumiaux-2022-ssl-deep-learning-survey|Grumiaux et al. 2022: A Survey of SSL with Deep Learning Methods]]
- [[sources/tervo-2009-sound-intensity-direction|Tervo 2009: Direction Estimation Based on Sound Intensity Vectors]] — empirical comparison of five conventional intensity-vector DoA estimators on concert-hall data
- [[sources/pan-2025-data-driven-acoustics|Pan 2025: Fundamentals of Data-Driven Approaches to Acoustic Signal Detection, Filtering, and Transformation]] — detection-based formulation of localization with loss-construction options and typical networks (Section 4)
