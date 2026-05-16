---
type: concept
created: 2026-05-16
updated: 2026-05-16
tags:
  - bone-conduction
  - speech-enhancement
  - transfer-function
  - data-augmentation
---

# Bone Conduction Function (BCF)

The **Bone Conduction Function (BCF)** describes the transfer function from air-conducted speech audio to bone-conducted vibration captured by an accelerometer on the head. It models how acoustic speech propagates through the skull and soft tissues to produce measurable vibration signals.

## Formulation

The relationship between bone-conducted vibration and speech is modeled as:

$$
s_{vib} = f(s_{speech}) + \epsilon_{vib}
$$

where $s_{vib}$ is the raw accelerometer signal, $s_{speech}$ is the clean speech audio, $f$ is the BCF, and $\epsilon_{vib}$ is vibration noise.

The corresponding microphone signal is:

$$
s_{mic} = s_{speech} + \epsilon_{mic}
$$

where $\epsilon_{mic}$ is environmental noise captured by the microphone.

## Properties

- **Noise immunity**: Bone-conducted vibration is primarily determined by the user's vocal cord vibrations and is minimally affected by ambient airborne noise, making BCF useful for speech enhancement in noisy environments.
- **Frequency-limited**: The mainstream IMU sampling rate (~1.6 kHz) provides ~800 Hz bandwidth, covering the lower part of human speech.
- **User-dependent**: BCF varies across individuals due to differences in skull geometry, body fat, tissue density, and sensor placement.
- **Time-varying**: Minor changes in sensor placement and physiological state can cause BCF drift over time.

## BCF Estimation

The BCF is estimated from paired audio-vibration recordings using spectral analysis:

1. Split paired recordings into 5-second windows.
2. Compute power spectral density (PSD) using Welch's method for both signals.
3. Estimate the frequency response between audio and vibration from the PSD ratio.
4. Model the BCF as a Gaussian distribution in the frequency domain:

$$
f \sim N(\mu, \sigma^2)
$$

where $\mu$ captures the average frequency response contour and $\sigma$ captures the variance due to head skeleton complexity (Chang et al., 2016).

## Applications: Data Augmentation

BCFs enable synthetic vibration data generation from large public audio datasets (e.g., LibriSpeech):

1. Randomly select a BCF $(\mu, \sigma)$ from a pre-estimated pool.
2. Restore the frequency response from the Gaussian distribution.
3. Apply the frequency response to clean audio via frequency-domain multiplication.
4. The augmented spectrogram achieves only ~4.5% error vs. real acceleration signals (He et al., 2025).

This approach reduces the required paired audio-vibration data by >72×, making large-scale multi-modal training feasible without extensive data collection.

## Related Concepts

- [[../concepts/bone-conduction|Bone Conduction]]
- [[../concepts/bcs-guided-speech-enhancement|BCS-Guided Speech Enhancement]]
- [[../concepts/inertial-measurement-unit|Inertial Measurement Unit (IMU)]]
- [[../concepts/spectrogram-analysis|Spectrogram Analysis]]
- [[../concepts/wiener-filter|Wiener Filter]]

## Related Sources

- [[../sources/he-2025-vibomni|He, Guo, Hou & Yan 2025: VibOmni]]
