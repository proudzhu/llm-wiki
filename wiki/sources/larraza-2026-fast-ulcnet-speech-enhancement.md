---
type: source
created: 2026-07-19
updated: 2026-07-19
sources:
  - raw/papers/larraza-2026-fast-ulcnet-speech-enhancement/full-text.md
  - https://doi.org/10.48550/arXiv.2601.14925
  - zotero://select/items/0_292A8CGG
tags:
  - deep-learning
  - speech-enhancement
  - low-complexity
  - low-latency
  - recurrent-neural-network
  - fastgrnn
  - state-drift
---

# Larraza & de Koeijer 2026: Fast-ULCNet

**Authors**: [[entities/nicolas-arrieta-larraza|Nicolás Arrieta Larraza]], [[entities/niels-de-koeijer|Niels de Koeijer]]

**Affiliation**: Bang & Olufsen, Struer, Denmark

**Venue**: ICASSP 2026 (IEEE International Conference on Acoustics, Speech and Signal Processing)

**Year**: 2026 | **Type**: Conference Paper (preprint) | **DOI**: [10.48550/arXiv.2601.14925](https://doi.org/10.48550/arXiv.2601.14925)

**arXiv**: [2601.14925](https://arxiv.org/abs/2601.14925)

**Zotero**: [292A8CGG](zotero://select/items/0_292A8CGG)

## Summary

This paper proposes **Fast-ULCNet**, an extension of [[concepts/ulcnet|ULCNet]] that replaces the GRU recurrent layers with [[concepts/fastgrnn|FastGRNN]] units to reduce both model size and inference latency. The authors additionally identify and empirically demonstrate a performance decay in FastGRNN over long input sequences (>60 s) caused by internal RNN state drift, and propose **[[concepts/comfi-fastgrnn|Comfi-FastGRNN]]** (complementary filter FastGRNN) — a trainable complementary filter extension that mitigates the drift. Fast-ULCNet matches the noise-suppression performance of the original ULCNet while reducing the parameter count by more than half (0.338M vs. 0.685M) and decreasing the real-time factor by ~34% on embedded ARM targets.

## Problem Formulation

Single-channel speech enhancement on resource-constrained embedded devices requires algorithms with jointly low latency and low computational complexity. The state-of-the-art [[concepts/ulcnet|ULCNet]] architecture (Shetu et al., ICASSP 2024) achieves strong noise suppression at 0.685M parameters and 2.057M MACs, using [[concepts/channel-wise-feature-reorientation|channel-wise feature reorientation]] and [[concepts/power-law-compression|power-law compression]] with GRU-based recurrent layers. The GRU choice was common among low-complexity SE architectures but represents the dominant residual computational and parameter cost.

The paper targets two coupled questions:

1. Can the GRU layers be replaced by a lighter gated RNN without quality loss?
2. Does the lighter RNN remain stable over the long sequences encountered in real deployment (minutes-long streaming), where training-time stability guarantees may not transfer to inference?

The second question is motivated by an empirical observation: **FastGRNN's claimed length-invariance was validated only on sequences up to 1.63 s** in the original work (Kusupati et al., NeurIPS 2018), leaving the streaming-inference regime untested.

## Methodology

### FastGRNN Replacement

The FastGRNN state update replaces the GRU's dual-gate mechanism with a weighted residual connection that reuses the same weight matrices $W$, $U$ for both the candidate update and the gate, controlled by two scalar trainable parameters $\zeta, \nu \in [0, 1]$:

$$
z_t = \sigma(W x_t + U h_{t-1} + b_z)
$$

$$
\tilde{h}_t = \tanh(W x_t + U h_{t-1} + b_h)
$$

$$
h_t = (\zeta (1 - z_t) + \nu) \odot \tilde{h}_t + z_t \odot h_{t-1}
$$

This reuses $W$ and $U$ across both updates, roughly halving the parameter count of the recurrent block relative to a GRU at the same hidden size.

### Comfi-FastGRNN: Complementary-Filter Drift Correction

The authors observed that FastGRNN, applied to >60 s audio signals for SE, exhibits monotonic growth of the mean hidden-state magnitude over time during inference. This drift correlates with a measurable degradation in enhancement quality (see Figure 2). The root cause is traced to the state update equation: the coefficients of $\tilde{h}_t$ and $h_{t-1}$ do **not** satisfy a sum-to-one constraint, so the state lacks a contraction guarantee over long horizons.

Motivated by complementary filters used in accelerometer–gyroscope orientation estimation (where a high-pass filter on the gyroscope is fused with a low-pass filter on the accelerometer to suppress drift), the authors extend FastGRNN with two scalar trainable parameters $\lambda, \gamma \in \mathbb{R}$:

$$
h_{t\,\text{comfi}} = \gamma h_t + (1 - \gamma) \lambda
$$

Here $\lambda$ acts as a scalar modulation factor compensating for state drift, and $\gamma$ controls the relative contribution of the hidden state and the drift-correction term. Initialization: $\gamma = 0.999$, $\lambda = 0.0$ (i.e., near-identity at start of training).

![[raw/papers/larraza-2026-fast-ulcnet-speech-enhancement/figures/9ac760ded9d676728633223234cd59266619afdec4edd935a40377f6bdfe0c39.jpg|Figure 1: Comfi-FastGRNN block diagram]]
*Figure 1: Block diagram of Comfi-FastGRNN, comprising the original FastGRNN architecture extended with a trainable complementary filter.*

![[raw/papers/larraza-2026-fast-ulcnet-speech-enhancement/figures/5dd7a6b2a8c83ee47d77b226d2180ac9af088e25fbd3f34db64e6029ce44fc28.jpg|Figure 2: State drift and performance decay]]
*Figure 2: Fast-ULCNet inference shows drifting on the mean RNN state $h_t$ (top) and performance decay on the processed signal (bottom) over time with FastGRNN (left column), whereas Comfi-FastGRNN (right column) maintains stable mean RNN state $h_{t\,\text{comfi}}$ and consistent performance.*

### Model Architecture

![[raw/papers/larraza-2026-fast-ulcnet-speech-enhancement/figures/daf61a6c8e86573c3c4d2b42a04be9c2397276ce5778e20080fa97ea6a3c661c.jpg|Figure 3: Fast-ULCNet architecture]]
*Figure 3: Architecture of Fast-ULCNet. Black boxes represent components from the original ULCNet architecture; dotted light-blue boxes highlight the FastGRNN-based modifications introduced in this work, with or without the complementary filter.*

The architecture preserves ULCNet's two-stage structure:

**Stage 1 — Magnitude mask estimation**

1. Modified [[concepts/power-law-compression|power-law compression]] applied to both real and imaginary STFT components of the noisy input
2. [[concepts/channel-wise-feature-reorientation|Channel-wise feature reorientation]]: overlapping rectangular uniform window, 1.5 kHz frequency resolution, overlap factor 0.33
3. Conv Block: 4 depthwise-separable convolutions (kernel 1×3, frequency-axis only), filter counts 32 / 64 / 96 / 128, max-pool ×2 downsampling on layers 2–4
4. Bidirectional Freq-FastGRNN: 64 units + pointwise convolution (64 filters)
5. 2 subband temporal Fast-GRNN blocks, each with 2 FastGRNN layers (128 units)
6. 2 fully-connected layers (257 neurons each) → real-valued magnitude mask

**Stage 2 — Phase refinement**

7. CNN on intermediate representations from the estimated magnitude mask and noisy phase: two 2D conv layers (32 filters, kernel 1×3) + pointwise conv (2 output channels)
8. [[concepts/complex-ratio-mask|Complex ratio masking (CRM)]] to reconstruct the enhanced complex spectrogram

### Loss Function

A consolidated time-frequency MAE loss (Braun & Tashev 2021) combining magnitude and complex spectrogram $L_1$ terms:

$$
\mathcal{L} = \frac{1}{TF} \sum_{t=1}^{T} \sum_{f=1}^{F} \left( \left| |S| - |\hat{S}| \right| + \left| S - \hat{S} \right| \right)
$$

where $S$ and $\hat{S}$ are the clean and predicted complex spectrogram values, and $T$, $F$ are the total frame and frequency bin counts.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Training data | Interspeech 2020 DNS Challenge dataset, 1000 h |
| Sampling rate | 16 kHz |
| SNR range | Uniform [−10, 30] dB |
| Train/val split | 85 / 15 |
| Test set | DNS Challenge 2020 synthetic non-reverberant test set (10 s) + extended 90 s version (each clip concatenated with itself 9×) |
| STFT window / hop / FFT | 32 ms / 16 ms / 512-point |
| Optimizer | Adam, initial LR $1 \times 10^{-3}$ |
| Gradient clipping | 3.0 |
| LR scheduler | Halve on 3 epochs without val-loss improvement |
| Early stopping | 5 epochs without improvement |
| Batch size | 32 samples × 10 s |
| Steps per epoch | 4000 train / 1000 val |
| FastGRNN nonlinearity $\sigma$ | Sigmoid |
| Comfi init $\gamma, \lambda$ | 0.999, 0.0 |
| Frequency resolution / overlap | 1.5 kHz / 0.33 |
| Conv Block filters | 32, 64, 96, 128 |
| Freq-FastGRNN units | 64 (+ pointwise conv 64) |
| Subband temporal FastGRNN | 2 blocks × 2 layers × 128 units |
| FC layers | 2 × 257 neurons |
| Stage-2 CNN | 2 × (2D conv, 32 filters, 1×3) + pointwise conv (2 channels) |
| Embedded RTF targets | Raspberry Pi 3 B+, Arm Cortex-A53 (single-thread, mean of 10 000 iterations) |

## Results

### Objective Quality (DNSMOS / PESQ / SI-SDR)

| Test signal length | Model | OVRLMOS | SIGMOS | BAKMOS | PESQ | SI-SDR |
|--------------------|-------|---------|--------|--------|------|--------|
| 10 s | ULCNet | 3.10 | 3.39 | 3.96 | 2.62 | 16.24 |
| 10 s | Fast-ULCNet | 3.09 | 3.39 | 3.95 | 2.51 | 15.99 |
| 10 s | Fast-ULCNet<sub>comfi</sub> | 3.09 | 3.39 | 3.97 | 2.50 | 16.01 |
| 90 s | ULCNet | 3.09 | 3.39 | 3.95 | 2.66 | 16.89 |
| 90 s | Fast-ULCNet | 2.93 | 3.39 | 3.62 | 2.24 | 13.58 |
| 90 s | Fast-ULCNet<sub>comfi</sub> | 3.10 | 3.39 | 3.99 | 2.51 | 16.48 |

**Key observations**:

- On 10 s signals, both Fast-ULCNet variants match ULCNet on DNSMOS sub-metrics; small PESQ / SI-SDR gaps (≤0.12 PESQ, ≤0.25 dB SI-SDR) favor ULCNet.
- On 90 s signals, plain Fast-ULCNet collapses: BAKMOS drops from 3.95 → 3.62, SI-SDR from 16.89 → 13.58, OVRLMOS from 3.09 → 2.93. This is the FastGRNN state-drift failure mode identified by the paper.
- Comfi-FastGRNN **fully recovers** long-sequence performance — DNSMOS sub-metrics slightly exceed ULCNet, while PESQ and SI-SDR remain within 0.15 PESQ / 0.41 dB of ULCNet.

### Computational Complexity

| Model | Params (M) | MACs (M) | RTF<sub>Pi3</sub> | RTF<sub>ARM</sub> |
|-------|-----------:|---------:|------------------:|------------------:|
| ULCNet | 0.685 | 2.057 | 0.976 | 0.927 |
| Fast-ULCNet | 0.338 | 1.691 | 0.657 | 0.604 |

- Parameter count reduced by **~51%** (0.685M → 0.338M)
- MACs reduced by **~18%** (2.057M → 1.691M)
- RTF improved by **~33%** on Raspberry Pi 3 B+ and **~35%** on Arm Cortex-A53
- The Comfi-FastGRNN variant has identical complexity (two extra scalars) and is omitted from the table.

## Key Contributions

1. **Fast-ULCNet architecture**: First application of FastGRNN to speech enhancement; replaces ULCNet's GRU layers with FastGRNN-based layers, halving the parameter count and reducing inference latency by ~34% on embedded ARM targets at matched SE quality.
2. **Empirical identification of FastGRNN state drift**: Demonstrates that FastGRNN — despite its proven training-time stability — drifts in the forward pass on long (>60 s) inference sequences, with measurable degradation in enhancement quality. The original FastGRNN evaluation only covered sequences up to 1.63 s; this is the first reported failure mode at streaming scale.
3. **Comfi-FastGRNN (Complementary Filter FastGRNN)**: A novel, parameter-efficient (two scalars: $\gamma, \lambda$) extension inspired by complementary filters in inertial-sensor fusion, which fully recovers long-sequence performance. This is the first reported use of a trainable complementary filter to mitigate RNN state drift.
4. **Open-source release**: Implementations of both Fast-ULCNet and Comfi-FastGRNN are publicly available, along with an online demo.

## Related Concepts

- [[concepts/fast-ulcnet|Fast-ULCNet]]
- [[concepts/fastgrnn|FastGRNN]]
- [[concepts/comfi-fastgrnn|Comfi-FastGRNN]]
- [[concepts/ulcnet|ULCNet]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/channel-wise-feature-reorientation|Channel-Wise Feature Reorientation]]
- [[concepts/power-law-compression|Power-Law Compression]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask]]

## Related Sources

- [[sources/shetu-2024-hybrid-low-complexity-aenr|Shetu et al. 2024: Hybrid Low-Complexity AENR]] — the parent ULCNet architecture that Fast-ULCNet extends; shares the channel-wise feature reorientation and power-law compression design

## Related Synthesis

- [[synthesis/joint-multitask-ultra-low-latency-se|Joint Multi-Task SE & Ultra-Low-Latency Paradigm]] — Fast-ULCNet is a single-task NS point on the low-complexity frontier, and Comfi-FastGRNN illustrates a streaming-specific failure mode (state drift over long sequences) that complements the linear-RNN replacement strategy discussed in the synthesis
