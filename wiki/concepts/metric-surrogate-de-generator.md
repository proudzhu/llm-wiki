---
type: concept
created: 2026-11-22
updated: 2026-11-22
sources:
  - raw/papers/close-2022-metricgan-plus-minus/full-text.md
tags:
  - metric-optimization
  - gan
  - speech-enhancement
  - loss-function
  - robustness
---

# Metric-Surrogate De-Generator

The **de-generator** $\mathcal{N}$ is a third network added to the [[concepts/metricgan|MetricGAN]]/MetricGAN+ framework by [[sources/close-2022-metricgan-plus-minus|MetricGAN+/- (Close, Hain & Goetze, EUSIPCO 2022)]]: a mask estimator structurally identical to the enhancement generator, but trained to produce speech with an **assigned sub-perfect metric score** $w \in (0,1)$ instead of the perfect score 1. Its purpose is not enhancement — it manufactures *controlled degraded training data for the metric discriminator*, so the surrogate observes score regions that the training set sparsely covers.

## Motivation: Surrogate Score Coverage

A learned metric surrogate $D \approx Q'$ is only accurate on the signal distribution it was fitted on ([[concepts/black-box-metric-optimization|local validity]]). In MetricGAN+, $D$ sees clean speech ($Q'=1$), noisy inputs, and enhanced outputs that cluster near the top of the score range as $G$ improves — mid-range scores are barely observed, degrading $D$'s gradient quality in-domain and off-distribution. The de-generator fills those holes on demand.

## Formulation

$$L_{\mathcal{N}} = \mathbb{E}\big[(\mathcal{D}(\mathbf{Y}_f,\mathbf{S}_f) - w)^2\big], \qquad 0 < w < 1$$

where $y$ is $\mathcal{N}$'s masked output. The discriminator gains a fourth regression term $(\mathcal{D}(\mathbf{Y}_f,\mathbf{S}_f) - Q'(y,s))^2$; the enhancement generator's objective is unchanged. Both $\mathcal{G}$ and $\mathcal{N}$ outputs enter the shared replay buffer, effectively doubling it.

**Choosing $w$**: target sparsely populated $Q'$ values in the dataset. Best result at $w = 0.5$ (normalized PESQ ≈ raw PESQ 3): VoiceBank+DEMAND PESQ 3.05 → **3.22**. Even $w = 1$ improves over the baseline (3.20) — attributed to output diversity between the two generators plus the larger buffer, so coverage widening is not the only mechanism.

## Lineage: Score Assignment Repurposed

This is [[sources/fu-2019-metricgan|MetricGAN (2019)]]'s score-assignment experiment turned from analysis into training machinery: there, driving $s<1$ revealed *what a metric measures* (PESQ-down adds noise; STOI-down deletes speech); here, the same controllability *generates the surrogate's curriculum*. The de-generator inherits the cheapest-degradation property, which cuts both ways — the paper's ~400 Hz residual-energy artefact is **worsened** by $\mathcal{N}$'s influence on $D$ (lower CBAK), i.e. widening coverage can also teach the surrogate to tolerate artefacts.

## Evidence and Limits

- Out-of-domain gain (VBD-trained, CHiME-3 test): PESQ 1.54 → 1.76 (real), 2.14 → 2.38 (simulated) — the metric-surrogate line's first explicit unseen-environment result.
- Buffer-size control: baseline MetricGAN+ at `history_portion` 0.4 reaches 3.17, recovering most of the gain — and **refuting MetricGAN+'s reported saturation above 0.2**.
- Benefit demonstrated for PESQ only; STOI-objective variants stay flat (0.933 vs 0.934).
- Costs: a second generator to train and a doubled replay buffer; structure/clamp copied from $\mathcal{G}$ without ablation (future work).

## Related Concepts

- [[concepts/metricgan|MetricGAN]] — the framework; score assignment is the mechanism reused
- [[concepts/black-box-metric-optimization|Black-Box Metric Score Optimization]] — coverage as a first-class surrogate requirement
- [[concepts/learnable-sigmoid-mask|Learnable Sigmoid Mask]] — the mask head $\mathcal{N}$ shares with $\mathcal{G}$
- [[concepts/pesq|PESQ]] · [[concepts/stoi|STOI]] — the metrics used as $Q$

## Related Sources

- [[sources/close-2022-metricgan-plus-minus|Close, Hain & Goetze 2022: MetricGAN+/-]] — the originating paper
- [[sources/fu-2019-metricgan|Fu, Liao, Tsao & Lin 2019: MetricGAN]] — the score-assignment degrader this repurposes
- [[sources/fu-2021-metricgan-plus|Fu et al. 2021: MetricGAN+]] — the baseline whose buffer-saturation claim is refuted
