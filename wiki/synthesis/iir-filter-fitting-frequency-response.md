---
type: synthesis
created: 2026-04-12
updated: 2026-04-29
sources:
- zotero://select/items/0_TAXBEPC7
- zotero://select/items/0_5SFJK2MD
- zotero://select/items/0_2LKM9QRI
tags:
- frequency-response
- iir-fitting
- model-reduction
- state-space
- system-identification
- vector-fitting
- parameterized-modeling
- curve-fitting
- optimization
aliases:
- IIR 滤波器拟合频响曲线
- Vector Fitting
- 参数化 IIR 曲线拟合
---

# IIR 滤波器拟合频响曲线：从测量到状态空间模型

> 跨来源综合：Liang et al. (2026) MPC 中的向量拟合、Lesniewski 状态空间与卡尔曼滤波、Vaudrey & Baumann (2003) 反馈稳定性对模型精度的要求、以及 Cioffi & Kailath (1984) 快速最小二乘。

---

## 问题定义

在 ANC 系统设计中，经常需要从**测量的频响数据**（幅度和相位 vs 频率）拟合出一个 **IIR 滤波器传递函数**：

$$H(z) = \frac{B(z)}{A(z)} = \frac{b_0 + b_1 z^{-1} + \cdots + b_q z^{-q}}{1 + a_1 z^{-1} + \cdots + a_p z^{-p}}$$

**为什么要 IIR 而非 FIR**：
- **参数量**：一个 15 阶 IIR 可以拟合一个需要 512 阶 FIR 才能描述的共振系统
- **物理意义**：极点位置对应共振频率和阻尼比
- **MPC 需求**：模型预测控制需要状态空间模型，而 IIR 可以自然转换为状态空间

**典型应用场景**：
1. **次级路径建模**（$\hat{S}(z)$）：测量扬声器→误差麦克风的频响，拟合为 IIR
2. **主路径建模**（$\hat{P}(z)$）：测量参考麦克风→误差麦克风的频响
3. **MPC 预测模型**：Liang (2026) 用 15 阶 IIR 建模 ANC 系统

---

## 方法 1：向量拟合（Vector Fitting）

### Liang et al. (2026) 实践

Liang et al. 在 MPC for ANC 中使用**向量拟合** [18] 从测量数据识别系统模型：

| 参数 | 值 |
|------|-----|
| 频率范围 | 100–800 Hz |
| 模型阶数 | 15 阶（分子 = 分母 = 15） |
| 传递函数 | $G(z) = \frac{b_0 + b_1 z^{-1} + \cdots + b_{15} z^{-15}}{1 + a_1 z^{-1} + \cdots + a_{15} z^{-15}}$ |
| 最低阶数要求 | < 15 阶无法准确复现共振峰和相位特性 |

**关键发现**：模型阶数 < 15 时，拟合误差在共振频率处显著增大，导致 MPC 性能下降 3-5 dB。

### 向量拟合算法

向量拟合 (Gustavsen & Semlyen, 1999) 的核心思想：通过**迭代极点 relocating** 来改善初始极点估计。

**算法流程**：

```
输入: {ω_k, H_k} 频响数据点 (k=1,...,K)
输出: IIR 传递函数 H(s) 或 H(z)

1. 初始化极点 {p_i^(0)}（线性或对数分布在频率范围内）
2. 迭代 n = 1, 2, ...:
   a. 求解最小二乘问题:
      min || σ(s)H(s) - θ(s) ||²
      其中 σ(s) = ∏(s - p̃_i) 是缩放函数
            θ(s) = ∑ c̃_i/(s - p_i^(n-1)) + d + s·h
   
   b. 找到 σ(s) 的零点 → 新极点 {p_i^(n)}
   
   c. 如果极点收敛（变化 < 阈值），退出迭代
   
3. 已知最终极点 {p_i}，求解留数 {c_i} 和常数项 d, h
4. 转换为 IIR 形式（双线性变换 s → z）
```

**数学细节**：

在第 $n$ 次迭代中，求解以下 overdetermined 线性最小二乘问题：

$$\min_{c_i, d, h, \tilde{c}_i} \sum_{k=1}^{K} \left| H(j\omega_k) - \frac{\sum_{i=1}^{N} \frac{\tilde{c}_i}{j\omega_k - p_i^{(n-1)}} + d + j\omega_k h}{1 + \sum_{i=1}^{N} \frac{\tilde{c}_i}{j\omega_k - p_i^{(n-1)}}} \right|^2$$

