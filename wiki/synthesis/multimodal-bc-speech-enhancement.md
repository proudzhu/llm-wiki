---
type: synthesis
created: 2026-04-22
updated: 2026-05-16
sources:
  - wiki/sources/he-2025-vibomni.md
  - wiki/sources/zhang-2022-bone-conducted-speech-dissertation.md
  - wiki/sources/dai-2026-speech-preserving-deep-anc.md
  - zotero://select/items/0_K592VRRE (Wang 2022: Complex Fusion)
  - zotero://select/items/0_B92ER5KS (Khanagha 2026: Conditional Diffusion)
  - zotero://select/items/0_NIIDMA7J (Contrastive Learning for BC)
tags:
  - bone-conduction
  - multimodal-fusion
  - speech-enhancement
  - deep-learning
  - diffusion-models
  - smart-hearables
---

# Multimodal Smart Hearables: Bone-Conduction Aided Speech Enhancement

This synthesis tracks the evolution of Bone-Conducted (BC) speech integration in smart hearables (headphones, AR glasses), moving from traditional statistical analysis to state-of-the-art generative diffusion models.

## 1. The Multimodal Imperative: AC vs. BC
Traditional Air-Conducted (AC) microphones capture full-band audio but are highly susceptible to background noise. BC sensors (accelerometers) capture vibrations directly from the skull, providing **noise-immune** signals that are intrinsically limited in bandwidth (usually <2 kHz).

| Modality | Bandwidth | Noise Immunity | Limitation |
| :--- | :--- | :--- | :--- |
| **AC (Air)** | Full-band | Low | Unusable at very low SNRs (-10 dB) |
| **BC (Bone)**| Low-pass | **High** | Muffled quality; missing high frequencies |

---

## 2. Technical Evolution of Fusion Strategies

### 2.1 Statistical and Mapping Era (2020-2022)
Focuses on "restoring" BC speech or using it as a reference for AC denoising.
- **Pitch Extraction (Zhang, 2022)**: Combines AC weighted auto-correlation with BC cepstrum (WACF-CEP) to detect pitch in 0 dB SNR environments.
- **Complex Spectral Mapping (Wang, 2022)**: Uses Deep Complex CRNs (DC-CRN) to fuse AC and BC signals in the complex domain, preserving phase information.
- **Attention-based Fusion**: Replaces simple concatenation with attention masks to "selectively" weigh AC and BC features based on instantaneous SNR.

### 2.2 Lightweight Multi-Modal Fusion (2023-2025)
Parallel to the generative trend, a line of work focuses on practical, lightweight multi-modal fusion using commodity IMU sensors already available in earables.

- **He et al. (MobiSys 2023 / arXiv 2025) — VibOmni**: Demonstrates that the IMU (accelerometer + gyroscope) already present in commercial earables for head-tracking can capture bone-conducted vibration at ~1.6 kHz sampling rate. The system uses a dual-encoder DPRNN architecture with:
  - **Auxiliary decoder** on the vibration branch to prevent modality collapse (audio dominating training).
  - **Bone Conduction Function (BCF) data augmentation**: Models the audio→vibration transfer function as a Gaussian in the frequency domain, enabling synthetic vibration generation from LibriSpeech with only 4.5% spectrogram error.
  - **Multi-modal SNR estimator** for continual self-supervised learning and adaptive inference.
  - **Key result**: 31× lower latency than FullSubNet on mobile devices, 21% PESQ improvement, ~40% WER reduction — all using existing IMU sensors without additional hardware.

### 2.3 Generative and Diffusion Era (2025-2026)
Shifts from predicting clean speech to **generating** it using BC signals as guidance.
- **Conditioned Diffusion (Khanagha, 2026)**: The **BCDM** (Bone-Conduction Conditional Diffusion Model) treats clean speech recovery as a stochastic process.
- **Conditioning Strategies**:
    - **Input Concatenation (IC)**: Simple but effective at low computational cost.
    - **Decoder Conditioning (DC)**: Injects BC features directly into the decoder's upsampling layers, providing superior speech naturalness (POLQA/PESQ) at the cost of higher latency.
