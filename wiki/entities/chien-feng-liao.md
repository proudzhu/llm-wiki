---
type: entity
created: 2026-11-20
updated: 2026-11-22
tags:
  - researcher
  - speech-enhancement
  - machine-learning
---

# Chien-Feng Liao

**Affiliation**: National Taiwan University & Academia Sinica, Taiwan (at the time of MetricGAN)
**Role**: Researcher
**Research Focus**: Deep learning for speech enhancement; generative models as learned loss functions; domain-adversarial training for robust speech processing.

## Key Contributions

- Co-author of **MetricGAN** — the discriminator-as-metric-surrogate formulation that trains a GAN generator directly against black-box evaluation metrics (PESQ 2.86 / CSIG 3.99 / CBAK 3.18 / COVL 3.42 on VoiceBank+DEMAND, best of six compared systems) — [[sources/fu-2019-metricgan|Fu, Liao, Tsao & Lin 2019]]
- Co-author of noise-adaptive speech enhancement using domain-adversarial training (2018), cited by MetricGAN as an application of the adversarial measurement of "realness"
- Co-first author of "Boosting Objective Scores of a Speech Enhancement Model by MetricGAN Post-processing" (APSIPA ASC 2020) — MetricGAN as a fine-tuning post-processor for a causal Transformer with convolutional positional encoding (DNS 2020: PESQ 3.104, MOS 3.21 vs NSNet 2.692 / 3.03) — [[sources/fu-2020-metricgan-post-processing|Fu et al. 2020]]

## Related Concepts

- [[concepts/metricgan|MetricGAN]]
- [[concepts/black-box-metric-optimization|Black-Box Metric Score Optimization]]

## Related Sources

- [[sources/fu-2019-metricgan|Fu, Liao, Tsao & Lin 2019: MetricGAN: Generative Adversarial Networks based Black-box Metric Scores Optimization for Speech Enhancement]]
- [[sources/fu-2020-metricgan-post-processing|Fu et al. 2020: Boosting Objective Scores by MetricGAN Post-Processing]]
