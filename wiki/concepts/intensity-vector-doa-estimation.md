---
type: concept
created: 2026-09-09
updated: 2026-09-09
sources:
  - raw/papers/tervo-2009-sound-intensity-direction/full-text.md
tags:
  - doa-estimation
  - sound-intensity
  - circular-statistics
  - sound-source-localization
---

# Intensity-Vector DOA Estimation

**Intensity-vector DOA estimation** determines the direction of a sound source from the set of [[concepts/sound-intensity-vector|sound intensity vectors]] accumulated over frequency bins within a time frame. Each vector contributes a radial component $r_i$ (magnitude) and an azimuth $\theta_i$ (bias-compensated). Because azimuths are circular data, the estimators are built on circular statistics or on wrapped probability distributions. Tervo (EUSIPCO 2009) organizes the field into two classes and compares five methods on real concert-hall data — one of the few systematic pre-deep-learning evaluations of this family.

## Class 1: Direct Averaging (Circular Statistics)

- **CME (circular mean)**: $\hat{\theta}_{\text{CME}} = \arg \sum_{i=1}^{N} w_i e^{j\theta_i}$ with uniform weights $w_i = 1/N$.
- **MCA (mean of the Cartesian presentation)**: choosing $w_i = r_i$ makes the circular mean equal to the arctangent of expected Cartesian intensity components, $\arctan\big(\mathbb{E}\{I_y\}/\mathbb{E}\{I_x\}\big)$ — i.e., energy-weighted averaging.
- **CMD (circular median)**: median of the real and imaginary parts of $w_i e^{j\theta_i}$ taken separately, $w_i = 1/N$.

## Class 2: Convolutive Mixture Models

The per-frame azimuth histogram is a **mixture**: a concentrated component caused by the source plus a broad component modeling the noise floor (each additional source adds a further component). A two-component wrapped mixture is fitted by maximum likelihood (Nelder–Mead or EM), and the source direction is the mean $\mu$ of the more concentrated component:

- **VMM**: von Mises mixture, $f_{\text{VM}}(\theta\mid\mu,\kappa) = e^{\kappa\cos(\theta-\mu)} / (2\pi I(0,\kappa))$ — $\kappa$ is the concentration.
- **WGM**: wrapped Gaussian mixture, $K = 2$ wrappings of $\mathcal{N}(\mu, \sigma^2)$.

## Empirical Comparison (Tervo 2009, concert hall, RT ≈ 2.1 s, SNR 0–40 dB)

| Method | Class | Verdict |
| --- | --- | --- |
| **VMM** | Mixture | **Best overall** — lowest total anomaly rate; < 50 % anomalies in all violin conditions; most robust to additive noise because the noise distribution stays low-concentration even when noise energy exceeds source energy |
| WGM | Mixture | Close second — slightly better than averaging methods in all conditions |
| CME | Averaging | Best of class 1; gap to mixture models "not drastic" |
| CMD | Averaging | Similar to CME |
| **MCA** | Averaging | **Clearly worst** — ≈ 38 % anomalies even at the highest SNR |

Key lessons:

1. **Mixture fitting beats simple averaging** on accuracy and especially on noise robustness — the concentrated-vs-broad decomposition actively separates source from noise rather than averaging them together.
2. **Radial (energy) weighting is harmful**: MCA's $w_i = r_i$ weighting lets high-energy bins — often reverberation- or noise-dominated — dominate the estimate. Uniform weighting (CME) lands close to the true direction. Remedies: selecting subsets of azimuth/radial components, or maximum-likelihood weighting of cross-spectral components as in time-delay estimation.
3. **Bias is small but reverberation-limited**: all methods stay under 4° circular bias; with a broadband (white-noise) source the residual bias *grows* with SNR because at high SNR reverberation — not additive noise — dominates the error.
4. **Broadband sources are easier**: white noise outperforms violin (sparse spectrum) for every method, since all frequency bins contribute evidence.

## Relation to Other DOA Families

Unlike [[concepts/search-based-doa-estimation|search-based methods]] (SRP-PHAT, MUSIC) that scan a spatial grid of delay-and-sum or subspace spectra, intensity-vector methods read direction off a physical energy-flow quantity measured by a compact probe — no steering, no grid, small apertures. The [[sources/grumiaux-2022-ssl-deep-learning-survey|Grumiaux et al. 2022 survey]] notes classical intensity methods degrade quickly under reflections; Tervo's concert-hall data quantifies that degradation and shows mixture-model fitting recovers a substantial part of it. In modern DNN systems, intensity vectors survive as **input features** (FOA active/reactive intensity in SELD/ACCDOA) rather than as the estimator itself.

## Related Concepts

- [[concepts/sound-intensity-vector|Sound Intensity Vector]] — the measured quantity, probe geometries, bias compensation
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]] — the general problem
- [[concepts/sound-source-localization|Sound Source Localization]] — umbrella field
- [[concepts/search-based-doa-estimation|Search-Based DOA Estimation]] — contrasting grid-scanning family
- [[concepts/gaussian-mixture-model|Gaussian Mixture Model]] — WGM is the wrapped circular analog
- [[concepts/activity-coupled-cartesian-doa|ACCDOA]] — modern DNN representation consuming intensity-vector features

## Related Sources

- [[sources/tervo-2009-sound-intensity-direction|Tervo 2009: Direction Estimation Based on Sound Intensity Vectors]] — the five-method comparison defining this page's taxonomy
- [[sources/grumiaux-2022-ssl-deep-learning-survey|Grumiaux et al. 2022: A Survey of SSL with Deep Learning Methods]] — positions intensity methods among conventional SSL approaches and DL feature families