这可以写为矩阵方程 $Ax = b$ 并通过 QR 分解或 SVD 求解。

### 极点的稳定性处理

向量拟合可能产生**不稳定极点**（右半平面或单位圆外）。处理方法：

1. **镜像翻转**：将不稳定极点翻转到稳定侧
   $$p_i^{\text{stable}} = \begin{cases} p_i & \text{if } |p_i| < 1 \\ 1/p_i^* & \text{if } |p_i| \geq 1 \end{cases}$$

2. **固定极点重新拟合**：固定极点为稳定值，只优化留数

3. **加权最小二乘**：在稳定性敏感频率区域增加权重

---

## 方法 2：最小二乘频域辨识（Cioffi & Kailath 1984）

### 方程误差法

给定频响数据 $\{H(e^{j\omega_k})\}_{k=1}^K$，最小化方程误差：

$$\min_{a,b} \sum_{k=1}^{K} |A(e^{j\omega_k})H(e^{j\omega_k}) - B(e^{j\omega_k})|^2$$

其中 $A(z) = 1 + a_1 z^{-1} + \cdots + a_p z^{-p}$，$B(z) = b_0 + b_1 z^{-1} + \cdots + b_q z^{-q}$。

**矩阵形式**：

$$\begin{bmatrix}
H(e^{j\omega_1})e^{-j\omega_1} & \cdots & H(e^{j\omega_1})e^{-jp\omega_1} & -1 & -e^{-j\omega_1} & \cdots & -e^{-jq\omega_1} \\
\vdots & \ddots & \vdots & \vdots & \vdots & \ddots & \vdots \\
H(e^{j\omega_K})e^{-j\omega_K} & \cdots & H(e^{j\omega_K})e^{-jp\omega_K} & -1 & -e^{-j\omega_K} & \cdots & -e^{-jq\omega_K}
\end{bmatrix}
\begin{bmatrix}
a_1 \\ \vdots \\ a_p \\ b_0 \\ \vdots \\ b_q
\end{bmatrix}
=
\begin{bmatrix}
-H(e^{j\omega_1}) \\ \vdots \\ -H(e^{j\omega_K})
\end{bmatrix}$$

这可以通过**快速递归最小二乘**（Cioffi & Kailath 1984）在 $O(K \cdot (p+q))$ 时间内求解。

**局限性**：方程误差法对噪声敏感，因为误差被 $A(e^{j\omega_k})$ 加权。当频响测量包含噪声时，拟合结果可能有偏。

---

## 方法 3：输出误差法（迭代优化）

### Levy 方法

最小化输出误差（真正的频响误差）：

$$\min_{a,b} \sum_{k=1}^{K} \left| H(e^{j\omega_k}) - \frac{B(e^{j\omega_k})}{A(e^{j\omega_k})} \right|^2$$

这是**非线性**最小二乘问题，需要迭代求解：

```
1. 用方程误差法初始化 {a_i}, {b_i}
2. 迭代直到收敛:
   a. 计算当前输出误差: e_k = H_k - B_k/A_k
   b. 线性化: B_k/A_k ≈ B_k/A_k^{(old)} + ∂(B/A)/∂a · Δa + ∂(B/A)/∂b · Δb
   c. 求解线性最小二乘: min ||e - J·[Δa; Δb]||²
   d. 更新参数: a += Δa, b += Δb
   e. 检查稳定性: 如果有不稳定极点，翻转并重新拟合
```

**优势**：输出误差法对测量噪声更鲁棒，拟合精度更高。

**劣势**：计算量比方程误差法大 5-10 倍（需要迭代）。

---

## 方法 4：状态空间辨识（Lesniewski）

### 从频响到状态空间

Lesniewski 的状态空间笔记提供了从频响数据直接识别状态空间模型的方法：

$$x(n+1) = A x(n) + B u(n)$$
$$y(n) = C x(n) + D u(n)$$

传递函数：
$$H(z) = C(zI - A)^{-1}B + D$$

**辨识步骤**：

