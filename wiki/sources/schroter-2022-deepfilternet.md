---
type: source
created: 2026-06-07
updated: 2026-06-07
sources:
  - raw/papers/schroter-2022-deepfilternet/full-text.md
  - https://arxiv.org/abs/2110.05588
  - zotero://select/items/0_TXVFFJPG
tags:
  - speech-enhancement
  - deep-filtering
  - low-complexity
  - full-band-audio
  - icassp-2022
---

# Schröter, Escalante-B., Rosenkranz & Maier 2022: DeepFilterNet

> Hendrik Schröter, Alberto N. Escalante-B., Tobias Rosenkranz, Andreas Maier

| Field | Value |
|-------|-------|
| **Institutions** | FAU Erlangen-Nürnberg ([[entities/hendrik-schroter|Hendrik Schröter]], [[entities/andreas-maier|Andreas Maier]]), WS Audiology ([[entities/alberto-n-escalante-b|Alberto N. Escalante-B.]], [[entities/tobias-rosenkranz|Tobias Rosenkranz]]) |
| **Venue** | ICASSP 2022, pp. 7407–7411 |
| **Year** | 2022 |
| **Type** | Conference paper |
| **DOI** | [10.48550/arXiv.2110.05588](https://doi.org/10.48550/arXiv.2110.05588) |
| **Code** | [github.com/Rikorose/DeepFilterNet](https://github.com/Rikorose/DeepFilterNet) |
| **Zotero** | [Open in Zotero](zotero://select/items/0_TXVFFJPG) |

## Summary

DeepFilterNet is a low-complexity two-stage speech enhancement framework for full-band (48 kHz) audio based on deep filtering. Stage 1 enhances the spectral envelope using ERB-scaled gains that model human frequency perception, while Stage 2 applies deep filtering to enhance periodic speech components. The architecture enforces sparsity via separable convolutions and grouped linear/GRU layers, achieving 1.8M parameters and 0.35 GMACs/s — making it viable for real-time embedded deployment. DeepFilterNet outperforms complex ratio masks (CRMs) across FFT sizes from 5–30 ms and matches state-of-the-art models like DCCRN+ with substantially lower computational cost.

## Problem Formulation

Given a noisy mixture signal $x(t) = s(t) * h(t) + z(t)$ where $s(t)$ is clean speech, $h(t)$ is a room impulse response, and $z(t)$ is additive noise, the goal is to estimate $\hat{s}(t)$. The signal is processed in the STFT domain:

$$
X(k, f) = S(k, f) \cdot H(k, f) + Z(k, f)
$$

Deep filtering is defined as a complex linear filter applied along the time axis in each frequency band:

$$
Y(k, f) = \sum_{i=0}^{N} C(k, i, f) \cdot X(k - i + l, f)
$$

where $C$ are complex coefficients of filter order $N$, $l$ is an optional look-ahead, and $Y$ is the enhanced spectrogram. A learned weighting factor $\alpha(k)$ blends deep-filtered and gain-enhanced outputs:

$$
Y^{\text{DF}}(k, f) = \alpha(k) \cdot Y^{\text{DF}'}(k, f) + (1 - \alpha(k)) \cdot Y^G(k, f)
$$

## Methodology

### Two-Stage Framework

1. **Stage 1 — ERB Gain Estimation**: A log-power spectrogram is computed, normalized via exponential mean normalization, and passed through an ERB filter bank (default 32 bands). An encoder-decoder (UNet) architecture predicts ERB-scaled gains that are transformed back to full frequency resolution and applied pointwise to the noisy spectrogram.

2. **Stage 2 — Deep Filtering**: Applied only up to $f_{\text{DF}} = 5\text{ kHz}$ where periodic speech energy is concentrated. A separate network predicts per-band complex filter coefficients of order $N=5$ with a look-ahead of $l_{\text{DF}} = 1$. The alpha weighting ensures deep filtering only affects periodic components.

### DNN Architecture

- **Encoder**: 4 convolutional blocks with separable convolutions (depthwise 3×2 + 1×1), batch normalization, ReLU; progressively halve frequency resolution
- **Bottleneck**: 3 grouped GRU layers ($P=8$ groups, hidden size 64 each) with grouped linear layers
- **Decoder**: Transposed convolutions mirroring the encoder with 1×1 pathway convolutions as add-skip connections
- **DF Net**: 2 grouped GRU layers followed by convolutional output layers predicting DF coefficients
- **Grouping**: Input split into $P=8$ groups, processed by independent smaller GRUs/linear layers, outputs shuffled to recover inter-group correlations

### Loss Function

Compressed spectral loss with magnitude and phase-aware terms:

$$
\mathcal{L}_{\text{spec}} = \sum_{k,f} \||Y|^c - |S|^c\|^2 + \sum_{k,f} \||Y|^c e^{j\varphi_Y} - |S|^c e^{j\varphi_S}\|^2
$$

where $c = 0.6$ is a compression factor modeling perceived loudness. An additional loss $\mathcal{L}_\alpha$ forces the DF component to activate only on periodic speech segments by computing local SNR below $f_{\text{DF}}$:

$$
\mathcal{L}_\alpha = \sum_k \|\alpha \cdot \mathbb{1}_{\text{LSNR} < -10\text{dB}}\|^2 + \sum_k \|(1 - \alpha) \cdot \mathbb{1}_{\text{LSNR} > -5\text{dB}}\|^2
$$

Combined loss: $\mathcal{L} = \lambda_{\text{spec}} \cdot \mathcal{L}_{\text{spec}} + \lambda_\alpha \cdot \mathcal{L}_\alpha$ with $\lambda_{\text{spec}} = 1$, $\lambda_\alpha = 0.05$.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| **Training data** | DNS Challenge dataset (750h clean speech, 180h noise) |
| **Oversampled** | VCTK, PTDB (10×) |
| **RIRs** | 10,000 simulated (image source model, RT60 0.05–1.00 s) |
| **Augmentation** | 2nd-order filters, EQs, random gains {−6, 0, 6} dB, random resampling |
| **SNR range** | {−5, 0, 5, 10, 20, 40} dB |
| **Sample length** | 3 s |
| **Batch size** | 32 |
| **Optimizer** | Adam, lr $1 \times 10^{-3}$, decay 0.9 every 3 epochs |
| **Epochs** | 30 |
| **FFT size** | 960 (20 ms, default) |
| **ERB bands** | 32 |
| **DF frequency** | 5 kHz |
| **DF order** | 5 |
| **Look-ahead** | $l_{\text{DNN}} = 2$, $l_{\text{DF}} = 1$ |
| **Test set** | VCTK/DEMAND, custom DNS split (70/15/15%) |

## Results

### Comparison on VCTK-DEMAND

| Model | Params [M] | MACS [G/s] | WB-PESQ [MOS] | SI-SDR [dB] |
|-------|-----------|------------|----------------|-------------|
| Noisy | — | — | 1.97 | 8.41 |
| PercepNet | 8.0 | 0.80 | 2.73 | — |
| DCCRN | 3.7 | 14.36 | 2.68 | — |
| DCCRN+ | 3.3 | — | 2.84 | — |
| **DeepFilterNet** | **1.8** | **0.35** | **2.81** | **16.63** |
| w/o stage 2 | 0.9 | 0.25 | 2.57 | 13.81 |

### DF vs CRM Across FFT Sizes

Deep filtering consistently outperforms complex ratio masks across all tested FFT sizes (240–1440, corresponding to 5–30 ms latency). The gap is largest at small FFT sizes (e.g., 16.5 vs 15.9 dB SI-SDR at 5 ms), demonstrating DF's particular advantage for low-latency applications.

## Key Contributions

1. **Two-stage deep filtering framework**: Combines ERB-scaled spectral envelope enhancement with per-band deep filtering for periodic component enhancement, achieving strong performance at low complexity.
2. **Deep filtering superiority over CRMs**: Systematic comparison shows DF outperforms complex ratio masks across all FFT sizes from 5–30 ms, especially at low latencies where CRMs degrade due to insufficient frequency resolution.
3. **Efficient architecture**: Separable convolutions + grouped GRU/linear layers ($P=8$) achieve 1.8M parameters and 0.35 GMACs/s — dramatically lower than DCCRN (3.7M, 14.36 GMACs) while matching performance.
4. **Alpha masking**: Learned per-frame weighting prevents deep filtering from introducing artifacts on noise-only or unvoiced segments by gating DF activation based on local SNR.
5. **Open-source framework**: Full implementation and pretrained weights released under open-source license.

## Related Concepts

- [[concepts/deep-filtering|Deep Filtering]]
- [[concepts/erb-scale|ERB Scale]]
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]]
- Grouped GRU/Linear layers — input split into $P=8$ groups with independent processing, output shuffled to recover cross-group correlations

## Related Synthesis

- [[synthesis/computational-efficiency-evolution|Computational Efficiency Evolution]]
