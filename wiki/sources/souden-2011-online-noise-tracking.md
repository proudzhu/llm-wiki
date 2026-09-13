---
type: source
created: 2026-09-13
updated: 2026-09-13
sources:
  - raw/papers/souden-2011-online-noise-tracking/full-text.md
  - https://doi.org/10.1109/TASL.2011.2118205
  - zotero://select/items/0_VYWKWM7A
tags:
  - noise-estimation
  - speech-enhancement
  - multi-channel
  - spp
  - mcra
  - wiener-filter
  - statistical-model
---

# Souden, Chen, Benesty & Affes 2011: An Integrated Solution for Online Multichannel Noise Tracking and Reduction

**Authors**: [[entities/mehrez-souden|Mehrez Souden]], [[entities/jingdong-chen|Jingdong Chen]], [[entities/jacob-benesty|Jacob Benesty]], [[entities/sofienne-affes|Sofiène Affes]]
**Venue**: IEEE Transactions on Audio, Speech, and Language Processing, Sep. 2011
**Type**: Journal article
**DOI**: [10.1109/TASL.2011.2118205](https://doi.org/10.1109/TASL.2011.2118205)
**Zotero**: [VYWKWM7A](zotero://select/items/0_VYWKWM7A)

## Summary

This paper turns the theoretical [[concepts/multi-channel-speech-presence-probability|MC-SPP]] (Souden et al. 2010) into a practical, fully online system for multichannel noise tracking and reduction. It contributes (i) a multivariate a priori speech absence probability (SAP) estimator based on Hotelling's $T^2$ and $F$ distributions, (ii) the first generalization of minima-controlled recursive averaging ([[concepts/multichannel-mcra|MCRA]]) from scalar noise PSD to full noise PSD *matrix* tracking, driven by the MC-SPP through a two-iteration procedure, and (iii) a new SPP-driven modified multichannel Wiener filter. The estimator is integrated into three [[concepts/parametric-multi-channel-wiener-filter|PMWF]]-family filters (MVDR, multichannel Wiener, modified Wiener), achieving large gains over single-channel OM-LSA/IMCRA — up to ~9 dB output SINR improvement in babble noise with four microphones.

## Problem Formulation

A speech source impinges on an $N$-microphone array of arbitrary geometry. In the STFT domain:

$$Y_n(k,l) = X_n(k,l) + V_n(k,l), \quad n = 1,\dots,N$$

with the goal of estimating the clean speech spectrum $X_1(k,l)$ at a reference microphone. The noise and noisy PSD matrices, $\boldsymbol{\Phi}_{vv}$ and $\boldsymbol{\Phi}_{yy}$, are tracked by recursive smoothing (forgetting factors $\alpha_y$, $\tilde{\alpha}_v$). The central design issue: $\tilde{\alpha}_v(k,l)$ must be **small when speech is absent** (so the noise estimate follows nonstationary noise) and **large when speech is present** (to avoid overestimating the noise PSD matrix and cancelling speech) — i.e., noise tracking must be controlled by a reliable speech presence detector, generalized from the single-channel to the multichannel case. Unlike the single-channel setting where only spectral information is available, here the extra spatial dimension must be optimally exploited.

## Methodology

### MC-SPP

Under the two-state Gaussian model ($H_0$: $\mathbf{y} = \mathbf{v}$; $H_1$: $\mathbf{y} = \mathbf{x} + \mathbf{v}$), the MC-SPP is

$$p(k,l) = \left\{1 + \frac{q(k,l)}{1-q(k,l)} [1+\xi(k,l)] \exp\left[-\frac{\beta(k,l)}{1+\xi(k,l)}\right]\right\}^{-1}$$

where $\xi(k,l) = \mathrm{tr}[\boldsymbol{\Phi}_{vv}^{-1}\boldsymbol{\Phi}_{xx}]$ is the multichannel a priori SNR (also the theoretical output SNR of the PMWF), $\beta(k,l) = \mathbf{y}^H \boldsymbol{\Phi}_{vv}^{-1}\boldsymbol{\Phi}_{xx}\boldsymbol{\Phi}_{vv}^{-1}\mathbf{y}$ (denoted $\gamma$ on the [[concepts/multi-channel-speech-presence-probability|MC-SPP]] page), and $q(k,l)$ is the a priori SAP. The MC-SPP depends only on the noise/noisy PSD matrices and the current observation — making it directly combinable with recursive statistics estimation. Perfect detection is possible for point-source noise (coherent cancellation) and detection is enhanced by coherent summation of speech for spatially white noise.

### Multivariate A Priori SAP Estimation

Two multichannel a posteriori SNR measures drive the SAP estimate:

$$\psi(k,l) = \mathbf{y}^H \hat{\boldsymbol{\Phi}}_{vv}^{-1}(k,l)\,\mathbf{y}(k,l), \qquad \tilde{\psi}(k,l) = \mathrm{tr}\left[\hat{\boldsymbol{\Phi}}_{vv}^{-1}(k,l)\,\hat{\boldsymbol{\Phi}}_{yy}(k,l)\right]$$

$\psi$ is the instantaneous and $\tilde{\psi}$ the long-term multichannel a posteriori SNR ($\tilde{\psi} \geq N$ under $H_0$). To control the false-alarm rate at significance level $\epsilon = 0.01$, detection thresholds $\psi_0, \tilde{\psi}_0$ are derived from multivariate statistics: under Gaussian i.i.d. and Wishart-distributed PSD-matrix estimates, $\psi$ follows a **Hotelling's $T^2$ distribution** and $\tilde{\psi}$ is approximated by a scaled **$F$ distribution** (with $d = 2N$, $m_E = m_H = L$). The SAP is then built from three soft detectors — local (per frequency bin, soft transition between the thresholds), global (Hann-windowed average over $2K_1+1$ neighboring bins), and frame-wise — combined multiplicatively:

$$\hat{q}(k,l) = \hat{q}_{\mathrm{local}}(k,l)\,\hat{q}_{\mathrm{global}}(k,l)\,\hat{q}_{\mathrm{frame}}(l)$$

with $\hat{q}$ capped at $q_{\max} = 0.99$ for numerical stability. This generalizes Cohen's single-channel soft-decision framework by jointly processing all $N$ microphone observations.

### Multichannel MCRA and Two-Iteration Tracking

The single-channel MCRA noise tracker is generalized to the matrix case: under $H_0$ the noise PSD matrix updates by recursive averaging, under $H_1$ it is frozen. Both cases combine into

$$\hat{\boldsymbol{\Phi}}_{vv}(k,l) = \tilde{\alpha}_v(k,l)\,\hat{\boldsymbol{\Phi}}_{vv}(k,l-1) + [1-\tilde{\alpha}_v(k,l)]\,\mathbf{y}(k,l)\mathbf{y}^H(k,l)$$

with the SPP-controlled smoothing $\tilde{\alpha}_v(k,l) = \alpha_v + (1-\alpha_v)\,p(k,l)$. Since computing $p(k,l)$ needs a good $\hat{\boldsymbol{\Phi}}_{vv}$ but only $\hat{\boldsymbol{\Phi}}_{vv}(k,l-1)$ is available, the algorithm runs a **two-iteration procedure**: iteration 1 computes a first MC-SPP and a first noise PSD matrix estimate from the previous-frame statistics; iteration 2 recomputes $\hat{\xi}, \hat{q}, \hat{\beta}$ from the refined estimate to obtain the final MC-SPP and noise PSD matrix. Initialization assumes the first $L_{\mathrm{init}} = 20$ frames are noise-only. No further improvement is observed beyond the second iteration.

### Integrated Noise Reduction

With $\hat{\boldsymbol{\Phi}}_{xx} = \hat{\boldsymbol{\Phi}}_{yy} - \hat{\boldsymbol{\Phi}}_{vv}$ and $\hat{\xi} = \mathrm{tr}[\hat{\boldsymbol{\Phi}}_{vv}^{-1}\hat{\boldsymbol{\Phi}}_{xx}]$, the tracked statistics feed three PMWF-family filters:

1. **MVDR**: $\mathbf{h}_{\mathrm{MVDR}} = \frac{\hat{\boldsymbol{\Phi}}_{vv}^{-1}\hat{\boldsymbol{\Phi}}_{xx}\mathbf{u}_1}{\hat{\xi}}$
2. **Multichannel Wiener**: $\mathbf{h}_{\mathrm{W}} = \frac{\hat{\boldsymbol{\Phi}}_{vv}^{-1}\hat{\boldsymbol{\Phi}}_{xx}\mathbf{u}_1}{1+\hat{\xi}}$
3. **Modified Wiener (new)**: $\mathbf{h}_{\mathrm{mW}} = \Omega(k,l)\,\mathbf{h}_{\mathrm{MVDR}}$ with $\Omega(k,l) = \left\{1 - \left[\frac{1}{1+\hat{\xi}(k,l)}\right]^{\hat{p}(k,l)}\right\}^{1/\hat{p}(k,l)}$

The heuristic $\Omega$ post-processor applies extra suppression in noise-only segments (small $\hat{p}$) and converges to the Wiener behavior when speech is present ($\hat{p} \to 1$). All three filters belong to the statistics-only PMWF framework of [[sources/souden-2010-pmwf|Souden, Benesty & Affes 2010]], requiring no channel transfer functions or array geometry.

## Experimental Setup

| Item | Value |
|:-----|:------|
| Speech | 6 IEEE sentences (half male, half female), 8 kHz sampling |
| Room | $304.8 \times 457.2 \times 381.0$ cm, image method; anechoic and reverberant ($T_{60} = 210$ ms) |
| Array | Uniform linear, $N = 2$ or $4$ microphones, 6.9 cm spacing |
| Noise | Point-source interference (F-16, babble; NOISEX-92) + white Gaussian; SIR = 5 dB, SNR = 10 dB |
| STFT | 32 ms (anechoic) / 64 ms (reverberant) frames, 50% overlap, Hamming window; FFT size 512 (257 bins) |
| Parameters | $K_1 = 15$, $L = 32$, $\alpha_p = 0.6$, $\alpha_v = \alpha_y = 0.92$, $\epsilon = 0.01$, $q_{\max} = 0.99$, $L_{\mathrm{init}} = 20$ |
| Baseline | Single-channel OM-LSA with IMCRA noise tracking (Cohen & Berdugo), first microphone |
| Metrics | Output SINR, noise reduction factor, signal distortion index |

## Results

**Speech detection.** The second iteration of the MC-SPP procedure yields clearly better detection than the first; more microphones improve detection most where speech energy is weak. ROC curves show a clear gain over the single-channel IMCRA-based SPP — especially for babble noise, the more nonstationary interference.

![[raw/papers/souden-2011-online-noise-tracking/figures/1579a4518c827c7b3088843940f84478afc271a8685d26a47c0ebb42b3cbed0c.jpg|MC-SPP vs instantaneous input SINR after one and two iterations, F-16 interference, panel (a)]]

![[raw/papers/souden-2011-online-noise-tracking/figures/01b859291c5090fcc9de4133f468a2d76b7ff544192e1367216ea7a8a9eb3f2e.jpg|MC-SPP vs instantaneous input SINR after one and two iterations, F-16 interference, panel (b)]]

*Figure 1: MC-SPP versus instantaneous input SINR after one and two iterations (F-16 interference, N = 2 and 4 microphones). The second iteration sharpens the transition of the probability toward 0/1.*

![[raw/papers/souden-2011-online-noise-tracking/figures/2a1bb85728ae9ba7283c5026c6f8f0d8e82e3fdd17050ee69f85ef7eceebf96a.jpg|ROC curves, MC-SPP with 2 and 4 microphones vs single-channel IMCRA, F-16 interference]]

*Figure 3: ROC curves of MC-SPP (2 and 4 microphones) versus single-channel IMCRA, F-16 interference.*

![[raw/papers/souden-2011-online-noise-tracking/figures/83c30e6d999a5e66061180b003a9bfe4a233dfc654cc316368ea890bfb5fc937.jpg|ROC curves, MC-SPP with 2 and 4 microphones vs single-channel IMCRA, babble interference]]

*Figure 4: ROC curves of MC-SPP (2 and 4 microphones) versus single-channel IMCRA, babble interference — the multichannel gain is largest for this nonstationary noise.*

**Noise tracking.** The estimator accurately tracks not only the noise PSD but also the cross-PSD terms (magnitude and phase) between microphones; tracking halts while speech is active and resumes as soon as speech energy decays, allowing the algorithm to follow nonstationary noise.

![[raw/papers/souden-2011-online-noise-tracking/figures/34d66bc81a6e3e3f781b7fa7bac7274662f6a137050eefbd5aaf2141813a69c6.jpg|Noise statistics tracking with F-16 interference: speech periodogram, MC-SPP, noise PSD, cross-PSD magnitude and phase]]

*Figure 5: Noise statistics tracking (F-16 interference, N = 4, SNR = 10 dB, SIR = 5 dB): (a) target speech periodogram, (b) estimated MC-SPP, (c) noise PSD tracking, (d) cross-PSD magnitude tracking, (e) cross-PSD phase tracking.*

![[raw/papers/souden-2011-online-noise-tracking/figures/5a2b439aec3c36edd44bda5cb510fa74fde1048f0e83970198553279b8cdaea3.jpg|Multichannel output SINR tracking, babble interference]]

*Figure 8: Estimated frequency-bin-wise output SINR $\xi(k,l)$ accurately tracking its theoretical value at 1 kHz (babble interference, N = 4).*

**Noise reduction (reverberant room, $T_{60} = 210$ ms).** All measures in dB:

*Table III: Proposed multichannel approach (MVDR / Wiener / modified Wiener).*

| Mics | Filter | Output SINR (F-16 / Babble / White) | Noise reduction (F-16 / Babble / White) | Distortion index (F-16 / Babble / White) |
|:-----|:-------|:-----------------------------------|:----------------------------------------|:-----------------------------------------|
| 2 | MVDR | 12.12 / 11.16 / 12.82 | 8.62 / 7.68 / 9.28 | −19.08 / −19.25 / −19.57 |
| 2 | Wiener | 13.79 / 12.84 / 14.46 | 10.59 / 9.67 / 11.18 | −17.65 / −17.62 / −18.37 |
| 2 | Modified Wiener | 16.01 / 14.70 / 16.63 | 12.83 / 11.55 / 13.37 | −16.33 / −16.32 / −17.13 |
| 4 | MVDR | 15.80 / 15.20 / 15.22 | 12.26 / 11.67 / 11.66 | −19.52 / −20.06 / −19.86 |
| 4 | Wiener | 17.67 / 17.14 / 17.30 | 14.26 / 13.73 / 13.85 | −19.43 / −19.81 / −20.01 |
| 4 | Modified Wiener | 19.88 / 19.27 / 19.45 | 16.48 / 15.88 / 16.02 | −18.48 / −18.71 / −18.97 |

*Table IV: Single-channel OM-LSA (first microphone), same setup.*

| Mics | Filter | Output SINR (F-16 / Babble / White) | Noise reduction (F-16 / Babble / White) | Distortion index (F-16 / Babble / White) |
|:-----|:-------|:-----------------------------------|:----------------------------------------|:-----------------------------------------|
| 2 | MVDR | 10.25 / 9.06 / 11.64 | 6.99 / 5.82 / 8.32 | −15.88 / −16.49 / −15.63 |
| 2 | Wiener | 12.09 / 10.63 / 13.44 | 9.22 / 7.76 / 10.44 | −14.44 / −14.97 / −14.59 |
| 2 | Modified Wiener | 14.27 / 11.97 / 15.71 | 11.44 / 9.14 / 12.75 | −13.50 / −14.08 / −13.88 |
| 4 | MVDR | 12.63 / 11.65 / 13.84 | 9.64 / 8.76 / 10.80 | −13.19 / −12.79 / −13.17 |
| 4 | Wiener | 14.53 / 13.23 / 15.67 | 11.78 / 10.56 / 12.81 | −12.69 / −12.32 / −12.87 |
| 4 | Modified Wiener | 16.99 / 14.81 / 18.03 | 14.28 / 12.18 / 15.21 | −12.14 / −11.87 / −12.49 |

Key findings:

- The **modified Wiener filter** achieves the largest noise reduction and output SINR in all scenarios at the price of increased (but still small, and concentrated on weak speech components) distortion — consistent with its SPP-driven post-processor amplifying the effect of speech miss-detections.
- **Four microphones beat two** on every measure, confirming that better detection and more spatial aperture compound.
- **Babble noise is the hardest** interference (least noise reduction) because its statistics vary too fast to track.
- In the **anechoic room**, the multichannel advantage over OM-LSA is largest: with four microphones and the modified Wiener filter, the output SINR gain reaches ~9 dB in babble noise with ~8 dB better speech distortion. (The anechoic tables in the extraction lost their filter dimension; the qualitative summary follows the paper's discussion.)

## Key Contributions

1. **Practical MC-SPP implementation** — the first working estimator for the Gaussian-model MC-SPP of Souden et al. (2010), including a two-iteration procedure that resolves the chicken-and-egg dependency between the SPP and the noise PSD matrix.
2. **Multivariate a priori SAP estimation** — local/global/frame soft-decision SAP built on Hotelling's $T^2$ and $F$-distribution thresholds at significance level 0.01, jointly processing all microphone signals rather than one channel.
3. **Multichannel MCRA** — the first generalization of minima-controlled recursive averaging from scalar noise PSD to full noise PSD *matrix* tracking, with SPP-controlled smoothing $\tilde{\alpha}_v = \alpha_v + (1-\alpha_v)p$.
4. **SPP-driven modified multichannel Wiener filter** — a new filter $\mathbf{h}_{\mathrm{mW}} = \Omega\,\mathbf{h}_{\mathrm{MVDR}}$ whose $\Omega$ post-processor exploits the MC-SPP for extra suppression in noise-only segments.
5. **Integrated online system** — detection, noise tracking, and PMWF-family filtering evaluated end-to-end against single-channel OM-LSA/IMCRA in anechoic and reverberant rooms, stationary and nonstationary noise.

## Related Concepts

- [[concepts/multi-channel-speech-presence-probability|Multi-Channel Speech Presence Probability (MC-SPP)]]
- [[concepts/multichannel-mcra|Multichannel MCRA]]
- [[concepts/speech-presence-probability|Speech Presence Probability (SPP)]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/parametric-multi-channel-wiener-filter|Parametric Multi-Channel Wiener Filter (PMWF)]]
- [[concepts/minimum-statistics|Minimum Statistics]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
