---
type: source
created: 2026-05-13
updated: 2026-05-13
sources:
  - raw/papers/seo-2016-feedback-anc-constrained-optimization/full-text.md
  - https://doi.org/10.1109/ICCE-Asia.2016.7804751
  - zotero://select/items/0_926LI9YV
tags:
  - feedback-anc
  - constrained-optimization
  - frequency-warping
  - headphone
  - earphone
  - low-order-filter
  - robust-stability
---

# Seo, Park & Youn 2016: Feedback ANC via Constrained Optimization for Headphones

**Authors**: [[../entities/ji-ho-seo|Ji-ho Seo]]¹, [[../entities/young-cheol-park|Young-cheol Park]]², [[../entities/dae-hee-youn|Dae Hee Youn]]¹

**Affiliations**: ¹ Department of Electrical and Electronic Engineering, Yonsei University, Seoul, Korea; ² Computer & Telecommunication Engineering Division, Yonsei University, Wonju, Korea

**Venue**: 2016 IEEE International Conference on Consumer Electronics-Asia (ICCE-Asia), pp. 1–4

**Year**: 2016

**Type**: Conference Paper

**DOI**: [10.1109/ICCE-Asia.2016.7804751](https://doi.org/10.1109/ICCE-Asia.2016.7804751)

**Zotero**: [zotero://select/items/0_926LI9YV](zotero://select/items/0_926LI9YV)

## Summary

This paper presents an efficient method for designing low-order feedback ANC filters using constrained optimization in the warped frequency domain. By combining Q-parameterization with frequency warping, the proposed 16th-order WFIR filter achieves nearly the same noise attenuation (~19dB) as a conventional 128th-order FIR filter at low frequencies, while maintaining robust stability across different acoustic plants.

## Problem Formulation

The feedback ANC system minimizes the error signal variance via the sensitivity function:

$$S = \frac{1}{1 + CP}$$

where $C$ is the noise control filter, $P$ is the actual acoustic plant, and $S$ is the sensitivity function. High sampling rates (48kHz) in headphone applications require high-order FIR filters for reasonable low-frequency attenuation, which is computationally expensive for low-power devices.

## Methodology

### Q-Parameterization with Frequency Warping

The method formulates the optimization problem using Q-parameterization and frequency discretization, solved via sequential quadratic programming. The unit delay is replaced by an all-pass element:

$$\tilde{z}^{-1} = \frac{z^{-1} - \lambda}{1 - \lambda z^{-1}}$$

where $\lambda$ is the warping parameter (larger $\lambda$ = better low-frequency resolution).

### Cost Function

$$\min \frac{1}{L} \sum_{k=0}^{L-1} \left| \left(1 - Q_w(k) P_{0,w}(k)\right) W_{1,w}(k) \right|^2$$

s.t. $\left|Q_w(k)P_{0,w}(k)W_{2,w}(k)\right| < 1$

$\left| \left(1 - Q_w(k) P_{0,w}(k)\right) W_{3,w}(k) \right| < 1$

where:
- $W_{1,w}(k)$: band-pass weighting for control band (low-pass, cutoff 400Hz)
- $W_{2,w}(k)$: robustness constraint for plant perturbation (high-pass, cutoff 4kHz)
- $W_{3,w}(k)$: noise boosting threshold (0.7071 = max 3dB boosting)

### Final Control Filter

$$C_w = \frac{Q_w}{1 - Q_w P_{0,w}}$$

The nominal plant $p_0(n)$ is obtained via ARMA modeling (15 AR + 15 MA coefficients) from the measured actual plant.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Sampling frequency | 48kHz |
| Actual plant | BOSE ANC headphone secondary path (128 taps) |
| Nominal plant | ARMA model (15 AR + 15 MA) |
| FIR filter order | 128 |
| WFIR filter order | 16 |
| Warping parameters | $\lambda = 0.8, 0.85$ |
| FFT size | 512 |
| $W_1$ cutoff | 400Hz (Butterworth LP) |
| $W_2$ cutoff | 4kHz (Butterworth HP) |
| $W_3$ threshold | 0.7071 (3dB max boosting) |

## Results

- **16th-order WFIR** achieves ~19dB maximum attenuation, nearly matching **128th-order FIR** at frequencies < 1kHz
- Maximum 3dB noise boosting (waterbed effect constraint)
- Larger $\lambda$ (0.85) improves low-frequency attenuation but increases boosting — trade-off
- Robust performance across different acoustic plants (1-3dB variation)
- WFIR outperforms 8th-order IIR approximation even with frequency warping applied to IIR

![System block diagram](raw/papers/seo-2016-feedback-anc-constrained-optimization/figures/8c0c30e82e82a12884b0a0e5f30bb672f46239e7a096513a7d08b412333055fc.jpg)

*Figure 1: Block diagram of the proposed ANC filter design algorithm.*

![Sensitivity function comparison](raw/papers/seo-2016-feedback-anc-constrained-optimization/figures/e8392c1710a7f3b78b2ebe2fc1311e38ac9d4bfa5a7585bb35c882d372289aa0.jpg)

*Figure 4: Sensitivity function (upper) and error spectra (lower) — 128th FIR vs 16th WFIR.*

## Key Contributions

1. **Low-order WFIR filter design** via constrained optimization in warped frequency domain — 16th order achieves performance of 128th-order FIR
2. **Frequency warping integration** with Q-parameterization for improved low-frequency resolution without increasing filter order
3. **Robust stability** across different acoustic plants via multiplicative uncertainty modeling
4. **Tunable warping parameter** $\lambda$ for trade-off between attenuation and boosting performance

## Related Concepts

- [[../concepts/feedback-anc|Feedback ANC]]
- [[../concepts/frequency-warping|Frequency Warping]]
- [[../concepts/warped-fir-filter|Warped FIR Filter]]
- [[../concepts/q-parameterization|Q-Parameterization]]
- [[../concepts/sensitivity-function|Sensitivity Function]]
- [[../concepts/waterbed-effect|Waterbed Effect]]
- [[../concepts/robust-control|Robust Control]]

## Related Sources

- [[../sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial]]
- [[../sources/pawelczyk-1997-anc-feedback-fixed-adaptive|Pawelczyk 1997: ANC Feedback Fixed/Adaptive]]
