---
type: concept
created: 2026-05-27
updated: 2026-09-19
sources:
  - raw/papers/jin-2017-multichannel-noise-reduction-mobile/full-text.md
  - raw/papers/taseska-2018-informed-spatial-filters/full-text.md
  - raw/papers/richard-2023-audio-signal-processing-21st-century/full-text.md
  - raw/papers/xiang-2025-wiener-gain-reverberant/full-text.md
  - raw/papers/xiang-2024-multichannel-cdr-estimation/full-text.md
tags:
  - signal-processing
  - spatial-audio
  - dereverberation
  - coherence
  - speech-enhancement
---

# Coherent-to-Diffuse Power Ratio (CDR)

**Coherent-to-Diffuse Power Ratio (CDR)**, also referred to as the direct-to-diffuse ratio, is the time-frequency-dependent power ratio between coherent (directional) and diffuse (non-directional) signal components in an acoustic scene. CDR estimation from spatial coherence measurements is a key technique for dereverberation, noise suppression, and spatial audio processing.

## Definition

For a two-microphone array, the CDR is defined as the ratio between the desired signal power $\Phi_s$ and the undesired diffuse/noise power $\Phi_n$:

$$\text{CDR}(l,f) = \frac{\Phi_s(l,f)}{\Phi_n(l,f)}$$

The CDR is related to the diffuseness $D$ by:

$$D = \frac{1}{\text{CDR} + 1}$$

## CDR from Spatial Coherence

The complex spatial coherence $\Gamma_x$ of the mixed signal relates to the CDR through the signal and noise coherence models:

$$\Gamma_x = \frac{\text{CDR} \cdot \Gamma_s + \Gamma_n}{\text{CDR} + 1}$$

where:
- $\Gamma_s$ is the direct signal coherence (a complex phasor $\Gamma_s = e^{j\omega\Delta t}$ determined by TDOA)
- $\Gamma_n$ is the diffuse noise coherence ($\Gamma_n = \sin(kd)/(kd)$ for 3D isotropic diffuse field)

## CDR Estimator Families

### DOA-dependent (require $\Gamma_s$ and $\Gamma_n$)

| Estimator | Equation | Property |
|-----------|----------|----------|
| Jeub | $\widehat{CDR} = \frac{|\hat\Gamma_x|^2 - \tilde\Gamma_n^2}{\tilde\Gamma_s^2 - |\hat\Gamma_x|^2}$ | Biased |
| Thiergart 1 | $\widehat{CDR} = \max(0, \text{Re}\{\frac{\tilde\Gamma_n - \hat\Gamma_x}{\hat\Gamma_x - \tilde\Gamma_s}\})$ | Unbiased, sensitive to phase |
| Proposed 1 (Schwarz) | $\widehat{CDR} = \max(0, \frac{\tilde\Gamma_s^*(\tilde\Gamma_n - \hat\Gamma_x)}{\text{Re}\{\tilde\Gamma_s^*\hat\Gamma_x\} - 1})$ | Unbiased |
| Proposed 2 (Schwarz) | $\widehat{CDR} = \left\|\frac{\tilde\Gamma_s^*(\tilde\Gamma_n - \hat\Gamma_x)}{\text{Re}\{\tilde\Gamma_s^*\hat\Gamma_x\} - 1}\right\|$ | Unbiased, best ASR performance |

### DOA-independent (require only $\Gamma_n$)

| Proposed 3 (Schwarz) | $\widehat{CDR}$ from solving $|\Gamma_s|=1$ | Unbiased, enables blind dereverberation |

### Noise-coherence-independent (require only $\Gamma_s$)

| Proposed 4 (Schwarz) | $\widehat{CDR} = \frac{\text{Im}\{\hat\Gamma_x\}}{\text{Im}\{\tilde\Gamma_s\} - \text{Im}\{\hat\Gamma_x\}}$ | Unbiased, requires TDOA $\neq$ 0 |

### Noise-aware DOA-independent (Xiang et al. 2025)

Xiang, Chen, Benesty, Lei & Pan 2025 extend the pairwise Schwarz & Kellermann estimator to **noisy** reverberant fields: given the SNR (from a decision-directed estimator), the observed-coherence term is corrected by the noise coherence,

$$e_{i,j} = [\boldsymbol{\Gamma}_Y]_{i,j} + \frac{[\boldsymbol{\Gamma}_Y]_{i,j} - [\boldsymbol{\Gamma}_V]_{i,j}}{\mathrm{SNR}}$$

