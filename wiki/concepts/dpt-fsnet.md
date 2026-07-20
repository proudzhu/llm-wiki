---
type: concept
created: 2026-07-20
updated: 2026-07-20
sources:
  - raw/papers/chen-2023-ultra-dual-path-compression/full-text.md
tags:
  - speech-enhancement
  - deep-learning
  - transformer
  - dual-path
  - subband
---

# DPT-FSNet

**Dual-Path Transformer-based Full-Subband Network (DPT-FSNet)** is a speech-enhancement architecture introduced by Dang, Chen & Zhang (ICASSP 2022) that combines a 2D convolutional encoder/decoder with a dual-path transformer operating on the full time-frequency (T-F) feature map. It achieves high wide-band perceptual evaluation of speech quality (WB-PESQ) on noise-suppression tasks with a small parameter count but suffers from large computational cost — motivating the compression work in [[sources/chen-2023-ultra-dual-path-compression\|Chen et al. 2023]].

## Architecture

The offline DPT-FSNet pipeline:

1. **Input layer**: stacked real and imaginary parts of the complex spectrum, with shape $2C \times T \times F$.
2. **2D convolutional encoder**: transforms the input into a feature of shape $E \times T \times F$, where $E$ is the feature dimension per T-F bin.
3. **Dual-path transformer**: alternates between
   - **Intra-frame (subband) attention/GRU** — models spectral patterns within a frame
   - **Inter-frame (fullband) attention/GRU** — models temporal patterns across frames along the full band
4. **2D convolutional decoder**: maps features back to complex masks of shape $2C \times T \times F$.

## Properties Relevant to Compression

- The complexity is **directly tied to the number of frames $T$ and frequency bins $F$**, making it a natural target for time-frequency compression.
- The model combines a 2D-conv encoder, dual-path transformer, and 2D-conv decoder, so compression methods must be applicable to different module types.
- The original model has a small parameter count (~100K), but its MACs/s is high — Chen et al. report 1822M MACs/s uncompressed.

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

## Related Sources

- [[sources/chen-2023-ultra-dual-path-compression\|Chen et al. 2023: Ultra Dual-Path Compression]] — uses online DPT-FSNet as the base architecture for compression experiments
