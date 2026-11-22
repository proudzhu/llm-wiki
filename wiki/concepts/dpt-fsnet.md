---
type: concept
created: 2026-07-20
updated: 2026-11-22
sources:
  - raw/papers/dang-2022-dpt-fsnet/full-text.md
  - raw/papers/chen-2023-ultra-dual-path-compression/full-text.md
tags:
  - speech-enhancement
  - deep-learning
  - transformer
  - dual-path
  - subband
---

# DPT-FSNet

**Dual-Path Transformer-based Full-band and Sub-band fusion Network (DPT-FSNet)** is a speech-enhancement architecture introduced by Dang, Chen & Zhang (ICASSP 2022 — [[sources/dang-2022-dpt-fsnet|Dang et al. 2022]]) that combines a convolutional encoder/decoder with a [[concepts/dual-path-transformer|dual-path transformer]] operating on the full time-frequency (T-F) feature map: the intra path models sub-band information, the inter path full-band information ([[concepts/full-band-sub-band-fusion|full-band/sub-band fusion]] inside one sequence model). At 0.88 M parameters it reports WB-PESQ 3.33 on VoiceBank+DEMAND and 3.53/3.26 on the DNS 2020 test sets; its high computational cost motivated the streaming compression work in [[sources/chen-2023-ultra-dual-path-compression|Chen et al. 2023]].

## Architecture

The offline DPT-FSNet pipeline:

1. **Input layer**: stacked real and imaginary parts of the complex spectrum, with shape $2C \times T \times F$.
2. **2D convolutional encoder**: transforms the input into a feature of shape $E \times T \times F$, where $E$ is the feature dimension per T-F bin.
3. **Dual-path transformer**: alternates between
   - **Intra-frame (subband) attention/GRU** — models spectral patterns within a frame
   - **Inter-frame (fullband) attention/GRU** — models temporal patterns across frames along the full band
4. **2D convolutional decoder**: maps features back to complex masks of shape $2C \times T \times F$.

## Original Offline Model (Dang et al. 2022)

Concrete specification from [[sources/dang-2022-dpt-fsnet|the original paper]]:

- **Encoder/decoder**: 1×1 conv + dilated dense block (four 2×3 dilated convs, dilation rate 2, dense concatenation with input channels $C, 2C, 3C, 4C$, LayerNorm + PReLU); $C = 64$ feature maps, halved to $C' = 32$ inside the processing module.
- **Dual-path transformer**: $B = 4$ blocks, $h = 4$ heads, $d_{model} = 32$, $d_{ff} = 128$; each transformer = multi-head self-attention + GRU-replacing-FC feed-forward network.
- **Output**: [[concepts/complex-ratio-mask|complex ratio mask]] on the RI-stacked STFT (25 ms window, 6.25 ms hop, FFT 512, 16 kHz).
- **Loss**: $0.4 \times$ waveform MSE $+ 0.6 \times$ L1 on the magnitudes of the real/imaginary parts.
- **Size**: 0.88 M parameters; no MACs/latency analysis in the original paper.
- **Ablation** (matched params/complexity/latency): time-domain input 2.97 → STFT input 3.33 WB-PESQ; sub-band-only dual path 3.20 → full-sub fusion 3.33; BLSTM 3.05 → improved transformer 3.20.

## Properties Relevant to Compression

- The complexity is **directly tied to the number of frames $T$ and frequency bins $F$**, making it a natural target for time-frequency compression.
- The model combines a 2D-conv encoder, dual-path transformer, and 2D-conv decoder, so compression methods must be applicable to different module types.
- The original offline model has **0.88 M parameters** (Dang et al. 2022, Table 1); the ~109K-parameter figure and 1822M MACs/s belong to Chen et al.'s online redesign, not the original. (CMGAN's TASLP paper cites 0.91 M — the original paper's 0.88 M is authoritative.)

## Online Streaming Variant (Chen et al. 2023)

[[sources/chen-2023-ultra-dual-path-compression\|Chen et al. 2023]] redesign DPT-FSNet for streaming:

- Multi-signal input: microphone $d$, far-end reference $x$, linear-AEC error $\hat{e}$
- Individual masks per input signal; final output is the sum of masked signals
- Linear attention replaces softmax attention for $\mathcal{O}(T)$ memory
- Single GRU after the first attention layer replaces stacked LSTMs
- Unidirectional subband (online) + bidirectional fullband (chunk-level) attention

This streaming variant is the base architecture for the dual-path compression work.

## Related Concepts

- [[concepts/dual-path-compression\|Dual-Path Compression]]
- [[concepts/trainable-frequency-compression\|Trainable Frequency Compression]]
- [[concepts/frame-skip-prediction\|Frame-Skip Prediction]]
- [[concepts/post-processing-network\|Post-Processing Network]]
- [[concepts/erb-scale\|ERB Scale]]
- [[concepts/dual-path-transformer|Dual-Path Transformer]]
- [[concepts/full-band-sub-band-fusion|Full-Band and Sub-Band Fusion]]

## Related Sources

- [[sources/chen-2023-ultra-dual-path-compression\|Chen et al. 2023: Ultra Dual-Path Compression]] — uses online DPT-FSNet as the base architecture for compression experiments
- [[sources/dang-2022-dpt-fsnet|Dang, Chen & Zhang 2022: DPT-FSNet]] — the original paper: architecture, dual-domain loss, ablations, VoiceBank+DEMAND and DNS results
