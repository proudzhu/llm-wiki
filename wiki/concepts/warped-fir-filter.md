---
type: concept
created: 2026-05-13
updated: 2026-07-23
sources:
  - raw/papers/harma-2000-frequency-warped-signal-processing/full-text.md
  - raw/papers/klatt-2025-laguerre-feedback-anc/full-text.md
tags:
  - signal-processing
  - filter-design
  - frequency-warping
---

# Warped FIR Filter

**Warped FIR (WFIR) filters** are finite impulse response filters operating in a warped frequency domain, where unit delays are replaced by first-order all-pass elements $D(z)$. This provides non-uniform frequency resolution — typically enhanced resolution at low frequencies for auditory applications.

## Key Formulations

A WFIR filter is obtained by transforming an FIR filter through the [[concepts/frequency-warping|frequency warping]] mapping:

$$H_{\mathrm{WFIR}}(z) = \sum_{n=0}^{M} h^{-}(n) \tilde{z}^{-n} = \sum_{n=0}^{M} \beta_n \{D(z)\}^n$$

where $D(z) = \frac{z^{-1} - \lambda}{1 - \lambda z^{-1}}$ is the [[concepts/all-pass-filter|all-pass]] delay element and $\lambda$ is the warping parameter.

Although structurally FIR-like, the WFIR has an **infinite impulse response** due to the recursive nature of $D(z)$. Coefficients can be derived from a nonwarped FIR via:

- **Synthesis** (Eq. 20a): $H(z) = \sum_{k=0}^{\infty} \tilde{h}(k) \tilde{z}^{-k}$, implemented using $+\lambda$
- **Analysis** (Eq. 20b, dewarping): $\tilde{H}(\tilde{z}) = \sum_{n=0}^{\infty} h(n) \left(\frac{\tilde{z}^{-1} + \lambda}{1 + \lambda z^{-1}}\right)^n$, implemented using $-\lambda$

The reflection coefficients of a WFIR lattice filter may be obtained from WFIR coefficients using the same recursive computation as in nonwarped filters.

## Advantages over Conventional FIR

- **Lower order**: A 16th-order WFIR can match the performance of a 128th-order FIR at low frequencies (ANC applications); a 500th-order WFIR ($\lambda=0.63$) matches FIR quality at order 2000–5000 (guitar body modeling)
- **Tunable resolution**: The warping parameter $\lambda$ controls the trade-off between low-frequency and high-frequency resolution
- **Computational efficiency**: Although WFIRs are 3–4× slower per order than FIRs on DSP processors, warping can reduce filter order by ~5× or more, yielding a net efficiency gain
- **Quantization robustness**: Warped filters are less sensitive to coefficient quantization (poles spread more uniformly)

## Relation to Laguerre Filters

The [[concepts/laguerre-filter|Laguerre filter]] is the orthonormal-basis counterpart of the WFIR: each Laguerre basis function $\Lambda_m(z, \alpha) = \sqrt{1-\alpha^2}\,\frac{(z^{-1}-\alpha)^m}{(1-\alpha z^{-1})^{m+1}}$ is the impulse response of the m-fold cascade of the same all-pass delay with a first-order low-pass pre-filter, so a Laguerre network is a low-pass-filtered warped transversal structure. In feedback ANC the two achieve the same goal by different means: Seo 2016's 16th-order WFIR ≈ 128th-order FIR in the warped domain, while [[sources/klatt-2025-laguerre-feedback-anc|Klatt & Martin 2025]]'s 17th-order Laguerre network ≈ 255th-order FIR with the added benefit that the Laguerre frequency response stays affine in the coefficients, preserving convexity of the IMC optimization.

## Related Concepts

- [[concepts/frequency-warping|Frequency Warping]]
- [[concepts/all-pass-filter|All-Pass Filter]]
- [[concepts/warped-iir-filter|Warped IIR Filter]] — the IIR counterpart
- [[concepts/warped-linear-prediction|Warped Linear Prediction]] — uses WFIR as the prediction error filter

## Related Sources

- [[sources/harma-2000-frequency-warped-signal-processing|Härmä et al. 2000: Frequency-Warped Signal Processing for Audio Applications]] — the canonical tutorial presenting WFIR design, dewarping, and applications
- [[sources/seo-2016-feedback-anc-constrained-optimization|Seo et al. 2016: Feedback ANC via Constrained Optimization]] — applies WFIR + Q-parameterization to headphone ANC
- [[sources/klatt-2025-laguerre-feedback-anc|Klatt & Martin 2025: Laguerre Filter-based Robust Feedback Active Noise Control]] — the Laguerre (orthonormal warped-basis) route to the same low-order ANC controller goal
