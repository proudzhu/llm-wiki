---
type: source
created: 2026-04-22
updated: 2026-04-22
sources:
  - zotero://select/items/0_XAZIKCJU
tags:
  - review-paper
  - artificial-intelligence
  - active-vibration-control
  - active-noise-control
  - machine-learning
---

# AI 驱动的主动振动与噪声控制：技术路径、工程应用与未来趋势

> **论文**：A review of artificial intelligence-driven active vibration and noise control
> **作者**：Zongkang Jiang, et al.
> **发表**：Machines 2025
> **阅读时长**：约 20 分钟
> **难度**：⭐⭐⭐⭐
> **前置知识**：主动控制理论 (ANC/AVC)、深度学习基础 (ANN/RL)、系统辨识

---

## TL;DR

本文系统性地综述了 AI 在主动振动与噪声控制 (AI-AVNC) 领域的应用。核心贡献是将 AI-AVNC 划分为四种功能路径：输入成型参数优化、系统辨识与建模、控制器参数优化及端到端控制器建模。文章阐述了从模型驱动向数据驱动演进的技术路线，并深入分析了在新能源汽车、航空航天及精密制造中的工程落地现状。

---

## 论文概述

**问题**：传统 AVNC 依赖精确线性模型，在处理高度非线性、时变系统及复杂耦合环境时存在性能瓶颈。

**方案**：引入机器学习 (DL/RL/Meta-heuristic) 替代或增强控制回路中的关键模块，实现自适应特征提取与非线性映射。

**贡献**：
1. 提出了 AI-AVNC 的四位一体技术分类架构。
2. 对比了物理信息神经网络 (PINN)、强化学习 (RL) 等前沿算法在振动抑制中的优劣。
3. 总结了 AI-AVNC 在 10 余个细分工程场景的应用性能基准。
4. 明确了实时性 (Te2e)、可解释性 (XAI) 与泛化性是当前向工业大规模部署的三大挑战。

---

## 背景与动机

传统主动控制 (如 FxLMS) 面临以下核心瓶颈：
- **模型依赖**：需要精确的次级路径 $S(z)$ 估计，环境变化导致模型失效。
- **线性局限**：无法处理执行器饱和、传感器迟滞等非线性环节。
- **调参成本**：PID、LQR 等增益在多变工况下难以兼顾稳态精度与收敛速度。
- **因果约束**：前馈系统受声学路径延迟限制，缺乏预测能力。

---

## 核心方法

### 1. 整体架构与四大技术路径

![技术分类架构](raw/assets/jiang-2025-review/images/p18_vec1.png)
*(图示：AI-AVNC 的四种核心应用路径)*

### 路径一：AI 驱动的输入成型 (Input Shaping) 优化
- **核心目标**：优化前馈开环脉冲序列，消除柔性结构的残余振动。
- **AI 角色**：使用 DNN 映射频率响应至成型器参数，或利用 RL 在策略空间搜索最优脉冲时刻。
- **性能**：在 40% 的频率失配下，ANN 成型器可降低 50% 以上的残余振幅，且推理延迟极低。

### 路径二：AI 系统辨识与建模
- **次级路径建模**：使用 **DNoiseNet** 等轻量化 MLP 在线估算 $S(z)$，无需注入辅助噪声，避免了对控制性能的影响。
- **动力学辨识**：
  - **NARX-ANN**：捕捉非线性动力学，RMSE 降低 50%。
  - **GNN**：将结构离散化为图，进行快速模态分析，识别速度比 FDD 快 16 倍。

![系统辨识方法对比](raw/assets/jiang-2025-review/images/p19_vec8.png)
*(图示：基于 DL 的次级路径实时更新框架)*

### 路径三：控制器参数动态优化
- **元启发式算法 (PSO, GA, CS)**：全局搜索 PID 或 LQR 的最优权重，例如 **CS-PID** 可实现一阶模态下 44.75 dB 的衰减。
- **安全强化学习 (Safe-RL)**：动态调整控制增益，并通过在线监视器在性能恶化时回退至保守基准。

### 路径四：端到端控制器建模
- **Deep MCANC**：利用卷积递归网络 (CRN) 实现多通道复杂声场映射。
- **GFANC (Generative Fixed-Filters)**：1D-CNN 根据噪声帧实时合成控制滤波器。

![端到端控制器建模](raw/assets/jiang-2025-review/images/p28_vec3.png)
*(图示：基于 CRN 的多通道 ANC 系统架构)*

---

## 实验分析与工程应用

文章验证了 AI-AVNC 在以下场景的显著优势：

1. **新能源汽车 (NEVs)**：
   - 路噪控制：**STFNet** 在人耳位置实现非平稳噪声控制。
   - 电驱系统：通过 **MAC-DDPG** 抑制转子不平衡振动。
2. **航空航天**：
   - 旋翼机振动：RL 补偿襟翼控制延迟。
   - 卫星天线：**DL-NMPC** 在低信噪比下精确抑制柔性臂振动。
3. **精密制造**：
   - 铣仓颤振：**SAC** 驱动压电执行器，实时抑制薄板加工颤振。

---

## 深度理解问答

### Q1: AI-AVNC 中最致命的挑战是什么？

**Te2e (端到端延迟)**。
在 kHz 级的控制回路中，AI 推理延迟必须严格限制在采样间隔的 20% 以内 (例如 5kHz 下需 $<40\mu s$)。文章指出，尽管 Deep ANC 性能强劲，但由于帧处理引入的 OLA (Overlap-and-add) 延迟，其在处理突发瞬态噪声时仍存在不稳定性。

### Q2: 为什么 PINN 在振动控制建模中逐渐取代纯数据驱动模型？

**外推泛化能力与物理一致性**。
纯黑盒模型 (如标准 MLP) 在训练集分布之外表现极差。**PINN** 通过在损失函数中强加微分方程约束 (如波动方程)，确保模型在数据稀疏的情况下依然符合物理规律，减少了控制溢出 (Control Spillover) 的风险。

### Q3: 强化学习 (RL) 在 AVC 调参中的优势与代价？

**优势**：无需梯度模型，直接在交互中学习非线性策略，适合高维复杂约束。
**代价**：采样效率极低 (文中指出稳定收敛需 $>10^6$ 次交互) 且在硬件探索中存在碰撞风险，通常需要 **"热启动"** 或 **"安全屏障函数 (CBF)"** 保护。

---

## 总结

### 核心贡献
- 填补了 AI 在振动与噪声控制领域系统性分类的空白。
- 量化了各主流算法在典型工程任务中的性能基准数据。

### 局限性
- 缺乏针对移动端极低功耗硬件 (如 FP16/INT8 精度) 下的量化性能分析。
- 对多物理场耦合 (如热-振-声) 下的 AI 建模讨论较少。

### 适用场景
- 高度非线性执行器 (如压电迟滞、电磁饱和)。
- 高信噪比但动力学时变的结构 (如精密定位台、轻量化车身)。

---

## Related Concepts
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/active-vibration-control|Active Vibration Control]]
- [[concepts/maximum-correntropy-criterion|Maximum Correntropy Criterion]]
- [[concepts/model-predictive-control|Model Predictive Control]]
- [[concepts/system-identification|System Identification]]
- [[concepts/transparency-mode|Transparency Mode]]

## Related Synthesis
