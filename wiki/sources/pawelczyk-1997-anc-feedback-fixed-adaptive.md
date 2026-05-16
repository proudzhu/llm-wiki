---
type: source
created: 2026-04-12
updated: 2026-04-12
sources:
  Controllers.md
tags:
- adaptive-control
- feedback-anc
- filtered-x-lms-algorithm
- internal-model-control
- isvr-memorandum
- minimum-variance-control
- recursive-least-squares
- robust-control
- wiener-filter
aliases:
- 'Pawelczyk 1997: ANC Feedback Fixed/Adaptive'
---

# Active Noise Control Using Feedback. Fixed and Adaptive Controllers

**Authors**: [[entities/marek-pawelczyk|Marek Pawełczyk]], [[entities/stephen-j-elliott|Stephen J. Elliott]], [[entities/boaz-rafaely|Boaz Rafaely]]
**Published**: ISVR Technical Memorandum No. 822, December 1997
**Institution**: Institute of Sound and Vibration Research, University of Southampton
**Pages**: 74 (scanned document with OCR)

---

## 一、问题定义：无前馈参考传感器的 ANC

前馈 ANC 需要一个参考传感器来提前获取噪声信息，但在许多场景（耳机、头枕等）中，无法获取良好的前馈参考信号。反馈 ANC 仅基于**残余误差信号**进行控制。

本文系统地推导了**固定（最优）控制器**和**自适应控制器**的设计方法，覆盖了从最小方差控制（MVC）到 IMC-FXLMS 的完整理论框架。

---

## 二、系统与扰动模型

### 2.1 广义植物模型

$$
y(z) = z^{-k} \frac{B}{A} u(z) + \frac{C}{A} e(z)
$$

其中：
- $A, B, C$：$z^{-1}$ 的多项式
- $k$：离散时间延迟
- $u(i)$：控制信号
- $e(i)$：方差为 $\lambda^2$ 的白噪声
- $y(i)$：输出（降噪效果）
- $d(i) = \frac{C}{A} e(i)$：声学扰动

扰动通过 **Diophantine 方程**分解为可预测和不可预测两部分：

$$
C = F + z^{-k} G, \quad \dim F = k-1, \quad \dim G = \dim C - k
$$

---

## 三、最优（固定）控制器

### 3.1 两种控制结构

**MVC（最小方差控制）**：经典反馈结构

$$
H_{MVC} = -\frac{G}{BF}
$$

**IMC（内部模型控制）**：控制器由两部分组成 $W$ 和 $\hat{P}$（植物模型）

$$
W = -\frac{G}{FC}
$$

当模型完美时（$\hat{P} = P$），两种结构**等价**。

### 3.2 最小相位植物

对于最小相位植物（$B$ 的所有零点在单位圆内），最优控制器为：

$$
H = -\frac{G}{FB} = -\frac{A}{B} \cdot \frac{G}{C}
$$

最优降噪（仅取决于扰动成形滤波器）：

$$
J = 10 \log_{10} \left| \sum_{i=0}^{k-1} f_i^2 \right| \text{ [dB]}
$$

当 $C = 1$（扰动为白噪声）时，$J = 0$ dB——没有降噪意义。

### 3.3 非最小相位植物

当 $B$ 有单位圆外零点时，最优控制器（14）会导致闭环不稳定。两种解决方案：

**方案 1：分裂多项式 B**
$$
B = B^+ B^-
$$
其中 $B^+$ 为最小相位部分，$B^-$ 为非最小相位部分。仅补偿 $B^+$，但输出变为 ARMA 过程，方差增大。

**方案 2：代价函数中加入控制努力（WMVC）**
$$
L(i+k) = E\{y^2(i+k) + q^2 u^2(i)\}
$$

最优控制器：
$$
H_q = -\frac{L}{BF + qAC}, \quad q = \frac{A}{b_0}
$$

稳定性条件：
$$
A(B + qA) = 0
$$

**关键 trade-off**：增大 $q$ → 更好的稳定性裕度但更大的输出方差（降噪降低）。

输出和控制努力的方差严格相关：
$$
E\{y^2(i+k)\} = (q/b_0)^2 E\{u^2(i)\} + E\{[Fe(i+k)]^2\}
$$

### 3.4 信号处理方法——Wiener 滤波器

将 IMC 简化为前馈控制（当 $\hat{P} = P$ 时），代价函数为：

$$
L(i) = w^T A w + 2w^T b + c
$$

其中：
- $A$：$r(i)$ 的自相关 Toeplitz 矩阵
- $b$：$r(i)$ 与 $d(i)$ 的互相关向量
- $c = E\{d^2(i)\}$

最优 Wiener 滤波器：
$$
w_{opt} = -A^{-1} b
$$

当自相关矩阵病态时，引入 Tikhonov 正则化：
$$
w_{opt} = -(A + \beta I)^{-1} b
$$

等价于最小化 $L(i) = E\{y^2(i) + \beta w^T w\}$。

### 3.5 鲁棒控制

植物变化用乘性不确定性描述：
$$
P = P_0(1 + \Delta_u), \quad |\Delta_u(\omega)| < W_u(\omega)
$$

鲁棒稳定性条件：
$$
\|T_0 W_u\|_\infty < 1
$$

结合性能的代价函数：
$$
L = \|SD\|_2^2 + \beta^2 \|T_0 W_u\|_2^2
$$

**关键洞察**：测量噪声 $n(i)$ 的存在等价于对由噪声谱界定的植物变化的鲁棒性。

