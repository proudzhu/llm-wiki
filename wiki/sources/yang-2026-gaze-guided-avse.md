---
type: source
created: 2026-04-22
updated: 2026-04-22
sources:
  - zotero://select/items/0_3UH8NL5G
tags:
  - speech-enhancement
  - gaze-tracking
  - audio-visual
  - cocktail-party-problem
  - mamba
---

# Yang et al. (2026): GG-AVSE - Gaze-Guided Audio-Visual Speech Enhancement

> **论文**：Tracking listener attention: gaze-guided audio-visual speech enhancement framework
> **作者**：Hsiang-Cheng Yang, et al.
> **发表**：arXiv 2026 (2604.08359)
> **阅读时长**：约 15 分钟
> **难度**：⭐⭐⭐⭐
> **前置知识**：Audio-Visual Speech Enhancement (AVSE)、Mamba 架构 (SSM)、目标检测 (YOLO)、眼动追踪

---

## TL;DR

本文提出了一种注视引导的音视频语音增强 (GG-AVSE) 框架，旨在解决多发言人环境下的"鸡尾酒会效应"。核心创新是引入了 **GG-VM (Gaze-Guided Visual Module)**，利用用户的注视点作为监督信号，动态从 YOLO5Face 检测到的多个脸部中锁定目标。该框架基于 **AVSEMamba** 架构，利用选择性状态空间模型 (SSM) 的线性复杂度优势，实现了高性能、低延迟的目标发言人提取。

---

## 论文概述

**问题**：传统的 AVSE 系统假设输入的视频流即为目标发言人，但在真实场景（如智能眼镜、AR 硬件）中，视野内常有多个面孔，系统难以自动判断用户想听谁。

**方案**：集成注视追踪硬件（Ganzin Sol Glasses），通过空间距离与 IoU 匹配算法锁定目标人脸，并将其视觉特征输入轻量化的 AVSEMamba 模型。

**贡献**：
1.  **GG-VM 模块**：解耦了目标选择与语音增强任务，通过注视点关联面部特征。
2.  **Mamba 融合策略**：对比了零样本合并 (Zero-shot merging) 与局部视觉微调 (Partial visual fine-tuning) 两种策略。
3.  **AVSEC2-Gaze 数据集**：首个包含真实注视点轨迹的音视频增强基准数据集。

---

## 核心方法

### 1. GG-VM (Gaze-Guided Visual Module)

![GG-VM 架构图](raw/assets/yang-2026-avse/images/p3_fig1.png)
*(图示：注视点信号与 YOLO5Face 联合锁定目标面部的流程)*

识别逻辑采用综合评分函数：
$$Score(i) = \gamma \cdot D(i) + (1-\gamma) \cdot IoU(i)$$
-   $D(i)$：注视点与面部中心的欧氏距离倒数。
-   $IoU(i)$：注视区域与面部检测框的重叠度。
-   $\gamma = 0.75$（经验值）：平衡了几何接近度与区域重合度。

### 2. AVSEMamba 增强架构

相比 Transformer 的 $O(L^2)$ 复杂度，GG-AVSE 采用 **Mamba (Selective SSM)**：
-   **线性缩放**：在处理长序列时具有极高的推理速度。
-   **时频融合**：视觉编码器提取的脸部特征通过 Time-Frequency Mamba Blocks 与音频频谱图进行深度交互。

### 3. 模型集成策略

-   **Zero-shot Merging**：直接将锁定的人脸特征输入预训练模型，验证注视点作为通用索引的有效性。
-   **Partial Visual Fine-tuning**：仅解冻视觉编码器部分，通过注视引导的真实面孔数据进行针对性优化，以提升在极端姿态下的鲁棒性。

---

## 实验分析

研究在 AVSEC2-Gaze 数据集上对比了注视引导模型与注视感知基准模型：

**关键性能指标**：
-   **PESQ (语音质量)**：从 2.370 提升至 **2.609** (↑ 10.08%)。
-   **STOI (可懂度)**：从 0.8802 提升至 **0.9258** (↑ 5.18%)。
-   **SI-SDR (信源失真比)**：从 9.16 dB 提升至 **11.33 dB** (↑ 23.69%)。
-   **低延迟**：得益于 Mamba 架构，模型在边缘 GPU 上的推理延迟较 Conformer 降低了约 **40%**。

---

## 深度理解问答

### Q1: 为什么在锁定发言人时，单一的注视点坐标是不够的？

**注视点的抖动与漂移**。
由于人眼的扫视 (Saccades) 与微震，注视点坐标通常存在高频波动。如果仅根据坐标锁定面部，在面部密集的场景下会导致目标频繁切换。引入 IoU (区域重叠) 项可以将注视点扩展为一个注视区域，通过概率覆盖的方式显著提高了在目标面部运动时的追踪稳定性。

### Q2: Mamba 架构在 AVSE 中相比 Transformer 有哪些本质优势？

**递归性的记忆与线性的开销**。
在音频流处理中，Transformer 需要缓存所有历史 Key-Value 对，内存消耗随时间步增长。Mamba 引入的选择性状态压缩机制，使得模型能以恒定的内存占用维护"听觉上下文"，这对于实时可穿戴设备（如助听器或智能眼镜）的长效运行至关重要。

### Q3: 视觉微调策略解决了什么特定的 Generalization 问题？

**域偏移 (Domain Shift)**。
通用的 face-tracking 模型在实验室环境下表现良好，但在真实注视数据中，用户注视点往往落在线条复杂的背景或发言人边缘。通过 Partial Visual Fine-tuning，模型学会了容忍注视偏差，并专注于提取与音频节奏（唇动、肌肉拉伸）最相关的视觉特征，而非仅仅识别面部。

---

## 总结

### 核心贡献
- 实现了真正意义上以人为中心的"按需增强"语音系统。
- 证明了 SSM/Mamba 架构在多模态实时交互中的优越性。

### 局限性
- 依赖佩戴专用眼动仪（如 Ganzin Sol），短期内难以在大众手机设备上普及。
- 对于快速扫视期间的系统响应平滑度仍有改进空间。

### 适用场景
- 助听器与人工耳蜗。
- 智能驾驶舱多乘员语音交互。
- VR/MR 社交协作平台。

---

## 相关概念
- [[../concepts/transparency-mode|Transparency Mode]]
- [[../concepts/voice-activity-detection|Voice Activity Detection]]
- [[../concepts/beamforming|Beamforming]]
- [[wiki/concepts/state-space-model|State-Space Model]]
- [[wiki/concepts/neural-networks|Neural Networks]]

## Related Concepts

- [[../concepts/beamforming|Beamforming]]
- [[../concepts/transparency-mode|Transparency Mode]]
- [[../concepts/voice-activity-detection|Voice Activity Detection]]
- [[wiki/concepts/neural-networks|Neural Networks]]
- [[wiki/concepts/state-space-model|State-Space Model]]

## Related Synthesis
