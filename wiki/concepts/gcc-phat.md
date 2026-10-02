---
type: concept
created: 2026-10-02
updated: 2026-10-02
sources:
  - raw/papers/grinstein-2024-srp-tutorial-review/full-text.md
tags:
  - time-delay-estimation
  - sound-source-localization
  - audio-processing
  - gcc
---

# GCC-PHAT (Generalized Cross-Correlation with Phase Transform)

**GCC-PHAT** is the dominant correlation function for time-delay estimation between microphone pairs in [[concepts/sound-source-localization|sound source localization]] (originally proposed by Knapp & Carter 1976). "Generalized" refers to the pre-filtering applied per frequency component before cross-correlation; the **phase transform (PHAT)** weighting whitens the cross-spectrum — discarding magnitude information dominated by the source spectrum and room acoustics, keeping only phase — which sharpens the correlation peak and makes the delay estimate robust in reverberant environments. It is the correlation underlying [[concepts/steered-response-power|SRP-PHAT]].

## Formulation

For frequency-domain microphone frames $\bar{\mathbf{x}}_{l}(t)$ and $\bar{\mathbf{x}}_{m}(t)$:

$$\text{GCC-PHAT}(f;\bar{\mathbf{x}}_{l},\bar{\mathbf{x}}_{m})=\frac{\bar{x}_{l}(t,f)\,\bar{x}^{*}_{m}(t,f)}{|\bar{x}_{l}(t,f)|\,|\bar{x}_{m}(t,f)|},$$

computed over the analysis frequency set $\mathcal{F}$ and inverse-Fourier-transformed into a temporal correlation vector, whose peak (ideally at the pair's true time-difference of arrival, TDOA) yields the delay estimate. For broadband sources in anechoic conditions the GCC-PHAT is impulse-like; for narrowband sources it degrades to a sinc with ripples.

## Partial Whitening: GCC-PHAT$_\beta$

A parameterized family interpolates between the plain cross-correlation ($\beta=0$) and full PHAT ($\beta=1$):

$$\text{GCC-PHAT}_{\beta}(f;\bar{\mathbf{x}}_{l},\bar{\mathbf{x}}_{m})=\frac{\bar{x}_{l}(t,f)\,\bar{x}^{*}_{m}(t,f)}{|\bar{x}_{l}(t,f)\,\bar{x}^{*}_{m}(t,f)|^{\beta}+\gamma},$$

with $\gamma$ for numerical stability (one proposal sets $\gamma$ to the minimum signal coherence over all frequency bins). Surveys summarized by Grinstein et al. 2024 report an acceptable $\beta$ range of 0.65–0.7 for general signals — partial whitening is empirically more stable than the conventional $\beta=1$ — and $\beta=0.8$ for narrowband signals under directional-noise interference at low SNR.

## Variants and Replacements

- **Neural replacements**: Deep-GCC networks regress an idealized single-peak correlation (Gaussian target at the true TDOA), using GCC-PHAT or spectrogram inputs.
- **Alternative weightings and correlations**: kurtosis-based weighting, sum-of-Gaussians smoothing, multi-channel cross-correlation (MCCC), eigenvector-domain correlations, analytic-signal envelope (against sinc ripples), wavelet-based GCCs for outdoor conditions.
- The role of GCC-PHAT inside SRP: each grid candidate samples the pair's GCC at its TDOA — see [[concepts/steered-response-power|Steered-Response Power]].

## Related Concepts

- [[concepts/steered-response-power|Steered-Response Power (SRP)]]
- [[concepts/sound-source-localization|Sound Source Localization]]
- [[concepts/interaural-time-difference|Interaural Time Difference]] — the binaural special case of TDOA estimation

## Related Sources

- [[sources/grinstein-2024-srp-tutorial-review|Grinstein et al. 2024: SRP for Sound Source Localization — a Tutorial Review]] — the tutorial formulation and the partial-whitening synthesis on this page
- [[sources/kim-2014-doa-based-snr-estimation|Kim & Kim 2014: DOA-based SNR Estimation]] — uses the GCC/SRP-PHAT reliability within the target-DOA error window
