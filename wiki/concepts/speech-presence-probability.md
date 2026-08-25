---
type: concept
created: 2026-08-15
updated: 2026-08-25
sources:
  - raw/papers/jin-2017-multichannel-noise-reduction-mobile/full-text.md
  - raw/papers/bagheri-2019-pmwf-spp/full-text.md
tags:
  - noise-estimation
  - speech-enhancement
  - voice-activity-detection
  - signal-processing
---

# Speech Presence Probability (SPP)

**Speech Presence Probability (SPP)** is a soft-decision voice activity detector that estimates, per time-frequency bin, the probability $\rho(\tau, \omega) \in [0, 1]$ that the desired speech signal is present in a noisy observation. SPP replaces the binary speech/pause decision of classical [[concepts/voice-activity-detection|VAD]] with a continuous confidence value, enabling smoother and more robust noise PSD estimation. The widely used formulation of Gerkmann & Hendriks (2011) [7] is the SPP variant employed by [[sources/jin-2017-multichannel-noise-reduction-mobile|Jin et al. 2017]] as the low-frequency stage of their [[concepts/adaptive-coherence-noise-estimation|adaptive coherence NE]] and as the speech-absence gate for coherence/covariance adaptation.

## Formulation (Gerkmann & Hendriks 2011)

Given the noisy DFT coefficient $X_1(\tau, \omega)$ of the primary microphone and the previous-frame noise estimate $\widehat{\Phi_s}(\tau - 1, \omega)$, the SPP is:

$$\rho(\tau, \omega) = \left(1 + (1 + \xi_{\mathrm{opt}}) \exp\left(-\frac{|X_1(\tau, \omega)|^2}{\widehat{\Phi_s}(\tau - 1, \omega)} \frac{\xi_{\mathrm{opt}}}{\xi_{\mathrm{opt}} + 1}\right)\right)^{-1} \tag{1}$$

where $\xi_{\mathrm{opt}}$ is a fixed optimal a priori SNR. The noise PSD is then updated by soft-combining the previous estimate with the current noisy periodogram:

$$\widehat{\Phi_s}(\tau, \omega) = \rho(\tau, \omega) \cdot \widehat{\Phi_s}(\tau - 1, \omega) + (1 - \rho(\tau, \omega)) |X_1(\tau, \omega)|^2 \tag{2}$$

- $\rho \to 1$: speech present → freeze the noise estimate (keep $\widehat{\Phi_s}(\tau - 1, \omega)$).
- $\rho \to 0$: speech absent → update toward the current periodogram $|X_1|^2$.

## Properties

- **Soft-decision** — avoids the threshold tuning and clipping artifacts of binary VADs.
- **Per-bin** — operates independently in each STFT bin, so noise can be tracked frequency-selectively.
- **Recursive** — only requires the previous-frame noise estimate, enabling online operation.
- **VAD-compatible** — a hard binary VAD can be recovered by thresholding $\rho$ (e.g., $\rho < 0.1$ is used by Jin et al. 2017 as the speech-absent gate for coherence and noise-covariance updates).

## Relation to Other Noise Estimators

SPP-based NE is one of two main single-channel noise PSD estimators in the wiki:

- **[[concepts/minimum-statistics|Minimum Statistics]]** (Martin 2001) — VAD-free; tracks spectral minima. Updates during speech activity via minimum search.
- **SPP-based NE** (Gerkmann & Hendriks 2011) — soft-decision VAD; updates during speech *absence*, weighted by $1 - \rho$.

The two are complementary: SPP gives faster tracking in truly non-stationary noise (no search-window delay), while minimum statistics avoids the soft-decision threshold altogether. Jin et al. 2017 chose SPP for the low-frequency stage precisely because low-frequency coherence-based NE is unreliable, and SPP provides both the low-frequency noise PSD *and* the speech-absence gate needed by the high-frequency coherence stage.

## Multi-Channel Extension (MC-SPP)

The Gaussian-model **multi-channel SPP** (Souden et al. 2010) replaces the scalar a priori SNR with the multi-channel statistics $\xi(\ell,k) = \mathrm{tr}\{\boldsymbol{\Phi}_{vv}^{-1}\boldsymbol{\Phi}_{yy}\} - N$ and a quadratic-form a posteriori term, computing the posterior from the whole observation vector — see [[concepts/multi-channel-speech-presence-probability|Multi-Channel Speech Presence Probability]]. [[sources/bagheri-2019-pmwf-spp|Bagheri & Giacobello 2019]] use MC-SPP for the same soft-combined recursive noise update as Eq. (2), generalized to the noise PSD *matrix* with effective smoothing $\tilde{\alpha}_v = \alpha_v + (1-\alpha_v)\,p(\ell,k)$, and additionally to control a PMWF trade-off parameter and an MMSE output blend.

## Related Concepts

- [[concepts/voice-activity-detection|Voice Activity Detection]] — SPP is the soft-decision generalization of binary VAD
- [[concepts/minimum-statistics|Minimum Statistics]] — alternative single-channel NE paradigm
- [[concepts/adaptive-coherence-noise-estimation|Adaptive Coherence Noise Estimation]] — uses SPP for both low-frequency NE and the speech-absence gate
- [[concepts/wiener-filter|Wiener Filter]] — downstream consumer of the estimated noise PSD
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/multi-channel-speech-presence-probability|Multi-Channel Speech Presence Probability]] — multi-channel Gaussian-model extension

## Related Sources

- [[sources/jin-2017-multichannel-noise-reduction-mobile|Jin, Taghizadeh, Chen & Xiao 2017: Multi-channel Noise Reduction for Hands-free Voice Communication on Mobile Phones]] — uses SPP for the low-frequency NE stage and as the speech-absence gate for the multi-channel coherence stage
- [[sources/bagheri-2019-pmwf-spp|Bagheri & Giacobello 2019: Exploiting MC-SPP in Parametric Multi-Channel Wiener Filter]] — multi-channel Gaussian-model extension driving noise PSD matrix tracking, PMWF trade-off, and MMSE output
