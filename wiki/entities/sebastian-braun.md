---
type: entity
created: 2026-09-02
updated: 2026-11-21
tags:
  - researcher
  - speech-enhancement
  - multi-channel
  - wiener-filter
  - deep-learning
---

# Sebastian Braun

**Affiliation**: International Audio Laboratories Erlangen, Erlangen, Germany (2015); later Microsoft (Redmond, WA, USA)
**Role**: Researcher
**Research Focus**: Multichannel speech enhancement and Wiener-filter theory; later low-complexity neural noise suppression, dereverberation, and loss functions for speech enhancement.

## Key Contributions

- First author of "Residual Noise Control Using a Parametric Multichannel Wiener Filter" (ICASSP 2015) — generalized [[concepts/parametric-multi-channel-wiener-filter|PMWF]] that directly controls maximum noise reduction via target-signal redefinition, without the rank-one assumption — [[sources/braun-2015-residual-noise-control|Braun, Kowalczyk & Habets 2015]]
- Co-authored "Linear Prediction-Based Online Dereverberation and Noise Reduction Using Alternating Kalman Filters" (IEEE TASLP 2018) — two alternating KFs iterating speech estimation and multichannel autoregressive reverberation-model updates to break circular dereverberation/noise-reduction dependencies (cited in [[synthesis/kalman-filter-theory-and-application|Kalman filter theory and application]])
- Co-authored [[concepts/nsnet2|NSNet2]] (Braun & Tashev, Speech and Computer 2020) — lightweight fully-connected + recurrent architecture that became a standard baseline and postfilter backbone for low-complexity speech enhancement
- First author of "A Consolidated View of Loss Functions for Supervised Deep Learning-Based Speech Enhancement" (TSP 2021, pp. 72–76) — controlled comparison of 17 spectral training losses on one 2.8 M FF+GRU gain predictor over reverberant CHiME-2 data: magnitude+complex mixtures always help even when the phase is never estimated, power-law-compressed losses lead (PESQ 3.31 vs. 3.17 for mixed MSE), and phase-sensitive SI-SDR gains require linear-domain losses (MAE 9.75 dB); origin of the compressed complex MSE / consolidated TF loss adopted by Bark-AEC, DiffVQE, tPLCnet, and LiSenNet — [[sources/braun-2021-loss-functions-speech-enhancement|Braun & Tashev 2021]]

## Related Sources

- [[sources/braun-2015-residual-noise-control|Braun, Kowalczyk & Habets 2015: Residual Noise Control PMWF]]
- [[sources/braun-2021-loss-functions-speech-enhancement|Braun & Tashev 2021: A Consolidated View of Loss Functions for Supervised Deep Learning-Based Speech Enhancement]]
