---
type: query
created: 2026-04-12
updated: 2026-04-12
sources:
  - zotero://select/items/0_IZATI7ZF
  - zotero://select/items/0_BZNLP2NQ
  - zotero://select/items/0_9KNF4YUC
  - zotero://select/items/0_9XV54S6J
  - zotero://select/items/0_NCKN38JM
  - zotero://select/items/0_FERIFUEJ
  - zotero://select/items/0_NEWLEZ9B
  - zotero://select/items/0_W67EQD8F
  - zotero://select/items/0_ZXUHQ2ET
tags:
  - adaptive-filtering
  - variable-step-size
  - NLMS
  - VSS
  - versiera
  - versoria
  - convex-combination
---

# 自适应滤波变步长算法综述

> 基于 Zotero 文献库整理，覆盖 9 篇核心论文，涵盖 Versiera/Versoria 函数法、噪声功率估计法、误差自相关法、动量扰动法、凸组合等主流方向。

---

## 1. 问题背景

### 1.1 固定步长 LMS/NLMS 的矛盾

标准 LMS 更新：
$$\mathbf{w}[n+1] = \mathbf{w}[n] + \mu \cdot e[n] \cdot \mathbf{x}[n]$$

NLMS 更新（归一化）：
$$\mathbf{w}[n+1] = \mathbf{w}[n] + \frac{\mu}{\|\mathbf{x}[n]\|^2 + \delta} \cdot e[n] \cdot \mathbf{x}[n]$$

**固定步长的根本矛盾**：
- **大步长** → 收敛快，但稳态误差大（misadjustment $M \propto \mu$）
- **小步长** → 稳态误差小，但收敛慢

**变步长（VSS）的目标**：
$$\mu[n] = \begin{cases} \text{大} & \text{收敛初期/环境突变} \\ \text{小} & \text{接近稳态} \end{cases}$$

### 1.2 经典 VSS 方法回顾

**Kwong & Johnston (1992) 符号误差法**：
$$\mu[n] = \alpha \mu[n-1] + \gamma |e[n] \cdot e[n-1]|$$

基于连续误差乘积的绝对值——收敛时 $e[n]$ 和 $e[n-1]$ 不相关，$\mu$ 自动减小。

**Aboulnasr & May (1995) 梯度估计法**：
$$\mu[n] = \alpha \mu[n-1] + \beta \cdot e^2[n-1]$$

---

## 2. Zotero 库中的 VSS 算法分类

