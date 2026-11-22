---
type: concept
created: 2026-11-20
updated: 2026-11-22
sources:
  - raw/papers/dang-2022-dpt-fsnet/full-text.md
  - raw/papers/fu-2019-metricgan/full-text.md
  - raw/papers/abdulatif-2024-cmgan/full-text.md
  - raw/papers/fu-2020-metricgan-post-processing/full-text.md
  - raw/papers/fu-2021-metricgan-plus/full-text.md
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

The scheme became a standard recipe in speech enhancement: **MetricGAN+** (Fu et al., Interspeech 2021) is the direct successor and a benchmark fixture (PESQ 3.15 on VoiceBank+DEMAND), and the "MetricGAN-style discriminator that predicts PESQ scaled to (0,1)" recurs in later systems such as [[concepts/lisennet|LiSenNet]] and [[concepts/cmgan|CMGAN]] — where it appears as an *added* loss term alongside reconstruction losses rather than as the sole generator objective of the original. The weight is system-specific: LiSenNet uses 0.05, whereas [[sources/abdulatif-2024-cmgan|Abdulatif, Cao & Yang 2024]] give CMGAN's $\mathcal L_{GAN}$ weight as **0.01**. Removing CMGAN's discriminator reduces PESQ from 3.41 to 3.24; replacing PESQ with normalized LLR for dereverberation improves SRMR but trades away CD/FWSegSNR performance.

**The MetricGAN+ revision** ([[sources/fu-2021-metricgan-plus|Fu et al., Interspeech 2021]]) keeps both objectives verbatim and improves *what the discriminator is fitted on* plus the mask head: (1) noisy-speech regression targets $(D(x,y) - Q'(x,y))^2$ added to $L_D$ (adopted from Kawanaka et al., ICASSP 2020), anchoring the surrogate at the low-quality end; (2) the experience-replay `history_portion` raised 0.1 → 0.2 — the buffer is load-bearing, since without it PESQ collapses to 2.82 (catastrophic forgetting of previously generated speech makes $D$'s gradient a poor proxy for $Q$'s); (3) a [[concepts/learnable-sigmoid-mask|learnable sigmoid]] mask head ($\beta = 1.2$, per-bin $\alpha$). With input normalization also removed, the cumulative ablation runs 2.86 → 2.95 → 3.02 → 3.05 → **3.15** PESQ on VoiceBank+DEMAND at an unchanged BLSTM backbone. Its discriminator is a smaller uniform CNN (4 × 15 filters, 5×5 kernels, global pooling to 15 features) than the original's growing 15→50 stack. Released in SpeechBrain, this is the recipe most later "MetricGAN-style" losses descend from.

**As a post-processing module** ([[sources/fu-2020-metricgan-post-processing|Fu et al., APSIPA ASC 2020]]): instead of training from scratch, an SE model is pre-trained with $L_1$/$L_2$ to convergence and *then* fine-tuned against the surrogate, using the stable-training techniques of Kawanaka et al. (ICASSP 2020). The paper demonstrates this on a causal Transformer generator (after the original's BLSTM and Kawanaka's convolutional BLSTM), arguing the framework is generator-agnostic: DNS-2020 PESQ rises 2.966 → 3.104 with **unchanged parameters and inference time**, since only weights are fine-tuned. Its discriminator here is a spectrally-normalized 4-layer CNN "Quality-Net" (not the original BLSTM), and it warns that PESQ/STOI surrogates can induce high-frequency noise — both metrics ignore high-frequency differences — recommending the post-processing for mask-estimation models over direct spectral mapping.

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
- [[sources/dang-2022-dpt-fsnet|Dang, Chen & Zhang 2022: DPT-FSNet]] — discriminative counterpoint on VoiceBank+DEMAND: a dual-domain reconstruction loss (waveform MSE + RI-magnitude L1, no discriminator) reaches PESQ 3.33 vs MetricGAN's 2.86, at 0.88 M params
- [[sources/fu-2020-metricgan-post-processing|Fu et al. 2020: MetricGAN Post-Processing]] — converts the framework into a post-hoc fine-tuning stage for a converged causal Transformer (DNS 2020: +0.138 PESQ at zero inference-cost change), with a CNN Quality-Net discriminator
- [[sources/fu-2021-metricgan-plus|Fu et al. 2021: MetricGAN+]] — the direct successor: noisy-speech $D$ targets, replay 0.2, learnable sigmoid mask; PESQ 2.86 → 3.15 on VoiceBank+DEMAND, released in SpeechBrain
