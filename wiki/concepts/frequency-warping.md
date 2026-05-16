---
type: concept
created: 2026-05-13
updated: 2026-05-13
tags:
  - signal-processing
  - frequency-warping
  - audio
---

# Frequency Warping

**Frequency warping** is a signal processing technique that modifies the frequency resolution of a system by replacing unit delay elements $z^{-1}$ with first-order all-pass elements:

$$\tilde{z}^{-1} = \frac{z^{-1} - \lambda}{1 - \lambda z^{-1}}$$

where $\lambda \in (-1, 1)$ is the **warping parameter**. Larger $\lambda$ values increase low-frequency resolution at the expense of high-frequency resolution.

## Key Formulations

The transformation maps an FIR filter in the linear frequency domain to a **warped FIR (WFIR)** filter in the warped frequency domain:

$$\sum_{n=0}^{\infty} l(n) \left(\frac{\tilde{z}^{-1} + \lambda}{1 + \lambda \tilde{z}^{-1}}\right)^{-n} = \sum_{k=0}^{\infty} w(k) \tilde{z}^{-k}$$

where $l(n)$ is the original FIR filter and $w(k)$ is the WFIR filter. The WFIR must be truncated to finite length:

$$W_{trunc.}(z) = \sum_{n=0}^{W} w(n) [D(z)]^n$$

where $D(z)$ is the all-pass element and $W$ is the final filter order.

## Applications

- **Active Noise Control**: Enables low-order WFIR filters to achieve performance comparable to high-order FIR filters, especially at low frequencies
- **Audio Signal Processing**: Frequency-warped signal processing for audio applications (Härmä et al. 2000)

## Related Concepts

- [[concepts/warped-fir-filter|Warped FIR Filter]]
- [[concepts/all-pass-filter|All-Pass Filter]]

## Related Sources

- [[sources/seo-2016-feedback-anc-constrained-optimization|Seo et al. 2016: Feedback ANC via Constrained Optimization]]