1. **Hankel 矩阵构建**：从频响的逆 FFT 得到脉冲响应 $h[n]$
2. **SVD 分解**：$H = U\Sigma V^T$
3. **模型降阶**：保留前 $r$ 个奇异值
4. **状态空间提取**：
   $$A = \Sigma^{-1/2} U^T H_{\text{shifted}} V \Sigma^{-1/2}$$
   $$B = \Sigma^{1/2} V^T e_1, \quad C = e_1^T U \Sigma^{1/2}$$

**与向量拟合的关系**：向量拟合得到的是传递函数（极点-留数形式），可以通过**伴随形式**（companion form）转换为状态空间。两者在数学上是等价的，但向量拟合更适合高阶系统，而 Hankel-SVD 更适合低阶近似。

---

## 方法 5：参数化 IIR 拟合

### 5.1 二阶节（SOS / Biquad）参数化

将 IIR 传递函数分解为级联的二阶节：

$$H(z) = G \prod_{k=1}^{K} \frac{1 + b_{1,k} z^{-1} + b_{2,k} z^{-2}}{1 + a_{1,k} z^{-1} + a_{2,k} z^{-2}}$$

每个二阶节可以用**物理参数**直接参数化：

$$H_k(z) = g_k \cdot \frac{1 - 2\cos(\omega_{z,k}) z^{-1} + z^{-2}}{1 - 2r_{p,k}\cos(\omega_{p,k}) z^{-1} + r_{p,k}^2 z^{-2}}$$

其中：
- $\omega_{p,k} = 2\pi f_{p,k} / f_s$：极点角频率（共振频率）
- $r_{p,k} \in (0, 1)$：极点半径（决定 Q 值/带宽）
- $\omega_{z,k}$：零点角频率（反共振频率）
- $g_k$：该节增益

**Q 值与极点半径的关系**：

$$Q_k \approx \frac{1}{2(1 - r_{p,k})} \quad \text{（当 } r_{p,k} \to 1 \text{ 时）}$$

| 极点半径 $r_p$ | Q 值 | 带宽 | 适用场景 |
|---------------|------|------|---------|
| 0.70 | 1.7 | 宽 | 低 Q 共振 |
| 0.85 | 3.3 | 中 | 中等共振 |
| 0.95 | 10.0 | 窄 | 尖锐共振 |
| 0.99 | 50.0 | 极窄 | 高频共振峰 |

**优势**：
- **物理可解释**：每个参数对应明确的物理量（频率、Q、增益）
- **稳定性保证**：只需约束 $0 < r_{p,k} < 1$
- **模块化**：可以独立调整每个二阶节而不影响其他节
- **数值稳定**：级联 SOS 比直接形式系数更鲁棒

### 5.2 峰值/谷值滤波器参数化

对于 ANC 中的次级路径建模，频响通常由一系列**共振峰**和**反共振谷**组成。可以使用峰值/谷值滤波器的叠加来参数化：

**峰值滤波器**（增强某个频率）：

$$H_{\text{peak}}(z) = 1 + \frac{g \cdot (1 - r^2) \cdot 2\cos(\omega_0) z^{-1}}{1 - 2r\cos(\omega_0) z^{-1} + r^2 z^{-2}}$$

**谷值滤波器**（衰减某个频率）：

$$H_{\text{notch}}(z) = 1 - \frac{g \cdot (1 - r^2) \cdot 2\cos(\omega_0) z^{-1}}{1 - 2r\cos(\omega_0) z^{-1} + r^2 z^{-2}}$$

整体传递函数：

$$H(z) = H_0 \cdot \prod_{k=1}^{N_{\text{peak}}} H_{\text{peak},k}(z) \cdot \prod_{m=1}^{N_{\text{notch}}} H_{\text{notch},m}(z)$$

**参数向量**：

$$\theta = \left[ g_0, \{g_k, \omega_k, r_k, \text{type}_k\}_{k=1}^{N} \right]$$

其中 $\text{type}_k \in \{\text{peak}, \text{notch}\}$。

### 5.3 梯度优化拟合

给定频响数据 $\{H_{\text{meas}}(e^{j\omega_m})\}_{m=1}^M$，直接优化参数化 IIR 的参数：

$$\min_{\theta} \sum_{m=1}^{M} W(\omega_m) \left| H_{\text{meas}}(e^{j\omega_m}) - H(e^{j\omega_m}; \theta) \right|^2$$