- **Contrastive Learning (Li, 2025)**: Uses twin-tower networks to minimize the embedding distance between AC and BC modalities, improving cross-modal feature alignment.

---

## 3. Core Technical Challenges

### 3.1 The Bandwidth Gap (Super-Resolution)
Because BC speech is missing frequencies above 2 kHz, multimodal systems must perform **Guided Super-Resolution**. Generative models (GANs and Diffusion) excel here by hallucinating plausible high-frequency details that match the low-frequency "skeleton" provided by the BC sensor.

### 3.2 Real-time Implementation & Latency
- **STFT vs. Time-Domain**: Frequency-domain methods (STFT) introduce frame-level latency (~32-64ms).
- **Embedded Constraints**: Diffusion models require multiple reverse steps (e.g., $N=60$), making them challenging for low-power DSPs. Recent work (Liang, 2026) emphasizes **Analytic/Closed-form** solutions to minimize these overheads.

### 3.3 Data Scarcity
Parallel AC-BC data is difficult to collect. **Semi-supervised frameworks** (using CycleGANs) allow models to learn from non-parallel AC and BC datasets, significantly lowering the barrier for training robust production models.

---

## 4. Key Performance Benchmarks

| Method | NR (dB) | PESQ Gain | Best For |
| :--- | :--- | :--- | :--- |
| **Standard FxLMS** | 2-5 | Low | Steady-state noise only |
| **DC-CRN (Wang)** | 10-15 | Moderate | General mobile communication |
| **BCDM (Khanagha)**| **18+** | **High** | Extreme noise environments (-10 dB SNR) |

## References
- [[wiki/sources/zhang-2022-bone-conducted-speech-dissertation|Zhang 2022: BC Statistical Analysis]]
- [[wiki/sources/dai-2026-speech-preserving-deep-anc|Dai 2026: Speech-Preserving Deep ANC]]
- *Wang et al. (2022) Fusing BC and AC Sensors for Complex-Domain SE*
- *Khanagha et al. (2026) BC Guided Multimodal SE with Conditional Diffusion*
- [[wiki/synthesis/modern-headphone-anc-systems|Modern Headphone ANC Systems]]

### 2.4 Lightweight T-F Domain Fusion (2024)
Parallel to the IMU-based approach, a line of work focuses on lightweight time-frequency domain fusion using dedicated BC microphones.

- **Kuang, Yang & Yang (JASA 2024) — DenGCAN**: A lightweight fused BC/AC speech enhancement model using:
  - **Iterative Attentional Feature Fusion (iAFF)** for coarse-then-refined multi-modal fusion
  - **DenGCAN backbone** with dense blocks (feature reuse), gated convolutions, and sConformer bottleneck
  - **Attention Gate (AG) skip-connections** that consider local + global features
  - **Key result**: 1.03M params, 0.859 GMACs, 1.870 wb-PESQ improvement, RTF 0.649 on ARM — lowest compute among all compared models
  - **A4BS dataset**: 4-position BC recordings from 109 speakers (~107 h)

## Related Concepts

- [[../concepts/bcs-guided-speech-enhancement|BCS-Guided Speech Enhancement]]
- [[../concepts/bone-conduction|Bone Conduction]]
- [[../concepts/densely-gated-convolutional-attention-network|DenGCAN]]
- [[../concepts/iterative-attentional-feature-fusion|Iterative Attentional Feature Fusion (iAFF)]]
- [[../concepts/attention-gate|Attention Gate (AG)]]

## Related Sources

- [[wiki/sources/dai-2026-speech-preserving-deep-anc|Dai 2026: Speech-Preserving Deep ANC]]
- [[wiki/sources/zhang-2022-bone-conducted-speech-dissertation|Zhang 2022: BC Statistical Analysis]]
- [[wiki/sources/kuang-2024-lightweight-speech-enhancement-bone-air|Kuang, Yang & Yang 2024: A Lightweight Speech Enhancement Network Fusing Bone- and Air-Conducted Speech]]
