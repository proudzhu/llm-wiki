---
type: concept
created: 2026-04-25
updated: 2026-04-30
sources:
tags:
  - signal-processing
  - multichannel
  - dereverberation
  - spatial-processing
---

# Spatial Coherence

**Spatial Coherence** (空间相干性) 描述了多通道信号之间的空间相关性程度，是区分相干声源（直达声）和扩散声场（混响、噪声）的关键工具。

## 定义

两个传感器信号之间的空间相干性定义为互功率谱密度的归一化形式：

$$\Gamma_{x_1 x_2}(\omega) = \frac{S_{x_1 x_2}(\omega)}{\sqrt{S_{x_1 x_1}(\omega) \cdot S_{x_2 x_2}(\omega)}}$$

其中 $S_{x_1 x_2}$ 是互功率谱密度，$S_{x_1 x_1}$ 和 $S_{x_2 x_2}$ 是自功率谱密度。

## 扩散声场的相干性模型

对于各向同性扩散声场（晚期混响），两个全向麦克风之间的理论相干性为：

$$\Gamma_{\text{diff}}(\omega) = \frac{\sin(kd)}{kd}$$

其中 $k = \omega/c$ 是波数，$d$ 是麦克风间距。这一可预测的模式使得仅从相干性测量就能区分直达声和混响。

## 相干-扩散比 (CDR)

Coherence-to-Diffuse Ratio (CDR) 是从空间相干性估计中推导的功率比：

$$\text{CDR} = \frac{|\Gamma_{x_1 x_2}|^2 - |\Gamma_{\text{diff}}|^2}{1 - |\Gamma_{x_1 x_2}|^2}$$

CDR > 0 表示相干分量（直达声）占主导，CDR < 0 表示扩散分量（混响）占主导。

## 应用

| 应用 | 原理 |
|------|------|
| **去混响** | 利用扩散声场相干性模型估计晚期混响功率，构建谱增益 |
| **噪声 reduction** | 区分相干目标源和扩散噪声 |
| **鲁棒 ASR** | 从短时相干性提取空间特征向量作为 DNN 输入 |
| **波束形成辅助** | CDR 估计可作为 MVDR/MWF 的后滤波器 |

## 与其他概念的关系

- [[beamforming|Beamforming]]：空间滤波，与相干性估计互补
- [[wiener-filter|Wiener Filter]]：CDR 可构建多通道维纳滤波器的后滤波增益
- [[mclp|MCLP]]：不同的去混响范式——MCLP 做线性预测，相干性做谱掩蔽
- [[deep-learning-for-signal-processing|Deep Learning for Signal Processing]]：空间特征作为 DNN 输入

## 关键文献

- [[sources/schwarz-2019-dereverberation-spatial-coherence|Schwarz 2019]] — 博士论文，系统研究空间相干性模型在去混响和 ASR 中的应用
- [[sources/liu-2026-scm-reconstruction-speech-enhancement|Liu 2026]] — 利用扩散声场相干矩阵 $\Gamma_d$ 作为预定义基，通过方差比估计重建 SCM
