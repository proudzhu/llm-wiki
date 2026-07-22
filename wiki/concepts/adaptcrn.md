---
type: concept
created: 2026-07-22
updated: 2026-07-22
sources:
  - raw/papers/wang-2025-adaptive-convolution-cnn-speech-enhancement/full-text.md
tags:
  - neural-network
  - speech-enhancement
  - lightweight-model
  - convolutional-recurrent-network
  - adaptive-convolution
---

# AdaptCRN

**AdaptCRN** (Adaptive Convolutional Recurrent Network) is an ultra-lightweight speech-enhancement model proposed by Wang et al. (IEEE TASLPRO 2025). It pairs [[concepts/adaptive-convolution|adaptive convolution]] with a ConvNeXt/StarNet-inspired encoder-decoder, [[concepts/grouped-recurrent-neural-network|grouped]] [[concepts/dprnn|DPRNN]] bottleneck, and [[concepts/erb-scale|ERB]]-based spectral compression to achieve competitive SE quality at **41 MMACs/s and 135K parameters** — outperforming much larger baselines (e.g., DeepFilterNet at 350 MMACs/s, ULCNet at 98 MMACs/s) on the Voicebank+DEMAND benchmark.

## Architecture

![[raw/papers/wang-2025-adaptive-convolution-cnn-speech-enhancement/figures/03ca36f6ebb8b19d3592f61a091b70149251d58740dea042a6150304a3e9eabb.jpg|AdaptCRN architecture]]

*Figure: (a) AdaptCRN overall architecture. (b) Basic block (ConvNeXt/StarNet-inspired). (c) Adaptive block — basic block + joint multi-layer + channel attention.*

AdaptCRN operates in the STFT domain. Pipeline:

1. **Input**: spectral magnitude + real + imaginary parts of the noisy spectrum.
2. **Spectral compression**: ERB-based frequency downsampling (65 low-frequency bins below 2 kHz kept; 192 high-frequency bins → 64 ERB bands) + dynamic-range compression (log for magnitude, [[concepts/power-law-compression|power-law]] exponent 0.7 for real/imag) → 129-D compressed features. SFE (subband feature extraction, kernel 3) produces 9-channel 129-D features per frame.
3. **Encoder**: 5 adaptive blocks. Hidden channels = 16 (final block middle PW Conv reduced to 4). Encoder conv kernel sizes: $(1,5)$ with frequency stride 2 for the first two layers; $(3,3)$ with stride 1 for the last three.
4. **Bottleneck**: 2 grouped DPRNN modules (2 groups, 33-D frequency dimension). Intra-frame GRU hidden = 8; inter-frame GRU hidden = 16. Representation rearrangement after grouped RNN is removed — the FC layer inherently performs inter-group fusion, and rearrangement is mathematically equivalent to permuting FC weight rows.
5. **Decoder**: 5 adaptive blocks mirroring the encoder; the last two layers use depthwise transposed convolutions to restore frequency resolution.
6. **Spectral decompression**: Transpose of the downsampling matrix (non-learnable).
7. **Output**: spectral **magnitude** mask via a learnable sigmoid. For trained ultra-lightweight models, the imaginary part of a complex ratio mask is observed to be near-zero, making CRM ≈ magnitude mask — so AdaptCRN skips CRM.
8. **Skip connections** between corresponding encoder/decoder layers.

### Basic Block (ConvNeXt/StarNet-inspired)

- Layer normalization along channel and frequency dimensions (smooths energy distribution, preserves spectral patterns).
- DW Conv → PW Conv → GELU → PW Conv (with BN + PReLU after DW Conv and the second PW Conv).
- A StarNet-style "star operation" $f_\text{ReLU6}(x) * x$ was tried as the middle activation but offered no advantage over GELU.
- Skip connection when no frequency downsampling and input/output channels match.

### Adaptive Block

The basic block augmented with **joint attention** that simultaneously produces:
- Adaptive kernel attention weights for all three sub-layers (multi-head FC with $N\times K$ outputs, $N=3$, $K=8$).
- Input and output temporal channel attention maps (applied to features entering and leaving the block, not per-kernel).

## Loss Function

Combined SI-SNR + power-compressed spectral losses:

$$\mathcal{L} = \lambda_1 \mathcal{L}_\text{SI-SNR} + \lambda_2 \mathcal{L}_\text{mag} + \lambda_3 (\mathcal{L}_\text{real} + \mathcal{L}_\text{imag})$$

with $\lambda_1=0.01$, $\lambda_2=0.7$, $\lambda_3=0.3$. Magnitude MSE uses compression exponent 0.3; real/imag MSE uses exponent 0.7. Same multi-domain loss family as [[concepts/gtcrn|GTCRN]] and [[concepts/cofi-lite|CoFi-Lite]] (same lab lineage).

## Results

### Voicebank+DEMAND (VCTK-DEMAND)

