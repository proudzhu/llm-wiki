---
type: concept
created: 2026-05-20
updated: 2026-05-20
tags:
  - deep-learning
  - neural-networks
  - acoustic-signal-processing
  - convolutional-blocks
---

# Time-Frequency Separate Convolutions

**Time-Frequency Separate Convolutions (TF-SepConvs)** is an efficient, parallel one-dimensional (1D) convolutional module designed specifically for processing 2D time-frequency representations of audio signals (e.g., Log-Mel spectrograms) in neural networks. Introduced by Cai et al. (2024), TF-SepConvs splits the input channels and processes the temporal and frequential axes in parallel, maximizing accuracy while minimizing parameters and MACs.

## Mathematical Formulation

Given an input feature map $x \in \mathbb{R}^{C \times F \times T}$ where $C$ is the channel dimension, $F$ is the frequency bins, and $T$ is the temporal frames:

### 1. Transition and Shuffle
First, a $1 \times 1$ pointwise convolution expands or shrinks the channel count from $C$ to $C'$:

$$x^{\prime} = \text{PWConv}_{1\times 1}(x) \in \mathbb{R}^{C^{\prime} \times F \times T}$$

A channel shuffle operation is applied to $x^{\prime}$ to establish information flow across channel groups. The feature map is then split evenly along the channel dimension into two halves:

$$x^{(f)}, x^{(t)} \in \mathbb{R}^{C^{\prime}/2 \times F \times T}$$

### 2. Parallel Paths with Broadcasting
The two halves are processed independently:

- **Frequential Path**: Processes frequency structures using a $k_f \times 1$ depthwise convolution (typically $k_f = 3$), frequency-wise average pooling, and a $1 \times 1$ pointwise convolution to yield a 1D vector $v^{(f)} \in \mathbb{R}^{C^{\prime}/2 \times 1 \times T}$:
  $$v^{(f)} = \text{PWConv}_{1\times 1}\left( \frac{1}{F}\sum_{i=1}^{F} \text{DWConv}_{3\times 1}(x^{(f)})_{i,j} \right)$$
  The features are broadcasted back to 2D shape by adding the 1D modulation vector:
  $$\hat{x}^{(f)}_{i,j} = x^{(f)}_{i,j} + v^{(f)}_j$$

- **Temporal Path**: Processes time structures using a $1 \times k_t$ depthwise convolution (typically $k_t = 3$), time-wise average pooling, and a $1 \times 1$ pointwise convolution to yield $v^{(t)} \in \mathbb{R}^{C^{\prime}/2 \times F \times 1}$:
  $$v^{(t)} = \text{PWConv}_{1\times 1}\left( \frac{1}{T}\sum_{j=1}^{T} \text{DWConv}_{1\times 3}(x^{(t)})_{i,j} \right)$$
  The features are broadcasted back to 2D shape:
  $$\hat{x}^{(t)}_{i,j} = x^{(t)}_{i,j} + v^{(t)}_i$$

### 3. Concatenation
Finally, the outputs from the frequential and temporal paths are concatenated along the channel dimension to produce the module's output $y \in \mathbb{R}^{C^{\prime} \times F \times T}$:

$$y = [\hat{x}^{(f)}, \hat{x}^{(t)}]$$

## Advantages over Consecutive Kernels

Unlike consecutive 1D kernels (e.g., applying a $k_f \times 1$ convolution directly followed by a $1 \times k_t$ convolution), TF-SepConvs offers two key benefits:
1. **Parallel Execution**: Frequential and temporal processing paths are independent, making them highly suitable for hardware with parallel processing units.
2. **Larger Receptive Field**: Parallel processing prevents the spatial information loss associated with cascading operations, leading to a broader and more uniform Effective Receptive Field (ERF).

## Related Concepts

- [[concepts/acoustic-scene-classification|Acoustic Scene Classification]]
- [[concepts/effective-receptive-field|Effective Receptive Field]]
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]]
- [[concepts/bc-resnet|BC-ResNet]]

## Related Sources

- [[sources/cai-2024-tf-sepnet|Cai, Zhang & Li 2024: TF-SepNet]]
