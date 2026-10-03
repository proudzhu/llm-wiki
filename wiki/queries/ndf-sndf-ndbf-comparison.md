---
type: query
created: 2026-10-03
updated: 2026-10-03
sources:
  - raw/papers/wechsler-2024-neural-directional-filtering/full-text.md
  - raw/papers/huang-2025-steerable-neural-directional-filtering/full-text.md
  - raw/papers/huang-2026-dual-mic-steerable-neural-beamformer/full-text.md
tags:
  - neural-directional-filtering
  - differential-microphone-array
  - beam-steering
  - directivity-pattern
  - deep-learning
---

# NDF、SNDF、NDBF 三代神经方向滤波方法对比

> 基于三篇论文的完整阅读生成：[[sources/wechsler-2024-neural-directional-filtering|Wechsler et al. 2024（NDF）]]、[[sources/huang-2025-steerable-neural-directional-filtering|Huang et al. 2025（SNDF）]]、[[sources/huang-2026-dual-mic-steerable-neural-beamformer|Huang & Habets 2026（NDBF）]]。

## 基本信息

| | **NDF** (Wechsler et al. 2024) | **SNDF** (Huang et al. 2025) | **NDBF** (Huang & Habets 2026) |
|---|---|---|---|
| 会议 | IWAENC 2024 | Euronoise 2025 | arXiv 2609.27021 |
| 定位 | 奠基论文：DNN 直接学习 VDM 信号 | 首个可转向 NDF（单模型任意方向） | 双麦线性阵列的神经差分波束形成器 |
| 阵列 | Q=4：中心麦 + 3麦UCA（3 cm 直径） | 同 NDF | **Q=2 线性阵列，3 cm 间距**（混叠 >5.7 kHz） |
| VDM/参考点 | 中心麦克风 | 中心麦克风 | 阵列中心 $\mathbf{p}_c$ |

## 网络结构

| | NDF | SNDF | NDBF |
|---|---|---|---|
| 骨干 | FT-JNF（Tesch & Gerkmann 2023） | JNF-SSF（同款骨干） | JNF-SSF（同款骨干） |
| 主干 | F-BiLSTM（频率轴）→ T-UniLSTM（时间轴，因果）→ linear+tanh | F-BiLSTM（256）→ T-UniLSTM（128）→ linear+tanh | F-BiLSTM → T-UniLSTM → linear+tanh |
| 输入 | $[B,T,F,2Q]{=}[B,T,F,8]$，实/虚堆叠 | $[B,T,F,8]$ | $[B,T,F,4]$（2 麦 × 实/虚） |
| **输出形式** | **单通道复数掩码** $\mathcal{M}[f,t]$，作用于参考麦 $\hat{Z}=\mathcal{M}\cdot Y_1$ | **单通道复数掩码** $\mathcal{M}_{\theta_s}[f,t]\cdot Y_1$ | **复数权重向量** $\mathbf{w}_{\theta_s}(f)$，$\hat{Z}=\mathbf{w}^{H}\mathbf{y}$ — 真正的波束形成 |
| 转向条件 | 无（固定 $\vartheta_0=0$，每个指向图单独训练） | one-hot($\theta_s$) → linear → F-BiLSTM 前向/后向初始状态（每时间帧） | 沿用 SNDF 机制，$M=36$ 类 |
| 参数量 | 873K | 873K | 未标注（骨干同款） |
| STFT | 32 ms sqrt-Hann，50% overlap，16 kHz | 同左 | 同左（遵循 NDF 训练细节） |

**核心架构差异只有两处**：① SNDF 在 NDF 上加转向条件分支；② NDBF 把 SNDF 的掩码输出换成权重向量、阵列从圆形换成线性双麦。

## 损失函数

| | NDF | SNDF | NDBF |
|---|---|---|---|
| 损失 | **SA-ε-tSDR**（源聚合正则化门限 SDR，von Neumann 2022） | **batch 聚合归一化 L1**：$\mathcal{L}=\frac{\sum_b\|z^b-\hat{z}^b\|_1}{\sum_b\|z^b\|_1+\epsilon}$ | 同 SNDF 归一化 L1（训练细节遵循 NDF） |
| 选择原因 | 掩码动态范围大（多源位于零点时需强衰减），纯 SDR 梯度不稳定 | 更简单稳定；配 **mini-batch 采样规则**：每批至少 1 个样本在目标转向方向附近有说话人，防止 L1 分母坍缩 | 沿用 |
| ε | $1.2\times10^{-7}$，门限 30 dB | $1.2\times10^{-7}$ | $1.2\times10^{-7}$ |

## 训练设置

