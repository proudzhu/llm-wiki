---
type: entity
created: 2026-08-03
updated: 2026-11-22
tags:
  - researcher
  - speech-enhancement
  - speech-recognition
---

# Szu-Wei Fu

**Affiliation**: NVIDIA (2026); formerly Academia Sinica, Taipei, Taiwan
**Role**: Researcher
**Research Focus**: Speech enhancement, universal speech restoration, voice conversion, speech synthesis, real-time/streaming deployment of deep learning for speech.

## Key Contributions

- Co-authored "An investigation of incorporating mamba for speech enhancement" (IEEE SLT 2024) — [[concepts/semamba|SEMamba]] — [[sources/chao-2024-mamba-speech-enhancement|Chao et al. 2024]]
- First author of "One Model, Many Latencies: Universal Speech Enhancement for Diverse Real-Time Applications" (arXiv preprint 2606.25621 (v3), 2026) — one-for-all real-time universal speech enhancement with selectable algorithmic and computational latency — [[sources/fu-2026-one-model-many-latencies|Fu et al. 2026]]
- First author of "MetricGAN: Generative Adversarial Networks based Black-box Metric Scores Optimization for Speech Enhancement" (ICML 2019) — redefined the GAN discriminator as a learned surrogate of a black-box evaluation metric, the first SE system trained directly against PESQ/STOI (PESQ 2.86 / CSIG 3.99 / CBAK 3.18 / COVL 3.42 on VoiceBank+DEMAND) — [[sources/fu-2019-metricgan|Fu, Liao, Tsao & Lin 2019]]
- Co-first author of "Boosting Objective Scores of a Speech Enhancement Model by MetricGAN Post-processing" (APSIPA ASC 2020) — turns MetricGAN into a universal post-processing stage: an $L_1$-pre-trained causal Transformer fine-tuned against a PESQ surrogate gains +0.13 PESQ at zero inference cost, beating the DNS 2020 NSNet baseline on objective scores and P.808 MOS — [[sources/fu-2020-metricgan-post-processing|Fu et al. 2020]]
- First author of "MetricGAN+ — An Improved Version of MetricGAN for Speech Enhancement" (Interspeech 2021) — three domain-knowledge training techniques (noisy-speech discriminator targets, replay buffer 0.2, learnable sigmoid mask) lift MetricGAN to PESQ 3.15 on VoiceBank+DEMAND; released in SpeechBrain — [[sources/fu-2021-metricgan-plus|Fu et al. 2021]]


## Related Sources

- [[sources/fu-2026-one-model-many-latencies|Fu et al. 2026: One Model, Many Latencies: Universal Speech Enhancement for Diverse Real-Time Applications]]
- [[sources/fu-2019-metricgan|Fu, Liao, Tsao & Lin 2019: MetricGAN — Black-Box Metric Score Optimization for Speech Enhancement]]
- [[sources/fu-2020-metricgan-post-processing|Fu et al. 2020: Boosting Objective Scores by MetricGAN Post-Processing]]
- [[sources/fu-2021-metricgan-plus|Fu et al. 2021: MetricGAN+ — An Improved Version of MetricGAN for Speech Enhancement]]
