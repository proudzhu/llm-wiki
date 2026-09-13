---
type: concept
created: 2026-08-25
updated: 2026-09-13
sources:
  - raw/papers/souden-2011-online-noise-tracking/full-text.md
  - raw/papers/bagheri-2019-pmwf-spp/full-text.md
  - raw/papers/grinstein-2025-tiny-param-mwf/full-text.md
  - raw/papers/braun-2015-residual-noise-control/full-text.md
tags:
  - noise-estimation
  - speech-enhancement
  - multi-channel
  - spp
  - statistical-model
---

# Multi-Channel Speech Presence Probability (MC-SPP)

The **Multi-Channel Speech Presence Probability (MC-SPP)** extends single-channel [[concepts/speech-presence-probability|SPP]] to microphone arrays of arbitrary geometry by modelling speech and noise as complex multivariate Gaussian random vectors (Souden, Chen, Benesty & Affes, IEEE TASLP 2010). It estimates, per time-frequency bin, the probability that speech is present given the *entire* observation vector $\mathbf{y}(\ell,k)$, exploiting spatial information across channels rather than only the spectral magnitude of one channel.

## Formulation

Under hypotheses $H_0$: $\mathbf{y} = \mathbf{v}$ (speech absent) and $H_1$: $\mathbf{y} = \mathbf{x} + \mathbf{v}$ (speech present), the MC-SPP is

$$p(\ell,k) = \left\{1 + \frac{q(\ell,k)}{1-q(\ell,k)}\,[1+\xi(\ell,k)]\,\exp\left[-\frac{\gamma(\ell,k)}{1+\xi(\ell,k)}\right]\right\}^{-1}$$

where $q(\ell,k)$ is the a priori speech absence probability and the multi-channel statistics are

$$\xi(\ell,k) = \mathrm{tr}\{\boldsymbol{\Phi}_{vv}^{-1}\boldsymbol{\Phi}_{yy}\} - N, \qquad \gamma(\ell,k) = \mathbf{y}^{H}\boldsymbol{\Phi}_{vv}^{-1}\boldsymbol{\Phi}_{xx}\boldsymbol{\Phi}_{vv}^{-1}\mathbf{y}$$

$\xi$ is the multi-channel a priori SNR (also the theoretical output SNR of the [[concepts/parametric-multi-channel-wiener-filter|PMWF]]). Both require $\boldsymbol{\Phi}_{vv}^{-1}$ — creating a chicken-and-egg dependency resolved in practice by using the previous frame's inverse (optionally with a few iterations).

## Uses

1. **Noise PSD matrix estimation** — SPP-weighted recursive averaging $\tilde{\alpha}_v = \alpha_v + (1-\alpha_v)\,p(\ell,k)$ generalizes MCRA noise tracking to the multi-channel case (cf. [[concepts/multichannel-mcra|Multichannel MCRA]]); it also underlies online multi-channel noise tracking with SAP estimators (Souden et al. 2011).
2. **PMWF trade-off control** — the smoothed SPP modulates the PMWF trade-off parameter $\beta(\ell,k)$ between low distortion (speech present) and strong noise reduction (speech absent).
3. **MMSE output estimation** — per-bin blending of the filtered signal with a $G_{\min}$-gated reference channel.

## Practical Implementation (Souden, Chen, Benesty & Affes 2011)

[[sources/souden-2011-online-noise-tracking|Souden et al. 2011]] turn the Gaussian-model MC-SPP into a fully online estimator:

