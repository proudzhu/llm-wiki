---
type: entity
created: 2026-09-02
updated: 2026-09-02
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
- Co-authored the compressed complex MSE / consolidated time-frequency loss family (Braun & Tashev 2021) — the $L_1$ magnitude + complex-spectrogram combination used to train [[concepts/nsnet2|NSNet2]]-style suppressors, adopted by later work such as Bark-AEC and DiffVQE

## Related Sources

- [[sources/braun-2015-residual-noise-control|Braun, Kowalczyk & Habets 2015: Residual Noise Control PMWF]]
