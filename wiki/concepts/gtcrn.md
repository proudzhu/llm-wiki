---
type: concept
created: 2026-05-24
updated: 2026-07-21
tags:
  - neural-network
  - speech-enhancement
  - lightweight-model
  - grouped-convolution
  - attention
---

# Grouped Temporal Convolutional Recurrent Network (GTCRN)

**GTCRN** (Grouped Temporal Convolutional Recurrent Network) is an ultralightweight speech enhancement architecture proposed by Rong et al. (ICASSP 2024). It achieves state-of-the-art efficiency with only 23.7 K parameters and 39.6 MMACs/s by applying grouped strategies across all components — grouped convolution, grouped RNN, and ERB-based band grouping — built on the [[concepts/convolutional-recurrent-network|DPCRN]] backbone.

## Architecture

GTCRN follows an encoder-decoder structure with skip connections:

1. **Band Merging (BM)**: Reduces high-frequency bands from 192 to 64 using the ERB scale, producing a 129-dimensional compressed feature map (65 low-frequency + 64 ERB bands above 2 kHz)
2. **Encoder**: Two Conv blocks (convolution + BN + PReLU) mapping input to high-dimensional embeddings, followed by three GT-Conv blocks
3. **Grouped Dual-Path RNN (G-DPRNN)**: Bottleneck with grouped bidirectional GRU (intra-frame) and grouped unidirectional GRU (inter-frame)
4. **Decoder**: Mirror of encoder with transposed convolutions
5. **Band Splitting (BS)**: Restores original frequency resolution
6. **Subband Feature Extraction (SFE)**: Optional modules on skip connections to enhance frequency information

## Key Components

### Grouped Temporal Convolution (GT-Conv)

Based on the ShuffleNetV2 unit, GT-Conv adds temporal dilation to depthwise convolution for long-range temporal modeling. Input channels are split in half: one branch passes through unchanged, the other through a P-Conv2D → DD-Conv2D (dilated depthwise) → P-Conv2D pipeline. Outputs are concatenated and channel-shuffled.

### Grouped Dual-Path RNN (G-DPRNN)

Combines grouped RNN (GRNN) with [[concepts/dprnn|DPRNN]]. Both input features and hidden states are split into 2 groups, each processed by a smaller recurrent layer with 2× fewer parameters. Intra-frame: grouped bidirectional GRU. Inter-frame: grouped unidirectional GRU (causal).

### Subband Feature Extraction (SFE)

Enhances convolution layers' frequency information capture via an unfold operation with kernel size $k$ along the frequency dimension, combining adjacent bands into subband units stacked along the channel dimension.

### Temporal Recurrent Attention (TRA)

Multiplicative attention mask computed via:
1. Global energy aggregation: $Z(c,t) = \frac{1}{F}\sum_{f=1}^F V^2(c,t,f)$
2. GRU processes the temporal energy sequence
3. FC layer + sigmoid produces the attention mask

TRA outperforms standard time-dimension attention (TA) with minimal overhead.

## Loss Function

Multi-domain loss combining SISNR, magnitude MSE, and complex component MSE:

$$\mathcal{L} = \alpha \mathcal{L}_\text{SISNR} + (1-\beta)\mathcal{L}_\text{mag} + \beta(\mathcal{L}_\text{real} + \mathcal{L}_\text{imag})$$

with $\alpha = 0.01$, $\beta = 0.3$, and spectrogram compression exponent $0.3$.

## Results

With 23.7 K parameters and 39.6 MMACs/s, GTCRN achieves:
- **PESQ 2.87** on VCTK-DEMAND (vs 2.84 for S-DCCRN with 100× more params)
- **SISNR 18.83 dB** on VCTK-DEMAND (vs 16.63 for [[sources/schroter-2022-deepfilternet|DeepFilterNet]] with 75× more params)
- **DNSMOS P.808 3.44** on DNS3 blind test set (vs 3.15 for RNNoise)

## Successors

- **[[concepts/cofi-lite|CoFi-Lite]]** (Yang et al., IEEE SPL 2026) reuses GTCRN's BM, SFE, TRA modules and loss function, but decouples spectral modeling into parallel coarse (full-band envelope, ×16 compression) and fine (low-frequency detail below 2 kHz, ×2 compression) paths bridged by [[concepts/cross-path-fusion|Cross-Path Fusion]]. It **outperforms GTCRN** (PESQ 2.16 vs. 2.07 on DNS3) at only 40.26% of its MACs (12.87M vs. 31.97M MACs/s) and 34% lower RTF — trading a higher parameter count (83.12k vs. 23.67k) for drastically lower compute.

## Related Concepts

- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[concepts/dprnn|Dual-Path RNN (DPRNN)]]
- [[concepts/cofi-lite|CoFi-Lite]]
- [[concepts/cross-path-fusion|Cross-Path Fusion (CPF)]]
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]]
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[concepts/erb-scale|ERB Scale]]
- [[concepts/broadcasted-residual-learning|Broadcasted Residual Learning]]
- [[concepts/adaptive-residual-normalization|Adaptive Residual Normalization]]
- [[concepts/grouped-recurrent-neural-network|Grouped Recurrent Neural Network]]
- [[concepts/distributed-binaural-speech-enhancement|Distributed Binaural Speech Enhancement]]
- [[concepts/tango-framework|Tango Framework]]

## Related Sources

- [[sources/rong-2024-gtcrn-speech-enhancement-ultralow|Rong et al. 2024: GTCRN — A Speech Enhancement Model Requiring Ultralow Computational Resources]]
- [[sources/yang-2026-cofi-lite-ultra-lightweight-speech-enhancement|Yang et al. 2026: CoFi-Lite — Pushing the Limits of Ultra-Lightweight Speech Enhancement]]
- [[sources/schroter-2022-deepfilternet|Schröter et al. 2022: DeepFilterNet]]
- [[sources/zhao-2026-halo-half-frame-rate-adaptive-operator|Zhao et al. 2026: HALO — Half-frame-rate Adaptive Learnable Operator for Lightweight STFT-based Speech Enhancement]]
- [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|Benslimane et al. 2026: RT-Tango]]
