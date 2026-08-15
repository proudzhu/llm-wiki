---
type: concept
created: 2026-05-27
updated: 2026-08-15
sources:
  - raw/papers/jin-2017-multichannel-noise-reduction-mobile/full-text.md
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

## Related Concepts

- [[concepts/spatial-coherence|Spatial Coherence]]
- [[concepts/dereverberation|Dereverberation]]
- [[concepts/diffuse-sound-extraction|Diffuse Sound Extraction]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/wiener-filter|Wiener Filter]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/adaptive-coherence-noise-estimation|Adaptive Coherence Noise Estimation]] — global MMSE coherence-based noise variance decomposition (Jin et al. 2017)

## Key Sources

- [[sources/schwarz-2015-coherent-to-diffuse-power-ratio|Schwarz & Kellermann 2015: CDR Estimation for Dereverberation]] — foundational CDR estimation paper with unbiased estimators
- [[sources/lollmann-2020-generalized-coherence-based-signal-enhancement|Löllmann, Brendel & Kellermann 2020: Generalized Coherence-Based Signal Enhancement]] — GMC-based CDR estimator using eigenvalue decomposition for multi-microphone arrays
- [[sources/schwarz-2019-dereverberation-spatial-coherence|Schwarz 2019: Dereverberation and Robust Speech Recognition]] — comprehensive treatment of CDR methods
- [[sources/jin-2017-multichannel-noise-reduction-mobile|Jin, Taghizadeh, Chen & Xiao 2017: Multi-channel Noise Reduction for Hands-free Voice Communication on Mobile Phones]] — global MMSE coherence-based noise variance decomposition with adaptive coherence model