| | NDF | SNDF | NDBF |
|---|---|---|---|
| 场景 | 全圆 144 DOA，3 m 活动圆，与阵列同心 | 全圆 72 点网格（5°） | **半圆**（线性阵列左右对称）：训练 {0°, 5°, …, 175°} |
| 场景复用 | 无（每模型一个固定方向） | **每个声学场景 × 72 个转向目标**作为独立样本 | 每场景 × 36 个转向目标（SNDF 策略） |
| 训练规模 | 10,000 样本 × 6 个模型（每 $N_{\text{train}}$ 上限一个） | 11,520 场景 × 72 目标 | 1,440 场景 × 36 目标 |
| 并发说话人 | $N_{\text{train}}\in\{1..6\}$（≥3 后收益饱和） | ≤3 | ≤3 训练；**恰好 2** 测试 |
| 源距离 | 3 m 圆 | 3 m 圆 | 1.5 m 固定 |
| 响度/噪声 | [−33, −25] LUFS；30 dB SNR | [−33, −25] dBFS；30 dB SNR | EARS 最小响度 −42 dBFS；30 dB SNR |
| 优化 | batch 10，lr 0.001，250 epochs | batch 10，lr 0.001，≤100 epochs | 遵循 NDF |
| 验证/测试 DOA | 验证 5°/15°/…；测试 2.5°/7.5°/…（交错划分） | 验证 2.5° 交错；测试 144 点、偏移 1.25° | 验证 {2.5°, …, 177.5°}；测试 {1.25°, 3.75°, …, 178.75°} |
| 测试集 | LibriSpeech test-clean，3,000 样本 | test-clean，3,240 场景 × 5 转向 {0°, 30°, 60°, 90°, 120°} | **EARS 数据集**，3,240 样本，转向 {0°, 30°, 60°, 90°} |

## 目标指向图与结果

| | NDF | SNDF | NDBF |
|---|---|---|---|
| 目标图 | 一阶心形 $(\tfrac{1}{2},\tfrac{1}{2})$；三阶 $(0,\tfrac{1}{6},\tfrac{1}{2},\tfrac{1}{3})$ | 一阶心形；三阶；**六阶** $(\tfrac{1}{49},\tfrac{8}{49},\tfrac{8}{49},-\tfrac{48}{49},-\tfrac{48}{49},\tfrac{64}{49},\tfrac{64}{49})$，零点 −40 dB 截断 | 简化 DMA 图 $\Lambda=(\mu+(1-\mu)\cos(\theta-\theta_s))^{J}$：一阶心形（$\mu{=}0.5, J{=}1$）与 **三阶心形**（$J{=}3$） |
| 经典需求 | 3 阶需 6 麦 CDMA → 4 麦实现 | 6 阶超经典 UCA 界 → 4 麦实现 | 3 阶经典需 4 麦、且 2 麦不可转向 → **2 麦实现且可转向** |
| SDR 结果 | 心形均值 26.2 dB；三阶 18.4 dB（最佳模型） | 跨方向一致：一阶 ≈25.9；三阶 ≈20.2；六阶 ≈17.1 | 端射：一阶 25.93；三阶 23.24（双麦） |
| 基线对比 | LS 波束形成器（三阶失败 −5.9）、参数化基线（12.7） | — | 经典 DMA −0.99/N/A；参数化空间滤波器 13.77/10.32；**重训 NDF** 25.85/23.13 |
| 独特能力 | 首证 DNN 可学高阶 DMA 图 | 推理中转向切换；语音训练泛化到音乐 | **X-Y 立体声录音**（双模型 135°/45°，匹配 VDM 对含声道间电平差） |

## 演进主线

1. **NDF**：证明可行 — 掩码式单通道输出 + 4 麦 UCA 学 3 阶 DMA 图；
2. **SNDF**：证明可转 — 加 one-hot 条件 + 场景复用策略，单模型 360° 转向，阶数推到 6 阶；
3. **NDBF**：证明可超越经典 — 输出从掩码改为复数权重向量，几何收缩到极限（2 麦线阵），在经典完全无解（一阶不可转向）的配置下实现可转向 3 阶，且零点抑制强于掩码式的 NDF。

## Related Concepts

- [[concepts/neural-directional-filtering|Neural Directional Filtering]]
- [[concepts/steerable-neural-directional-filtering|Steerable Neural Directional Filtering]]
- [[concepts/neural-differential-beamformer|Neural Differential Beamformer]]
- [[concepts/virtual-directional-microphone|Virtual Directional Microphone]]
- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Non-Linear Filter]]

## Related Sources

- [[sources/wechsler-2024-neural-directional-filtering|Wechsler et al. 2024: Neural Directional Filtering]]
- [[sources/huang-2025-steerable-neural-directional-filtering|Huang et al. 2025: Steerable Neural Directional Filtering]]
- [[sources/huang-2026-dual-mic-steerable-neural-beamformer|Huang & Habets 2026: Dual-Microphone Steerable High-Order Neural Differential Beamformer]]
