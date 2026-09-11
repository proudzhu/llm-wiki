---
type: concept
created: 2026-09-11
updated: 2026-09-11
sources:
  - raw/papers/gerkmann-2012-mmse-noise-psd-tracking/full-text.md
tags:
  - speech-enhancement
  - signal-processing
  - noise-estimation
  - single-channel
---

# Decision-Directed A Priori SNR Estimation

**Decision-directed (DD) a priori SNR estimation** is the recursive estimator introduced by Ephraim & Malah ("Speech enhancement using a minimum mean-square error short-time spectral amplitude estimator", IEEE TASSP 1984), which forms the a priori SNR $\xi$ from a geometrically weighted combination of the *previous frame's estimated speech spectrum* and the *current frame's maximum-likelihood estimate*. In the wiki it appears both as an ingredient of MMSE/[[concepts/wiener-filter|Wiener]]-style spectral gain rules and as an auxiliary speech-PSD estimator inside early [[concepts/mmse-based-noise-psd-estimation|MMSE-based noise PSD tracking]].

## Formulation

With noisy DFT coefficient $Y_k(l)$, noise PSD estimate $\widehat{\sigma_{\mathrm{N},k}^2}$ and the previous frame's speech amplitude estimate $\widehat{S}_k(l-1)$:

$$\xi_k(l) = \alpha_{\mathrm{dd}}\, \frac{|\widehat{S}_k(l-1)|^{2}}{\widehat{\sigma_{\mathrm{N},k}^2}(l-1)} + (1 - \alpha_{\mathrm{dd}})\, \max\left(\gamma_k(l) - 1,\; 0\right)$$

where $\gamma_k(l) = |Y_k(l)|^2 / \widehat{\sigma_{\mathrm{N},k}^2}(l-1)$ is the a posteriori SNR, and $\alpha_{\mathrm{dd}}$ is a smoothing constant typically **0.98** (as used in Gerkmann & Hendriks 2012). The first term is the "decision-directed" part — it reuses the previous estimate, treating it as a decision — and the second is the instantaneous (biased) ML term.

Properties:

- The recursion makes $\xi$ track the speech envelope smoothly rather than the raw periodogram, drastically reducing the variance of the resulting spectral gain.
- `max(·, 0)` in the ML term floors the instantaneous contribution, which is what keeps $\xi$ from collapsing in speech pauses.
- It presupposes a noise PSD estimate $\widehat{\sigma_{\mathrm{N},k}^2}$ — a circular dependency: DD needs the noise estimate, and (in the 2010 MMSE-based noise tracker) the noise estimate needs DD. Gerkmann & Hendriks 2012 break that loop on the noise side by using a bias-analytic [[concepts/temporal-cepstrum-smoothing|TCS]] speech estimate instead, so only **one** speech PSD estimate remains in the noise tracker.

## Roles in the Wiki

- **Spectral gain rules** — the a priori SNR input of MMSE-STSA, super-Gaussian and Wiener-type gains. Gerkmann & Hendriks 2012 use $\alpha_{\mathrm{dd}} = 0.98$ to drive the super-Gaussian estimator of Erkelens et al. (2007) in their enhancement evaluation.
- **Bias compensation in MMSE-based noise PSD estimation** — in Hendriks, Heusdens & Jensen (ICASSP 2010) the DD estimate is the *second* speech PSD estimate used purely to evaluate the analytic ML bias $B(\sigma_{\mathrm{S}}^2, \sigma_{\mathrm{N}}^2)$.
- **Spatial SNR estimation** — [[concepts/doa-based-snr-estimation|DOA-based SNR estimation]] (Kim & Kim 2014) also uses decision-directed updates, there on a spatial TNR/LRT-derived estimate.

## Related Concepts

- [[concepts/mmse-based-noise-psd-estimation|MMSE-Based Noise PSD Estimation]] — used the DD estimate for bias compensation before the TCS-based variant
- [[concepts/temporal-cepstrum-smoothing|Temporal Cepstrum Smoothing (TCS)]] — the bias-analytic speech estimator that makes the DD branch unnecessary
- [[concepts/wiener-filter|Wiener Filter]] — consumes the a priori SNR
- [[concepts/minimum-statistics|Minimum Statistics]] — supplies the noise PSD that DD requires
- [[concepts/doa-based-snr-estimation|DOA-Based SNR Estimation]] — another user of decision-directed updating

## Related Sources

- [[sources/gerkmann-2012-mmse-noise-psd-tracking|Gerkmann & Hendriks 2012: Improved MMSE-Based Noise PSD Tracking Using Temporal Cepstrum Smoothing]] — uses DD with $\alpha_{\mathrm{dd}} = 0.98$ in the enhancement framework, and removes it from the noise-tracking branch
