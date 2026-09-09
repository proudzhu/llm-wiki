---
type: source
created: 2026-09-09
updated: 2026-09-09
sources:
  - raw/papers/tervo-2009-sound-intensity-direction/full-text.md
  - zotero://select/items/0_4F8ZDGYE
tags:
  - sound-source-localization
  - doa-estimation
  - sound-intensity
  - array-processing
  - circular-statistics
  - signal-processing
---

# Tervo 2009: Direction Estimation Based on Sound Intensity Vectors

**Authors**: [[entities/sakari-tervo|Sakari Tervo]]
**Institution**: Helsinki University of Technology (TKK), Department of Media Technology, Finland
**Type**: Conference paper
**Published**: 17th European Signal Processing Conference (EUSIPCO 2009), Glasgow, Scotland, August 24–28, 2009, pp. 700–704, © EURASIP
**Zotero**: [4F8ZDGYE](zotero://select/items/0_4F8ZDGYE)

---

## Summary

A systematic comparison of **five direction-of-arrival estimation methods based on [[concepts/sound-intensity-vector|sound intensity vectors]]**, evaluated on real room impulse responses measured in a concert hall (Pori, Finland, reverberation time ≈ 2.1 s). The methods fall into two classes: simple circular-statistics estimators (circular mean CME, Cartesian mean MCA, circular median CMD) and **convolutive mixture models** that fit two-component wrapped distributions (von Mises mixture VMM, wrapped Gaussian mixture WGM) to the azimuth histogram of the intensity vectors. The mixture-model class performs slightly better overall and is markedly **more robust against additive noise**, with VMM the best method of the five; MCA — the only estimator that weights each frequency bin by the radial component of its intensity vector — is clearly the worst. This is one of the few pre-deep-learning empirical studies of intensity-vector DOA, and it quantifies exactly how these estimators degrade in a real reverberant hall.

## Problem Formulation

In a room, the signal at receiver $n$ is a convolutive mixture of the source signal with the propagation path plus measurement noise:

$$p_n(t) = h_n(t) * s(t) + w(t)$$

where $*$ denotes convolution and $w(t)$ is i.i.d. measurement noise. Unlike time-delay estimation (e.g., cross-correlation), which has been researched for decades, direction estimation from sound intensity vectors had not been widely compared — the paper's goal is to fill that gap with real concert-hall data.

### Sound Intensity from a Four-Microphone Square Grid

On a Cartesian axis $a$, the sound intensity in the frequency domain is

$$I_a(\omega) = \operatorname{Re}\{P^*(\omega)\, U_a(\omega)\}$$

with $P(\omega)$ the sound pressure, $U_a(\omega)$ the particle velocity, and $*$ the complex conjugate. Intensity vectors are obtained either from microphone-pair (p–p probe) measurements or from B-format signals; both introduce a directional **bias** (non-ideal directivity patterns in Soundfield microphones; non-constant pressure gradient within the sensor array in p–p probes).

For the four-microphone square grid of Figure 1, the pressure at the grid center is approximated as the microphone average, and the particle velocity along $x$ as a finite difference of the microphone pair along that axis:

$$P(\omega) \approx \frac{1}{4} \sum_{n=1}^{4} P_n(\omega), \qquad U_x(\omega) \approx \frac{-j}{\omega \rho_0 d}\big[P_1(\omega) - P_2(\omega)\big]$$

where $d$ is the microphone spacing, $\rho_0 = 1.2~\mathrm{kg/m^3}$ the median air density, and $j$ the imaginary unit. The $y$-component follows by replacing microphones 1 and 2 with 3 and 4.

![[raw/papers/tervo-2009-sound-intensity-direction/figures/fig01.png|Square grid with four microphones and coordinate system]]

*Figure 1: The square grid with four microphones and the coordinate system (azimuth $\theta$, radius $r$). Pressure is the average of the four microphones; particle velocity per axis is the finite difference of the pair along that axis.*

### Bias Compensation

Because the pressure signals are subtracted in the finite-difference velocity estimate, the intensity azimuth suffers a systematic, frequency-dependent bias. For the four-microphone square grid (after Kallinger et al.):

$$\theta_{\text{biased}} = \arctan\!\left( \frac{\sin\!\big(\tfrac{\omega d}{2c} \sin\theta\big)}{\sin\!\big(\tfrac{\omega d}{2c} \cos\theta\big)} \right)$$

with $c = 343~\mathrm{m/s}$. The inverse of this mapping has no closed form; following Kallinger et al., it is found by **linear interpolation**, and it exists only up to the frequency limit $f_{\max} = c/(d\sqrt{2})$. The compensated (unbiased) azimuth estimate at frequency bin $i$ is denoted $\theta_i$. Each intensity vector retains a radial component $r_i$ alongside its azimuth $\theta_i$; direction estimation operates on the set $\{(r_i, \theta_i)\}$ accumulated over frequency within one time frame.

## Methodology

The five estimators split into two classes: **direct** (simple averaging of the per-bin azimuths) and **mixture estimation** (fitting probability distributions to the azimuth data).

### Class 1: Circular Mean and Median

Because azimuths are circular data ($\theta_i \in (-\pi, \pi]$), plain averaging fails; the circular mean (CME) is

$$\hat{\theta}_{\text{CME}} = \arg \sum_{i=1}^{N} w_i e^{j\theta_i}$$

with weighting $w_i = 1/N$. Choosing instead $w_i = r_i$ (the radial intensity component) makes the CME equal to the **mean of the Cartesian presentation** (MCA):

$$\arg \sum_{i=1}^{N} r_i e^{j\theta_i} = \arctan \frac{\mathbb{E}\{I_y\}}{\mathbb{E}\{I_x\}} =: \hat{\theta}_{\text{MCA}}$$

The circular median (CMD) is defined analogously, mediating the real and imaginary parts separately:

$$\hat{\theta}_{\text{CMD}} = \arg\Big( \operatorname{Me}\big\{\operatorname{Re}\{w_i e^{j\theta_i}\}\big\} + j\, \operatorname{Me}\big\{\operatorname{Im}\{w_i e^{j\theta_i}\}\big\} \Big)$$

with $w_i = 1/N$ (the circular mode is a possible alternative but is not considered).

### Class 2: Mixture Models (VMM, WGM)

The azimuth histogram of the intensity vectors within a frame is a **mixture of two distributions**: a concentrated component caused by the sound source and a broad component modeling the noise floor (Figure 2). The shape of both depends on the room impulse response and the source spectrum; each additional source introduces a further component. Since azimuth is circular, wrapped distributions are fitted.

The **von Mises** (VM) distribution:

$$f_{\text{VM}}(\theta \mid \mu, \kappa) = \frac{e^{\kappa \cos(\theta - \mu)}}{2\pi\, I(0, \kappa)}$$

where $\kappa$ measures concentration, $\mu$ is the mean, and $I(0, \kappa)$ is the modified Bessel function of order 0. The **wrapped Gaussian** (WG) distribution:

$$f_{\text{WG}}(\theta \mid \mu, \sigma) = \frac{1}{\sqrt{2\pi\sigma^2}} \sum_{k=-K}^{K} e^{-\frac{(\theta - \mu - 2\pi k)^2}{2\sigma^2}}, \qquad K = 2$$

The two-component mixture is

$$p(\theta \mid \boldsymbol{\mu}, \boldsymbol{\rho}) = \sum_{m=1}^{M} a_m f^{(m)}(\theta \mid \mu_m, \rho_m), \qquad a_m = \tfrac{1}{M}, \quad M = 2$$

with $f = f_{\text{VM}}$ for VMM and $f = f_{\text{WG}}$ for WGM, and $\boldsymbol{\rho}$ collecting the shape parameters ($\kappa$ or $\sigma$). The estimated source direction is the mean $\mu$ of the **more concentrated** component. Parameters are found by maximum likelihood,

$$L(\boldsymbol{\mu}, \boldsymbol{\rho}) = \sum_{i=1}^{N} \log p(\theta_i \mid \boldsymbol{\mu}, \boldsymbol{\rho})$$

maximized with MATLAB's `fminsearch` (Nelder–Mead); expectation–maximization is noted as a potentially better-suited alternative.

![[raw/papers/tervo-2009-sound-intensity-direction/figures/fig02.png|Histogram of estimated azimuth angles with von Mises and wrapped Gaussian mixture fits]]

*Figure 2: Normalized histogram of the estimated azimuth angles (top), the von Mises mixture model fit (middle), and the wrapped Gaussian mixture model fit (bottom), with mixture components shown separately. Vertical lines mark the true source angle $\theta_s = -19^\circ$ and the estimates $\hat{\theta}_{\text{VMM}} = -23^\circ$, $\hat{\theta}_{\text{WGM}} = -22^\circ$ (source S3, receiver R2).*

## Experimental Setup

| Item | Value |
| --- | --- |
| Microphone array | Two four-microphone square grids sharing the same center: $d = 10~\mathrm{mm}$ (used 1–5 kHz) and $d = 100~\mathrm{mm}$ (used 100 Hz–1 kHz); bias compensation applied separately per grid |
| Room | Concert hall of Pori, Finland — 700 seats, reverberation time ≈ 2.1 s; measured impulse responses at 48 kHz |
| Geometry | 3 source positions (S1–S3) × 3 receiver positions (R1–R3); omnidirectional loudspeaker, 26 cm diameter, 12 driver elements |
| Source signals | 2 s of violin and 2 s of white noise, each convolved with the measured RIRs |
| Noise | Additive white noise; SNR varied 0–40 dB |
| Framing | 1024-sample frames, 50 % overlap → 187 frames per condition; FFT size 8192; 837 bins used (100 Hz–5 kHz) |
| Estimates | 187 frames × 9 source/receiver conditions = 1683 direction estimates per method and SNR |
| Metrics | Anomaly: $|\hat{\theta}_i - \theta_s| > 30^\circ$; PAN = percentage of anomalies; circular bias $\mu_\theta = \arg \sum_i e^{j(\tilde{\theta}_i - \theta_s)}$ and circular standard deviation $\sigma_\theta = \big[2\big(1 - \tfrac{1}{\tilde{N}}\big|\sum_i e^{j(\tilde{\theta}_i - \theta_s)}\big|\big)\big]^{1/2}$ over the $\tilde{N}$ non-anomalous estimates |

The broadband split between the two grids respects the bias-compensation limit $f_{\max} = c/(d\sqrt{2})$: ≈ 2.4 kHz for $d = 100~\mathrm{mm}$ and ≈ 24 kHz for $d = 10~\mathrm{mm}$ — the large grid covers low frequencies, the small grid high frequencies.

![[raw/papers/tervo-2009-sound-intensity-direction/figures/fig03.png|Receiver and source positions in the concert hall of Pori]]

*Figure 3: Receiver (R) and source (S) positions in the concert hall of Pori. Receiver positions R1–R3 and source positions S1–S3 were used in the experiments.*

## Results

![[raw/papers/tervo-2009-sound-intensity-direction/figures/fig04.png|Bias, standard deviation and percentage of anomalies vs SNR, white noise source]]

*Figure 4: Bias (top), standard deviation (middle), and percentage of anomalies (bottom) of the non-anomalous estimates against SNR. White-noise source signal, reverberation time ≈ 2.1 s.*

![[raw/papers/tervo-2009-sound-intensity-direction/figures/fig05.png|Bias, standard deviation and percentage of anomalies vs SNR, violin source]]

*Figure 5: Bias (top), standard deviation (middle), and percentage of anomalies (bottom) against SNR. Violin source signal, reverberation time ≈ 2.1 s.*

- **Mixture models win.** VMM and WGM perform best in all conditions; VMM has the lowest total number of anomalies and is the most robust method against additive noise — in the harder violin conditions (Fig. 5) VMM stays below 50 % anomalies everywhere. Even when total noise energy exceeds the source energy, VMM still isolates the source-caused distribution, because the noise distribution has much lower concentration than the source distribution.
- **Averaging methods are close but worse.** The best class-1 estimator is CME; the gap between mixture models and the simple averaging methods CME/CMD is "not drastic".
- **MCA is clearly worst** — PAN ≈ 38 % even at the highest SNR. The failure is attributed to the radial-component weighting: dropping the weighting (CME) brings the estimate close to the true direction. Tervo suggests selecting subsets of azimuth/radial components or maximum-likelihood weighting of the cross-spectral components (as in time-delay estimation) as remedies.
- **Bias is small for all methods** (< 4° in all cases). Curiously, with the white-noise source the bias *increases* with SNR — at high SNR the residual error is reverberation-induced, possibly compounded by microphone non-idealities; the violin signal shows the opposite trend. Standard deviation decreases with SNR as expected.
- **Broadband sources help.** White noise, having energy at all frequencies, yields more robust and accurate direction estimates than the violin signal.

## Key Contributions

1. **First broad empirical comparison of intensity-vector DOA methods**: five estimators (CME, MCA, CMD, VMM, WGM) evaluated on real concert-hall data (RT ≈ 2.1 s) across SNR 0–40 dB, two source signals, and nine source/receiver geometries — 1683 estimates per method and condition.
2. **Two-class taxonomy** of intensity-vector direction estimation: direct circular-statistics averaging vs. convolutive mixture-model fitting, with the finding that mixture models (especially von Mises) are slightly more accurate and substantially more noise-robust.
3. **Negative result on radial weighting**: MCA's intensity-magnitude weighting is shown to be actively harmful for continuous-signal DOA (worst method in all conditions), motivating selective or ML-based weighting schemes instead.
4. **Practical bias-compensation recipe** for broadband four-microphone square grids: linear-interpolation inversion of the finite-difference bias function, with two grid sizes split at the $f_{\max} = c/(d\sqrt{2})$ validity limit (100 mm for 100 Hz–1 kHz, 10 mm for 1–5 kHz).

## Limitations and Caveats

- Single source only ($M = 2$ mixture components: source + noise floor); multi-source scenarios would require more components and source counting.
- Azimuth only — the square grid gives a 2-D intensity vector; elevation is not estimated.
- One concert hall and one loudspeaker; generalization to other rooms is untested.
- Frame-based (1024 samples ≈ 21 ms at 48 kHz) with 8192-point FFT zero-padding — the per-frame azimuth histogram needs enough active bins; sparse-source signals (violin) degrade all methods.
- The unexpected bias-vs-SNR trend for white noise is acknowledged as unexplained.

## Related Concepts

- [[concepts/sound-intensity-vector|Sound Intensity Vector]] — the physical quantity and its p–p probe estimation, central to this paper
- [[concepts/intensity-vector-doa-estimation|Intensity-Vector DOA Estimation]] — the five-method taxonomy and comparison results
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]] — the general problem
- [[concepts/sound-source-localization|Sound Source Localization]] — umbrella field
- [[concepts/gaussian-mixture-model|Gaussian Mixture Model]] — WGM is the wrapped, circular analog
- [[concepts/room-impulse-response|Room Impulse Response]] — the concert-hall measurement data
- [[concepts/ambisonics|Ambisonics]] — B-format signals are the other route to intensity vectors

## Related Sources

- [[sources/grumiaux-2022-ssl-deep-learning-survey|Grumiaux et al. 2022: A Survey of SSL with Deep Learning Methods]] — classifies intensity-based features/methods among conventional SSL approaches; Tervo 2009 provides the pre-DL empirical comparison the survey references only briefly
