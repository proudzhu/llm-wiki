---
type: concept
created: 2026-07-17
updated: 2026-07-17
sources:
  - raw/papers/valin-2021-percepnet-joint-echo-control/full-text.md
tags:
  - speech-enhancement
  - acoustic-echo-cancellation
  - low-complexity
  - real-time
  - perceptual
  - hybrid-dsp-dnn
---

# PercepNet

PercepNet is a perceptually-motivated, low-complexity hybrid DSP/DNN approach to real-time speech enhancement and (in its 2021 extension) joint acoustic echo control. Originally introduced by Valin et al. (ICASSP 2020) for fullband speech enhancement, it was extended in [[sources/valin-2021-percepnet-joint-echo-control|Valin et al. 2021]] to combine a traditional AEC with joint residual echo and noise suppression, winning the ICASSP 2021 AEC Challenge.

## Core Ideas

The PercepNet algorithm is based on two main ideas from the paper:

1. **Spectral envelope restoration via perceptual band scaling** — scale the energy of perceptually-spaced spectral bands to match the near-end speech. The STFT is divided into 32 triangular bands following the [[concepts/erb-scale|ERB scale]]. The ideal gain g_b(l) = X_b(l) / Y_b(l) is approximated by the DNN.
2. **Pitch periodicity restoration via comb filter** — use a multi-tap non-causal comb filter at the pitch frequency to remove noise between harmonics and match the periodicity of the near-end speech. Controlled by strength parameter r_b(l) in [0, 1] (0 = no filtering, 1 = full comb filtering).

## DNN Architecture

- 2 convolutional layers (1x5 then 1x3) + 5 GRU layers
- Look-ahead M = 2 frames (40 ms algorithmic delay budget)
- Input: 100 features = 96 band features (3 per ERB band: energy Y_b(l+M), pitch coherence q_y,b(l), far-end energy F_b(l+M)) + 4 scalar features (pitch period T, pitch correlation, non-stationarity, L1/L2 excitation norm ratio)
- Output: 64 = 32 gains g_hat_b + 32 strengths r_hat_b
- 8M weights, quantized to 8-bit integers (forced to ±1/2 range)
- Envelope postfilter applied to output gains

## Sparse Variants

Structured sparsity with 16x4 sub-blocks for SIMD vectorization:

- Second conv layer: 50% dense
- GRU new-state matrices: 40% dense
- GRU update gate: 20% dense
- GRU reset gate: 10% dense

Two sparse variants:

- 2.1M non-zero weights (25% of full model)
- 800k non-zero weights (10% of full model)

## Distinction from Later "PercepNet-Style" Works

> **Important**: The original PercepNet uses the **ERB scale (32 bands)**, NOT the Bark scale. Later works in the [[concepts/percepnet-style-neural-post-filter|PercepNet-style neural post filter]] lineage — [[sources/seidel-2024-bark-scale-nn-residual-suppression|Bark-AEC (Seidel 2024)]] (86 Bark bands) and [[sources/li-2025-echofree-neural-aec|EchoFree (Li 2025)]] (100 Bark bands) — switched to the Bark scale. The "PercepNet-style" pattern name refers to the hybrid AEC + perceptual-band neural post filter architecture, not strictly to the ERB scale.

## Related Concepts

- [[concepts/percepnet-style-neural-post-filter|PercepNet-Style Neural Post Filter]]
- [[concepts/erb-scale|ERB Scale]]
- [[concepts/pitch-coherence|Pitch Coherence]]
- [[concepts/multidelay-block-frequency-domain-adaptive-filter|Multidelay Block Frequency-Domain Adaptive Filter (MDF)]]
- [[concepts/structured-sparsity|Structured Sparsity]]
- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]]
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/valin-2021-percepnet-joint-echo-control|Valin et al. 2021: Joint Neural Echo Control and Speech Enhancement Based On PercepNet]]