其中 $W(\omega)$ 是频率权重函数。

**梯度计算**（以峰值滤波器为例）：

$$\frac{\partial H}{\partial g} = \frac{(1 - r^2) \cdot 2\cos(\omega_0) z^{-1}}{1 - 2r\cos(\omega_0) z^{-1} + r^2 z^{-2}}$$

$$\frac{\partial H}{\partial r} = \frac{g \cdot 2r \cdot [2\cos(\omega_0) z^{-1} - z^{-2}]}{[1 - 2r\cos(\omega_0) z^{-1} + r^2 z^{-2}]^2}$$

$$\frac{\partial H}{\partial \omega_0} = \frac{g \cdot (1 - r^2) \cdot 2\sin(\omega_0) z^{-1} \cdot [1 + r^2 z^{-2}]}{[1 - 2r\cos(\omega_0) z^{-1} + r^2 z^{-2}]^2}$$

**优化算法选择**：

| 算法 | 适用场景 | 优点 | 缺点 |
|------|---------|------|------|
| **Levenberg-Marquardt** | 中小规模（< 50 参数） | 收敛快 | 需要 Jacobian |
| **L-BFGS** | 大规模（> 50 参数） | 内存高效 | 需要梯度 |
| **Adam** | 非常大规模 / 有噪声 | 鲁棒 | 收敛慢 |

**参数约束处理**：

$$r_k = \frac{1}{1 + \exp(-\tilde{r}_k)} \in (0, 1) \quad \text{(sigmoid 映射)}$$

$$\omega_k = \frac{\pi}{1 + \exp(-\tilde{\omega}_k)} \in (0, \pi)$$

这样可以对无约束变量 $\tilde{r}_k, \tilde{\omega}_k$ 进行优化，同时保证参数在物理可行范围内。

### 5.4 频率加权策略

ANC 系统中不同频率的重要性不同。常用的加权策略：

| 加权策略 | 公式 | 适用场景 |
|---------|------|---------|
| **A 计权** | $W_A(f)$ 标准曲线 | 人耳感知 |
| **1/f 加权** | $W(f) = 1/f$ | 低频优先 |
| **共振峰加权** | $W(f) = |H_{\text{meas}}(f)|$ | 共振区域优先 |
| **均匀加权** | $W(f) = 1$ | 所有频率平等 |

**ANC 特殊加权**：考虑次级路径建模误差对 ANC 性能的影响：

$$W_{\text{ANC}}(f) = \frac{1}{|S(e^{j2\pi f/f_s})|^2 + \epsilon}$$

这使得在次级路径增益较小的频率区域（通常是高频共振谷）给予更大权重，因为这些区域的相对误差对 ANC 稳定性影响更大。

### 5.5 实际应用示例：15 阶次级路径拟合

以下是一个典型的 ANC 耳机次级路径参数化拟合结果（对应 Liang 2026 的 15 阶模型）：

| 节 | 类型 | 频率 (Hz) | Q 值 | 增益 (dB) | 极点半径 |
|----|------|----------|------|----------|---------|
| 1 | peak | 120 | 8.0 | +12 | 0.94 |
| 2 | peak | 250 | 5.5 | +8 | 0.91 |
| 3 | notch | 350 | 3.0 | -6 | 0.85 |
| 4 | peak | 450 | 12.0 | +15 | 0.96 |
| 5 | peak | 600 | 6.0 | +10 | 0.92 |
| 6 | notch | 700 | 4.0 | -8 | 0.88 |
| 7 | peak | 780 | 10.0 | +13 | 0.95 |

**增益** $G = 0.85$（整体缩放）

**拟合误差**：
- 幅度 RMS 误差：0.8 dB
- 相位 RMS 误差：12°
- 最大相位误差：28°（< 90° 稳定性极限）

---

## IIR 拟合在 ANC 中的关键应用

### 1. 次级路径建模 $\hat{S}(z)$

**Liang (2026) 的经验**：

| 模型阶数 | NR 损失 | 计算量 | 稳定性 |
|---------|--------|--------|--------|
| 5 阶 | > 8 dB | 低 | 稳定但不准确 |
| 10 阶 | 3-5 dB | 中 | 相位误差大 |
| **15 阶** | **< 1 dB** | **中** | **准确且稳定** |
| 25 阶 | < 0.5 dB | 高 | 过拟合风险 |

