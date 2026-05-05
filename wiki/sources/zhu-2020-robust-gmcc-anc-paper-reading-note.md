---
type: source
created: 2026-04-12
updated: 2026-04-12
sources:
  for active noise control.md
tags:
- active-noise-control
- continuous-mixed-norm
- convex-combination
- generalized-correntropy
- generalized-maximum-correntropy-criterion
- impulsive-noise
aliases:
- 'Zhu 2020: Robust GMCC for ANC Paper Reading Note'
---

# 论文精读 | Robust Generalized Maximum Correntropy Criterion Algorithms for Active Noise Control

**作者**: Yingying Zhu, Haiquan Zhao, Xiangping Zeng, Badong Chen
**机构**: Southwest Jiaotong University, Xi'an Jiaotong University
**发表**: IEEE/ACM TASLP, Vol. 28, pp. 1282-1292, 2020
**DOI**: [10.1109/TASLP.2020.2982030](https://doi.org/10.1109/TASLP.2020.2982030)
**📎 Zotero**: [zotero://select/items/0_E297XA9L](zotero://select/items/0_E297XA9L)

---

## 一、问题定义：FxMCC 的局限性

[[../concepts/maximum-correntropy-criterion|Maximum Correntropy Criterion]] (MCC) 已成功应用于脉冲噪声环境下的 ANC。但默认的**高斯核**并非总是最优选择。

**FxMCC 算法**（使用高斯核）的更新规则：

$$
{\bf w}(n+1) = {\bf w}(n) + \mu \exp\left(-\frac{e(n)^2}{2\sigma^2}\right) e(n) {\bf x}'(n)
$$

高斯核的问题：
1. 对"最不承诺异常值"的同时，也**对所有其他事项表达了最大不确定性** [32-34]
2. 单一误差范数（$L_2$），在强脉冲噪声下**收敛速度慢、降噪性能差**
3. 核带宽 $\sigma$ 的选择依赖先验误差知识

本文的贡献链：

```
FxMCC（高斯核）
  ↓  引入 GGD 核
FxGMCC（广义最大 correntropy）
  ↓  引入连续混合 Lp 范数
IFxGMCC（改进版）
  ↓  凸组合方案
C-IFxGMCC（凸组合改进版）
```

---

## 二、广义 Correntropy 回顾

广义核函数使用广义高斯密度（GGD）：

$$
\kappa_{\text{GMCC}}(X-Y) = \lambda_p \exp\left(-\eta |X-Y|^p\right)
$$

其中：
- $p > 0$：分散参数（控制尾行为）
- $\eta = 1/\vartheta^p$：核带宽参数
- $\lambda_p = p / (2\vartheta\Gamma(1/p))$：归一化常数
- $\vartheta = [\sigma^2 \Gamma(1/p)/\Gamma(3/p)]^{1/2}$

**关键关系**：当 $p = 2$ 时，退化为标准高斯核 correntropy。

广义 correntropy 的样本估计：

$$
\hat{V}_{\text{GMCC}}(X,Y) \approx \frac{1}{M} \sum_{i=1}^M \lambda_{p,\vartheta} \exp\left(-\eta |x(i)-y(i)|^p\right)
$$

---

## 三、FxGMCC 算法

### 3.1 代价函数

取当前样本（$M=1$）：

$$
J_{\text{FxGMCC}} = \lambda_{p,\vartheta} \exp\left(-\eta |e(n)|^p\right)
$$

其中 $e(n) = d(n) - y'(n)$，$y'(n) = {\bf w}^T(n) {\bf x}'(n)$。

### 3.2 梯度下降更新

$$
{\bf w}(n+1) = {\bf w}(n) + \mu_g \exp\left(-\eta |e(n)|^p\right) |e(n)|^{p-1} \text{sign}(e(n)) {\bf x}'(n)
$$

其中 $\mu_g = \mu \lambda_{p,\vartheta} p \eta$，${\bf x}'(n) = {\bf x}(n) * \hat{s}(n)$。

### 3.3 特殊形式

令 $\mu_e(n) = \mu_g \exp(-\eta |e(n)|^p)$ 为可变步长：

$$
{\bf w}(n+1) = {\bf w}(n) + \mu_e(n) |e(n)|^{p-1} \text{sign}(e(n)) {\bf x}'(n)
$$

这等价于一个**可变步长 FxLMP（VSS-FxLMP）**算法。

**当 $p=2$**：退化为原始 FxMCC 算法。

---

## 四、IFxGMCC：连续混合 Lp 范数

### 4.1 动机

FxGMCC 仍采用单一误差范数 $|e(n)|^p$，在非高斯环境下**收敛慢、降噪差**。此外，参数 $p$ 的选择依赖先验误差知识。

### 4.2 连续混合范数代价函数

受连续混合范数（CMN）[40] 启发：

$$
J_{\text{IFxGMCC}}(n) = \int_1^2 \tau(p) E\left[|e(n)|^p\right] dp
$$

其中 $\tau(p)$ 是概率密度函数（假设均匀分布 $\tau(p)=1$）。

### 4.3 积分项解析解

将 CMN 引入 GMCC 代价函数：

$$
J_{\text{IFxGMCC}} = \int_1^2 \lambda_{p,\vartheta} \exp\left(-\eta |e(n)|^p\right) dp
$$

梯度下降后得到更新规则：

$$
{\bf w}(n+1) = {\bf w}(n) + \mu_g \exp\left\{-\eta C_p(n)\right\} I_p(n) \text{sign}(e(n)) {\bf x}'(n)
$$

其中两个关键积分项（MATLAB 解析求解）：

$$
I_p(n) = \frac{1 - |e(n)| + [(2|e(n)|-1)\log|e(n)|]}{\log^2|e(n)|}
$$

$$
C_p(n) = \frac{|e(n)|(|e(n)|-1)}{\log|e(n)|}
$$

**关键优势**：
1. 消除了手动选择 $p$ 值的问题——积分覆盖了 $[1, 2]$ 整个范围
2. 继承了 FxGMCC 对脉冲噪声的鲁棒性
3. 比单一范数具有更好的收敛速度和降噪性能

### 4.4 IFxGMCC 伪代码

```
初始化: w(0) = 0
参数: μ_g > 0, η
For n = 0, 1, 2, ...
  1. 计算输出: y(n) = w^T(n)x(n), y'(n) = y(n)*s(n)
  2. 计算误差: e(n) = d(n) - y'(n)
  3. 更新权重:
     w(n+1) = w(n) + μ_g exp{-η·C_p(n)} · I_p(n) · sign(e(n)) · x'(n)
End
```

---

## 五、C-IFxGMCC：凸组合方案

### 5.1 动机

固定步长的 IFxGMCC 存在经典权衡：**快速收敛 vs 低稳态失配**。

### 5.2 凸组合架构

两个 IFxGMCC 滤波器并行运行，不同步长：

| 滤波器 | 步长 | 作用 |
|--------|------|------|
| 滤波器 1 | $\mu_1$（大） | 快速收敛 |
| 滤波器 2 | $\mu_2$（小） | 低稳态误差 |

整体输出：

$$
y(n) = \beta(n) y_1'(n) + (1-\beta(n)) y_2'(n)
$$

其中混合参数 $\beta(n)$ 通过 sigmoid 函数调节：

$$
\beta(n) = \frac{1}{1 + \exp(-\zeta(n))}
$$

### 5.3 混合参数更新

$\zeta(n)$ 通过最小化整体误差更新：

$$
\zeta(n+1) = \zeta(n) + \mu_\zeta \exp\{-\eta_\zeta C_{p_\zeta}(n)\} I_{p_\zeta}(n) \text{sign}(e(n)) (y_1'(n) - y_2'(n)) \beta(n)(1-\beta(n))
$$

### 5.4 滤波器更新

$$
{\bf w}_1(n+1) = {\bf w}_1(n) + \mu_1 I_{p_1}(n) \exp\{-\eta_1 C_{p_1}(n)\} \text{sign}(e_1(n)) {\bf x}'(n)
$$

$$
{\bf w}_2(n+1) = {\bf w}_2(n) + \mu_2 I_{p_2}(n) \exp\{-\eta_2 C_{p_2}(n)\} \text{sign}(e_2(n)) {\bf x}'(n)
$$

整体权重：${\bf w}(n) = \beta(n){\bf w}_1(n) + (1-\beta(n)){\bf w}_2(n)$

当 $\zeta(n) \geq \sigma$（$\sigma=4$）时，将小步长滤波器复制为整体滤波器：${\bf w}_2(n+1) = {\bf w}(n)$，避免退化。

### 5.5 组合动态

- **迭代初期**：$\beta(n) \approx 1$，大步长滤波器主导 → 快速收敛
- **稳态阶段**：$\beta(n) \approx 0$，小步长滤波器主导 → 低稳态误差

---

## 六、得分函数（Score Function）分析

自适应算法的统一形式：

$$
{\bf w}(n+1) = {\bf w}(n) + \mu f(e(n)) {\bf x}'(n)
$$

其中 $f(e(n))$ 是**得分函数**。不同算法的得分函数对比：

| 算法 | 得分函数 $f(e(n))$ | 大误差行为 |
|------|-------------------|-----------|
| FxLMS | $e(n)$ | 线性增长 → 脉冲下不稳定 |
| FxLMP | $|e(n)|^{p-1}\text{sign}(e(n))$ | 幂律增长 → 仍可能发散 |
| FxlogLMS | $\log(|e(n)|)e(n)$ | 对数增长，但 $|e|<1$ 时有死区 |
| RFsLMS | $e(n)/(e(n)^2 + 2\sigma^2)$ | 有界，但仍有改进空间 |
| FxMCC | $\exp(-e(n)^2/2\sigma^2) e(n)$ | **指数衰减 → 零** |
| FxGMCC | $\exp(-\eta|e(n)|^p)|e(n)|^{p-1}\text{sign}(e(n))$ | **指数衰减 → 零** |
| **IFxGMCC** | $\exp\{-\eta C_p(n)\} I_p(n)\text{sign}(e(n))$ | **更窄的调节范围** |
| **C-IFxGMCC** | 同上（凸组合） | 同上 |

**关键洞察**：correntropy 家族的得分函数在大误差时趋于零——脉冲被**自动抑制**而非放大。IFxGMCC 进一步将 $|e(n)|$ 调节在更窄范围内，增强了对强脉冲噪声的鲁棒性。

---

## 七、计算复杂度

| 算法 | 乘法 | 加法 | $L_p$ 范数 | 指数 | 对数 |
|------|------|------|-----------|------|------|
| FxLMS | $2N+2K+1$ | $2N+2K-3$ | — | — | — |
| RFxLMS | $2N+2K+7$ | $2N+2K+5$ | — | — | — |
| FxLMP | $2N+2K+2$ | $2N+2K-3$ | 1 | — | — |
| FxMCC | $2N+2K+6$ | $2N+2K-3$ | — | 1 | — |
| FxGMCC | $2N+2K+4$ | $2N+2K-3$ | — | 1 | — |
| **IFxGMCC** | $2N+2K+6$ | $2N+2K-1$ | — | 1 | 3 |
| **C-IFxGMCC** | $4N+3K+16$ | $4N+3K+2$ | — | 2 | 6 |

其中 $N$ = 自适应滤波器长度，$K$ = 次级路径模型长度。

**IFxGMCC** 的计算量与 FxMCC 相当（仅多了 3 次对数运算）。**C-IFxGMCC** 的计算量约是 FxLMS 的两倍多，但以计算成本换取了收敛速度和稳态性能的提升。

---

## 八、实验结果

### 8.1 α-稳定分布脉冲噪声

| 噪声条件 | FxLMP | RFxLMS | FxMCC | FxGMCC | IFxGMCC | **C-IFxGMCC** |
|---------|-------|--------|-------|--------|---------|--------------|
| α = 1.9（强脉冲） | 差 | 中 | 好 | 较好 | 好 | **最优** |
| α = 1.7（中脉冲） | 差 | 中 | 好 | 较好 | 好 | **最优** |
| α = 1.5（近高斯） | 中 | 好 | 好 | 较好 | 好 | **最优** |

**GMCC 家族全面优于 FxMCC**。C-IFxGMCC 在收敛速度和稳态误差上均有显著提升。

### 8.2 正弦 + 脉冲混合噪声

$$
x(n) = 2\sin\left(\frac{2\pi \cdot 500 \cdot n}{8000}\right) + v(n), \quad v(n) \sim S\alpha S, \alpha=1.5
$$

GMCC 家族对含离群点的纯音噪声仍然鲁棒。RFxLMS 也表现良好。

### 8.3 真实噪声：牵引变电站噪声

三个实验条件：

| 实验 | 次级路径 | 噪声突变时表现 |
|------|---------|---------------|
| 实验 1 | 最小相位 $S(z) = z^{-2} + 0.5z^{-3}$ | 所有算法收敛，GMCC 家族在突变后收敛更快 |
| 实验 2 | **非最小相位** $S(z) = z^{-2} + 1.5z^{-3} - z^{-4}$ | FxLMP 和 FxMCC 性能下降，**GMCC 家族不受影响** |
| 实验 3 | 真实传递函数（FIR 建模） | FxMCC 在噪声突变时失效，**C-IFxGMCC 几乎无波动** |

**62Hz 处降噪水平对比**（实验 1，最小相位）：

| 算法 | 降噪量 |
|------|--------|
| FxGMCC | 41.44 dB |
| IFxGMCC | 43.10 dB |
| **C-IFxGMCC** | **47.96 dB** |

**实验 2（非最小相位）** 的关键发现：
- FxMCC 在非最小相位系统下无法达到理想效果
- FxGMCC 和 IFxGMCC **不受系统相位特性影响**
- C-IFxGMCC 的凸组合方案**增强了算法对系统结构的鲁棒性**

---

## 九、与已有算法的系统对比

| 维度 | FxLMS | FxMCC | FxGMCC | IFxGMCC | C-IFxGMCC |
|------|-------|-------|--------|---------|-----------|
| **脉冲噪声鲁棒性** | 差 | 好 | 更好 | 更好 | 最好 |
| **收敛速度** | 中 | 慢 | 慢 | 中 | **快** |
| **稳态误差** | 中 | 中 | 中 | 中 | **低** |
| **参数选择难度** | 低（仅 $\mu$） | 中（$\mu, \sigma$） | 高（$\mu, \eta, p$） | 中（$\mu, \eta$） | 高（双滤波器） |
| **计算复杂度** | 最低 | 中 | 中 | 中 | 高（~2×FxLMS） |
| **非最小相位鲁棒性** | 差 | 差 | **好** | **好** | **好** |
| **噪声突变跟踪** | 差 | 差 | 中 | 中 | **好** |

---

## 十、Q&A

**Q1: IFxGMCC 为什么比 FxGMCC 好？**

FxGMCC 使用单一 $p$ 范数，需要手动选择 $p$ 值（依赖先验知识）。IFxGMCC 通过对 $p \in [1,2]$ 积分，自动覆盖从轻尾（$p \approx 2$）到重尾（$p \approx 1$）的整个范围。积分项 $I_p(n)$ 和 $C_p(n)$ 有解析解，无需数值积分。

**Q2: 凸组合方案为什么有效？**

经典自适应滤波器的困境：大步长 → 快收敛但大稳态误差；小步长 → 慢收敛但小稳态误差。凸组合让两个滤波器**各自独立更新**，混合参数 $\beta(n)$ 根据当前误差自动调节——初期 $\beta \approx 1$（大步长主导），稳态 $\beta \approx 0$（小步长主导）。这相当于一个**自适应的时变步长策略**。

**Q3: 为什么 correntropy 家族对脉冲噪声鲁棒？**

核心在得分函数 $f(e(n))$。FxLMS 的得分函数是 $f(e) = e$——大误差产生大更新，脉冲被放大。Correntropy 家族的得分函数包含指数项 $\exp(-\eta|e|^p)$——当 $|e|$ 大时，指数项趋于零，得分函数趋于零，脉冲被**自动抑制**。

**Q4: 本文与 [[chen-2016-generalized-correntropy-robust-adaptive-filtering|Chen 2016: Generalized Correntropy for Robust Adaptive Filtering]] 的关系？**

Chen 2016 提出了广义 correntropy 和 GMCC 算法的**一般理论**（不限应用领域）。本文将其**专门应用于 ANC**，并做了两个关键改进：(1) 连续混合 Lp 范数消除 $p$ 值选择问题；(2) 凸组合方案解决收敛速度-稳态误差权衡。可以看作是 Chen 2016 的 ANC 领域扩展和改进版本。

---

## Related Concepts

- [[../concepts/correntropy|Correntropy]] — 非线性相似度度量
- [[../concepts/generalized-correntropy|Generalized Correntropy]] — GGD 核 correntropy，$p$ 参数控制尾行为
- [[../concepts/maximum-correntropy-criterion|Maximum Correntropy Criterion]] — 基于 correntropy 的优化准则
- [[../concepts/active-noise-control|Active Noise Control]] — 应用场景
- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — 对比基线
- [[../concepts/robust-adaptive-filtering|Robust Adaptive Filtering]] — 脉冲噪声下的鲁棒自适应滤波

## Related Sources

- [[chen-2016-generalized-correntropy-robust-adaptive-filtering|Chen 2016: Generalized Correntropy for Robust Adaptive Filtering]] — 广义 correntropy 和 GMCC 的一般理论（不限领域）

## Related Entities

- [[../entities/haiquan-zhao|Haiquan Zhao]] — 通讯作者，Southwest Jiaotong University
- [[../entities/badong-chen|Badong Chen]] — 共同作者，Xi'an Jiaotong University，广义 correntropy 的提出者

## Related Synthesis
