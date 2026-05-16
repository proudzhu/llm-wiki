---
type: query
created: 2026-04-10
updated: 2026-04-10
sources:
tags:
  - anc
  - adaptive-feedback
  - overview
---

# 什么是 Simplified Adaptive Feedback ANC

**Question**: 介绍下 Simplified Adaptive Feedback ANC

## Summary

SimpAFB 是 Wu, Qiu, Guo (2014) 提出的一种主动噪声控制（ANC）架构，核心创新是用 **误差信号直接作为参考信号**，消除了传统 IMC-based 系统中昂贵的卷积运算。

## Core Idea

```
SimpAFB:    X_sa(z) = E(z)              ← 零额外运算
IMC-based:  X(z)  = E(z) - Ŝ(z)·Y(z)    ← 需要卷积运算
```

## Why This Simplification Works

1. **实际 ANC 系统永远做不到完美消除** — 通常只有 ~10 dB 衰减，误差信号始终含有原始噪声成分
2. **自适应初期衰减小** — 刚开始收敛时，误差信号 ≈ 原始噪声
3. **次级路径估计本就不准** — 实际中 Ŝ(z) ≠ S(z)，IMC 合成的参考信号质量跟直接用误差信号差不多

## Closed-Loop Transfer Function

```
H_sa(z) = E(z)/D(z) = 1 / [1 - S(z)·W_sa(z)]
```

等价于非自适应反馈系统的传递函数 — SimpAFB 就是它的 **自适应版本**。

## Stability Condition

```
|∠S(e^jω) - ∠[1 - S(e^jω)·W_sa(e^jω)] - ∠Ŝ(e^jω)| < π/2,  ∀ω
```

比 IMC 系统更严格，多出的 `∠[1 - S(e^jω)·W_sa(e^jω)]` 项意味着滤波器本身影响稳定性。

**解决方案**：使用 [[concepts/leaky-fxlms-algorithm|Leaky FxLMS Algorithm]] 限制滤波器增益增长，防止发散。

## Performance

| 次级路径估计 | SimpAFB | IMC-based | 差距 |
|-------------|---------|-----------|------|
| 完美 Ŝ(z) | ~10 dB | ~15 dB | 5 dB |
| 小误差 | 相当 | 相当 | ~2 dB |
| 大误差 | 相当 | 相当 | ~2 dB |

关键点：实际应用中次级路径估计总有误差，此时两者差距仅 ~2 dB。

## Experimental Results

- 200 cm 管道，TMS320C6747 DSP, 16 kHz
- **250–300 Hz 窄带噪声** → ~10 dB 降噪
- **250–350 Hz 窄带噪声** → ~7 dB 降噪（带宽越宽，可预测性越低）

## Three-Way Comparison

| 架构 | 性能 | 优点 | 缺点 |
|------|------|------|------|
| **SimpAFB** | 好 | 自适应、低计算量、易实现 | 稳定性较弱 |
| **IMC-based** | 最好 | 自适应、稳定性好、降噪强 | 计算量大、不能直接用商用控制器 |
| **非自适应** | 一般 | 低成本、结构简单 | 不自适应、设计复杂 |

## Implementation

可以直接用市售的 FxLMS 自适应前馈 ANC 控制器 — 只需把误差传感器输出连到参考输入端，**不需要改动硬件或软件架构**。

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/internal-model-control|Internal Model Control]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/leaky-fxlms-algorithm|Leaky FxLMS Algorithm]]
- [[concepts/simplified-adaptive-feedback-anc|Simplified Adaptive Feedback ANC]]

## Related Sources

- [[sources/wu-2014-simplified-adaptive-feedback-anc|Wu 2014: Simplified Adaptive Feedback ANC]] — Original paper
