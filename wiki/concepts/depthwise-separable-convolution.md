---
type: concept
created: 2026-05-20
updated: 2026-05-21
sources:
  - raw/papers/kim-2021-broadcasted-residual-learning/full-text.md
tags:
  - deep-learning
  - neural-networks
  - computational-efficiency
---

# Depthwise Separable Convolution

**Depthwise Separable Convolution** is an efficient convolutional operation that factorizes a standard convolution into two separate steps: a **depthwise convolution** (filtering step) and a **pointwise convolution** (combination step). This factorization significantly reduces the computational cost (MACs) and parameter count of deep neural networks, making it a cornerstone for mobile and low-complexity network architectures.

---

## Mathematical Formulation

Consider an input feature map $X \in \mathbb{R}^{H \times W \times C_{in}}$, where $H$ is the height, $W$ is the width, and $C_{in}$ is the number of input channels. Let the target output have shape $H \times W \times C_{out}$.

### 1. Standard Convolution
A standard 2D convolution uses a set of filters $K \in \mathbb{R}^{D_k \times D_k \times C_{in} \times C_{out}}$, where $D_k$ is the spatial kernel size.

- **Parameters**: 
  $$P_{std} = D_k \times D_k \times C_{in} \times C_{out}$$
- **MACs (Multiplication-Accumulation operations)**:
  $$M_{std} = D_k \times D_k \times C_{in} \times C_{out} \times H \times W$$

---

### 2. Depthwise Separable Convolution Steps

#### Step 1: Depthwise Convolution (DWConv)
Apply a single spatial filter to each input channel independently. The depthwise kernel is $K_{dw} \in \mathbb{R}^{D_k \times D_k \times C_{in} \times 1}$.

- **Operation**:
  $$\hat{Y}_{h, w, c} = \sum_{i=-\lfloor D_k/2 \rfloor}^{\lfloor D_k/2 \rfloor} \sum_{j=-\lfloor D_k/2 \rfloor}^{\lfloor D_k/2 \rfloor} K_{dw}(i, j, c) \cdot X(h+i, w+j, c)$$
  where $c \in \{1, \dots, C_{in}\}$.
- **Parameters**:
  $$P_{dw} = D_k \times D_k \times C_{in}$$
- **MACs**:
  $$M_{dw} = D_k \times D_k \times C_{in} \times H \times W$$

#### Step 2: Pointwise Convolution (PWConv)
Compute a linear combination of the depthwise output channels using a $1 \times 1$ convolution. The pointwise kernel is $K_{pw} \in \mathbb{R}^{1 \times 1 \times C_{in} \times C_{out}}$.

- **Operation**:
  $$Y_{h, w, j} = \sum_{c=1}^{C_{in}} K_{pw}(1, 1, c, j) \cdot \hat{Y}_{h, w, c}$$
  where $j \in \{1, \dots, C_{out}\}$.
- **Parameters**:
  $$P_{pw} = C_{in} \times C_{out}$$
- **MACs**:
  $$M_{pw} = C_{in} \times C_{out} \times H \times W$$

---

### 3. Total Savings and Complexity Reduction

Summing the parameters and MACs for both steps:

- **Total Parameters**:
  $$P_{dw\_sep} = D_k^2 \cdot C_{in} + C_{in} \cdot C_{out}$$
- **Total MACs**:
  $$M_{dw\_sep} = (D_k^2 \cdot C_{in} + C_{in} \cdot C_{out}) \cdot H \times W$$

#### Efficiency Ratio
The ratio of the cost of depthwise separable convolution to standard convolution is:

$$\frac{P_{dw\_sep}}{P_{std}} = \frac{M_{dw\_sep}}{M_{std}} = \frac{D_k^2 \cdot C_{in} + C_{in} \cdot C_{out}}{D_k^2 \cdot C_{in} \cdot C_{out}} = \frac{1}{C_{out}} + \frac{1}{D_k^2}$$

For a standard $3 \times 3$ kernel ($D_k = 3$) and large $C_{out}$, this yields a computational and parameter saving of approximately **$8$ to $9$ times** (saving $\sim 89\%$ of standard convolution cost).

---

## Related Concepts

- [[concepts/neural-networks|Neural Networks]]
- [[concepts/bc-resnet|BC-ResNet]]
- [[concepts/time-frequency-separate-convolutions|Time-Frequency Separate Convolutions]]
- [[concepts/acoustic-scene-classification|Acoustic Scene Classification]]

## Related Sources

- [[sources/kim-2021-broadcasted-residual-learning|Kim, Chang, Lee & Sung 2021: Broadcasted Residual Learning]]
- [[sources/cai-2024-tf-sepnet|Cai, Zhang & Li 2024: TF-SepNet]]
