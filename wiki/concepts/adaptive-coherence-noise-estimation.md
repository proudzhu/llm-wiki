---
type: concept
created: 2026-08-15
updated: 2026-08-15
sources:
  - raw/papers/jin-2017-multichannel-noise-reduction-mobile/full-text.md
tags:
  - noise-estimation
  - multi-channel
  - coherence
  - speech-enhancement
  - adaptive
---

# Adaptive Coherence Noise Estimation

**Adaptive Coherence Noise Estimation** is a multi-channel noise PSD estimation method proposed by Jin et al. (2017) for hands-free voice communication on mobile phones. It combines a single-channel [[concepts/speech-presence-probability|SPP]]-based estimator at low frequencies with a globally MMSE-optimized coherence-based estimator at high frequencies, unified by an **adaptively varying split frequency** derived from the coherence model itself. The coherence function is initialized with the theoretical diffuse-field sinc model and adaptively updated during speech-absent frames, accommodating time-varying noise fields and microphone-mounting-induced deviations.

## Motivation

Prior multi-channel noise estimators suffer from three limitations that this method addresses:

| Prior Method | Limitation | Remedy in Jin et al. 2017 |
|--------------|------------|---------------------------|
| Zelinski [12] | Assumes spatially white (incoherent) noise | Adaptive coherence model (Eq. 5) |
| McCowan [13] | Assumes fully diffuse noise (sinc coherence) | Adaptive coherence model (Eq. 5) |
| Nelke et al. [8] | Fixed split frequency; pairwise averaging | Adaptive split (Eq. 11); global MMSE solve (Eq. 8–10) |
| All of the above | Average pairwise estimates → not MMSE-optimal for $P > 2$ | Global least-squares over all $P$ microphones |

## Method

The system runs in an STFT overlap-add pipeline ($N = 512$, Hamming, 50% overlap) on $P$ microphone channels. The noise PSD estimate is assembled in three stages.

### Stage 1 — Single-Channel SPP NE (low frequencies)

The [[concepts/speech-presence-probability|SPP-based NE]] of Gerkmann & Hendriks [7] runs on the primary microphone. The SPP $\rho(\tau, \omega) \in [0, 1]$ (Eq. 2 of the source paper) gates a recursive smoothed estimate (Eq. 3). The output is $\widehat{\Phi_s}(\tau, \omega)$. The SPP is reused in Stage 2 as a speech-absence gate ($\rho < 0.1$) for coherence and covariance updates.

### Stage 2 — Multi-Channel Coherence NE (high frequencies)

The theoretical diffuse-field coherence initializes the model:

$$\gamma_{pq} = \operatorname{sinc}\left(\frac{2 \pi f d_{pq}}{c}\right)$$

and is updated only when speech is absent:

$$\gamma_{pq}(\tau, \omega) = \alpha_\gamma \gamma_{pq}(\tau - 1, \omega) + (1 - \alpha_\gamma) \frac{\Phi_{pq}}{\sqrt{\Phi_{pp} \Phi_{qq}}}, \quad \rho(\tau, \omega) < 0.1$$

with $\alpha_\gamma = 0.9$. The noise covariance matrix $\mathbf{R}_n \in \mathbb{C}^{P \times P}$ is updated in parallel under the same SPP gate.

The noise field is decomposed into a coherent-diffuse component (variance $\sigma_c^2$) and an incoherent component (variance $\sigma_w^2$). Stacking the diagonal and off-diagonal entries of $\mathbf{R}_n$ yields the linear system:

$$\mathbf{R} = \boldsymbol{\Phi} \boldsymbol{\sigma}, \quad \boldsymbol{\sigma} = \begin{bmatrix} \sigma_c^2 \\ \sigma_w^2 \end{bmatrix}$$

where $\boldsymbol{\Phi} \in \mathbb{R}^{P^2 \times 2}$ is built from the adaptive coherence matrix. The MMSE-optimal least-squares solution is:

$$\widehat{\boldsymbol{\sigma}} = \operatorname{real}\left(\boldsymbol{\Phi}^{\ddagger} \mathbf{R}\right)$$

via the Moore-Penrose pseudo-inverse $\boldsymbol{\Phi}^{\ddagger}$. The high-frequency noise PSD is $\widehat{\Phi_c} = \sigma_c^2$.

**Key distinction**: this global formulation solves over *all* $P$ microphones simultaneously, whereas Zelinski / McCowan / Nelke average pairwise estimates and are therefore suboptimal for $P > 2$.

### Stage 3 — Adaptive Split-Frequency Selection

The split $\omega_s$ is derived per frame as the lowest frequency at which the magnitude-squared coherence of any microphone pair crosses 0.5:

$$\widehat{\Phi}_n(\tau, \omega) = \begin{cases} \widehat{\Phi_s}(\tau, \omega), & \omega < \min(f_{12}, \dots, f_{pq}) \cdot 2\pi \\ \widehat{\Phi_c}(\tau, \omega), & \omega \geq \min(f_{12}, \dots, f_{pq}) \cdot 2\pi \end{cases}$$

The criterion $|\gamma|^2 = 0.5$ marks the frequency above which speech and noise coherence are sufficiently distinguishable. This adapts the crossover to the current noise field, avoiding the brittleness of Nelke et al.'s static threshold when speech/noise coherence entangle at low SNR.

## Properties

- **Adaptive to time-varying noise** — coherence model and noise covariance are updated only during speech-absent frames, tracked via SPP.
- **MMSE-optimal for $P > 2$** — the global least-squares solution exploits all microphones; pairwise averaging is provably suboptimal.
- **Robust at low frequencies** — the single-channel SPP stage avoids the unreliable coherence-based estimate where speech/noise coherence overlap.
- **Real-time capable** — overlap-add STFT, recursive smoothing, and a small pseudo-inverse ($2 \times P^2$).

## Empirical Results

Evaluated on a Huawei Mate 8 (3 microphones) in two scenarios (pink point source, Marienplatz rush-hour diffuse noise), the method outperforms Zelinski, McCowan, single-channel NR (Ephraim-Malah), and Nelke et al. on WSS, PESQ, and SDR. The advantage is largest in the non-stationary Marienplatz scenario, where the global MMSE formulation extracts more from the array than pairwise averaging.

See [[sources/jin-2017-multichannel-noise-reduction-mobile|Jin et al. 2017]] for the full quantitative tables.

## Related Concepts

- [[concepts/speech-presence-probability|Speech Presence Probability (SPP)]] — Stage 1 estimator and the speech-absence gate for Stages 2–3
- [[concepts/spatial-coherence|Spatial Coherence]] — the adaptive coherence model
- [[concepts/coherent-to-diffuse-power-ratio|Coherent-to-Diffuse Power Ratio]] — related coherence-based decomposition
- [[concepts/mvdr-beamformer|MVDR Beamformer]] — front-end beamformer the method post-filters
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]] — the broadband MMSE factorization context
- [[concepts/minimum-statistics|Minimum Statistics]] — alternative single-channel NE (the SPP method is the soft-decision counterpart)
- [[concepts/voice-activity-detection|Voice Activity Detection]]

## Related Sources

- [[sources/jin-2017-multichannel-noise-reduction-mobile|Jin, Taghizadeh, Chen & Xiao 2017: Multi-channel Noise Reduction for Hands-free Voice Communication on Mobile Phones]] — introduces the method