and the unit-diagonal constraint on the source coherence matrix yields a closed-form CDR per sensor pair, averaged over all $M(M-1)/2$ pairs. Because existing CDR estimators ignore additive noise, they are biased when noise and reverberation coexist; the noise-aware variant shows lower estimation error at $M = 4$, $T_{60} = 500$ ms, input SNR 20 dB. A practical consequence: the DRR of the resulting Wiener post-filter stays nearly constant across input SNRs, since CDR estimation is barely influenced by the background noise level.

### Multichannel (M > 2) estimators (Xiang et al. 2024)

Xiang, Lei, Pan, Chen & Benesty 2024 extend CDR estimation beyond two microphones with two DOA-free estimators. **Weighted-average estimation** partitions the array into groups of two-sensor subarrays with consistent spacing and orientation, applies any two-channel estimator per group, and fuses the group CDRs with softmax-style weights. **Array manifold information-based estimation** jointly diagonalizes $\boldsymbol{\Gamma}_{\mathbf{y}}$ and $\boldsymbol{\Gamma}_{\mathrm{dn}}$ (GEVD of $\boldsymbol{\Gamma}_{\mathrm{dn}}^{-1}\boldsymbol{\Gamma}_{\mathbf{y}}$), takes the principal eigenvector as the scaled manifold vector $\widehat{\mathbf{d}}$, and solves the closed form

$$\hat{\beta} = \frac{\widehat{\mathbf{d}}^{\mathrm{H}} \boldsymbol{\Gamma}_{\mathbf{y}} \widehat{\mathbf{d}} - \widehat{\mathbf{d}}^{\mathrm{H}} \boldsymbol{\Gamma}_{\mathrm{dn}} \widehat{\mathbf{d}}}{M^2 - \widehat{\mathbf{d}}^{\mathrm{H}} \boldsymbol{\Gamma}_{\mathbf{y}} \widehat{\mathbf{d}}}$$

Both outperform the two-channel Schwarz method, averaged-coherence, GMSC, and ERANK baselines in estimation accuracy (mse, error kurtosis), SNR gain, LSD, and DRR, with the advantage growing with the number of microphones (validated up to $M = 16$). See [[concepts/multichannel-cdr-estimation|Multichannel CDR Estimation]] for the full method landscape.

## Geometric Interpretation

The signal coherence $\Gamma_s$, noise coherence $\Gamma_n$, and mixed coherence $\Gamma_x$ all lie on a straight line in the complex plane. $\Gamma_s$ lies on the unit circle, $\Gamma_n$ on the real axis, and $\Gamma_x$ lies between them at a position determined by the CDR. This geometric view enables intuitive understanding of estimator behavior and bias.

## Applications

| Application | Role of CDR |
|-------------|-------------|
| **Dereverberation** | CDR-driven postfilter gain for suppressing late reverberation |
| **Diffuse noise suppression** | Distinguishing directional target from diffuse noise |
| **Robust ASR** | Spatial feature extraction for reverberation-robust recognition |
| **Beamforming postfilter** | CDR-based Wiener postfilter for beamformer output |
| **Spatial audio coding** | Parametric representation of sound field diffuseness |

## Relation to Global Coherence-Based Noise Variance Decomposition

Jin et al. (2017) propose a related but distinct coherence-based decomposition for multi-channel noise PSD estimation. Rather than estimating a per-bin CDR ratio, they solve a **global least-squares problem** over all $P$ microphones to decompose the noise field into a coherent-diffuse component (variance $\sigma_c^2$) and an incoherent component (variance $\sigma_w^2$):

$$\mathbf{R} = \boldsymbol{\Phi} \boldsymbol{\sigma}, \quad \widehat{\boldsymbol{\sigma}} = \operatorname{real}(\boldsymbol{\Phi}^{\ddagger} \mathbf{R})$$

where $\mathbf{R}$ stacks the diagonal/off-diagonal entries of the noise covariance matrix and $\boldsymbol{\Phi}$ is built from the adaptive coherence model. This formulation is MMSE-optimal for $P > 2$, whereas classical CDR estimators typically operate on microphone pairs and average. The coherence model itself is initialized with the diffuse-field sinc function and **adaptively updated** during speech-absent frames (SPP $\rho < 0.1$), accommodating time-varying noise fields — a generalization of the static diffuse coherence assumption underlying classical CDR. See [[concepts/adaptive-coherence-noise-estimation|Adaptive Coherence Noise Estimation]] for the full method.

