---
type: source
created: 2026-08-30
updated: 2026-08-30
sources:
  - raw/papers/yan-2014-dual-mic-bt-noise-reduction/full-text.md
  - https://doi.org/10.11684/j.issn.1000-310X.2014.04.004
  - zotero://select/items/0_YIANQBJD
tags:
  - speech-enhancement
  - bluetooth-headset
  - dual-microphone
  - multi-channel
  - coherence
  - gsc
  - speech-distortion
---

# Yan, Qiu & Lu 2014: Two-Microphone Noise Suppression for Bluetooth Headsets

**Authors**: [[entities/xinye-yan|Xinye Yan]], [[entities/xiaojun-qiu|Xiaojun Qiu]] (corresponding), [[entities/jing-lu|Jing Lu]]
**Institution**: Key Laboratory of Modern Acoustics, Institute of Acoustics, Nanjing University
**Venue**: 应用声学 (Applied Acoustics, Chinese journal), Vol. 33, No. 4, 2014, pp. 313–323
**Type**: journalArticle (analysis/comparison paper with own experiments)
**DOI**: 10.11684/j.issn.1000-310X.2014.04.004
**Zotero**: [YIANQBJD](zotero://select/items/0_YIANQBJD)

## Summary

针对双传声器蓝牙耳机系统的降噪问题，本文将常用多通道降噪算法归纳为**基于相干函数法**与**基于空间预分离法**两大类进行分析比较，并从约束语音损伤（speech distortion, SD）的角度推导无损降噪的最优滤波器形式。以 CPSD（互功率谱）算法与 ATF-GSC（自适应传递函数广义旁瓣消除器）算法为两类代表进行实验对比，结果表明：CPSD 降噪量大但语音损伤严重，ATF-GSC 通过权衡降噪量与语音损伤获得更优的综合性能，且对佩戴角度失配和不同使用者具有鲁棒性。

## Taxonomy

论文将双传声器降噪算法分为两大类：

| 类别 | 原理 | 代表算法 | 特点 |
|------|------|----------|------|
| **基于相干函数法** (coherence based) | 利用两通道间信号的相干函数对含噪信号滤波 | Le 1992 原始算法、CPSD 算法（Rahmani 2009）、Yousefian 2012 幅度响应法、能量差法、相位差法 | 简单易实现；关键是噪声互功率谱估计；**语音损伤严重** |
| **基于空间预分离法** (spatially preprocess based) | 利用空间特性从含噪信号中分离出噪声参考信号 | GSC（1982）、TF-GSC（Gannot 2004）、MWF / SDW-MWF（Doclo / Spriet）、最优滤波器（Chen / Souden & Benesty） | 无语音泄漏时可无损降噪相干噪声；需传递函数信息；牺牲一定降噪量 |

两类算法本质关联：能量差法与相位差法与相干函数法思想类似，均以不同参数逼近维纳滤波器；GSC、MWF 可归入语音损伤约束最优滤波器的特例。

## Methodology

### 系统模型

人头佩戴蓝牙耳机的典型角度有 0°、45°（正常佩戴）和 90°。两全指向传声器间距 $d$ 为 3~4 cm，时域模型为：

$$y_i(t) = s(t) * g_i + v_i(t) = x_i(t) + v_i(t), \quad i = 1, 2$$

模型特点：(1) 传声器间距小，两通道信号相关性较高；(2) 声源（人嘴）与传声器位置相对固定，声学路径变化较小。近场+人头遮挡使得面向远场设计的传统波束形成方法不能直接用于耳机。

![[raw/papers/yan-2014-dual-mic-bt-noise-reduction/figures/67427ef93d3d7ba761144d19855956c56be47a953f1b561c3e07fbd27125b579.jpg|双传声器蓝牙耳机系统平面图]]

*Figure 1: 双传声器蓝牙耳机系统平面图（45° 正常佩戴）。*

### 基于相干函数算法（CPSD 算法）

STFT 域相干函数定义为：

$$\Gamma_{Y_1 Y_2}(k, m) = \frac{|P_{Y_1 Y_2}(k, m)|}{\sqrt{P_{Y_1 Y_1}(k, m) P_{Y_2 Y_2}(k, m)}}$$

假设两通道噪声不相关、语音相关，则语音存在时相干函数接近 1，仅噪声时接近 0，可直接作为滤波器。为降低实际环境两通道噪声相关性的影响，改进的 CPSD 滤波器为：

$$H_{\mathrm{CPSD}}(k, m) = \frac{|P_{Y_1 Y_2}(k, m)| - |P_{N_1 N_2}(k, m)|}{\sqrt{P_{Y_1 Y_1}(k, m) P_{Y_2 Y_2}(k, m)}}$$

关键在于噪声互功率谱 $P_{N_1 N_2}$ 的估计——一般在语音间歇段平滑估计，用先验信噪比、相干性强度、统计参数（如最小统计）调节平滑因子。**优点是简单易行，缺点是对语音音质损伤严重**。

![[raw/papers/yan-2014-dual-mic-bt-noise-reduction/figures/4a5b6d807388b798e4e0bb369336e3ba65d3903ed4cb95891240e47490574150.jpg|基于相干函数算法的流程图]]

*Figure 2: 基于相干函数算法的流程图。*

### 空间预分离法（GSC / TF-GSC）

GSC 通过波束形成矩阵 $A = [A_1(k), A_2(k)]$ 和阻塞矩阵 $B = [B_1(k), B_2(k)]$ 得到语音参考 $Y_s$ 与噪声参考 $Y_n$，仅在噪声段自适应更新滤波器消除语音参考中的噪声。若能得到**无语音泄漏的噪声参考**，则可无损降噪——TF-GSC（Gannot 2004）通过系统辨识获得相对传递函数（RTF）实现较纯净的噪声参考，但需要收敛时间；结合后处理可进一步消除不相干噪声。

![[raw/papers/yan-2014-dual-mic-bt-noise-reduction/figures/18d77acb7141355564271063e29fc10506b4b029bef73a15e370d49564d271f7.jpg|GSC 的一般结构图]]

*Figure 3: GSC 的一般结构图。*

### 语音损伤约束下的最优滤波器

以第一传声器为参考估计语音，误差分为语音失真部分 $\varepsilon_x = (\boldsymbol{H} - \boldsymbol{u})^{\mathrm{H}}\boldsymbol{X}$ 和残留噪声部分 $\varepsilon_v = \boldsymbol{H}^{\mathrm{H}}\boldsymbol{V}$（$\boldsymbol{u} = [1, 0]^{\mathrm{T}}$）。在语音失真约束下最小化残留噪声：

$$\boldsymbol{h}_{\text{optim}} = \arg\min \mathrm{E}\{|\varepsilon_v(\omega)|^2\}, \quad \text{s.t. } \mathrm{E}\{|\varepsilon_x(\omega)|^2\} \leqslant \sigma^2(\omega)$$

由拉格朗日乘数法得到闭式解：

$$\boldsymbol{h}_{\text{optim}} = \left[\Phi_{xx}(\omega) + \beta \Phi_{vv}(\omega)\right]^{-1} \Phi_{xx}(\omega) \boldsymbol{u}$$

权重因子 $\beta$ 由失真阈值 $\sigma(\omega)$ 决定：$\beta$ 越高降噪量越大，语音失真也越厉害。特例：**TF-GSC** 对应 $\mathrm{E}\{|\varepsilon_x|^2\} = 0$ 的约束（失配时相当于 $\beta = 1$）；**SDW-MWF** 最小化加权误差能量 $\mathrm{E}\{|\varepsilon_v|^2\} + \mu \mathrm{E}\{|\varepsilon_x|^2\}$。实际难点：$\Phi_{xx} = \Phi_{yy} - \Phi_{vv}$ 只能在不同时段估计，噪声非平稳性越高越难估计准确。

### ATF-GSC 蓝牙耳机实现

论文实现的自适应传递函数 GSC（ATF-GSC）算法：$A_{\mathrm{ATF-GSC}} = [1, W_s]$，阻塞矩阵 $B_{\mathrm{ATF-GSC}} = [1, -W_s]$。阻塞矩阵可预先在**安静环境**下建模——佩戴位置变化对它影响不大；也可在噪声环境下通过系统辨识自适应更新，但此时语音功率谱难以准确估计，建模误差较大（实验中建模时间 25 s，步长 0.0003）。

![[raw/papers/yan-2014-dual-mic-bt-noise-reduction/figures/1744652447894e4a69ba77e27ad43a0bbbd5b0929d7fee71542358f532a27058.jpg|ATF-GSC 的结构图]]

*Figure 4: ATF-GSC 算法结构图。*

## Experimental Comparison

### 实验设置

| 项目 | 设置 |
|------|------|
| 干扰噪声 | 粉红噪声、人声干扰 |
| 输入信噪比 | 0 / 6 / 12 dB |
| 佩戴条件 | 45° 无失配；0°、90° 失配（45° 建模的传递函数直接使用）；噪声环境自适应建模（6 dB SNR 下 45° 建模，25 s，步长 0.0003） |
| 多使用者实验 | 5 位实验者（4 男 1 女）共用同一预建模阻塞矩阵；视听室中 4 个扬声器正方形排列发声，实验者位于对角线交点，距扬声器 2 m；额外 1 个传声器置于嘴旁采集干净参考 |
| 评价指标 | SegSNR（整体性能，越大越好）、NR（降噪量，越大越好）、LSD（语音失真，越小越好）、PESQ（-0.5~4.5） |

### 结果

语谱图对比：CPSD 算法能在一定程度上消除噪声但对语音损伤非常严重；ATF-GSC 算法仍有一部分残留噪声但语音损伤较小。不同佩戴角度对性能无显著影响；自适应更新建模的降噪效果变差（噪声环境下语音功率谱难估计，建模误差不可避免）。

![[raw/papers/yan-2014-dual-mic-bt-noise-reduction/figures/3f97fe6c9514cd7ccff009c9069dce709b064f2fc65a0d2524f417cddd56aa31.jpg|CPSD 算法增强信号语谱图（粉红噪声干扰）]]

![[raw/papers/yan-2014-dual-mic-bt-noise-reduction/figures/714a6b780312357e0bc45c89672e7fc5f8733e8b5e449c90c755f85ddbc8b43d.jpg|CPSD 算法增强信号语谱图（人声干扰）]]

*Figure 5: CPSD 算法增强信号语谱图——(a) 粉红噪声干扰；(b) 人声干扰。*

![[raw/papers/yan-2014-dual-mic-bt-noise-reduction/figures/29a2a82c9754f293c97797f81a23f2a37e5dde2f3b74a135f01735dfa12ec3be.jpg|ATF-GSC 算法增强信号语谱图（粉红噪声干扰，无失配）]]

![[raw/papers/yan-2014-dual-mic-bt-noise-reduction/figures/760866b33c946239acb766f2ce73041f6d5236c79f6ad2800cecfc867dbefae5.jpg|ATF-GSC 算法增强信号语谱图（人声干扰，无失配）]]

*Figure 6: ATF-GSC 算法增强信号语谱图——(a) 粉红噪声干扰（无失配）；(b) 人声干扰（无失配）。*

PESQ 评分（表 1）与 SegSNR / NR / LSD 曲线（图 7~12）的趋势一致：

- **音质**：ATF-GSC 在所有情况下（含失配、自适应建模、不同使用者）的 PESQ 均优于 CPSD；如 6 dB 粉红噪声下，ATF-GSC 无失配 2.94 vs CPSD 2.10，人声干扰下 2.90 vs 1.30。
- **鲁棒性**：0°/90° 佩戴失配与不同使用者（平均性能与无失配接近）对 ATF-GSC 影响小；自适应建模性能明显变差且 SNR 越低越差，但仍优于 CPSD。
- **综合性能**：ATF-GSC 优于 CPSD，验证了权衡语音损伤对综合性能的重要性。

| 输入 SNR (dB) | ATF-GSC 45°无失配（粉红/人声） | ATF-GSC 0°失配 | ATF-GSC 90°失配 | ATF-GSC 使用者均值 | ATF-GSC 自适应 | CPSD |
|---|---|---|---|---|---|---|
| 0 | 2.60 / 2.99 | 2.66 / 2.96 | 2.55 / 2.64 | 2.53 / 2.83 | 2.17 / 2.47 | 1.77 / 1.37 |
| 6 | 2.94 / 2.90 | 2.87 / 2.88 | 2.80 / 2.61 | 2.55 / 2.92 | 2.44 / 2.46 | 2.10 / 1.30 |
| 12 | 3.55 / 3.17 | 3.44 / 3.13 | 3.12 / 2.90 | 2.64 / 2.98 | 2.61 / 2.58 | 2.32 / 1.91 |

*Table 1: 不同噪声干扰、不同信噪比条件下各算法的 PESQ 评分。*

## Key Contributions

1. **两类算法分类框架**：将适用于双传声器蓝牙耳机的多通道降噪算法归纳为基于相干函数法与基于空间预分离法两大类，并阐明其本质联系（均为逼近维纳滤波器/最优滤波器的特例）。
2. **语音损伤约束最优解分析**：从约束语音损伤的角度推导最优滤波器闭式形式 $\boldsymbol{h} = [\Phi_{xx} + \beta\Phi_{vv}]^{-1}\Phi_{xx}\boldsymbol{u}$，将 TF-GSC（零失真约束）与 SDW-MWF（加权目标）统一为 $\beta$ 权衡的特例，指出实际实现中逼近该最优解的关键在于 $\Phi_{xx}$ 的估计。
3. **面向蓝牙耳机的 ATF-GSC 实现与系统评估**：安静环境预建模阻塞矩阵对佩戴角度失配和不同使用者鲁棒；在降噪量-语音损伤权衡上，ATF-GSC 的综合性能（SegSNR/PESQ）显著优于 CPSD，验证了语音损伤约束对可穿戴双传声器系统的重要性。

## Limitations and Caveats

- 仅为双传声器、全指向传声器的蓝牙耳机系统；骨传导传感器、三传声器结构（Jawbone ERA、Plantronics Voyager Legend 类产品）只在引言中提及而未评估。
- 自适应建模在噪声环境下（尤其低 SNR）误差较大，论文未提出根本解决方案，仅指出更准确的建模是提升方向。
- 实验规模有限（5 位实验者、2 种噪声类型），PESQ 与客观指标为主，未报告正式的主观听测（MOS）。
- 未涉及深度学习方法；VAD 准确性、自适应算法优化、后处理消除不相干噪声均作为展望提出。

## Related Concepts

- [[concepts/coherence-based-noise-reduction|Coherence-Based Noise Reduction]]
- [[concepts/atf-gsc|ATF-GSC]]
- [[concepts/speech-distortion-constrained-noise-reduction|Speech-Distortion-Constrained Noise Reduction]]
- [[concepts/gsc-beamformer|GSC]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/spatial-coherence|Spatial Coherence]]
- [[concepts/relative-transfer-function|Relative Transfer Function]]
- [[concepts/minimum-statistics|Minimum Statistics]]
- [[concepts/voice-activity-detection|Voice Activity Detection]]
- [[concepts/pesq|PESQ]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Related Sources

- [[sources/lollmann-2020-generalized-coherence-based-signal-enhancement|Lollmann et al. 2020]] — 相干函数法的推广与统一分析
- [[sources/taseska-2018-informed-spatial-filters|Taseska et al. 2018]] — informed GSC，同样以 RTF 阻塞矩阵与信号检测控制更新
- [[sources/jin-2017-multichannel-noise-reduction-mobile|Jin et al. 2017]] — 移动设备多通道降噪，MVDR+维纳后滤波分解与自适应相干噪声估计
- [[sources/schwarz-2015-coherent-to-diffuse-power-ratio|Schwarz & Kellermann 2015]] — 扩散场相干性模型与 CDR 估计
- [[sources/lu-2024-headphone-speech-listening-ambient-noise|Lu 2024]] — 耳机语音聆听与环境噪声，同一团队相关综述
