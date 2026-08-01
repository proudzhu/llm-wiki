---
type: concept
created: 2026-08-01
updated: 2026-08-01
sources:
  - raw/papers/liu-2023-iccrn/full-text.md
tags:
  - neural-network
  - speech-enhancement
  - convolutional-recurrent-network
  - cepstral-analysis
  - inplace-model
  - complex-spectrum-mapping
---

# ICCRN

**ICCRN** (Inplace Cepstral Convolutional Recurrent Neural Network) is a monaural speech-enhancement architecture proposed by Liu & Zhang (ICASSP 2023). It extends the authors' earlier [[concepts/igcrn|IGCRN]] by replacing the GLU-based blocks with a novel [[concepts/cepstral-frequency-block|Cepstral Frequency Block (CFB)]] that performs neural processing in a cepstral space reached via real-valued FFT. ICCRN is **inplace** (no frequency downsampling) and predicts real and imaginary STFT components directly ([[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]).

## Architecture

ICCRN follows a U-Net structure with skip connections:

1. **Input** — real and imaginary parts of the noisy STFT stacked along channel dimension, shape `[Batch, 2, F=160, Time]`.
2. **Encoder projection** — a channel-wise BLSTM (F-chBLSTM) lifts the 2-channel input to a higher-dimensional feature (channel size $c = 20$).
3. **Encoder** — 5 sequential [[concepts/cepstral-frequency-block|Cepstral Frequency Blocks]] (CFBs). Frequency dimension stays at $f = 160$ throughout (inplace design); all convolutions share output channel size $c = 20$.
4. **Bottleneck** — 2-layer channel-wise LSTM (T-chLSTM×2, hidden $2c$) produces a mask multiplied with the encoder output.
5. **Decoder** — 5 cascaded CFBs process the masked feature concatenated with skip-connection features; a final T-chLSTM refines the time dimension.
6. **Output** — $1 \times 1$ convolution compresses the channel dimension to 2, producing the estimated real and imaginary STFT components.

The system is **causal** (no reference to future frames) and uses 50%-overlap STFT (20 ms Hamming window, 160 frequency bins).

## Loss Function

Weighted L1 combination of real, imaginary, and amplitude errors, evaluated on the **STFT-consistent** spectrum (estimated spectrum is first inverted to time domain and re-transformed to TF domain before loss):

$$\mathcal{L} = \left\| \mathcal{R}(\hat{S}) - \mathcal{R}(S) \right\|_1 + \left\| \mathcal{I}(\hat{S}) - \mathcal{I}(S) \right\|_1 + \alpha \left\| |\hat{S}| - |S| \right\|_1$$

with $\alpha = 2$ to emphasize amplitude. The STFT-consistency step alleviates the [[concepts/stft-consistency|STFT consistency]] problem.

## Inplace Design Choice

IGCRN (Liu & Zhang 2021), ICCRN's predecessor, was originally designed for multi-channel speech enhancement where preserving per-bin spatial cues matters. It therefore discards the CRN's frequency downsampling and uses channel-wise LSTM that processes each frequency bin independently — like beamforming.IGCRN's monaural performance was weak because discarding frequency downsampling also discards full-band modeling capacity. ICCRN recovers that capacity by replacing GLUs with CFBs that model speech in the cepstral space, where the harmonic structure is sparsely represented.

## Results on WSJ0 SI-84 (Auditec Babble & Cafeteria)

| Model | Params (M) | MAC (G) | -5 dB Babble STOI / PESQ | -5 dB Caf. STOI / PESQ |
|-------|-----------|---------|--------------------------|------------------------|
| GCRN | 9.77 | 2.42 | 80.98 / 2.014 | 77.95 / 1.936 |
| DCCRN | 3.67 | 5.59 | 80.52 / 2.177 | 79.25 / 2.221 |
| DPCRN | 0.81 | 3.18 | 80.30 / 2.174 | 75.87 / 2.013 |
| DCCRN(CSM) | 3.67 | 5.59 | 81.72 / 2.216 | 80.30 / 2.241 |
| DPCRN(CSM) | 0.81 | 3.18 | 83.21 / 2.212 | 80.03 / 2.226 |
| **ICCRN** | **0.46** | **2.09** | **84.48 / 2.231** | **80.73 / 2.257** |

ICCRN is the most compact model in the comparison (about half the parameters of DPCRN and one-eighth of DCCRN) and the lowest-MAC, while achieving the best STOI in every test condition, with the largest gap at -5 dB.

## Ablation Highlights

| Variant | -5 dB Babble STOI / PESQ |
|---------|--------------------------|
| ICCRN | 84.48 / 2.231 |
| ICCRN(-freq) — remove TF `Conv3×1` branch | 83.21 / 2.134 |
| ICCRN(-ceps) — remove cepstral unit | 74.12 / 1.793 |
| ICCRN(cepsLN) — cepstral LN only, no Ceps-chBLSTM | 78.35 / 1.947 |

Removing the cepstral branch (`ICCRN(-ceps)`) is far more damaging than removing the TF branch (`ICCRN(-freq)`). A single cepstral LayerNorm (no LSTM/CNN in the cepstral branch) already lifts `ICCRN(-ceps)` by +4.23 pp STOI — because the learned affine $\gamma$ acts as a bank of full-size 160-tap circular-convolution kernels in the frequency domain.

## Position in the Inplace-CRN Lineage

- **[[concepts/igcrn|IGCRN]]** (Liu & Zhang 2021, Interspeech — [[sources/liu-2021-igcrn|source]]) — inplace gated CRN for dual-channel SE; uses [[concepts/inplace-convolution|inplace convolutions]] and a [[concepts/channel-wise-lstm|channel-wise LSTM reused across frequency bins]] to preserve per-bin spatial cues. Also applied to mono and stereo AEC.
- **ICCRN** (Liu & Zhang 2023, ICASSP) — replaces GLU with CFB; introduces cepstral-space processing; achieves SOTA low-SNR STOI on WSJ0 SI-84 at minimum complexity.

The authors note that ICCRN's improved single-channel SE is expected to also lift multi-channel SE and AEC systems built on the inplace-CRN backbone.

## Related Concepts

- [[concepts/cepstral-frequency-block|Cepstral Frequency Block (CFB)]] — the core novel module
- [[concepts/cepstral-space-speech-enhancement|Cepstral-Space Speech Enhancement]] — the broader paradigm
- [[concepts/igcrn|IGCRN]] — predecessor in the inplace-CRN lineage
- [[concepts/inplace-convolution|Inplace Convolution]] — inherited architectural choice (no frequency downsampling)
- [[concepts/channel-wise-lstm|Channel-wise LSTM with Model Reuse]] — inherited bottleneck design
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — CRN family baseline
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]] — training paradigm
- [[concepts/stft-consistency|STFT Consistency]] — loss-construction technique used in training
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/liu-2021-igcrn|Liu & Zhang 2021: IGCRN — Inplace Gated Convolutional Recurrent Neural Network]] — predecessor; introduces the inplace CRN design that ICCRN inherits
- [[sources/liu-2023-iccrn|Liu & Zhang 2023: ICCRN — Inplace Cepstral Convolutional Recurrent Neural Network]]
