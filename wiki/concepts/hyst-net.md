---
type: concept
created: 2026-09-06
updated: 2026-09-06
sources:
  - raw/papers/zhao-2026-spectrally-adaptive-loss/full-text.md
tags:
  - speech-enhancement
  - deep-learning
  - neural-network-architecture
  - lightweight
  - streaming
---

# HyST-Net

**HyST-Net** (Hybrid Spectral-Temporal modelling Network, Zhao & Madhu 2026) is a lightweight streaming speech-enhancement backbone that applies a **hybrid bottleneck**: multi-head attention (MHA) along the frequency axis and GRUs along the time axis, interleaved in three spectral-temporal blocks. The design exploits the observation that the two STFT axes have different parallelism properties — all frequency bins of a frame are simultaneously available (suited to parallel attention), while temporal processing needs causal recurrence (suited to the GRU's compact state).

## Architecture

- **Encoder–decoder**: U-Net with a three-layer causal convolutional encoder–decoder configured identically to FTF-Net, bottleneck channel size $Ch=64$, one-time-step buffer caches in convolutional layers for streaming.
- **Bottleneck**: three interleaved spectral-temporal blocks — MHA for spectral modelling (avoids the processing latency of recurrent spectral modelling), GRU for temporal modelling (avoids the linear-in-context cost of causal-attention key-value caching).
- **Input**: Re/Im parts of the power-law compressed ($c=0.3$) noisy complex spectrogram, concatenated channel-wise (STFT 512 samples, 50% overlap).
- **Output**: complex-valued ideal ratio mask in the compressed domain, applied then magnitude-decompressed; 32 ms algorithmic latency, frame-by-frame streaming.

## Efficiency (DNS Challenge, strict frame-by-frame CPU streaming)

| Model | MACs [M/s] | Params [M] | RTF | PESQ |
|-------|-----------|-----------|-----|------|
| CRUSE4-64-1×GRU2 | 301.2 | 2.85 | 0.26 | 2.84 |
| FTF-Net | 318.2 | 0.14 | 1.05 | 2.91 |
| **HyST-Net** | **266.4** | **0.11** | **0.22** | 2.86 |

HyST-Net matches FTF-Net's quality with 16.3% fewer MACs, 21% fewer parameters, and ~4.77× lower RTF (FTF-Net's recurrent spectral bottleneck serialises streaming inference); vs CRUSE it achieves similar RTF with 96% fewer parameters.

## Related Concepts

- [[concepts/spectrally-adaptive-loss|Spectrally Adaptive Loss]] — the loss functions HyST-Net was designed to evaluate
- [[concepts/gated-recurrent-unit|Gated Recurrent Unit]] — temporal modelling
- [[concepts/attention-mechanism|Attention Mechanism]] — spectral modelling
- [[concepts/complex-ratio-mask|Complex Ratio Mask (cRM)]] — the compressed-domain output target
- [[concepts/power-law-compression|Power-Law Compression]]
- [[concepts/dprnn|Dual-Path RNN]] — the interleaved spectral-temporal modelling paradigm HyST-Net's bottleneck belongs to
- [[concepts/gtcrn|GTCRN]] · [[concepts/cofi-lite|CoFi-Lite]] — the lightweight-SE efficiency frontier

## Related Sources

- [[sources/zhao-2026-spectrally-adaptive-loss|Zhao & Madhu 2026: Spectrally Adaptive Loss for Streaming Speech Enhancement]]
