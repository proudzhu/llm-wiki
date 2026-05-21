---
type: concept
created: 2026-05-20
updated: 2026-05-21
sources:
  - raw/papers/kim-2021-broadcasted-residual-learning/full-text.md
  - raw/papers/cai-2024-tf-sepnet/full-text.md
tags:
  - deep-learning
  - neural-networks
  - keyword-spotting
  - acoustic-signal-processing
---

# BC-ResNet

**BC-ResNet** (Broadcasting-Residual Network) is a highly efficient convolutional neural network architecture for acoustic classification tasks such as [[concepts/keyword-spotting|keyword spotting]] and [[concepts/acoustic-scene-classification|acoustic scene classification]]. It was introduced by Kim, Chang, Lee & Sung at INTERSPEECH 2021 and later became a common baseline macro-architecture for low-complexity audio classification models such as TF-SepNet.

## Core Idea

BC-ResNet is built around [[concepts/broadcasted-residual-learning|Broadcasted Residual Learning]], which bridges 1D temporal convolutions and 2D frequency-temporal processing. In processing spectrogram features $X \in \mathbb{R}^{C \times F \times T}$, standard $3 \times 3$ 2D convolutions preserve local time-frequency structure but are computationally expensive. Pure $1 \times 3$ temporal convolutions reduce computation but lose frequency-dependent locality.

BC-ResNet resolves this by applying a lightweight frequency-aware 2D operation, averaging over frequency, processing the compressed temporal representation, and broadcasting the temporal residual back across frequency.

## Broadcasted Residual Block

Given intermediate features $x \in \mathbb{R}^{C \times F \times T}$:

1. **Frequency-wise processing**: apply a $3 \times 1$ frequency-depthwise convolution to capture local frequency patterns.
2. **SubSpectral Normalization**: normalize frequency sub-bands separately using [[concepts/subspectral-normalization|SubSpectral Normalization]].
3. **Temporal compression**: average the feature map along the frequency axis to create a 1D temporal representation $x_{1D} \in \mathbb{R}^{C \times 1 \times T}$.
4. **1D temporal convolution**: process temporal features using a $1 \times 3$ temporal depthwise convolution plus pointwise projection:
   $$y_{1D} = f_1(avgpool(f_2(x))) \in \mathbb{R}^{C \times 1 \times T}$$
5. **Broadcasting**: expand $y_{1D}$ back to 2D and add it to the residual path:
   $$y = x + f_2(x) + BC(y_{1D})$$

This broadcasting operation modulates 2D feature maps with low-complexity temporal activations while preserving a frequency-aware auxiliary residual.

![[raw/papers/kim-2021-broadcasted-residual-learning/figures/bc-resblock.png|BC-ResBlock architecture]]
*Figure 1: The BC-ResBlock combines frequency-depthwise convolution, SSN, temporal depthwise separable convolution, and broadcasted residual addition.*

## Architecture and Scaling

The base BC-ResNet-1 uses a front $5 \times 5$ convolution followed by four stages of BC-ResBlocks with repeat counts $(2, 2, 4, 4)$. It then applies a final depthwise convolution, $1 \times 1$ projection, global average pooling, and classifier.

BC-ResNet scales by a width coefficient $\tau$: BC-ResNet-$\tau$ multiplies channel widths while keeping depth fixed. This makes the model family easy to adapt to specific memory and compute budgets.

## Keyword Spotting Performance

On Google Speech Commands, BC-ResNet reaches a strong accuracy-efficiency frontier:

| Model | v1 Accuracy | v2 Accuracy | Parameters | Multiplies |
|---|---:|---:|---:|---:|
| BC-ResNet-1 | 96.6 | 96.9 | 9.2k | 3.1M |
| BC-ResNet-3 | 97.6 | 98.2 | 54.2k | 16.2M |
| BC-ResNet-8 | 98.0 | 98.7 | 321k | 89.1M |

BC-ResNet-3 outperforms MHAtt-RNN with 13.7× fewer parameters, while BC-ResNet-8 sets state-of-the-art results reported in the paper.

## Influence

BC-ResNet has served as a baseline macro-architecture for later low-complexity audio classification work. [[sources/cai-2024-tf-sepnet|TF-SepNet]] adapts its efficient audio-CNN structure for acoustic scene classification and replaces the original broadcasted block with parallel time-frequency separate convolutions.

## Related Concepts

- [[concepts/keyword-spotting|Keyword Spotting]]
- [[concepts/broadcasted-residual-learning|Broadcasted Residual Learning]]
- [[concepts/subspectral-normalization|SubSpectral Normalization]]
- [[concepts/acoustic-scene-classification|Acoustic Scene Classification]]
- [[concepts/time-frequency-separate-convolutions|Time-Frequency Separate Convolutions]]
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]]
- [[concepts/adaptive-residual-normalization|Adaptive Residual Normalization]]

## Related Sources

- [[sources/kim-2021-broadcasted-residual-learning|Kim, Chang, Lee & Sung 2021: Broadcasted Residual Learning]]
- [[sources/cai-2024-tf-sepnet|Cai, Zhang & Li 2024: TF-SepNet]]
