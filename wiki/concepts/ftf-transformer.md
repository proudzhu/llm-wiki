---
type: concept
created: 2026-11-10
updated: 2026-11-10
sources:
  - raw/papers/zhao-2025-lightweight-transformer/full-text.md
tags:
  - speech-enhancement
  - neural-network-architecture
  - transformer
  - lightweight
  - streaming
  - attention
---

# Frequency–Time–Frequency (FTF) Transformer

The **FTF transformer** is the bottleneck block introduced by Zhao & Madhu (EUSIPCO 2025): three lightweight transformer stages stacked as **frequency → time → frequency**, each containing an RNN block and a multi-head-attention (MHA) block, with parameters shared along the dimension it does *not* model. It is the block of the **LCT-GAN** generator (referred to as **FTF-Net** in the authors' follow-up work) and the direct predecessor of [[concepts/hyst-net|HyST-Net]].

![[raw/papers/zhao-2025-lightweight-transformer/figures/fig2.png|Fig. 2]]

*Figure 2: The ladder-shaped information flow. Frequency is exchanged within each previous frame (1st frequency transformer), propagated causally to the current frame (time transformer), then re-exchanged within the current frame (2nd frequency transformer).*

## Structure

| Stage | RNN block | Attention block | Parameter sharing |
|:------|:----------|:----------------|:------------------|
| 1st frequency transformer | Bi-directional GRU + Linear | 4-head MHA over frequency | shared across all frames |
| Time transformer | Uni-directional GRU + Linear, laid out as $(B\!\cdot\!F, T, C)$ so frequency is the batch axis | causal MHA with trapezoidal mask, context $\leq 1$ s | GRU shared across all frequency bins |
| 2nd frequency transformer | Bi-directional GRU + Linear | 4-head MHA over frequency | shared across all frames |

Every RNN and MHA block is pre-norm (LayerNorm) with a residual connection. The GRUs are grouped (grouping factor 4) and their hidden size equals the input channel count ($Ch=64$ in LCT-GAN). Sharing is what makes attention affordable: the GRU inside the time transformer sees only $C$ features per bin instead of the flattened $F\!\cdot\!C$ a conventional bottleneck would use, removing the quadratic dependence on feature width.

## Why F–T–F Rather Than T–F or More Stacking

The paper's ablation (all bottlenecks at matched MACs and parameters, generator-only, causal) is the evidence for the ordering:

| Bottleneck | PESQ | STOI | SI-SDR | P.835 SIG |
|---|---|---|---|---|
| TT | 2.18 | 0.895 | 14.01 | 2.93 |
| FF | 2.34 | 0.908 | 14.24 | 2.69 |
| TF | 2.55 | 0.923 | 15.55 | 2.89 |
| FT | 2.57 | 0.924 | 15.73 | 2.93 |
| TFT | 2.62 | 0.929 | 16.00 | 2.95 |
| **FTF** | **2.68** | **0.932** | **16.29** | 2.93 |
| TFTF | 2.68 | 0.934 | 16.40 | 2.97 |
| FTFT | 2.69 | 0.933 | 16.25 | 2.99 |

- **Both axes are needed**: frequency-only modelling buys PESQ/STOI/SI-SDR/BAK, time-only modelling buys SIG (speech-preservation MOS), and neither alone approaches an interleaved stack.
- **Order matters**: FT beats TF at equal cost, because the time stage should operate on information already made spectrally coherent.
- **FTF is the knee**: adding a fourth stage (TFTF, FTFT) returns $\leq 0.01$ PESQ / $\leq 0.06$ dB SI-SDR for proportionally more compute.
- **Wrapping, not replacing**: the symmetric outer pair makes every TF bin emissive and receptive in both dimensions, so the current frame's bins see global context after the second frequency stage.

## Efficiency

Against the conventional GRU bottleneck of CRUSE (Braun et al. 2021, which flattens frequency into the feature dimension), the FTF stack cuts **MACs by 27% and parameters by 98%**. The complete LCT-GAN generator is 0.14 M parameters at 0.35 G MAC/s — some 6% of DeepFilterNet2's parameters — while achieving 3.06 PESQ on VoiceBank+DEMAND.

## Relation to Successors

The follow-up [[concepts/hyst-net|HyST-Net]] (Zhao & Madhu 2026) keeps the three-block interleave but replaces FTF's *spectral* GRU with frequency-axis MHA, reporting RTF 0.22 vs FTF's 1.05 in strict frame-by-frame CPU streaming: the frequency GRU is a serial dependency along a dimension whose bins are all available at once. That result does not contradict FTF's ablation (which measured quality at fixed complexity, not wall-clock latency) but it does relocate the bottleneck — FTF's cost is quality-optimal per MAC, not latency-optimal per frame.

## Related Concepts

- [[concepts/trapezoidal-causal-masking|Trapezoidal Causal Masking]] — bounds the time transformer's attention context
- [[concepts/hyst-net|HyST-Net]] — successor replacing the spectral GRU with MHA
- [[concepts/dprnn|Dual-Path RNN (DPRNN)]] — the two-stage interleaved precedent FTF extends to three
- [[concepts/grouped-recurrent-neural-network|Grouped Recurrent Neural Network]] — grouping factor 4 in each GRU
- [[concepts/gated-recurrent-unit|Gated Recurrent Unit]]
- [[concepts/attention-mechanism|Attention Mechanism]]
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — the encoder–decoder family the bottleneck sits in

## Related Sources

- [[sources/zhao-2025-lightweight-transformer|Zhao & Madhu 2025: Study of Lightweight Transformer Architectures for Single-Channel Speech Enhancement]] — block origin, ordering ablation, LCT-GAN
- [[sources/zhao-2026-spectrally-adaptive-loss|Zhao & Madhu 2026: Spectrally Adaptive Loss for Streaming Speech Enhancement]] — HyST-Net reuses FTF-Net's encoder–decoder and measures FTF-Net's RTF
