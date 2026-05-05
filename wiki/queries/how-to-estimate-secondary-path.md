---
type: query
created: 2026-04-10
updated: 2026-04-10
sources:
tags:
  - anc
  - secondary-path
  - system-identification
  - literature-review
---

# 如何估计次级通道

**Question**: 如何估计次级通道 S(z)

> **Zotero 链接**: 所有文献引用都包含 `zotero://select/items/0_XXX` 链接。在 Obsidian 中点击即可直接在 Zotero 中打开对应条目（需 Zotero 运行中）。

## 次级通道是什么

次级通道 S(z) 是从控制器输出到误差传感器之间的完整传递函数，包含：

```
D/A → 重构滤波器 → 功率放大器 → 扬声器 → 声学路径 → 误差麦克风 → 前置放大器 → 抗混叠滤波器 → A/D
```

它是传统 FXLMS 算法的核心 — 参考信号必须通过 Ŝ(z) 滤波后才能用于权重更新。没有准确的 Ŝ(z)，FXLMS 算法会**不稳定**。

FXLMS 算法对 Ŝ(z) 的精度要求不算苛刻：慢自适应条件下可容忍 **~90° 相位误差**，40° 以内几乎不影响收敛速度。

---

## 分类一：需要显式建模 S(z)

### 方法 1.1：离线建模（Offline Modeling）

**最简单、最常用**。在 ANC 系统正式运行前一次性估计 Ŝ(z)。

#### 步骤

1. 停止 ANC 控制器（W(z) = 0）
2. 注入白噪声 v(n) 驱动次级源（扬声器）
3. 记录误差麦克风输出 e(n)
4. 用 LMS 算法自适应一个 FIR 滤波器 Ŝ(z)，使其输出逼近 e(n)
5. 收敛后将 Ŝ(z) 固定，启动 ANC

#### 适用场景

- 次级通道**变化缓慢**的固定安装
- 大多数工业 ANC 应用

#### 局限

- 次级通道**时变**时（温度、气流、耳机佩戴位置），离线估计很快过时
- 需要 ANC 系统**停机**重新建模

---

### 方法 1.2：加性随机噪声在线建模（Additive Random Noise Online Modeling）

**Kuo & Morgan (1999) Section VI 推荐的标准方法。**

在系统中注入一个**低功率零均值白噪声** v(n)：

```
y(n) + v(n) → [S(z)] → e(n)
```

辨识时**只用 v(n) 作为参考信号**：

```
ŝ(n+1) = ŝ(n) + μ_v · e(n) · v(n)
```

#### 收敛分析

关键结论：在线建模所需迭代次数是离线的 **σ_d² / σ_v² 倍**。若干扰功率 σ_d² 是注入噪声功率 σ_v² 的 100 倍（-20 dB），则在线建模需要 **100 倍**的时间才能收敛。

#### 改进技术

1. **自适应噪声消除**：用额外自适应滤波器以 x(n) 为参考从 e(n) 中消除 dₑ(n)。可提升收敛速度 **~30 倍**。
2. **自适应预测器**：在 e(n) 前加自适应预测误差滤波器，最佳延迟等于次级通道脉冲响应长度。

#### 近年进展（Zotero 文献）

