---
type: concept
created: 2026-05-20
updated: 2026-05-20
tags:
  - acoustic-signal-processing
  - machine-listening
  - pattern-recognition
---

# Acoustic Scene Classification

**Acoustic Scene Classification (ASC)** is a core audio pattern recognition task that aims to classify a recorded environmental audio signal into one of several predefined location-based classes (acoustic scenes), such as "airport", "park", "shopping mall", "street", or "subway station". ASC plays a vital role in context-aware mobile devices, robotics, smart hearing aids, and environmental monitoring.

## Key Challenges and Formulations

The primary objective of ASC is to map an audio sample $x(t)$ to a class label $c \in \{1, 2, \dots, N\}$. 

### 1. Feature Representation
Audio signals are high-dimensional time-domain signals. ASC systems typically transform them into 2D time-frequency representations using the **Short-Time Fourier Transform (STFT)**. 

The raw spectrogram is then processed through a Mel-scale filter bank to match human auditory perception, resulting in a **Log-Mel spectrogram** input $X \in \mathbb{R}^{1 \times F \times T}$, where $F$ is the number of Mel frequency bins and $T$ is the number of temporal frames.

### 2. Device Robustness (Domain Shift)
Audio recordings in ASC benchmarks are often collected across different cities and physical recording devices (smartphones, studio microphones, etc.). Different device frequency responses introduce a severe domain shift. To solve this, methods like **Mixup** and **Freq-MixStyle** are used to augment the training data by manipulating Mel-spectrogram distributions.

### 3. Model Complexity (Edge Deployment)
Because ASC is frequently deployed on resource-constrained devices (e.g., wearables, mobile phones), a major constraint is the computational cost, measured in Multiply-Accumulate operations (MACs) and parameter counts. 

This constraint has driven the development of highly efficient convolutional neural network (CNN) architectures that replace 2D kernels with 1D kernels (e.g., consecutive or parallel separate kernels).

## Related Concepts

- [[concepts/spectrogram-analysis|Spectrogram Analysis]]
- [[concepts/time-frequency-separate-convolutions|Time-Frequency Separate Convolutions]]
- [[concepts/bc-resnet|BC-ResNet]]
- [[concepts/adaptive-residual-normalization|Adaptive Residual Normalization]]

## Related Sources

- [[sources/cai-2024-tf-sepnet|Cai, Zhang & Li 2024: TF-SepNet]]