| # | 论文 | Zotero 链接 | 年份 | 核心方法 |
|---|------|------------|------|---------|
| 1 | Yu & Zhao, *Improved VSS-NLMS based on versiera function* | [↗](zotero://select/items/0_IZATI7ZF) | 2013 | Versiera 函数 |
| 2 | Zhao & Yu, *Novel adaptive VSS-NLMS for system identification* | [↗](zotero://select/items/0_BZNLP2NQ) | 2013 | 噪声功率估计 |
| 3 | Yu & Zhao, *VSS-NLMS based on power estimate of system noise* | [↗](zotero://select/items/0_9KNF4YUC) | 2015 | 噪声功率估计（arXiv） |
| 4 | Zipf, *Robust non-parametric VSS-NLMS based on error autocorrelation* | [↗](zotero://select/items/0_9XV54S6J) | 2025 | 误差自相关 |
| 5 | Tian & Feng, *VSS-LMS based on modified versoria function* | [↗](zotero://select/items/0_NCKN38JM) | 2026 | 修正 Versoria |
| 6 | Song & Zhao, *FXLMS/F with convex combination* | [↗](zotero://select/items/0_FERIFUEJ) | 2019 | 凸组合 FxLMS/F |
| 7 | Kar, *Momentum perturbed VSS for HNANC* | [↗](zotero://select/items/0_NEWLEZ9B) | 2024 | 动量扰动 |
| 8 | Kar & Burra, *VSS combined FxLMS* | [↗](zotero://select/items/0_W67EQD8F) | 2025 | 组合 FxLMS |
| 9 | Le & Dang, *Convex combination Chebyshev nonlinear filter* | [↗](zotero://select/items/0_ZXUHQ2ET) | 2025 | 凸组合非线性滤波 |

---

## 3. 基于 Versiera/Versoria 函数的 VSS

### 3.1 Versiera 函数法（Yu & Zhao, 2013）

**Zotero**: [IZATI7ZF](zotero://select/items/0_IZATI7ZF) — ICSPCC 2013

**Versiera 函数**（也叫 Agnesi 曲线）：
$$V(x) = \frac{a^3}{x^2 + a^2}$$

在 VSS-NLMS 中，将误差信号映射为：
$$\mu[n] = \mu_{\max} \cdot \frac{a^3}{e^2[n] + a^2}$$

其中 $a$ 为控制参数。改进版引入**功率估计自适应**：
$$a[n] = \alpha \cdot a[n-1] + (1-\alpha) \cdot e^2[n]$$

**算法步骤**：
1. 计算瞬时功率估计：$p[n] = \alpha p[n-1] + (1-\alpha) e^2[n]$
2. 计算 Versiera 步长：$\mu[n] = \mu_{\max} \cdot \frac{p[n]}{e^2[n] + p[n]}$
3. NLMS 更新：$\mathbf{w}[n+1] = \mathbf{w}[n] + \frac{\mu[n]}{\|\mathbf{x}[n]\|^2 + \delta} e[n] \mathbf{x}[n]$

**收敛性分析**：

在稳态时 $E\{e^2[n]\} \approx \sigma_v^2$（噪声功率），此时：
$$\mu_{\text{ss}} \approx \mu_{\max} \cdot \frac{\sigma_v^2}{2\sigma_v^2} = \frac{\mu_{\max}}{2}$$

通过调节 $\mu_{\max}$ 可以控制稳态步长。

### 3.2 修正 Versoria 函数法（Tian & Feng, 2026）

**Zotero**: [NCKN38JM](zotero://select/items/0_NCKN38JM) — Sensors 2026

在 Versiera 基础上引入**修正因子**：
$$\mu[n] = \mu_{\max} \cdot \left(\frac{a^3}{e^2[n] + a^2}\right)^\gamma$$

其中 $\gamma > 0$ 为形状参数：
- $\gamma = 1$：退化为标准 Versiera
- $\gamma > 1$：收敛时步长下降更快
- $\gamma < 1$：收敛时步长更平缓

**抗干扰设计**（针对 anti-jamming 场景）：
$$a[n] = \beta \cdot a[n-1] + (1-\beta) \cdot |e[n]|$$

使用绝对值而非平方值，降低大误差脉冲（干扰）对步长的影响。

**对比实验**：
| 算法 | 稳态 MSE (dB) | 收敛迭代次数 | 抗干扰能力 |
|------|--------------|-------------|-----------|
| 标准 LMS | -25.3 | 200 | 差 |
| VSS-LMS (Kwong) | -32.1 | 120 | 中 |
| VSS-LMS (Versiera) | -35.8 | 100 | 好 |
| **VSS-LMS (修正 Versoria)** | **-38.2** | **85** | **最优** |

---

## 4. 基于噪声功率估计的 VSS

### 4.1 噪声功率估计法（Zhao & Yu, 2013/2015）

**Zotero**: [BZNLP2NQ](zotero://select/items/0_BZNLP2NQ) — ICICIP 2013; [9KNF4YUC](zotero://select/items/0_9KNF4YUC) — arXiv 2015

**核心思想**：利用系统噪声功率 $\sigma_v^2$ 的估计来动态调整步长。

**噪声功率估计**：

在系统识别场景中，噪声功率估计为：
$$\widehat{\sigma}_v^2[n] = \alpha \widehat{\sigma}_v^2[n-1] + (1-\alpha) e^2[n] - \beta \|\mathbf{w}[n] - \mathbf{w}[n-1]\|^2$$

其中第二项补偿了滤波器系数变化带来的额外误差。

**步长公式**：
$$\mu[n] = 1 - \frac{\widehat{\sigma}_v^2[n]}{\widehat{\sigma}_e^2[n] + \delta}$$

其中 $\widehat{\sigma}_e^2[n]$ 为误差信号功率估计。

**直观理解**：
- 收敛初期：$\widehat{\sigma}_e^2 \gg \widehat{\sigma}_v^2$ → $\mu \approx 1$（大步长）
- 稳态时：$\widehat{\sigma}_e^2 \approx \widehat{\sigma}_v^2$ → $\mu \approx 0$（小步长）

**算法流程**：

```
初始化: w[0] = 0, σ̂²_v[0] = σ̂²_e[0] = 小值

for n = 0, 1, 2, ...:
    e[n] = d[n] - w[n]ᵀ x[n]              # 误差
    σ̂²_e[n] = α·σ̂²_e[n-1] + (1-α)·e²[n]  # 误差功率
    Δw = w[n] - w[n-1]                     # 系数变化
    σ̂²_v[n] = α·σ̂²_v[n-1] + (1-α)·e²[n] - β·‖Δw‖²  # 噪声功率
    μ[n] = 1 - σ̂²_v[n] / (σ̂²_e[n] + δ)    # 步长
    μ[n] = clip(μ[n], μ_min, μ_max)       # 限幅
    w[n+1] = w[n] + (μ[n] / (‖x[n]‖² + δ)) · e[n] · x[n]
```

**与经典方法的比较**：

| 方法 | 步长依赖 | 计算量/迭代 | 需要预设参数 |
|------|---------|------------|-------------|
| Kwong & Johnston | $|e[n]e[n-1]|$ | $O(N)$ + 2 参数 | $\alpha, \gamma$ |
| Aboulnasr & May | $e^2[n-1]$ | $O(N)$ + 2 参数 | $\alpha, \beta$ |
| **Zhao & Yu** | $\widehat{\sigma}_v^2 / \widehat{\sigma}_e^2$ | $O(N)$ + 3 参数 | $\alpha, \beta, \delta$ |
| **优势** | 物理意义明确 | 额外计算量小 | 参数有明确物理含义 |

---

## 5. 基于误差自相关的 VSS

### 5.1 非参数误差自相关法（Zipf, 2025）

**Zotero**: [9XV54S6J](zotero://select/items/0_9XV54S6J) — IJMIC 2025

**核心思想**：利用误差自相关函数 $R_{ee}(\tau)$ 在 $\tau=0$ 和 $\tau=1$ 的比值来判断收敛状态。

**误差自相关估计**：
$$\widehat{R}_{ee}[n] = \alpha \widehat{R}_{ee}[n-1] + (1-\alpha) e[n] \cdot e[n-1]$$

**步长公式**：
$$\mu[n] = \mu_{\max} \cdot \tanh\left(\kappa \cdot \left|\frac{\widehat{R}_{ee}[n]}{\widehat{R}_{ee}[0]}\right|\right)$$

其中 $\widehat{R}_{ee}[0]$ 为误差方差估计，$\kappa$ 为比例因子。

**为什么有效**：
- 收敛初期：$e[n]$ 和 $e[n-1]$ 高度相关 → $|R_{ee}[1]/R_{ee}[0]| \approx 1$ → 大步长
- 稳态时：$e[n]$ 接近白噪声 → $R_{ee}[1] \approx 0$ → 小步长

**非参数特性**：

该方法不需要知道噪声功率 $\sigma_v^2$，也不需要假设信号模型，因此称为"非参数"（non-parametric）。相比需要噪声功率估计的方法，它在非平稳噪声环境下更鲁棒。

**应用范围**：
- 系统识别
- 回声消除
- 信道均衡
- 噪声消除

---

## 6. 动量扰动 VSS

### 6.1 智能动量扰动法（Kar, 2024）

**Zotero**: [NEWLEZ9B](zotero://select/items/0_NEWLEZ9B) — Digital Signal Processing 2024

**应用场景**：混合主动噪声控制（HNANC）系统。

**核心思想**：在步长更新中引入**动量项**（momentum），加速收敛并避免局部极小。

**更新方程**：
$$\mu[n] = \alpha \mu[n-1] + \beta |e[n]| + \gamma |\mu[n-1] - \mu[n-2]|$$

其中第三项为**动量扰动**（momentum perturbation），捕获步长的变化趋势。

**在 HNANC 中的应用**：

HNANC = 前馈 FxLMS + 反馈 ANC。两个通道各自独立调整 VSS：

```
前馈通道:
  μ_ff[n] = α·μ_ff[n-1] + β·|e_ff[n]| + γ·|Δμ_ff[n-1]|
  w_ff[n+1] = w_ff[n] + (μ_ff[n]/(‖x_ff[n]‖²+δ))·e_ff[n]·x_ff[n]

反馈通道:
  μ_fb[n] = α·μ_fb[n-1] + β·|e_fb[n]| + γ·|Δμ_fb[n-1]|
  w_fb[n+1] = w_fb[n] + (μ_fb[n]/(‖x_fb[n]‖²+δ))·e_fb[n]·x_fb[n]
```

**性能指标**：
- Mean Noise Reduction (MNR): 比固定步长高 3-5 dB
- Mean Square Error (MSE): 收敛速度快 40%

---

## 7. 凸组合 VSS

### 7.1 凸组合 FxLMS/F（Song & Zhao, 2019）

**Zotero**: [FERIFUEJ](zotero://select/items/0_FERIFUEJ) — MSSP 2019, 重要论文

**背景**：FxLMS/F（Filtered-x Least Mean Square/Fourth）利用四阶代价函数 $J = E\{e^4[n]\}$，对非高斯噪声更鲁棒，但收敛速度慢。

**凸组合方案**：

将两个滤波器（快速 FxLMS + 鲁棒 FxLMS/F）的输出凸组合：
$$y[n] = \lambda[n] y_1[n] + (1-\lambda[n]) y_2[n]$$

其中 $0 \leq \lambda[n] \leq 1$ 为混合参数。

**混合参数更新**：
$$a[n+1] = a[n] + \mu_a \cdot e[n] \cdot (y_1[n] - y_2[n]) \cdot \mathbf{x}_f^T[n] \cdot \mathbf{w}_{\text{combined}}[n]$$

$$\lambda[n] = \frac{1}{1 + e^{-a[n]}}$$

（sigmoid 函数保证 $0 \leq \lambda \leq 1$）

**算法流程**：

```
滤波器 1 (FxLMS):  快速收敛，稳态误差大
  w₁[n+1] = w₁[n] + μ₁·e[n]·x_f[n]

滤波器 2 (FxLMS/F): 慢速收敛，稳态误差小
  w₂[n+1] = w₂[n] + μ₂·e³[n]·x_f[n]

组合输出:
  λ[n] = 1/(1 + exp(-a[n]))
  y[n] = λ[n]·y₁[n] + (1-λ[n])·y₂[n]
  e[n] = d[n] - y[n]

混合参数更新:
  a[n+1] = a[n] + μ_a·e[n]·(y₁[n]-y₂[n])·x_f[n]·(λ[n](1-λ[n]))
```

**为什么有效**：
- 收敛初期：$a[n] \approx 0$ → $\lambda \approx 0.5$，两个滤波器权重接近
- 中期：$a[n] \to +\infty$ → $\lambda \to 1$，主要由 FxLMS 主导（快速）
- 稳态：$a[n]$ 自适应调整，在 FxLMS 和 FxLMS/F 之间找到最优平衡

**对比实验**：
| 算法 | 收敛时间 (ms) | 稳态 MSE (dB) | 非高斯噪声鲁棒性 |
|------|--------------|--------------|----------------|
| FxLMS | 50 | -18 | 差 |
| FxLMS/F | 200 | -28 | 好 |
| **Convex FxLMS/F** | **60** | **-26** | **好** |

### 7.2 凸组合 Chebyshev 非线性滤波（Le & Dang, 2025）

**Zotero**: [ZXUHQ2ET](zotero://select/items/0_ZXUHQ2ET) — SIVP 2025

**核心思想**：将 Chebyshev 非线性滤波器与线性滤波器凸组合，同时捕获线性和非线性噪声成分。

**Chebyshev 滤波器**：
$$y_{\text{cheb}}[n] = \sum_{k=0}^{K} \mathbf{h}_k^T \cdot T_k(\mathbf{x}[n])$$

其中 $T_k(\cdot)$ 为 $k$ 阶 Chebyshev 多项式。

**凸组合**：
$$y[n] = \lambda[n] y_{\text{linear}}[n] + (1-\lambda[n]) y_{\text{cheb}}[n]$$

**部分更新策略（Partial Update）**：

为降低计算量，每次迭代只更新 $M$ 个系数中的 $M/2$ 个：
- 基于系数幅度选择（LUP）：更新幅度最大的 $M/2$ 个
- 基于周期性选择（SPU）：交替更新奇偶索引

---

## 8. VSS FxLMS 在 ANC 中的应用

### 8.1 组合 VSS FxLMS（Kar & Burra, 2025）

**Zotero**: [W67EQD8F](zotero://select/items/0_W67EQD8F) — CSSP 2025

**问题**：当参考噪声信号与干扰噪声**相关**时，标准 FxLMS 性能下降。

**解决方案**：结合联立方程法（SEM）和 VSS-FxLMS。

**VSS 更新**：
$$\mu[n] = \mu_{\min} + (\mu_{\max} - \mu_{\min}) \cdot \frac{e^2[n]}{e^2[n] + \sigma_{\text{ref}}^2[n]}$$

其中 $\sigma_{\text{ref}}^2[n]$ 为参考信号功率估计。

**SEM + VSS-FxLMS 联合算法**：

```
Step 1: 用 SEM 估计初级路径 P(z)
Step 2: 用 SEM 估计次级路径 S(z)
Step 3: VSS-FxLMS 更新
  μ[n] = μ_min + (μ_max - μ_min) · e²[n] / (e²[n] + σ²_ref[n])
  w[n+1] = w[n] + (μ[n] / (‖x_f[n]‖²+δ)) · e[n] · x_f[n]
```

**性能**：
- 相关噪声场景：比标准 FxLMS 高 5-8 dB
- 不相关噪声场景：与标准 FxLMS 相当

---

## 9. 算法对比总结

### 9.1 核心公式对比

| 方法 | 步长公式 | 关键参数 | 计算量 |
|------|---------|---------|--------|
| **Versiera** (Yu & Zhao 2013) | $\mu_{\max} \cdot \frac{a^3}{e^2+a^2}$ | $\mu_{\max}, a$ | $O(N)+2$ mult |
| **修正 Versoria** (Tian 2026) | $\mu_{\max} \cdot \left(\frac{a^3}{e^2+a^2}\right)^\gamma$ | $\mu_{\max}, a, \gamma$ | $O(N)+3$ mult |
| **噪声功率估计** (Zhao & Yu 2015) | $1 - \frac{\widehat{\sigma}_v^2}{\widehat{\sigma}_e^2}$ | $\alpha, \beta$ | $O(N)+4$ mult |
| **误差自相关** (Zipf 2025) | $\mu_{\max} \cdot \tanh(\kappa|R_{ee}|)$ | $\mu_{\max}, \kappa, \alpha$ | $O(N)+3$ mult |
| **动量扰动** (Kar 2024) | $\alpha\mu[n-1]+\beta|e|+\gamma|\Delta\mu|$ | $\alpha, \beta, \gamma$ | $O(N)+3$ mult |
| **凸组合** (Song & Zhao 2019) | $\lambda = \text{sigmoid}(a)$ | $\mu_1, \mu_2, \mu_a$ | $O(N)+$双滤波器 |

### 9.2 适用场景对比

| 方法 | 系统识别 | ANC | 回声消除 | 非平稳噪声 | 非高斯噪声 |
|------|:--------:|:---:|:--------:|:---------:|:---------:|
| Versiera | ✅ | ✅ | ✅ | ⚠️ | ⚠️ |
| 修正 Versoria | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| 噪声功率估计 | ✅✅ | ⚠️ | ✅ | ⚠️ | ⚠️ |
| 误差自相关 | ✅ | ✅ | ✅✅ | ✅✅ | ⚠️ |
| 动量扰动 | ⚠️ | ✅✅ | ⚠️ | ✅ | ⚠️ |
| 凸组合 FxLMS/F | ⚠️ | ✅✅ | ⚠️ | ⚠️ | ✅✅ |
| 凸组合 Chebyshev | ⚠️ | ✅ | ✅ | ⚠️ | ✅ |

### 9.3 参数敏感性

| 方法 | 参数数量 | 调参难度 | 鲁棒性 |
|------|---------|---------|--------|
| Versiera | 2 | 低 | 中 |
| 修正 Versoria | 3 | 中 | 高 |
| 噪声功率估计 | 3 | 中 | 中 |
| 误差自相关 | 3 | 中 | **高** |
| 动量扰动 | 3 | 中 | 中 |
| 凸组合 FxLMS/F | 4 | 高 | **高** |

---

## 10. 关键设计原则总结

### 10.1 步长函数的理想特性

1. **单调性**：$\mu(e)$ 随 $|e|$ 增大而增大
2. **有界性**：$0 < \mu_{\min} \leq \mu[n] \leq \mu_{\max} < 2$（稳定性保证）
3. **对称性**：$\mu(e) = \mu(-e)$
4. **平滑性**：$\mu(e)$ 连续可导（避免步长突变）
5. **鲁棒性**：对异常值（outliers）不敏感

### 10.2 Versiera/Versoria vs 其他函数的选择

| 函数 | 公式 | 计算量 | 鲁棒性 | 适用场景 |
|------|------|--------|--------|---------|
| **Versiera** | $\frac{a^3}{e^2+a^2}$ | 除+平方 | 中 | 一般用途 |
| **修正 Versoria** | $(\frac{a^3}{e^2+a^2})^\gamma$ | 除+平方+幂 | 高 | 抗干扰 |
| **Sigmoid** | $\frac{1}{1+e^{-ae}}$ | 指数 | 中 | 凸组合 |
| **Tanh** | $\tanh(ae^2)$ | 双曲 | 高 | 误差自相关 |
| **Sign** | $\text{sgn}(|e|-T)$ | 比较 | 低 | 简单场景 |

### 10.3 在 ANC 中应用 VSS 的注意事项

1. **FxLMS 中的二次路径影响**：步长需要针对滤波后的参考信号 $\mathbf{x}_f[n] = \hat{s}[n] * \mathbf{x}[n]$ 归一化
2. **声学反馈**：VSS 可能加剧反馈不稳定性，需要配合 AFC
3. **实时性约束**：步长计算不能增加 DSP 延迟（通常在 45µs 预算内）
4. **多通道扩展**：多通道 ANC 中每个通道独立 VSS 可能不协调，需要联合步长控制

---

## 相关 Wiki 页面

- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — FxLMS 标准算法
- [[concepts/active-noise-control|Active Noise Control]] — ANC 概述
- [[concepts/online-secondary-path-modeling|Online Secondary-Path Modeling]] — 在线次级路径建模（VSS 在 ANC 中的前提）
