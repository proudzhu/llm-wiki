---
type: source
created: 2026-04-12
updated: 2026-04-12
sources:
- raw/articles/Forward propagation of errors through time.md
tags:
- backpropagation-through-time
- blog-post
- forward-error-propagation
- gradient-computation
- numerical-stability
- recurrent-neural-networks
aliases:
- 'Zucchet 2026: Forward Propagation of Errors Through Time'
---

# Forward Propagation of Errors Through Time

**Author**: Nicolas Zucchet
**Published**: 2026-02-17
**URL**: [nicolaszucchet.github.io/Forward-propagation-errors-through-time](https://nicolaszucchet.github.io/Forward-propagation-errors-through-time/)

---

## 一、问题定义：BPTT 必须从后往前算吗？

RNN 训练的标准方法是 **Backpropagation Through Time (BPTT)**：

$$
h_t = f_\theta(h_{t-1}, x_t), \quad t = 1 \text{ to } T
$$

$$
L = \sum_{t=1}^T l_t(h_t)
$$

定义误差项 $\delta_t = \left(\frac{\mathrm{d} L}{\mathrm{d} h_t}\right)^\top$，BPTT 的递归公式为：

$$
\delta_t = J_t^\top \delta_{t+1} + \left(\frac{\partial l_t}{\partial h_t}\right)^\top
$$

其中 $J_t = \partial_h f_\theta(h_t, x_{t+1})$ 是递归 Jacobian。

**BPTT 的两个根本问题**：
1. **内存约束**：必须存储全部隐藏状态轨迹，内存随序列长度线性增长
2. **生物不合理**：要求时间反演，不可能是大脑的学习方式，也不适合神经形态硬件

现有的前向替代方案 RTRL 内存 $O(N^3)$、计算 $O(N^4T)$，不可行。近似方法牺牲了梯度精确性。

---

## 二、FPTT 算法推导

### 2.1 洞察 1：反转 BPTT 方程

BPTT 方程是一个线性系统，通常从 $\delta_{t+1}$ 计算 $\delta_t$，但也可以**反过来**（当 $J_t$ 可逆时）：

$$
\delta_{t+1} = J_t^{-\top} \left(\delta_t - \left(\frac{\partial l_t}{\partial h_t}\right)^\top\right)
$$

问题：$\delta_0$ 是什么？我们不知道。

### 2.2 洞察 2：Warm-up 阶段确定 $\delta_0$

关键性质：两个从不同初始条件出发的误差轨迹，其差异只依赖于初始条件和 Jacobian 连乘积：

$$
\delta'_T - \delta_T = \left(\prod_{t'=0}^{T-1} J_{t'}^{-\top}\right)(\delta'_0 - \delta_0)
$$

从 $\delta'_0 = 0$ 做 warm-up 得到 $\delta'_T$，已知 $\delta_T = \left(\frac{\partial l_T}{\partial h_T}\right)^\top$，反解出：

$$
\delta_0 = \left(\prod_{t'=T-1}^{0} J_{t'}\right)\left(\delta'_T - \left(\frac{\partial l_T}{\partial h_T}\right)^\top\right)
$$

### 2.3 完整算法

**Phase 1（Warm-up）**：
- 初始化 $J = \text{Id}$，$h_0 = 0$，$\delta'_0 = 0$
- 处理序列，递归更新 $h_t$、$\delta'_{t+1}$、$J = J J_t$
- 计算 $\delta_0 = J(\delta'_T - (\partial l_T/\partial h_T)^\top)$

**Phase 2（梯度计算）**：
- 用正确的 $\delta_0$ 正向传播
- 累积梯度 $\partial_\theta f(h_{t-1}, x_t)^\top \delta_t$

### 2.4 多层扩展

对于 $L$ 层 RNN，需要 **$L+1$ 次前向传播**。第 $l$ 层的 warm-up 在第 $l+1$ 层进入误差计算阶段时完成。

| 算法 | 内存 | 前向/后向次数 | 精确 |
|------|------|-------------|------|
| BPTT | $LNT$ | 1 / 1 | 是 |
| RTRL | $(LN)^3$ | 1 / 0 | 是 |
| Diag RTRL | $LN^2$ | 1 / 0 | 否 |
| **FPTT** | $LN^2$ | $L+1$ / 0 | **是** |

---

## 三、实验结果：MNIST98

| 算法 | Test Loss ↓ | Test Accuracy ↑ |
|------|------------|----------------|
| Spatial BP | 0.731 | 96.55% |
| BPTT | 0.691 | 98.30% |
| **FBPTT** | **0.673** | 98.19% |

FBPTT 测试损失甚至略优于 BPTT。

---

## 四、致命问题：数值不稳定性

### 4.1 遗忘 = 不稳定

稳定系统要求 $|\lambda| < 1$，但 FPTT 需要反转 Jacobian → 特征值变为 $1/\lambda$ → $|1/\lambda| > 1$。

**1D 线性案例**：$\delta_0$ 的误差 $\varepsilon$ 在序列末尾变为 $\lambda^{-T} \varepsilon$，指数发散。

> **"Networks that forget cannot be learned with our forward propagation of error algorithm."**

### 4.2 为什么不再研究

1. **数值不稳定**：对 $\delta_0$ 极度敏感，Jacobian 低秩时直接崩溃
2. **可逆 BPTT 全面优于 FPTT**：精确、2 次传播、无数值问题
3. **Jacobian 计算/反转成本**：$O(N^3)$
4. **仍需存储输入序列**

---

## 五、附录：复杂度对比

| 算法 | 内存 | 时间 | 前向/后向 | 精确 |
|------|------|------|----------|------|
| BPTT | $NT$ | $N^2T$ | 1 / 1 | 是 |
| Exact RTRL | $N^3$ | $N^4T$ | 1 / 0 | 是 |
| Diagonal RTRL | $N^2$ | $N^3T$ | 1 / 0 | 否 |
| **Reversible BPTT** | **$N$** | $N^2T$ | 1 / 1 | 是 |
| **FPTT** | $N^2$ | $N^3T$ | 2 / 0 | 是 |

---

## Related Concepts

- [[../concepts/backpropagation-through-time|Backpropagation Through Time]]
- [[../concepts/real-time-recurrent-learning|Real-Time Recurrent Learning]]
- [[../concepts/linear-recurrent-unit|Linear Recurrent Unit]]

## Related Entities

- [[../entities/nicolas-zucchet|Nicolas Zucchet]]

## Related Synthesis
