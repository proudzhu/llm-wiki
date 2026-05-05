---
type: source
created: 2026-04-12
updated: 2026-04-12
sources:
  in active noise and vibration control.md
tags:
- active-noise-control
- active-vibration-control
- constraint-handling
- dsp-implementation
- model-predictive-control
- quadratic-programming
aliases:
- 'Wills 2008: MPC Constraint Handling in ANC/AVC'
---

# Model Predictive Control Applied to Constraint Handling in Active Noise and Vibration Control

**Authors**: Adrian G. Wills, Dale Bates, Andrew J. Fleming, Brett Ninness, S. O. Reza Moheimani
**Published**: IEEE Transactions on Control Systems Technology, Vol. 16, pp. 3-12, January 2008
**DOI**: [10.1109/TCST.2007.903062](https://doi.org/10.1109/TCST.2007.903062)
**📎 Zotero**: [zotero://select/items/0_QU9NZUUG](zotero://select/items/0_QU9NZUUG)

---

## 一、问题定义：执行器饱和是 ANC/AVC 的核心瓶颈

主动噪声/振动控制（ANC/AVC）中，执行器（扬声器、压电片等）有严格的物理限制：
- **电压/电流范围**：放大器输出有限
- **位移范围**：扬声器振膜行程有限
- **去极化电压**：压电陶瓷有最低电压限制

**传统处理方式的缺陷**：
1. **超规格硬件**：增大动态范围 → 信噪比降低、分辨率下降、成本增加
2. **简单饱和**：遇到饱和时控制器开环 → 性能退化甚至不稳定
3. **保守调参**：降低控制器增益 → 永远达不到最佳性能

**MPC 的优势**：约束作为优化问题的边条件直接纳入，在限制内找到最优控制。

---

## 二、MPC 公式化

### 2.1 状态空间模型

$$
x_{t+1} = A x_t + B u_t + K e_t
$$

$$
y_t = C x_t + D u_t + e_t
$$

其中 $e_t$ 是 Kalman 滤波器的新息（innovation）。

### 2.2 MPC 优化问题

在每个时刻 $k$，求解：

$$
\min_{U} \sum_{t=0}^{N-1} \ell(\hat{y}_{t|k}, \hat{u}_{t|k}) + \ell_f(\hat{x}_{N|k})
$$

s.t.
- $\hat{x}_{t+1|k} = A \hat{x}_{t|k} + B \hat{u}_{t|k}$
- $\hat{y}_{t|k} = C \hat{x}_{t|k} + D \hat{u}_{t|k}$
- $(\hat{y}_{t|k}, \hat{u}_{t|k}) \in \mathcal{C}$（约束集）

其中 $N$ 是预测视界，$\ell$ 是阶段代价（通常二次型），$\ell_f$ 是终端代价。

### 2.3 终端权重的选择

为保证无约束时的闭环稳定性，终端权重矩阵 $P$ 选为 DARE 的正定解：

$$
P = A^\top P A + Q - (A^\top P B)(R + B^\top P B)^{-1}(B^\top P A)
$$

此时无约束 MPC 等价于 LQG。对于充分大的 $N$，即使有约束也能保证稳定性。

### 2.4 二次规划形式

通过堆叠预测变量，MPC 问题等价于凸 QP：

$$
\min_z \frac{1}{2} z^\top H z + x_k^\top F z
$$

s.t. $G z \leq W + S x_k$

其中 $H$ 正定，$z$ 是未来控制序列。

---

## 三、实验设置：悬臂梁主动振动控制

### 3.1 装置

- **梁**：铝制悬臂梁，550 mm × 50 mm × 3 mm
- **执行器**：3 个压电陶瓷片（PI PIC151），位于模态应变最大处（55 mm 和 215 mm）
- **传感器**：压电片电压（反馈信号）+ 激光测振仪（梁尖端速度，性能评估）
- **硬件**：Analog Devices ADSP-21262，32-bit 浮点 DSP，200 MHz

### 3.2 系统辨识

- 频域数据：5-500 Hz，908 个非等间隔频率点
- 14 阶状态空间模型（2 输入 2 输出）
- 覆盖前 5 个弯曲模态（5 Hz - 500 Hz）
- 采样率：5 kHz（最高模态频率的 10 倍）

### 3.3 高频未建模模态处理

模型只包含前 5 个模态，高频控制作用可能激发未建模模态。解决方案：

**在代价函数中惩罚高频控制作用**：
- 串联 4 阶 Butterworth 高通滤波器（截止频率 450 Hz）
- 对滤波后的信号施加惩罚
- 增广系统从 14 阶 → 18 阶

### 3.4 约束设置

$$
-0.5 \leq u_t \leq 0.5
$$

对应压电片输入电压在放大前的简单边界限制。

---

## 四、DSP 实现细节

### 4.1 离线 vs 在线计算

| 阶段 | 内容 |
|------|------|
| **离线** | 系统矩阵 $A,B,C,D,K$，权重 $Q,R,P$，约束集 $G,W,S$ |
| **在线** | 状态估计 $\hat{x}_k$，求解 QP 得到 $u_k$ |

### 4.2 QP 求解器

采用 **Goldfarb-Idnani 活动集法**：
- 不需要可行初始点（从未约束解开始）
- 支持热启动（用上一次解初始化）
- 处理等式、不等式、简单边界约束
- 手动用汇编实现以最小化开销

### 4.3 内存需求

| 组件 | 存储（字） |
|------|-----------|
| 观测器 | ~300 |
| QP 求解器 | ~970 |
| **总计（N=12, n=18）** | **~1270 字 ≈ 10 KB** |

非常 modest——ADSP-21262 有 1 Mb 存储空间。

### 4.4 求解时间

| 预测视界 $N$ | 最坏情况 QP 时间 | 约束激活比例 |
|-------------|-----------------|-------------|
| 4 | ~30 μs | 14% |
| 8 | ~70 μs | 28% |
| **12** | **<150 μs** | **36%** |

采样周期 = 200 μs（5 kHz），因此 QP 求解时间充足。

---

## 五、实验结果

### 5.1 无约束情况（未碰到限制）

周期 chirp 扰动（5-800 Hz），调整增益使不碰到约束。

**结果**：MPC 与 LQG 性能相同（理论预期），开环→闭环频率响应匹配仿真。

### 5.2 有约束情况（碰到限制）

带通滤波阶跃函数（230-270 Hz，第四模态），增大增益确保碰到约束。

**对比基线**：饱和 LQG（SLQG）——遇到约束时简单截断控制信号。

**关键发现**：
- **MPC 显著缩短 settling time**：比 SLQG 更快收敛
- **MPC 降低总能量**：输出能量和输入能量均低于 SLQG
- **SLQG 在饱和时"开环"**：控制器失去对系统的控制能力

### 5.3 QP 求解器实证极限

150 万次 QP 调用记录：
- $N=12$ 时，最坏情况 <150 μs
- 约束激活时的求解时间分布：大多数 <50 μs，少数 >100 μs
- 约束激活数：0-3 个约束同时激活最常见

---

## 六、与 [[liang-2026-delayed-mpc-anc-paper-reading-note|Liang 2026: Delayed MPC for ANC Paper Reading Note]] 的对比

| 维度 | Wills 2008（本文） | Liang 2026（Delayed MPC） |
|------|-------------------|--------------------------|
| **核心目标** | 约束处理（执行器饱和） | 消除 BPTT 时间反向需求 |
| **应用领域** | 主动振动控制（压电悬臂梁） | 主动噪声控制（驻波管） |
| **MPC 类型** | 传统在线 QP（活动集法） | 正向误差传播（解析闭式解） |
| **采样率** | **5 kHz** | 4 kHz |
| **模型阶数** | 18 阶 | 30 阶（15+15） |
| **预测视界** | 12 步 | 9 步 |
| **硬件** | 200 MHz DSP（ADSP-21262） | Speedgoat 实时目标机 |
| **计算时间** | <150 μs/QP | ~921 次乘法/样本 |
| **数值稳定性** | 好（凸 QP） | **差**（Jacobian 反转导致不稳定） |
| **约束处理** | **显式纳入优化** | 仅通过饱和近似 |

**互补关系**：Wills 2008 展示了传统 MPC 在约束处理上的成功，但需要在每个采样时刻求解 QP。Liang 2026 尝试用解析闭式解替代 QP 求解，但遇到了数值稳定性问题。

---

## 七、Q&A

**Q1: 为什么不用 Explicit MPC（查找表）？**

Explicit MPC 将 QP 的解预先计算为分段仿射函数，在线只需查表。但对于本文问题：
- $N=12$，18 阶系统 → 查找表需要 **超过 1 Mb 内存**
- ADSP-21262 只有 1 Mb 总存储
- "维度灾难"——自由度数增加时表大小指数增长

因此选择传统在线 QP 求解。

**Q2: MPC 相比 FXLMS 在 ANC 中有什么优势？**

FXLMS 是无约束的梯度下降算法，遇到执行器饱和时性能退化。MPC 显式处理约束：
- 饱和前：MPC ≈ LQG ≈ FXLMS（稳态）
- 饱和时：MPC 在限制内重新分配控制能量，FXLMS 直接"开环"
- 代价：MPC 计算量远大于 FXLMS（QP vs 向量乘法）

**Q3: 为什么预测视界 $N=12$？**

$N$ 太小 → 约束下不保证稳定性；$N$ 太大 → 计算超时。实验表明 $N=12$ 在 5 kHz 采样率下是最坏 150 μs（<200 μs 采样周期）且约束处理效果良好。

---

## Related Concepts

- [[../concepts/model-predictive-control|Model Predictive Control]]
- [[../concepts/active-noise-control|Active Noise Control]]
- [[../concepts/active-vibration-control|Active Vibration Control]]
- [[../concepts/quadratic-programming|Quadratic Programming]]
- [[../concepts/kalman-filter|Kalman Filter]]

## Related Sources

- [[liang-2026-delayed-mpc-anc-paper-reading-note|Liang 2026: Delayed MPC for ANC Paper Reading Note]] — 另一种 MPC 用于 ANC 的方法（解析闭式解 vs 在线 QP）

## Related Entities

- [[../entities/adrian-g-wills|Adrian G. Wills]] — 第一作者，University of Newcastle
- [[../entities/andrew-j-fleming|Andrew J. Fleming]] — 共同作者，主动振动控制专家

## Related Synthesis
