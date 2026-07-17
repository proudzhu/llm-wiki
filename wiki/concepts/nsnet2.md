---
type: concept
created: 2026-07-17
updated: 2026-07-17
sources:
  - raw/papers/seidel-2024-bark-scale-nn-residual-suppression/full-text.md
tags:
  - speech-enhancement
  - deep-learning
  - low-complexity
  - neural-network-architecture
  - noise-suppression
---

# NSNet2

**NSNet2** (Noise Suppression Network 2) is a lightweight fully-connected + recurrent neural network architecture for real-time monaural speech enhancement / noise suppression, introduced by Braun & Tashev (Speech and Computer 2020). It is widely used as a baseline and as a backbone for low-complexity speech-enhancement and [[concepts/acoustic-echo-cancellation\|AEC]] postfilters due to its favorable trade-off between performance and computational cost.

## Architecture

The NSNet2 topology alternates **fully-connected (FC) layers** and **gated recurrent unit (GRU) layers**:

- Input: log-power spectral features (typically STFT magnitude) of the noisy mic signal (and optionally additional references such as the far-end echo estimate).
- Body: stack of FC layers feeding one or more GRU layers (unidirectional, for causal streaming).
- Output: a real-valued (or sigmoid-bounded) time-frequency mask $M_\ell(k)$ applied to the noisy magnitude to recover the enhanced speech magnitude; phase is inherited from the noisy input.

The architecture is fully causal (streaming-friendly) and uses only dense + recurrent operations — no convolutions. This makes it significantly easier to deploy on resource-constrained DSPs and microcontrollers than convolutional alternatives.

## Role in Hybrid AEC Postfilters

NSNet2-style backbones are the basis for several [[concepts/percepnet-style-neural-post-filter\|PercepNet-style neural postfilters]] in hybrid AEC pipelines, including:

- The proposed Bark-scale postfilter in [[sources/seidel-2024-bark-scale-nn-residual-suppression\|Seidel et al. 2024]], which augments NSNet2 with a [[concepts/bark-scale-spectral-features\|Bark-scale input mapping]] (86 bands) to improve nearend speech preservation. Achieves 235 MMACs/s with 1.58M params.
- Various Microsoft DNS Challenge baselines.

## Key Properties

| Property | Value / Description |
|----------|---------------------|
| Layer types | FC + GRU (no conv) |
| Causality | Streaming / causal |
| Mask type | Real-valued gain mask |
| Deployment | Easily implementable on dedicated DSPs and speakerphones |
| Typical params | ~1–2M (depending on width/depth) |
| Typical compute | <500 MMACs/s |

## Distinction from Other Architectures

| Architecture | Layer type | Use case | Example |
|--------------|------------|----------|---------|
| **NSNet2** | FC + GRU | Low-complexity postfilter | [[sources/seidel-2024-bark-scale-nn-residual-suppression\|Seidel 2024]] |
| [[concepts/u-net-post-filter\|U-Net]] | Conv (encoder-decoder) | Lightweight postfilter with multi-scale features | [[sources/li-2025-echofree-neural-aec\|EchoFree 2025]] |
| [[concepts/dtln\|DTLN]] | LSTM (dual signal transformation) | Fully data-driven AEC | [[sources/seidel-2024-bark-scale-nn-residual-suppression\|Seidel 2024]] baseline |
| CRN | Conv encoder + LSTM + Conv decoder | Real-time SE | [[sources/tan-2018-convolutional-recurrent-network-speech-enhancement\|Tan & Wang 2018]] |
| DeepVQE | Residual CNN + GRU + CCM | Joint AEC+NS+DR SOTA | [[sources/indenbom-2023-deepvqe\|Indenbom 2023]] |

NSNet2's advantage is its **fully-connected + recurrent** nature, which is significantly easier to implement efficiently on a speakerphone DSP than convolutional architectures — a key reason Seidel et al. chose it for deployment on speakerphones despite slightly higher parameter counts than convolutional alternatives like DeepVQE-S.

## Related Concepts

- [[concepts/bark-scale-spectral-features\|Bark-Scale Spectral Features]]
- [[concepts/percepnet-style-neural-post-filter\|PercepNet-Style Neural Post Filter]]
- [[concepts/acoustic-echo-cancellation\|Acoustic Echo Cancellation]]
- [[concepts/dtln\|DTLN]]
- [[concepts/speech-enhancement\|Speech Enhancement]]
- [[concepts/complex-compressed-mse\|Complex Compressed MSE (CCMSE)]]

## Related Sources

- [[sources/seidel-2024-bark-scale-nn-residual-suppression\|Seidel, Mowlaee & Fingscheidt 2024]] — adopts NSNet2 as the postfilter backbone with an added Bark-scale input mapping
