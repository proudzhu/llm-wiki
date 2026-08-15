---
type: source
created: 2026-08-15
updated: 2026-08-15
sources:
  - raw/papers/jin-2017-multichannel-noise-reduction-mobile/full-text.md
  - https://doi.org/10.1109/ICASSP.2017.7952207
  - zotero://select/items/0_45QQHIE9
tags:
  - speech-enhancement
  - multi-channel
  - noise-estimation
  - coherence
  - mobile-phones
  - beamforming
  - post-filtering
---

# Jin, Taghizadeh, Chen & Xiao 2017: Multi-channel Noise Reduction for Hands-free Voice Communication on Mobile Phones

- **Authors**: [[entities/wenyu-jin|Wenyu Jin]], [[entities/mohammad-taghizadeh|Mohammad J. Taghizadeh]], [[entities/kainan-chen|Kainan Chen]], [[entities/wei-xiao|Wei Xiao]]
- **Affiliation**: Huawei European Research Center, Munich, Germany
- **Venue**: IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) 2017
- **Year**: 2017
- **Type**: Conference paper
- **DOI**: [10.1109/ICASSP.2017.7952207](https://doi.org/10.1109/ICASSP.2017.7952207)
- **Zotero**: [45QQHIE9](zotero://select/items/0_45QQHIE9)

## Summary

This paper proposes a multi-channel noise reduction (NR) system for hands-free voice communication on high-end mobile phones equipped with multiple microphones. The method combines a single-channel [[concepts/speech-presence-probability|speech presence probability (SPP)]]-based noise PSD estimator (low frequencies) with a globally optimized multi-channel [[concepts/adaptive-coherence-noise-estimation|coherence-based noise estimator]] (high frequencies), unified by an **adaptively varying split frequency** derived from the magnitude-squared coherence crossing 0.5. The multi-channel stage solves a least-squares problem over *all* microphones simultaneously (rather than averaging pairwise estimates), yielding the MMSE-optimal decomposition of the noise field into coherent-diffuse and incoherent components. Evaluated on a 3-microphone Huawei Mate 8 setup in real-world non-stationary noise (pink point source and a real Marienplatz rush-hour recording played over a 22.2 speaker array), the method outperforms Zelinski, McCowan, single-channel, and Nelke et al. baselines on WSS, PESQ, and SDR.

## Problem Formulation

The p-th microphone signal is modeled as a convolutive mixture of the source speech and additive (assumed diffuse) noise:

$$X_p(t) = S(t) * h_p(t) + N_p(t) \tag{1}$$

Following Simmer et al. [14], the broadband MMSE-optimal NR can be factored as a single-channel [[concepts/wiener-filter|Wiener filter]] applied to the output of an [[concepts/mvdr-beamformer|MVDR beamformer]]. The proposed system adopts this factorization (Fig. 1(a)) and concentrates its contribution on the noise PSD estimation stage that drives the Wiener post-filter.

The paper targets three specific shortcomings of prior multi-channel NE methods (Zelinski [12], McCowan [13], Nelke et al. [8]):

1. **Static coherence assumptions** — Zelinski assumes spatially white (incoherent) noise; McCowan assumes fully diffuse coherence. Neither adapts to time-varying noise fields.
2. **Inaccurate at low frequencies** — coherence of speech and noise is high at low frequencies, so multi-channel NE is unreliable there (especially for close microphone spacings typical of mobile phones).
3. **Pairwise averaging is suboptimal** — prior methods average pairwise NE outputs, which is not the MMSE-optimal solution for $P > 2$ microphones.
4. **Fixed split frequency is brittle** — Nelke et al. [8] combine single/multi-channel NE via a fixed frequency threshold, which is vulnerable when speech/noise coherence models entangle at low SNR.

## Methodology

The system (Fig. 1(b)) is an overlap-add STFT pipeline: 512-sample Hamming-windowed frames at 50% overlap, 16 kHz sampling. Three stages: (i) single-channel SPP-based NE on the primary microphone; (ii) multi-channel adaptive-coherence NE over all microphones; (iii) adaptive split-frequency selection that fuses the two estimates.

![[raw/papers/jin-2017-multichannel-noise-reduction-mobile/figures/98336da4e7bd0aefac81abd0a8ab92ac5911a4b84cf02b164af1460d79fdce26.jpg|Proposed NR system block diagram]]

*Figure 1: (a) Filter-sum beamformer with proposed NR; (b) Proposed speech enhancement system. Novel blocks are highlighted. (After Jin et al. 2017, Fig. 1.)*

### 3.1 Single-Channel SPP-Based NE (Low Frequencies)

At low frequencies, the noise PSD $\widehat{\Phi_s}(\tau, \omega)$ is estimated from the primary microphone using the soft-decision SPP method of Gerkmann & Hendriks [7]. The SPP $\rho(\tau, \omega) \in [0, 1]$ is:

$$\rho(\tau, \omega) = \left(1 + (1 + \xi_{\mathrm{opt}}) \exp\left(-\frac{|X_1(\tau, \omega)|^2}{\widehat{\Phi_s}(\tau - 1, \omega)} \frac{\xi_{\mathrm{opt}}}{\xi_{\mathrm{opt}} + 1}\right)\right)^{-1} \tag{2}$$

where $\xi_{\mathrm{opt}}$ is a fixed optimal a priori SNR. The noise PSD is updated by soft-combining the previous estimate with the current noisy periodogram:

$$\widehat{\Phi_s}(\tau, \omega) = \rho(\tau, \omega) \cdot \widehat{\Phi_s}(\tau - 1, \omega) + (1 - \rho(\tau, \omega)) |X_1(\tau, \omega)|^2 \tag{3}$$

$\rho = 1$ indicates complete speech presence (frozen estimate); $\rho = 0$ indicates speech absence (full update). The SPP is also reused as the speech-absence gate for the coherence adaptation in stage (ii).

### 3.2 Coherence-Based NE (High Frequencies)

The theoretical diffuse-field noise coherence between microphones $p, q$ is the sinc function:

$$\gamma_{pq} = \operatorname{sinc}\left(\frac{2 \pi f d_{pq}}{c}\right) \tag{4}$$

In practice, microphone mounting and non-omnidirectional capsules cause deviations, so the coherence is initialized with Eq. (4) and **adaptively updated during speech-absent frames** ($\rho < 0.1$):

$$\gamma_{pq}(\tau, \omega) = \alpha_\gamma \gamma_{pq}(\tau - 1, \omega) + (1 - \alpha_\gamma) \frac{\Phi_{pq}}{\sqrt{\Phi_{pp} \Phi_{qq}}}, \quad \text{when } \rho(\tau, \omega) < 0.1 \tag{5}$$

with smoothing factor $\alpha_\gamma = 0.9$. The auto-/cross-PSDs are recursively smoothed ($\alpha = 0.8$):

$$\Phi_{pq}(\tau) = \alpha \Phi_{pq}(\tau - 1) + (1 - \alpha) X_p X_q^{*} \tag{6}$$

The noise covariance matrix $\mathbf{R}_n \in \mathbb{C}^{P \times P}$ is updated in parallel, also gated by $\rho < 0.1$:

$$\mathbf{R}_n(\tau) = \alpha \mathbf{R}_n(\tau - 1) + (1 - \alpha) \mathbf{x}^T \operatorname{conj}(\mathbf{x}) \tag{7}$$

#### Globally Optimized MMSE Noise Variance Estimation

The noise field is decomposed into a coherent-diffuse component (variance $\sigma_c^2$) and an incoherent component (variance $\sigma_w^2$). Stacking the diagonal and off-diagonal entries of $\mathbf{R}_n$ yields a linear system:

$$\mathbf{R} = \boldsymbol{\Phi} \boldsymbol{\sigma}, \quad \boldsymbol{\sigma} = \begin{bmatrix} \sigma_c^2 \\ \sigma_w^2 \end{bmatrix} \tag{8}$$

where $\mathbf{R} = [\operatorname{diag}(\mathbf{R}_n); \operatorname{odiag}(\mathbf{R}_n)] \in \mathbb{R}^{P^2 \times 1}$ and $\boldsymbol{\Phi} \in \mathbb{R}^{P^2 \times 2}$ is built from the adaptive coherence matrix (Eq. 9). The MMSE-optimal least-squares solution is:

$$\widehat{\boldsymbol{\sigma}} = \operatorname{real}\left(\boldsymbol{\Phi}^{\ddagger} \mathbf{R}\right) \tag{10}$$

where $\boldsymbol{\Phi}^{\ddagger}$ is the Moore-Penrose pseudo-inverse. The high-frequency noise PSD estimate is $\widehat{\Phi_c} = \sigma_c^2$.

**Key distinction from prior work**: this formulation solves for the noise variances globally over all $P$ microphones, whereas Zelinski/McCowan/Nelke average pairwise estimates and are therefore not MMSE-optimal for $P > 2$.

### 3.3 Adaptive Split-Frequency Selection

Rather than using a fixed crossover frequency (as in Nelke et al. [8]), the split frequency is **adaptively derived per frame** from the adaptive coherence model. For each microphone pair $(p, q)$, $f_{pq}$ is the frequency at which $|\gamma_{pq}|^2 = 0.5$. The split frequency $\omega_s$ is the minimum across all pairs:

$$\widehat{\Phi}_n(\tau, \omega) = \begin{cases} \widehat{\Phi}_s(\tau, \omega), & \omega < \min(f_{12}, \dots, f_{pq}) \cdot 2\pi \\ \widehat{\Phi}_c(\tau, \omega), & \omega \geq \min(f_{12}, \dots, f_{pq}) \cdot 2\pi \end{cases} \tag{11}$$

The criterion $|\gamma|^2 = 0.5$ marks the frequency above which speech and noise coherence are sufficiently distinguishable. This avoids the brittleness of a static split when speech/noise coherence entangle at low SNR.

Given $\widehat{\Phi}_n(\tau, \omega)$, the NR gain is computed with the single-channel magnitude DFT estimator under the generalized gamma model of Erkelens et al. [18], and applied to the primary microphone spectrum.

## Experimental Setup

| Item | Value |
|------|-------|
| **Device** | Huawei Mate 8 smartphone with 3 omnidirectional microphones |
| **Microphone geometry** | Mic1, Mic2 at bottom (3.4 cm spacing); Mic3 at top (15.7 cm from Mic2); horizontal planar |
| **Target source** | Loudspeaker at 2 m, broadside (0°) |
| **Noise scenario 1** | Point pink noise at 4.5 m, 135°, SNR = 3 dB |
| **Noise scenario 2** | Real Marienplatz (Munich) rush-hour recording via Eigenmike, ambisonics-coded, replayed over 22.2-channel speaker array at > 3 m, SNR = 5 dB (diffuse, babble, interference) |
| **Room** | Acoustically treated, RT60 = 0.2 ± 0.1 s (125 Hz–8 kHz) |
| **Sampling rate** | 16 kHz |
| **Frame size** | 512 samples, Hamming window, 50% overlap |
| **Speech coherence assumption** | $\gamma_s = 1$ |
| **Smoothing factors** | $\alpha = 0.8$ (PSD/covariance), $\alpha_\gamma = 0.9$ (coherence) |
| **Baselines** | MVDR-only; MVDR + single-channel NR [4]; MVDR + Zelinski [12]; MVDR + McCowan [13]; MVDR + Nelke et al. [8] |
| **Metrics** | WSS (lower better), PESQ (higher better), SDR (higher better, dB) |
| **Recording length** | 20 s per condition |

![[raw/papers/jin-2017-multichannel-noise-reduction-mobile/figures/09d63fdcb8ef7848eb6c8e943abb4283887b678dac0b92f2ca977a6a56787ac1.jpg|Three microphones on Huawei Mate 8]]

*Figure 2: Three-microphone layout on the Huawei Mate 8 smartphone. Mic1 and Mic2 are at the bottom (3.4 cm apart); Mic3 is at the top (15.7 cm from Mic2). (After Jin et al. 2017, Fig. 2.)*

![[raw/papers/jin-2017-multichannel-noise-reduction-mobile/figures/9a799c531c84fb9616c86fd19456b6b0828db961d87feb3c4ec3604b4b227eaa.jpg|Experimental setup at Huawei GRC]]

*Figure 3: Experimental setup at Huawei German Research Center (GRC), Munich. Target loudspeaker at 2 m broadside; pink-noise source at 135°; 22.2-channel array reproduces the Marienplatz diffuse field. (After Jin et al. 2017, Fig. 3.)*

## Results

### Table 1: Pink noise (point source, SNR = 3 dB)

| Method | WSS ↓ | PESQ ↑ | SDR (dB) ↑ |
|--------|------:|-------:|-----------:|
| Beamforming (BF) only | 93.07 | 1.78 | 4.27 |
| BF + Single-channel NR [4] | 92.18 | 1.91 | 4.38 |
| BF + Zelinski postfilter [12] | 81.47 | 1.93 | 5.23 |
| BF + McCowan postfilter [13] | 81.66 | 1.93 | 5.29 |
| BF + Nelke's NR [8] | 78.65 | 2.05 | 7.21 |
| **BF + Proposed NR** | **76.13** | **2.15** | **7.47** |

### Table 2: Marienplatz rush-hour recording (diffuse/non-stationary, SNR = 5 dB)

| Method | WSS ↓ | PESQ ↑ | SDR (dB) ↑ |
|--------|------:|-------:|-----------:|
| BF only | 96.85 | 1.25 | 1.63 |
| BF + Single-channel NR [4] | 100.23 | 1.43 | 3.50 |
| BF + Zelinski postfilter [12] | 104.85 | 1.49 | 1.72 |
| BF + McCowan postfilter [13] | 104.38 | 1.51 | 1.73 |
| BF + Nelke's NR [8] | 80.01 | 1.76 | 5.46 |
| **BF + Proposed NR** | **80.36** | **1.83** | **5.84** |

**Key observations**:

- The proposed method wins on all three metrics in both scenarios except for a marginal WSS win by Nelke in the Marienplatz case (80.01 vs. 80.36 — essentially tied), while still delivering clearly better PESQ and SDR.
- The gain over Nelke et al. [8] is larger in the non-stationary Marienplatz scenario (SDR +0.38 dB pink vs. +0.38 dB Marienplatz; PESQ +0.10 pink vs. +0.07 Marienplatz), confirming that the global MMSE formulation extracts more from the microphone array under complex conditions.
- Zelinski and McCowan postfilters fail to outperform single-channel NR in the Marienplatz scenario (their fixed coherence assumptions are too rigid for non-stationary diffuse noise), while the adaptive-coherence methods (Nelke and proposed) retain a large margin.
- Subjective evaluation by expert listeners was consistent with the objective metrics.

## Key Contributions

1. **Adaptive split-frequency selection** between single- and multi-channel noise estimation — the split is derived per frame from the adaptive coherence model (frequency where $|\gamma_{pq}|^2 = 0.5$), replacing the brittle fixed threshold of Nelke et al.
2. **Globally optimized multi-channel noise variance estimation** — a least-squares solution (Eq. 8–10) over *all* microphones simultaneously, yielding the MMSE-optimal decomposition into coherent-diffuse and incoherent noise components. Prior methods (Zelinski, McCowan, Nelke) average pairwise estimates and are suboptimal for $P > 2$.
3. **Adaptive coherence model** — the diffuse-field sinc coherence (Eq. 4) is treated as an initialization and updated during speech-absent frames ($\rho < 0.1$), accommodating time-varying noise fields and microphone-mounting-induced deviations.
4. **Real-world validation on a commercial smartphone** — three microphones on a Huawei Mate 8, evaluated in both point-source pink noise and a real Marienplatz rush-hour recording replayed over a 22.2-channel array, against four principled baselines.

## Related Concepts

- [[concepts/adaptive-coherence-noise-estimation|Adaptive Coherence Noise Estimation]] — the paper's proposed method
- [[concepts/speech-presence-probability|Speech Presence Probability (SPP)]] — low-frequency NE stage and coherence-update gate
- [[concepts/mvdr-beamformer|MVDR Beamformer]] — front-end beamformer
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]] — the broadband MMSE-optimal factorization the system adopts (Wiener post-filter on MVDR output)
- [[concepts/spatial-coherence|Spatial Coherence]] — the adaptive coherence model
- [[concepts/coherent-to-diffuse-power-ratio|Coherent-to-Diffuse Power Ratio]] — related coherence-based decomposition
- [[concepts/voice-activity-detection|Voice Activity Detection]] — SPP serves as a soft-decision VAD
- [[concepts/minimum-statistics|Minimum Statistics]] — alternative single-channel noise PSD estimator (the SPP method here is the MMSE-soft-decision counterpart)
- [[concepts/beamforming|Beamforming]]
- [[concepts/wiener-filter|Wiener Filter]]
- [[concepts/pesq|PESQ]] — evaluation metric

## Related Synthesis

(No existing synthesis pages currently cover multi-channel noise estimation tradeoffs for mobile-phone hands-free scenarios.)
