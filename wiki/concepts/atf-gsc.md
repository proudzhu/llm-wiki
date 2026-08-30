---
type: concept
created: 2026-08-30
updated: 2026-08-30
sources:
  - raw/papers/yan-2014-dual-mic-bt-noise-reduction/full-text.md
tags:
  - gsc
  - beamforming
  - speech-enhancement
  - bluetooth-headset
  - dual-microphone
---

# ATF-GSC (Adaptive Transfer Function GSC)

**Category**: 面向蓝牙耳机的空间预分离降噪算法

## Definition

ATF-GSC（自适应传递函数广义旁瓣消除器）是 [[sources/yan-2014-dual-mic-bt-noise-reduction|Yan et al. 2014]] 针对双传声器蓝牙耳机实现的 [[concepts/gsc-beamformer|GSC]] 类算法，采用 RTF（相对传递函数）形式的波束形成矩阵与阻塞矩阵：

$$A_{\mathrm{ATF-GSC}} = [1, W_s], \qquad B_{\mathrm{ATF-GSC}} = [1, -W_s]$$

语音参考为两通道直接求和，噪声参考由阻塞矩阵 $[1, -W_s]$ 消除语音分量得到；自适应算法仅在噪声段更新滤波器，从语音参考中消除噪声。$W_s$ 即声源到第二传声器相对于第一传声器的 [[concepts/relative-transfer-function|RTF]]。

## 阻塞矩阵的两种获取方式

1. **安静环境预建模**：出厂前在安静环境下辨识得到。由于声源（人嘴）与传声器位置相对固定、且近场路径主要由几何决定，佩戴位置变化（0°/45°/90°）和不同使用者对它影响不大。
2. **噪声环境自适应更新**：通过系统辨识方法（Cohen 2004）在噪声环境下在线估计，但需要语音信号的功率谱，在噪声环境下难以准确估计，低信噪比时建模误差大（论文实验：25 s 建模时间、步长 0.0003 仍有明显误差）。

## 性能特征

- 相对于 [[concepts/coherence-based-noise-reduction|CPSD 算法]]：降噪量略小但语音损伤显著更小，综合性能（SegSNR、PESQ）更优。
- 鲁棒性：佩戴角度失配与不同使用者（共用同一预建模阻塞矩阵）影响有限，平均性能与无失配接近。
- 失配情况下存在语音泄漏，相当于语音损伤约束最优滤波器中 $\beta = 1$ 的情形。
- 对自适应算法不能消除的不相干噪声，需后处理算法进一步消除。

## Related Concepts

- [[concepts/gsc-beamformer|GSC]]
- [[concepts/relative-transfer-function|Relative Transfer Function]]
- [[concepts/speech-distortion-constrained-noise-reduction|Speech-Distortion-Constrained Noise Reduction]]
- [[concepts/informed-gsc|Informed GSC]] — 同样以 RTF 阻塞矩阵 + 信号检测控制更新的现代变体
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Related Sources

- [[sources/yan-2014-dual-mic-bt-noise-reduction|Yan, Qiu & Lu 2014]] — 提出 ATF-GSC 蓝牙耳机实现并与 CPSD 算法对比
- [[sources/taseska-2018-informed-spatial-filters|Taseska et al. 2018]] — informed GSC，RTF 阻塞矩阵 + 检测器控制的逐 bin 更新
