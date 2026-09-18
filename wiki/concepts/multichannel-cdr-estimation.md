---
type: concept
created: 2026-09-19
updated: 2026-09-19
sources:
  - raw/papers/xiang-2024-multichannel-cdr-estimation/full-text.md
tags:
  - speech-enhancement
  - dereverberation
  - cdr-estimation
  - coherence
  - multichannel
---

# Multichannel CDR Estimation

**Multichannel CDR estimation** extends coherent-to-diffuse power ratio (CDR) estimation from the classical two-microphone setting to arrays with $M > 2$ sensors, exploiting the redundant and complementary information across all sensors to improve estimation accuracy, dereverberation, and noise reduction. The central difficulty is that pairwise coherence estimates cannot simply be averaged across arbitrary microphone pairs: pairs with inconsistent sensor spacing and orientation have different diffuse-noise coherence models, so naive averaging can degrade rather than improve performance.

## Method Families

### GMSC-based estimation (Löllmann, Brendel & Kellermann 2020)

The [[concepts/generalized-magnitude-coherence|generalized magnitude-squared coherence (GMSC)]] of the signal pseudo-coherence matrix — its largest eigenvalue — represents the coherence function of signal and noise, enabling CDR estimation from all microphones simultaneously ([[sources/lollmann-2020-generalized-coherence-based-signal-enhancement|Löllmann et al. 2020]]).

### Effective-rank estimation (Löllmann, Brendel & Kellermann 2021)

ERANK estimates the diffuseness from the effective rank of the input covariance matrix and converts it to the CDR. It achieves competitive accuracy but has substantially higher computational complexity than coherence-based methods, due to a curve-fitting step that determines the coefficients of the inverse function.

### Weighted-average subarray estimation (Xiang et al. 2024)

The array is partitioned into $N$ groups of two-sensor subarrays such that subarrays within a group share identical spacing and orientation (hence identical diffuse-noise coherence $\gamma_{\mathrm{dn}}^{(n)}$). Per group, the pairwise correlation coefficients are averaged and a two-channel CDR estimator (any existing one) is applied; the group CDRs are fused by softmax-style weights

$$\hat{\beta} = \sum_{n=1}^{N} w_n \, g\!\left[\gamma_y^{(n)}, \gamma_{\mathrm{dn}}^{(n)}\right], \qquad w_n \propto e^{\zeta_0 g[\gamma_y^{(n)}, \gamma_{\mathrm{dn}}^{(n)}]}, \quad \zeta_0 = 0.1$$

This transforms multichannel CDR estimation into weighted two-channel estimation, adapts to any array geometry, and works with any pairwise CDR estimator as the inner $g(\cdot)$.

### Array manifold information-based estimation (Xiang et al. 2024)

Estimates the array manifold vector $\widehat{\mathbf{d}}$ (with $\|\widehat{\mathbf{d}}\|_2^2 = M$) via **joint diagonalization** — the [[concepts/generalized-eigenvalue-decomposition|generalized eigenvalue decomposition]] of $\boldsymbol{\Gamma}_{\mathrm{dn}}^{-1} \boldsymbol{\Gamma}_{\mathbf{y}}$ — taking the principal eigenvector $\mathbf{u}_1$ scaled as $\widehat{\mathbf{d}} = \frac{\sqrt{M}}{\|\mathbf{u}_1\|_2} \mathbf{u}_1$. The CDR then follows in closed form:

$$\hat{\beta} = \frac{\widehat{\mathbf{d}}^{\mathrm{H}} \boldsymbol{\Gamma}_{\mathbf{y}} \widehat{\mathbf{d}} - \widehat{\mathbf{d}}^{\mathrm{H}} \boldsymbol{\Gamma}_{\mathrm{dn}} \widehat{\mathbf{d}}}{M^2 - \widehat{\mathbf{d}}^{\mathrm{H}} \boldsymbol{\Gamma}_{\mathbf{y}} \widehat{\mathbf{d}}}$$

This estimator is DOA-free, needs no subarray decomposition, and relies only on the diffuse noise field assumption.

### Noise-aware pairwise averaging (Xiang et al. 2025)

The successor [[concepts/snr-cdr-wiener-gain|SNR–CDR Wiener gain]] work corrects each pairwise coherence observation by the noise coherence given the SNR and solves the unit-diagonal constraint on the source coherence matrix per sensor pair, averaging over all $M(M-1)/2$ pairs — targeting noisy rather than purely reverberant fields.

## Empirical Behavior

- **Scaling with $M$**: SNR gain, LSD, and DRR all improve from $M = 2$ to 16 (e.g., weighted-average postfilter SNR gain 7.58 → 15.09 dB at $T_{60} = 500$ ms, input SNR 5 dB); the advantage over two-channel and GMSC/ERANK baselines grows with $M$.
- **Accuracy**: both Xiang et al. 2024 estimators show much smaller estimation mse and higher error kurtosis (errors concentrated near zero) than averaged-coherence, GMSC, and ERANK baselines.
- **Noise insensitivity of DRR**: the DRR of CDR-driven postfilters varies minimally with input SNR, since the CDR estimate reflects the reverberation level, not the background noise.
- **Complexity**: weighted-average costs slightly more than averaged coherence; diagonalization-based is comparable to GMSC; ERANK is the most expensive (17-s signal runtimes: 11.37 s, 25.54 s, and 47.51 s respectively).
- **Real RIRs**: on measured MARDY impulse responses ($T_{60} = 447$ ms), the two Xiang et al. 2024 estimators achieve the best SNR gain (9.23 / 9.37 dB) and DRR among compared methods.

## Related Concepts

- [[concepts/coherent-to-diffuse-power-ratio|Coherent-to-Diffuse Power Ratio]] — the estimated quantity and its two-channel estimator families
- [[concepts/spatial-coherence|Spatial Coherence]] — pairwise coherence foundation and diffuse sinc model
- [[concepts/generalized-magnitude-coherence|Generalized Magnitude Coherence]] — eigenvalue-based multichannel coherence (GMSC baseline)
- [[concepts/generalized-eigenvalue-decomposition|Generalized Eigenvalue Decomposition]] — joint diagonalization for manifold estimation
- [[concepts/dereverberation|Dereverberation]] — primary application
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/snr-cdr-wiener-gain|SNR–CDR Wiener Gain]] — successor postfilter with noise-aware CDR

## Related Sources

- [[sources/xiang-2024-multichannel-cdr-estimation|Xiang, Lei, Pan, Chen & Benesty 2024: On Multichannel Coherent-to-Diffuse Power Ratio Estimation]] — introduces the weighted-average and array-manifold estimators
- [[sources/lollmann-2020-generalized-coherence-based-signal-enhancement|Löllmann, Brendel & Kellermann 2020: Generalized Coherence-Based Signal Enhancement]] — GMSC multichannel estimator
- [[sources/schwarz-2015-coherent-to-diffuse-power-ratio|Schwarz & Kellermann 2015: CDR Estimation for Dereverberation]] — the two-channel foundation extended by these methods
- [[sources/xiang-2025-wiener-gain-reverberant|Xiang, Chen, Benesty, Lei & Pan 2025: Design of the Wiener Gain in Noisy and Reverberant Environments]] — noise-aware pairwise CDR estimation and the joint SNR–CDR postfilter
