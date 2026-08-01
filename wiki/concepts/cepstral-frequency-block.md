---
type: concept
created: 2026-08-01
updated: 2026-08-01
sources:
  - raw/papers/liu-2023-iccrn/full-text.md
tags:
  - neural-network
  - speech-enhancement
  - cepstral-analysis
  - normalization
  - cross-domain-modeling
  - fft
---

# Cepstral Frequency Block (CFB)

The **Cepstral Frequency Block (CFB)** is the core novel building block of [[concepts/iccrn|ICCRN]] (Liu & Zhang, ICASSP 2023). It augments a time-frequency (TF) domain residual branch with a parallel **cepstral-space** branch, so the network can model speech both in the frequency domain and in the cepstral domain within a single inplace block. The CFB replaces the Gated Linear Units (GLUs) used in ICCRN's predecessor IGCRN.

## Motivation

Speech production decomposes into excitation (vocal cords) and vocal tract (filter). In the cepstral domain, the slowly varying spectral envelope — carrying timbre and semantic content — concentrates in the narrow low-quefrency band, while the densely periodic harmonics collapse to a few sparsely distributed pitch peaks in the higher-quefrency band. Because most noises do not share this envelope/harmonic structure, speech components are distinguishable from noise cepstrally even at low SNR. The CFB exploits this sparsity by processing features in a cepstral space that the network reaches via real-valued FFT applied internally to the TF feature map.

## Structure

![[raw/papers/liu-2023-iccrn/figures/3e6ba05bde3daf360d53cc18c4ec6214b4b956971227ab629b14c74049135d2a.jpg|Cepstral frequency block (CFB) and cepstral unit]]
*Figure: The Cepstral Frequency Block (CFB) and the cepstral unit. Conv F×T = 2D convolution over frequency×time; Ceps-chBLSTM(c)×n = BLSTM processing on the cepstral-bin sequence within a frame (c = hidden size per direction, n = number of layers); Sig = sigmoid; LN = LayerNorm on channel and frequency dimensions; [b, c, f, t] = dimension sizes (batch, channel, frequency, time).*

The CFB has three sub-modules:

### 1. Task-split gate

A `LN → Conv1×1 → Sigmoid` module produces a gate. The input TF feature is projected by a `Conv1×1` and multiplied by the gate, splitting the task into a cepstral-branch input and a TF-branch residual.

### 2. Cepstral unit (Ceps Unit)

The gated feature is transformed into the cepstral space by a real-valued FFT applied per channel per frame. The cepstral feature is processed by:

- **Cepstral LayerNorm**. Statistics $E_{c,f}$ and $\mathrm{Var}_{c,f}$ are computed jointly over channel and cepstral dimensions to stabilize the very different energy distributions across quefrency bands. A learned affine $\gamma \in \mathbb{R}^{c \times f}$ and $\beta \in \mathbb{R}^{c \times f}$ then individually rescale each cepstral bin in each channel:

  $$\mathrm{LN}(\mathbf{x}) = \frac{\mathbf{x} - E_{c,f}[\mathbf{x}]}{\sqrt{\mathrm{Var}_{c,f}[\mathbf{x}] + \epsilon}} \odot \gamma + \beta$$

  Multiplication in the cepstral domain is equivalent to circular convolution in the frequency domain, so the learned $\gamma$ acts as a bank of full-size (160-tap) frequency-domain filters — even before any densely connected neural layers.

- **Cepstral channel-wise BLSTM (Ceps-chBLSTM)**. Treats cepstral bins as a time series and processes them with a BLSTM, so the network knows which quefrency band it is filtering and can apply different patterns to different bands. This replaces the alternative of splitting the cepstrum into ≥10 sub-bands with separate $3 \times 1$ convolutions, at much lower complexity.

### 3. TF-domain residual branch

A `LN → Conv3×1` module processes the residual of the gated feature directly in the TF domain. Speech energy is sparse cepstrally; some noise (e.g., tonal or narrowband) is sparser in the frequency domain, so cross-domain modeling is complementary.

The outputs of the cepstral unit and the TF branch are added to produce the CFB output.

## Why FFT for the Space Transformation?

The cepstral transform uses the classical FFT rather than a learnable transform, for three reasons:

1. **Orthogonality / no information loss** — DFT coefficients are independent; data-driven transforms introduce dataset bias and may generalize poorly.
2. **Physical interpretability** — DFT bins are ordered low to high quefrency, enabling visualization, analysis, and tuning.
3. **Cost** — FFT is parameterless and has linearithmic complexity. In ICCRN the FFT costs only **0.15 G MAC**, vs. ~0.95 G MAC for a DFT or neural-based transform.

## Ablation Evidence

From the ICCRN ablation table on WSJ0 SI-84 at -5 dB babble noise:

| Variant | STOI (%) | PESQ |
|---------|----------|------|
| ICCRN (full CFB) | 84.48 | 2.231 |
| ICCRN(-freq) — TF `Conv3×1` branch removed | 83.21 | 2.134 |
| ICCRN(-ceps) — cepstral unit removed | 74.12 | 1.793 |
| ICCRN(cepsLN) — cepstral LN only, no Ceps-chBLSTM | 78.35 | 1.947 |

Removing the cepstral branch (`ICCRN(-ceps)`) is far more damaging than removing the TF branch (`ICCRN(-freq)`). The cepstral LayerNorm alone (no LSTM/CNN in the cepstral branch) already lifts `ICCRN(-ceps)` by +4.23 pp STOI and +0.154 PESQ, confirming the central role of the cepstral-space affine parameters as an implicit full-size frequency filter bank.

## Comparison with Related FFT-Domain Modules

- **FFC-SE** (Shchekotov et al., Interspeech 2022) — uses Fast Fourier Convolution (FFC) inspired by computer vision. Applies $1 \times 1$ convolutions in the FFT domain, suited to image content with little shared pattern. The CFB instead uses a cepstral BLSTM that models the cepstral-bin sequence with both short- and long-term patterns, exploiting the fairly fixed cepstral pattern of speech. FFC-SE uses batch normalization; the CFB uses layer normalization, which the authors argue is better suited to cepstral-feature distributions.

## Related Concepts

- [[concepts/iccrn|ICCRN]] — the model that introduces the CFB
- [[concepts/cepstral-space-speech-enhancement|Cepstral-Space Speech Enhancement]] — the broader paradigm
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — CRN family
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]] — training paradigm
- [[concepts/stft-consistency|STFT Consistency]] — loss-construction technique

## Related Sources

- [[sources/liu-2023-iccrn|Liu & Zhang 2023: ICCRN — Inplace Cepstral Convolutional Recurrent Neural Network]]
