---
type: source
created: 2026-04-18
updated: 2026-05-02
sources:
  - raw/papers/zhang-2024-neural-kalman-howling/full-text.txt
  - https://doi.org/10.21437/Interspeech.2024-166
  - zotero://select/items/0_T3GXM3RI
tags:
  - acoustic-howling-suppression
  - kalman-filter
  - neural-network
  - adaptive-filtering
---

# Zhang, Zhang, Yu & Yu 2024: Neural Network Augmented Kalman Filter for AHS

**Authors**: [[entities/yixuan-zhang|Yixuan Zhang]], [[entities/hao-zhang|Hao Zhang]], [[entities/meng-yu|Meng Yu]], [[entities/dong-yu|Dong Yu]]
**Institutions**: Ohio State University, Columbus, OH, USA; Tencent AI Lab, Bellevue, WA, USA
**Published**: Interspeech 2024, pp. 1715–1719
**Type**: Conference Paper
**DOI**: [10.21437/Interspeech.2024-166](https://doi.org/10.21437/Interspeech.2024-166)
**Zotero**: [T3GXM3RI](zotero://select/items/0_T3GXM3RI)

---

## Summary

Proposes NeuralKalmanAHS, which integrates neural network modules into a frequency-domain Kalman filter (FDKF) for acoustic howling suppression. Two NN components enhance the FDKF: (1) a learned reference signal via LSTM-based ratio mask, and (2) neural covariance matrix estimation for $\Psi_{vv}$ and $\Psi_{\Delta\Delta}$. A streaming training strategy with howling detection ensures convergence. Outperforms standalone NN and Kalman filter methods, achieving 2.32 dB SDR at G=2.

---

## Problem Formulation

### Acoustic Howling Model

Without AHS, the microphone signal forms a recursive feedback loop:

$$y(t) = s(t) + [G \cdot y(t - \Delta t)] * h(t)$$

where $G$ is loudspeaker gain, $\Delta t$ is system delay, $h(t)$ is the acoustic path from loudspeaker to microphone.

With AHS:

$$y(t) = s(t) + [G \cdot \hat{s}(t - \Delta t)] * h(t)$$

where $\hat{s}(t)$ is the AHS output. Robustness depends on how thoroughly howling is removed in each iteration.

### Key Distinction from AEC

Acoustic howling differs from acoustic echo in two ways:
1. Howling involves recursively accumulated and re-amplified playback signals
2. In howling scenarios, the playback signal originates from the same near-end speaker, making AHS more challenging

### Frequency-Domain Kalman Filter

FDKF estimates the feedback signal by modeling the acoustic path with an adaptive filter $W(k)$:

**Prediction step:**

$$\hat{S}(k) = Y(k) - X(k)\hat{W}(k)$$

**Update step:**

$$\hat{W}(k+1) = A[\hat{W}(k) + K(k)\hat{S}(k)]$$

**Kalman gain:**

$$K(k) = P(k)X^H(k)[X(k)P(k)X^H(k) + \Psi_{vv}(k)]^{-1}$$

$$P(k+1) = A^2[I - \alpha K(k)X(k)]P(k) + \Psi_{\Delta\Delta}(k)$$

where $\Psi_{vv}(k)$ and $\Psi_{\Delta\Delta}(k)$ are observation and process noise covariances, approximated by $\Psi_{\hat{s}\hat{s}}(k)$ and $\Psi_{\hat{W}\hat{W}}(k)$ respectively.

---

## Methodology

### NeuralKalmanAHS Architecture

Two NN modules augment the FDKF:

**1. Reference Signal Refinement** — LSTM-based ratio mask:

$$R(k) = H_r(Y(k), X(k-1))$$

- Two-layer LSTM (300 units/layer) + linear layer with Sigmoid
- Input: concatenation of log power spectrums of $X(k-1)$ and $Y(k)$
- Output: ratio mask applied to microphone signal → refined reference $R(k)$
- Reduces operational load on Kalman filter for severe howling

**2. Covariance Matrix Estimation** — LSTM cells:

$$\Psi_{vv}(k) = H_{\Psi_1}(\hat{S}(k)), \quad \Psi_{\Delta\Delta}(k) = H_{\Psi_2}(\hat{W}(k))$$

- Each: LSTM cell with 65 hidden states
- Input for $\Psi_{vv}$: magnitude of estimated near-end speech $\hat{S}(k)$
- Input for $\Psi_{\Delta\Delta}$: magnitude of estimated acoustic path $\hat{W}(k)$
- Replaces static approximations with learned, dynamic estimates

### Training Strategy

**Loss function:** L1 on magnitude spectrum

$$Loss = l_1(S, \hat{S})$$

**Streaming training:** Model trained in streaming mode aligned with the streaming inference framework from DeepAHS, eliminating training-inference mismatch.

**Howling detection:** During training, if output amplitude exceeds upper limit for 100+ consecutive samples, training halts to prevent energy explosion and NAN issues. This prevents gradient update failures and enhances convergence.

---

## Experimental Setup

| Parameter | Value |
|:----------|:------|
| Training Epochs | 60 |
| Batch Size | 128 |
| Near-end Speech | AISHELL-2 dataset |
| RIRs | 10,000 pairs, image method, RT60 0–0.6 s |
| System Delay | Simulated |
| Loudspeaker Gain (G) | 1.5, 2.0, 2.5, 3.0 |
| Metrics | SDR (dB), PESQ |
| Baseline Methods | Kalman filter, HybridAHS, DeepAHS |

---

## Results

### Ablation Study (G=2)

| Configuration | SDR (dB) | PESQ |
|:-------------|:---------|:-----|
| **NeuralKalmanAHS** | **2.32 ± 1.92** | **2.27 ± 0.46** |
| without R | 1.28 ± 1.42 | 1.72 ± 0.38 |
| without $\Psi_{vv}, \Psi_{\Delta\Delta}$ | 2.17 ± 1.85 | 2.21 ± 0.47 |
| Kalman filter only | -11.92 ± 15.62 | 1.62 ± 0.80 |

Key findings from ablation:
- **Reference signal refinement** provides the largest performance boost (SDR: 1.28 → 2.32)
- **Covariance estimation** improves robustness (lower std deviation)
- **Streaming training** ensures robustness against howling even with lightweight models

### Comparison with Baselines

NeuralKalmanAHS outperforms standalone NN and Kalman filter methods across all gain settings (G=1.5 to 3.0), demonstrating remarkable stability in challenging scenarios.

---

## Key Contributions

1. **NN-augmented FDKF for AHS**: First integration of NN modules for both reference refinement and covariance estimation in the AHS domain
2. **Streaming training strategy**: Eliminates training-inference mismatch by training in streaming mode
3. **Howling detection for training stability**: Prevents energy explosion during recursive training
4. **Insight on covariance estimation**: Exclusively using NNs to estimate Kalman filter components doesn't necessarily help; leveraging NNs for absent or approximated components does

---

## Related Concepts

- [[concepts/kalman-filter|Kalman Filter]]
- [[concepts/acoustic-howling-suppression|Acoustic Howling Suppression]]
- [[concepts/frequency-domain-kalman-filter|Frequency-Domain Kalman Filter]]
- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]
- [[concepts/active-noise-control|Active Noise Control]]

## Related Synthesis

- [[synthesis/kalman-filter-theory-and-application|Kalman Filter Theory and Application]]
- [[synthesis/ai-driven-anc|AI-Driven ANC]]
