---
type: concept
created: 2026-10-24
updated: 2026-10-24
sources:
  - raw/papers/mezza-2024-hybrid-plc/full-text.md
tags:
  - evaluation-metric
  - packet-loss-concealment
  - speech-quality
  - neural-network
---

# PLCMOS

**PLCMOS** is a convolutional-recurrent neural estimator of the Mean Opinion Score that human listeners would give audio degraded by packet loss. It was developed for the **INTERSPEECH 2022 Audio Deep Packet Loss Concealment Challenge** (Diener, Sootla, Branets, Saabas, Aichner & Cutler) and is now the de facto objective proxy for [[concepts/packet-loss-concealment|PLC]] quality, used both as a benchmark metric and as a training/selection objective.

## Properties

- **Output range** 1–5, intended to estimate MOS per ITU-T Rec. P.808-style crowdsourced listening.
- **Input rate** 16 kHz, scored over non-overlapping 10-second windows and averaged.
- **Trained on speech only** — its feature space and MOS mapping encode speech impairments (warble, buzz, dropouts) rather than musical ones.
- **Threshold convention**: scores above 2.0 correspond to what P.808 calls better-than-"poor" listening quality.

## Caveats Outside Speech

Because PLCMOS learned speech-degradation statistics, applying it to **music** is an extrapolation. [[sources/mezza-2024-hybrid-plc|Mezza et al. 2024]] retrain/apply it at 16 kHz on 32 kHz piano material and find it still tracks listener judgments remarkably well ($r=0.899$ against MUSHRA, $P=2.3\times10^{-3}$), though closer inspection shows ranking subtleties: several feed-forward baselines whose packets click audibly score *above* what their MUSHRA scores suggest. Related work has documented the same divergence at full band, where PLCMOS (≤8 kHz) and full-band metrics such as log-spectral distance tell opposite stories about the same system pair.

## Related Concepts

- [[concepts/packet-loss-concealment|Packet Loss Concealment]]
- [[concepts/pesq|PESQ]] — classical speech quality metric
- [[concepts/peaq|PEAQ]] — perceptual audio quality metric for music/codecs
- [[concepts/mushra-listening-test|MUSHRA Listening Test]] — the subjective arbiter PLCMOS is compared against

## Related Sources

- [[sources/mezza-2024-hybrid-plc|Mezza, Amerena, Bernardini & Sarti 2024]] — PLCMOS applied to 32 kHz piano PLC; PARCnet is the only method above 2.0; $r=0.899$ vs. MUSHRA
- [[sources/valin-2022-real-time-plc|Valin et al. 2022]] — PLCMOS as a challenge metric and model-selection aid
- [[sources/nguyen-2023-predictive-plc|Nguyen, Nguyen & Khong 2023]] — PLCMOS reported alongside full-band LSD, exposing its ≤8 kHz band limit