| Model | Para. (K) | MACs (M) | SI-SNR | STOI | PESQ |
|-------|-----------|----------|--------|------|------|
| DeepFilterNet | 1780 | 350 | 16.63 | 0.942 | 2.81 |
| GTCRN | 24 | 34 | 18.83 | 0.940 | 2.87 |
| ULCNet | 688 | 98 | 17.20 | — | 2.87 |
| FSPEN | 79 | 89 | — | 0.942 | 2.97 |
| LiSenNet* | 37 | 56 | — | 0.937 | 2.95 |
| **AdaptCRN** | **135** | **41** | **18.82** | **0.940** | **2.98** |

\* LiSenNet trained without PESQ loss for fair comparison.

### DNS5

| Model | Para. (K) | MACs (M) | SI-SNR | ESTOI | PESQ | DNSMOS-OVRL |
|-------|-----------|----------|--------|-------|------|-------------|
| DPCRN-light | 80.78 | 194.57 | 14.431 | 0.752 | 2.313 | 2.910 |
| GTCRN | 23.67 | 33.83 | 13.552 | 0.727 | 2.130 | 2.838 |
| GTCRN-Adaptive | 117.36 | 40.75 | 14.296 | 0.747 | 2.292 | 2.887 |
| LiSenNet | 36.78 | 55.77 | 14.352 | 0.742 | 2.244 | 2.897 |
| **AdaptCRN** | **134.51** | **40.80** | **14.892** | **0.759** | **2.387** | **2.939** |

AdaptCRN matches GTCRN's compute (40.8 vs 33.8 MMACs/s) with 5.7× more parameters, but achieves substantially better quality. Comparing to GTCRN-Adaptive (same params/MACs as AdaptCRN) shows AdaptCRN's additional structural design choices (joint attention, grouped DPRNN, spectral compression) contribute significant gains over simply dropping adaptive convolution into GTCRN.

## Ablation Highlights

| Variant | SI-SNR | PESQ | DNSMOS-OVRL |
|---------|--------|------|-------------|
| AdaptCRN | 14.892 | 2.387 | 2.939 |
| w/o Adaptive convolution | 13.826 | 2.192 | 2.872 |
| w/o Joint channel attention | 14.718 | 2.352 | 2.925 |
| w/o Joint multi-layer kernel attention | 14.803 | 2.386 | 2.939 |
| w/o Dynamic range compression | 14.695 | 2.342 | 2.929 |
| DW(8)-PW(8)-skip-PW(8) (no mid activation) | 14.672 | 2.358 | 2.931 |
| DW(8)-PW(8) (single PW, K=8) | 14.551 | 2.343 | 2.926 |
| DW(8)-PW(64) (single PW, K=64) | 14.826 | 2.390 | 2.942 |

Adaptive convolution alone contributes ≈1 dB SI-SNR, 0.19 PESQ, 0.06+ DNSMOS-OVRL for ~7M MACs. Joint multi-layer attention matches independent per-layer attention quality with 30K+ fewer parameters. The DW(8)-PW(64) row confirms the analysis in [[concepts/adaptive-convolution|Adaptive Convolution]]: cascading two adaptive PW Convs with $K=8$ approximates a single layer with $K^2=64$ kernels in a low-rank subspace, performing slightly below direct $K=64$ but at half the parameters.

## Position in the Lightweight SE Lineage

AdaptCRN extends the NJU/Horizon Robotics lightweight-SE lineage:

- [[sources/tan-2018-convolutional-recurrent-network-speech-enhancement|CRN (Tan & Wang 2018)]] — original CRN
- [[sources/rong-2024-gtcrn-speech-enhancement-ultralow|GTCRN (Rong et al. 2024)]] — 23.7K params, 39.6 MMACs/s; same lab
- [[sources/yang-2026-cofi-lite-ultra-lightweight-speech-enhancement|CoFi-Lite (Yang et al. 2026)]] — 83K params, 12.87 MMACs/s; same lab
- **AdaptCRN (Wang et al. 2025)** — 135K params, 41 MMACs/s; same lab

AdaptCRN trades more parameters than GTCRN/CoFi-Lite for stronger quality (PESQ 2.98 on VCTK-DEMAND, the best among the listed models), demonstrating that adaptive capacity expansion (params ↑, MACs ≈ flat) is a complementary axis to the asymmetric-path-decoupling axis of CoFi-Lite.

## Related Concepts

- [[concepts/adaptive-convolution|Adaptive Convolution]] — the core module
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — the broader CRN family
- [[concepts/gtcrn|GTCRN]] — predecessor; GTCRN-Adaptive is an explicit comparison point
- [[concepts/cofi-lite|CoFi-Lite]] — sibling ultra-lightweight model from the same lab
- [[concepts/dprnn|Dual-Path RNN (DPRNN)]] — bottleneck architecture
- [[concepts/grouped-recurrent-neural-network|Grouped Recurrent Neural Network]] — grouped DPRNN efficiency pattern
- [[concepts/erb-scale|ERB Scale]] — spectral compression
- [[concepts/power-law-compression|Power-Law Compression]] — dynamic-range compression
- [[concepts/dynamic-convolution|Dynamic Convolution]] — CV ancestor of the core module
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]] — basic block structure

## Related Sources

- [[sources/wang-2025-adaptive-convolution-cnn-speech-enhancement|Wang et al. 2025: Adaptive Convolution for CNN-based Speech Enhancement Models]]
