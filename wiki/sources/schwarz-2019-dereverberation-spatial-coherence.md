---
type: source
created: 2026-04-25
updated: 2026-04-25
sources:
tags:
  - dereverberation
  - spatial-coherence
  - speech-recognition
  - multichannel
  - spectral-enhancement
  - doctoral-dissertation
---

# Schwarz 2019: Dereverberation and Robust Speech Recognition Using Spatial Coherence Models

> 📎 [Zotero](zotero://select/items/0_BD6AVHPW) | [Open Access](https://open.fau.de/handle/openfau/12553)

## 基本信息

| 字段 | 内容 |
|------|------|
| 作者 | Andreas Schwarz |
| 类型 | 博士论文 (Doctoral Dissertation) |
| 大学 | Friedrich-Alexander-Universität Erlangen-Nürnberg (FAU) |
| 年份 | 2019 |
| 语言 | English |

## 摘要

远场语音通信和识别的核心挑战是采集到的语音信号受混响和噪声影响。本文聚焦于利用**空间相干性模型**（spatial coherence models）进行信号增强，其优势在于仅依赖于不同房间间相对相似的声学特性，对声学场景做最少假设。

## 核心贡献

### 1. 空间相干性模型对混响的适用性

研究了不同空间相干性模型对混响的适用性，以及它们对房间声学特性的依赖关系。空间相干函数仅取决于声学特性（如房间尺寸、混响时间），在不同房间间相对相似。

### 2. 谱增强方法框架

- 回顾了利用短时相干性估计来估计相干（期望）与扩散（非期望）声场分量功率比的谱增强方法
- 将已知谱增强方法统一到该框架中
- 提出具有理论和实践优势的新估计器

### 3. 无源位置信息的去混响系统

基于新估计器，提出了一种有效的去混响系统，**无需知道期望源的位置**，仅利用混响的特征空间相干性即可运行。

### 4. 考虑早期反射的去混响

提出了一种更实验性的去混响系统，额外考虑了房间中早期信号反射的影响，为未来研究提供了有前景的方向。

### 5. 空间信息用于鲁棒 ASR

研究了如何在基于深度神经网络声学模型的自动语音识别器中有效利用空间信息。提出了一种新方法：从短时相干性估计中提取空间特征向量，作为神经网络输入。结果表明该方法可以超过应用信号增强方法进行去混响所获得的改进。

## 技术要点

### 空间相干性 (Spatial Coherence)

空间相干函数描述了多通道信号之间的空间相关性。对于扩散声场（混响），相干性具有可预测的模式，这使得仅从相干性估计就能区分直达声和混响。

### 核心信号模型

- **相干分量**：来自目标源的直达声和早期反射
- **扩散分量**：晚期混响和环境噪声
- **功率比估计**：通过短时相干性估计相干/扩散功率比（CDR）

### 与现有方法的关系

| 方法 | 关系 |
|------|------|
| MWF (Multichannel Wiener Filter) | 可用 CDR 估计构建后滤波器 |
| MVDR Beamforming | 空间信息互补——MVDR 做空间滤波，相干性做谱增强 |
| WPE (Weighted Prediction Error) | 不同范式——WPE 做线性预测去混响，相干性做谱掩蔽 |
| DNN-based ASR | 本文将空间特征作为 DNN 附加输入，超越纯信号增强 |

## 与 Wiki 内容的关联

- **去混响**：与 [[sources/dietzen-2020-isclp-kalman|Dietzen 2020: ISCLP Kalman]] 的 MCLP 方法互补——Schwarz 用空间相干性，Dietzen 用线性预测
- **多通道语音增强**：与 [[queries/far-field-multichannel-speech-enhancement-algorithms|远场多麦克风语音增强综述]] 中的谱增强和波束形成章节直接相关
- **空间相干性**：扩散声场相干性模型是 MVDR/MWF 等多通道方法的理论基础
- **鲁棒 ASR**：空间特征向量作为 DNN 输入的思路，与 [[sources/yang-2026-gaze-guided-avse|Yang 2026: Gaze-Guided AVSE]] 的多模态特征融合有方法论上的相似性

## 引用信息

```bibtex
@phdthesis{Schwarz2019,
  author = {Schwarz, Andreas},
  title = {Dereverberation and Robust Speech Recognition Using Spatial Coherence Models},
  year = {2019},
  school = {Friedrich-Alexander-Universit{\"a}t Erlangen-N{\"u}rnberg},
  url = {https://open.fau.de/handle/openfau/12553}
}
```
