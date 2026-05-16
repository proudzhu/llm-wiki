---
type: synthesis
created: 2026-04-25
updated: 2026-04-27
sources:
tags:
  - anc
  - secondary-path
  - system-identification
  - online-modeling
  - offline-modeling
---

# 次级通道建模：从离线辨识到免建模演进

## 核心矛盾

次级通道 $S(z)$ 是 FXLMS 算法的命脉——参考信号必须经 $\hat{S}(z)$ 滤波后才能更新权重。但 $S(z)$ 本身是时变的（耳机佩戴位移、温度漂移、气流变化），而建模过程又与 ANC 运行相互干扰。**整个次级通道建模领域都在解决一个矛盾：如何在不干扰降噪的前提下，持续跟踪一个不断变化的传递函数。**

## 四条技术路线

### 路线 1：离线建模 → 定期重校

最简单的方案：ANC 停机 → 注入白噪声 → LMS 辨识 → 固定 $\hat{S}(z)$ → 启动 ANC。

| 优势 | 劣势 |
|------|------|
| 实现简单，无干扰 | 时变环境下很快过时 |
| 辨识精度高（无信号污染） | 需要停机，用户体验差 |

**适用**：固定安装（管道、建筑），$S(z)$ 准静态。

Kuo (1999) 给出离线 LMS 辨识的标准流程，收敛后 $\hat{S}(z)$ 固定。Benois (2020) 的 FPGA 原型也采用离线预标定，但指出耳机场景下佩戴变化导致 $\hat{S}(z)$ 偏差是主要性能瓶颈。

### 路线 2：加性噪声在线建模

ANC 运行时注入低功率辅助噪声 $v(n)$，同时辨识 $\hat{S}(z)$。

**核心困难**：$v(n)$ 必须足够大才能辨识，但太大会被用户听到。Kuo (1999) 分析了收敛速度与 $\sigma_d^2 / \sigma_v^2$ 的关系——在线建模比离线慢该比值倍。

**改进方向**：
- **Eriksson (1989)**：基本两滤波器加性噪声结构，$v(n)$ 出现在残余误差中，约束其功率
- **Zhang (2001)**：三滤波器交叉更新法，在经典方法中性能最佳
- **Akhtar (2006)**：两滤波器 + MFxLMS + [[concepts/variable-step-size-lms|VSS LMS]]（逆步长策略），以更少滤波器达到更好性能，−12.35 dB NMSE
- **自适应噪声消除**：用辅助滤波器消除 $d(n)$ 对辨识的干扰，加速 ~30 倍
- **RMFxLMS**（Yang 2026）：鲁棒多通道变体，处理多通道场景下的交叉耦合

### 路线 3：免辅助噪声建模

不注入额外信号，仅利用 ANC 运行中已有的信号辨识 $\hat{S}(z)$。

- **联立方程法**（Jin 2007, Fujii 1999）：对输入输出信号做差分，建立代数方程联立求解 $\hat{S}(z)$，无需 $v(n)$
- **系数更新法**：利用 FxLMS 权重更新方程中的隐含信息反推 $\hat{S}(z)$

**代价**：收敛更慢、稳定性更差，且对信噪比敏感。

### 路线 4：绕过 $S(z)$ 辨识

最激进的路线——完全不建模 $\hat{S}(z)$，从算法层面消除对它的依赖。

| 方法 | 原理 | 代价 |
|------|------|------|
| **SPR 条件**（Zhou 2007） | 严格正实条件保证稳定性，无需 $\hat{S}(z)$ | 条件苛刻，实际难以满足 |
| **进化搜索**（GA/PSO） | 遗传算法/粒子群直接搜索最优 $W(z)$ | 计算量极大，不适合实时 |
| **Careful Control**（Lopes 2022） | 双控制框架交替最小二乘 | 收敛慢，但无需 $\hat{S}(z)$ |
| **元学习初始化**（Yang 2026） | MAML 预训练 $W(z)$ 初始值 | 需要大量离线数据 |
| **MPC**（Liang 2026, Wills 2008） | 状态空间模型内嵌 $S(z)$，QP 求解绕过显式辨识 | 需要精确的植物模型 |

Liang (2026) 的延迟 MPC 是一个有趣的案例：MPC 的状态空间模型需要 $S(z)$ 的参数化形式（通过向量拟合获得），但一旦模型建立，QP 求解器直接输出最优控制信号，不再需要 $\hat{S}(z)$ 滤波参考信号这一步。**$S(z)$ 从"每样本使用的滤波器"退化为"一次性标定的模型参数"**。

## 决策矩阵

| 场景 | 推荐路线 | 理由 |
|------|---------|------|
| 固定安装，$S(z)$ 准静态 | 路线 1（离线） | 简单可靠，无需在线开销 |
| 耳机/可穿戴，$S(z)$ 缓变 | 路线 2（加性噪声） | 平衡精度与实时性 |
| 对辅助噪声敏感（助听器） | 路线 3（免辅助噪声） | 不引入可听噪声 |
| 非线性/非平稳严重 | 路线 4（MPC 或元学习） | 绕过 $S(z)$ 辨识瓶颈 |

## 建模误差的影响链

$\hat{S}(z)$ 误差通过以下链条影响系统：

```
相位误差 > 90° → FXLMS 发散（失稳）
相位误差 40°-90° → 收敛速度下降，稳态残余增大
幅度误差 → 步长等效缩放，收敛变慢但不失稳
时变偏差 → 周期性振荡，需在线跟踪
```

Kuo (1999) 的经典结论：慢自适应条件下 FXLMS 可容忍 ~90° 相位误差，40° 以内几乎不影响收敛。这意味着**粗略的 $\hat{S}(z)$ 通常够用**，但时变环境下"粗略"本身也在恶化。

## 演进趋势

1. **从离线到在线**：可穿戴设备驱动，$S(z)$ 时变成为常态
2. **从显式到隐式**：MPC、元学习等方法将 $S(z)$ 内嵌到模型中，避免每样本滤波
3. **从单一到混合**：Luo (2026) 的 GFANC-FxNLMS 用生成模型提供初始滤波器，FxNLMS 在线微调——$\hat{S}(z)$ 的精度要求被降低
4. **从辨识到绕过**：终极目标是完全消除对 $\hat{S}(z)$ 的依赖，但目前只有 MPC 在特定条件下接近这一目标
5. **从迭代到深度学习**：Fareedha (2026) 的 [[concepts/deep-secondary-path-estimation|DeepSPE]] 用 Conv1D + BiLSTM + Attention 替代迭代自适应，帧级推理达到 −16.27 dB NMSE，比 Akhtar VSS-LMS 提升 3.92 dB

## 相关页面

- [[concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/online-secondary-path-modeling|Online Secondary-Path Modeling]]
- [[concepts/offline-secondary-path-modeling|Offline Secondary-Path Modeling]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/variable-step-size-lms|Variable Step Size LMS]]
- [[concepts/deep-secondary-path-estimation|Deep Secondary Path Estimation]]
- [[synthesis/mpc-vs-fxlms-for-anc|MPC vs Traditional ANC]]
- [[queries/how-to-estimate-secondary-path|如何估计次级通道]]
