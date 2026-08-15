---
type: concept
created: 2026-04-12
updated: 2026-08-15
sources:
  - raw/papers/liu-2025-pcen-mask-vad-speech-enhancement/full-text.md
  - raw/papers/tashev-2008-sound-capture-spatial-filter/full-text.md
tags:
- audio-processing
- machine-learning
- signal-processing
---

# Voice Activity Detection

**Voice Activity Detection (VAD)** is a technique used in speech processing to detect the presence or absence of human speech in an audio signal.

## Overview

VAD is a critical component for many audio applications, including speech coding, echo cancellation, speech recognition, and modern headphone features like [[transparency-mode|Transparency Mode]]. A VAD system typically outputs a binary flag indicating whether speech is present in a given frame of audio.

## VAD in Modern Headphones

In the context of ANC headphones, VAD is often split into two categories (Masilamani 2024):
1. **OVAD (Own Voice Activity Detection)**: Detects when the person wearing the headphones is speaking. This often uses **[[bone-conduction|Bone Conduction]]** sensors (accelerometers) to pick up vibrations in the skull, ensuring that external noise is not mistaken for the user's voice.
2. **TVAD (Target Voice Activity Detection)**: Detects when a person in the environment (the "target" speaker) is speaking. This relies on external microphones and often employs spatial filtering (see [[beamforming|Beamforming]]).

## Methods and Features

### 1. Traditional Signal Processing
- **Energy Thresholding**: Comparing the signal energy to the background noise floor.
- **Zero-Crossing Rate**: Speech often has a different zero-crossing profile compared to white noise or periodic hum.
- **Spectral Slope/Flux**: Analyzing changes in the frequency domain.

A simple, classical instance is the **energy-based binary VAD with minimum-energy tracking** used by Tashev et al. (2008) for their small-device sound-capture system: a state machine with two thresholds ("noise" and "voice" states) gates whether the current frame updates the noise-only statistical models or the speech-direction statistical models of the post-filter. The VAD itself is not the contribution; it is a binary gate for the [[concepts/probability-based-spatial-filter|probability-based spatial filter]]'s model adaptation.

### 2. Machine Learning Approaches
- **GMMs and HMMs**: Traditional statistical models for speech.
- **Deep Neural Networks (DNN/CNN/RNN)**: Modern VAD systems use small, efficient neural networks that can be run on low-power DSPs. These are trained to distinguish speech from complex background noises like traffic, wind, or music.

### 3. Mis-trigger Rejection
Sophisticated VAD systems use multi-modal data to avoid false positives from:
- **Coughing, Chewing, Humming**: Often identified via spectral analysis or correlation with bone conduction data.
- **Wind Noise**: Identified by its high energy at very low frequencies and lack of harmonic structure.

## Applications

- **Battery Saving**: Disabling high-power speech processing or transmission when no speech is detected.
- **[[transparency-mode|Transparency Mode]]**: Automatically enabling ambient sound pass-through when the user starts a conversation.
- **Acoustic Echo Cancellation**: Knowing when the local user is speaking helps the AEC algorithm distinguish between local speech and echoed remote speech.

## Training-Time VAD for Loss Gating

Most VAD usage described above is an **inference-time** component — it runs at runtime to gate processing or steer a beamformer. A distinct role for VAD, introduced by [[sources/liu-2025-pcen-mask-vad-speech-enhancement|Liu et al. 2025 (Dolby patent)]], is as a **training-time** mechanism that conditions the loss function rather than the inference pipeline.

In that patent, a mask-based DNN speech-enhancement model must learn two contradictory behaviors: preserve speech (favoring over-preservation of speech over noise removal) in speech frames, but aggressively suppress artifacts in non-speech frames. Rather than letting the DNN implicitly learn a VAD, an explicit VAD gates the loss:

