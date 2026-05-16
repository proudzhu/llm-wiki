---
type: source
created: 2026-05-15
updated: 2026-05-15
sources:
  - raw/papers/zhang-2023-hybrid-ahs/full-text.txt
  - https://doi.org/10.48550/arXiv.2305.02583
  - zotero://select/items/0_ILJW385X
tags:
  - acoustic-howling-suppression
  - kalman-filter
  - deep-learning
  - hybrid-method
---

# Zhang, Yu, Wu, Yu & Yu 2023: Hybrid AHS

**Authors**: [[entities/hao-zhang|Hao Zhang]], [[entities/meng-yu|Meng Yu]], [[entities/yuzhong-wu|Yuzhong Wu]], [[entities/tao-yu|Tao Yu]], [[entities/dong-yu|Dong Yu]]
**Institutions**: Tencent AI Lab, Bellevue, WA, USA; Tencent Ethereal Audio Lab, Shenzhen, Guangdong, China
**Published**: arXiv preprint arXiv:2305.02583, 2023-05-04
**Type**: Preprint
**DOI**: [10.48550/arXiv.2305.02583](https://doi.org/10.48550/arXiv.2305.02583)
**URL**: http://arxiv.org/abs/2305.02583
**Zotero**: [ILJW385X](zotero://select/items/0_ILJW385X)

---

## Summary

Hybrid AHS combines a frequency-domain Kalman filter (FDKF) with a self-attentive recurrent neural network (SARNN) for acoustic howling suppression. The Kalman module first pre-processes the microphone signal, and the DNN is trained with both the Kalman output and a teacher-forced ideal microphone signal so that offline training better matches recursive streaming inference. Across both offline and streaming evaluations, the hybrid cascade consistently outperforms standalone Kalman, Deep AHS, and Deep MFC baselines, especially under stronger howling conditions.

---

## Problem Formulation

### Acoustic Howling Model

In a single-channel acoustic amplification system, the loudspeaker playback re-enters the microphone through the acoustic path and nonlinear loudspeaker distortion:

$$d(t) = NL[x(t)] * h(t)$$

Without suppression, the microphone signal becomes a recursive closed loop:

$$y(t) = s(t) + n(t) + NL[y(t-\Delta t) \cdot G] * h(t)$$

where $s(t)$ is target speech, $n(t)$ is background noise, $h(t)$ is the loudspeaker-to-microphone acoustic path, $G$ is amplifier gain, and $\Delta t$ is system delay.

### Teacher-Forced Reformulation

Directly training a deep model inside the recursive loop is inefficient and mismatched with offline supervision. Hybrid AHS follows Deep AHS and replaces the recursive playback during training with the ideal target speech sent to the loudspeaker:

$$y(t) = s(t) + n(t) + h(t) * NL[s(t-\Delta t) \cdot G]$$

This converts AHS training into a speech separation problem while preserving the one-time playback component. The DNN then learns to recover $s(t)$ from the ideal microphone signal together with a Kalman-preprocessed signal.

### Kalman Prediction and Update

The Kalman module uses the enhanced signal as reference and estimates the feedback path in the STFT domain:

$$E(k) = Y(k) - R(k)\hat{H}(k)$$

$$\hat{H}(k+1) = A[\hat{H}(k) + K(k)E(k)]$$

where $Y(k)$ is the microphone STFT, $R(k)$ is the reference STFT derived from the enhanced signal, $E(k)$ is the error signal, $A$ is the transition factor, and $K(k)$ is the Kalman gain.

---

## Methodology

### Hybrid Cascade Structure

The system contains two modules:

1. **FDKF front-end**: estimates and subtracts the feedback component, producing a pre-processed signal $e(t)$
2. **SARNN back-end**: takes the ideal microphone signal and Kalman-preprocessed signal as inputs and predicts an enhanced speech signal

During streaming inference, the DNN output is fed back as the Kalman reference signal, so the two modules operate recursively inside the acoustic loop.

### Input Features

The model uses 16 kHz audio with 32 ms frames, 16 ms frame shift, and 512-point STFT. Input features include:

- normalized log-power spectra (LPS) of microphone and Kalman-preprocessed signals
- correlation matrices across time and frequency to capture temporal and spectral dependencies
- channel covariance features between the two input signals

These features are fused by a linear layer before entering the recurrent network.

### SARNN Architecture

The DNN module is a self-attentive recurrent neural network with three stages:

1. A GRU layer with 257 hidden units plus two 1D convolution layers estimates complex-valued filters for the input signals
2. Intermediate enhanced signals are converted to LPS features and processed again as three-channel inputs
3. A final SARNN block with two linear layers, two multi-head self-attention layers, one GRU, and residual connections estimates a three-channel enhancement filter

The final enhanced speech is reconstructed through multi-channel deep filtering followed by inverse STFT.

### Why the Hybrid Helps

The paper argues for two main benefits:

1. Kalman pre-processing provides a stronger reference and reduces the mismatch between offline training and streaming inference
2. The DNN compensates for leakage and nonlinear distortion that the Kalman filter alone cannot model well

---

## Experimental Setup

| Parameter | Value |
|:----------|:------|
| Dataset | AISHELL-2 |
| Sampling rate | 16 kHz |
| Frame / shift | 32 ms / 16 ms |
| STFT size | 512 |
| RIR generation | 10,000 sets via image method |
| RT60 range | 0 to 0.6 s |
| System delay | 0.1 to 0.3 s |
| Gain range | 1.0 to 3.2 |
| SPR | -10 to 10 dB |
| SNR | -10 to 30 dB |
| Training / val / test | 10k / 0.3k / 0.5k |
| Epochs / batch size | 60 / 32 |
| Metrics | SI-SDR, PESQ |
| Baselines | Kalman, Deep AHS, Deep MFC |

Nonlinear distortion is simulated using hard clipping and sigmoidal nonlinearities.

### Streaming and Real-Device Evaluation

The paper also evaluates recursive streaming inference under light, moderate, and severe howling by gradually increasing gain. For deployment-oriented validation, the authors train a smaller single-layer LSTM model with 100 hidden units (0.13M parameters), using 8 ms frames and 4 ms shift with only LPS features, and test it on real recordings from a simple acoustic amplification setup.

---

## Results

### Offline Evaluation

Table 1 reports SI-SDR and PESQ for gains $G=1,2,3$:

| Method | SI-SDR @ G=1 | G=2 | G=3 | PESQ @ G=1 | G=2 | G=3 |
|:-------|-------------:|----:|----:|-----------:|----:|----:|
| Kalman | 8.59 | 2.82 | -0.66 | 2.83 | 2.41 | 2.18 |
| Deep AHS | 14.82 | 8.60 | 2.61 | 3.46 | 3.13 | 2.81 |
| Deep MFC | 7.66 | -1.42 | -10.56 | 2.88 | 2.44 | 2.07 |
| **Hybrid AHS** | **20.16** | **17.11** | **14.43** | **3.76** | **3.60** | **3.43** |

Key observations:

- Hybrid AHS is the best method at every gain level in both SI-SDR and PESQ
- The advantage widens as gain increases, showing stronger robustness in severe howling conditions
- Deep MFC degrades sharply at high gain, while Kalman alone suffers from leakage and distortion

### Streaming Inference

In recursive streaming tests with light, moderate, and severe howling, all deep-learning-based methods prevent catastrophic howling, but Hybrid AHS gives the best overall spectrogram quality. The hybrid design preserves speech better while maintaining suppression under progressively increasing gain.

### Real-Recording Validation

The small deployable model also improves over Kalman-only processing on real recordings, showing that the hybrid idea transfers beyond simulation and can work with a lightweight recurrent model.

---

## Key Contributions

1. **Hybrid Kalman + DNN AHS architecture**: cascades FDKF and SARNN so each compensates for the other's weaknesses
2. **Teacher-forced AHS training formulation**: converts recursive AHS into a tractable offline speech separation problem
3. **Kalman-preprocessed neural input**: uses adaptive filtering output as an informative auxiliary input for the DNN
4. **Strong robustness in streaming inference**: maintains suppression quality under recursive closed-loop operation and increasing gain
5. **Deployment-oriented validation**: demonstrates effectiveness with a lightweight LSTM model on real recordings

---

## Related Concepts

- [[concepts/acoustic-howling-suppression|Acoustic Howling Suppression]]
- [[concepts/frequency-domain-kalman-filter|Frequency-Domain Kalman Filter]]
- [[concepts/kalman-filter|Kalman Filter]]
- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]
- [[concepts/neural-networks|Neural Networks]]
- [[concepts/acoustic-feedback|Acoustic Feedback]]
- [[concepts/adaptive-filtering|Adaptive Filtering]]

## Related Synthesis

- [[synthesis/kalman-filter-theory-and-application|Kalman Filter Theory and Application]]
- [[synthesis/ai-driven-anc|AI-Driven ANC]]
