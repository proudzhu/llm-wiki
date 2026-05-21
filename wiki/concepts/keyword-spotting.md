---
type: concept
created: 2026-05-21
updated: 2026-05-21
sources:
  - raw/papers/kim-2021-broadcasted-residual-learning/full-text.md
tags:
  - speech-processing
  - acoustic-signal-processing
  - edge-ai
---

# Keyword Spotting

**Keyword spotting** (KWS) is the task of detecting predefined spoken keywords or commands in an audio stream. It is central to wake-word detection and voice interaction on resource-constrained devices such as phones, earbuds, and smart speakers.

## Problem Setting

A KWS model maps an acoustic feature sequence, often a log-Mel spectrogram $X \in \mathbb{R}^{F \times T}$, to a fixed set of command classes:

$$\hat{y} = \arg\max_c p(c \mid X)$$

Typical small-vocabulary benchmarks include Google Speech Commands, where models classify ten command words plus unknown and silence classes.

## Design Constraints

KWS systems usually run continuously, so architecture design must balance:

- **Accuracy**: low false reject and false accept rates for target commands.
- **Latency**: near-real-time inference for wake-word and command response.
- **Memory**: small model size for embedded deployment.
- **Compute**: low multiply-accumulate operations for battery-powered devices.

## Efficient CNN Approaches

[[concepts/bc-resnet|BC-ResNet]] shows that KWS benefits from preserving frequency-aware structure while shifting most computation to temporal operations. Its broadcasted residual blocks process local frequency information, collapse features over frequency, apply temporal depthwise separable convolution, and broadcast the residual back to the 2D time-frequency map.

## Related Concepts

- [[concepts/broadcasted-residual-learning|Broadcasted Residual Learning]]
- [[concepts/bc-resnet|BC-ResNet]]
- [[concepts/subspectral-normalization|SubSpectral Normalization]]
- [[concepts/spectrogram-analysis|Spectrogram Analysis]]
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]]

## Related Sources

- [[sources/kim-2021-broadcasted-residual-learning|Kim, Chang, Lee & Sung 2021: Broadcasted Residual Learning]]