### 3.6 植物延迟对性能的影响

**关键结论**：延迟从 1 样本增加到 2 样本 → 降噪降低约 **10 dB（约 40%）**。延迟 > 7 样本时反馈控制无意义。

延迟由三部分组成：
1. **声学路径**：$T_{acoustic} = l / (c_0 T_s)$（主动耳机约 0.058 样本）
2. **模拟滤波器**：每极点贡献约 1/8 周期延迟，8 阶滤波器 × 2 = **6 样本**
3. **数据转换器 + 数字计算**：1 样本

**对于主动耳机**：总延迟约 7 样本，其中 **6 个来自模拟滤波器**。应尽可能降低滤波器阶数或提高采样率。

---

## 四、自适应控制器

### 4.1 植物的预测模型

MVC 和 IMC 控制器的参数可以通过**预测模型**直接在线识别：

$$
y(i) - R u(i-k) - S x(i-k) = (AC-1)[Fe(i)-y(i)] + Fe(i) = \varepsilon(i)
$$

控制律：
$$
u(i) = \frac{1}{r_0}[\hat{Y}(i) - \phi^T(i-k)\hat{\theta}]
$$

### 4.2 控制器识别

#### RLS（递归最小二乘）

带遗忘因子的 RLS：
$$
\hat{\theta}(i) = \hat{\theta}(i-1) + k(i)[Y(i) - \phi^T(i-k)\hat{\theta}(i-1)]
$$

$$
k(i) = \frac{P(i-1)\phi(i-k)}{\sigma + \phi^T(i-k)P(i-1)\phi(i-k)}
$$

当遗忘因子 $\sigma = 1$ 时，$\text{Trace}(P)$ 可作为收敛性评估。

**收敛条件**（Ljung 1977）：
- 扰动成形滤波器可分解为 $C = A\bar{C}$
- $\bar{C}$ 满足正实条件：$\text{Re}(1/\bar{C}) > 0$
- 植物充分激励

当 $k=1$ 时，估计是一致的。

#### LMS（最小均方）

$$
\hat{\theta}(i+1) = \hat{\theta}(i) + \mu[\hat{Y}(i) - \phi^T(i-k)\hat{\theta}(i)]\phi(i-k)
$$

### 4.3 IMC 与 FXLMS

IMC 结构下，当植物模型完美时，自适应滤波器输入为：
$$
r(i) = p^T x(i)
$$

其中 $p$ 是植物脉冲响应。由于 $p$ 未知，用模型 $\hat{p}$ 替代：

**FXLMS 更新**：
$$
W(i+1) = W(i) + \mu r(i) y(i)
$$
$$
r(i) = \hat{p}^T x(i)
$$

**收敛条件**：模型与植物的相位差 < π/2（对单频扰动）。

**收敛系数上界**：
$$
\mu < \frac{2}{N \sigma_r^2}
$$

其中 $N$ 是 FIR 滤波器长度，$\sigma_r^2$ 是滤波后参考信号的方差。

### 4.4 全自适应 IMC + FXLMS

当植物时变时，需要在线更新植物模型。Rafaely & Elliott (1996) 证明：仅存在扰动时，无法从 IMC 系统的可观测信号中提取植物响应。因此需要**外加识别信号**。

### 4.5 鲁棒自适应 IMC

通过引入泄漏因子（Leaky LMS）：
$$
W(i+1) = \xi W(i) + \mu r(i) y(i), \quad 0 < \xi < 1
$$

等价于最小化修改后的代价函数：
$$
L(i) = E\{y^2(i)\} + \frac{1-\xi}{\mu} w^T(i) w(i)
$$

---

## 五、关键对比：固定 vs 自适应

| 维度 | 固定控制器 | 自适应控制器 |
|------|-----------|-------------|
| **设计方法** | 离线优化（MVC/IMC/Wiener） | 在线识别（RLS/LMS/FXLMS） |
| **鲁棒性** | 通过 $H_\infty$ 约束保证 | 通过泄漏/归一化保证 |
| **跟踪能力** | 无法跟踪植物/扰动变化 | 可跟踪慢变非平稳性 |
| **计算复杂度** | 固定（仅滤波） | 高（在线参数更新） |
| **稳定性保证** | 设计时保证 | 需要小心选择 $\mu$ 和 $\sigma$ |
| **适用场景** | 植物参数已知且稳定 | 植物时变或扰动非平稳 |

---

## 六、与现有文献的关系

本文是后续发表期刊论文的基础：
- Pawełczyk & Elliott (1998/1999) — 相关内容发表在 Journal of Sound and Vibration
- Rafaely & Elliott (1996) — IMC 鲁棒反馈 ANC
- Elliott (1994) — 最小相位植物的反馈 ANC

---

## Related Concepts

- [[concepts/feedback-anc|Feedback ANC]]
- [[concepts/internal-model-control|Internal Model Control]]
- [[concepts/minimum-variance-control|Minimum Variance Control]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/wiener-filter|Wiener Filter]]
- [[concepts/robust-adaptive-filtering|Robust Adaptive Filtering]]

## Related Entities

- [[entities/marek-pawelczyk|Marek Pawełczyk]] — 第一作者，ISVR/Silesian Technical University
- [[entities/stephen-j-elliott|Stephen J. Elliott]] — ANC 理论先驱，ISVR
- [[entities/boaz-rafaely|Boaz Rafaely]] — 反馈 ANC 研究者，ISVR

## Related Synthesis
