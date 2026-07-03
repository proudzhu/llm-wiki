---
type: concept
created: 2026-05-02
updated: 2026-07-03
sources:
  - raw/papers/zhang-2024-neural-kalman-howling/full-text.txt
  - raw/papers/zhang-2023-hybrid-ahs/full-text.txt
  - raw/papers/ashur-2026-acoustic-howling-suppression-fine-tuning/full-text.md
tags:
  - acoustic-howling
  - feedback-cancellation
  - signal-processing
---

# Acoustic Howling Suppression

**Acoustic Howling Suppression (AHS)** is the process of preventing or mitigating the positive feedback loop in audio amplification systems where the loudspeaker output is captured by the microphone and recursively re-amplified, producing high-pitched tonal artifacts.

## Overview

Acoustic howling occurs when:

$$y(t) = s(t) + [G \cdot y(t - \Delta t)] * h(t)$$

The recursive re-amplification of playback signal through the acoustic path $h(t)$ with gain $G > 1$ creates an unstable positive feedback loop that reinforces specific frequency components.

### Distinction from Acoustic Echo

| Aspect | Acoustic Howling | Acoustic Echo |
|--------|-----------------|---------------|
| Signal source | Same near-end speaker recursively amplified | Far-end speaker |
| Accumulation | Recursively accumulated and re-amplified | Single pass |
| Challenge | More challenging due to recursive nature | Less severe |

## AHS Methods

### Gain Control
Reduce loudspeaker gain to break the feedback loop. Simple but limits system output.

### Notch Filter
Insert narrow-band filters at detected howling frequencies. Requires accurate howling detection.

### Adaptive Feedback Cancellation (AFC)
Use adaptive filters (e.g., Kalman filter, FxLMS) to estimate and subtract the feedback component. Real-time adaptation breaks the positive feedback loop.

### Deep Learning Approaches
- **DeepMFC**: Trains neural networks exclusively on offline-generated synthetic howling data, primarily to stabilize the feedback loop. Establishes feasibility of learning-based AHS but is later surpassed by hybrid and recursive methods.
- **DeepAHS**: Teacher-forcing strategy with streaming inference
- **HybridAHS**: Cascades FDKF and SARNN, using Kalman-preprocessed signals as auxiliary neural inputs
- **NeuralKalmanAHS**: NN modules integrated into FDKF for reference refinement and covariance estimation
- **Denoiser fine-tuning (Ashur & Cohen 2026)**: A pretrained real-time speech-enhancement ([[concepts/denoiser-network|Denoiser Network (DEMUCS)]]) is fine-tuned by mixing offline-generated howling samples with the original noise-reduction training data. Unlike dedicated AHS models, this approach explicitly **preserves speech-enhancement capabilities** while gaining AHS robustness — the 60-40 mixing ratio achieves state-of-the-art PESQ stability across gains (only ~0.05 PESQ drop from G=1.5 to G=3 vs. 0.5–0.6 for HybridAHS/NKal-AHS), with <1% noise-reduction degradation. No architectural modification or recursive training required.

## Key Challenge

Training-inference mismatch: offline training without AHS processing differs from real-time streaming inference where AHS output recursively influences input. Streaming training strategies and hybrid adaptive-neural designs address this.

## Related Concepts

- [[concepts/kalman-filter|Kalman Filter]] — adaptive filter used in AFC-based AHS
- [[concepts/frequency-domain-kalman-filter|Frequency-Domain Kalman Filter]] — FDKF for AHS
- [[concepts/acoustic-feedback|Acoustic Feedback]] — the feedback phenomenon that causes howling
- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]] — NN-based AHS methods
- [[concepts/teacher-forcing|Teacher Forcing]] — training strategy for recursive AHS models (used by DeepAHS/HybridAHS, not by the Denoiser fine-tuning approach)
- [[concepts/self-attentive-recurrent-neural-network|Self-Attentive Recurrent Neural Network]] — Hybrid AHS neural backbone
- [[concepts/denoiser-network|Denoiser Network (DEMUCS)]] — pretrained speech-enhancement backbone fine-tuned for AHS in Ashur & Cohen 2026
- [[concepts/speech-enhancement|Speech Enhancement]] — the original task that fine-tuned Denoiser preserves alongside AHS

## Related Sources

- [[sources/zhang-2023-hybrid-ahs|Zhang 2023: Hybrid AHS]]
- [[sources/zhang-2024-neural-kalman-howling|Zhang 2024: Neural Network Augmented Kalman Filter for AHS]]
- [[sources/ashur-2026-acoustic-howling-suppression-fine-tuning|Ashur & Cohen 2026: AHS by Fine-Tuning Deep Speech Enhancement Networks]]
