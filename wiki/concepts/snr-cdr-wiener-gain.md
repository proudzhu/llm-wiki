---
type: concept
created: 2026-09-18
updated: 2026-09-18
sources:
  - raw/papers/xiang-2025-wiener-gain-reverberant/full-text.md
tags:
  - speech-enhancement
  - wiener-filter
  - dereverberation
  - noise-reduction
  - cdr-estimation
---

# SNR–CDR Wiener Gain

The **SNR–CDR Wiener gain** (Xiang, Chen, Benesty, Lei & Pan 2025) is a scalar STFT-domain post-filter that unifies the two classical degenerate Wiener gains — the SNR-based gain for additive-noise suppression and the CDR-based gain for reverberation suppression — into a single formulation driven by estimates of **both** the signal-to-noise ratio and the coherent-to-diffuse ratio, for environments where noise and reverberation coexist.

## Key Formulations

### Degenerate ancestors

With only additive noise, the optimal gain reduces to the classical Wiener spectral gain:

$$G(n,k) = \frac{\mathrm{SNR}(n,k)}{1 + \mathrm{SNR}(n,k)}, \qquad \mathrm{SNR} \triangleq \frac{\phi_S}{\phi_V}$$

With only reverberation, it reduces to the CDR gain (reverberation modeled as diffuse):

$$G(n,k) = \frac{\mathrm{CDR}(n,k)}{1 + \mathrm{CDR}(n,k)}, \qquad \mathrm{CDR} \triangleq \frac{\phi_S}{\phi_R}$$

### Joint gain

With both interferers and a distortionless spatial filter ($\alpha_S \approx 1$), the optimal gain weights each interferer by its leakage through the beamformer ($\alpha_R, \alpha_V$, the coherence-weighted quadratic forms of the reverberation and noise coherence matrices):

$$G(n,k) = \frac{1}{1 + \alpha_R(k)\frac{1}{\mathrm{CDR}(n,k)} + \alpha_V(k)\frac{1}{\mathrm{SNR}(n,k)}}$$

### Generalized two-hyperparameter form

The design is then generalized with two hyperparameters that separate the trade-off axes:

$$G(n,k) = \frac{1}{1 + \beta_1\frac{\alpha_R(k)}{\mathrm{CDR}(n,k)} + \beta_2\frac{\alpha_V(k)}{\mathrm{SNR}(n,k)}}, \qquad \beta_1, \beta_2 \geq 0$$

- $\beta_1$ governs **reverberation suppression** — raising it increases DRR efficiently but raises LSD (distortion)
- $\beta_2$ governs **noise reduction** — raising it increases SNR gain, saturating for $\beta_2 \gtrsim 5$

The applied gain is floored by $G \leftarrow \max\{G, G_{\min}\}$ to suppress musical noise; a kurtosis-ratio analysis shows $G_{\min} = 0.1$ to be a stable operating point.

### Noise-aware CDR estimation

The gain requires a CDR estimate valid in noisy fields. The companion estimator extends the pairwise Schwarz & Kellermann formulation by folding the noise coherence into the observed-coherence term given the SNR:

$$e_{i,j}(k) = [\boldsymbol{\Gamma}_Y]_{i,j} + \frac{[\boldsymbol{\Gamma}_Y]_{i,j} - [\boldsymbol{\Gamma}_V]_{i,j}}{\mathrm{SNR}(k)}$$

and solving the unit-diagonal constraint on the source coherence matrix for the CDR (a closed-form quadratic root), averaged over all sensor pairs. This lowers CDR estimation error relative to noise-ignoring estimators and keeps DRR nearly constant across input SNRs.

## Empirical behavior

Applied after a robust superdirective beamformer (4-mic ULA, 2 cm, image-method rooms), the joint gain achieved the best SNR gain (11.4 dB) and DRR (9.3 dB) and tied the best LSD (7.2 dB) against SD-SNR, SD-CDR, SD-TSNR, SD-HRNR, and AWPE baselines (input SNR 5 dB, $T_{60} \approx 500$ ms, $\beta_1 = 5$, $\beta_2 = 3$). AWPE degrades rapidly as input SNR drops, while the joint gain — whose SNR-driven term tracks the noise level — remains robust in jointly noisy and reverberant conditions.

## Related Concepts

- [[concepts/wiener-filter|Wiener Filter]] — the optimal-filter root and the degenerate noise-only gain
- [[concepts/coherent-to-diffuse-power-ratio|Coherent-to-Diffuse Power Ratio]] — the reverberation-side ratio and its noise-aware estimation
- [[concepts/multichannel-cdr-estimation|Multichannel CDR Estimation]] — the same group's $M > 2$ extension of pairwise CDR estimation (weighted-average subarrays, array-manifold joint diagonalization)
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]] — the beamformer + Wiener gain decomposition this post-filter completes
- [[concepts/superdirective-beamforming|Superdirective Beamforming]] — the adopted spatial filter
- [[concepts/decision-directed-a-priori-snr|Decision-Directed a Priori SNR]] — the SNR estimation stage
- [[concepts/dereverberation|Dereverberation]]

## Related Sources

- [[sources/xiang-2025-wiener-gain-reverberant|Xiang, Chen, Benesty, Lei & Pan 2025: Design of the Wiener Gain in Noisy and Reverberant Environments]] — introduces the formulation, the noise-aware CDR estimator, and the two-hyperparameter trade-off study
- [[sources/xiang-2024-multichannel-cdr-estimation|Xiang, Lei, Pan, Chen & Benesty 2024: On Multichannel Coherent-to-Diffuse Power Ratio Estimation]] — the same group's predecessor: multichannel (M > 2) CDR estimation via weighted-average subarray fusion and array-manifold joint diagonalization
