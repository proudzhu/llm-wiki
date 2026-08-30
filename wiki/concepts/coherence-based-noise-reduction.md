---
type: concept
created: 2026-08-30
updated: 2026-08-30
sources:
  - raw/papers/yan-2014-dual-mic-bt-noise-reduction/full-text.md
tags:
  - speech-enhancement
  - multi-channel
  - dual-microphone
  - coherence
---

# Coherence-Based Noise Reduction

**Category**: 双传声器语音增强算法族

## Definition

基于相干函数的降噪算法利用两个通道信号之间的相干函数（coherence function）对含噪信号进行滤波，达到降噪目的。由 Le 等于 1992 年提出。核心假设：两通道噪声不相关而语音相关，因此语音存在时相干函数接近 1，仅噪声存在时接近 0，相干函数可直接（或修正后）作为谱增益滤波器。

$$\Gamma_{Y_1 Y_2}(k, m) = \frac{|P_{Y_1 Y_2}(k, m)|}{\sqrt{P_{Y_1 Y_1}(k, m) P_{Y_2 Y_2}(k, m)}}$$

## CPSD 改进形式

实际环境中两通道噪声相关性增加会导致性能急剧下降，改进方法从互功率谱中减去噪声互功率谱（CPSD 算法，Rahmani 等）：

$$H_{\mathrm{CPSD}}(k, m) = \frac{|P_{Y_1 Y_2}(k, m)| - |P_{N_1 N_2}(k, m)|}{\sqrt{P_{Y_1 Y_1}(k, m) P_{Y_2 Y_2}(k, m)}}$$

性能关键在于噪声互功率谱 $P_{N_1 N_2}$ 的估计——一般在语音间歇段平滑估计，可用先验信噪比（Rahmani）、迭代计算、最小统计模型（Freudenbergberger、Kallel）或相干性强度调节平滑因子提高准确性。Yousefian 等利用输入信号相干函数的幅度响应在扩散声场条件下增强语音，无需估计噪声参数且可用于有竞争话者的场合。

## 相关变体

基于能量差和基于相位差的算法与相干函数法本质思想类似，均用不同参数逼近维纳滤波器。双通道谱减法（Kallel）将单通道谱减法应用到双通道。

## 主要缺陷

**语音音质损伤（speech distortion）严重**是这一族算法的主要缺陷——算法只关注噪声谱的估计，完全没有考虑对目标语音统计的建模。降噪量越大，语音损伤越严重。[[sources/yan-2014-dual-mic-bt-noise-reduction|Yan et al. 2014]] 的实验中，CPSD 算法在 6 dB 人声干扰下 PESQ 仅为 1.30（输入 6 dB）。

与 [[concepts/coherent-to-diffuse-power-ratio|CDR]] 方法的关系：CDR 将扩散场相干性模型（sinc 函数）作为先验引入以获得更稳健的增益，而本族算法直接使用实测相干函数；两者均属于以相干性为中间量的谱增益方法。

## Related Concepts

- [[concepts/spatial-coherence|Spatial Coherence]]
- [[concepts/coherent-to-diffuse-power-ratio|Coherent-to-Diffuse Power Ratio]]
- [[concepts/wiener-filter|Wiener Filter]]
- [[concepts/speech-distortion-constrained-noise-reduction|Speech-Distortion-Constrained Noise Reduction]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Related Sources

- [[sources/yan-2014-dual-mic-bt-noise-reduction|Yan, Qiu & Lu 2014]] — 两类算法分类框架中的第一类，含 CPSD 代表算法实验
- [[sources/lollmann-2020-generalized-coherence-based-signal-enhancement|Löllmann et al. 2020]] — 相干函数法的推广（GMC）与统一分析
- [[sources/jin-2017-multichannel-noise-reduction-mobile|Jin et al. 2017]] — 自适应相干噪声估计用于多通道降噪
