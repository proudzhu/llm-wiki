---
type: concept
created: 2026-04-12
updated: 2026-05-06
sources:
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

## VAD-Free Alternatives

While VAD is widely used, VAD-free noise estimation methods avoid the binary speech/pause decision and its associated tuning difficulties:

- **[[concepts/minimum-statistics|Minimum Statistics]]** (Martin 2001): Tracks spectral minima in each frequency band without distinguishing speech from silence. Derives optimal time-varying smoothing parameters and bias compensation. Performs well in low SNR and nonstationary noise, and updates noise estimates even during speech activity.

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
