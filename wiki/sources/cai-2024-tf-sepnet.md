---
type: source
created: 2026-05-20
updated: 2026-05-20
sources:
  - raw/papers/cai-2024-tf-sepnet/full-text.md
  - https://doi.org/10.1109/ICASSP48485.2024.10447999
  - zotero://select/items/0_FYGJZNTZ
tags:
  - acoustic-scene-classification
  - convolutional-neural-networks
  - low-complexity-models
  - effective-receptive-field
  - time-frequency-separate-convolutions
  - adaptive-residual-normalization
---

# Cai, Zhang & Li 2024: TF-SepNet

**Authors**: [[entities/yiqiang-cai|Yiqiang Cai]], [[entities/peihong-zhang|Peihong Zhang]] & [[entities/shengchen-li|Shengchen Li]]
**Institution**: School of Advanced Technology, Xi'an Jiaotong-Liverpool University (XJTLU), Suzhou, China
**Venue**: ICASSP 2024 - 2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)
**Year**: 2024
**Type**: Conference Paper
**arXiv**: [2309.08200](http://arxiv.org/abs/2309.08200)
**DOI**: [10.1109/ICASSP48485.2024.10447999](https://doi.org/10.1109/ICASSP48485.2024.10447999)
**Zotero**: [FYGJZNTZ](zotero://select/items/0_FYGJZNTZ)

## Summary

This paper presents **TF-SepNet** (Time-Frequency Separate Network), an extremely efficient convolutional neural network (CNN) architecture designed for low-complexity **Acoustic Scene Classification (ASC)**. Traditional ASC systems typically stack consecutive 1D kernels (e.g., $k \times 1$ followed by $1 \times k$) to reduce complexity compared to 2D kernels. In contrast, TF-SepNet introduces a parallel processing approach using **Time-Frequency Separate Convolutions (TF-SepConvs)**, where feature maps are split along the channel dimension and processed independently by frequential ($k \times 1$) and temporal ($1 \times k$) paths. By combining separate path outputs, TF-SepNet achieves state-of-the-art accuracy on the TAU Urban Acoustic Scene 2022 Mobile development dataset with up to a 59% reduction in MACs and a 39% reduction in parameter count compared to the competitive BC-ResNet baseline. A core contribution is the demonstration that parallel separate kernels result in a significantly larger **Effective Receptive Field (ERF)**, enabling the model to capture richer time-frequency acoustic structures.

---

## Problem Formulation

### ASC Model Complexity Trade-offs
Acoustic scene classification requires identifying environmental sounds (e.g., airports, parks) on resource-constrained edge devices, necessitating low model complexity. Traditional CNN architectures use 2D kernels ($k \times k$). To reduce parameters, recent systems employ consecutive 1D kernels ($k \times 1$ and $1 \times k$), where:
- Parameters for a 2D kernel: $k^2$
- Parameters for consecutive 1D kernels: $2k$ (a reduction of $\frac{2}{k}$ times)

However, consecutive 1D kernels still process features sequentially and might restrict the receptive field or fail to capture independent frequential and temporal variations optimally.

### Disentanglement of Time-Frequency Information
Audio signals inherently present distinct time and frequency patterns. Rather than using additional high-cost pre-processing steps like Harmonic-Percussive Source Separation (HPSS) to separate these components, the authors propose embedding the principle of time-frequency disentanglement directly into the convolutional blocks.

![[raw/papers/cai-2024-tf-sepnet/figures/x1.png|Simplified diagrams of 1D-kernel design approaches]]
*Figure 1: Simplified diagrams of two 1D-kernel-based design approaches in CNNs. (a) Consecutive kernels sequentially apply temporal and frequential convolutions. (b) The proposed separate kernels process time and frequency features in parallel.*

---

## Methodology

### 1. Time-Frequency Separate Convolutions (TF-SepConvs)
The core component of TF-SepNet is the TF-SepConvs module, which splits channels to process the frequential and temporal axes independently and in parallel:

1. **Transition Layer**: A $1\times 1$ pointwise convolution maps the input features from $C$ channels to $C'$ channels:
   $$x \in \mathbb{R}^{C\times F\times T} \rightarrow \mathbb{R}^{C^{\prime}\times F \times T}$$
2. **Channel Shuffle**: A shuffle unit establishes connections of feature maps between channel groups to prevent channel isolation.
3. **Channel Splitting**: The feature map is split evenly by channels into two halves:
   $$x^{(f)}, x^{(t)} \in \mathbb{R}^{C^{\prime}/2\times F\times T}$$
4. **Frequential Path**: Processes $x^{(f)}$ using a $3\times 1$ depthwise convolution ($d_{3\times 1}$), frequency average pooling, and a $1\times 1$ pointwise convolution ($p_{1\times 1}$) to obtain a 1D vector $v^{(f)} \in \mathbb{R}^{C^{\prime}/2\times 1\times T}$:
   $$v^{(f)} = p_{1\times 1}\left(\frac{1}{F}\sum_{i=1}^{F}d_{3\times 1}(x_{ij}^{(f)})\right)$$
   This is broadcasted back to 2D via addition:
   $$\hat{x}^{(f)} = \sum_{j=1}^{T}(x_{ij}^{(f)} + v_{j}^{(f)}) \in \mathbb{R}^{C'/2 \times F \times T}$$
5. **Temporal Path**: Processes $x^{(t)}$ using a $1\times 3$ depthwise convolution ($d_{1\times 3}$), temporal average pooling, and a $1\times 1$ pointwise convolution ($p_{1\times 1}$) to get $v^{(t)} \in \mathbb{R}^{C^{\prime}/2\times F\times 1}$:
   $$v^{(t)} = p_{1\times 1}\left(\frac{1}{T}\sum_{j=1}^{T}d_{1\times 3}(x_{ij}^{(t)})\right)$$
   This is broadcasted back to 2D:
   $$\hat{x}^{(t)} = \sum_{i=1}^{F}(x_{ij}^{(t)} + v_{i}^{(t)}) \in \mathbb{R}^{C'/2 \times F \times T}$$
6. **Concatenation**: The outputs of both paths are concatenated along the channel dimension to yield the output feature $y \in \mathbb{R}^{C^{\prime}\times F\times T}$:
   $$y = [\hat{x}^{(f)}, \hat{x}^{(t)}]$$

![[raw/papers/cai-2024-tf-sepnet/figures/x2.png|TF-SepConvs block diagram]]
*Figure 2: Left: Visualization of the Time-Frequency Separate Convolutions (TF-SepConvs) module. Right: Transformation of feature maps. DWConv is depthwise convolution, PWConv is pointwise convolution, and Shuffle is the channel shuffle.*

### 2. Macro-Architecture
TF-SepNet adapts the macro-structure of BC-ResNet, inserting MaxPool layers for downsampling and plugging in **Adaptive Residual Normalization (AdaResNorm)**.

| Output Shape | Layer / Block | Kernel ($k$) | Stride ($s$) | Padding ($p$) |
|--------------|---|---|---|---|
| $1, F, T$ | Input spectrogram | - | - | - |
| $C/2, F/2, T/2$ | ConvBnRelu | 3 | 2 | 1 |
| $2C, F/4, T/4$ | ConvBnRelu (group $g = C/2$) | 3 | 2 | 1 |
| $C, F/4, T/4$ | TF-SepConvs $\times 2$ | - | - | - |
| $C, F/8, T/8$ | MaxPool | 2 | 2 | 0 |
| $1.5C, F/8, T/8$ | TF-SepConvs $\times 2$ | - | - | - |
| $1.5C, F/16, T/16$| MaxPool | 2 | 2 | 0 |
| $2C, F/16, T/16$ | TF-SepConvs $\times 2$ | - | - | - |
| $2.5C, F/16, T/16$| TF-SepConvs $\times 3$ | - | - | - |
| $10, F/16, T/16$ | Conv | 1 | 1 | 0 |
| $10, 1, 1$ | AvgPool (Classifier output) | - | - | - |

*Table 1: Macro-architecture of TF-SepNet.*

---

## Experimental Setup

- **Dataset**: TAU Urban Acoustic Scene 2022 Mobile development dataset (10 acoustic scenes, multiple recording devices, official 7:3 split).
- **Audio Preprocessing**: Down-sampled to 32 kHz. STFT extracted with window size 3072 and hop size 500. A Mel-scaled filter bank with 256 frequency bins and 4096 FFT maps the STFT to Mel-spectrograms, converted to Log-Mel.
- **Training Configurations**:
  - Epochs: 100 epochs, Adam optimizer (default settings), batch size 32.
  - Learning Rate: Warmup from 0 to 0.01 over the first 5 epochs, followed by cosine annealing decay to 0.
  - Regularization / Augmentation: Mixup ($\alpha = 0.3$) and Freq-MixStyle ($\alpha = 0.3, p = 0.7$).

---

## Results

### 1. Classification Performance and Complexity Comparison
TF-SepNet is compared against consecutive-kernel models: BC-ResNet (1st place in DCASE 2021) and BC-Res2Net (2nd place in DCASE 2022).

| Model | Accuracy / $\%$ | MACs / M | Parameters / K |
|-------|---|---|---|
| DCASE 2022 Baseline | 42.9 | 29.2 | 46.5 |
| BC-ResNet-40 | 57.1 | 17.2 | 88.1 |
| BC-Res2Net-40 | 59.1 | 17.2 | 85.8 |
| **TF-SepNet-40 (ours)** | **60.0** | **7.0** | **53.4** |
| BC-ResNet-80 | 58.4 | 45.8 | 315.0 |
| BC-Res2Net-80 | 59.6 | 42.7 | 307.0 |
| **TF-SepNet-80 (ours)** | **61.6** | **24.2** | **196.7** |

*Table 2: Performance on the test set of the TAU Urban Acoustic Scene 2022 Mobile development dataset.*

### 2. Effective Receptive Field (ERF) Analysis
The larger receptive field of TF-SepNet is analyzed by tracking the high-contribution area ratio ($r$) for different contribution thresholds ($t$):

| Model | $r$ ($t = 20\%$) | $r$ ($t = 30\%$) | $r$ ($t = 50\%$) |
|---|---|---|---|
| BC-ResNet-40 | 9.6 $\%$ | 17.3 $\%$ | 39.3 $\%$ |
| BC-Res2Net-40 | 9.9 $\%$ | 18.9 $\%$ | 39.8 $\%$ |
| **TF-SepNet-40 (ours)** | **13.9 $\%$** | **22.5 $\%$** | **43.8 $\%$** |

*Table 3: Statistical analysis of Effective Receptive Fields (ERF). A larger area ratio $r$ represents a more uniform contribution distribution, indicating a larger receptive field.*

![[raw/papers/cai-2024-tf-sepnet/figures/erf.png|Effective Receptive Fields visualization]]
*Figure 3: Effective Receptive Field (ERF) visualization. TF-SepNet shows a significantly broader and more uniform distribution of high-intensity regions along the time and frequency axes compared to consecutive kernels, allowing the network to capture wider contextual structures.*

### 3. Ablation Study
Ablation results on key architectural features highlight their impact:

| Model Version | Accuracy / $\%$ | MACs / M | Parameters / K |
|---|---|---|---|
| **TF-SepNet-40** | **60.0** | **7.03** | **53.4** |
| w/o shuffle | 59.5 | 7.03 | 53.4 |
| w/o freq path | 56.7 | 7.80 | 80.0 |
| w/o temp path | 57.5 | 6.96 | 80.0 |
| w/o AdaResNorm | 58.5 | 7.03 | 52.3 |

*Table 4: Ablation study showing the importance of separate time-frequency paths, channel shuffling, and AdaResNorm.*

---

## Key Contributions

1. **Parallel 1D-Kernel Design**: Shifted from sequential (consecutive) 1D kernels to parallel (separate) 1D kernels for processing time and frequency dimensions.
2. **TF-SepConvs Block**: Designed a modular block featuring pointwise convolutions, channel shuffling, channel splitting, depthwise separable 1D convolutions with average pooling broadcasting, and concatenation.
3. **Low Complexity + High Accuracy**: Outperformed competitive DCASE baselines, reducing Multiply-Accumulate operations (MACs) by 59% and parameters by 38-39%.
4. **Theoretical ERF Insights**: Proven that separate time-frequency paths enlarge the Effective Receptive Field (ERF) to cover a wider acoustic context.

---

## Related Concepts

- [[concepts/acoustic-scene-classification|Acoustic Scene Classification]] — The primary application domain for this model.
- [[concepts/effective-receptive-field|Effective Receptive Field]] — Theoretical explanation for TF-SepNet's performance gains.
- [[concepts/time-frequency-separate-convolutions|Time-Frequency Separate Convolutions]] — The custom parallel 1D convolution block introduced.
- [[concepts/adaptive-residual-normalization|Adaptive Residual Normalization]] — Crucial normalization technique used in the macro-architecture.
- [[concepts/bc-resnet|BC-ResNet]] — The macro-architecture baseline modified by this work.
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]] — Core building block utilized within TF-SepConvs.

---

## Related Sources

- None.
