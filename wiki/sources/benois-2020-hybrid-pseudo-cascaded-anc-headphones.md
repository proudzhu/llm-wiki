---
type: source
created: 2026-04-13
updated: 2026-04-13
sources:
  to Headphones.md
tags:
- active-noise-control
- feedforward-control
- hybrid-anc
- internal-model-control
- minimum-variance-control
- modified-fxlms
- phd-dissertation
- pseudo-cascaded-control
aliases:
- 'Benois 2020: Hybrid and Pseudo-Cascaded ANC for Headphones'
---

# Hybrid and Pseudo-Cascaded Active Noise Control Applied to Headphones

**Author**: Piero Iared Rivera Benois
**Supervisors**: Prof. Udo Zölzer, Prof. Delf Sachau
**Published**: PhD Dissertation, Helmut-Schmidt-Universität Hamburg, 2020
**Pages**: 204
**DOI**: [10.24405/11644](https://doi.org/10.24405/11644)
**📎 Zotero**: [zotero://select/items/0_CD3T4L4I](zotero://select/items/0_CD3T4L4I)

---

## 一、论文概述

这是目前 wiki 中**最全面的 ANC 耳机控制理论博士论文**。系统性地将三种经典 ANC 控制方案（前馈 FF、最小方差 MVC、内部模型 IMC）两两组合，进而提出三种**同时组合三种方案的新型控制结构**，无需额外麦克风或扬声器。

### 核心贡献

1. **三种新型混合/伪级联控制结构**：同时组合 FF + MVC + IMC
2. **两阶段优化策略**：先 MVC+IMC 联合优化，再 FF 优化
3. **Modified Normalized FxLMS 的集成**：最小内存和计算开销的自适应实现
4. **FPGA 原型验证**：虚拟人头测量，同侧/对侧随机噪声激励

---

## 二、三种经典控制方案回顾

### 2.1 前馈控制（Feedforward, FF）

**系统传递函数**：
$$
H_f(z) = \frac{E(z)}{X(z)} = P(z) - S(z) W_f(z)
$$

**最优 Wiener 控制器**：
$$
W_{f,opt} = -\Phi_{xx}^{-1} \phi_{dx}^+
$$

**关键限制**：
- **因果性**：次级路径延迟 $D_{ps}$ 决定了最大可实现带宽
- **相干性**：参考信号 $x(n)$ 与扰动 $d(n)$ 的幅度平方相干函数 $C_{dx}(z)$ 决定了理论上限
- **控制器长度**：$L_w < L_p$ 时性能显著下降

### 2.2 最小方差控制（MVC）

**控制器**：
$$
W_m(z) = -\frac{G(z)}{F(z) B(z)}
$$

其中 $C = F + z^{-k}G$ 是 Diophantine 方程分解。

**关键限制**：
- **延迟敏感**：延迟从 1→2 样本 → 降噪降低 ~10 dB
- **非最小相位植物**：需要 WMVC（加权最小方差）加入控制努力惩罚

### 2.3 内部模型控制（IMC）

**结构**：控制器由 $W$ 和 $\hat{P}$（植物模型）两部分组成

**IMC 控制器**：
$$
W_i(z) = -\frac{G(z)}{F(z) C(z)}
$$

当模型完美时（$\hat{P} = P$），IMC 等价于 MVC。

---

## 三、两两组合（Chapter 5）

### 3.1 MVC + IMC 组合

**等效 MVC 控制器**：
$$
\tilde{W}_m(z) = \frac{W_m(z) + W_i(z)}{1 - \hat{S}(z) W_i(z)}
$$

**两种结构**：
- **独立最优解**：MVC 和 IMC 各自独立优化
- **依赖最优解**：IMC 最优解依赖于 MVC 参数

### 3.2 MVC + FF 组合

混合系统同时使用前馈参考信号和反馈误差信号。

### 3.3 IMC + FF 组合

IMC 提供反馈鲁棒性，FF 提供前馈预测能力。

---

## 四、三种新型控制结构（Chapter 6）

### 4.1 核心思想

同时组合 FF + MVC + IMC，提供**三种不同的依赖级别**：

| 依赖级别 | 特点 | 适用场景 |
|---------|------|---------|
| **低依赖** | 可复用现有 ANC 知识，各控制器独立设计 | 已有系统升级 |
| **中依赖** | 部分参数耦合，联合优化 MVC+IMC | 平衡设计灵活性 |
| **高依赖** | 全部控制器集体优化 | 最高性能需求 |

### 4.2 等效 MVC 控制器推导

对于 MVC-IMC 组合，等效 MVC 传递函数为：

$$
\tilde{W}_m(z) = \frac{W_m(z) + W_i(z)}{1 - \hat{S}(z) W_i(z)}
$$

**内部稳定性**：分母与 IMC 相同，只需 IMC 内部稳定即可保证。

### 4.3 系统稳定性

闭环特征方程：
$$
C_{mi}(z) = 1 + S(z)W_m(z) + [S(z) - \hat{S}(z)]W_i(z)
$$

**标称稳定性**：与纯 MVC 相同（$\hat{S} = S$ 时）。

**鲁棒稳定性**（乘性不确定性 $S = S_0(1 + G_2 \Delta)$）：
$$
|1 + S_0 W_m| > |G_2 \cdot [S_0 W_m + W_i]|
$$

- 当 $W_m = 0$ → 简化为 IMC 鲁棒条件
- 当 $W_i = 0$ → 简化为 MVC 鲁棒条件
- **需要但不充分**：MVC 和 IMC 各自鲁棒稳定

### 4.4 扰动放大约束（Waterbed 效应控制）

$$
\left|\frac{1 - \hat{S} W_i}{1 + S W_m + (S - \hat{S})W_i}\right| \leq G_3
$$

控制反馈控制器允许的水床效应放大倍数。

### 4.5 前馈控制器优化

**低依赖结构（FIMPDI）**：
- 最优 FF 控制器通过 Wiener 推导
- MVC 和 IMC 参数固定后，FF 独立优化

**中依赖结构（FIMPDO）**：
- FF 优化考虑 MVC+IMC 已优化的等效二次路径
- 当 $L_w = L_p$ 时性能与经典 FF 相当
- 当 $L_w < L_p$ 时，低频显著改善（45 Hz - 1 kHz），但 1.8-3.5 kHz 和 6 kHz 有损失

**高依赖结构**：
- 全部三个控制器集体优化
- 最高设计灵活性

### 4.6 自适应实现：Modified Normalized FxLMS

将 MN-FxLMS 集成到新型结构中：

**更新方程**：
$$
W(n+1) = W(n) + \mu \frac{r(n) e(n)}{r^T(n) r(n)}
$$

其中 $r(n) = \hat{s}^T x(n)$ 是滤波后的参考信号。

**Pseudo-Cascaded 自适应集成**：
- 反馈控制器先做残余误差预估计
- 前馈控制器基于改进的参考信号自适应
- 最小内存和计算开销

---

## 五、实验结果（Chapter 7）

### 5.1 实验设置

- **硬件**：FPGA 平台 ANC 耳机原型
- **被测对象**：虚拟人头（dummy-head）
- **激励**：同侧（ipsilateral）和对侧（contralateral）随机噪声
- **采样率**：48 kHz
- **控制器长度**：$L_{wf} = 512$，$L_{sf} = 2048$，$L_{\tilde{w}m} = 1024$

### 5.2 同侧激励结果

**关键发现**：
- 新型控制结构的仿真结果得到验证
- 当估计的次级路径脉冲响应**不够长**时，性能退化
- 混合结构在低频（<500 Hz）显著优于纯前馈

### 5.3 对侧激励结果

**关键发现**：
- 前馈控制器在低频引入加性噪声，性能退化
- **但 MVC + IMC 组合本身**仍能达到与同侧激励相当的性能
- 如果未来自适应前馈控制器的缺陷得到解决，新型结构在对侧场景下也能改善性能

---

## 六、关键设计洞察

### 6.1 因果性与延迟

- 次级路径延迟 $D_{ps}$ 决定了非因果场景下的带宽限制
- 延迟 > 7 样本时反馈控制无意义
- 主动耳机中约 6 个样本延迟来自模拟抗混叠/重构滤波器

### 6.2 控制器长度 trade-off

| 控制器长度 | 性能 | 计算量 |
|-----------|------|--------|
| $L_w = L_p$ | 最优，~30 dB 峰值衰减 | 高 |
| $L_w = 64$ | 显著下降，方差高 | 低 |
| $L_w = 512$（实验） | 中等，低频改善 | 中 |

### 6.3 混合结构的优势

- **短控制器时最显著**：当 $L_w \ll L_p$ 时，MVC+IMC 在低频提供显著额外衰减
- **水床效应补偿**：反馈控制器的水床效应被前馈控制器补偿
- **无需额外硬件**：仅通过算法组合实现性能提升

### 6.4 自适应 vs 固定

| 维度 | 固定（Wiener） | 自适应（MN-FxLMS） |
|------|---------------|-------------------|
| 设计 | 离线优化 | 在线跟踪 |
| 计算 | 一次矩阵求逆 | 每步更新 |
| 鲁棒性 | 依赖准确模型 | 可跟踪慢变非平稳性 |
| 实现 | FPGA 友好 | 需小心选择 $\mu$ |

---

## 七、与现有工作的关系

| 本文献 | 关系 |
|--------|------|
| [[pawelczyk-1997-anc-feedback-fixed-adaptive|Pawelczyk 1997: ANC Feedback Fixed/Adaptive]] | 同导师（Elliott 学派），MVC/IMC 理论基础 |
| [[kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] | FF/IMC 基础知识，本文扩展为混合结构 |
| [[wills-2008-mpc-constraint-handling-anc-avc|Wills 2008: MPC Constraint Handling in ANC/AVC]] | 不同方向：MPC 约束处理 vs 混合结构组合 |
| [[liang-2026-delayed-mpc-anc-paper-reading-note|Liang 2026: Delayed MPC for ANC Paper Reading Note]] | MPC 用于 ANC 的另一路径 |

---

## 八、Q&A

**Q1: "Pseudo-Cascaded" 与真正的级联有什么区别？**

真正的级联是物理上将两个控制器串联。Pseudo-Cascaded 是通过**反馈控制器预先估计残余误差**，将这个估计用作前馈控制器的改进参考信号——等效于级联效果，但无需物理串联。

**Q2: 三种依赖级别如何选择？**

- **低依赖**：已有 ANC 产品想升级，可复用现有 FF 或反馈控制器设计
- **中依赖**：新设计，希望平衡灵活性和性能
- **高依赖**：追求极致性能，愿意接受更复杂的设计流程

**Q3: 为什么对侧激励下前馈性能退化？**

对侧（contralateral）噪声源从另一侧入射，参考麦克风测量的 $x(n)$ 与耳杯内扰动 $d(n)$ 的**相干性降低**。前馈控制器基于低相干信号计算，在低频产生加性噪声。但 MVC+IMC 反馈部分不依赖外部参考，因此仍能有效工作。

---

## Related Concepts

- [[../concepts/feedforward-anc|Feedforward ANC]]
- [[../concepts/minimum-variance-control|Minimum Variance Control]]
- [[../concepts/internal-model-control|Internal Model Control]]
- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[../concepts/active-noise-control|Active Noise Control]]
- [[../concepts/hybrid-anc|Hybrid ANC]]

## Related Entities

- [[../entities/piero-iared-rivera-benois|Piero Iared Rivera Benois]] — 作者，Helmut-Schmidt-Universität
- [[../entities/udo-zolzer|Udo Zölzer]] — 导师，信号处理与通信
- [[../entities/delf-sachau|Delf Sachau]] — 联合导师，主动噪声控制

## Related Synthesis
