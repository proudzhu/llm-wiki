---
type: source
created: 2026-05-04
updated: 2026-05-04
sources:
  - raw/papers/yang-2026-transformer-e2e-cfg-anc/full-text.md
  - https://arxiv.org/abs/2605.00494
  - zotero://select/items/0_5DHKAHI8
tags:
  - active-noise-control
  - generative-fixed-filter-anc
  - transformer
  - end-to-end-learning
  - unsupervised-learning
---

# Yang, Luo, Zou, Wang, Huang & Gan 2026: Transformer-based E2E-CFG for ANC

**Authors**: [[../entities/ziyi-yang|Ziyi Yang]], [[../entities/zhengding-luo|Zhengding Luo]], [[../entities/yisong-zou|Yisong Zou]], [[../entities/boxiang-wang|Boxiang Wang]], [[../entities/qirui-huang|Qirui Huang]], [[../entities/woon-seng-gan|Woon-Seng Gan]]

**Affiliation**: School of Electrical and Electronic Engineering, Nanyang Technological University, Singapore

**Venue**: arXiv preprint (eess.AS), arXiv:2605.00494

**Year**: 2026 | **Type**: Preprint

**DOI**: [10.48550/arXiv.2605.00494](https://doi.org/10.48550/arXiv.2605.00494) | **Zotero**: [5DHKAHI8](zotero://select/items/0_5DHKAHI8)

## Summary

Proposes a Transformer-based End-to-End Control-Filter Generation (E2E-CFG) framework that directly generates control filters for ANC without sub-filter decomposition and recombination. By integrating a Transformer co-processor with a real-time controller in a fully differentiable ANC system, the method is trained unsupervised using only the accumulated residual error. On unseen real noises, E2E-CFG achieves 18.36 dB average NR, outperforming GFANC (16.63 dB) and FxNLMS (11.13 dB).

## Problem Formulation

Existing GFANC methods generate control filters indirectly through a decomposition-and-recombination process: a CNN co-processor predicts combination weights of sub-control filters, which are then recombined into the final filter. This introduces two limitations:

1. **Pipeline complexity**: Performance depends on the intermediate sub-filter representation, and errors in weight prediction accumulate through the recombination stage
2. **Supervised training requirement**: The co-processor requires labeled target filters for training, necessitating extra offline data preparation

The residual error in an ANC system is:

$$e(n) = d(n) - \sum_{k=0}^{N-1} w_k x'(n-k)$$

where $x'(n) = x(n) * \hat{s}(n)$ is the filtered reference signal and $w_k$ are the control-filter coefficients.

## Methodology

### Overall Framework

The E2E-CFG framework follows a **two-rate structure**: the physical ANC path operates at the sampling rate, while the neural co-processor updates the control filter at the frame rate. For each buffered input frame, the co-processor directly outputs the full control-filter coefficient vector $\mathbf{w} \in \mathbb{R}^N$.

### Transformer-based Co-processor

The co-processor consists of:

1. **Conv1d front-end**: 1 input channel → 256 output channels, kernel size 64, stride 4, padding 30, followed by batch normalization, ReLU, and max pooling (stride 4). Overall temporal downsampling factor: 16.
2. **Positional encoding**: Maximum length 912
3. **Transformer encoder**: $d_\text{model} = 256$, 8 attention heads, 1 encoder layer, feedforward dimension 1024, dropout 0.1, pre-normalization
4. **Output head**: Linear(256→512) → ReLU → Dropout(0.1) → Linear(512→512), producing control filter of length $N = 512$

Total trainable parameters: **1,201,152** (vs. 211,215 for GFANC baseline).

### End-to-End Differentiable Training

The co-processor and ANC forward path are integrated into one differentiable system. The unsupervised training objective is:

$$\mathcal{L} = \frac{1}{T} \sum_{n=0}^{T-1} \alpha_n e^2(n)$$

where $\alpha_n$ follows a forgetting-factor scheme with $\lambda = 0.999$. The full mapping $\mathbf{x}_f \rightarrow \mathbf{w} \rightarrow y(n) \rightarrow e(n) \rightarrow \mathcal{L}$ is differentiable, enabling backpropagation without labeled target filters.

### Key Design Differences from GFANC

| Aspect | GFANC (Luo 2024) | E2E-CFG (Proposed) |
|--------|-------------------|---------------------|
| Co-processor | CNN (Conv1d + residual blocks) | Transformer (Conv1d + self-attention) |
| Filter generation | Weight prediction → sub-filter recombination | Direct coefficient regression |
| Output dimension | $M = 15$ combination weights | $N = 512$ filter coefficients |
| Temporal modeling | Local receptive fields (CNN) | Global dependencies (self-attention) |
| Training | Unsupervised (accumulated error) | Unsupervised (accumulated error) |

## Experimental Setup

| Parameter | E2E-CFG | GFANC | FxNLMS |
|-----------|---------|-------|--------|
| Filter length $N$ | 512 | 512 | 512 |
| Input frame length $L$ | 13,000 | — | — |
| Optimizer | Adam | Adam | — |
| Learning rate | $5 \times 10^{-4}$ | $10^{-2}$ | — |
| Weight decay | $10^{-4}$ | — | — |
| Batch size | 128 | — | — |
| Epochs | 40 | 10 | — |
| LR scheduler | StepLR (step=5, γ=0.5) | StepLR (step=3, γ=0.5) | — |
| Parameters | 1,201,152 | 211,215 | — |
| Step size μ | — | — | 0.001 |
| Training data | 79,977 synthetic band-limited noises (1s, 13 kHz) | Same | — |
| Training SNR | 10 dB additive Gaussian | — | — |

**Test noises**:
- **Real**: aircraft, compressor, genset, handheld drill, large SUV pass-by, mixed aircraft traffic, motorbike, traffic
- **Synthetic**: 20–490 Hz, 490–960 Hz, 20–960 Hz, 1430–1900 Hz

**Evaluation**: NR computed over last 1 s of 5 s run; arithmetic mean over test noises.

## Results

### Noise Reduction on Unseen Noises (dB)

| Category | Noise | GFANC | E2E-CFG | FxNLMS |
|----------|-------|-------|---------|--------|
| Real | Aircraft | 15.88 | **17.83** | 9.17 |
| Real | Compressor | **21.96** | 19.88 | 14.78 |
| Real | Genset | 12.32 | **17.03** | 9.01 |
| Real | Handheld drill | 20.65 | **22.83** | 16.96 |
| Real | Large SUV pass-by | 14.84 | **17.77** | 9.70 |
| Real | Mix aircraft traffic | 13.03 | **16.67** | 8.40 |
| Real | Motorbike | **21.28** | 17.94 | 10.02 |
| Real | Traffic | 13.09 | **16.90** | 10.96 |
| | **Real avg.** | 16.63 | **18.36** | 11.13 |
| Synthetic | 20–490 Hz | **21.24** | 19.35 | 21.15 |
| Synthetic | 490–960 Hz | 13.07 | 15.32 | **21.50** |
| Synthetic | 20–960 Hz | 16.23 | **20.29** | 12.43 |
| Synthetic | 1430–1900 Hz | 14.63 | 19.02 | **21.14** |
| | **Synthetic avg.** | 16.29 | 18.50 | **19.06** |

### Key Findings

1. **Real-noise advantage**: E2E-CFG outperforms GFANC in 6/8 real noise cases and achieves the highest average NR (18.36 dB vs. 16.63 dB). The Transformer's global attention captures non-stationary temporal patterns in real noises more effectively than CNN's local receptive fields.

2. **Synthetic-noise competitiveness**: On synthetic band-limited noises, FxNLMS achieves the highest average NR (19.06 dB). The regular spectral structure of synthetic noises suits FxNLMS's sample-by-sample adaptation.

3. **Time-varying robustness**: Under sequential noise-type changes, E2E-CFG maintains lower NMSE than both baselines across most segments, with visible advantage after abrupt transitions.

4. **Direct generation vs. decomposition**: Removing the sub-filter decomposition stage simplifies the pipeline and avoids error accumulation, but requires the network to regress a higher-dimensional target (512 coefficients vs. 15 weights), potentially requiring more training data.

## Key Contributions

1. **End-to-end control-filter generation**: Directly generates control-filter coefficients for each input frame without sub-filter decomposition and recombination, reducing the gap between generated and optimal filters
2. **Transformer-based unsupervised learning**: Replaces CNN co-processor with Transformer architecture, trained unsupervised by minimizing accumulated residual error without labeled target filters
3. **Generalization to unseen noises**: Under same end-to-end training paradigm with only synthetic noise training, achieves more consistent improvement on unseen real-noise conditions than GFANC baseline

## Related Concepts

- [[../concepts/active-noise-control|Active Noise Control]] — parent domain
- [[../concepts/selective-fixed-filter-anc|Selective Fixed-Filter ANC]] — SFANC/GFANC family of methods
- [[../concepts/generative-fixed-filter-anc|Generative Fixed-Filter ANC]] — GFANC framework that E2E-CFG extends
- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — adaptive baseline (FxNLMS)
- [[../concepts/end-to-end-differentiable-anc|End-to-End Differentiable ANC]] — differentiable training paradigm

## Related Sources

- [[../sources/luo-2026-hybrid-gfanc-fxnlms|Luo 2026: Hybrid GFANC-FxNLMS]] — unsupervised GFANC baseline with CNN co-processor
