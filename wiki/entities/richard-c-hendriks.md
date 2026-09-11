---
type: entity
created: 2026-09-11
updated: 2026-09-11
tags:
  - researcher
  - speech-enhancement
  - noise-estimation
  - single-channel
  - statistical-signal-processing
---

# Richard C. Hendriks

**Affiliation**: Signal and Information Processing Lab, Delft University of Technology, The Netherlands
**Role**: Researcher (associate professor, Delft University of Technology)
**Research Focus**: Single-channel and multi-microphone speech enhancement, noise PSD estimation and tracking, MMSE-based statistical estimators, speech intelligibility prediction and enhancement for hearing-impaired listeners.

## Key Contributions

- Co-author of "Improved mmse-based noise PSD tracking using temporal cepstrum smoothing" (ICASSP 2012) — [[sources/gerkmann-2012-mmse-noise-psd-tracking|Gerkmann & Hendriks 2012]]. Replaced the limited-ML + decision-directed speech-PSD pair of the MMSE-based noise tracker with a single temporal-cepstrum-smoothing estimate, removing the explicit bias-compensation branch and improving noise tracking in babble noise by ~1 dB segmental SNR at 0 dB input SNR.
- Co-author of "MMSE based noise PSD tracking with low complexity" (ICASSP 2010, with R. Heusdens and J. Jensen) [1] — the baseline estimator this wiki's ICASSP 2012 page revisits; it computes the conditional noise-periodogram expectation $\mathrm{E}[|N|^2 \mid y]$ and tracks quickly changing noise faster than minimum-statistics approaches.
- Co-author of "Minimum mean-square error estimation of discrete Fourier coefficients with generalized Gamma priors" (IEEE TASLP 2007, with J. S. Erkelens, R. Heusdens and J. Jensen) [10] — the super-Gaussian spectral amplitude estimator used as the enhancement framework in the 2012 evaluation.
