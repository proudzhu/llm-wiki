---
type: concept
created: 2026-11-01
updated: 2026-11-07
sources:
  - raw/papers/ahn-2026-fastenhancer/full-text.md
  - raw/papers/kim-2026-faster-enhancer/full-text.md
tags:
  - neural-network-architecture
  - speech-enhancement
  - dual-path
  - transformer
  - streaming
  - efficiency
---

# RNNFormer

**RNNFormer** is the dual-path bottleneck block of [[sources/ahn-2026-fastenhancer|FastEnhancer]] (Ahn, Han, Woo & Kim, ICASSP 2026): each block pairs a **time-axis GRU** sub-block with a **frequency-axis multi-head self-attention (MHSA)** sub-block. The name encodes the hybrid — an RNN half and a Transformer half — and the design encodes a claim about the two STFT axes: *temporal dependencies are best modeled recurrently (for streaming), while spectral dependencies are best modeled with global attention (because harmonics and spectral structure are non-sequential).*

## Structure

Each RNNFormer block contains two residual sub-blocks:

1. **Time-axis GRU block** — unidirectional [[concepts/gated-recurrent-unit|GRU]] → convolution → batch normalization → residual skip. The GRU's constant-size recurrent state needs no key-value caching, keeping streaming inference cheap.
2. **Frequency-axis MHSA block** — 4-head [[concepts/attention-mechanism|self-attention]] → convolution → batch normalization → residual skip. All frequency bins of the current frame are available simultaneously, so attention over frequency is causal-in-time by construction and needs no cache. A trainable positional encoding is added to the input of the *first* MHSA block.

FastEnhancer stacks K blocks (K = 2…5 across its T–L model sizes), with channel widths C₂ = 20…96 and frequency resolution F = 16…64.

## Why This Axis Assignment

The assignment inverts the standard [[concepts/dprnn|DPRNN]] pattern (RNN on *both* axes) and the dual-path-transformer pattern (attention on *both* axes):

- **Against frequency-RNN (DPRNN)**: an RNN along frequency assumes frequency bands have a *sequential* relationship, but spectral relationships (e.g., harmonics) are **global** — a model should handle all frequency interactions concurrently. Ablation: replacing the frequency MHSA with a frequency GRU (making a DPRNN) clearly degrades SISDR at similar STOI.
- **Against time-MHSA (DPT)**: streaming self-attention along time requires caching previous key/value frames — additional memory operations, and quality improves only by *increasing* the cache (Bae et al. 2023), raising memory and arithmetic cost. Ablation: replacing the time GRU with time-MHSA (31-frame lookbehind) has fewer parameters but dramatically higher RTF.
- **BN over LN**: batch normalization fuses into adjacent layers at inference (a multiply-add), layer normalization does not — an RTF win at zero parameter cost.

## Relation to HyST-Net

[[concepts/hyst-net|HyST-Net]] (Zhao & Madhu 2026) independently converged on the **same axis assignment** — frequency-axis MHA + time-axis GRU in interleaved spectral-temporal blocks — motivated identically (parallel frequency axis, recurrent temporal axis for streaming). The two models differ in scope: HyST-Net targets DNS-Challenge-quality at sub-CRUSE complexity (~0.11M params); FastEnhancer explicitly optimizes the RTF/quality Pareto frontier with speed-oriented architecture-wide choices (time-kernel-1 convolutions, BN fusion, fixed filterbank bridges). RNNFormer adds the dual-path ablation evidence (vs DPRNN and DPT) that HyST-Net does not report.

## Deployment as an int8 Runtime

[[sources/kim-2026-faster-enhancer|Kim 2026]] ported FastEnhancer-Medium at 48 kHz to faster-enhancer.c, a dependency-free int8 C runtime, with architecture and weights untouched. The port validates the block's deployment profile from the systems side: the fused GRU kernel is the **largest per-frame compute bucket** (82.2 µs of a ~452 µs frame on an Apple M2, ahead of QKV projection at 36.3 µs), which is why the runtime fuses the GRU's two matrices, three gates, hidden update and fp16 state write into one kernel per SIMD tier so int32 accumulators never reach memory. Quantized to int8 with per-frame activation ranges, the block chain tracks fp32 to −0.006 PESQ over 824 VoiceBank-DEMAND utterances.

## Related Concepts

- [[concepts/dprnn|Dual-Path RNN (DPRNN)]] — the recurrence-on-both-axes predecessor
- [[concepts/gated-recurrent-unit|Gated Recurrent Unit]] — the time-axis component
- [[concepts/attention-mechanism|Attention Mechanism]] — the frequency-axis component
- [[concepts/hyst-net|HyST-Net]] — independent convergence on the same axis assignment
- [[concepts/gtcrn|GTCRN]] / [[concepts/lisennet|LiSenNet]] / [[concepts/cofi-lite|CoFi-Lite]] — the complexity-optimized lightweight-SE line FastEnhancer contrasts against
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — the encoder-decoder backbone family

## Related Sources

- [[sources/ahn-2026-fastenhancer|Ahn, Han, Woo & Kim 2026: FastEnhancer — Speed-Optimized Streaming Neural Speech Enhancement]] — origin of the block; DPRNN/DPT ablations
- [[sources/zhao-2026-spectrally-adaptive-loss|Zhao & Madhu 2026: Spectrally Adaptive Loss for Streaming Speech Enhancement]] — HyST-Net's independent frequency-MHA + time-GRU convergence
- [[sources/kim-2026-faster-enhancer|Kim 2026: faster-enhancer.c]] — int8 runtime port of FastEnhancer-Medium; GRU kernel is the top compute bucket and gets the deepest fusion
