---
type: query
created: 2026-10-17
updated: 2026-10-17
sources:
  - raw/papers/maeda-1999-anc-simultaneous-perturbation/full-text.md
  - https://doi.org/10.1002/ecjc.10112
  - https://doi.org/10.1109/ICASSP.2003.1200036
tags:
  - active-noise-control
  - secondary-path
  - gradient-free-optimization
  - simultaneous-perturbation
---

# 扰动 ANC 算法对比：Maeda & Yoshida 1999 (SP/TDSP) vs Kajikawa & Nomura 2000–2003 (FDSP/变扰动/FDTDSP)

> 问题：Maeda & Yoshida 1999 的 SP 方法与后续 Kajikawa & Nomura 2000–2003 的扰动 ANC 方法在算法细节上的主要区别是什么？

## 结论速览

两者共享同一核心思想（对控制滤波器系数加随机扰动、只用误差传声器"测量"梯度，从而完全绕开次级通路模型），但在**优化域、梯度信息量、扰动结构和扰动幅度调度**四个算法细节上有本质区别。Kajikawa 系列并非 Maeda 1999 的简单后续——两条线在关西大学校内**平行发展**（Maeda & Yoshida, ACTIVE 99, 1999-12；Kajikawa & Nomura, IEICE J82-A 1999 / ISCAS 2000），Maeda 论文致谢中与 Kajikawa、Nomura 的讨论印证了这一点。

## 逐项对比

| 维度 | Maeda & Yoshida 1999 (SP / TDSP) | Kajikawa–Nomura 系列 2000–2003 (FDSP → 变扰动 → FDTDSP) |
|------|----------------------------------|--------------------------------------------------------|
| **优化域** | 时域；目标 $J(\boldsymbol{w})=\sum_{k=1}^{\lambda}e^2(k)$ 是一个**标量**（整块误差功率之和） | 频域；误差块做 FFT，$\mathrm{diag}[E^*]E$ 给出**每个频率 bin 的误差功率**（Kajikawa & Nomura 2001, IEICE E84-A） |
| **每次更新的梯度信息量** | 1 个标量差分 $J(\boldsymbol{w}+c\boldsymbol{s})-J(\boldsymbol{w})$，所有系数共享，仅靠随机符号 $s_i$ 区分 | N 个独立复数梯度分量（每个 bin 一个），一次 block 处理即得整条梯度向量 |
| **扰动结构** | 实数符号向量 $\boldsymbol{s}\in\{\pm1\}^n$，标量幅度 $c$ 加到所有时域 tap | 频域**复数**符号向量，实部/虚部独立取 $\pm1$（每个 bin 的幅度相位同时被随机扰动） |
| **扰动幅度** | 固定 $c$ | **可变**：Mori 期刊版（Electron. Commun. Jpn.）报告 $c=0.08$ 时收敛提速 >50 倍 |
| **每次更新的测量数** | SP 需 2 个 block；TDSP 需 1 个（时间差分 $J(\boldsymbol{w}_t)-J(\boldsymbol{w}_{t-1})$，含 $\pm\Delta w_{\max}$ 截断） | FDSP（ICASSP 2003）：扰动滤波器**半块叠加、半块移除**，扰动/未扰动两个误差向量在同一个 block 内测得，每块更新一次；后续 FDTDSP：扰动常叠加，改用相邻块时间差分（单测量） |
| **实验/性能** | 5-tap FIR、200 Hz 正弦、TMS320C30 管道实验：SP ~25 dB、TDSP ~15 dB | 仿真为主（128-tap、白噪声、fs 2 kHz、S/N 20 dB）；ICASSP 版：步长可大 ~75×（$\mu=6.0\times10^{-5}$ vs $8.0\times10^{-7}$），300k 样本处次级通路突变后快速恢复；计算量 $2N^2+34N+16N\log_2N+4$，约为 FxLMS（$6N^2+2N$）的 1/3 |

## 最本质的区别：标量差分 vs 逐 bin 梯度

Maeda 方法的核心瓶颈在于目标函数是整块误差功率——**一个标量**。一次扰动实验只能测得一个数，第 $i$ 个系数的"梯度估计" $\Delta w_t^i = \frac{J(\boldsymbol{w}+c\boldsymbol{s})-J(\boldsymbol{w})}{c}s_t^i$ 中所有系数共享同一差分值，信息量仅相当于一次测量。这正是它收敛慢、且噪声频率越高收敛越慢的结构性原因（Tokoro et al. 2006 明确指出该缺陷）。

