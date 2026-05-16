---
type: source
created: 2026-05-16
updated: 2026-05-16
sources:
  - raw/papers/he-2025-vibomni/full-text.md
  - https://doi.org/10.48550/arXiv.2512.02515
  - zotero://select/items/0_M9GHH9GT
tags:
  - speech-enhancement
  - multi-modal
  - bone-conduction
  - earables
  - arxiv
---

# He, Guo, Hou & Yan 2025: VibOmni — Towards Scalable Bone-Conduction Speech Enhancement on Earables

**Authors**: [[../entities/lixing-he|Lixing He]], [[../entities/yunqi-guo|Yunqi Guo]], [[../entities/haozheng-hou|Haozheng Hou]], [[../entities/zhenyu-yan|Zhenyu Yan]]
**Affiliation**: Department of Information Engineering, The Chinese University of Hong Kong (CUHK)
**Venue**: arXiv preprint (submitted to IEEE Transactions on Mobile Computing)
**Year**: 2025
**Type**: Preprint
**DOI**: [10.48550/arXiv.2512.02515](https://doi.org/10.48550/arXiv.2512.02515)
**arXiv**: [2512.02515](https://arxiv.org/abs/2512.02515)
**Zotero**: [M9GHH9GT](zotero://select/items/0_M9GHH9GT)
**Extended version of**: MobiSys 2023 paper (He et al., 2023)

## Summary

VibOmni is a lightweight, end-to-end multi-modal speech enhancement system for earables that leverages bone-conducted vibrations captured by widely available Inertial Measurement Units (IMUs). It integrates a two-branch encoder-decoder deep neural network with DPRNN to fuse audio and vibration features. To overcome the scarcity of paired audio-vibration datasets, it introduces a novel data augmentation technique that models Bone Conduction Functions (BCFs) from limited recordings. A multi-modal SNR estimator enables continual learning and adaptive inference without on-device back-propagation. Evaluated on 32 volunteers, VibOmni achieves up to 21% improvement in PESQ, 26% in SNR, and ~40% WER reduction with much lower latency on mobile devices.

![VibOmni system overview](raw/papers/he-2025-vibomni/figures/x1.png)
*Figure 1: VibOmni enhances speech quality of head-mounted wearables by extracting the user's clear voice from bone-conducted vibrations.*

## Problem Formulation

The bone conduction vibration and microphone signals are modeled as:

$$
s_{vib}=f(s_{speech})+\epsilon_{vib}\quad s_{mic}=s_{speech}+\epsilon_{mic}
$$

where $s_{vib}$ and $s_{mic}$ are the raw data captured by the accelerometer and microphone, respectively; $s_{speech}$ denotes the ground-truth clean speech; $\epsilon_{vib}$ and $\epsilon_{mic}$ are environmental noises; and $f$ is the **Bone Conduction Function (BCF)**.

The design goal is to extract clean speech from the noisy microphone mixture $s_{mic}$, conditioned on the vibration signal $s_{vib}$ as a complementary modality.

## Methodology

### Multi-Modal Speech Enhancement Network

The network operates in the time-frequency domain using STFT spectrograms:

1. **Encoders**: Separate CNN encoders for audio (16 kHz) and vibration (1.6 kHz) extract high-level features. Due to the 10× sampling rate difference, the audio branch has additional layers and a projection layer aligns frequency dimensions.
2. **DPRNN**: A Dual-Path RNN separates speech from noise at the feature level using inter-block (time) and intra-block (frequency) modeling.
3. **Dual Decoders**: A fusion decoder (both modalities) estimates full-band speech, while an auxiliary decoder (vibration only) predicts low-frequency components to prevent modality collapse during training.
4. **Loss**: SISNR loss for full-band output + auxiliary loss (weight 0.05) for low-band reconstruction.

All convolutions are causal and RNNs are unidirectional for real-time frame-by-frame inference.

![Network architecture](raw/papers/he-2025-vibomni/figures/x11.png)
*Figure 9: Network architecture of the multi-modal speech enhancement network.*

### Pre-training with Bone Conduction Functions (BCFs)

To overcome scarce paired audio-vibration data:

1. **BCF Estimation**: Split paired recordings into 5-second windows. Estimate power spectral density (PSD) via Welch's method. Model BCF as a Gaussian distribution $f \sim N(\mu, \sigma^2)$ in the frequency domain, where $\mu$ and $\sigma$ capture the contour and fluctuation of the frequency response.
2. **Data Augmentation**: Randomly select a BCF from the pool, restore the frequency response from Gaussian parameters, and multiply the frequency domain response with audio from large public datasets (e.g., LibriSpeech) to generate synthetic vibration data.
3. **Accuracy**: Only 4.5% spectrogram similarity error between augmented and real acceleration signals.

![BCF estimation](raw/papers/he-2025-vibomni/figures/x12.png)
*Figure 10: Bone Conduction Functions estimated from dataset 1.*

### Adaptive Speech Enhancement

**Multi-Modal SNR Estimator**: A CNN-based estimator takes concatenated audio and vibration spectrograms to estimate the SNR. Multi-modal input significantly improves estimation accuracy at high SNR (>0 dB) compared to audio-only estimation.

**Continual Learning**: Selects clean audio samples based on estimated SNR, and re-mixes them with noise samples for self-supervised fine-tuning, achieving ~3 dB improvement over out-of-domain models without requiring any clean data.

**Adaptive Inference**: Dynamically adjusts the number of DPRNN separator blocks based on estimated noise level, reducing latency from 0.9s to 0.5s while maintaining output quality.

## Experimental Setup

| Dataset | Content | Duration | Role |
|---------|---------|----------|------|
| LibriSpeech-train | English | 1000 h | Pre-train |
| LibriSpeech-dev | English | 1000 h | Noise |
| Ai-shell | Mandarin | — | Noise |
| VibVoice (self-collected) | English | 3 h | Fine-tune |
| FSD50K | General sound | — | Noise |

**Volunteers**: 15 volunteers for lab data + 22 for in-the-wild + 35 for user study (32 unique).
**Noise**: Mixed at SNRs from -5 dB to 15 dB. Types: FSD50K general noise, speech noise (Ai-shell/LibriSpeech), self-noise. Audio convolved with room impulse responses.
**Baselines**: FullSubNet (FSN, audio-only) and SEANet (SN, audio-vibration).

## Results

### Overall Performance

| Condition | Metric | VibOmni | Improvement vs Baseline |
|-----------|--------|---------|------------------------|
| High noise (0 dB speech noise) | PESQ | 2.0 (vs FSN 1.6) | +26% SNR |
| Low noise (10 dB) | PESQ | 2.7 (vs FSN 2.21) | +21% PESQ |
| In-the-wild (WER) | WER | — | ~40% WER reduction vs baseline |
| User preference | Preference | 87% | Preferred over baseline |

### Ablation Study

| Variant | PESQ | SNR | LSD |
|---------|------|-----|-----|
| Full VibOmni | 2.6 | 15.6 | 3.5 |
| w/o auxiliary decoder | 2.5 | 15.1 | 4.4 |
| w/o data augmentation | 1.9 | 14.0 | 5.0 |
| w/o Gaussian approx | 2.4 | 15.2 | 4.2 |
| Vibration @ 800 Hz | 2.45 | 14.3 | 4.5 |

**Key finding**: Data augmentation reduces paired data requirement by >72× while maintaining comparable performance.

### Runtime (seconds per 5-second clip)

| Device | VibOmni | FSN | SN |
|--------|---------|-----|-----|
| Desktop CPU | 0.05 | 0.27 | 0.5 |
| Desktop GPU | 0.016 | 0.034 | 0.07 |
| Huawei P30 | 0.16 | 5.0 | 1.9 |
| Google Pixel 7 | 0.31 | 5.2 | 1.4 |

VibOmni achieves **31× less latency** than FSN and **12× less** than SN on mobile devices.

## Key Contributions

1. **Multi-modal speech enhancement network** for earables using IMU bone-conducted vibration, with a two-branch encoder-decoder architecture and DPRNN for lightweight real-time inference.
2. **Bone Conduction Function (BCF) data augmentation** that models the audio-to-vibration transfer function as a Gaussian distribution, enabling synthetic vibration generation from public audio datasets and reducing paired data requirements by >72×.
3. **Multi-modal SNR estimator** enabling continual self-supervised learning and adaptive inference — adjusting model depth based on noise level without on-device back-propagation.

## Related Concepts

- [[../concepts/bone-conduction|Bone Conduction]]
- [[../concepts/bone-conduction-function|Bone Conduction Function (BCF)]]
- [[../concepts/bcs-guided-speech-enhancement|BCS-Guided Speech Enhancement]]
- [[../concepts/inertial-measurement-unit|Inertial Measurement Unit (IMU)]]
- [[../concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[../concepts/dprnn|Dual-Path RNN (DPRNN)]]
- [[../concepts/spectrogram-analysis|Spectrogram Analysis]]
- [[../concepts/voice-activity-detection|Voice Activity Detection]]
- [[../concepts/self-supervised-speech-representation|Self-Supervised Speech Representation]]
- [[../concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]

## Related Synthesis

- [[../synthesis/multi-modal-speech-enhancement|Multi-Modal Speech Enhancement]]
