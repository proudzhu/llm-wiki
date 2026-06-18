---
type: source
created: 2026-06-18
updated: 2026-06-18
sources:
  - raw/papers/zhao-2026-halo-half-frame-rate-adaptive-operator/full-text.md
  - https://doi.org/10.48550/arXiv.2606.12328
  - zotero://select/items/0_WQLLU8C4
tags:
  - speech-enhancement
  - lightweight-model
  - stft-processing
  - temporal-redundancy
  - dynamic-convolution
  - arxiv-2026
---

# Zhao, Wang, Sun, Yang, Rong, Sun, Hu & Lu 2026: HALO — Half-frame-rate Adaptive Learnable Operator

**Authors**: [[entities/jiadong-zhao|Jiadong Zhao]], [[entities/dahan-wang|Dahan Wang]], [[entities/yu-sun|Yu Sun]], [[entities/leyan-yang|Leyan Yang]], [[entities/xiaobin-rong|Xiaobin Rong]], [[entities/shiruo-sun|Shiruo Sun]], [[entities/yuxiang-hu|Yuxiang Hu]], [[entities/jing-lu|Jing Lu]]
**Affiliations**: Key Laboratory of Modern Acoustics & Institute of Acoustics, Nanjing University; NJU-Horizon Intelligent Audio Lab, Horizon Robotics; Samsung Electronics (China)
**Venue**: arXiv preprint, June 2026
**Type**: preprint
**DOI**: [10.48550/arXiv.2606.12328](https://doi.org/10.48550/arXiv.2606.12328)
**Zotero**: [Open in Zotero](zotero://select/items/0_WQLLU8C4)

## Summary

HALO (Half-frame-rate Adaptive Learnable Operator) is a causal plug-in module for lightweight STFT-based speech enhancement that reduces the internal frame rate processed by a backbone network without altering the STFT/ISTFT procedure. By halving the frame rate via adaptive dynamic-convolution-based rate reduction and restoration operators, HALO reduces backbone computational cost with no added algorithmic latency, freeing budget for channel widening. Evaluated on the DNS3 dataset across GTCRN, DPCRN, LiSenNet, and UL-UNAS, HALO consistently improves objective metrics (PESQ, ESTOI, SI-SNR) under matched complexity.

## Problem Formulation

Monaural speech enhancement in the time-frequency domain models the observed signal in the time domain as:

$$x(t) = s(t) + n(t)$$

where $s(t)$ is clean speech and $n(t)$ is additive distortion. Applying STFT yields complex spectrograms:

$$X = [\Re\{X\}; \Im\{X\}] \in \mathbb{R}^{2 \times T \times F}$$

$$X(t,f) = S(t,f) + N(t,f)$$

The objective is to estimate enhanced spectrum $\hat{S}$ from $X$, with ISTFT reconstructing the enhanced waveform $\hat{s}$.

**Key insight**: STFT with 50% overlap (standard in speech enhancement) makes adjacent frames share many time-domain samples, creating strong temporal correlation. This overlap-induced redundancy means a backbone network wastes computation processing highly similar adjacent frames. Simply removing overlap degrades performance — a trade-off that HALO addresses by *adaptively compressing* the redundant frame sequence rather than discarding information.

## Methodology

### HALO Framework

HALO consists of two adaptive learnable operators positioned around a backbone enhancement network:

![[raw/papers/zhao-2026-halo-half-frame-rate-adaptive-operator/figures/Fig1.png|HALO overall framework]]

*Figure 1: HALO inserts a rate-reduction operator $D(\cdot)$ before the backbone and a rate-restoration operator $U(\cdot)$ after. The backbone processes at half the original frame rate, reducing compute with no algorithmic latency.*

1. **Rate reduction** $D(\cdot)$: Compresses the input sequence from $T$ to $\lceil T/2\rceil$ frames
2. **Backbone processing** $f_\theta(\cdot)$: Operates on the shortened sequence
3. **Rate restoration** $U(\cdot)$: Expands each half-rate frame back to two adjacent frames on the original STFT grid

$$X_{T/2} = D(X) \in \mathbb{R}^{2 \times \lceil T/2 \rceil \times F}$$
$$\hat{S}_{T/2} = f_\theta(X_{T/2}) \in \mathbb{R}^{2 \times \lceil T/2 \rceil \times F}$$
$$\hat{S} = U(\hat{S}_{T/2}) \in \mathbb{R}^{2 \times T \times F}$$

### Frame-Rate Reduction Operator

For each reduced-time index $l$, the operator forms a two-frame paired feature by concatenating adjacent frames:

$$\tilde{X}(:,l,f) = \text{cat}(X(:,2l-1,f), X(:,2l,f)) \in \mathbb{R}^{4}$$

This is mapped to a half-frame-rate representation $\mathbb{R}^{2}$ via dynamic convolution with lightweight gating:

![[raw/papers/zhao-2026-halo-half-frame-rate-adaptive-operator/figures/Fig2.png|Adaptive learnable rate-reduction operator]]

*Figure 2: The rate-reduction operator uses a kernel bank $\{W_k\}_{k=1}^K$ with T-F-dependent mixture weights predicted by a gating network $g_d(\cdot)$.*

The operator maintains a kernel bank $\{W_k\}_{k=1}^K$, $W_k \in \mathbb{R}^{4 \times 2}$, and predicts T-F-dependent mixture weights:

$$\alpha(l,f) = g_d(\tilde{X}(:,l,f)), \quad \sum_{k=1}^K \alpha_k(l,f) = 1, \quad \alpha_k(l,f) \geq 0$$

The gating network $g_d(\cdot)$ consists of two pointwise convolutions and a PReLU nonlinearity, followed by softmax over the $K=5$ kernel indices. The reduced feature is:

$$X_{T/2}(:,l,f) = \sum_{k=1}^K \alpha_k(l,f)\, W_k \tilde{X}(:,l,f)$$

### Frame-Rate Restoration Operator

The restoration operator $U(\cdot)$ reconstructs the full-rate sequence from the half-rate backbone output. It uses the same kernel-bank and gated design (with $V_k \in \mathbb{R}^{2 \times 4}$, $K=5$):

$$\beta(l,f) = g_u(\hat{S}_{T/2}(:,l,f)), \quad \sum_{k=1}^K \beta_k(l,f) = 1, \quad \beta_k(l,f) \geq 0$$

The restored two-frame pair is formed at each bin:

$$\tilde{S}(:,l,f) = \sum_{k=1}^K \beta_k(l,f)\, V_k \hat{S}_{T/2}(:,l,f) \in \mathbb{R}^{4}$$

This is split into two complex frames:

$$\hat{S}(:,2l,f) = \tilde{S}(1:2,l,f), \quad \hat{S}(:,2l+1,f) = \tilde{S}(3:4,l,f)$$

**Causality**: The reduction at index $l$ depends only on $X(:,2l-1,:)$ and $X(:,2l,:)$; restoration produces $\hat{S}(:,2l,:)$ and $\hat{S}(:,2l+1,:)$ solely from $\hat{S}_{T/2}(:,l,:)$ without accessing future input — no added algorithmic latency.

## Experimental Setup

| Parameter | Setting |
|-----------|---------|
| Dataset | DNS3 + DiDiSpeech (Mandarin) |
| Training pairs | 72,000 (10-second noisy-clean) |
| Validation / Test pairs | 840 / 800 |
| SNR range | −5 to 15 dB |
| Sampling rate | 16 kHz |
| STFT window | 32 ms square-root Hann |
| Hop length | 16 ms (50% overlap) |
| FFT length | 512 |
| Dynamic conv kernels (K) | 5 |
| Gating hidden channels | 8 |
| Optimizer | Adam |
| Initial learning rate | 0.001 |
| LR schedule | Halved on 10-epoch validation plateau |
| Batch size | 8 |
| Training loss | Same as GTCRN |
| Backbones tested | GTCRN, DPCRN (ultralight/light/middle/large), LiSenNet, UL-UNAS |

**Complexity matching**: When inserting HALO, backbone channel width is widened so the combined model operates at similar MAC/s to the baseline — isolating HALO's effect under comparable computational budget.

## Results

### Ablation Study (GTCRN backbone)

| Variant | Para. (k) | MAC/s (M) | PESQ | ESTOI | SI-SNR | OVRL |
|---------|-----------|-----------|------|-------|--------|------|
| Noisy | — | — | 1.406 | 0.669 | 5.610 | 1.628 |
| GTCRN (baseline) | 23.67 | 33.83 | 2.101 | 0.754 | 11.390 | 2.629 |
| No-overlap STFT | 47.30 | 31.84 | 1.783 | 0.722 | 10.960 | 2.512 |
| D-FixedRed + U-FixedRest | 47.40 | 32.02 | 2.118 | 0.758 | 11.620 | 2.663 |
| D-Decimate + U-FixedRest | 47.32 | 32.70 | 2.104 | 0.755 | 11.510 | 2.600 |
| D-Decimate + U-Duplicate | 47.30 | 32.60 | 2.086 | 0.752 | 11.400 | 2.568 |
| HALO (w/o channel widening) | 24.07 | 22.05 | 2.093 | 0.754 | 11.430 | 2.625 |
| **HALO (w/ channel widening)** | **46.87** | **32.85** | **2.198** | **0.769** | **11.900** | **2.673** |

Key ablation findings:
- Removing overlap entirely (**no-overlap STFT**) causes severe degradation — overlap cannot be trivially discarded
- **D-FixedRed + U-FixedRest**: Without adaptive gating, performance drops below HALO
- **D-Decimate + U-FixedRest**: Replacing learnable reduction with simple decimation weakens results
- **D-Decimate + U-Duplicate**: Simplest variant (decimate + duplicate) gives the worst performance among HALO-like designs
- **HALO w/o widening**: Reduces MAC/s by ~35% (33.83 → 22.05 M) while maintaining near-baseline quality
- **HALO w/ widening**: Best overall — PESQ +0.097, SI-SNR +0.51 dB vs. baseline at matched MAC/s

### Comparison Across Backbones

| Model | MAC/s (M) | PESQ | ESTOI | SI-SNR | OVRL |
|-------|-----------|------|-------|--------|------|
| GTCRN-50% | 33.83 | 2.101 | 0.754 | 11.390 | 2.629 |
| + HALO | 32.85 | **2.198** | **0.769** | **11.900** | **2.673** |
| GTCRN-75% | 67.66 | 2.121 | 0.756 | 11.370 | 2.639 |
| + HALO | 65.49 | **2.237** | **0.772** | **11.990** | **2.674** |
| DPCRN-ultralight | 31.80 | 2.025 | 0.750 | 11.070 | 2.597 |
| + HALO | 31.34 | **2.212** | **0.771** | **11.920** | **2.648** |
| DPCRN-light | 59.84 | 2.146 | 0.764 | 11.550 | 2.631 |
| + HALO | 61.48 | **2.247** | **0.778** | **12.100** | **2.657** |
| DPCRN-middle | 225.11 | 2.340 | 0.788 | 12.350 | 2.713 |
| + HALO | 223.45 | **2.402** | **0.796** | **12.670** | **2.708** |
| DPCRN-large | 872.09 | 2.522 | 0.807 | 13.130 | 2.777 |
| + HALO | 869.86 | **2.536** | **0.809** | **13.150** | **2.766** |
| LiSenNet | 55.77 | 2.177 | 0.762 | 11.760 | 2.681 |
| + HALO | 55.76 | **2.275** | **0.778** | **12.390** | **2.703** |
| UL-UNAS | 33.61 | 2.245 | 0.773 | 12.100 | 2.681 |
| + HALO | 31.26 | **2.261** | **0.777** | **12.240** | **2.684** |

HALO improves all metrics across all tested architectures. The gain magnitude depends on backbone capacity:
- **Smaller backbones** (GTCRN, DPCRN-ultralight, DPCRN-light): Larger improvements — these models spend a higher fraction of compute on overlapping frames, so HALO's redundancy reduction is most effective
- **Larger backbones** (DPCRN-large): Gains diminish as additional channels from widening are less effective once capacity is already large
- **Highly optimized backbones** (UL-UNAS): Modest gains — the NAS-optimized architecture already minimizes redundancy, leaving less headroom

## Key Contributions

1. **HALO module**: A causal, plug-in module that halves the internal frame rate processed by the backbone without modifying the STFT/ISTFT procedure or adding algorithmic latency
2. **Adaptive learnable operators**: Rate-reduction and rate-restoration operators based on lightweight dynamic convolutions with T-F-dependent gating, enabling content-aware temporal compression
3. **Overlap-induced redundancy framework**: Systematic identification and exploitation of temporal redundancy from STFT overlap — a bottleneck orthogonal to architectural slimming
4. **Broad compatibility**: Demonstration across 4 backbone families (GTCRN, DPCRN, LiSenNet, UL-UNAS) with 8 total configurations, showing consistent gains at matched computational cost
5. **Practical streaming suitability**: Causality-preserving design with no lookahead, suitable for real-time edge deployment

## Related Concepts

- [[concepts/gtcrn|Grouped Temporal Convolutional Recurrent Network (GTCRN)]]
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network (CRN/DPCRN)]]
- [[concepts/spectrogram-analysis|Spectrogram Analysis & STFT]]
- [[concepts/dprnn|Dual-Path RNN (DPRNN)]]
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[concepts/attention-gate|Attention Gate / Gating Mechanisms]]
- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]

## Related Synthesis

- [[synthesis/multi-modal-speech-enhancement|Multi-Modal Speech Enhancement]]
- [[synthesis/computational-efficiency-evolution|Computational Efficiency Evolution]]
