---
type: source
created: 2026-04-22
updated: 2026-06-28
sources:
  - raw/papers/jiang-2025-ai-driven-avnc-review/full-text.md
  - https://doi.org/10.3390/machines13100946
  - zotero://select/items/0_XAZIKCJU
tags:
  - review-paper
  - artificial-intelligence
  - active-vibration-control
  - active-noise-control
  - machine-learning
  - reinforcement-learning
  - deep-learning
---

# Jiang, Xue, Yue et al. 2025: AI-Driven Active Vibration and Noise Control Review

> **论文**: A review of artificial intelligence-driven active vibration and noise control
> **作者**: [[entities/zongkang-jiang|Zongkang Jiang]], [[entities/hongtao-xue|Hongtao Xue]], [[entities/huiyu-yue|Huiyu Yue]] (corresponding), Xiaoyi Bao, Junwei Zhu, Xuan Wang, Liang Zhang
> **机构**: School of Automotive and Traffic Engineering, Jiangsu University, Zhenjiang 212013, China; International Joint Laboratory on Mobility Equipment and Artificial Intelligence for IT Operations
> **发表**: *Machines* 2025, 13(10), 946
> **DOI**: [10.3390/machines13100946](https://doi.org/10.3390/machines13100946)
> **URL**: [https://www.mdpi.com/2075-1702/13/10/946](https://www.mdpi.com/2075-1702/13/10/946)
> **Zotero**: [XAZIKCJU](zotero://select/items/0_XAZIKCJU)
> **阅读时长**: 约 20 分钟
> **难度**: ⭐⭐⭐⭐
> **前置知识**: 主动控制理论 (ANC/AVC)、深度学习基础 (ANN/RL)、系统辨识

---

## TL;DR

本文系统性地综述了 AI 在主动振动与噪声控制 (AI-AVNC) 领域的应用。核心贡献是将 AI-AVNC 划分为四种功能路径：输入成型参数优化、系统辨识与建模、控制器参数优化及端到端控制器建模。文章阐述了从模型驱动向数据驱动演进的技术路线，并深入分析了在新能源汽车、航空航天及精密制造中的工程落地现状。

---

## Summary

传统 AVNC 依赖精确线性模型，在处理高度非线性、时变系统及复杂耦合环境时存在性能瓶颈。本文引入机器学习 (DL/RL/Meta-heuristic) 替代或增强控制回路中的关键模块，实现自适应特征提取与非线性映射。文章从控制策略本质出发，将 AI-AVNC 分为四大技术路径，对比了 [[concepts/physics-informed-neural-network|PINN]]、[[concepts/reinforcement-learning-for-control|强化学习]] 等前沿算法在振动抑制中的优劣，总结了 10 余个细分工程场景的应用性能基准，并明确了实时性 (Te2e)、可解释性 (XAI) 与泛化性是当前向工业大规模部署的三大挑战。

---

## Problem Formulation

传统主动控制 (如 [[concepts/filtered-x-lms-algorithm|FxLMS]]) 面临以下核心瓶颈：

- **模型依赖**: 需要精确的次级路径 $S(z)$ 估计，环境变化导致模型失效。
- **线性局限**: 无法处理执行器饱和、传感器迟滞等非线性环节。
- **调参成本**: PID、LQR 等增益在多变工况下难以兼顾稳态精度与收敛速度。
- **因果约束**: 前馈系统受声学路径延迟限制，缺乏预测能力。

当建模误差或相位失配达到一定量级时，传统 AVNC 算法的控制性能急剧恶化，甚至导致系统不稳定。

---

## Methodology

### 1. 整体架构与四大技术路径

![[raw/assets/jiang-2025-review/images/p18_vec1.png|AI-AVNC 的四种核心应用路径]]

*Figure: AI-AVNC 的四种核心应用路径分类。*

文章从控制策略本质出发，将 AI-AVNC 分为四条技术路径：

| 技术路径 | AI 角色 | 在线计算负担 | 实时性要求 |
|----------|---------|-------------|-----------|
| 输入成型参数优化 | DNN/RL 搜索最优脉冲序列 | 最轻 | 易满足硬实时 |
| 系统辨识与建模 | DL 在线估算 $S(z)$ / 动力学 | 较重 | kHz 级采样下压力大 |
| 控制器参数优化 | 元启发式/RL 调整 PID/LQR 增益 | 依赖离线训练 | 难以在线迭代 |
| 端到端控制器建模 | CRN/DRL 直接生成控制信号 | 最重 | 推理延迟需 <采样间隔 20% |

### 路径一：AI 驱动的输入成型 (Input Shaping) 优化

- **核心目标**: 优化前馈开环脉冲序列，消除柔性结构的残余振动。
- **AI 角色**: 使用 DNN 映射频率响应至成型器参数，或利用 RL 在策略空间搜索最优脉冲时刻。
- **关键方法**:
  - **ANN-based IS**: Ramli et al. (2018) 使用神经网络映射频率响应至成型器参数，在 40% 频率失配下降低 50% 以上残余振幅。
  - **RL-based IS**: Vu et al. (2018) 使用 RL 在策略空间搜索最优脉冲时刻。
  - **PINN-based IS**: Li & Xiao (2025) 使用 [[concepts/physics-informed-neural-network|PINN]] 约束柔性单臂机器人振动抑制。
- **局限**: 高度依赖模态频率和阻尼精度；环境导致参数漂移时脉冲序列失配，甚至诱发反向激励。

### 路径二：AI 系统辨识与建模

![[raw/assets/jiang-2025-review/images/p19_vec8.png|基于 DL 的次级路径实时更新框架]]

*Figure: 基于 DL 的次级路径实时更新框架。*

#### 次级路径建模
- **DNoiseNet** (Cha 2023): 轻量化 MLP 在线估算 $S(z)$，无需注入辅助噪声，避免对控制性能的影响。
- **DNN-based SPE** (Oh 2024): 实时更新次级路径估计，驱动 FxLMS 实现自适应降噪，使用 ERLE 评估性能。

#### 动力学辨识
- **NARX-ANN** (Song 2022): 捕捉非线性动力学，振动台上 RMSE 仅 $3.68 \times 10^{-3}\,\text{g}$，较传统方法降低约 50%。
- **PINN** (Teloli 2025): 将结构力学方程嵌入损失函数，通过自动微分获取高阶导数，同时辨识参数和重建位移，增强小样本下的外推泛化能力。
- **GNN** (Li 2023): 将结构离散化为图，进行快速模态分析。在仅 18% 节点配备传感器时仍可稳定识别前几阶模态；100 个桁架样本批量识别仅需 2.5s (传统 FDD 需 39.95s，快 16 倍)。

#### 激励扰动源建模
- **LSTM-based ANC** (Kwon 2022): 预测参考噪声信号生成控制信号，单次推理 <20ms，适用于资源受限的嵌入式系统。
- **TNResNet** (Yang 2024): 基于 Mel 频谱图的轮胎噪声识别网络，用于路况识别。
- **DRL wind disturbance** (Ma 2024): 在线风场建模嵌入 DRL 观测空间和奖励函数，实现无人机抗风扰动控制。

### 路径三：控制器参数动态优化

![[raw/assets/jiang-2025-review/images/p22_vec2.png|AI 驱动的控制器参数优化架构]]

*Figure: AI 驱动的控制器参数优化架构。*

#### 元启发式算法 (PSO, GA, CS)
- **PSO-PID**: 将 PID 参数 $(K_p, K_i, K_d)$ 编码为粒子位置，以 ISE/ITAE 为适应度函数全局搜索。
- **CS-PID**: 实现一阶模态下 44.75 dB 的衰减。
- **PSO-FLC**: 编码隶属度函数形状参数为粒子位置，动态调整模糊规则。

#### 安全强化学习 (Safe-RL)
- **RL-PID**: 将 PID 增益向量参数化为 DPG agent 的连续动作，闭环迭代更新；监督器监控运行奖励，性能恶化超阈值时回退至保守基准 PID。
- **DCDDPG-GESO**: 将 GESO 增益调谐建模为连续动作 RL，双 critic 取 min-Q 抑制过估计。
- **RBFNN-SMC**: 使用 RBFNN 在线逼近执行器未知非线性和时变不确定性，基于 Lyapunov 推导权重自整定律。

#### AI 增强模型预测控制
- **ESN-MPC**: 使用回声状态网络 (ESN) 多步预测时变扰动，写入 MPC 输出预测和代价函数形成约束 QP。
- **NMPC-NARX**: NMPC 在滚动时域求解最优 PZT 驱动，NARX 学习非线性并在线修正预测误差。

### 路径四：端到端控制器建模

![[raw/assets/jiang-2025-review/images/p28_vec3.png|基于 CRN 的多通道 ANC 系统架构]]

*Figure: 基于 CRN 的多通道 ANC 系统架构。*

- **Deep MCANC**: 利用卷积递归网络 (CRN) 实现多通道复杂声场映射。
- **GFANC** (Generative Fixed-Filters): 1D-CNN 根据噪声帧实时合成控制滤波器，实现快速匹配噪声分布。
- **ARN (Attention Recurrent Network)**: 短帧长注意力递归网络 + "预测-延迟补偿"训练，将 Deep ANC 算法延迟压缩至工程实用范围。

---

## Experimental Setup

文章综述性梳理了 AI-AVNC 在三大工程领域的应用，无统一实验设置。以下为关键应用场景及对应方法：

| 应用领域 | 场景 | 关键方法 | 性能指标 |
|---------|------|---------|---------|
| 新能源汽车 (NEVs) | 车内路噪 | STFNet-headrest ANC | 人耳位置非平稳噪声控制 |
| 新能源汽车 (NEVs) | 电驱系统振动 | MAC-DDPG | 抑制柔性转子同步振动 |
| 新能源汽车 (NEVs) | 悬架振动 | PPO/DDPG | 改善乘坐舒适性 |
| 航空航天 | 旋翼机振动 | RL 襟翼控制 | 延迟补偿+扰动抑制 |
| 航空航天 | 卫星天线 | DL-NMPC | 低信噪比下精确振动抑制 |
| 精密制造 | 铣削颤振 | SAC 驱动压电执行器 | 实时抑制薄板加工颤振 |
| 精密制造 | 纳米定位台 | NN-SORC | 补偿迟滞非线性，残余振动控制 |

---

## Results

### 关键定量发现

1. **ANN 输入成型器**: 在 40% 频率失配下降低 50% 以上残余振幅，推理延迟极低。
2. **NARX-ANN 辨识**: 振动台 RMSE $3.68 \times 10^{-3}\,\text{g}$，较传统方法降低约 50%。
3. **GNN 模态识别**: 100 个桁架样本批量识别 2.5s (FDD 需 39.95s)，快 16 倍；仅 18% 节点传感仍可稳定识别。
4. **CS-PID**: 一阶模态下 44.75 dB 衰减。
5. **LSTM-ANC**: 单次推理 <20ms，适用于嵌入式系统。
6. **DeepSPE (Fareedha 2026)**: −16.27 dB NMSE，较最佳经典方法好 3.92 dB；双流设计仅 1.05M 参数、0.43ms 延迟。

### 三大技术挑战

1. **实时性与计算复杂度的矛盾 (Te2e)**: kHz 级控制回路中，AI 推理延迟必须严格限制在采样间隔的 10-20% 以内 (例如 5kHz 下需 $<40\mu s$)。Deep ANC 因 OLA 帧处理引入延迟，处理突发瞬态噪声时存在不稳定性。
2. **模型可解释性与可信度不足**: 黑盒模型 (DNN/RL) 难以提供闭环稳定性、可控性、可观测性的审计证据；[[concepts/safe-reinforcement-learning|Safe-RL]] 通过 CMDP、Lyapunov、CBF 机制集成硬约束和风险度量。
3. **跨域泛化能力不足**: 训练数据分布外的工况 (负载变化、执行器饱和、传感器特性变化) 导致性能急剧下降；时序基础模型+自监督预训练+LoRA 是未来方向。

---

## Key Contributions

1. 提出了 AI-AVNC 的四位一体技术分类架构 (输入成型、系统辨识、控制器参数优化、端到端控制器建模)，从控制策略本质出发而非简单按算法类型分类。
2. 对比了 [[concepts/physics-informed-neural-network|PINN]]、[[concepts/reinforcement-learning-for-control|强化学习]] 等前沿算法在振动抑制中的优劣，量化了各方法在辨识精度、收敛速度、鲁棒性方面的基准。
3. 总结了 AI-AVNC 在新能源汽车、航空航天、精密制造 10 余个细分工程场景的应用性能基准。
4. 明确了实时性 (Te2e)、可解释性 (XAI) 与泛化性是当前向工业大规模部署的三大挑战，并提出了低延迟混合架构、可信可验证框架、跨场景迁移学习三大未来方向。

---

## Future Work

1. **低延迟可部署混合 AI-AVNC 系统**: 从纯端到端网络转向短帧时域网络+固定/半固定滤波+轻量化在线校准的混合范式；算法-硬件协同设计 (逻辑门网络)。
2. **可信可验证 AI-AVNC 系统**: [[concepts/safe-reinforcement-learning|Safe-RL]] 集成硬约束和风险度量；神经 Lyapunov 函数提供安全证明；XAI 与因果推理结合。
3. **跨场景可迁移 AI-AVNC 系统**: 时序基础模型+自监督预训练构建统一表示空间；参数高效适配 (LoRA) 降低冷启动成本；测试时适配 (TTA) 实现在线域适应。

---

## Limitations

- 缺乏针对移动端极低功耗硬件 (如 FP16/INT8 精度) 下的量化性能分析。
- 对多物理场耦合 (如热-振-声) 下的 AI 建模讨论较少。
- 未提供统一的实验对比基准 (综述性质所致)。

---

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/active-vibration-control|Active Vibration Control]]
- [[concepts/input-shaping|Input Shaping]]
- [[concepts/physics-informed-neural-network|Physics-Informed Neural Network]]
- [[concepts/reinforcement-learning-for-control|Reinforcement Learning for Control]]
- [[concepts/safe-reinforcement-learning|Safe Reinforcement Learning]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/model-predictive-control|Model Predictive Control]]
- [[concepts/system-identification|System Identification]]
- [[concepts/generative-fixed-filter-anc|Generative Fixed-Filter ANC]]
- [[concepts/maximum-correntropy-criterion|Maximum Correntropy Criterion]]
- [[concepts/transparency-mode|Transparency Mode]]
- [[concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/deep-secondary-path-estimation|Deep Secondary Path Estimation]]
- [[concepts/end-to-end-differentiable-anc|End-to-End Differentiable ANC]]

## Related Synthesis

- [[synthesis/ai-driven-anc|AI-Driven Active Noise Control]]
- [[synthesis/anc-architecture-evolution|ANC Architecture Evolution]]
- [[synthesis/nonlinear-anc-approaches|Nonlinear ANC Approaches]]
- [[synthesis/secondary-path-modeling-evolution|Secondary Path Modeling Evolution]]
- [[synthesis/adaptive-algorithm-tradeoffs|Adaptive Algorithm Tradeoffs]]
