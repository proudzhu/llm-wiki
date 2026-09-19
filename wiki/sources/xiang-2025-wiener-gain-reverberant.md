---
type: source
created: 2026-09-18
updated: 2026-09-19
sources:
  - raw/papers/xiang-2025-wiener-gain-reverberant/full-text.md
  - https://doi.org/10.1016/j.apacoust.2024.110491
  - zotero://select/items/0_BMNB6JBP
tags:
  - speech-enhancement
  - dereverberation
  - noise-reduction
  - wiener-filter
  - cdr-estimation
  - coherence
  - beamforming
---

# Xiang, Chen, Benesty, Lei & Pan 2025: Design of the Wiener Gain in Noisy and Reverberant Environments

**Authors**: [[entities/qian-xiang|Qian Xiang]], [[entities/jingdong-chen|Jingdong Chen]], [[entities/jacob-benesty|Jacob Benesty]], [[entities/tao-lei|Tao Lei]], [[entities/chao-pan|Chao Pan]]
**Institution**: Fuyang Normal University, Fuyang & Shaanxi University of Science and Technology, Xi'an; Northwestern Polytechnical University, Xi'an; INRS-EMT, University of Quebec, Montreal
**Venue**: Applied Acoustics, March 2025 (article 110491)
**Type**: Journal article
**DOI**: [10.1016/j.apacoust.2024.110491](https://doi.org/10.1016/j.apacoust.2024.110491)
**Zotero**: [BMNB6JBP](zotero://select/items/0_BMNB6JBP)
**Funding**: National Key R&D Program of China (2021ZD0201502); NSFC Key Program (62192713, 61831019, 62171373, 62271296)

## Summary

Traditional Wiener gain formulations are based solely on either the SNR (targeting additive noise) or the coherent-to-diffuse ratio (CDR, targeting reverberation), rendering them suboptimal when noise and reverberation coexist. This paper designs a Wiener gain that incorporates estimates of **both** SNR and CDR, introduces two hyperparameters $\beta_1, \beta_2$ to govern the extent of noise reduction versus reverberation suppression, and derives a **noise-aware, DOA-independent CDR estimator** that extends pairwise coherence-based estimation to noisy environments. Combined with a robust superdirective beamformer as the spatial filter, the proposed post-filter outperforms SD-SNR, SD-CDR, SD-TSNR, SD-HRNR, and AWPE in SNR gain, LSD, DRR, PESQ, SRMR, and kurtosis ratio — a superiority confirmed both in simulation and in real-classroom experiments with measured impulse responses.

## Problem Formulation

An $M$-microphone array picks up speech in a noisy and reverberant environment. The time-domain observation at the $m$th sensor decomposes into early and late reflection components plus additive noise:

$$y_m(t) = g_{m,\text{early}}(t) * s(t) + g_{m,\text{late}}(t) * s(t) + v_m(t)$$

In the STFT domain, the vector model is $\mathbf{y}(n,k) = \mathbf{d}(k)S(n,k) + \mathbf{r}(n,k) + \mathbf{v}(n,k)$, where $\mathbf{r}$ is late reverberation and $\mathbf{v}$ is additive noise, mutually uncorrelated with the source. For small-spacing arrays, reverberation and noise covariances factor as coherence matrices times variances, $\boldsymbol{\Phi}_R = \boldsymbol{\Gamma}_R \phi_R$ and $\boldsymbol{\Phi}_V = \boldsymbol{\Gamma}_V \phi_V$, so the beamformer output variance is

$$\phi_Z = \alpha_S(k)\phi_S + \alpha_R(k)\phi_R + \alpha_V(k)\phi_V$$

with $\alpha_S = |\mathbf{h}^H\mathbf{d}|^2$ and $\alpha_R, \alpha_V$ the coherence-weighted leakage of reverberation and noise through the spatial filter. A post-filter $G(n,k) \in [0,1]$ is then applied to $Z(n,k)$ to produce the final estimate.

The two classical degenerate gains motivate the problem:

- **Noise-only** (no reverberation): $G = \mathrm{SNR}/(1+\mathrm{SNR})$, with $\mathrm{SNR} \triangleq \phi_S/\phi_V$
- **Reverberation-only** (no noise): $G = \mathrm{CDR}/(1+\mathrm{CDR})$, with $\mathrm{CDR} \triangleq \phi_S/\phi_R$

Existing work estimates the gain in one form or the other; few efforts consider both interferers simultaneously — precisely the objective of this work.

## Methodology

### Joint SNR–CDR Wiener Gain

With both reverberation and noise present, the optimal Wiener gain follows from the output variance decomposition. Assuming the distortionless constraint ($\alpha_S \approx 1$):

$$G(n,k) = \frac{1}{1 + \alpha_R(k)\frac{1}{\mathrm{CDR}(n,k)} + \alpha_V(k)\frac{1}{\mathrm{SNR}(n,k)}}$$

The paper then **generalizes** this with two hyperparameters:

$$G(n,k) = \frac{1}{1 + \beta_1\frac{\alpha_R(k)}{\mathrm{CDR}(n,k)} + \beta_2\frac{\alpha_V(k)}{\mathrm{SNR}(n,k)}}$$

where $\beta_1, \beta_2 \geq 0$ control the trade-off between noise reduction and reverberation suppression. The applied gain is floored by $G \leftarrow \max\{G, G_{\min}\}$ to mitigate musical noise (isolated STFT peaks), with $G_{\min} \in (0,1)$, e.g. 0.01.

### Implementation Pipeline

1. **Covariance/coherence estimation**: recursively averaged observation covariance (forgetting factor $\lambda$), normalized to coherence; noise covariance estimated during signal absence; reverberation coherence modeled as diffuse-field sinc coherence $\sin(\omega\Delta_{ij}/c)/(\omega\Delta_{ij}/c)$.
2. **Spatial filter**: robust [[concepts/superdirective-beamforming|superdirective beamformer]] $\mathbf{h}(k) = \frac{\boldsymbol{\Gamma}_{R,\epsilon}^{-1}(k)\mathbf{d}_0(k)}{\mathbf{d}_0^H\boldsymbol{\Gamma}_{R,\epsilon}^{-1}(k)\mathbf{d}_0(k)}$ with [[concepts/diagonal-loading|diagonal loading]] $\epsilon = 10^{-3}$; $\alpha_R, \alpha_V$ computed from the coherence matrices through this beamformer.
3. **SNR estimation**: [[concepts/decision-directed-a-priori-snr|decision-directed approach]] — smoothing a priori and instantaneous SNR estimates ($\xi, \zeta$), with the noise variance from minimum tracking.
4. **CDR estimation**: a **noise-aware DOA-independent pairwise estimator**. Writing the observation covariance as $\boldsymbol{\Phi}_Y = \phi_S\boldsymbol{\Gamma}_S + \phi_R\boldsymbol{\Gamma}_R + \phi_V\boldsymbol{\Gamma}_V$ and using the unit-diagonal constraint on the source coherence matrix, the estimator for the $(i,j)$ sensor pair given the SNR is

$$\mathrm{CDR}_{i,j}(k) = \frac{-g_{i,j}(k) - \sqrt{g_{i,j}^2(k) - (|e_{i,j}(k)|^2 - 1)|f_{i,j}(k)|^2}}{|e_{i,j}(k)|^2 - 1}$$

with $e_{i,j} = [\boldsymbol{\Gamma}_Y]_{i,j} + \frac{[\boldsymbol{\Gamma}_Y]_{i,j} - [\boldsymbol{\Gamma}_V]_{i,j}}{\mathrm{SNR}}$ folding the noise coherence into the standard Schwarz & Kellermann pairwise formulation, $f_{i,j} = [\boldsymbol{\Gamma}_Y]_{i,j} - [\boldsymbol{\Gamma}_R]_{i,j}$, and $g_{i,j} = \Re\{e_{i,j} f_{i,j}^*\}$. The array-wide CDR is the mean over all $M(M-1)/2$ pairs.

![[raw/papers/xiang-2025-wiener-gain-reverberant/figures/2e44d9b2d14b11ea57485c97378e981b78316fea3510e75d1539034583cf93ef.jpg|Signal processing diagram of the proposed approach]]
*Figure 1: Signal processing diagram — robust superdirective beamformer followed by the joint SNR/CDR Wiener post-filter.*

## Experimental Setup

### Simulation

| Item | Value |
|------|-------|
| Room | $6 \times 4 \times 3$ m, [[concepts/image-source-method|image-method]] RIRs |
| Array | 4-element uniform linear, 2 cm spacing |
| Source | Clean speech from TIMIT, 17 s, 16 kHz |
| Reverberation | $T_{60}$ from 140 ms to 1000 ms |
| Noise | Interference + diffuse + white (interference and diffuse each ≈ 6.5 dB relative to white) |
| STFT | 512-sample frames, 128 hop, Hanning window |
| Baselines | SD-SNR, SD-CDR, SD-TSNR, SD-HRNR (all gains applied to the superdirective output), AWPE |
| Metrics | Fullband SNR gain, LSD, DRR, SRMR, PESQ, kurtosis ratio (KR) |
| Hyperparameters | $\beta_1 = 5$, $\beta_2 = 3$ (reference condition: input SNR 5 dB, $T_{60} \approx 500$ ms) |

### Real-world experiments (added in the published version)

Experiments were conducted in a classroom of $12.6 \times 9.5 \times 4$ m with $T_{60} \approx 675$ ms. A 4-element uniform linear array (2 cm spacing, Panasonic WM-61A microphones, RME FireFace UFX III interface) was used; room impulse responses from the source (KRK Rokit7 G5 loudspeaker, 1.5 m source-to-microphone distance) were **measured with the spectral division method** and treated as ground truth for generating the observations, consistent with the simulation setup. Input SNR was controlled at 10 dB.

![[raw/papers/xiang-2025-wiener-gain-reverberant/figures/b50fca12f1aa59d58ca59e75dd0d815da06c87337f9f2e84eb13c277d5b58080.jpg|A photo of the 4-element uniform linear microphone array]]
*Figure 10: The 4-element uniform linear microphone array used in the real-world experiments.*

![[raw/papers/xiang-2025-wiener-gain-reverberant/figures/a3671ba159e1d9d06387c7cb5c1bf3e58dbef2716c51c17a855fa5ce7a015f43.jpg|A photo of the experimental setup]]
*Figure 11(b): Photo of the real-classroom experimental setup.*

## Results

**CDR estimation accuracy** (input SNR 20 dB, $T_{60} = 500$ ms, $M = 4$): the proposed noise-aware estimator shows lower estimation error than the SD-CDR approach of Schwarz & Kellermann, whose estimator ignores the additive-noise term.

![[raw/papers/xiang-2025-wiener-gain-reverberant/figures/029642f5c77a81bbba8d27231dd82af76f767b39ce5a2ff72d2917e1373d1420.jpg|The error between groundtruth and estimated CDRs]]
*Figure 2: Error between ground-truth and estimated CDRs — the proposed estimator vs. the noise-ignoring one.*

**Trade-off analysis** ($\beta_1, \beta_2$ swept 1–10): DRR increases with $\beta_1$ while SNR gain rises with $\beta_2$, saturating for $\beta_2 \geq 5$; reverberation suppression is most efficiently improved by $\beta_1$, at the price of LSD (distortion). LSD first decreases with $\beta_2$ (correlating with SNR-gain improvement) then increases — more SNR enhancement eventually means more distortion.

![[raw/papers/xiang-2025-wiener-gain-reverberant/figures/335506758c22bc6be7a3ff980868eac0873dc738b4181741abed6faa5fdd6386.jpg|DRR vs. SNR Gain as a function of beta1 and beta2]]
*(a) DRR vs. SNR gain.*
![[raw/papers/xiang-2025-wiener-gain-reverberant/figures/00f2653364210642a645e1f79723ac59c9b2135f7ed44bd73bd15aab4c559919.jpg|LSD vs. SNR Gain as a function of beta1 and beta2]]
*(b) LSD vs. SNR gain.*
*Figure 3: Trade-off curves of the proposed approach as a function of $\beta_1, \beta_2$ (input SNR = 5 dB, $T_{60} = 500$ ms), against baseline approaches.*

**Spectrograms** ($\beta_1 = 5$, $\beta_2 = 3$): the proposed approach effectively attenuates noise in the observations.

![[raw/papers/xiang-2025-wiener-gain-reverberant/figures/011cea195edde0eae8ee76a4cb13e186675616ffad99a9e1417a57524b7e6c2c.jpg|Spectrogram of the clean speech]]
*(a) Clean speech.*
![[raw/papers/xiang-2025-wiener-gain-reverberant/figures/d95dfb47caa31a7108ae8d69d02a0968710659926ab9ae6cb9b7bd357d3be8b8.jpg|Spectrogram of the noisy observation]]
*(b) Noisy observation (input SNR = 5 dB, $T_{60} = 500$ ms).*
![[raw/papers/xiang-2025-wiener-gain-reverberant/figures/04c9092c85aadf682b81ec27d578255a511345e7c6352f100d8f5d404d8a9402.jpg|Spectrogram of the filter output]]
*(c) Filter output (SNR gain = 11.4 dB).*
*Figure 4: Spectrograms of the clean, noisy, and enhanced signals.*

**Overall simulation comparison** (Table 1; input SNR 5 dB, $T_{60} \approx 500$ ms, $\beta_1 = 5$, $\beta_2 = 3$):

| Approach | SNR Gain | LSD | DRR |
|----------|----------|-----|-----|
| SD-SNR | 9.8 | 7.2 | 8.3 |
| SD-CDR | 8.6 | 8.1 | 9.2 |
| SD-TSNR | 10.2 | 7.4 | 8.5 |
| SD-HRNR | 10.1 | 8.0 | 8.7 |
| AWPE | — | 11.1 | — |
| **Proposed** | **11.4** | **7.2** | **9.3** |

The proposed gain achieves the best SNR gain and DRR and ties the best LSD. Across input SNRs, its DRR is nearly constant (CDR-driven, insensitive to noise level), and its SNR gain and LSD dominate at all conditions. Versus reverberation time, DRR of all methods declines with $T_{60}$ but the proposed one stays above the baselines (notably at $T_{60} = 200$–$500$ ms). AWPE's SRMR degrades rapidly as input SNR drops — high noise sensitivity — while the proposed approach outperforms it in jointly noisy and reverberant environments.

**PESQ** (Table 2, added in the published version) — the proposed approach attains the best PESQ in all four evaluated conditions:

| Condition | Observed | SD | SD-SNR | SD-CDR | SD-TSNR | SD-HRNR | AWPE | **Proposed** |
|-----------|----------|-----|--------|--------|---------|---------|------|----------|
| 200 ms, 20 dB | 2.02 | 2.11 | 2.87 | 2.59 | 2.77 | 2.73 | 2.09 | **2.90** |
| 200 ms, 10 dB | 1.22 | 1.32 | 2.09 | 1.70 | 1.95 | 1.90 | 1.34 | **2.16** |
| 500 ms, 20 dB | 1.62 | 1.63 | 1.84 | 1.90 | 1.84 | 1.83 | 1.84 | **1.96** |
| 500 ms, 30 dB | 1.89 | 1.91 | 1.95 | 2.12 | 1.96 | 1.95 | 2.08 | **2.12** |

![[raw/papers/xiang-2025-wiener-gain-reverberant/figures/8656862fda18183a8c38b6d07cb0ce9d8a9acdf8e16c434cfd42c93c29eff5e6.jpg|CDR]]
*(a) CDR.*
![[raw/papers/xiang-2025-wiener-gain-reverberant/figures/4bbe014afc93fce8411a8a19cb7c8f9f3321395c9ca9e3b65eba52d66077a311.jpg|SNR]]
*(b) SNR.*
![[raw/papers/xiang-2025-wiener-gain-reverberant/figures/b87391fac0fa2591c6ea2afeda1df4dc0e9fa74e3eb2666c01cd4f6bd4c0c2ea.jpg|Filter gain]]
*(c) Filter gain.*
*Figure 5: Time-frequency maps of the estimated CDR, SNR, and the resulting joint Wiener gain — the gain tracks both interferer fields.*

**Impact of $G_{\min}$**: the kurtosis ratio (musical-noise risk indicator) grows as $G_{\min}$ decreases; it is stable for $G_{\min} \geq 0.1$, making $G_{\min} = 0.1$ a prudent choice. The proposed gain's KR stays below SD-SNR, SD-TSNR, and SD-HRNR; the SD-CDR approach's KR is also minimal, but its inferior SNR gain leaves the proposed method ahead overall.

**Real-world validation** (Table 3, added in the published version; classroom, measured RIRs, input SNR 10 dB):

| Method | SNR Gain | LSD | DRR | PESQ |
|--------|----------|-----|-----|------|
| Observed | — | — | — | 1.28 |
| SD | 7.11 | 12.12 | 4.96 | 1.49 |
| SD-SNR | 9.31 | 9.49 | 5.23 | 1.57 |
| SD-CDR | 13.26 | 9.34 | 8.20 | 1.68 |
| SD-TSNR | 9.57 | 9.39 | 5.28 | 1.57 |
| SD-HRNR | 8.65 | 10.31 | 5.24 | 1.55 |
| AWPE | — | 9.31 | — | 1.50 |
| **Proposed** | **14.88** | **7.78** | **8.98** | **1.74** |

The proposed method outperforms all comparison methods on every metric in the real-classroom condition, aligning with the simulation findings. Notably, SD-CDR becomes a much stronger baseline with real measured RIRs (13.26 dB SNR gain vs. 8.6 dB in simulation) — yet the joint SNR–CDR gain still dominates it on all four metrics.

## Key Contributions

1. **Joint SNR–CDR Wiener gain**: a gain formulation that unifies the two classical degenerate Wiener gains (SNR-based and CDR-based) into a single post-filter covering noisy *and* reverberant environments, with per-bin weights $\alpha_R, \alpha_V$ that account for how the spatial filter leaks each interferer.
2. **Two-hyperparameter trade-off control**: $\beta_1$ and $\beta_2$ separately govern reverberation suppression and noise reduction, with a systematic empirical characterization of the resulting DRR/SNR-gain/LSD trade-off surface.
3. **Noise-aware DOA-independent CDR estimator**: extends the pairwise Schwarz & Kellermann estimator with an additive-noise coherence term $([\boldsymbol{\Gamma}_Y]_{i,j} - [\boldsymbol{\Gamma}_V]_{i,j})/\mathrm{SNR}$, lowering CDR estimation error in noisy reverberant fields and averaging over all sensor pairs.
4. **Musical-noise-aware gain floor analysis**: kurtosis-ratio-based study of $G_{\min}$ showing 0.1 as a stable operating point, with lower KR than SNR-driven baselines.
5. **Real-world experimental validation** (published version): classroom experiments with measured impulse responses and a PESQ evaluation across four $T_{60}$/SNR conditions confirm the simulation conclusions — the proposed gain is best on SNR gain, LSD, DRR, and PESQ simultaneously.

## Related Concepts

- [[concepts/snr-cdr-wiener-gain|SNR–CDR Wiener Gain]] — the paper's central contribution
- [[concepts/wiener-filter|Wiener Filter]] — the single-channel/optimal-filter root; the two degenerate gains
- [[concepts/coherent-to-diffuse-power-ratio|Coherent-to-Diffuse Power Ratio]] — CDR estimation extended with noise awareness
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]] — the Wiener beamformer = MVDR + Wiener gain decomposition this post-filter completes
- [[concepts/superdirective-beamforming|Superdirective Beamforming]] — the adopted robust spatial filter
- [[concepts/decision-directed-a-priori-snr|Decision-Directed a Priori SNR]] — SNR estimation stage
- [[concepts/spatial-coherence|Spatial Coherence]] — diffuse sinc coherence model for reverberation
- [[concepts/dereverberation|Dereverberation]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/diagonal-loading|Diagonal Loading]] — robustness of the superdirective filter
- [[concepts/image-source-method|Image-Source Method]] — RIR simulation

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] — the post-filter side of the MVDR + Wiener gain decomposition, with two-knob trade-off control in the SD-constrained lineage