- **Multivariate a priori SAP** — built from the instantaneous ($\psi = \mathbf{y}^H\hat{\boldsymbol{\Phi}}_{vv}^{-1}\mathbf{y}$, Hotelling's $T^2$-distributed under $H_0$) and long-term ($\tilde{\psi} = \mathrm{tr}\{\hat{\boldsymbol{\Phi}}_{vv}^{-1}\hat{\boldsymbol{\Phi}}_{yy}\}$, approximated by a scaled $F$ distribution) multichannel a posteriori SNRs, with false-alarm thresholds set at significance level $\epsilon = 0.01$; local, global (Hann-windowed over $2K_1+1$ neighboring bins), and frame-wise soft decisions are combined multiplicatively and capped at $q_{\max} = 0.99$.
- **Two-iteration procedure** — resolves the chicken-and-egg dependency between the MC-SPP and the noise PSD matrix: a first pass computes the SPP and a first noise PSD matrix estimate from the previous frame's statistics; a second pass recomputes $\hat{\xi}, \hat{q}, \hat{\beta}$ from the refined estimate. No further improvement is observed beyond the second iteration.
- **Safeguards** — SPP smoothing with $\alpha_p = 0.6$ and a noise-only initialization of $L_{\mathrm{init}} = 20$ frames.
- **ROC evidence** — the second iteration sharpens detection, and the MC-SPP with 2 or 4 microphones clearly outperforms single-channel IMCRA-based SPP, with the largest gain in (highly nonstationary) babble noise; additional microphones help most where speech energy is weak.

## Practical Safeguards (Bagheri & Giacobello 2019)

- Recursive smoothing of the SPP with coefficient $\alpha_p$ and clamping to $[p_{\min}, p_{\max}]$ (e.g., $[0.01, 0.99]$) to avoid stagnation.
- Fallback to $\widehat{\boldsymbol{\Phi}}_{vv}^{-1} = \widehat{\boldsymbol{\Phi}}_{yy}^{-1}$ when estimation errors yield negative $\gamma$ or $\xi$.
- Fixed $q_0 = 0.5$ a priori speech absence probability works well in their implementation.

## Mask-Derived SPP Proxy (Grinstein et al. 2025)

[[sources/grinstein-2025-tiny-param-mwf|Grinstein et al. 2025]]'s [[concepts/neuralpmwf|NeuralPMWF]] replaces the Gaussian-model MC-SPP with a lightweight SPP *proxy* computed from the magnitude of a learned multi-channel complex mask at the reference channel:

$$\hat{p}[t,w]=\text{sigmoid}\big(\mathbf{p}^{(a)}[w]\,|\mathbf{G}[t,w,0]|+\mathbf{p}^{(b)}[w]\big)$$

with per-frequency gains $\mathbf{p}^{(a)},\mathbf{p}^{(b)}\in\mathbb{R}^{F}$ learned end-to-end through the differentiable PMWF. This SPP proxy drives the distortion trade-off $\beta[t,w]=\beta^{(0)}[w](1-\hat{p}[t,w])$ and proves to be the single most valuable component of the system (+4.5 STOI over fixed-$\beta$ variants) — evidence that the *role* of SPP as a distortion/suppression scheduler survives the move from statistical-model to neural estimation, without any explicit Gaussian hypothesis or iterative $\Phi_{vv}^{-1}$ dependency.

## Relation to Single-Channel SPP

The single-channel [[concepts/speech-presence-probability|SPP]] (e.g., Gerkmann & Hendriks 2011, Gerkmann & Malah 1989 optimum a priori SNR modification) computes the posterior from one channel's a posteriori SNR; the MC-SPP replaces scalar SNRs with the multi-channel quadratic forms above, gaining robustness from the array's spatial aperture. Alternative multi-channel a priori SAP estimators exploit spatial structure directly, e.g., the CDR-based estimator of [[concepts/multichannel-mcra|Multichannel MCRA]] (Taseska & Habets) or complex-coherence-based a priori SAP (Taseska & Habets 2012).

## Related Concepts

- [[concepts/speech-presence-probability|Speech Presence Probability (SPP)]]
- [[concepts/parametric-multi-channel-wiener-filter|Parametric Multi-Channel Wiener Filter (PMWF)]]
- [[concepts/multichannel-mcra|Multichannel MCRA]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/neuralpmwf|NeuralPMWF]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask]]

## Related Sources

- [[sources/bagheri-2019-pmwf-spp|Bagheri & Giacobello 2019: Exploiting MC-SPP in Parametric Multi-Channel Wiener Filter]]
- [[sources/souden-2011-online-noise-tracking|Souden, Chen, Benesty & Affes 2011: An Integrated Solution for Online Multichannel Noise Tracking and Reduction]] — first practical online MC-SPP implementation: multivariate a priori SAP, two-iteration refinement, ROC gains over single-channel IMCRA
- [[sources/taseska-2018-informed-spatial-filters|Taseska 2018: Informed Spatial Filters for Speech Enhancement]]
- [[sources/jin-2017-multichannel-noise-reduction-mobile|Jin et al. 2017: Multi-channel Noise Reduction for Mobile Phones]] — single-channel SPP counterpart in an MVDR + post-filter pipeline
- [[sources/grinstein-2025-tiny-param-mwf|Grinstein et al. 2025: Controlling the PMWF Using a Tiny Neural Network]] — mask-magnitude SPP proxy scheduling the PMWF distortion parameter
- [[sources/braun-2015-residual-noise-control|Braun, Kowalczyk & Habets 2015: Residual Noise Control Using a Parametric Multichannel Wiener Filter]]

