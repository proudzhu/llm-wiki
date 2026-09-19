---
type: concept
created: 2026-04-25
updated: 2026-09-19
sources:
  - raw/papers/pan-2026-array-self-awareness/full-text.md
  - raw/papers/lollmann-2020-generalized-coherence-based-signal-enhancement/full-text.md
  - raw/papers/schwarz-2015-coherent-to-diffuse-power-ratio/full-text.md
  - raw/papers/jin-2017-multichannel-noise-reduction-mobile/full-text.md
  - raw/papers/yan-2014-dual-mic-bt-noise-reduction/full-text.md
  - raw/papers/richard-2023-audio-signal-processing-21st-century/full-text.md
  - raw/papers/xiang-2025-wiener-gain-reverberant/full-text.md
  - raw/papers/xiang-2024-multichannel-cdr-estimation/full-text.md
tags:
  - signal-processing
  - multichannel
  - dereverberation
  - spatial-processing
---

# Spatial Coherence

**Spatial coherence** describes the degree of spatial correlation between multichannel signals, and is a key tool for distinguishing coherent sound sources (direct sound) from diffuse sound fields (reverberation, noise).

## Definition

The spatial coherence between two sensor signals is defined as the normalized form of the cross power spectral density:

$$\Gamma_{x_1 x_2}(\omega) = \frac{S_{x_1 x_2}(\omega)}{\sqrt{S_{x_1 x_1}(\omega) \cdot S_{x_2 x_2}(\omega)}}$$

where $S_{x_1 x_2}$ is the cross power spectral density, and $S_{x_1 x_1}$ and $S_{x_2 x_2}$ are the auto power spectral densities.

## Coherence Model of the Diffuse Sound Field

For an isotropic diffuse sound field (late reverberation), the theoretical coherence between two omnidirectional microphones is:

$$\Gamma_{\text{diff}}(\omega) = \frac{\sin(kd)}{kd}$$

where $k = \omega/c$ is the wavenumber and $d$ is the microphone spacing. This predictable pattern makes it possible to distinguish direct sound from reverberation using coherence measurements alone.

## Coherence-to-Diffuse Ratio (CDR)

The Coherence-to-Diffuse Ratio (CDR) is a power ratio derived from the spatial coherence estimate:

$$\text{CDR} = \frac{|\Gamma_{x_1 x_2}|^2 - |\Gamma_{\text{diff}}|^2}{1 - |\Gamma_{x_1 x_2}|^2}$$

CDR > 0 indicates that the coherent component (direct sound) dominates, while CDR < 0 indicates that the diffuse component (reverberation) dominates.

Classical CDR estimators assume a noise-free sound field and are therefore biased in environments where noise and reverberation coexist. [[sources/xiang-2025-wiener-gain-reverberant|Xiang et al. 2025]] fold the noise coherence and the decision-directed SNR into the Schwarz & Kellermann DOA-independent pairwise estimator, yielding a **noise-aware** CDR estimate that drives the [[concepts/snr-cdr-wiener-gain|joint SNR–CDR Wiener gain]] after a robust superdirective beamformer, suppressing noise and reverberation simultaneously.

## Adaptive Coherence Model

In theory, the coherence of a diffuse sound field is given by the sinc function (Eq. $\Gamma_{\text{diff}}$), but on real mobile devices, the non-omnidirectional characteristics of microphones and reflections from the device housing cause measured coherence to deviate from the theoretical model. In multichannel noise estimation, Jin et al. (2017) proposed using the sinc model as an **initialization**, and adaptively updating the coherence function during speech-absent frames (SPP $\rho < 0.1$):

$$\gamma_{pq}(\tau, \omega) = \alpha_\gamma \gamma_{pq}(\tau - 1, \omega) + (1 - \alpha_\gamma) \frac{\Phi_{pq}}{\sqrt{\Phi_{pp} \Phi_{qq}}}, \quad \rho < 0.1$$

where $\alpha_\gamma = 0.9$. This adaptive scheme allows the noise coherence model to track time-varying noise fields rather than relying on static assumptions of a fully diffuse or fully incoherent field (the limitation of Zelinski/McCowan). The updated coherence function is used both: (i) in a least-squares global solution of an MMSE decomposition of noise variances (coherent-diffuse component $\sigma_c^2$ and incoherent component $\sigma_w^2$); and (ii) to adaptively determine the crossover frequency between single- and multichannel noise estimation (the frequency where $|\gamma|^2 = 0.5$). See [[concepts/adaptive-coherence-noise-estimation|Adaptive Coherence Noise Estimation]].

## Multichannel Generalization: GMC

