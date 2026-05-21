---
type: source
created: 2026-05-21
updated: 2026-05-21
sources:
  - raw/papers/kim-2021-broadcasted-residual-learning/full-text.md
  - https://doi.org/10.48550/arXiv.2106.04140
  - https://arxiv.org/abs/2106.04140
  - zotero://select/items/0_EFJM3USE
tags:
  - keyword-spotting
  - efficient-neural-networks
  - acoustic-signal-processing
  - broadcasted-residual-learning
  - bc-resnet
---

# Kim, Chang, Lee & Sung 2021: Broadcasted Residual Learning

**Authors**: [[entities/byeonggeun-kim|Byeonggeun Kim]], [[entities/simyung-chang|Simyung Chang]], [[entities/jinkyu-lee|Jinkyu Lee]] & [[entities/dooyong-sung|Dooyong Sung]]
**Institution**: Qualcomm AI Research
**Venue**: INTERSPEECH 2021
**Year**: 2021
**Type**: Conference Paper / arXiv Preprint
**arXiv**: [2106.04140](https://arxiv.org/abs/2106.04140)
**DOI**: [10.48550/arXiv.2106.04140](https://doi.org/10.48550/arXiv.2106.04140)
**Code**: [Qualcomm-AI-research/bcresnet](https://github.com/Qualcomm-AI-research/bcresnet)
**Zotero**: [EFJM3USE](zotero://select/items/0_EFJM3USE)

## Summary

Kim et al. introduce **broadcasted residual learning**, a low-complexity residual mapping for keyword spotting that combines inexpensive 1D temporal convolutions with frequency-aware 2D processing. The resulting **BC-ResNet** family achieves state-of-the-art Google Speech Commands accuracy while using substantially fewer parameters and multiply operations than earlier KWS architectures.

## Problem Formulation

[[concepts/keyword-spotting|Keyword spotting]] models must detect a small vocabulary of wake words or speech commands on edge devices where memory, latency, and multiply-accumulate operations are tightly constrained. Existing CNN approaches face a trade-off:

- **1D temporal convolutions** reduce computation but discard convolutional inductive bias over frequency.
- **2D frequency-temporal convolutions** preserve local time-frequency structure but increase parameters and MACs.
- **Efficient residual CNNs** such as depthwise-separable ResNets still need a mechanism that keeps frequency awareness without paying the full 2D convolution cost in every residual branch.

The paper frames the goal as building an acoustic classifier over log-Mel spectrograms that preserves useful 2D frequency structure while moving most residual computation into 1D temporal operations.

## Methodology

### Broadcasted Residual Learning

A conventional residual block is:

$$y = x + f(x)$$

where the residual branch and shortcut have the same dimensionality. Broadcasted residual learning decomposes the residual function into a 2D frequency-aware operation $f_2$ and a 1D temporal operation $f_1$:

$$y = x + BC(f_1(avgpool(f_2(x))))$$

where $avgpool$ averages along the frequency axis and $BC$ broadcasts the resulting temporal feature back across the frequency dimension.

The full BC-ResBlock adds an auxiliary 2D residual branch:

$$y = x + f_2(x) + BC(f_1(avgpool(f_2(x))))$$

This design preserves a 2D path for frequency-local information while applying the expensive depthwise separable temporal and pointwise operations on a compressed $1 \times T$ representation.

![[raw/papers/kim-2021-broadcasted-residual-learning/figures/bc-resblock.png|Broadcasted residual learning and BC-ResBlock]]
*Figure 1: Broadcasted residual learning averages frequency-aware 2D features into temporal features, processes them with temporal convolutions, then broadcasts the residual back to the 2D feature map.*

### BC-ResBlock

Each BC-ResBlock contains:

- a $3 \times 1$ frequency-depthwise convolution for local frequency processing;
- [[concepts/subspectral-normalization|SubSpectral Normalization]] to normalize frequency sub-bands separately;
- frequency average pooling to convert 2D features into temporal features;
- a $1 \times 3$ temporal depthwise convolution, batch normalization, Swish activation, $1 \times 1$ pointwise convolution, and channel-wise dropout;
- broadcasted addition back into the 2D residual representation.

Transition blocks add a front $1 \times 1$ convolution with batch normalization and ReLU when the stage changes channel width, and omit the identity shortcut.

### BC-ResNet Family

The base **BC-ResNet-1** uses a front $5 \times 5$ convolution, four stages of BC-ResBlocks with repeats $(2, 2, 4, 4)$, a final $5 \times 5$ depthwise convolution, pointwise projection, average pooling, and a $1 \times 1$ classifier.

| Input | Operator | Repeats | Channels | Stride | Dilation |
|---|---|---:|---:|---|---|
| $1 \times 40 \times W$ | conv2d $5 \times 5$ - BN - ReLU | - | 16 | $(2,1)$ | 1 |
| $16 \times 20 \times W$ | BC-ResBlock | 2 | 8 | 1 | 1 |
| $8 \times 20 \times W$ | BC-ResBlock | 2 | 12 | $(2,1)$ | $(1,2)$ |
| $12 \times 10 \times W$ | BC-ResBlock | 4 | 16 | $(2,1)$ | $(1,4)$ |
| $16 \times 5 \times W$ | BC-ResBlock | 4 | 20 | 1 | $(1,8)$ |
| $20 \times 5 \times W$ | DWconv $5 \times 5$ | - | 20 | 1 | 1 |
| $20 \times 1 \times W$ | conv2d $1 \times 1$ - BN - ReLU | - | 32 | 1 | 1 |
| $32 \times 1 \times W$ | avgpool | - | - | - | - |
| $32 \times 1 \times 1$ | conv2d $1 \times 1$ | - | 12 | - | - |

The family scales by width only: BC-ResNet-$\tau$ multiplies channel width by the scaling factor $\tau$, making it straightforward to fit a target device budget.

## Experimental Setup

| Component | Setting |
|---|---|
| Datasets | Google Speech Commands v1 and v2 |
| Classes | 10 command words plus unknown and silence |
| Audio | 1 s utterances, 16 kHz sampling rate |
| Features | 40-dimensional log-Mel spectrograms |
| Window / hop | 30 ms window, 10 ms frame shift |
| Augmentation | time shift, background noise, SpecAugment for larger variants |
| Normalization | SubSpectral Normalization with five sub-bands |
| Optimizer | SGD with momentum 0.9, weight decay 0.001 |
| Training | 200 epochs, batch size 100, 5-epoch warmup to LR 0.1, cosine decay |
| Evaluation | top-1 test accuracy, parameter count, multiply operations |

## Results

### Impact of Broadcasted Residual Learning

| Model | v1 Accuracy | v2 Accuracy | Parameters | Multiplies |
|---|---:|---:|---:|---:|
| ResNet-1D (w=2) | 95.0 ± 0.25 | 95.7 ± 0.46 | 27.3k | 3.2M |
| ResNet-2D (w=1) | 94.8 ± 0.42 | 94.9 ± 0.32 | 7.9k | 5.9M |
| ResNet-2D w/ SSN | 95.5 ± 0.22 | 95.6 ± 0.24 | 9.4k | 5.9M |
| BC-ResNet-Attn | 96.0 ± 0.14 | 96.2 ± 0.24 | 9.2k | 3.1M |
| **BC-ResNet-1** | **96.6 ± 0.21** | **96.9 ± 0.30** | **9.2k** | **3.1M** |

BC-ResNet-1 outperforms both pure 1D and pure 2D residual baselines. The comparison shows that broadcasted residual mapping is not merely an attention replacement: the attention variant is 0.6-0.7 percentage points worse than additive broadcasted residual learning.

### Ablation Findings

| Variant | v1 Accuracy | v2 Accuracy | Parameters | Multiplies |
|---|---:|---:|---:|---:|
| BC-ResNet-1 | 96.6 ± 0.21 | 96.9 ± 0.30 | 9.2k | 3.1M |
| w/o auxiliary 2D residual | 96.2 ± 0.20 | 96.5 ± 0.10 | 9.2k | 3.1M |
| w/o shortcut | 96.4 ± 0.34 | 96.8 ± 0.18 | 9.2k | 3.1M |
| w/o SSN | 96.1 ± 0.11 | 96.5 ± 0.12 | 7.8k | 3.1M |
| w/o 2D residual and SSN | 95.4 ± 0.29 | 95.7 ± 0.32 | 7.9k | 3.1M |

The auxiliary 2D residual and SSN both mitigate information loss from collapsing the frequency axis. Removing both causes the largest degradation, supporting the claim that BC-ResNet works because it preserves frequency-aware structure while compressing computation.

### Comparison with Prior KWS Models

| Model | v1 Accuracy | v2 Accuracy | Parameters | Multiplies |
|---|---:|---:|---:|---:|
| TC-ResNet14-1.5 | 96.6 | - | 305k | 6.7M |
| TENet12 | 96.6 | - | 100k | 2.9M |
| BC-ResNet-1 | 96.6 | 96.9 | 9.2k | 3.1M |
| MatchboxNet-3x1x64 | 97.2 | 96.9 | 77k | 9.3M |
| MHAtt-RNN | 97.2 | 98.0 | 743k | 22.7M |
| BC-ResNet-3 | 97.6 | 98.2 | 54.2k | 16.2M |
| BC-ResNet-6 | 97.9 | 98.6 | 188k | 53.1M |
| **BC-ResNet-8** | **98.0** | **98.7** | **321k** | **89.1M** |

BC-ResNet-3 exceeds MHAtt-RNN accuracy with 13.7× fewer parameters. BC-ResNet-8 reaches 98.0% and 98.7% on Speech Commands v1 and v2, respectively, while remaining 2.3× smaller than MHAtt-RNN.

## Key Contributions

1. **Broadcasted residual learning**: A residual formulation that averages 2D features over frequency, applies low-cost temporal processing, then broadcasts the residual to the original 2D feature map.
2. **BC-ResNet architecture**: A small-footprint KWS network that combines frequency-depthwise convolution, SSN, temporal depthwise separable convolution, auxiliary 2D residuals, and width-only scaling.
3. **Efficiency-accuracy frontier**: State-of-the-art Speech Commands results with strong parameter efficiency, including 96.6% v1 accuracy with only 9.2k parameters and 98.7% v2 accuracy with 321k parameters.
4. **Ablation evidence**: Shows that frequency-aware SSN, auxiliary 2D residuals, and broadcasted additive mapping all contribute to performance.

## Related Concepts

- [[concepts/keyword-spotting|Keyword Spotting]] — the target task for BC-ResNet.
- [[concepts/broadcasted-residual-learning|Broadcasted Residual Learning]] — the residual formulation introduced by the paper.
- [[concepts/bc-resnet|BC-ResNet]] — the architecture family built from broadcasted residual blocks.
- [[concepts/subspectral-normalization|SubSpectral Normalization]] — frequency-subband normalization used in BC-ResBlocks.
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]] — the efficient convolution factorization used in temporal and frequency components.
- [[concepts/spectrogram-analysis|Spectrogram Analysis]] — the log-Mel input representation used for KWS.
- [[concepts/neural-networks|Neural Networks]] — broader family of architectures including residual CNNs.

## Related Synthesis

- None.
