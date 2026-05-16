---
type: concept
created: 2026-05-16
updated: 2026-05-16
sources:
  - wiki/sources/kuang-2024-lightweight-speech-enhancement-bone-air.md
tags:
  - speech-enhancement
  - deep-learning
  - architecture
  - lightweight-network
---

# DenGCAN (Densely Gated Convolutional Attention Network)

**DenGCAN** is a lightweight encoder-decoder architecture for speech enhancement that combines densely connected convolutional layers, gated convolutions, and self-attention. It was proposed by Kuang, Yang & Yang (2024) for fusing bone-conducted (BC) and air-conducted (AC) speech.

## Architecture

DenGCAN follows a convolutional encoder-decoder structure with:

### Encoder (5 dense blocks)

| Block | Input Size | Output Size |
|-------|-----------|-------------|
| Dense block 1 | 6 × T × 161 | 16 × T × 79 |
| Dense block 2 | 16 × T × 79 | 32 × T × 38 |
| Dense block 3 | 32 × T × 38 | 48 × T × 18 |
| Dense block 4 | 48 × T × 18 | 64 × T × 8 |
| Dense block 5 | 64 × T × 8 | 64 × T × 3 |

### Bottleneck (2-layer grouped sConformer)

The 64 × T × 3 encoder output is reshaped to T × 192 and fed through two sConformer layers, which model long-term temporal dependencies via self-attention. Grouping with feature rearrangement is used between layers for efficiency.

### Decoder (5 dense blocks, symmetric)

| Block | Input Size | Output Size |
|-------|-----------|-------------|
| Dense block 5 | 128 × T × 3 | 64 × T × 8 |
| Dense block 4 | 128 × T × 8 | 48 × T × 18 |
| Dense block 3 | 96 × T × 18 | 32 × T × 38 |
| Dense block 2 | 64 × T × 38 | 16 × T × 79 |
| Dense block 1 | 32 × T × 79 | 2 × T × 161 |

The channel doubling in some decoder blocks comes from concatenating the skip-connected encoder features.

### Key Components

#### Dense Block
Each dense block contains:
1. **Dense layer**: 4 convolution layers, each taking ALL preceding feature maps as input (feature reuse). Kernel (1,3), stride (1,1), 8 channels per conv.
2. **Gated layer**: Two convolutions — one for the gate (sigmoid) and one for the main path. Kernel (1,4), stride (1,2) to halve frequency dimension.

Channel progression in encoder: 6 → 16 → 32 → 48 → 64 → 64
Channel regression in decoder (from 64 → 48 → 32 → 16 → 2 output channels)

#### Attention Gate (AG) Skip-Connections
Instead of simple concatenation or PWConv-based skip-connections, DenGCAN uses [[concepts/attention-gate|attention gates]] that consider both local and global features. The AG takes the encoder feature map $\mathbf{X}_l$ and the decoder feature map $\mathbf{G}_{l+1}$, computes attention coefficients, and selectively scales the encoder features.

#### Squeezed Conformer (sConformer) Bottleneck
A lightweight variant of Conformer that uses self-attention to model long-term temporal dependencies. The sConformer can flexibly use future context frames, offering a trade-off between latency and performance. Removing sConformer (replacing with LSTM) causes a 0.114 average wb-PESQ drop.

## Key Properties

- **Parameters**: 1.03M
- **MACs**: 0.859 G (lowest among competitive models)
- **RTF on ARM Cortex-A53**: 0.649 (real-time capable)
- **RTF on x86 Kaby Lake**: 0.068
- **Causal**: Yes (can operate with 30 ms input-output latency)
- **Future context**: Optional — 0–160 ms additional latency improves wb-PESQ from 2.98 to 3.11

## Related Concepts

- [[concepts/iterative-attentional-feature-fusion|Iterative Attentional Feature Fusion (iAFF)]]
- [[concepts/attention-gate|Attention Gate (AG)]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask (cRM)]]
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]

## Related Sources

- [[sources/kuang-2024-lightweight-speech-enhancement-bone-air|Kuang, Yang & Yang 2024: A Lightweight Speech Enhancement Network Fusing Bone- and Air-Conducted Speech]]
