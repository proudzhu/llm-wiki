---
type: concept
created: 2026-09-11
updated: 2026-09-11
sources:
  - raw/papers/gerkmann-2012-mmse-noise-psd-tracking/full-text.md
tags:
  - noise-estimation
  - speech-enhancement
  - power-spectral-density
  - signal-processing
  - single-channel
---

# MMSE-Based Noise PSD Estimation

**MMSE-based noise PSD estimation** tracks the noise power spectral density by computing the *minimum mean-square error estimate of the noise periodogram itself*, $\mathrm{E}\left[|N|^2 \mid y\right]$, from the noisy observation $y$ rather than by tracking spectral minima or by gating updates with a speech-presence decision. It was introduced by Hendriks, Heusdens & Jensen ("MMSE based noise PSD tracking with low complexity", ICASSP 2010) and improved by [[sources/gerkmann-2012-mmse-noise-psd-tracking|Gerkmann & Hendriks (ICASSP 2012)]], with an unbiased, low-complexity, low-delay formulation in IEEE TASLP 2012 (Hendriks, Heusdens, Jensen & Kjær).

It is the third major single-channel noise-PSD family alongside [[concepts/minimum-statistics|minimum statistics]] (spectral-minima tracking, VAD-free) and [[concepts/speech-presence-probability|SPP-based noise estimation]] (soft-decision speech-absence gating). Its selling point over MS is **faster tracking of non-stationary noise** — noise that changes within the span of one second — at the cost of requiring a speech PSD estimate to evaluate the conditional expectation.

## Estimator

Assuming complex Gaussian speech and noise DFT coefficients with variances $\sigma_{\mathrm{S}}^2$ and $\sigma_{\mathrm{N}}^2$, the conditional mean of the noise periodogram given the observed coefficient $y$ is

$$\mathrm{E}\left[|N|^2 \mid y\right] = \left(\frac{\sigma_{\mathrm{N}}^2}{\sigma_{\mathrm{N}}^2 + \sigma_{\mathrm{S}}^2}\right)^{2} |y|^{2} + \frac{\sigma_{\mathrm{S}}^2}{\sigma_{\mathrm{N}}^2 + \sigma_{\mathrm{S}}^2}\, \sigma_{\mathrm{N}}^2$$

This is a convex combination: when the a priori SNR $\xi = \sigma_{\mathrm{S}}^2/\sigma_{\mathrm{N}}^2$ is low the first term dominates and the estimate follows the observed periodogram $|y|^2$; when speech dominates, the estimate falls back to the previous noise PSD $\sigma_{\mathrm{N}}^2$.

Because both quantities on the right-hand side are unknown expected values, they must be estimated:

- **Noise PSD** — taken from the previous frame, $\widehat{\sigma_{\mathrm{N}}^2} = \widehat{\sigma_{\mathrm{N}}^2}(l-1)$, exploiting the slow frame-to-frame change of the noise.
- **Speech PSD** — the crux of the method. The original formulation uses a *limited maximum-likelihood* estimate, $\widehat{\sigma_{\mathrm{S,ML}}^2} = \max(0, |y|^2 - \widehat{\sigma_{\mathrm{N}}^2})$, which is biased; the resulting bias in $\mathrm{E}[|N|^2 \mid y]$ is computed analytically as $B(\sigma_{\mathrm{S}}^2, \sigma_{\mathrm{N}}^2)$ and requires a **second, independent** speech estimate (the [[concepts/decision-directed-a-priori-snr|decision-directed]] estimate) to be evaluated.

The corrected estimate is followed by recursive temporal smoothing:

$$\widehat{\sigma_{\mathrm{N}}^2}(l) = \alpha_{\mathrm{pow}}\, \widehat{\sigma_{\mathrm{N}}^2}(l-1) + (1 - \alpha_{\mathrm{pow}})\, \widetilde{\sigma_{\mathrm{N}}^2}, \qquad \alpha_{\mathrm{pow}} = 0.8$$

To prevent locking onto an erroneously low value, the estimate is additionally forced to be at least the minimum of the noisy periodograms of the **last 0.8 s**.

## Improvement: replacing the two-estimate speech branch with TCS

[[sources/gerkmann-2012-mmse-noise-psd-tracking|Gerkmann & Hendriks 2012]] keep the estimator above but replace *both* speech PSD estimates with a single [[concepts/temporal-cepstrum-smoothing|temporal cepstrum smoothing (TCS)]] estimate. TCS exploits the known cepstral structure of speech (low coefficients = spectral envelope, a quefrency peak = fundamental period) to suppress non-speech spectral outliers, and its residual bias is an analytic scaling $\mathcal{B} = \exp(\psi(\bar\mu) + C)/\bar\mu$ (typically 1.45–1.55).

Consequences reported by that paper:

| Property | Hendriks et al. 2010 (baseline) | Gerkmann & Hendriks 2012 (TCS) |
|---|---|---|
| Speech PSD estimates needed | 2 (limited ML + DD) | 1 (TCS) |
| Bias compensation | explicit branch, using the DD estimate | analytic scale factor $\mathcal{B}$ |
| Extra cost | — | 2 real-valued FFTs (cepstrum + inverse) |
| LogErr (noise tracking error) | baseline | lower, for both modulated Gaussian and babble noise |
| Segmental SNR gain in babble at 0 dB input SNR | baseline | ≈ 1 dB better |

## Position Among Single-Channel Noise Estimators

- **vs. [[concepts/minimum-statistics|Minimum Statistics]]** — MS tracks spectral minima and is VAD-free but responds to rising noise floors with a delay proportional to its search window; MMSE-based tracking was shown (Taghia et al., ICASSP 2011) to track quickly changing noise fields faster. In the 2012 comparison MS retains the highest segmental **speech** SNR but delivers the **lowest noise reduction**, i.e. it preserves speech by leaving noise behind; the MMSE-based estimators give the better distortion/noise-reduction trade-off (larger segmental-SNR gain).
- **vs. [[concepts/speech-presence-probability|SPP-based noise estimation]]** — SPP-based NE updates the noise estimate only where speech is absent (weighted by $1-\rho$) and therefore depends on a soft speech-presence decision; the MMSE-based estimator updates *every* frame through the conditional expectation and needs no presence decision, but does need a speech PSD estimate.

## Related Concepts

- [[concepts/temporal-cepstrum-smoothing|Temporal Cepstrum Smoothing (TCS)]] — the improved speech-PSD front end
- [[concepts/decision-directed-a-priori-snr|Decision-Directed A Priori SNR Estimation]] — the bias-compensation speech estimator the TCS variant eliminates
- [[concepts/minimum-statistics|Minimum Statistics]]
- [[concepts/speech-presence-probability|Speech Presence Probability (SPP)]]
- [[concepts/wiener-filter|Wiener Filter]] — downstream consumer of the estimated noise PSD
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/gerkmann-2012-mmse-noise-psd-tracking|Gerkmann & Hendriks 2012: Improved MMSE-Based Noise PSD Tracking Using Temporal Cepstrum Smoothing]] — replaces the two-estimate speech branch with TCS; ~1 dB segmental-SNR gain in babble noise
- [[sources/martin-2001-noise-psd-estimation-optimal-smoothing|Martin 2001: Noise PSD Estimation via Optimal Smoothing and Minimum Statistics]] — the minimum-statistics baseline used for comparison