FDSP（frequency-domain simultaneous perturbation，Kajikawa & Nomura 2001）把误差信号变换到频域后，逐 bin 构造梯度估计。以 FDTDSP 的多通道更新式为例（Ninagawa, Kajikawa & Nomura）：

$$
\boldsymbol{w}_{lj,n+1}=\boldsymbol{w}_{lj,n}-\mu\Delta\boldsymbol{w}_{lj,n},\qquad
\Delta\boldsymbol{w}_{lj,n}=\mathrm{IFFT}\text{ 前 }N\text{ 点}\big[U_{lj,n}\big]
$$

$$
U_{lj,n}=\mathrm{diag}[\boldsymbol{S}_{lj,n}]\cdot\sum_{m=1}^{M}\frac{\mathrm{diag}[\boldsymbol{E}^*_{m,n}]\boldsymbol{E}_{m,n}-\mathrm{diag}[\boldsymbol{E}^*_{m,n-1}]\boldsymbol{E}_{m,n-1}}{c_n}
$$

其中 $\boldsymbol{E}_{m,n}$ 是误差块的 FFT，$\boldsymbol{S}_{lj,n}$ 是复数符号向量（实虚部独立 $\pm1$），$c_n$ 是可变扰动幅度。依赖频域自适应滤波特有的逐 bin 解耦近似，**一次 block 测量得到 N 个独立梯度分量**——这是收敛速度数量级提升的根本原因。

## 变扰动幅度调度（Mori, Kajikawa & Nomura 2003）

固定小 $c$ 时收敛极慢；固定大 $c$ 时扰动本身注入的可听噪声增大且 block 处理会不稳定。变扰动方案按误差大小自适应调节：误差大时 $c$ 大（远离最优点，快速逼近），误差小时 $c$ 小（接近最优点，精收敛 + 抑制扰动噪声），Mori 期刊版报告在 $c=0.08$ 场景下收敛提速 50 倍以上。这一思路与变步长 LMS 的调度逻辑同构（参见 [[queries/adaptive-filtering-variable-step-size-algorithms|变步长自适应滤波综述]]），只是把调度对象从步长换成了扰动幅度。

## FDTDSP 的组合逻辑

Mori/Kajikawa/Nomura 2002–2003 的 FDTDSP = **FDSP（频域逐 bin 梯度）+ 变扰动（$c_n$ 调度）+ TDSP（时间差分，单测量）**，即同时吸收了 Maeda 一系的单测量思想与 Kajikawa 一系的频域化、变扰动改进。后续 Tokoro et al.（2006/2007）进一步修补频域化的遗留问题：考虑次级通路频率特性的**加权更新**（次级通路频响凹陷处标量扰动无法逐频点适配导致性能恶化）与频域变扰动控制。

## 谱系澄清

- **平行而非继承**：Kajikawa & Nomura 的"无次级通路模型 ANC"日文版（IEICE Trans. J82-A）与 Maeda & Yoshida（ACTIVE 99，1999 年 12 月）几乎同期，英文版发表于 ISCAS 2000（pp. 349–352）。两线同属关西大学（Maeda：电气工程系，神经控制背景；Kajikawa/Nomura：电子工程系，信号处理背景）。
- **演化主干在 Kajikawa 一线**：2001 频域化（IEICE E84-A）→ 2003 变扰动（Mori 等, Electron. Commun. Jpn.; Kajikawa & Nomura, ICASSP 2003）→ FDTDSP → Tokoro 2007 稳定性改进。
- **与联立方程法的关系**：Fujii 一系（关西大学同校）的 [[concepts/simultaneous-equations-method|联立方程法]] 同期也在规避次级通路估计，但走代数求解路线而非随机梯度测量路线。

## Related Pages

- [[concepts/simultaneous-perturbation|Simultaneous Perturbation]]
- [[sources/maeda-1999-anc-simultaneous-perturbation|Maeda & Yoshida 1999: ANC Using Simultaneous Perturbation]]
- [[synthesis/secondary-path-modeling-evolution|Secondary Path Modeling: From Offline Identification to Model-Free Evolution]]
- [[queries/how-to-estimate-secondary-path|如何估计次级通道]]
- [[concepts/frequency-domain-anc|Frequency Domain ANC]]
