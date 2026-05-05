---
type: source
created: 2026-04-22
updated: 2026-04-22
sources:
  - zotero://select/items/0_97XR3LJ7
tags:
  - active-noise-control
  - feedback-anc
  - deep-learning
  - atrous-convolution
---

# Cha et al. (2023): DNoiseNet - Deep Learning-Based Feedback ANC

> **论文**：DNoiseNet: Deep learning-based feedback active noise control in various noisy environments
> **作者**：Young-Jin Cha, et al.
> **发表**：Engineering Applications of Artificial Intelligence (2023)
> **阅读时长**：约 15 分钟
> **难度**：⭐⭐⭐⭐
> **前置知识**：Feedback ANC、Atrous Convolution、RNN、系统辨识

---

## TL;DR

DNoiseNet 是一种创新的端到端深度学习 Feedback ANC 架构，通过结合空洞卷积 (Atrous Convolution) 和 Elman RNN，解决了传统线性滤波器在非平稳、非线性环境中的性能瓶颈。其核心在于引入了专门的 MLP 次级路径估算器，实现了无需外部参考信号的高性能有源降噪，在建筑工地、机舱等复杂场景下显著优于 FxLMS。

---

## 论文概述

**问题**：传统 Feedback ANC 依赖线性 IIR/FIR 滤波器，难以应对环境中的高度非线性和非平稳噪声。此外，反馈结构仅有的误差信号难以准确重建参考噪声。

**方案**：构建 DNoiseNet 复合架构，集成空洞卷积 (AConv) 提取多尺度时域特征，Elman RNN 建模全局时序依赖。

**贡献**：
1.  设计了 **ASC (Atrous Scaled Convolution)** 模块，通过指数增长的扩张率扩展感受野，而不增加计算量。
2.  提出了基于 **MLP 的次级路径估算器**，能够在线补偿电声器件（扬声器、ADC/DAC）的非线性畸变。
3.  验证了**逐样本处理 (Sample-by-sample)** 模式，将端到端延迟降至最低，避免了频域处理的帧延迟。

---

## 核心方法

### 1. 整体架构

![DNoiseNet 架构图](raw/assets/cha-2023-dnoisenet/images/p8_fig2.png)
*(图示：DNoiseNet 结合 AConv、RNN 与 FCL 的端到端映射过程)*

数据流：误差/重构参考信号 (1x20) → Casual Conv → 4x ASC Modules → Elman RNN → MLP 修正 → 反噪声输出。

### 2. ASC (Atrous Scaled Convolution) 模块

ASC 模块是 DNoiseNet 提取非线性特征的核心。它由以下部分组成：
-   **1D AConv (空洞卷积)**：扩张率按 $r \in \{2^0, 2^1, 2^2, 2^3\}$ 指数增长。
-   **SeLU 激活函数**：具备自归一化特性，确保深层网络训练的稳定性，其公式为：
    $$out = \lambda(x) \text{ if } x > 0 \text{ else } \lambda(\alpha e^x - \alpha)$$
-   **Pointwise Convolution (PW)**：用于融合不同尺度提取的特征。

### 3. MLP 次级路径估算器

由于 Feedback ANC 架构中反噪声信号 $y(n)$ 必须经过次级路径 $S(z)$ 才能被误差麦克风捕获，模型必须补偿这一过程：
-   **结构**：3 层隐藏层 (8-4-2 神经元)，使用 Tanh 激活。
-   **逻辑**：在降噪开始前通过已知信号进行离线预训练，运行期间每 15-20 秒进行一次轻量化微调（仅 65 个参数），以应对密封性变化。

---

## 实验分析

研究对比了建筑工地、豹 1 坦克机舱、Volvo 340 车内及飞机驾驶舱四种极端的非平稳环境。

**关键结论**：
-   **收敛速度**：相比需要数百次迭代的 FxLMS，DNoiseNet 在初始阶段即展现出极高的稳定性。
-   **鲁棒性**：在次级路径增益漂移或传感器位置变动的情况下，由于 SeLU 和 MLP 的共同作用，降噪量下降幅度远小于传统方法。
-   **非线性抑制**：在扬声器饱和阶段，DNoiseNet 的 MLP 模块能够有效预测并抵消谐波失真。

---

## 深度理解问答

### Q1: 为什么选择空洞卷积 (Atrous) 而不是增加标准卷积的层数？

**计算效率与感受野的权衡**。
在实时 ANC 系统中，每一层卷积都会增加处理延迟。通过指数级增加扩张率，AConv 可以在保持线性计算复杂度的同时，使感受野 (Receptive Field) 迅速覆盖更长的时间窗口，这对于捕获低频长波信号的相位特征至关重要。

### Q2: DNoiseNet 是如何实现 Sample-by-sample 处理的？

**消除频域缓冲**。
大多数 Deep ANC 采用 STFT 或重叠相加法 (OLA)，这会引入至少一个帧长 (如 20ms) 的初始延迟。DNoiseNet 将输入限制为最近的 20 个采样点，并使用纯时域算子。当新采样点到来时，通过滑动窗口更新输入并立即触发一次推理，从而将算法延迟降至硬件处理极限。

### Q3: 为什么引入 MLP 辅助路径而不是直接让主网络学习 S(z)？

**任务解耦**。
主网络负责复杂的参考噪声预测，而 MLP 专门负责物理路径建模。这种设计降低了主网络的学习负担。实验证明，带有 MLP 的架构在 RMSE 性能上提升了约 12%，因为它能够显式补偿扬声器在特定电压下的频率响应畸变。

---

## 总结

### 核心贡献
- 实现了真正意义上的 Feedback 端到端深度降噪，摆脱了对外部参考麦克风的依赖。
- 证明了小规模网络（逐样本推理）在实时嵌入式控制中的可行性。

### 局限性
- 20 个采样点的窗口长度限制了其对极低频（波长极长）噪声的建模深度。
- 缺乏在大规模多通道 (MIMO) 场景下的扩展性讨论。

### 适用场景
- 移动端入耳式耳机 (TWS)。
- 空间受限无法布置参考麦克风的驾驶舱或工业控制台。

---

## 相关概念
- [[wiki/concepts/feedback-anc|Feedback ANC]]
- [[wiki/concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[wiki/concepts/neural-networks|Neural Networks]]
- [[wiki/concepts/robust-adaptive-filtering|Robust Adaptive Filtering]]

## Related Concepts

- [[wiki/concepts/feedback-anc|Feedback ANC]]
- [[wiki/concepts/neural-networks|Neural Networks]]
- [[wiki/concepts/robust-adaptive-filtering|Robust Adaptive Filtering]]
- [[wiki/concepts/secondary-path-modeling|Secondary Path Modeling]]

## Related Synthesis