**设计规则**：模型阶数至少应等于系统中主要共振模式的数量 × 2。

### 2. 反馈 ANC 的稳定性约束

Vaudrey & Baumann (2003) 指出，自适应反馈 ANC 的稳定性要求：

$$\angle \hat{S}(e^{j\omega}) - \angle S(e^{j\omega}) < 90^\circ$$

这意味着 IIR 拟合的**相位误差**必须控制在 90° 以内。对于 15 阶模型在 100-800 Hz 范围内，典型相位误差为 10-30°，远小于 90° 的极限。

### 3. MPC 预测模型

Liang (2026) 将 15 阶 IIR 转换为 15 维状态空间模型：

$$A \in \mathbb{R}^{15 \times 15}, \quad B \in \mathbb{R}^{15 \times 1}, \quad C \in \mathbb{R}^{1 \times 15}, \quad D \in \mathbb{R}$$

MPC 的计算复杂度为 $O(N_{state}^2) = O(225)$ 每控制步。

---

## 算法比较

| 方法 | 精度 | 计算量 | 稳定性保证 | 适用阶数 |
|------|------|--------|-----------|---------|
| **向量拟合** | ★★★★★ | 中（迭代） | 需要后处理 | 5-50 |
| **方程误差最小二乘** | ★★★☆☆ | 低（直接求解） | 无 | 5-20 |
| **输出误差迭代** | ★★★★☆ | 高（迭代） | 需要后处理 | 5-30 |
| **Hankel-SVD** | ★★★☆☆ | 中（SVD） | 自动稳定 | 3-15 |

---

## 实用设计流程

```
1. 测量频响 H(ω)
   ├── 正弦扫频 → 高信噪比
   ├── 白噪声激励 → 快速但噪声大
   └── MLS（最大长度序列）→ 最佳信噪比

2. 选择拟合方法
   ├── 快速原型 → 方程误差最小二乘
   ├── 高精度需求 → 向量拟合
   └── 低阶近似 → Hankel-SVD

3. 确定模型阶数
   ├── 观察奇异值衰减（Hankel-SVD）
   ├── 观察拟合误差随阶数变化
   └── 在 ANC 系统中验证 NR

4. 稳定性检查
   ├── 检查极点位置（单位圆内）
   ├── 检查相位误差 < 90°
   └── 必要时进行极点翻转

5. 转换为需要的形式
   ├── 传递函数 → FxLMS 控制器
   ├── 状态空间 → MPC 预测模型
   └── 极点-留数 → 模态分析
```

---

## Q&A

**Q1: 参数化 IIR 与直接最小二乘拟合的区别？**

直接最小二乘（方程误差法）求解 $Ax=b$ 是线性的，但误差被 $A(e^{j\omega})$ 加权，导致有偏估计。参数化 IIR 使用输出误差（真正的频响误差），是非线性优化，但无偏。

**Q2: 如何选择参数化的节数？**

从奇异值衰减或峰值检测开始。经验公式：$N_{\text{sections}} \geq 2 \times N_{\text{resonances}}$。然后交叉验证：增加节数直到验证误差不再显著下降。

**Q3: 为什么不用深度学习拟合频响？**

深度学习（如 Neural ODE）可以拟合任意函数，但缺乏物理可解释性，且难以保证稳定性。参数化 IIR 在保证稳定性的同时提供了清晰的物理含义——每个节对应一个共振模式。

---

## 相关概念

- [[concepts/system-identification|System Identification]]
- [[concepts/state-space-model|State-Space Model]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/model-predictive-control|Model Predictive Control]]
- [[concepts/feedback-anc|Feedback ANC]]
- [[concepts/online-secondary-path-modeling|Online Secondary-Path Modeling]]
- [[concepts/kalman-filter|Kalman Filter]]

## Related Concepts

- [[concepts/feedback-anc|Feedback ANC]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/kalman-filter|Kalman Filter]]
- [[concepts/model-predictive-control|Model Predictive Control]]
- [[concepts/online-secondary-path-modeling|Online Secondary-Path Modeling]]
- [[concepts/state-space-model|State-Space Model]]
- [[concepts/system-identification|System Identification]]

## Related Sources