- A simple **PCEN-VAD** computes, per frame, $E(t) = \sum_f PCEN(t,f)$ from the clean training target (see [[concepts/per-channel-energy-normalization|PCEN]]), and classifies the frame as speech if $E(t) > TH_\text{frame}$, where $TH_\text{frame} \approx TH_\text{band}\cdot N$.
- Speech frames use a signed error $IRM^\gamma - mask_\text{est}^\gamma$ in an asymmetric loss $a^\text{diff}-\text{diff}-1$ that penalizes over-suppression of speech more than under-suppression of noise.
- Non-speech frames have their [[concepts/ideal-ratio-mask|IRM]] set to 0 and a **sign-flipped** error $mask_\text{est}^\gamma$ so the prediction sits on the steeper-gradient side of the loss, driving the mask toward 0.

Key distinctions from inference-time VAD: (i) it operates only during training, adding no inference cost; (ii) its decisions zero the training target (IRM) and select the loss form, rather than steering a runtime beamformer or pass-through; (iii) it generalizes from frame-level binary decisions to sub-band **speech-presence-probability (SPP)** control within speech frames. Any VAD (e.g., WebRTC VAD) can be substituted, but the PCEN-VAD reuses the same PCEN computation already needed for the mask-thresholding step.

## VAD-Free Alternatives

While VAD is widely used, VAD-free noise estimation methods avoid the binary speech/pause decision and its associated tuning difficulties:

- **[[concepts/minimum-statistics|Minimum Statistics]]** (Martin 2001): Tracks spectral minima in each frequency band without distinguishing speech from silence. Derives optimal time-varying smoothing parameters and bias compensation. Performs well in low SNR and nonstationary noise, and updates noise estimates even during speech activity.

## Neural VAD as Audibility Estimator

Apostolidis et al. (2026) train a [[concepts/convolutional-recurrent-network|CRN]]-based neural VAD that does not output a binary speech/pause flag but instead estimates a per-time-frequency **audibility** map $\widehat{\mathrm{AUD}}(k,l) \in [0,1]$ adopted from the Speech Intelligibility Index (SII; ANSI S3.5-1997): the T-F SNR at the reference microphone is clipped to $[-15, 15]$ dB and linearly mapped to $[0, 1]$. The network is trained with MSE against ground-truth AUD computed from clean separated speech/noise. This continuous audibility output serves two roles in their [[concepts/output-based-speech-enhancement|output-based SE]] system: (i) forming ideal binary masks (with thresholds $\gamma_S, \gamma_V$) for the input-based [[concepts/mvdr-beamformer|MVDR]] baseline, and (ii) computing [[concepts/glimpse-proportion|Glimpse Proportion]] from each candidate [[concepts/mpdr-beamformer|MPDR]] output to drive selection. The fair comparison (same VAD in both systems) isolates the input-vs-output structural distinction rather than conflating it with VAD-architecture differences.

## Related Concepts

- [[concepts/minimum-statistics|Minimum Statistics]]
- [[transparency-mode|Transparency Mode]]
- [[beamforming|Beamforming]]
- [[bone-conduction|Bone Conduction]]
- [[active-noise-control|Active Noise Control]]

## Related Sources

- [[sources/masilamani-2024-headphone-conversation-detect-paper-reading-note|Masilamani 2024: Headphone Conversation Detect]]
- [[sources/fukumoto-2025-whisphone-paper-reading-note|Fukumoto 2025: Whisphone Paper Reading Note]]
- [[sources/heitkaemper-2026-bcs-speech-enhancement-earbuds|Heitkaemper et al. 2026: BCS-Guided Speech Enhancement for Earbuds]]
- [[sources/martin-2001-noise-psd-estimation-optimal-smoothing|Martin 2001: Noise PSD Estimation via Optimal Smoothing and Minimum Statistics]]
- [[sources/liu-2025-pcen-mask-vad-speech-enhancement|Liu et al. 2025: PCEN-Based Mask Thresholding and VAD for DNN Speech Enhancement Training]] — training-time PCEN-VAD that gates an asymmetric loss
- [[sources/tashev-2008-sound-capture-spatial-filter|Tashev et al. 2008: Sound Capture System and Spatial Filter for Small Devices]] — energy-based binary VAD with minimum-energy tracking used as a binary gate for spatial-filter model adaptation
