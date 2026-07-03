---
type: concept
created: 2026-07-03
updated: 2026-07-03
sources:
  - raw/papers/ashur-2026-acoustic-howling-suppression-fine-tuning/full-text.md
tags:
  - speech-enhancement
  - deep-learning
  - neural-network-architecture
  - time-domain
  - real-time
---

# Denoiser Network (DEMUCS)

**Denoiser** is a real-time waveform-domain speech enhancement network derived from the DEMUCS (Deep Extractor for Music Sources) architecture, originally proposed by Defossez et al. (2020) for source separation and adapted for low-latency speech enhancement. It has since served as a transferable baseline for downstream audio tasks including [[concepts/acoustic-howling-suppression|Acoustic Howling Suppression]].

## Architecture Overview

The Denoiser inherits DEMUCS's core design:

- **Encoder–decoder** structure with skip connections
- Stacked **convolutional layers** in the encoder progressively downsample the input waveform, capturing both spectral and temporal features
- **LSTM recurrent module** in the latent representation models long-range temporal dependencies
- Activation and normalization layers stabilize training and improve generalization

The Denoiser adapts this architecture for **real-time** speech enhancement by optimizing latency and computational efficiency while preserving the encoder–decoder design.

## Training Paradigm

The pretrained Denoiser is trained on large-scale noisy speech datasets (e.g., Valentini-Botinhao) using **time-domain loss** functions to map noisy inputs to clean speech targets. During inference, the pretrained network effectively suppresses background noise while maintaining speech intelligibility.

The Denoiser repository also estimates the **system delay** $\Delta t$ at inference time based on the target platform's hardware and software configuration.

## Use as a Transferable Baseline

Because the Denoiser is a strong, low-latency speech-enhancement backbone, it is well-suited to **fine-tuning** for related audio tasks:

- **Acoustic howling suppression** (Ashur & Cohen 2026): fine-tune the pretrained Denoiser by mixing offline-generated synthetic howling samples into the original noise-reduction training data. This requires no architectural modification, no recursive training, and introduces no additional inference latency — making it a practical drop-in strategy. The 60-40 howling/noise mixing ratio achieves state-of-the-art perceptual speech quality (PESQ) at higher feedback gains while preserving <1% of the original noise-reduction performance.

## Key Properties

- Operates directly on the **waveform** (time-domain), avoiding invalid-STFT problems common in frequency-domain enhancement
- Causal and low-latency: suitable for streaming inference in hearing aids, PA systems, and other real-time audio systems
- Trained with simple time-domain losses (no adversarial or perceptual losses required)

## Related Concepts

- [[concepts/speech-enhancement|Speech Enhancement]] — the Denoiser's primary task
- [[concepts/acoustic-howling-suppression|Acoustic Howling Suppression]] — a downstream task achieved via fine-tuning
- [[concepts/time-domain-speech-enhancement|Time-Domain Speech Enhancement]] — broader methodological category
- [[concepts/teacher-forcing|Teacher Forcing]] — alternative training strategy (used by DeepAHS), explicitly *not* used by the fine-tuning approach
- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]] — broader context

## Related Sources

- [[sources/ashur-2026-acoustic-howling-suppression-fine-tuning|Ashur & Cohen 2026: AHS by Fine-Tuning Deep Speech Enhancement Networks]] — fine-tunes the Denoiser for AHS
