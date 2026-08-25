---
type: source
created: 2026-08-25
updated: 2026-08-25
sources:
  - raw/papers/bagheri-2019-pmwf-spp/full-text.md
  - https://doi.org/10.21437/Interspeech.2019-2665
  - zotero://select/items/0_WNDECJQC
tags:
  - speech-enhancement
  - multi-channel
  - wiener-filter
  - spp
  - noise-estimation
  - beamforming
---

# Bagheri & Giacobello 2019: Exploiting MC-SPP in Parametric Multi-Channel Wiener Filter

**Authors**: [[entities/saeed-bagheri|Saeed Bagheri]], [[entities/daniele-giacobello|Daniele Giacobello]]
**Institution**: Sonos Inc., Santa Barbara, CA, USA
**Venue**: Interspeech 2019
**Type**: Conference paper
**DOI**: [10.21437/Interspeech.2019-2665](https://doi.org/10.21437/Interspeech.2019-2665)
**Zotero**: [WNDECJQC](zotero://select/items/0_WNDECJQC)

## Summary

This paper presents a practical implementation of the [[concepts/parametric-multi-channel-wiener-filter|parametric multi-channel Wiener filter (PMWF)]] that exploits the [[concepts/multi-channel-speech-presence-probability|multi-channel speech presence probability (MC-SPP)]] in three distinct ways: (i) SPP-controlled recursive estimation of the noise PSD matrix with a direct rank-1 update of its *inverse* via the Woodbury identity, (ii) an MC-SPP-controlled trade-off parameter $\beta(\ell,k)$ between noise reduction and speech distortion, and (iii) an MMSE output estimate that blends the filtered signal with a floor-gated reference channel based on the smoothed SPP. Simulations on a 4-microphone circular array in reverberant conditions show the MC-SPP-controlled PMWF with MMSE output outperforms MVDR and the conventional MCWF in SINR improvement, SegSNR improvement, and noise reduction, at only a marginal increase in speech distortion.

## Problem Formulation

In the STFT domain, each microphone of an $N$-element array receives $Y_n(\ell,k) = X_n(\ell,k) + V_n(\ell,k)$, stacking to $\mathbf{y}(\ell,k) = \mathbf{x}(\ell,k) + \mathbf{v}(\ell,k)$ with PSD matrices $\boldsymbol{\Phi}_{yy}, \boldsymbol{\Phi}_{xx}, \boldsymbol{\Phi}_{vv}$. Under uncorrelated zero-mean speech and noise:

$$\boldsymbol{\Phi}_{xx}(\ell,k) = \boldsymbol{\Phi}_{yy}(\ell,k) - \boldsymbol{\Phi}_{vv}(\ell,k)$$

The PMWF is derived as the solution of a constrained optimization: maximize the local noise reduction factor

$$\xi_{nr}(\mathbf{h}_i) = \frac{\Phi_{v_i v_i}}{\mathbf{h}_i^{H} \boldsymbol{\Phi}_{vv} \mathbf{h}_i}$$

subject to the local signal distortion index $\nu_{sd}(\mathbf{h}_i)$ remaining below a frequency-dependent threshold $\sigma^2(\ell,k)$. The closed-form solution (Souden, Benesty & Affes 2010) is

$$\mathbf{h}_i(\ell,k) = \frac{\boldsymbol{\Phi}_{vv}^{-1} \boldsymbol{\Phi}_{yy} - \mathbf{I}_N}{\beta(\ell,k) + \mathrm{tr}\{\boldsymbol{\Phi}_{vv}^{-1} \boldsymbol{\Phi}_{yy}\} - N}\, \mathbf{u}_i$$

where $\beta(\ell,k)$ (the inverse Lagrange multiplier) is a time-frequency-dependent trade-off parameter: $\beta = 0$ yields the MVDR beamformer, $\beta = 1$ the conventional multi-channel Wiener filter. A key property is that the PMWF depends only on input and noise second-order statistics (PSD matrices) — no assumptions on array geometry — making it suitable for distributed arrays with unknown relative geometry (e.g., multi-device smart loudspeakers).

## Methodology

The implementation exploits the MC-SPP at three points of the PMWF pipeline.

### 1. MC-SPP Estimation and Noise PSD Matrix Tracking

Under hypotheses $H_0$ (speech absent) / $H_1$ (speech present) with complex multivariate Gaussian speech and noise, the MC-SPP (Souden et al. 2010) is

$$p(\ell,k) = \left\{1 + \frac{q(\ell,k)}{1-q(\ell,k)} [1+\xi(\ell,k)] \exp\left[-\frac{\gamma(\ell,k)}{1+\xi(\ell,k)}\right]\right\}^{-1}$$

with a fixed a priori speech absence probability $q_0 = 0.5$, and multi-channel a posteriori / a priori SNR-like terms $\gamma(\ell,k)$, $\xi(\ell,k) = \mathrm{tr}\{\boldsymbol{\Phi}_{vv}^{-1}\boldsymbol{\Phi}_{yy}\} - N$ (the latter is also the theoretical output SNR of the PMWF and appears in its denominator). The noise PSD matrix is estimated by SPP-weighted recursive averaging — a multi-channel generalization of [[concepts/multichannel-mcra|MCRA]] noise tracking:

$$\widehat{\boldsymbol{\Phi}}_{vv}(\ell,k) = \tilde{\alpha}_v\,\widehat{\boldsymbol{\Phi}}_{vv}(\ell-1,k) + (1-\tilde{\alpha}_v)\, \mathbf{y}\mathbf{y}^{H}, \qquad \tilde{\alpha}_v = \alpha_v + (1-\alpha_v)\, p(\ell,k)$$

The smoothed SPP $\bar{p}(\ell,k)$ (first-order recursion with coefficient $\alpha_p$, clamped to $[p_{\min}, p_{\max}]$ to avoid stagnation) is used in place of the raw SPP.

### 2. Direct Update of the Inverse Noise PSD Matrix

Since computing $p(\ell,k)$ requires $\widehat{\boldsymbol{\Phi}}_{vv}^{-1}$ which is not yet available, the previous frame's inverse $\widehat{\boldsymbol{\Phi}}_{vv}^{-1}(\ell-1,k)$ is used (optionally iterated). Because the update in Eq. (12) is a rank-1 correction, the **Woodbury matrix identity (Sherman–Morrison formula)** updates the inverse directly without ever forming or inverting $\widehat{\boldsymbol{\Phi}}_{vv}(\ell,k)$:

$$\widehat{\boldsymbol{\Phi}}_{vv}^{-1}(\ell,k) = \frac{1}{\tilde{\alpha}_v}\left(\widehat{\boldsymbol{\Phi}}_{vv}^{-1}(\ell-1,k) - \frac{\tilde{\mathbf{y}}\,\tilde{\mathbf{y}}^{H}}{g(\ell,k)}\right)$$

with $\tilde{\mathbf{y}} = \widehat{\boldsymbol{\Phi}}_{vv}^{-1}(\ell-1,k)\,\mathbf{y}$ and $g = \tilde{\alpha}_v/(1-\tilde{\alpha}_v) + \mathbf{y}^{H}\tilde{\mathbf{y}}$. If estimation errors produce $\gamma < 0$ or $\xi < 0$, the fallback $\widehat{\boldsymbol{\Phi}}_{vv}^{-1} = \widehat{\boldsymbol{\Phi}}_{yy}^{-1}$ avoids numerical issues.

### 3. MC-SPP-Controlled Trade-Off Parameter

Instead of a fixed $\beta$, the trade-off parameter is controlled by the smoothed SPP:

$$\beta(\ell,k) = \frac{\beta_0}{\alpha_\beta + (1-\alpha_\beta)\,\beta_0\,\bar{p}(\ell,k)}$$

Small $\beta$ (less distortion) when speech is present, large $\beta$ (more noise reduction) when speech is absent; $\alpha_\beta$ interpolates between a fixed trade-off and a purely SPP-driven one.

### 4. MMSE Output Estimate

The final output blends the PMWF-filtered signal with a maximum-suppression floor on the reference channel:

$$\widehat{X}_i(\ell,k) = \bar{p}(\ell,k)\, \mathbf{h}_i^{H}\mathbf{y} + (1-\bar{p}(\ell,k))\, G_{\min} Y_i(\ell,k)$$

where $G_{\min}$ bounds the noise reduction applied when speech is absent and can be tuned to the downstream metric (e.g., ASR word error rate). This mitigates speech distortion caused by MC-SPP estimation errors.

### 5. Initialization

The first $L \geq N$ frames (250 ms, $L=16$) are treated as noise-only: $\boldsymbol{\Phi}_{yy}$ is accumulated by direct averaging, the inverse noise PSD is built via Woodbury updates, MC-SPP is set to 0, and output uses Eq. (17). This yields fast, consistent convergence of the noise PSD matrix independent of the noise's spatial/spectral structure.

## Experimental Setup

| Item | Value |
|:-----|:------|
| Sampling rate / STFT | 16 kHz; $M = 512$ samples, 50% overlap, Hann window |
| Room / reverberation | $[5 \times 5 \times 3]$ m; $T_{60} = 300$ ms; RIRs via image source model |
| Array | Circular, $N = 4$ mics, diameter 7.25 cm, at $[2.5, 1, 1]$ m |
| Speech material | TIMIT, 80 speakers (40 M / 40 F), 1 utterance each; source at 3 m, 120° |
| Interference | Babble and pink noise (NOISEX-92) at 2.5 m, 45°; plus spatially/temporally white Gaussian noise |
| Conditions | SIR = SNR; input SINR from −5 to 15 dB |
| Key parameters | $\alpha_v = 0.95$, $\alpha_y = 0.95$, $\alpha_p = 0.1$, $q_0 = 0.5$, $p_{\max} = 0.99$, $p_{\min} = 0.01$, $G_{\min} = 0.1$, $\delta = 10^{-5}$, $L = 16$ |
| Compared methods | MVDR ($\beta_0{=}0, \alpha_\beta{=}1$); MCWF ($\beta_0{=}1, \alpha_\beta{=}1$); SPP-controlled PMWF ($\beta_0{=}1, \alpha_\beta{=}0.75$); PMWF + MMSE output (17) |
| Metrics | ΔSINR, noise reduction factor, speech distortion factor, ΔSegSNR (time-domain, averaged over all utterances) |

## Results

![[raw/papers/bagheri-2019-pmwf-spp/figures/4026f6f1662217742816fbf1cdd0e179c7c9ebeb236124937e328aa7f482fb0d.jpg|Performance metrics for babble noise (left) and pink noise (right)]]

*Figure 1: Performance metrics as a function of input SINR for babble noise (left) and pink noise (right): ΔSINR, ΔSegSNR, noise reduction factor, and speech distortion factor for MVDR, MCWF, SPP-controlled PMWF, and PMWF with MMSE output.*

Results are graphical (Fig. 1); the qualitative findings are:

- **MCWF vs. MVDR**: MCWF consistently outperforms MVDR on all metrics *except* the speech distortion factor (as expected — MVDR is distortionless by construction).
- **SPP-controlled PMWF vs. MCWF**: the PMWF improves ΔSINR, ΔSegSNR, and noise reduction while speech distortion remains almost the same; the improvement shrinks as input SINR increases.
- **PMWF + MMSE output (proposed)**: outperforms all other methods on ΔSINR, ΔSegSNR, and noise reduction, with the gains most noticeable for pink noise; speech distortion increases slightly but the increase is small.
- Overall, MC-SPP improves noise reduction capability with a controlled, tunable increase in speech distortion.

## Key Contributions

1. **Practical PMWF implementation recipe** — assembles all ingredients of a working MC-SPP-driven PMWF: SPP smoothing with $[p_{\min}, p_{\max}]$ clamping, robust fallbacks for negative $\gamma/\xi$, and a noise-only initialization period for consistent convergence.
2. **Direct inverse noise PSD update** — exploits the rank-1 structure of the recursive update to apply the Woodbury/Sherman–Morrison identity, updating $\widehat{\boldsymbol{\Phi}}_{vv}^{-1}$ directly and avoiding costly per-frame matrix inversions.
3. **MC-SPP-controlled trade-off parameter** (Eq. 16) — replaces the fixed $\beta$ with an SPP-driven schedule ($\beta_0, \alpha_\beta$), outperforming the traditional fixed trade-off.
4. **MMSE output estimate with noise-reduction floor** (Eq. 17) — per-bin blending of the filtered signal with a $G_{\min}$-gated reference signal, bounding suppression during speech absence and mitigating SPP-estimation-error distortion; tunable to downstream metrics such as ASR WER.

## Related Concepts

- [[concepts/parametric-multi-channel-wiener-filter|Parametric Multi-Channel Wiener Filter (PMWF)]]
- [[concepts/multi-channel-speech-presence-probability|Multi-Channel Speech Presence Probability (MC-SPP)]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/speech-presence-probability|Speech Presence Probability]]
- [[concepts/multichannel-mcra|Multichannel MCRA]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Related Sources

- [[sources/taseska-2018-informed-spatial-filters|Taseska 2018: Informed Spatial Filters for Speech Enhancement]] — also uses SPP to drive the PMWF trade-off parameter within the informed spatial filter framework
- [[sources/jin-2017-multichannel-noise-reduction-mobile|Jin et al. 2017: Multi-channel Noise Reduction for Mobile Phones]] — alternative MVDR + single-channel Wiener post-filter factorization with SPP-based noise estimation
