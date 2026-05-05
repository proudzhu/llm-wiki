---
type: source
created: 2026-04-12
updated: 2026-04-12
sources:
  control in active noise control systems.md
tags:
- active-noise-control
- model-predictive-control
- real-time-implementation
- state-space
aliases:
- 'Liang 2026: Delayed MPC for ANC Paper Reading Note'
---

# 论文精读 | Real-time Implementation of Delayed MPC in ANC Systems

**作者**: Chao Liang, Francesco Ripamonti, Hamid Reza Karimi, Marek Pawełczyk
**机构**: Politecnico di Milano, Silesian University of Technology
**发表**: Journal of Sound and Vibration, Vol. 635, 119800, 2026
**DOI**: [10.1016/j.jsv.2026.119800](https://doi.org/10.1016/j.jsv.2026.119800)
**📎 Zotero**: [zotero://select/items/0_J5CZZBZ2](zotero://select/items/0_J5CZZBZ2)

---

## 一、问题定义：MPC 为什么在 ANC 中一直没用起来？

MPC（模型预测控制）在主动振动控制中已经广泛应用，但在 **主动噪声控制（ANC）** 中却几乎没人用。原因有两个致命问题：

### 1. 因果性违反：需要未来扰动信息

MPC 需要在每个时刻 $k$ 预测未来 $f$ 步的系统输出，然后优化控制序列。但在 ANC 中，**主路径的扰动 $u_p$ 是未知的未来信号**。

现有方案要么用卡尔曼预测器 [10]，要么用 AR/ARX 模型 [11-13] 来估计未来扰动。但这些预测模型**只对周期性/确定性噪声有效**，对宽带随机噪声完全不行。

### 2. 计算复杂度太高

传统 MPC 需要在每个采样时刻求解一个**约束优化问题**（通常是二次规划 QP），计算量远超 ANC 系统的高采样率要求（通常 4kHz+）。

替代方案：
- **显式 MPC** [14]：离线预计算控制律查找表 → 内存需求随控制变量数指数增长
- **内点法/有效集法** [15-16]：收敛快但计算量仍然很大

---

## 二、核心洞察：主路径延迟 = 免费的因果预览

这篇论文的关键洞察非常简洁但深刻：

> **ANC 系统的主路径天然存在传播延迟 $N_{dp}$。这个延迟意味着：在扰动到达误差麦克风之前，我们已经有 $N_{dp}$ 拍的参考信号可用。**

```
参考信号 u_p(k) → [主路径 P, 延迟 N_dp 拍] → 扰动 d(k+N_dp) → 误差麦克风
控制信号 u_s(k) → [次级路径 S, 延迟 N_ds 拍] → 抗噪声 a(k+N_ds) → 误差麦克风
```

**关键条件**：只要预测视界 $f$ 小于主/次路径的**延迟差** $N_d = N_{dp} - N_{ds}$，未来的主路径输入序列 ${\bf u}'_p$ 就全部是**过去已知的**：

```
f < N_d = N_{dp} - N_{ds}  →  因果性保证
```

这意味着：**不需要任何外部预测模型**——延迟本身就提供了因果的扰动预览。

---

## 三、系统建模

### 3.1 联合状态空间模型

主路径和次级路径分别建模为离散时间状态空间系统：

**主路径**：
$$
\begin{cases}
{\bf x}_{k+1}^p = {\bf A}_p {\bf x}_k^p + {\bf B}_p u_k^p \\
y_k^p = {\bf C}_p {\bf x}_k^p + {\bf D}_p u_k^p
\end{cases}
$$

**次级路径**：
$$
\begin{cases}
{\bf x}_{k+1}^s = {\bf A}_s {\bf x}_k^s + {\bf B}_s u_k^s \\
y_k^s = {\bf C}_s {\bf x}_k^s + {\bf D}_s u_k^s
\end{cases}
$$

**联合系统**（误差信号 $y_k = y_k^p - y_k^s$）：
$$
\begin{cases}
{\bf x}_{k+1} = \begin{bmatrix} {\bf A}_p & 0 \\ 0 & {\bf A}_s \end{bmatrix} {\bf x}_k + \begin{bmatrix} {\bf B}_p \\ 0 \end{bmatrix} u_k^p + \begin{bmatrix} 0 \\ {\bf B}_s \end{bmatrix} u_k^s \\
y_k = \begin{bmatrix} {\bf C}_p & -{\bf C}_s \end{bmatrix} {\bf x}_k + {\bf D}_p u_k^p - {\bf D}_s u_k^s
\end{cases}
$$

其中增广状态向量 ${\bf x}_k = [{\bf x}_k^p; {\bf x}_k^s]$。

### 3.2 延迟嵌入

实际测量的传递函数包含延迟：

$$
H_{\text{meas}}^p(z) = H_{\text{delayless}}^p(z) \cdot z^{-N_{dp}}, \quad
H_{\text{meas}}^s(z) = H_{\text{delayless}}^s(z) \cdot z^{-N_{ds}}
$$

**建模策略**：只在主路径中引入延迟（设 $N_{ds} = 0$），最大化可用预览长度：

```
N_d = N_{dp} - N_{ds} = N_{dp}
```

实验中：$N_{dp} = 10$ 拍（$T_d = 2.5$ ms @ 4kHz），$N_{ds} = 0$。

### 3.3 系统辨识

- 方法：向量拟合（Vector Fitting）[18]
- 频率范围：100–800 Hz
- 模型阶数：主/次路径各 **15 阶**（低于 15 阶无法准确复现共振峰和相位特性）
- 传递函数形式：
  $$
  G(z) = \frac{b_0 + b_1 z^{-1} + \cdots + b_q z^{-q}}{1 + a_1 z^{-1} + \cdots + a_r z^{-r}}, \quad q = r = 15
  $$

---

## 四、Delayed MPC 算法

### 4.1 预测方程

在预测视界 $f$ 上，未来的误差序列可表示为：

$$
{\bf y} = {\bf c}' - {\bf M}_{s,dl} {\bf u}'_s
$$

其中：
- ${\bf c}' = {\bf O}_{dl} {\bf x}'_k + {\bf M}_{p,dl} {\bf u}'_p$：当前状态 + 未来主路径输入的已知贡献
- ${\bf M}_{s,dl}$：次级路径输入预测矩阵
- ${\bf u}'_s$：待优化的次级控制序列

### 4.2 代价函数与解析解

MPC 代价函数：
$$
J({\bf u}'_s) = {\bf y}^T {\bf Q} {\bf y} + ({\bf u}'_s)^T {\bf R} {\bf u}'_s
$$

令 $\partial J / \partial {\bf u}'_s = 0$，得到**闭式最优解**：

$$
{\bf u}'_s^* = {\bf H}'^{-1} {\bf g}'
$$

其中：
$$
{\bf H}' = {\bf M}_{s,dl}^T {\bf Q} {\bf M}_{s,dl} + {\bf R}, \quad
{\bf g}' = {\bf M}_{s,dl}^T {\bf Q} {\bf c}'
$$

**关键优势**：这个解是**解析的、非迭代的**。不需要在线求解 QP——只需要矩阵乘法和一次线性系统求解（${\bf H}'$ 可离线预计算逆矩阵）。

### 4.3 饱和处理

虽然是无约束 MPC，但实际控制输入有上下限：

$$
u_{k}^{s,\text{sat}} = \begin{cases}
u_{\max}^s, & u_k^s > u_{\max}^s \\
u_{\min}^s, & u_k^s < u_{\min}^s \\
u_k^s, & \text{otherwise}
\end{cases}
$$

当无约束最优解大部分时间在允许范围内时，饱和近似等价于约束 MPC 的解。

### 4.4 完整算法（Algorithm 2）

**离线准备阶段**：
1. 定义状态空间矩阵：${\bf A}_{dl}^p, {\bf B}_{dl}^p, {\bf C}_{dl}^p, {\bf D}_{dl}^p, {\bf A}^s, {\bf B}^s, {\bf C}^s, {\bf D}^s$
2. 指定权重矩阵 ${\bf Q}, {\bf R}$
3. 设置预测视界 $f < N_d$，$N_{ds} = 0$
4. 计算预测矩阵 ${\bf O}_{dl}, {\bf M}_{dl}^p, {\bf M}_{dl}^s$

**在线优化循环**（每个采样时刻 $k$）：
1. 获取过去扰动序列 ${\bf u}'_p$（从 $k-N_{dp}$ 到 $k+f-N_{dp}$）
2. 计算 ${\bf c}' = {\bf O}_{dl} {\bf x}'_k + {\bf M}_{dl}^p {\bf u}'_p$
3. 计算最优序列 ${\bf u}'_s^* = {\bf H}'^{-1} {\bf g}'$
4. 取第一个元素 $u_k^s$，施加饱和限制
5. 应用控制输入，更新状态

**每个采样时刻只取最优序列的第一个元素 $u_k^s$ 应用到系统**——这就是 MPC 的"滚动时域"策略。

---

## 五、计算复杂度分析

| 算法 | 乘除法 | 加减法 | 复杂度 |
|------|--------|--------|--------|
| **FxNLMS** | $3K + L + 2$ | $2K + L - 1$ | $O(3K + L)$ |
| **（Delayed）MPC** | $f(2f+m+n+1) + m(m+1) + n(n+1)$ | $f(2f+m+n-2) + m(m-1) + n(n-1) + 2$ | $O(2f^2 + f(m+n) + m^2 + n^2)$ |

本文参数：$K=64$（自适应滤波器长度），$L=512$（次级路径估计长度），$f=9$（预测视界），$m=n=15$（状态维数）。

**实际计算量**：
- FxNLMS：**~706 次乘法/样本**
- Delayed MPC：**~921 次乘法/样本**

**仅增加约 30%**——在现代 DSP 上完全可以实时运行（4kHz 采样率下每样本只有 250μs 处理时间）。

---

## 六、实验结果

### 6.1 实验设置

- 测试平台：Kundt's tube（驻波管）
- 控制器：MATLAB/Simulink + Speedgoat 实时目标机
- 采样率：4kHz
- 权重矩阵：${\bf Q} = \alpha {\bf I}$（$\alpha=1$），${\bf R} = \beta {\bf I}$（$\beta=0.001$）
- 预测视界：$f = 9$
- 饱和限制：$u_{\max}^s = 1, u_{\min}^s = -1$
- 测试噪声：交通噪声、飞机噪声、人声、白噪声、冲击敲击噪声

### 6.2 降噪性能对比

| 算法 | 交通 | 飞机 | 人声 | 冲击敲击 | 白噪声 |
|------|------|------|------|---------|--------|
| 离线 FIR（$P(\omega)/S(\omega)$） | 4.87 | 4.13 | 4.79 | 4.61 | 4.34 |
| **FxNLMS** | 11.24 | 7.66 | 15.36 | — | 6.62 |
| **MPC** | **16.90** | **16.31** | **18.61** | **15.50** | **7.94** |
| **Delayed MPC** | **15.77** | **15.39** | **17.82** | **13.69** | **7.22** |

**关键发现**：
1. MPC 和 Delayed MPC 在所有噪声类型下均**显著优于** FxNLMS（提升 2.5–7.7 dB）
2. **冲击敲击噪声**：FxNLMS 完全无法抑制，MPC/Delayed MPC 仍能达到 13–15 dB 降噪
3. **收敛时间**：MPC 是**瞬时收敛**的（解析解），FxNLMS 需要迭代适应
4. MPC vs Delayed MPC：性能接近，Delayed MPC 在人声下略优

### 6.3 饱和影响

当参考信号幅度增大到 $A_{\max} = 0.8$ 时：

| 算法 | 交通 | 飞机 | 人声 | 冲击敲击 | 白噪声 |
|------|------|------|------|---------|--------|
| FxNLMS | 11.33 | — | 12.67 | — | 7.27 |
| MPC | 16.03 | 11.74 | 16.99 | 6.06 | 12.93 |
| Delayed MPC | 12.52 | 11.39 | 16.17 | 4.44 | 11.09 |

饱和会显著降低 MPC 性能（尤其是飞机和冲击噪声），但白噪声几乎不受影响（频谱均匀、峰值低）。

**权重矩阵 ${\bf R}$ 的调节**：增大 $\beta$ 可以降低控制幅值、缓解饱和，但会过度惩罚控制努力、降低降噪效果。$\beta = 0.001$ 是一个合理的折中。

---

## 七、与 FxNLMS 的系统对比

| 维度 | FxNLMS | Delayed MPC |
|------|--------|-------------|
| **原理** | 梯度下降自适应 | 滚动时域优化 |
| **收敛** | 迭代适应（需要时间） | **瞬时**（解析解） |
| **未来信息** | 不需要 | **主路径延迟提供因果预览** |
| **噪声类型限制** | 无 | 无（不需要预测模型） |
| **计算复杂度** | $O(3K + L)$ ≈ 706 | $O(2f^2 + f(m+n) + m^2 + n^2)$ ≈ 921 |
| **脉冲噪声鲁棒性** | 差（无法抑制冲击噪声） | **好**（13–15 dB 降噪） |
| **饱和敏感性** | 中等 | 高（但可通过 ${\bf R}$ 调节） |
| **模型依赖** | 仅需次级路径估计 | 需主+次路径状态空间模型 |

---

## 八、Q&A

**Q1: 为什么 MPC 以前在 ANC 中没用起来？**

两个核心障碍：
1. **因果性问题**：MPC 需要未来扰动信息，但 ANC 中扰动是未知的。现有方案用 AR/ARX 预测，但只对周期性噪声有效。
2. **计算量问题**：传统 MPC 需要在线求解 QP，远超 ANC 的高采样率要求。

本文的突破：**主路径延迟本身就是免费的因果预览**（不需要预测模型）+ **解析闭式解**（不需要在线 QP）。

**Q2: Delayed MPC 和普通 MPC 有什么区别？**

普通 MPC 需要预测未来主路径输入 ${\bf u}_p$（从 $k$ 到 $k+f$），这在实际中不可知。

Delayed MPC 利用主路径延迟，将 ${\bf u}'_p$ 的定义从 $[k-N_{dp}, k+f-N_{dp}]$ 偏移——只要 $f < N_{dp}$，整个序列都是**过去已知的**。

**Q3: 为什么 MPC 对冲击噪声比 FxNLMS 好得多？**

FxNLMS 是梯度下降算法，大误差会导致大步长更新，可能发散。实验表明 FxNLMS 对冲击敲击噪声完全无法抑制。

MPC 的优化目标是最小化整个预测视界上的误差平方和，对单个大误差脉冲的响应更平滑、更鲁棒。加上饱和限制，可以有效抑制冲击。

**Q4: 这个方法的局限是什么？**

1. **模型依赖**：需要主+次路径的准确状态空间模型（离线辨识）。时变环境中模型可能过时。
2. **饱和敏感**：大幅度信号下控制输入容易饱和，降噪性能显著下降。
3. **频率范围限制**：实验仅在 100–800 Hz 验证，高频段因相位误差性能下降。
4. **未来工作方向**：在线自适应 MPC（实时更新主/次路径模型）——论文结论部分明确提到这是下一步。

---

## Related Concepts

- [[../concepts/model-predictive-control|Model Predictive Control]] — 滚动时域优化框架
- [[../concepts/active-noise-control|Active Noise Control]] — 应用场景
- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — 对比基线算法
- [[../concepts/state-space-model|State-Space Model]] — 系统建模方法
- [[../concepts/system-identification|System Identification]] — 向量拟合获取状态空间模型

## Related Entities

- [[../entities/chao-liang|Chao Liang]] — 第一作者，Politecnico di Milano
- [[../entities/francesco-ripamonti|Francesco Ripamonti]] — 共同作者，Politecnico di Milano
- [[../entities/marek-pawelczyk|Marek Pawełczyk]] — 共同作者，Silesian University of Technology，ANC 研究者

## Related Synthesis
