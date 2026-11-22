---
type: concept
created: 2026-11-20
updated: 2026-11-22
sources:
  - raw/papers/fu-2019-metricgan/full-text.md
  - raw/papers/abdulatif-2024-cmgan/full-text.md
tags:
  - loss-function
  - metric-optimization
  - speech-enhancement
---

# Black-Box Metric Score Optimization

**Black-box metric score optimization** is the problem of training a model to maximize a scalar evaluation metric $Q$ whose internals are unavailable or unusable — a non-differentiable function, a proprietary implementation, or simply one too complex to backpropagate through. In speech enhancement the canonical cases are **PESQ** and **STOI**, both of which involve time alignment, perceptual transforms and non-smooth operations.

[[sources/fu-2019-metricgan|Fu et al. (ICML 2019)]] give the taxonomy this page is organized around, along with an empirical baseline for each family.

## White-Box vs. Black-Box

| Family | Mechanism | Requires metric internals? | Cost |
|:-------|:----------|:---------------------------|:-----|
| **White-box** | Replace $Q$ with a hand-crafted differentiable approximation and add it as a loss term | **Yes** — a designer must know what the metric measures and how to mimic it | Cheap per step; proxy may encode the designer's wrong beliefs about $Q$ |
| **Black-box (RL)** | Treat $Q$ as a reward and use policy-gradient / evolutionary search over the model's parameters | No | Sample-inefficient; Fu et al. report the method is "very sensitive to the hyperparameters (weight initialization, step size of jitter, …)", only worked for PESQ, and had to be **pre-trained** from a supervised model |
| **Black-box (learned surrogate)** | Fit a network $D \approx Q$ from metric evaluations, then backpropagate through $D$ | No | Needs alternation between surrogate fitting and generator training; surrogate is only locally valid |

The third row is the [[concepts/metricgan|MetricGAN]] mechanism, proposed as a black-box method that keeps RL's ignorance of metric internals while inheriting gradient-based training efficiency. The surrogate does not need $Q$ to be differentiable, only **evaluable** — $Q$ appears solely as a regression target for $D$.

## Why It Is Needed

Regression losses are poor proxies for perception. An $L_p$ distance between enhanced and clean speech does not track human auditory perception or ASR accuracy, and several studies cited by the paper show a smaller $L_p$ distance does **not** guarantee higher quality or intelligibility. Two failure modes drive this:

1. **Metric disagreement with reconstruction.** Each loss optimizes its own criterion and degrades others — see the four-loss comparison in [[sources/li-2020-residual-noise-control|Li et al. 2020]] and the [[concepts/generalized-loss-function|generalized loss]] family.
2. **Conditional-mean bias.** MAE/MSE presuppose a unimodal output distribution and bias predictions toward its mean, which is not what listeners or metrics reward.

Optimizing $Q$ directly sidesteps the proxy-selection problem, at the cost of needing to evaluate $Q$ during training.

## Key Requirements

- **Evaluability, not differentiability** — the metric is called as an oracle; gradients come from the surrogate.
- **Anchoring** — Fu et al. report that removing $Q$ from the surrogate's own objective makes training fail to converge. The surrogate must be pinned to the true metric; it cannot be learned from scratch alongside the generator.
- **Local validity** — a learned surrogate approximates $Q$ only in observed regions, forcing alternating rather than joint optimization.
- **Bias inheritance** — the trained model inherits whatever $Q$ over- or under-weights. Optimizing PESQ yields PESQ-optimal artifacts (Fu et al. show this explicitly means tolerating added noise), so the choice of $Q$ is now a design decision with perceptual consequences rather than a neutral evaluation step. This is the same Goodhart's-law concern later handled by down-weighting differentiable PESQ losses to $\lambda \sim 10^{-3}$ in [[sources/ahn-2026-fastenhancer|FastEnhancer]].

## Related Concepts

- [[concepts/metricgan|MetricGAN]] — the learned-surrogate implementation
- [[concepts/pesq|PESQ]] · [[concepts/stoi|STOI]] — the metrics most often optimized this way
- [[concepts/generalized-loss-function|Generalized Loss Function]] — the white-box loss-family alternative
- [[concepts/distortion-aware-training|Distortion-aware Training]]
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/fu-2019-metricgan|Fu, Liao, Tsao & Lin 2019: MetricGAN]] — defines the taxonomy and demonstrates the learned-surrogate route
- [[sources/li-2020-residual-noise-control|Li et al. 2020: Residual Noise Control]] — evidence that $L_p$ losses disagree with listeners
- [[sources/ahn-2026-fastenhancer|Ahn et al. 2026: FastEnhancer]] — the modern counterpoint: a differentiable PESQ term deliberately weighted at $10^{-3}$
- [[sources/abdulatif-2024-cmgan|Abdulatif, Cao & Yang 2024: CMGAN]] — applies the learned-surrogate route to [[concepts/cmgan|CMGAN]] with PESQ weight 0.01 alongside spectral and waveform reconstruction. Removing the discriminator drops PESQ 3.41 → 3.24; a frozen surrogate trained without enhanced tracks also underperforms, supporting adversarial co-adaptation. PESQ+STOI and MetricGAN+ variants improve selected metrics while reducing SSNR, and an LLR-targeted dereverberation variant shifts the trade-off toward SRMR.
