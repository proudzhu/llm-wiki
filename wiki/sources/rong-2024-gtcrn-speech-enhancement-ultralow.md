---
type: source
created: 2026-05-24
updated: 2026-05-24
sources:
  - raw/papers/rong-2024-gtcrn-speech-enhancement-ultralow/full-text.md
  - https://doi.org/10.1109/ICASSP48485.2024.10448310
  - zotero://select/items/0_BACCUUCC
tags:
  - speech-enhancement
  - lightweight-model
  - convolutional-recurrent-network
  - grouped-convolution
  - icassp-2024
---

# Rong, Sun, Zhang, Hu, Zhu & Lu 2024: GTCRN — A Speech Enhancement Model Requiring Ultralow Computational Resources

**Authors**: [[entities/xiaobin-rong|Xiaobin Rong]], [[entities/tianchi-sun|Tianchi Sun]], [[entities/xu-zhang|Xu Zhang]], [[entities/yuxiang-hu|Yuxiang Hu]], [[entities/changbao-zhu|Changbao Zhu]], [[entities/jing-lu|Jing Lu]]
**Affiliations**: Nanjing University / Horizon Robotics / Jiangsu Thingstar IT
**Venue**: ICASSP 2024, pp. 971–975
**Type**: Conference Paper
**DOI**: [10.1109/ICASSP48485.2024.10448310](https://doi.org/10.1109/ICASSP48485.2024.10448310)
**Zotero**: [BACCUUCC](zotero://select/items/0_BACCUUCC)

---

## Summary

GTCRN (Grouped Temporal Convolutional Recurrent Network) is a speech enhancement model requiring only 23.7 K parameters and 39.6 MMACs per second — among the lightest in the literature. Built on the [[concepts/convolutional-recurrent-network|DPCRN]] backbone, it applies grouped convolution, grouped RNN, an ERB-based band merging scheme, subband feature extraction (SFE) modules, and temporal recurrent attention (TRA) to drastically reduce model size while maintaining competitive performance. GTCRN outperforms RNNoise by a wide margin and matches or exceeds much larger baselines including DeepFilterNet and S-DCCRN.

## Problem Formulation

Speech enhancement aims to estimate clean speech $s(t)$ from a noisy mixture $x(t) = s(t) + n(t)$, where $n(t)$ is additive noise. Deep learning models operating in the time-frequency domain process the complex STFT spectrogram $X = \text{STFT}(x)$ to produce an enhanced spectrogram $\hat{S}$.

The challenge for edge deployment is minimizing model parameters and multiply-accumulate operations (MACs) while maintaining speech quality — a trade-off most SOTA models fail to achieve.

## Methodology

### Overall Architecture

GTCRN follows an encoder-decoder structure with skip connections:

![[raw/papers/rong-2024-gtcrn-speech-enhancement-ultralow/figures/6ebcf48dc18dd8002d7d963befeba38cdb45850cfd923caaf4fa0cf082af6a6b.jpg|GTCRN overall architecture]]

*Figure 1: Overall architecture of GTCRN. BM = Band Merging, BS = Band Splitting, SFE = Subband Feature Extraction, G-DPRNN = Grouped Dual-Path RNN.*

The architecture comprises:
1. **Band Merging (BM)** — reduces high-frequency bands using the ERB scale
2. **Encoder** — two Conv blocks + three GT-Conv blocks with grouped temporal convolution
3. **G-DPRNN** — grouped dual-path RNN bottleneck for intra/inter-frame modeling
4. **Decoder** — mirror of encoder with transposed convolutions
5. **Band Splitting (BS)** — restores original frequency resolution
6. **SFE (optional)** — subband feature extraction modules on skip connections

### Band Merging and Splitting

The BM operation downsamples spectral features using the ERB scale, merging the high-frequency bands (above 2 kHz) into 64 ERB bands while keeping the 65 low-frequency bands unaltered, producing a 129-dimensional compressed feature map. The BS operation restores the original resolution.

### Grouped Dual-Path RNN (G-DPRNN)

Combines grouped RNN (GRNN) with dual-path RNN (DPRNN). Both input features and hidden states are split into 2 disjoint groups, each processed by a smaller recurrent layer (2× fewer parameters). Intra-frame modeling uses grouped bidirectional GRU; inter-frame modeling uses grouped unidirectional GRU for causality.

### Grouped Temporal Convolution (GT-Conv)

Based on the ShuffleNetV2 unit, GT-Conv introduces temporal dilation into the depthwise convolution for improved long-range temporal dependency modeling. Input features are split in half along the channel axis — one branch remains unaltered, the other undergoes P-Conv2D → DD-Conv2D (dilated depthwise) → P-Conv2D processing. Outputs are concatenated and channel-shuffled.

![[raw/papers/rong-2024-gtcrn-speech-enhancement-ultralow/figures/569b1504453c6b0c12665b97db0b9558354ea80621dbe71e6528afb14ded32be.jpg|GT-Conv block]]

*Figure 2: Grouped temporal convolution block.*

### Subband Feature Extraction (SFE)

The SFE module enhances frequency information capture by performing an unfold operation on input features with kernel size $k$ in the frequency dimension, combining each frequency band with its $k-1$ adjacent bands into subband units. These are reshaped along the channel dimension, enabling the following convolution to leverage frequency information more efficiently.

![[raw/papers/rong-2024-gtcrn-speech-enhancement-ultralow/figures/916b4a09804d19243ff5d02c71a6eb6bb1c47ea8419801ddf4d06543b4928398.jpg|SFE module]]

*Figure 3: Subband feature extraction module.*

### Temporal Recurrent Attention (TRA)

The TRA module generates a multiplicative attention mask by modeling the energy distribution along the time axis. Given input $V \in \mathbb{R}^{C \times T \times F}$:

$$Z(c,t) = \frac{1}{F}\sum_{f=1}^{F} V^2(c,t,f) \quad \text{(global energy aggregation)}$$

The energy vector is processed by a GRU followed by a fully-connected layer and sigmoid to produce the attention mask.

![[raw/papers/rong-2024-gtcrn-speech-enhancement-ultralow/figures/08a4f25a96d6b22e3d3044e897ce71d9742c4dc373bc9c2a8d319ae848556e1d.jpg|TRA module]]

*Figure 4: Temporal recurrent attention module.*

### Loss Function

Multi-domain loss combining waveform and spectrogram terms:

$$\mathcal{L} = \alpha \mathcal{L}_\text{SISNR}(\tilde{s}, s) + (1-\beta)\mathcal{L}_\text{mag}(\tilde{S}, S) + \beta(\mathcal{L}_\text{real}(\tilde{S}, S) + \mathcal{L}_\text{imag}(\tilde{S}, S))$$

where $\alpha = 0.01$ and $\beta = 0.3$. The SISNR loss operates on waveforms, while magnitude and complex component losses operate on spectrograms with compression exponent $0.3$.

## Experimental Setup

| Dataset | Training samples | Test samples | SNR range | Sampling rate |
|---------|-----------------|--------------|-----------|---------------|
| VCTK-DEMAND | 11,572 utterances (28 speakers) | 824 utterances (2 speakers) | — | 16 kHz |
| DNS3 | 720,000 pairs (10s) | 800 pairs | -5 to 15 dB | 16 kHz |

**Implementation details**:
- STFT: square root Hanning window, 32 ms window, 16 ms hop, 512 FFT
- Input: channel-wise concatenation of real + imaginary + magnitude
- Conv blocks: 16 channels, kernel (1,5), stride (1,2), group size 2
- Optimizer: Adam, initial LR 0.001, halved on plateau (5 epochs)
- Batch size: 4 (VCTK-DEMAND), 16 (DNS3)
- Metrics: SISNR, PESQ, STOI, DNSMOS P.808/P.835

## Results

### Ablation Study (DNS3 test set)

| SFE | TA | TRA | Params (K) | MACs (M/s) | SISNR | PESQ | STOI |
|-----|----|-----|------------|------------|-------|------|------|
| Baseline (DPCRN) | — | — | — | — | 3.92 | 1.30 | 0.789 |
| — | — | — | 13.35 | 33.91 | 9.87 | 1.87 | 0.834 |
| — | ✓ | — | 14.84 | 34.00 | 10.00 | 1.89 | 0.838 |
| — | — | ✓ | 21.65 | 34.47 | 10.25 | 1.91 | 0.840 |
| ✓ | — | — | 15.37 | 39.07 | 10.10 | 1.90 | 0.838 |
| ✓ | ✓ | — | 16.87 | 39.16 | 10.27 | 1.92 | 0.841 |
| ✓ | — | ✓ | 23.66 | 39.63 | 10.62 | 1.95 | 0.845 |

### Comparison on VCTK-DEMAND

| Model | Params (M) | MACs (G/s) | SISNR | PESQ | STOI |
|-------|-----------|------------|-------|------|------|
| RNNoise (2018) | 0.06 | 0.04 | — | 2.29 | — |
| PercepNet (2020) | 8.00 | 0.80 | — | 2.73 | — |
| DeepFilterNet (2022) | 1.80 | 0.35 | 16.63 | 2.81 | 0.942 |
| S-DCCRN (2022) | 2.34 | — | — | 2.84 | 0.940 |
| **GTCRN (proposed)** | **0.02** | **0.04** | **18.83** | **2.87** | **0.940** |

### Comparison on DNS3 Blind Test Set

| Model | Params (M) | MACs (G/s) | DNSMOS P.808 | BAK | SIG | OVRL |
|-------|-----------|------------|-------------|-----|-----|------|
| RNNoise (2018) | 0.06 | 0.04 | 3.15 | 3.45 | 3.00 | 2.53 |
| S-DCCRN (2022) | 2.34 | — | 3.43 | — | — | — |
| **GTCRN (proposed)** | **0.02** | **0.04** | **3.44** | **3.90** | **3.00** | **2.70** |

## Key Contributions

1. **Ultralightweight architecture**: 23.7 K parameters and 39.6 MMACs/s — approximately 3× smaller than RNNoise and 100× smaller than DeepFilterNet
2. **Grouped strategies across the entire model**: Grouped convolution (GT-Conv), grouped RNN (G-DPRNN), and band grouping (ERB-based BM) collectively reduce complexity while maintaining representational capacity
3. **Subband Feature Extraction (SFE)**: Novel module that unfolds frequency bands into subband units along the channel dimension, enhancing frequency information utilization in convolutions
4. **Temporal Recurrent Attention (TRA)**: Attention mechanism using GRU-based energy aggregation that outperforms standard time-dimension attention with minimal computational overhead
5. **Competitive performance at extreme efficiency**: Outperforms RNNoise by substantial margins and achieves PESQ 2.87 (VCTK-DEMAND) vs 2.84 for S-DCCRN which has 100× more parameters

## Related Concepts

- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[concepts/dprnn|Dual-Path RNN (DPRNN)]]
- [[concepts/gtcrn|Grouped Temporal Convolutional Recurrent Network (GTCRN)]]
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]]
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]
- ERB Scale

## Related Synthesis

- [[synthesis/computational-efficiency-evolution|Computational Efficiency Evolution]]
- [[synthesis/adaptive-algorithm-tradeoffs|Adaptive Algorithm Trade-offs]]