## CDR as a Priori Speech Absence Probability Control (Taseska & Habets 2018)

Taseska & Habets use the CDR not as a post-filter gain, but as a **control signal for the a priori Speech Absence Probability (SAP)** in a [[concepts/multichannel-mcra|multichannel MCRA]] noise-PSD-matrix estimator. The CDR is mapped via a sigmoid-like function to an a priori SAP that is robust to non-stationary noise: because desired speech is coherent across the array while background noise is approximately diffuse, a low CDR reliably indicates speech absence even when the noise properties change. This CDR-controlled a priori SAP yields more accurate noise PSD matrix estimates and better noise tracking in non-stationary conditions than single-channel and multichannel SNR-based SAPs (SC-Cohen, MC-Souden). The estimated noise PSD matrix and SPP then drive [[concepts/informed-spatial-filter|informed MVDR and MWF filters]]. This is a distinct application of CDR — as a *detector control* rather than a *spectral gain* — and was shown to be crucial where the pure-ML noise-PSD/SPP solution fails in non-stationary environments.

## Related Concepts

- [[concepts/spatial-coherence|Spatial Coherence]]
- [[concepts/dereverberation|Dereverberation]]
- [[concepts/diffuse-sound-extraction|Diffuse Sound Extraction]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/wiener-filter|Wiener Filter]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/adaptive-coherence-noise-estimation|Adaptive Coherence Noise Estimation]] — global MMSE coherence-based noise variance decomposition (Jin et al. 2017)
- [[concepts/informed-spatial-filter|Informed Spatial Filter (ISF)]] — CDR used as a priori SAP control for informed MVDR/MWF (Taseska & Habets 2018)
- [[concepts/multichannel-mcra|Multichannel MCRA]] — CDR-controlled a priori SAP for noise PSD matrix estimation
- [[concepts/snr-cdr-wiener-gain|SNR–CDR Wiener Gain]] — the post-filter that consumes the noise-aware CDR estimate
- [[concepts/multichannel-cdr-estimation|Multichannel CDR Estimation]] — extension of pairwise estimation to arrays with more than two sensors (Xiang et al. 2024)

## Key Sources

- [[sources/schwarz-2015-coherent-to-diffuse-power-ratio|Schwarz & Kellermann 2015: CDR Estimation for Dereverberation]] — foundational CDR estimation paper with unbiased estimators
- [[sources/lollmann-2020-generalized-coherence-based-signal-enhancement|Löllmann, Brendel & Kellermann 2020: Generalized Coherence-Based Signal Enhancement]] — GMC-based CDR estimator using eigenvalue decomposition for multi-microphone arrays
- [[sources/schwarz-2019-dereverberation-spatial-coherence|Schwarz 2019: Dereverberation and Robust Speech Recognition]] — comprehensive treatment of CDR methods
- [[sources/jin-2017-multichannel-noise-reduction-mobile|Jin, Taghizadeh, Chen & Xiao 2017: Multi-channel Noise Reduction for Hands-free Voice Communication on Mobile Phones]] — global MMSE coherence-based noise variance decomposition with adaptive coherence model
- [[sources/taseska-2018-informed-spatial-filters|Taseska 2018: Informed Spatial Filters for Speech Enhancement]] — CDR as a priori SAP control for multichannel MCRA noise PSD matrix estimation (Ch 3)
- [[sources/xiang-2025-wiener-gain-reverberant|Xiang, Chen, Benesty, Lei & Pan 2025: Design of the Wiener Gain in Noisy and Reverberant Environments]] — noise-aware DOA-independent pairwise CDR estimator
- [[sources/xiang-2024-multichannel-cdr-estimation|Xiang, Lei, Pan, Chen & Benesty 2024: On Multichannel Coherent-to-Diffuse Power Ratio Estimation]] — multichannel (M > 2) CDR estimators: weighted-average subarray fusion and array-manifold joint diagonalization

## Related Sources

- [[sources/richard-2023-audio-signal-processing-21st-century|Richard, Smaragdis, Gannot, Naylor, Makino, Kellermann & Sugiyama 2023: Audio Signal Processing in the 21st Century]]
