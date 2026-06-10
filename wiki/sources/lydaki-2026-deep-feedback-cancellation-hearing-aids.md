---
type: source
created: 2026-06-10
updated: 2026-06-10
sources:
  - raw/papers/lydaki-2026-deep-feedback-cancellation-hearing-aids/full-text.md
  - https://doi.org/10.1109/TASLPRO.2026.3700049
  - zotero://select/items/0_QQE7D6DX
tags:
  - hearing-aids
  - feedback-cancellation
  - deep-learning
  - system-identification
  - impulse-response-estimation
---

# Lydaki, Tan, Jensen & Guo 2026: Deep Feedback Cancellation in Hearing Aids

**Authors**: [[entities/eleftheria-lydaki|Eleftheria Lydaki]], [[entities/zheng-hua-tan|Zheng-Hua Tan]], [[entities/jesper-jensen|Jesper Jensen]], [[entities/meng-guo|Meng Guo]]
**Institutions**: Eriksholm Research Centre, Snekkersten, Denmark; Department of Electronic Systems, Aalborg University, Denmark
**Published**: IEEE Transactions on Audio, Speech, and Language Processing, 2026, pp. 1-15
**Type**: Journal Article
**DOI**: [10.1109/TASLPRO.2026.3700049](https://doi.org/10.1109/TASLPRO.2026.3700049)
**Zotero**: [QQE7D6DX](zotero://select/items/0_QQE7D6DX)

## Summary

Deep Feedback Cancellation (DFC) is a compact DNN (856K parameters) that estimates the hearing aid feedback path impulse response directly from loudspeaker and microphone signals. Unlike prior deep learning approaches that predict the clean output signal (e.g., DeepMFC with 8.7M params), DFC predicts the feedback-path IR, exploiting the constrained solution space of plausible IRs. A two-stage training strategy (pre-train on synthetic IRs, fine-tune on measured HA IRs) and the NESD loss with temporal smoothing (average pooling N=50, exponential smoothing α=0.5) enable fast convergence and robust tracking. DFC outperforms FD-AFC and DeepMFC on both speech (PESQ 4.54 vs 4.34/4.35) and music (PEAQ -0.53 vs -2.31/-0.92), converges 30x faster after path changes, and achieves significantly higher MUSHRA scores (86.13 vs 57.48/37.45 for speech).

## Problem Formulation

Hearing aid acoustic feedback limits the [[concepts/maximum-stable-gain|Maximum Stable Gain]] (MSG), causing howling artifacts. Traditional adaptive filtering (AF) methods like NLMS and Kalman filters face:

1. **Convergence speed vs steady-state error trade-off**: Fast convergence requires large step sizes (high steady-state error); low steady-state error requires small step sizes (slow convergence)
2. **Biased estimation**: High correlation between target signal and feedback signal causes the adaptive filter to converge to a biased estimate

Existing deep learning approaches (DeepMFC, Neural-AFC) predict the clean output signal directly, requiring large networks (8.7M params for DeepMFC) and struggling when the feedback path changes.

## Methodology

### DFC Architecture

The DFC processes loudspeaker signal u(n) and microphone signal y(n) to estimate the feedback-path IR f̂(n):

1. **STFT**: 64-sample window (4 ms at 16 kHz), 50% overlap → 33 frequency bins
2. **Log magnitude + phase**: Concatenated as input features [log|U|, ∠U, log|Y|, ∠Y]
3. **Causal convolution**: 2 layers, (4,5) kernels with LeakyReLU(0.01) and (2,1) dilations
4. **Skip connection**: Input features added to conv output
5. **FC1**: Linear projection to 64 dims + LeakyReLU(0.01)
6. **LSTM**: 128 hidden units, captures temporal dynamics
7. **FC2 + FC3**: Two tanh layers projecting to IR length L_f
8. **AveragePooling**: Window N=50 for temporal smoothing
9. **IR estimate**: f̂(n) = α · f̄(n) + (1-α) · f̂(n-1), α=0.5

Total parameters: **856K** (10x smaller than DeepMFC's 8.7M).

### NESD Loss Function

The Normalized Euclidean System Distance loss with temporal smoothing:

```
L_NESD = (1/N) · Σ_{i=0}^{N-1} ||f(n-i) - f̂(n-i)||² / ||f(n-i)||²
```

The average pooling (N=50) and exponential smoothing (α=0.5) are critical: without them, the model achieves lower steady-state error but much slower convergence. The smoothing encourages consistent IR estimates across consecutive frames.

### Two-Stage Training

1. **Pre-training**: 500 epochs on synthetic IRs (exponentially decaying noise, random delays/decay rates)
2. **Fine-tuning**: 500 epochs on measured HA IRs (200 IRs from 10 HA types, 2 dome types, 5 acoustic conditions)

Fine-tuning on measured IRs improves PESQ from 4.35 to 4.54 and reduces variance significantly.

### Training Data

- **Speech**: LibriSpeech train-clean-360 (16 kHz)
- **Music**: Slakh2100 (73 MIDI instruments, 175 sub-mixes)
- **HA processing**: 128-band FIR filterbank with prescribed gains (moderate-severe hearing loss profile)
- **Feedback paths**: Synthetic (pre-training) + measured HA IRs (fine-tuning)
- **Loop magnitude**: Randomly selected so maximum loop magnitude ≤ 0 dB (Nyquist stability)

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Sample rate | 16 kHz |
| STFT window | 64 samples (4 ms) |
| STFT hop | 32 samples (50% overlap) |
| IR length L_f | 64 samples |
| LSTM hidden | 128 |
| Parameters | 856K |
| Training epochs | 500 (pre-train) + 500 (fine-tune) |
| Optimizer | Adam, lr=1e-3, ReduceLROnPlateau |
| Batch size | 32 |
| Metrics | PESQ, PEAQ, NESD, FSR, MSG, MUSHRA |

Three evaluation scenarios:
1. **Moderate feedback**: Gains 5-10 dB below instability
2. **Near instability**: Gains close to MSG
3. **Feedback path change**: Abrupt path switch at 7.5 seconds

## Results

### Speech Quality (PESQ)

| Method | Params | Moderate FB | Near Instability | Path Change |
|--------|--------|-------------|------------------|-------------|
| FD-AFC | - | 4.34 | 4.28 | 4.18 |
| FD-AFC-FS | - | 4.34 | 4.29 | 4.19 |
| DeepMFC | 8.7M | 4.35 | 4.20 | 3.85 |
| **DFC** | **856K** | **4.54** | **4.48** | **4.42** |

### Music Quality (PEAQ, higher = better, 0 = best)

| Method | Moderate FB | Near Instability | Path Change |
|--------|-------------|------------------|-------------|
| FD-AFC | -2.31 | -2.52 | -2.68 |
| FD-AFC-FS | -0.92 | -1.15 | -1.35 |
| DeepMFC | -0.92 | -1.20 | -1.85 |
| **DFC** | **-0.53** | **-0.68** | **-0.82** |

### MUSHRA Listening Test (24 participants)

| Method | Speech (no change) | Speech (change) | Music (no change) | Music (change) |
|--------|--------------------:|----------------:|-------------------:|----------------:|
| FD-AFC | 81.00 | 33.96 | - | - |
| FD-AFC-FS | - | - | 48.23 | 45.00 |
| DeepMFC | 45.36 | 29.53 | 60.96 | 36.53 |
| **DFC** | **92.06** | **80.20** | **96.50** | **86.93** |

### Convergence Speed

- DFC converges in ~0.5s after path change vs ~15s for FD-AFC (**30x faster**)
- DFC maintains higher MSG (~23 dB speech, ~21.5 dB music) vs FD-AFC (~19-22 dB)

### Computational Complexity

| Method | Parameters | RTF |
|--------|-----------|-----|
| FD-AFC | - | 0.05 |
| DeepMFC | 8.7M | 0.40 |
| **DFC** | **856K** | **0.10** |

### Cross-Domain Generalization

DFC_speech (trained only on speech) achieves reasonable performance on music, and vice versa. This is because DFC learns the relationship between loudspeaker and microphone signals (feedback-path IR), which is signal-type independent.

## Key Contributions

1. **DFC**: Compact DNN (856K params) for direct feedback-path IR estimation, 10x smaller than DeepMFC
2. **NESD loss with temporal smoothing**: Average pooling (N=50) + exponential smoothing (α=0.5) resolve convergence/steady-state trade-off
3. **Two-stage training**: Pre-train on synthetic IRs + fine-tune on measured HA IRs improves robustness
4. **Predicting IR vs clean signal**: IR estimation has a constrained solution space, enabling smaller models and better generalization
5. **Comprehensive evaluation**: Both speech and music, objective (PESQ/PEAQ) and subjective (MUSHRA), across multiple acoustic scenarios
6. **30x faster convergence** after path changes compared to FD-AFC

## Related Concepts

- [[concepts/deep-feedback-cancellation|Deep Feedback Cancellation]]
- [[concepts/hearing-aid-feedback-cancellation|Hearing Aid Feedback Cancellation]]
- [[concepts/normalized-euclidean-system-distance|Normalized Euclidean System Distance]]
- [[concepts/maximum-stable-gain|Maximum Stable Gain]]
- [[concepts/prediction-error-method|Prediction Error Method]]
- [[concepts/frequency-shift-feedback-cancellation|Frequency Shift Feedback Cancellation]]
- [[concepts/acoustic-feedback|Acoustic Feedback]]
- [[concepts/adaptive-feedback-control|Adaptive Feedback Control]]
- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]

## Related Sources

- [[sources/zhan-2025-deeppem-afc|Zhan 2025: DeepPEM-AFC]] — Deep learning step-size control for PEM-AFC
- Lydaki et al. 2025: Original DFC conference paper (ICASSP 2025)
- Zheng et al. 2022: Deep learning for marginal stability in hearing aids (DeepMFC)
- Zhang et al. 2023: Deep AHS for howling suppression
- Soleimani et al. 2023: Neural-AFC with closed-loop training