Löllmann et al. (2020) generalized coherence-based signal enhancement from microphone pairs to $N$ channels: the **Generalized Magnitude Coherence (GMC)** is computed via an eigendecomposition of the $N \times N$ coherence matrix, and is used to estimate the per-channel CDR. The signal to be enhanced is the "most suitable" microphone signal — implicitly selected by the principal eigenvector, without DOA estimation. In a 4-microphone binaural hearing-aid scenario, this scheme consistently outperforms the DOA-independent two-channel CDR estimators of Schwarz/Thiergart et al., see [[sources/lollmann-2020-generalized-coherence-based-signal-enhancement|Löllmann et al. 2020]].

## Coherence Matrices as Source Definitions

Recent work uses the full $M \times M$ coherence matrix not merely as a noise model but as the *definition* of a source: if the coherence matrices of the interferences and background noise are known a priori (estimable from several seconds of past observations, or blindly from BSS demixing matrices), the time-varying source variances follow efficiently under the maximum-likelihood principle. [[sources/pan-2026-array-self-awareness|Pan, Chen & Benesty 2026]] push this to [[concepts/array-self-awareness|array self-awareness]]: the coherence matrix of a *never-seen* source is recovered from the [[concepts/covariance-matrix-residual-model|residual model]] of the observation covariance matrix after the known components are subtracted, letting the array detect and extract new, moving, or sporadic sources in real time. A notable counterintuitive finding: reverberation *helps* this discrimination — reflections enrich the coherence matrices and make sources easier to distinguish, shrinking the failure region relative to anechoic conditions.

## Applications

| Application | Principle |
|------|------|
| **Dereverberation** | Use diffuse-field coherence models to estimate late reverberation power and construct a spectral gain |
| **Noise reduction** | Distinguish coherent target sources from diffuse noise |
| **Robust ASR** | Extract spatial feature vectors from short-time coherence as DNN input |
| **Beamforming assistance** | CDR estimation can serve as a post-filter for MVDR/MWF |
| **Two-microphone noise reduction** | Measured coherence functions (or CPSD forms with the noise cross-spectrum subtracted) serve directly as spectral gains — speech-correlated noise degrades performance, and noise cross-spectrum estimation is critical, see [[concepts/coherence-based-noise-reduction|Coherence-Based Noise Reduction]] |

## Relationship to Other Concepts

- [[beamforming|Beamforming]]: spatial filtering, complementary to coherence estimation
- [[wiener-filter|Wiener Filter]]: CDR can construct the post-filter gain of a multichannel Wiener filter
- [[mclp|MCLP]]: a different dereverberation paradigm — MCLP performs linear prediction, coherence performs spectral masking
- [[deep-learning-for-signal-processing|Deep Learning for Signal Processing]]: spatial features as DNN input

## Key Literature

- [[sources/schwarz-2015-coherent-to-diffuse-power-ratio|Schwarz & Kellermann 2015]] — foundational work on CDR estimation, proposing the unbiased CDR estimator and the DOA-independent dereverberation system
- [[sources/schwarz-2019-dereverberation-spatial-coherence|Schwarz 2019]] — doctoral thesis systematically studying spatial coherence models for dereverberation and ASR
- [[sources/liu-2026-scm-reconstruction-speech-enhancement|Liu 2026]] — uses the diffuse-field coherence matrix $\Gamma_d$ as a predefined basis, reconstructing the SCM via variance-ratio estimation
- [[sources/jin-2017-multichannel-noise-reduction-mobile|Jin et al. 2017]] — uses the sinc diffuse-field coherence as an initialization, adaptively updating the coherence function during speech-absent frames, for multichannel noise PSD estimation and crossover-frequency selection
- [[sources/lollmann-2020-generalized-coherence-based-signal-enhancement|Löllmann et al. 2020]] — N-channel Generalized Magnitude Coherence (GMC): CDR estimated via eigendecomposition of the coherence matrix, with the principal eigenvector implicitly selecting the enhanced channel
- [[sources/xiang-2025-wiener-gain-reverberant|Xiang et al. 2025]] — noise-aware DOA-independent CDR estimation: folds noise coherence and SNR into the pairwise estimator, driving the joint SNR–CDR Wiener gain
- [[sources/pan-2026-array-self-awareness|Pan, Chen & Benesty 2026]] — coherence matrices as source definitions: the coherence matrix of a never-seen source is recovered from the covariance-matrix residual, enabling real-time detection of new, moving, and sporadic sources
- [[sources/richard-2023-audio-signal-processing-21st-century|Richard, Smaragdis, Gannot, Naylor, Makino, Kellermann & Sugiyama 2023: Audio Signal Processing in the 21st Century]]
