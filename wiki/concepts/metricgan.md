---
type: concept
created: 2026-11-20
updated: 2026-11-20
sources:
  - raw/papers/fu-2019-metricgan/full-text.md
tags:
  - speech-enhancement
  - gan
  - loss-function
  - metric-optimization
---

# MetricGAN

**MetricGAN** is a conditional-GAN training scheme in which the **discriminator is a learned surrogate of a black-box evaluation metric** rather than a real/fake classifier. Introduced by [[entities/szu-wei-fu|Fu]], [[entities/chien-feng-liao|Liao]], [[entities/yu-tsao|Tsao]] & [[entities/shou-de-lin|Lin]] ([[sources/fu-2019-metricgan|ICML 2019]]), it turns the evaluation metric itself — PESQ, STOI, or any other scalar function — into the generator's training objective without requiring any knowledge of the metric's internals.

## Core Idea

Conventional [[concepts/least-squares-gan|conditional GAN]] training labels generated data `0` (fake) and real data `1`, so $D$ learns a *decision boundary* that need not correlate with any evaluation metric. MetricGAN replaces those labels with the metric value: $D$ is trained to **regress** the score, and $G$ is trained to make that score as high as specified.

$$L_{D} = \mathbb{E}_{\mathbf{x},\mathbf{y}}\big[(D(\mathbf{y},\mathbf{y}) - 1)^2 + (D(G(\mathbf{x}),\mathbf{y}) - Q'(G(\mathbf{x}),\mathbf{y}))^2\big]$$

$$L_{G} = \mathbb{E}_{\mathbf{x}}\big[(D(G(\mathbf{x}),\mathbf{y}) - s)^2\big]$$

with $Q'$ the metric normalized to $[0,1]$ (1 = best) and $s$ the **assigned target score**. Two structural differences from CGAN, both deliberate:

| Aspect | CGAN | MetricGAN |
|:-------|:-----|:----------|
| Label of generated data | constant 0 (fake) | the metric score $Q'(G(\mathbf{x}),\mathbf{y})$ |
| Conditioning input of $D$ | noisy $\mathbf{x}$ | **clean $\mathbf{y}$** — matching $Q$'s input signature |
| $D$'s output space | discrete (real/fake) | **continuous** (metric-valued) |
| Generator objective | adversarial + $L_p$ | surrogate only — **no $L_p$ term** |

The clean-signal conditioning is a direct consequence of wanting $D \approx Q$: since $Q$ compares a signal against its clean reference, $D$ must receive the same arguments.

## Why the Continuous Label Space Matters

Because the label is a metric value rather than a bit, the same trained system is both an enhancer and a controllable generator:

- $s = 1$ → clean-speech generation (the standard SE operating point).
- $s < 1$ → **speech degradation**, and the way the generator achieves the lower score reveals what the metric actually measures. Fu et al. use this to separate PESQ from STOI: driving STOI down deletes speech components, whereas driving PESQ down *adds noise* — evidence that STOI scores intelligibility (speech content) and PESQ scores quality (noise). The generator tends toward the cheapest degradation consistent with the target, so the experiment is informative precisely because the objective is underdetermined.

Multiple metrics are handled with one discriminator each; per iteration only the metric with the largest shortfall trains $G$, while all discriminators keep training toward their own metric. Unachievable target tuples do not converge, since the per-metric requirements act as constraints.

## Requirements and Failure Modes

- **$Q$ must match the evaluation metric.** A mismatched surrogate yields sub-optimal scores; the paper reports that **without $Q$ the training does not converge at all** — the surrogate needs a true-metric anchor and cannot bootstrap.
- **The surrogate is locally valid.** $D$ approximates $Q$ only in the region of spectrogram space it has observed, so $G$ and $D$ must be trained alternately to convergence rather than in a single pass.
- **It inherits the metric's biases.** Optimizing PESQ gives the most PESQ-like output, which the score-assignment experiment shows means tolerating added noise.

## Downstream Adoption

The scheme became a standard recipe in speech enhancement: **MetricGAN+** (Fu et al., Interspeech 2021) is the direct successor and a benchmark fixture (PESQ 3.15 on VoiceBank+DEMAND), and the "MetricGAN-style discriminator that predicts PESQ scaled to (0,1)" recurs in later systems such as [[concepts/lisennet|LiSenNet]] and the CMGAN line — where it appears as an *added* loss term alongside reconstruction losses, $\lambda \approx 0.05$, rather than as the sole generator objective of the original.

## Related Concepts

- [[concepts/black-box-metric-optimization|Black-Box Metric Score Optimization]] — the general framing this method belongs to
- [[concepts/least-squares-gan|Least-Squares GAN (LSGAN)]] — the loss form permitting continuous targets
- [[concepts/pesq|PESQ]] · [[concepts/stoi|STOI]] — the metrics optimized in the original work
- [[concepts/segan|SEGAN]] — the adversarial-SE predecessor whose inert adversarial term motivated MetricGAN
- [[concepts/learnable-sigmoid-mask|Learnable Sigmoid Mask]] — a MetricGAN+ contribution
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/fu-2019-metricgan|Fu, Liao, Tsao & Lin 2019: MetricGAN]] — the original paper
- [[sources/pascual-2017-segan|Pascual, Bonafonte & Serrà 2017: SEGAN]] — the CGAN-for-SE formulation MetricGAN modifies
