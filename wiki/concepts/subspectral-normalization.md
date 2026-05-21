---
type: concept
created: 2026-05-21
updated: 2026-05-21
sources:
  - raw/papers/kim-2021-broadcasted-residual-learning/full-text.md
tags:
  - neural-audio-processing
  - normalization
  - acoustic-signal-processing
---

# SubSpectral Normalization

**SubSpectral Normalization** (SSN) is a normalization method for neural audio models that splits the frequency axis into sub-bands and normalizes each sub-band separately. It is designed for spectrogram-like inputs where different frequency regions can have different statistics and acoustic meanings.

## Role in BC-ResNet

In [[concepts/bc-resnet|BC-ResNet]], SSN is applied after the $3 \times 1$ frequency-depthwise convolution inside each BC-ResBlock. This gives the frequency-processing path a frequency-aware normalization step before features are averaged over frequency and processed temporally.

Kim et al.'s ablation shows that replacing SSN with batch normalization reduces BC-ResNet-1 accuracy from 96.6% to 96.1% on Speech Commands v1 and from 96.9% to 96.5% on v2. Removing both SSN and the auxiliary 2D residual causes a larger drop, showing that SSN helps preserve useful frequency information during broadcasted residual learning.

## Conceptual Form

Given a feature map $X \in \mathbb{R}^{C \times F \times T}$, SSN partitions the frequency bins into $G$ sub-bands and computes normalization statistics within each sub-band rather than across the entire frequency axis. This can reduce inter-frequency statistic mixing and retain frequency-local structure.

## Related Concepts

- [[concepts/spectrogram-analysis|Spectrogram Analysis]]
- [[concepts/broadcasted-residual-learning|Broadcasted Residual Learning]]
- [[concepts/bc-resnet|BC-ResNet]]
- [[concepts/keyword-spotting|Keyword Spotting]]

## Related Sources

- [[sources/kim-2021-broadcasted-residual-learning|Kim, Chang, Lee & Sung 2021: Broadcasted Residual Learning]]
