---
type: concept
created: 2026-08-30
updated: 2026-08-30
sources:
  - raw/papers/yan-2014-dual-mic-bt-noise-reduction/full-text.md
tags:
  - speech-enhancement
  - multi-channel
  - speech-distortion
  - wiener-filter
---

# Speech-Distortion-Constrained Noise Reduction

**Category**: 多通道降噪的最优滤波理论框架

## Definition

从**约束语音损伤**的角度分析多通道降噪的最优解：以第一传声器为参考估计语音，将误差信号分解为语音失真部分 $\varepsilon_x(\omega) = (\boldsymbol{H} - \boldsymbol{u})^{\mathrm{H}}\boldsymbol{X}(\omega)$ 与残留噪声部分 $\varepsilon_v(\omega) = \boldsymbol{H}^{\mathrm{H}}\boldsymbol{V}(\omega)$（$\boldsymbol{u} = [1, 0]^{\mathrm{T}}$），在语音失真能量受限的条件下最小化残留噪声能量：

$$\boldsymbol{h}_{\text{optim}} = \arg\min_{\boldsymbol{h}} \mathrm{E}\{|\varepsilon_v(\omega)|^2\}, \quad \text{s.t. } \mathrm{E}\{|\varepsilon_x(\omega)|^2\} \leqslant \sigma^2(\omega)$$

由拉格朗日乘数法得到闭式解（Chen / Souden & Benesty）：

$$\boldsymbol{h}_{\text{optim}} = \left[\Phi_{xx}(\omega) + \beta \Phi_{vv}(\omega)\right]^{-1} \Phi_{xx}(\omega) \boldsymbol{u}$$

其中 $\Phi_{aa} = \mathrm{E}\{\boldsymbol{a}\boldsymbol{a}^{\mathrm{H}}\}$ 为空间协方差矩阵，$\beta$ 为由失真阈值 $\sigma(\omega)$ 决定的权重因子。

## β 权衡

- $\beta$ 越高 → 降噪量（NR）越大，语音失真（SD）越厉害；$\beta \to \infty$ 趋向零失真约束。
- **特例统一**：TF-GSC 对应 $\mathrm{E}\{|\varepsilon_x|^2\} = 0$ 约束；SDW-MWF 最小化加权误差 $\mathrm{E}\{|\varepsilon_v|^2\} + \mu\mathrm{E}\{|\varepsilon_x|^2\}$；GSC 失配时相当于 $\beta = 1$。
- 该框架是 [[concepts/multi-channel-wiener-filter|MWF]]（$\beta = \mu = 1$）的一般化，也与 [[concepts/variable-span-linear-filter|VSLF]] 的 tradeoff 参数同源。

## 实际实现难点

$\Phi_{vv}$ 可在语音间歇段估计，但 $\Phi_{xx} = \Phi_{yy} - \Phi_{vv}$ 中两项不在同一时段估计，噪声非平稳性越高越难估计准确——这是实际算法逼近理论最优解的主要障碍，也是约束语音损伤在实践中难以精确实现的原因。完美降噪与语音无损相互牵制，实用算法（如 [[concepts/atf-gsc|ATF-GSC]]）通过放松约束换取综合性能。

## Related Concepts

- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/wiener-filter|Wiener Filter]]
- [[concepts/gsc-beamformer|GSC]]
- [[concepts/atf-gsc|ATF-GSC]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/variable-span-linear-filter|Variable Span Linear Filter]]

## Related Sources

- [[sources/yan-2014-dual-mic-bt-noise-reduction|Yan, Qiu & Lu 2014]] — 以该框架统一两类双传声器算法并对比实验
