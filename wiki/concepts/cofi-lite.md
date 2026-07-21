---
type: concept
created: 2026-07-21
updated: 2026-07-21
tags:
  - neural-network
  - speech-enhancement
  - lightweight-model
  - dual-path
  - convolutional-recurrent-network
---

# CoFi-Lite

**CoFi-Lite** (Coarse-Fine Lite) is an ultra-lightweight speech enhancement architecture proposed by Yang et al. (IEEE SPL 2026). With only **12.87M MACs/s and 83.12k parameters**, it outperforms [[concepts/gtcrn|GTCRN]] (PESQ 2.16 vs. 2.07 on DNS3) at 40.26% of its computational cost, defining a new point on the ultra-lightweight SE efficiency frontier.

## Architecture

CoFi-Lite decouples spectral modeling into two parallel, symmetric encoder-decoder paths on a [[concepts/convolutional-recurrent-network|CRN]] backbone (encoder + decoder + two Inter-RNN bottlenecks each), bridged by a [[concepts/cross-path-fusion|Cross-Path Fusion (CPF)]] module:

1. **Coarse path** — models the **full-band magnitude envelope** at deep compression (ratio 16). Input is ERB band-merged log-magnitude processed by an SFE module (both inherited from GTCRN); three MB blocks (PW-Conv → DW-Conv → PW-Conv + TRA attention, derived from UL-UNAS) progressively halve frequency resolution.
2. **Fine path** — recovers **low-frequency detail below 2 kHz** ($f_\text{low} = 65$) at high resolution (ratio 2). Input concatenates log-magnitude with power-compressed (exponent 0.7) real/imaginary parts of the truncated spectrum; a single MB block with stride (1,2) keeps resolution high and compute low.
3. **CPF** — fuses the two paths' bottleneck features for mutual interaction.

Each path predicts an [[concepts/ideal-ratio-mask|IRM]]; the masks are applied sequentially — coarse mask over the full band, fine mask only below $f_\text{low}$. Phase is not modeled (noisy phase is reused), a deliberate performance-complexity trade-off.

## Key Design Principle

**Asymmetric capacity allocation beats uniform downscaling.** Naively shrinking a CRN degrades low-frequency bands first; CoFi-Lite instead compresses the coarse envelope path aggressively (tolerant to compression) while keeping the fine detail path nearly uncompressed (sensitive to compression). Ablations confirm: fine-path compression ratio 2→8 drops PESQ 2.16→2.09, while coarse-path ratio 8–32 makes no difference. The 2 kHz cutoff is also empirically optimal — salient speech structure concentrates below 2 kHz.

## Variants

- **CoFi-Lite** (base): 83.12k params, 12.87M MACs/s, RTF 0.033 — CPF latent $H=76$, 6 channels throughout
- **CoFi-Lite (Large)**: 221.31k params, 32.91M MACs/s, RTF 0.036 — $H=102$, coarse channels [6,12,14], fine 14; matches AdaptCRN (PESQ 2.30, SI-SNR 12.43) with 19.34% fewer MACs

## Results (DNS3 test set)

| Model | Params (k) | MACs/s (M) | RTF | PESQ | SI-SNR | OVRL |
|-------|-----------|------------|-----|------|--------|------|
| GTCRN | 23.67 | 31.97 | 0.050 | 2.07 | 11.30 | 2.63 |
| **CoFi-Lite** | 83.12 | **12.87** | **0.033** | **2.16** | **11.80** | **2.70** |
| AdaptCRN | 134.51 | 40.80 | 0.053 | 2.30 | 12.35 | 2.75 |
| **CoFi-Lite (Large)** | 221.31 | **32.91** | **0.036** | **2.30** | **12.43** | **2.75** |

Notably, CoFi-Lite trades a *higher* parameter count (83.12k vs. GTCRN's 23.67k) for drastically lower compute — a favorable trade for edge devices where MACs/s (energy, latency) binds harder than storage.

## Related Concepts

- [[concepts/cross-path-fusion|Cross-Path Fusion (CPF)]]
- [[concepts/gtcrn|Grouped Temporal Convolutional Recurrent Network (GTCRN)]]
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network (CRN)]]
- [[concepts/dprnn|Dual-Path RNN (DPRNN)]]
- [[concepts/ideal-ratio-mask|Ideal Ratio Mask (IRM)]]
- [[concepts/erb-scale|ERB Scale]]
- [[concepts/power-law-compression|Power-Law Compression]]

## Related Sources

- [[sources/yang-2026-cofi-lite-ultra-lightweight-speech-enhancement|Yang et al. 2026: CoFi-Lite — Pushing the Limits of Ultra-Lightweight Speech Enhancement]]
- [[sources/rong-2024-gtcrn-speech-enhancement-ultralow|Rong et al. 2024: GTCRN — A Speech Enhancement Model Requiring Ultralow Computational Resources]]
