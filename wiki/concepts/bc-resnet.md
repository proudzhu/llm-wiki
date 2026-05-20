---
type: concept
created: 2026-05-20
updated: 2026-05-20
tags:
  - deep-learning
  - neural-networks
  - keyword-spotting
  - acoustic-signal-processing
---

# BC-ResNet

**BC-ResNet** (Broadcasting-Residual Network) is a highly efficient convolutional neural network (CNN) macro-architecture designed for acoustic classification tasks, such as keyword spotting (KWS) and acoustic scene classification (ASC), on resource-constrained edge devices. Introduced by Kim et al. (Qualcomm AI Research, 2021), the core innovation is **Broadcasted Residual Learning**, which bridges 1D temporal convolutions and 2D frequency-temporal operations.

## Theoretical Foundations

In processing 2D time-frequency audio spectrograms $X \in \mathbb{R}^{C \times F \times T}$, standard 2D convolutions ($3 \times 3$) are computationally expensive. 1D convolutions along the temporal axis ($1 \times 3$) reduce computation but lose frequency-dependent localization. 

BC-ResNet resolves this using a broadcasted residual connection, where a 1D residual function is applied to temporal features and then "broadcasted" (expanded) across the frequency axis.

### Broadcasted Residual Block

Given intermediate features $x \in \mathbb{R}^{C \times F \times T}$:

1. **Frequency-Wise Processing**: The block first extracts frequency patterns using a 2D depthwise convolution with size $3 \times 1$ (operating on frequency) or a similar localized operation.
2. **Temporal Compression**: A pooling layer averages the feature map along the frequency axis $F$ to create a 1D temporal representation $x_{1D} \in \mathbb{R}^{C \times 1 \times T}$.
3. **1D Temporal Convolution**: The 1D temporal representations are processed by a $1 \times 3$ temporal convolution:
   $$y_{1D} = \text{DWConv}_{1\times 3}(x_{1D}) \in \mathbb{R}^{C \times 1 \times T}$$
4. **Broadcasting**: The 1D feature $y_{1D}$ is expanded back to 2D by adding it element-wise to the original 2D feature map:
   $$y_{2D, c, f, t} = x_{c, f, t} + y_{1D, c, 1, t}$$

This broadcasting operation permits the network to modulate 2D feature channels with low-complexity 1D temporal activations, minimizing computation while retaining frequency awareness.

## Influence and Scaling

BC-ResNet has served as the baseline macro-architecture for many subsequent low-complexity audio classification models (such as BC-Res2Net and TF-SepNet). The depth and width of the network are typically adjusted using a scale parameter $\tau$ (e.g., BC-ResNet-40, BC-ResNet-80) which scales the channel dimensions to fit memory constraints.

## Related Concepts

- [[concepts/acoustic-scene-classification|Acoustic Scene Classification]]
- [[concepts/time-frequency-separate-convolutions|Time-Frequency Separate Convolutions]]
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]]
- [[concepts/adaptive-residual-normalization|Adaptive Residual Normalization]]

## Related Sources

- [[sources/cai-2024-tf-sepnet|Cai, Zhang & Li 2024: TF-SepNet]]