| 文献                                                                     | 年份   | 贡献                                                            |
| ---------------------------------------------------------------------- | ---- | ------------------------------------------------------------- |
| Yang & Liu (2026) [J83HULJT](zotero://select/items/0_J83HULJT)         | 2026 | **RMFxLMS** — Reference-modulated noise injection，强背景噪声下的在线建模 |
| Cao & Lu (2025) [9EK2RDGX](zotero://select/items/0_9EK2RDGX)           | 2025 | **ELSTM-ANC-OSPM** — LSTM + MCC（最大相关熵准则）的在线建模，高斯噪声鲁棒          |
| Ji, Shi & Dongyuan (2023) [P5YI3AHL](zotero://select/items/0_P5YI3AHL) | 2023 | **计算高效的在线建模技术**，适用于 Modified FXLMS                            |
| Lao & Chang (2025) [RNFPJBE6](zotero://select/items/0_RNFPJBE6)        | 2025 | **混合 ANC 系统**中的在线建模，含硬件验证                                     |

---

### 方法 1.3：整体建模算法（Overall Modeling Algorithm）

用**三个自适应滤波器**同时完成噪声控制和次级通道辨识：

| 滤波器 | 作用 |
|--------|------|
| **W(z)** | 噪声控制器 |
| **Ŝ₁(z)** | 次级通道估计 |
| **Ŝ₂(z)** | 建模 Ŝ₁(z) 输出中的干扰成分 |

**优点**：不需要额外注入噪声 v(n)。
**缺点**：解不唯一，需要离线初始化。

---

### 方法 1.4：次级通道系数更新方法

| 文献 | 年份 | 贡献 |
|------|------|------|
| [Y8AMJVJM](zotero://select/items/0_Y8AMJVJM) | 2001 | Method to update coefficients of secondary path filter under ANC |
| Hsu & Cheng [KJTPS5AW](zotero://select/items/0_KJTPS5AW) | — | **Auto-selection method** — 自动选择建模次级路径估计滤波器 |

---

## 分类二：不需要注入辅助噪声

### 方法 2.1：联立方程法（Simultaneous Equations Method）

完全**不需要注入辅助噪声**，利用 ANC 系统中多个信号路径之间的代数关系建立联立方程组。

| 文献 | 年份 | 贡献 |
|------|------|------|
| Fujii & Muneyasu (1999) [XTIZ5EBN](zotero://select/items/0_XTIZ5EBN) | 1999 | **Simultaneous equations method not requiring the secondary path filter** — 早期工作 |
| Kajikawa & Nomura (2000) [QSWTDNSS](zotero://select/items/0_QSWTDNSS) | 2000 | Active noise control system without secondary path model |
| Jin, Yang & Xiao (2007) [CNPKK8D4](zotero://select/items/0_CNPKK8D4) | 2007 | **A simultaneous equation method-based online secondary path modeling algorithm** — 成熟版本，无需辅助滤波器系数估计 |

### 原理

在 ANC 运行过程中，系统在多个时刻/多通道条件下产生多组观测方程：

```
e₁(n) = d(n) + s · y₁(n)
e₂(n) = d(n) + s · y₂(n)
...
```

通过**联立求解**，可以同时辨识出 W(z) 和 S(z)。

### 优点/局限

- ✅ 完全不需要注入噪声 v(n)，不干扰降噪性能
- ❌ 可解性依赖于信号的激励充分性 — 窄带信号时可能欠定
- ❌ 对测量噪声更敏感

---

## 分类三：完全不需要辨识 S(z)

### 方法 3.1：基于 SPR 性质的算法

**Zhou & DeBrunner (2007)** [UJV4I3KI](zotero://select/items/0_UJV4I3KI) — 利用 **严格正实（Strictly Positive Real, SPR）** 性质设计 ANC 算法，不需要次级通道辨识。

- 基于 SPR 性质的滤波器设计确保收敛
- 适用于窄带 ANC
- 引用数：61

---

### 方法 3.2：进化/启发式搜索

| 文献                             | 年份   | 方法                        | 引用  | 标签                                                |
| ------------------------------ | ---- | ------------------------- | --- | ------------------------------------------------- |
| Chang & Chen (2010) [T8ZAD79B](zotero://select/items/0_T8ZAD79B) | 2010 | **自适应遗传算法 (AGA)**         | 96  | local minima, plant measurement                   |
| Chen & Chang (2009) [CWR692AB](zotero://select/items/0_CWR692AB) | 2009 | **自适应进化 ANC**             | 1   | —                                                 |
| Rout & Das (2012) [4GXVZ5JC](zotero://select/items/0_4GXVZ5JC)   | 2012 | **条件重初始化 PSO (CRPSO)**    | 72  | particle swarm optimization                       |
| Zhou & Zhao (2023) [TUGAUJFN](zotero://select/items/0_TUGAUJFN)  | 2023 | **GA-based adaptive ANC** | 11  | conditional reinitialization, online optimization |
| Ren & Zhang (2021) [GTJECBSQ](zotero://select/items/0_GTJECBSQ)  | 2021 | **无需次级通道建模的 ANC 算法与实现**   | 1   | —                                                 |

#### 遗传算法核心思想

不用梯度下降，而是维护一组候选 FIR 滤波器权重向量（种群），直接通过物理系统评估每个候选的适应度 F(w_i) = 1/(e_i² + ε)，用选择/交叉/变异迭代逼近最优解。

#### PSO 核心思想

用粒子群优化搜索最优控制器权重，通过条件重初始化避免陷入局部最优。

#### 优点/局限

- ✅ 完全不需要辨识 S(z)，容忍非线性次级通道，全局优化
- ❌ 计算复杂度极高，收敛慢，实时实现困难

---

### 方法 3.3：Careful Control（无需先验 S(z) 模型）

| 文献 | 年份 | 贡献 |
|------|------|------|
| Lopes & Gerald (2022) [JDJM5PAN](zotero://select/items/0_JDJM5PAN) | 2022 | **Careful least squares ANC with no prior secondary path model** — dual control, overall modeling |
| Lopes & Gerald (2024) [Z8AZA5Z3](zotero://select/items/0_Z8AZA5Z3) | 2024 | **Careful feedback ANC robust to large secondary path changes** — 对次级通道大变化鲁棒 |

"Careful control" 方法通过同时探索（exploration）和控制（exploitation），在没有先验 S(z) 模型的情况下实现 ANC，同时逐步学习 S(z)。

---

### 方法 3.4：元学习初始化

**Yang & Rao (2026)** [QBSF7T36](zotero://select/items/0_QBSF7T36) — 通过**元学习**（Meta-Learning）对控制滤波器和次级通道进行联合初始化，加速后续在线自适应。

- 结合机器学习与 ANC
- 适用于次级通道快速变化的场景

---

## 分类四：次级通道变化应对策略

### 方法 4.1：性能加权混合 FxLMS

**Sarkar & Mittal (2025)** [C4FC46KQ](zotero://select/items/0_C4FC46KQ) — **Performance-weighted blended FxLMS for changing secondary paths**

当次级通道变化时，不重新辨识 S(z)，而是混合多个预训练的 S(z) 模型，根据当前性能加权选择。

---

### 方法 4.2：建模误差影响分析

| 文献 | 年份 | 贡献 | 引用 |
|------|------|------|------|
| Lopes & Piedade (2004) [T5HV3E7L](zotero://select/items/0_T5HV3E7L) | 2004 | **Modified FX-LMS with secondary path modeling errors** — 分析建模误差对算法行为的影响 | 47 |
| Tabatabaei Ardekani & Abdulla (2012) [DC36URS5](zotero://select/items/0_DC36URS5) | 2012 | **Effects of imperfect secondary path modeling** — 不完备建模对收敛和稳态性能的影响分析 | 67 |

---

## 完整方法对比表

| 类别 | 方法 | 需要 Ŝ(z)? | 注入噪声? | 计算量 | 实时可行? | 代表文献 |
|------|------|-----------|----------|--------|----------|---------|
| **离线** | 离线建模 | 是 | 一次性 | 低 | ✅ | Kuo 1999 |
| **加性噪声在线** | 加性随机噪声 | 是 | 持续 | 中 | ✅ | Kuo 1999, Yang 2026 |
| **加性噪声在线** | ELSTM-ANC-OSPM | 是 | 持续 | 高 | ✅ | Cao 2025 |
| **无噪声在线** | 整体建模（3 滤波器） | 是 | **否** | 高 | ✅ | Kuo 1999 |
| **无噪声在线** | 联立方程法 | 是 | **否** | 中高 | ✅ | Jin 2007, Fujii 1999 |
| **无噪声在线** | 次级通道系数更新 | 是 | **否** | 中 | ✅ | Y8AMJVJM |
| **SPR** | SPR 性质算法 | **不需要** | **否** | 低 | ✅ | Zhou 2007 |
| **启发式** | 遗传算法 | **不需要** | **否** | 极高 | ❌ | Chang 2010, Zhou 2023 |
| **启发式** | PSO (CRPSO) | **不需要** | **否** | 极高 | ❌ | Rout 2012 |
| **Careful** | Careful least squares | 学习得到 | **否** | 中 | ✅ | Lopes 2022, 2024 |
| **混合** | 性能加权混合 FxLMS | 多模型 | **否** | 中 | ✅ | Sarkar 2025 |
| **元学习** | 元学习初始化 | 是 | 初始阶段 | 高（训练） | ✅ | Yang 2026 |

---

## Zotero 文献库中的 21 篇相关论文

### 在线建模（加性噪声）
1. **[J83HULJT](zotero://select/items/0_J83HULJT)** Yang & Liu (2026) — Reference-modulated noise injection for online secondary path modeling
2. **[9EK2RDGX](zotero://select/items/0_9EK2RDGX)** Cao & Lu (2025) — ELSTM-ANC-OSPM: enhanced LSTM in ANC with online secondary path modeling
3. **[P5YI3AHL](zotero://select/items/0_P5YI3AHL)** Ji et al. (2023) — Computation-efficient online secondary path modeling for Modified FXLMS
4. **[RNFPJBE6](zotero://select/items/0_RNFPJBE6)** Lao & Chang (2025) — Online secondary path modeling in hybrid ANC

### 联立方程法（无噪声注入）
5. **[CNPKK8D4](zotero://select/items/0_CNPKK8D4)** Jin & Yang (2007) — Simultaneous equation method-based online secondary path modeling
6. **[XTIZ5EBN](zotero://select/items/0_XTIZ5EBN)** Fujii & Muneyasu (1999) — Simultaneous equations method not requiring secondary path filter
7. **[QSWTDNSS](zotero://select/items/0_QSWTDNSS)** Kajikawa & Nomura (2000) — ANC system without secondary path model

### 不需要辨识 S(z) — 启发式/进化搜索
8. **[T8ZAD79B](zotero://select/items/0_T8ZAD79B)** Chang & Chen (2010) — Active noise cancellation without secondary path identification using adaptive GA (96 citations)
9. **[TUGAUJFN](zotero://select/items/0_TUGAUJFN)** Zhou & Zhao (2023) — GA-based adaptive ANC without secondary path identification
10. **[4GXVZ5JC](zotero://select/items/0_4GXVZ5JC)** Rout & Das (2012) — PSO-based ANC without secondary path identification (72 citations)
11. **[CWR692AB](zotero://select/items/0_CWR692AB)** Chen & Chang (2009) — Adaptive evolutionary ANC without secondary path measurement
12. **[GTJECBSQ](zotero://select/items/0_GTJECBSQ)** Ren & Zhang (2021) — ANC without secondary path modeling: algorithm and implementation

### 不需要辨识 S(z) — SPR 性质
13. **[UJV4I3KI](zotero://select/items/0_UJV4I3KI)** Zhou & DeBrunner (2007) — New ANC algorithm requiring no secondary path identification based on SPR (61 citations)

### 不需要辨识 S(z) — Careful Control
14. **[JDJM5PAN](zotero://select/items/0_JDJM5PAN)** Lopes & Gerald (2022) — Careful least squares ANC with no prior secondary path model
15. **[Z8AZA5Z3](zotero://select/items/0_Z8AZA5Z3)** Lopes & Gerald (2024) — Careful feedback ANC robust to large secondary path changes

### 元学习初始化
16. **[QBSF7T36](zotero://select/items/0_QBSF7T36)** Yang & Rao (2026) — Co-initialization of control filter and secondary path via meta-learning

### 次级通道变化应对
17. **[C4FC46KQ](zotero://select/items/0_C4FC46KQ)** Sarkar & Mittal (2025) — Performance-weighted blended FxLMS for changing secondary paths
18. **[KJTPS5AW](zotero://select/items/0_KJTPS5AW)** Hsu & Cheng — Auto-selection method for modeling secondary-path estimation filter
19. **[Y8AMJVJM](zotero://select/items/0_Y8AMJVJM)** (2001) — Method to update coefficients of secondary path filter under ANC

### 建模误差分析
20. **[T5HV3E7L](zotero://select/items/0_T5HV3E7L)** Lopes & Piedade (2004) — Behavior of modified FX-LMS with secondary path modeling errors (47 citations)
21. **[DC36URS5](zotero://select/items/0_DC36URS5)** Tabatabaei Ardekani & Abdulla (2012) — Effects of imperfect secondary path modeling (67 citations)

---

## Related Concepts

- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[../concepts/active-noise-control|Active Noise Control]]
- [[../concepts/broad-band-feedforward-anc|Broad-Band Feedforward ANC]]
- [[../concepts/multi-channel-anc|Multi-Channel ANC]]
- [[../concepts/online-secondary-path-modeling|Online Secondary-Path Modeling]]

## Related Sources

- [[../sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] — Section II-C (FXLMS), Section VI (Online Secondary-Path Modeling)
- [[../sources/wu-2014-simplified-adaptive-feedback-anc|Wu 2014: Simplified Adaptive Feedback ANC]] — Uses leaky FxLMS with offline secondary path modeling

---

## 附录：各方法推导公式

### A. 离线建模推导

**系统辨识框架**：ANC 停机（W(z) = 0），注入白噪声 v(n) 通过次级通道：

```
e(n) = s(n) * v(n)
```

其中 s(n) 是 S(z) 的脉冲响应。用 FIR 滤波器 ŝ(n) 建模，误差为：

```
ε(n) = e(n) - ŝᵀ(n) v(n)
```

LMS 更新最小化 J(n) = ε²(n)：

```
ŝ(n+1) = ŝ(n) + μ · ε(n) · v(n)
```

收敛条件：`0 < μ < 2 / (L · σ_v²)`，其中 L 是滤波器阶数，σ_v² 是 v(n) 的功率。

---

### B. 加性随机噪声在线建模推导（Kuo 1999 Eq. 59-63）

#### B.1 系统信号流

```
x(n) → [W(z)] → y(n) ──┬──→ [S(z)] ──→ e(n) = dₑ(n) + s(n)*y(n) + s(n)*v(n)
                        │
v(n) ───────────────────┘
```

误差信号分解为两部分：

```
e(n) = dₑ(n) + s(n) * v(n)
```

其中 `dₑ(n) = d(n) + s(n) * y(n)` 是原始噪声贡献（我们想消除的）。

#### B.2 LMS 更新与期望值分析

建模滤波器 ŝ(n) 用 LMS 更新：

```
ŝ(n+1) = ŝ(n) + μ_v · e(n) · v(n)          ...(62)
```

其中 `v(n) = [v(n), v(n-1), ..., v(n-L+1)]ᵀ` 是参考信号向量。

对 (62) 取期望：

```
E[ŝ(n+1)] = E[ŝ(n)] + μ_v · E[e(n) · v(n)]
```

由于 v(n) 与 dₑ(n) **不相关**：

```
E[e(n) · v(n)] = E[(dₑ(n) + s(n)*v(n)) · v(n)]
               = E[dₑ(n)·v(n)] + E[(s(n)*v(n))·v(n)]
               = 0 + R_vv · s
```

其中 R_vv = E[v(n)vᵀ(n)] = σ_v² · I（白噪声的自相关矩阵是对角阵）。

因此：

```
E[ŝ(n+1)] = E[ŝ(n)] + μ_v · σ_v² · s
```

收敛到 `E[ŝ(∞)] = s` 当且仅当 `0 < μ_v < 2/σ_v²`。

#### B.3 建模误差分析

然而，瞬时更新中 dₑ(n) 充当**干扰噪声**：

```
ŝ(n+1) = ŝ(n) + μ_v · [dₑ(n) + sᵀv(n)] · v(n)
       = ŝ(n) + μ_v · dₑ(n)·v(n)  ⏟ 干扰项  + μ_v · sᵀv(n)·v(n)
```

收敛后的均方建模误差为 [9]：

```
E[||s - ŝ(∞)||²] = μ_v · σ_d² / (2 · σ_v²) · ||s||²     ...(63)
```

**关键结论**：在线建模的步长上限比离线建模小 `σ_d²/σ_v²` 倍。

例：若 σ_v/σ_d = -20 dB（即 σ_d²/σ_v² = 100），指定归一化建模误差为 0.01，则：

```
μ_v ≤ 0.01 × (σ_v² / σ_d²) × (2/L) = (2/L) / 100
```

收敛时间比离线建模慢 **100 倍**。

#### B.4 自适应噪声消除改进

用额外的自适应滤波器以 x(n) 为参考从 e(n) 中消除 dₑ(n)：

```
d̂ₑ(n) = aᵀ(n) · x(n)
e'(n) = e(n) - d̂ₑ(n)
ŝ(n+1) = ŝ(n) + μ_v · e'(n) · v(n)
```

其中 a(n) 用独立的 LMS 更新。实验表明收敛速度提升 **~30 倍**。

---

### C. 整体建模算法推导（3 滤波器法）

#### C.1 系统结构

```
x(n) → [W(z)] → y(n) ──→ [S(z)] ──→ e(n)
                           ↑
                    [Ŝ₁(z)] ← y(n)
                           ↑
                    [Ŝ₂(z)] ← e(n)
```

三个滤波器同时更新：

1. **W(z)** — 噪声控制器（FxLMS）
2. **Ŝ₁(z)** — 次级通道估计
3. **Ŝ₂(z)** — 建模 Ŝ₁(z) 输出中的干扰

#### C.2 收敛分析

初始化阶段加入延迟 Δ 使初级和次级信号解耦：

```
初始化：Ŝ₁(z) → S(z),  Ŝ₂(z) → z^(-Δ)
```

正常运行阶段：

```
e(n) = d(n) + s(n) * y(n)
ŷ₁(n) = ŝ₁(n) * y(n)
ŷ₂(n) = ŝ₂(n) * e(n)

ŝ₁(n+1) = ŝ₁(n) + μ₁ · [e(n) - ŷ₁(n) - ŷ₂(n)] · y(n)
ŝ₂(n+1) = ŝ₂(n) + μ₂ · [e(n) - ŷ₁(n) - ŷ₂(n)] · e(n)
w(n+1)  = w(n)  + μ_w · e(n) · x̂_f(n)
```

其中 x̂_f(n) 是通过 Ŝ₁(z) 滤波的参考信号。

收敛后：

```
Ŝ₁(z) → S(z)
Ŝ₂(z) → z^(-Δ)
W(z) → P(z)/S(z)
```

#### C.3 解不唯一性证明

当 Ŝ₁(z) 和 Ŝ₂(z) 同时自适应时，存在多个稳态解满足：

```
Ŝ₁(z) + Ŝ₂(z) · S(z) = S(z)
```

即任何满足 `Ŝ₂(z) = 1 - Ŝ₁(z)/S(z)` 的解都是稳态解。需要通过离线初始化来固定到正确解。

---

### D. 联立方程法推导（Jin, Yang & Xiao 2007）

#### D.1 基本原理

ANC 系统运行时的误差信号：

```
e(n) = d(n) + sᵀ · y(n)                         (1)
```

在两个相邻时刻 n 和 n-1：

```
e(n)   = d(n)   + sᵀ · y(n)                      (2)
e(n-1) = d(n-1) + sᵀ · y(n-1)                    (3)
```

如果初级噪声 d(n) 变化缓慢（d(n) ≈ d(n-1)），两式相减：

```
e(n) - e(n-1) = sᵀ · [y(n) - y(n-1)]
Δe(n) = sᵀ · Δy(n)                               (4)
```

#### D.2 联立求解

收集 L 个连续时刻的差分方程：

```
[Δe(n), Δe(n-1), ..., Δe(n-L+1)]ᵀ = [Δy(n), Δy(n-1), ..., Δy(n-L+1)] · s
```

写成矩阵形式：

```
Δe = ΔY · s                                       (5)
```

其中 ΔY ∈ ℝ^(L×L) 是 Hankel 矩阵。如果 ΔY 满秩（需要 y(n) 有充分的激励多样性），则：

```
ŝ = ΔY⁻¹ · Δe                                    (6)
```

#### D.3 自适应实现

实际中 ΔY 可能接近奇异，用递推最小二乘（RLS）求解：

```
P(n) = P(n-1)/λ - P(n-1)·Δy(n)·Δyᵀ(n)·P(n-1) / [λ + Δyᵀ(n)·P(n-1)·Δy(n)]
ŝ(n) = ŝ(n-1) + P(n)·Δy(n)·[Δe(n) - Δyᵀ(n)·ŝ(n-1)]
```

其中 λ 是遗忘因子（0.95 ~ 1.0）。

#### D.4 无需辅助滤波器系数的改进（Jin 2007）

Jin 等人进一步消除了对辅助误差路径滤波器系数的需求。设误差路径为 F(z)，联立方程为：

```
e₁(n) = d(n) + s · y₁(n)
e₂(n) = d(n) + s · y₂(n)
```

通过构造两个独立的观测方程，同时消去 d(n) 和 f(n)（误差路径系数），直接解出 s。

---

### E. SPR 性质算法推导（Zhou & DeBrunner 2007）

#### E.1 SPR 性质回顾

一个传递函数 H(z) 是**严格正实（SPR）**的，如果：
1. H(z) 在 |z| ≥ 1 上解析（所有极点在单位圆内）
2. Re[H(e^(jω))] > 0, ∀ω ∈ [-π, π]

#### E.2 算法推导

考虑窄带 ANC 系统，参考信号为 x(n) = sin(ω₀n)。控制器输出：

```
y(n) = w₁(n)·sin(ω₀n) + w₂(n)·cos(ω₀n)
```

误差信号：

```
e(n) = d(n) + Re{S(e^(jω₀)) · W(e^(jω₀)) · e^(jω₀n)}
```

其中 W(e^(jω₀)) = w₁ - j·w₂ 是控制器在 ω₀ 处的频率响应。

如果 S(e^(jω₀)) 的实部 > 0（即 S(z) 在 ω₀ 处满足 SPR 性质），则更新：

```
w₁(n+1) = w₁(n) - μ · e(n) · sin(ω₀n)
w₂(n+1) = w₂(n) - μ · e(n) · cos(ω₀n)
```

收敛性证明：定义 Lyapunov 函数 V(n) = ||w(n) - w*||²，其中 w* 是最优解。

```
ΔV(n) = V(n+1) - V(n)
      = -2μ · e(n) · [s₁·sin(ω₀n) + s₂·cos(ω₀n)] · [Δw₁·sin(ω₀n) + Δw₂·cos(ω₀n)] + O(μ²)
```

当 Re[S(e^(jω₀))] > 0 时，ΔV(n) < 0，算法全局收敛。

#### E.3 宽带扩展

对于宽带信号，将信号分解为多个窄带子信号，对每个子带应用 SPR 条件。如果 S(z) 在整个频带内满足 SPR，则算法全局收敛。

---

### F. 遗传算法推导（Chang & Chen 2010）

#### F.1 问题表述

最小化误差信号功率：

```
min_w  J(w) = E[e²(n)] = E[(d(n) + wᵀx̃(n))²]
```

其中 x̃(n) = x(n) * s(n) 是通过实际物理次级通道的参考信号（未知）。

#### F.2 适应度评估

由于 S(z) 未知，不能直接计算 x̃(n)。但可以直接通过物理系统评估：

```
对每个候选 w_i：
  输出 y_i(n) = w_iᵀ · x(n)
  通过实际物理次级通道 S(z) 传播
  测量 e_i(n) = d(n) + y_i(n) * s(n)
  适应度 F(w_i) = 1 / (e_i²(n) + ε)
```

#### F.3 自适应遗传算法（AGA）

标准 GA 的交叉率 p_c 和变异率 p_m 是固定的。AGA 根据种群多样性自适应调整：

```
p_c = { k₁·(f_max - f')/(f_max - f_avg),  f' ≥ f_avg
      { k₂,                                f' < f_avg

p_m = { k₃·(f_max - f)/(f_max - f_avg),   f ≥ f_avg
      { k₄,                                f < f_avg
```

其中 f_max, f_avg 是种群最大和平均适应度，f' 是待交叉个体的适应度，f 是待变异个体的适应度。

**优点**：适应度高时（接近最优）降低交叉/变异率以精细搜索；适应度低时增加交叉/变异率以扩大搜索范围。

---

### G. PSO 算法推导（Rout & Das 2012）

#### G.1 标准 PSO

每个粒子 i 有位置 w_i 和速度 v_i。更新规则：

```
v_i(n+1) = ω·v_i(n) + c₁·r₁·(pbest_i - w_i(n)) + c₂·r₂·(gbest - w_i(n))
w_i(n+1) = w_i(n) + v_i(n+1)
```

其中 pbest_i 是粒子 i 的历史最优，gbest 是全局最优。

#### G.2 条件重初始化 PSO（CRPSO）

当种群停滞（gbest 连续 K 代不改进）时，重初始化除 gbest 外的所有粒子：

```
w_i(0) = gbest + δ·randn(),  i = 2, ..., P
w₁ = gbest  （保持最优解）
```

其中 δ 是重初始化范围，随迭代次数衰减。

---

### H. Careful Control 推导（Lopes & Gerald 2022）

#### H.1 Dual Control 框架

在 unknown plant S(z) 下同时实现控制（exploitation）和辨识（exploration）。定义代价函数：

```
J = E[e²(n)] + λ · E[||s - ŝ||²]
```

其中 λ 权衡控制性能和辨识精度。

#### H.2 Careful Least Squares

用最小二乘同时估计 W 和 S。在时刻 n，收集数据：

```
e(k) = d(k) + wᵀ·x̃(k) + ε(k),  k = 1, ..., n
```

其中 x̃(k) = x(k) * s。由于 s 未知，用泰勒展开：

```
x̃(k) ≈ x(k) * ŝ(k) + (s - ŝ) * x(k)
```

代入误差方程：

```
e(k) ≈ d(k) + wᵀ[x(k)*ŝ(k)] + wᵀ[(s-ŝ)*x(k)] + ε(k)
```

用交替最小二乘迭代更新 w 和 s：

```
Step 1 (fix s):  w = argmin Σ[e(k) - wᵀ(x(k)*ŝ)]²
Step 2 (fix w):  s = argmin Σ[e(k) - d(k) - wᵀ(x(k)*s)]²
```

Step 2 等价于系统辨识问题，可用标准 LMS/RLS 求解。

---

### I. 建模误差对 FXLMS 的影响（Lopes & Piedade 2004）

#### I.1 误差方程

设 Ŝ(z) = S(z) + ΔS(z)，其中 ΔS(z) 是建模误差。FXLMS 更新为：

```
w(n+1) = w(n) + μ · e(n) · x̂_f(n)
```

其中 x̂_f(n) = [Ŝ(z)] * x(n) = [S(z) + ΔS(z)] * x(n)。

#### I.2 稳定性条件

慢自适应近似下，收敛条件为：

```
|∠[S(e^(jω)) · Ŝ*(e^(jω))]| < π/2,  ∀ω
```

即 S(e^(jω)) 和 Ŝ(e^(jω)) 的相位差必须 < 90°。

#### I.3 稳态性能

收敛后的残余误差功率：

```
E[e²(∞)] = σ_d² + μ·L·σ_x²·σ_v² / [2 - μ·L·σ_x²] · ||ΔS||²
```

其中第一项是最优性能，第二项是建模误差引起的性能退化。当 ΔS → 0 时，退化项消失。

---

### J. 元学习初始化推导（Yang & Rao 2026）

#### J.1 问题表述

寻找一组初始化参数 θ* = (w₀, ŝ₀)，使得面对新的次级通道 S'(z) 时，只需少量梯度步骤即可收敛：

```
θ* = argmin_θ E_{S_i~p(S)} [L_i(θ - α·∇_θ L_i(θ))]
```

其中 L_i 是在第 i 个次级通道 S_i 下的 ANC 损失函数，p(S) 是次级通道分布。

#### J.2 MAML 应用于 ANC

用 Model-Agnostic Meta-Learning (MAML) 框架：

```
Outer loop (meta-update):
  θ ← θ - β · Σ_i ∇_θ L_i(θ_i')
  where θ_i' = θ - α · ∇_θ L_i(θ)

Inner loop (adaptation):
  For new S'(z):
    w₀, ŝ₀ = θ*
    w_{k+1} = w_k - α_w · ∇_w L(w_k, ŝ_k)
    ŝ_{k+1} = ŝ_k - α_s · ∇_s L(w_k, ŝ_k)
```

**优势**：相比随机初始化，元学习初始化的收敛速度提升 3-5 倍（Yang & Rao 2026 实验结果）。
