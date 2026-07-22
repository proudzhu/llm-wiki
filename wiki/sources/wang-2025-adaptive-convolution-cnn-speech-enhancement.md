---
type: source
created: 2026-07-22
updated: 2026-07-22
sources:
  - raw/papers/wang-2025-adaptive-convolution-cnn-speech-enhancement/full-text.md
  - https://doi.org/10.1109/TASLPRO.2025.3623897
  - zotero://select/items/0_G3J7XJQF
tags:
  - speech-enhancement
  - dynamic-convolution
  - lightweight-model
  - convolutional-recurrent-network
  - adaptive-filtering
  - causal
---

# Wang, Rong, Sun, Hu, Zhu & Lu 2025: Adaptive Convolution for CNN-based Speech Enhancement Models

**Authors**: [[entities/dahan-wang|Dahan Wang]], [[entities/xiaobin-rong|Xiaobin Rong]], [[entities/shiruo-sun|Shiruo Sun]], [[entities/yuxiang-hu|Yuxiang Hu]], [[entities/changbao-zhu|Changbao Zhu]], [[entities/jing-lu|Jing Lu]]
**Affiliations**: Key Laboratory of Modern Acoustics, Nanjing University / NJU-Horizon Intelligent Audio Lab, Horizon Robotics, China
**Venue**: IEEE Transactions on Audio, Speech, and Language Processing, 2025
**Type**: Journal Article
**DOI**: [10.1109/TASLPRO.2025.3623897](https://doi.org/10.1109/TASLPRO.2025.3623897)
**Zotero**: [G3J7XJQF](zotero://select/items/0_G3J7XJQF)

---

## Summary

The paper introduces **adaptive convolution**, a frame-wise causal dynamic convolution module that generates time-varying kernels per STFT frame by aggregating multiple parallel candidate kernels via a lightweight attention mechanism. Applied as a drop-in replacement for vanilla convolutions across diverse CNN-based speech-enhancement (SE) backbones (DPCRN at three scales, DCCRN, [[concepts/gtcrn|GTCRN]], LiSenNet), it yields large quality gains (≈0.1–0.16 PESQ, ≈0.05 DNSMOS-OVRL) at modest MACs increase, with the largest gains on lightweight models. The authors further propose **AdaptCRN**, an ultra-lightweight SE model pairing adaptive convolution with a ConvNeXt/StarNet-inspired encoder-decoder, grouped DPRNN, and ERB-based spectral compression, achieving competitive quality at only **41 MMACs/s and 135K parameters**. A visualization analysis reveals that candidate-kernel selection correlates strongly with speech spectral features (e.g., speaker pitch, speech vs. noise frames), giving an interpretability story absent from prior dynamic-convolution SE work.

## Problem Formulation

Speech enhancement estimates clean speech $s(t)$ from a noisy mixture $x(t)=s(t)+n(t)$. STFT-domain CNN-based SE models predict a mask $M$ (or complex filter) such that $\hat{S}=M\odot X$, where $X=\text{STFT}(x)$. Real-time deployment on edge devices imposes hard constraints on parameters and MACs/s.

Standard **dynamic convolution** (DyConv) from computer vision aggregates a kernel bank with input-dependent attention:

$$\mathbf{W} = \sum_{k=1}^{K} A_k \mathbf{W}_k$$

where $A_k$ is computed by a squeeze-and-excitation block over **global** spatial (frequency-time) statistics. Two issues arise for causal SE:

1. **Non-causality**: GAP aggregates the entire utterance, breaking real-time causality.
2. **Utterance-level kernel**: A single kernel configuration per utterance is suboptimal for highly non-stationary speech — the best kernel for a voiced frame, a noise frame, or a high-pitched vs. low-pitched speaker should differ.

The proposed solution: **frame-wise causal dynamic convolution**, generating per-frame kernels $A_k(t)$ via pooling along frequency only.

## Methodology

### Adaptive Convolution

The adaptive kernel is generated per frame $t$:

$$\mathbf{W}(t) = \sum_{k=1}^{K} A_k(t) \mathbf{W}_k$$

with $K=8$ candidate kernels by default. The candidate kernels $\mathbf{W}_k$ are end-to-end learned and fixed after training; only the per-frame attention $A_k(t)$ varies at inference. This is conceptually analogous to [[concepts/adaptive-filtering|adaptive filtering]] — filter coefficients are adjusted in real time based on input statistics.

![[raw/papers/wang-2025-adaptive-convolution-cnn-speech-enhancement/figures/18f0ac4751b5824aff8ff57e808695ca8b299b6c94ec988018466cb095edd351.jpg|Adaptive convolution architecture]]

*Figure 1(a): Overall architecture of an adaptive convolution layer. The kernel attention module produces per-frame attention weights $A_k(t)$ that aggregate $K$ candidate kernels into a time-varying kernel $\mathbf{W}(t)$.*

### Kernel Attention

Input features $\mathbf{Y}\in\mathbb{R}^{C\times T\times F}$ are compressed along frequency via **power average pooling** to obtain a time-channel energy descriptor:

$$P(c,t) = \frac{1}{F}\sum_{f=0}^{F-1} Y^2(c,t,f)$$

$P$ is then processed through channel modeling + softmax to produce $A_k(t)\in\mathbb{R}^{K\times T}$. Three channel-modeling variants are explored:

| Variant | Mechanism | Params | Best for |
|----------|-----------|--------|----------|
| Single-frame | FC → ReLU → FC (standard SE) | Lowest | Implicit history via upstream layers |
| Multi-frame | 1D-Conv (kernel 3) → ReLU → FC | Medium | Explicit short-range temporal context |
| Temporal (default) | GRU → FC | Highest | Best quality — explicit inter-frame modeling |

The temporal variant using a GRU is the default; it explicitly leverages historical information and yields the best kernel attention.

![[raw/papers/wang-2025-adaptive-convolution-cnn-speech-enhancement/figures/703d9e5fdc643ebbbbd5c7411e9386f2985919895b76ed1436d1103bced26bdd.jpg|Kernel attention]]

*Figure 1(b): Kernel attention module. Frequency pooling produces per-frame energy statistics; channel modeling (single-frame / multi-frame / temporal) then generates per-frame, per-candidate-kernel attention weights.*

### Joint Multi-Layer and Joint Channel/Spatial Attention

For efficient blocks composed of multiple depthwise/pointwise sub-layers (e.g., ConvNeXt blocks), a **joint multi-head attention** mechanism computes kernel attention for all sub-layers simultaneously at the block's start, via a single FC layer with $N\times K$ output channels (where $N$ is the number of sub-layers). This reduces parameters and MACs vs. independent attention per sub-layer.

Inspired by ODConv, joint attention can be extended to also produce per-frame **joint channel attention** $\mathbf{A}^{\mathrm{c}}(t)\in\mathbb{R}^{C_\text{in}}$, $\mathbf{A}^{\mathrm{f}}(t)\in\mathbb{R}^{C_\text{out}}$ and **joint spatial attention** $\mathbf{A}^{\mathrm{s}}(t)\in\mathbb{R}^{K_\mathrm{t}\times K_\mathrm{f}}$:

$$\mathbf{W}(t) = \mathbf{A}^{\mathrm{s}}(t) * \mathbf{A}^{\mathrm{c}}(t) * \mathbf{A}^{\mathrm{f}}(t) * \left[\sum_{k=1}^{K} A_k(t)\mathbf{W}_k\right]$$

### Multi-Frame Parallelism

Causal per-frame kernels break naive batched convolution across time. Two solutions:

1. **Output aggregation** (training only): Compute each candidate kernel's output in parallel, then weight-sum — mathematically equivalent but costs $\sim K\times$ MACs.
2. **Grouped convolution** (train + inference): Unfold along time with kernel size $K_\mathrm{t}$, merge batch+time into channels, divide into $B\times T$ groups, and apply the per-frame assembled kernels. No MACs increase.

### AdaptCRN

AdaptCRN is an ultra-lightweight SE model built around adaptive convolution. Architecture (see Figure 2):

![[raw/papers/wang-2025-adaptive-convolution-cnn-speech-enhancement/figures/03ca36f6ebb8b19d3592f61a091b70149251d58740dea042a6150304a3e9eabb.jpg|AdaptCRN architecture]]

*Figure 2: AdaptCRN. (a) Overall architecture: spectral compression → 5 adaptive-block encoder → 2 grouped DPRNN → 5 adaptive-block decoder → spectral decompression. (b) Basic block (ConvNeXt/StarNet-inspired: LN → DW Conv → PW Conv → GELU → PW Conv). (c) Adaptive block: basic block with joint multi-layer + channel attention.*

- **Spectral compression**: ERB-based frequency downsampling (65 low-frequency bins kept, 192 high-frequency bins → 64 ERB bands) + dynamic range compression (log for magnitude, power-law exponent 0.7 for real/imag), followed by SFE (subband feature extraction) producing 9-channel 129-D features per frame.
- **Encoder/Decoder**: 5 adaptive blocks each. Hidden channels = 16 (reduced to 4 in the final block's middle PW Conv). Conv kernel sizes $(K_\mathrm{t}, K_\mathrm{f})$: $(1,5)$ for the first two encoder layers (stride 2 in frequency), $(3,3)$ for the rest. Decoder mirrors, with the last two layers using depthwise transposed convolutions.
- **Bottleneck**: 2 grouped [[concepts/dprnn|DPRNN]] modules (2 groups, 33-D frequency dimension; intra-frame GRU hidden = 8, inter-frame GRU hidden = 16). Representation rearrangement after grouped RNN is removed (the FC layer performs inter-group fusion).
- **Output**: spectral magnitude mask (not CRM) via a learnable sigmoid activation; for trained ultra-lightweight models, the imaginary part of a CRM is observed to be near-zero, making CRM ≈ magnitude mask.
- **Skip connections** between encoder/decoder layers.

### Loss Function

Combined SI-SNR + power-compressed spectral losses:

$$\mathcal{L} = \lambda_1 \mathcal{L}_\text{SI-SNR} + \lambda_2 \mathcal{L}_\text{mag} + \lambda_3 (\mathcal{L}_\text{real} + \mathcal{L}_\text{imag})$$

with $\lambda_1=0.01$, $\lambda_2=0.7$, $\lambda_3=0.3$. Magnitude MSE uses compression exponent 0.3; real/imag MSE uses exponent 0.7 (compressing by $|S|^{0.7}$). See [[concepts/power-law-compression|Power-Law Compression]].

## Experimental Setup

| Dataset | Training samples | Test samples | SNR range | Sampling rate |
|---------|-----------------|--------------|-----------|---------------|
| DNS5 | ~200 h, 10 s clips | 1,000 samples | -5 to 15 dB | 16 kHz |
| Voicebank+DEMAND ([[concepts/voicebank-demand|VCTK-DEMAND]]) | 11,572 utterances (28 speakers) | 872 utterances (2 speakers) | 0/5/10/15 dB train; 2.5/7.5/12.5/17.5 dB test | 16 kHz |

**Implementation**:
- STFT: 32 ms window, 50% overlap (16 ms hop), 512-FFT, sqrt-Hanning
- Adaptive convolution: $K=8$ candidate kernels, channel-modeling hidden = 32, 1D-Conv kernel = 3 (multi-frame variant)
- Optimizer: Adam, initial LR 0.001, halved at epochs 120/150/170/180/190/200 (DNS5); cosine annealing over 300 epochs (VCTK-DEMAND)
- Batch size: 8; 10,000 samples/epoch (DNS5)
- Loss weights: $\lambda_1=0.01$, $\lambda_2=0.7$, $\lambda_3=0.3$
- Metrics: SI-SNR, PESQ, ESTOI/STOI, DNSMOS (SIG/BAK/OVRL)

**Baselines for ablation/generalization**: DPCRN-light/middle/large (own scaled versions), [[concepts/gtcrn|GTCRN]], LiSenNet, DCCRN. For AdaptCRN comparison: DPCRN-light, GTCRN, LiSenNet, DeepFilterNet, ULCNet, FSPEN.

## Results

### Ablation: Kernel Attention (DPCRN-light, DNS5)

| Variant | Para. (K) | MACs (M) | SI-SNR | ESTOI | PESQ | DNSMOS-OVRL |
|---------|-----------|----------|--------|-------|------|-------------|
| Vanilla convolution | 80.78 | 194.57 | 14.431 | 0.752 | 2.313 | 2.910 |
| Global dynamic conv (non-causal) | 358.62 | 194.88 | 15.060 | 0.758 | 2.410 | 2.924 |
| Single-frame channel modeling | 358.62 | 210.45 | 14.924 | 0.761 | 2.390 | 2.946 |
| Multi-frame channel modeling | 378.21 | 211.68 | 14.956 | 0.762 | 2.406 | 2.957 |
| **Temporal channel modeling (default)** | 410.21 | 213.80 | **15.147** | 0.765 | **2.427** | 2.964 |
| + Joint channel attention | 426.71 | 214.84 | 15.177 | 0.766 | 2.445 | **2.974** |
| + Joint spatial attention | 412.45 | 213.94 | 15.133 | 0.766 | 2.427 | 2.971 |
| + Joint channel/spatial | 428.95 | 214.98 | **15.192** | **0.766** | **2.445** | 2.970 |

**Key findings**:
- Any channel modeling beats vanilla by ≈0.1 PESQ / 0.05 DNSMOS-OVRL at modest MACs increase.
- Temporal (GRU) channel modeling > multi-frame > single-frame, justifying the default.
- Joint channel attention helps; joint spatial attention alone does not.
- Non-causal global dynamic convolution matches single-frame but is inferior to multi-frame and temporal variants — frame-level adjustment matters even when global (non-causal) information is available.

### Generalization Across Backbones (DNS5)

| Model | Conv | Para. (K) | MACs (M) | SI-SNR | PESQ | DNSMOS-OVRL |
|-------|------|-----------|----------|--------|------|-------------|
| GTCRN | Vanilla | 23.67 | 33.83 | 13.552 | 2.130 | 2.838 |
| GTCRN | Adaptive | 117.36 | 40.75 | 14.296 | 2.292 | 2.887 |
| LiSenNet | Vanilla | 36.78 | 55.77 | 14.352 | 2.244 | 2.897 |
| LiSenNet | Adaptive | 198.94 | 62.57 | 15.003 | 2.369 | 2.963 |
| DPCRN-light | Vanilla | 80.78 | 194.57 | 14.431 | 2.313 | 2.910 |
| DPCRN-light | Adaptive | 410.21 | 213.80 | 15.147 | 2.427 | 2.964 |
| DPCRN-middle | Adaptive | 1440.29 | 809.77 | 15.948 | 2.582 | 3.030 |
| DPCRN-large | Adaptive | 2455.01 | 1829.54 | 16.139 | 2.621 | 3.040 |
| DCCRN | Adaptive | 22449.07 | 8235.08 | 15.208 | 2.526 | 3.027 |

**Key findings**:
- Adaptive convolution helps most for **lightweight models** (GTCRN +0.16 PESQ, LiSenNet +0.12), where the limited parameter space benefits most from dynamic kernel expansion.
- Gains **diminish for larger models** (DPCRN-large +0.02 PESQ) because their kernels already cover diverse spectral features.
- For DCCRN (3.67M params), adaptive convolution inflates params 6× and MACs 1.5× — prohibitively costly, since convolutions already account for >97% of MACs. **Applicability is limited in large models**.

### AdaptCRN Performance (DNS5)

| Model | Para. (K) | MACs (M) | SI-SNR | ESTOI | PESQ | DNSMOS-OVRL |
|-------|-----------|----------|--------|-------|------|-------------|
| DPCRN-light | 80.78 | 194.57 | 14.431 | 0.752 | 2.313 | 2.910 |
| GTCRN | 23.67 | 33.83 | 13.552 | 0.727 | 2.130 | 2.838 |
| GTCRN-Adaptive | 117.36 | 40.75 | 14.296 | 0.747 | 2.292 | 2.887 |
| LiSenNet | 36.78 | 55.77 | 14.352 | 0.742 | 2.244 | 2.897 |
| **AdaptCRN** | **134.51** | **40.80** | **14.892** | **0.759** | **2.387** | **2.939** |

### AdaptCRN Performance (Voicebank+DEMAND)

| Model | Para. (K) | MACs (M) | SI-SNR | STOI | PESQ |
|-------|-----------|----------|--------|------|------|
| DeepFilterNet | 1780 | 350 | 16.63 | 0.942 | 2.81 |
| GTCRN | 24 | 34 | 18.83 | 0.940 | 2.87 |
| ULCNet | 688 | 98 | 17.20 | — | 2.87 |
| FSPEN | 79 | 89 | — | 0.942 | 2.97 |
| LiSenNet* | 37 | 56 | — | 0.937 | 2.95 |
| **AdaptCRN** | **135** | **41** | **18.82** | **0.940** | **2.98** |

\* LiSenNet trained without PESQ loss for fair comparison.

**Key findings**: AdaptCRN matches or exceeds much larger baselines (DeepFilterNet 13× more MACs, ULCNet 2.4× more MACs and 5× more params). On VCTK-DEMAND it achieves the best PESQ (2.98) among all compared models. GTCRN-Adaptive (same params/MACs as AdaptCRN) performs significantly worse, validating AdaptCRN's additional structural design choices.

### AdaptCRN Ablation (DNS5)

| Variant | Para. (K) | MACs (M) | SI-SNR | PESQ | DNSMOS-OVRL |
|---------|-----------|----------|--------|------|-------------|
| AdaptCRN | 134.51 | 40.80 | 14.892 | 2.387 | 2.939 |
| w/o Adaptive convolution | 29.44 | 33.67 | 13.826 | 2.192 | 2.872 |
| w/o Joint channel attention | 124.68 | 40.18 | 14.718 | 2.352 | 2.925 |
| w/o Joint multi-layer kernel attention | 169.21 | 43.19 | 14.803 | 2.386 | 2.939 |
| w/o Dynamic range compression | 134.51 | 40.80 | 14.695 | 2.342 | 2.929 |
| DW(8)-PW(8)-skip-PW(8) (no mid activation) | 134.51 | 40.01 | 14.672 | 2.358 | 2.931 |
| DW(8)-PW(8) (single PW, K=8) | 112.88 | 32.06 | 14.551 | 2.343 | 2.926 |
| DW(8)-PW(64) (single PW, K=64) | 255.00 | 41.41 | 14.826 | 2.390 | 2.942 |

Adaptive convolution alone contributes nearly 1 dB SI-SNR, 0.19 PESQ, 0.06+ DNSMOS-OVRL for ≈7M MACs increase. The nonlinearity introduced by adaptive convolution means cascading two adaptive PW Convs with $K=8$ is **not** equivalent to a single PW Conv (unlike vanilla); it is equivalent to a single layer with $K^2=64$ kernels in a low-rank subspace, so the original AdaptCRN achieves DW(8)-PW(64)-comparable quality with far fewer redundant parameters.

### Kernel Allocation vs. Speech Features

Visualization of the kernel attention weights from the third decoder layer of DPCRN-light with adaptive convolution reveals a strong correlation between candidate-kernel selection and signal characteristics:

- **Speaker-dependent**: One candidate kernel dominates for the high-pitched speaker; kernels 2–5 dominate for the lower-pitched speaker.
- **Noise-specialized**: Kernels 6–8 are predominantly activated during pure noise segments (both in speech-internal pauses and pure noise regions), functioning as **noise-specialized filters**.
- **Quantitative**: Across the DNS5 test set, in non-speech frames, kernels 6–8 dominate; in speech frames, all 8 kernels have notable selection probability (because speech frames still contain noise components and short pauses).

![[raw/papers/wang-2025-adaptive-convolution-cnn-speech-enhancement/figures/979114c3ecf4f8517d34c6a201db4da34c800577b54e76b2062c37e8693a9380.jpg|Kernel attention vs. speech features]]

*Figure 5: Proportion of frames where the k-th candidate kernel is selected as the dominant kernel, separated for speech vs. non-speech frames (VAD-based). Kernels 6–8 specialize in noise-related features.*

## Key Contributions

1. **Adaptive convolution**: A frame-wise causal dynamic convolution module generating per-frame kernels via lightweight frequency-pooled attention, explicitly leveraging historical information (single-frame / multi-frame / temporal channel modeling). A generalization of [[concepts/dynamic-convolution|dynamic convolution]] adapted to causal streaming SE, distinct from CV's per-pixel adaptive convolution.
2. **Joint multi-layer and joint channel/spatial attention**: A multi-head extension computing kernel attention for all sub-layers of a block simultaneously, plus optional joint channel and spatial attention inspired by ODConv — reduces parameters and MACs vs. independent per-layer attention.
3. **Multi-frame parallelism**: Two techniques (training-only output aggregation, and grouped-convolution-based unfolding that supports both training and inference) to enable parallel computation across frames despite per-frame causal kernels.
4. **Generalization across CNN backbones**: Drop-in replacement verified on DPCRN (3 scales), DCCRN, GTCRN, LiSenNet — significant gains especially for lightweight models, with diminishing returns and prohibitive cost for very large models.
5. **AdaptCRN**: An ultra-lightweight SE model pairing adaptive convolution with a ConvNeXt/StarNet-inspired encoder-decoder, grouped DPRNN, and ERB-based spectral compression. Achieves PESQ 2.98 on VCTK-DEMAND and PESQ 2.387 / SI-SNR 14.89 dB on DNS5 at **41 MMACs/s and 135K parameters**, outperforming models with 2–13× more compute.
6. **Interpretability of kernel allocation**: First explicit demonstration in dynamic-convolution SE that candidate-kernel selection correlates with speaker pitch and speech/noise activity — providing an interpretability story absent from prior SE dynamic-convolution work (DGCN).
7. **CV→SE transfer failures documented**: Temperature annealing and softmax normalization — both recommended in CV DyConv — are shown to provide no benefit in SE; these findings justify retaining softmax for interpretability but not for optimization.

## Related Concepts

- [[concepts/adaptive-convolution|Adaptive Convolution]] — the central contribution, detailed on its own page
- [[concepts/adaptcrn|AdaptCRN]] — the proposed ultra-lightweight model, detailed on its own page
- [[concepts/dynamic-convolution|Dynamic Convolution]] — the CV ancestor generalized by adaptive convolution
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — the broader CRN family (CRN → DCCRN → DPCRN → GTCRN → AdaptCRN)
- [[concepts/gtcrn|GTCRN]] — key baseline; same lab; GTCRN-Adaptive is an explicit comparison point in Table V
- [[concepts/dprnn|Dual-Path RNN (DPRNN)]] — AdaptCRN uses grouped DPRNN bottleneck
- [[concepts/grouped-recurrent-neural-network|Grouped Recurrent Neural Network]] — AdaptCRN's grouped DPRNN inherits this efficiency pattern
- [[concepts/erb-scale|ERB Scale]] — AdaptCRN's spectral compression uses ERB-based band merging
- [[concepts/power-law-compression|Power-Law Compression]] — AdaptCRN uses exponent 0.7 for real/imag compression
- [[concepts/adaptive-filtering|Adaptive Filtering]] — conceptual analogy: adaptive convolution adjusts filter coefficients per frame based on input statistics
- [[concepts/voice-activity-detection|Voice Activity Detection]] — used in the kernel-allocation interpretability analysis

## Related Synthesis

- [[synthesis/computational-efficiency-evolution|Computational Efficiency Evolution]] — AdaptCRN is a new Pareto point on the ultra-lightweight SE frontier (41 MMACs/s, 135K params); adaptive convolution adds a "dynamic capacity" axis (params ↑, MACs ≈ flat) to the existing efficiency-strategy taxonomy
