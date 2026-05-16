---
type: source
created: 2026-05-15
updated: 2026-05-15
sources:
  - raw/papers/zhan-2025-deeppem-afc/full-text.txt
  - https://doi.org/10.1109/ICASSP49660.2025.10890348
  - zotero://select/items/0_BPH79CM5
tags:
  - hearing-aids
  - adaptive-feedback-cancellation
  - prediction-error-method
  - deep-learning
  - step-size-control
---

# Zhan, Hao, Li & Zheng 2025: DeepPEM-AFC

**Authors**: [[../entities/xiaofan-zhan|Xiaofan Zhan]], [[../entities/fengyuan-hao|Fengyuan Hao]], [[../entities/xiaodong-li|Xiaodong Li]], [[../entities/chengshi-zheng|Chengshi Zheng]]
**Institutions**: Key Laboratory of Noise and Vibration Research, Institute of Acoustics, Chinese Academy of Sciences; University of Chinese Academy of Sciences
**Published**: ICASSP 2025, pp. 1-5
**Type**: Conference Paper
**DOI**: [10.1109/ICASSP49660.2025.10890348](https://doi.org/10.1109/ICASSP49660.2025.10890348)
**URL**: https://ieeexplore.ieee.org/abstract/document/10890348
**Zotero**: [BPH79CM5](zotero://select/items/0_BPH79CM5)

## Summary

DeepPEM-AFC proposes a deep learning-based prediction-error-method (PEM) adaptive feedback cancellation for hearing aids. It uses a GRU network to dynamically predict the optimal step size for filter coefficient updates, combining PEM's de-correlation capability with data-driven step-size control. A frequency-domain PEM implementation reduces computational complexity, and a simulated path generation scheme improves generalization across unseen feedback paths.

## Problem Formulation

Hearing aids suffer from acoustic feedback between receiver and microphone, limiting maximum stable gain (MSG). Traditional AFC methods face a bias problem due to high correlation between target and feedback signals. PEM solves this via whitening pre-filters, but introduces computational complexity and requires careful step-size tuning.

The PEM-AFC update in frequency domain:

```
F̂(l+1) = F̂(l) + G_Lf,10 · diag{μ̂(l)} · U_a^H(l) · E_a(l)
```

where G_Lf,10 is the linear constraint matrix, U_a is the whitened receiver signal, and E_a is the prediction error in frequency domain.

## Methodology

### DeepPEM-AFC Architecture

1. **Feature extraction**: Input features include normalized prediction error, whitened signals, and convergence state indicators
2. **GRU network**: 128-dim hidden states predict optimal step size μ̂(l) from feature vectors
3. **Step size mapping**: μ(l) = μ_max · σ(μ̂(l)) with bounds [ε, u]
4. **Frequency-domain PEM**: FFT-based whitening reduces computational complexity vs time-domain implementation
5. **Closed-loop training**: Model trained end-to-end with NESD loss on filter coefficient estimates

### Path Generation Scheme

To improve generalization, simulated feedback paths are generated:

```
f(n) = sin(2π·f_env·n + φ_env) · |r(n)| · exp(-β·(n - n_f))
```

where f_env ∈ [0.1, 0.2] Hz, β ∈ [0.05, 0.15], n_f ∈ [0, 10] samples.

### Frequency Shift Combination

FS+DeepPEM-AFC adds a 10 Hz frequency shift in the feed-forward path for additional de-correlation.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Dataset | LibriSpeech (16 kHz) |
| Feedback path length | L_f = 64 |
| Real paths | 280 training, remainder evaluation (from Sankowsky-Rothe et al.) |
| Simulated paths | 10,000 randomly generated |
| Frame length / shift | K=160, R=80 |
| GRU hidden dim | 128 |
| Optimizer | Adam, lr=1e-3, 60 epochs |
| Batch size | 32 |
| System delay | 7 ms total |
| Metrics | WB-PESQ, eSTOI, SI-SDR, NESD, ASG, Tracking time |

## Results

| Method | Params(M) | RTF | WB-PESQ | eSTOI | SI-SDR(dB) | Tracking(s) |
|--------|-----------|-----|---------|-------|------------|-------------|
| FS+NLMS | - | 0.05 | 1.93 | 0.85 | -5.06 | - |
| FS+KF | - | 0.05 | 3.64 | 0.97 | 9.83 | 0.69 |
| Neural-AFC | 0.856 | 0.22 | 3.90 | 0.98 | 19.73 | 0.13 |
| DeepPEM-AFC | 0.244 | 0.20 | 4.13 | 0.98 | 21.91 | 0.09 |
| FS+DeepPEM-AFC | 0.244 | 0.21 | 4.23 | 0.99 | 24.53 | 0.09 |
| FS+DeepPEM-AFC(v2) | 0.244 | 0.21 | 4.00 | 0.98 | 17.12 | 0.11 |

Key findings:
- DeepPEM-AFC uses only 30% of Neural-AFC parameters while outperforming it
- Tracking speed improved ~30% over Neural-AFC (0.13s → 0.09s)
- FS+DeepPEM-AFC achieves best overall performance across all metrics
- Simulated-path training (v2) maintains robustness on unseen paths (Path B: 16.60 dB vs -38.33 dB)

## Key Contributions

1. DeepPEM-AFC: GRU-based step-size prediction for PEM-AFC with comprehensive feature set
2. Frequency-domain PEM implementation reducing computational complexity (RTF < Neural-AFC)
3. Simulated path generation scheme for training generalization across unseen feedback paths
4. FS+DeepPEM-AFC combination achieving optimal feedback suppression performance

## Related Concepts

- [[../concepts/acoustic-feedback|Acoustic Feedback]]
- [[../concepts/adaptive-feedback-control|Adaptive Feedback Control]]
- [[../concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]
- [[../concepts/variable-step-size-lms|Variable Step-Size LMS]]
- [[../concepts/prediction-error-method|Prediction Error Method]]
- [[../concepts/hearing-aid-feedback-cancellation|Hearing Aid Feedback Cancellation]]
- [[../concepts/frequency-shift-feedback-cancellation|Frequency Shift Feedback Cancellation]]

## Related Synthesis
