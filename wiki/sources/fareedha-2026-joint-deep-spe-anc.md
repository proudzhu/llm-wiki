---
type: source
created: 2026-04-27
updated: 2026-04-27
sources:
  - raw/papers/fareedha-2026-joint-deep-spe-anc/full-text.txt
  - https://ieeexplore.ieee.org/abstract/document/11461474
  - zotero://select/items/0_P5G5VFR3
tags:
  - active-noise-control
  - secondary-path-estimation
  - deep-learning
  - real-time-systems
  - adaptive-control
  - end-to-end
  - icassp
---

# Fareedha, Vasundhara, Kar & Christensen 2026: Joint Deep SPE and Adaptive Control for ANC

**Authors**: Fareedha, Vasundhara, [[../entities/asutosh-kar|Asutosh Kar]], [[../entities/mads-graesboell-christensen|Mads Græsbøll Christensen]]
**Institutions**: NIT Warangal, Birmingham City University, Aalborg University
**Published**: ICASSP 2026, pp. 15177–15181
**Type**: Conference Paper
**DOI**: [10.1109/ICASSP55912.2026.11461474](https://doi.org/10.1109/ICASSP55912.2026.11461474)
**Zotero**: [P5G5VFR3](zotero://select/items/0_P5G5VFR3)

---

## Summary

This paper proposes an end-to-end deep learning framework that jointly performs secondary path estimation (SPE) and adaptive ANC control. The **DeepSPE** module uses convolutional, recurrent (BiLSTM), and attention layers to predict the secondary path in real time from ANC input-output pairs. The estimated path conditions an **ANC-Net** controller, which uses squeeze-and-excitation blocks and temporal attention to generate binary weights for dynamically selecting sub-control filters from a pre-trained bank. Experiments on real (AIR, RWCP) and simulated impulse responses demonstrate superior noise attenuation (NMSE = −12.38 dB), reduced latency (0.43 ms), and improved robustness compared to both classical adaptive filters and recent deep ANC approaches (SFANC, GFANC, GFANC-Kalman).

## Problem Formulation

### Why Joint SPE + Control?

Classical ANC approaches (FxLMS, etc.) rely on iterative adaptation for secondary path estimation, which:
- Converges slowly in dynamic environments
- Requires manual tuning of step sizes
- Degrades under rapidly changing acoustic conditions

Recent deep ANC methods (SFANC, GFANC variants) improve anti-noise generation via data-driven modeling but **assume a fixed secondary path** during training and inference, preventing adaptation to non-stationary environments.

### Key Insight

Separating SPE and control into independent modules is suboptimal — the controller's performance depends critically on SPE accuracy. A joint, end-to-end framework allows the two modules to cooperate: DeepSPE provides real-time path estimates that condition ANC-Net's filter selection.

## Methodology

### DeepSPE: Deep Secondary Path Estimator

Predicts the secondary path $\hat{S}(z)$ from ANC input-output pairs at frame level (512 samples = 32 ms at 16 kHz, 50% overlap).

| Layer | Parameters | Output Shape |
|:------|:-----------|:-------------|
| Conv1D | 64 filters, kernel=3, stride=1 | [64 × T] |
| BatchNorm + ReLU | — | [64 × T] |
| Conv1D | 128 filters, kernel=3, stride=1 | [128 × T] |
| BatchNorm + ReLU | — | [128 × T] |
| BiLSTM | 128 hidden units | [128 × T] |
| Multi-Head Attention | 4 heads | [128 × T] |
| FC + Sigmoid | — | Estimated IR |

**Ablation results** (SPE accuracy):

| Variant | NMSE (dB) | R |
|:--------|:----------|:--|
| DeepSPE (full) | **−16.27** | **0.9887** |
| w/o Attention | −13.10 | — |
| w/o BiLSTM | −10.90 | — |
| Conv1D Only | −8.30 | — |
| Eriksson's method | −7.63 | — |
| Kuo's method | −10.17 | — |
| Akhtar's method | −12.35 | — |

DeepSPE outperforms the best classical method (Akhtar) by 3.92 dB.

### ANC-Net Controller

Processes normalized serial-to-parallel input with the estimated $\hat{S}(z)$ to generate binary weights $w(n) \in \{0,1\}^K$ for selecting $K$ sub-control filters from a pre-trained bank $\{f_1, \ldots, f_K\}$:

$$F(z) = \sum_{k=1}^{K} w_k(n) \cdot f_k$$

$$y(n) = x(n) * F(z)$$

$$\hat{y}(n) = \hat{S}(z) * y(n)$$

$$e(n) = d(n) - \hat{y}(n)$$

**Architecture**: SE blocks (squeeze-and-excitation) compress and reweight features → BiLSTM captures temporal dependencies → Multi-head attention aggregates contextual information → FC + sigmoid thresholding produces binary weights.

**ANC-Net performance**:

| Method | NMSE (dB) | Parameters (M) | Latency (ms) |
|:-------|:----------|:---------------|:-------------|
| FxLMS (fixed S(z)) | −5.42 | — | 0.10 |
| FxLMS (adaptive S(z)) | −7.15 | — | 0.15 |
| 1D CNN | −8.64 | 0.42 | 0.30 |
| ResNet18 | −10.82 | 11.20 | 1.85 |
| ResNet50 | −11.25 | 23.50 | 2.60 |
| DenseNet121 | −11.68 | 7.98 | 2.20 |
| **ANC-Net (full)** | **−12.38** | **1.05** | **0.43** |
| w/o SE Block | −10.92 | 0.94 | 0.49 |
| w/o BiLSTM | −9.87 | 0.78 | 0.47 |
| w/o Attention | −8.72 | 0.83 | 0.46 |
| Conv2D Only | −8.15 | 0.63 | 0.44 |

ANC-Net achieves the best accuracy with 5–20× fewer parameters and up to 6× lower latency than ResNet/DenseNet baselines.

### Dual-Stream End-to-End Design

Two parallel streams:
1. **DeepSPE stream**: Frame-level secondary path prediction (512-sample frames)
2. **ANC-Net stream**: Sample-level anti-noise generation via dynamic filter selection

The estimated $\hat{S}(z)$ from DeepSPE conditions ANC-Net, enabling adaptation without iterative filter weight updates.

## Experimental Setup

- **Sampling rate**: 16 kHz with bandpass filtering (20–7980 Hz)
- **DeepSPE training**: 9000 impulse responses from AIR and RWCP databases, 500 for testing, 512-sample frames, Adam optimizer (lr = 1×10⁻⁴), MSE loss
- **ANC-Net training**: 80,000 synthetic samples, 2000 each for validation and testing
- **Filter bank**: 15 pre-trained sub-control filters
- **Hardware**: NVIDIA RTX 3090 GPU
- **Reproducibility**: 5 random trials with <0.3 dB variance

## Results

### End-to-End Framework Performance

The proposed system achieves the lowest residual noise levels with fast convergence, outperforming:
- **Classical approaches**: Eriksson, Kuo, Akhtar methods
- **Deep ANC baselines**: SFANC, GFANC, GFANC-Kalman

Methods lacking accurate secondary path modeling exhibit higher steady-state noise, confirming that precise real-time $\hat{S}(z)$ estimation integrated with a deep learning controller is key to ANC performance.

### Key Findings

1. Joint SPE + control outperforms separate optimization
2. SE blocks, BiLSTM, and attention are all essential components (ablation confirms)
3. Binary weight filter selection is efficient (1.05 M params, 0.43 ms latency)
4. The system generalizes to both real and simulated impulse responses

## Key Contributions

1. **DeepSPE**: First deep learning module for real-time secondary path estimation using Conv1D + BiLSTM + attention, achieving −16.27 dB NMSE (3.92 dB improvement over best classical method)
2. **ANC-Net**: SE-block-based controller with temporal attention for dynamic filter selection via binary weights, achieving −12.38 dB NMSE with only 1.05 M parameters
3. **Dual-stream end-to-end design**: Frame-level SPE + sample-level control without iterative adaptation
4. **Comprehensive evaluation**: Real and simulated IRs, comparison with classical and deep ANC baselines, ablation study

## Related Concepts

- [[../concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[../concepts/online-secondary-path-modeling|Online Secondary-Path Modeling]]
- [[../concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]
- [[../concepts/active-noise-control|Active Noise Control]]
- [[../concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[../concepts/neural-networks|Neural Networks]]

## Related Sources

- [[../sources/fareedha-2025-dfanc-ekf|Fareedha 2025: DFANC-EKF]] — Previous work by same authors: EKF + CNN for dynamic fixed-filter ANC
- [[../sources/akhtar-2006-vss-lms-online-spm|Akhtar 2006: VSS LMS for Online Secondary Path Modeling]] — Classical VSS-LMS baseline that DeepSPE outperforms by 3.92 dB

## Related Entities

- [[../entities/fareedha|Fareedha]]
- [[../entities/vasundhara|Vasundhara]]
- [[../entities/asutosh-kar|Asutosh Kar]]
- [[../entities/mads-graesboell-christensen|Mads Græsbøll Christensen]]
