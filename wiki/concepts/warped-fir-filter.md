---
type: concept
created: 2026-05-13
updated: 2026-05-13
tags:
  - signal-processing
  - filter-design
  - frequency-warping
---

# Warped FIR Filter

**Warped FIR (WFIR) filters** are finite impulse response filters operating in a warped frequency domain, where unit delays are replaced by first-order all-pass elements. This provides non-uniform frequency resolution — typically enhanced resolution at low frequencies.

## Key Formulations

A WFIR filter is obtained by transforming an FIR filter through the frequency warping mapping:

$$W_{trunc.}(z) = \sum_{n=0}^{W} w(n) [D(z)]^n$$

where $D(z) = \frac{z^{-1} - \lambda}{1 - \lambda z^{-1}}$ is the all-pass delay element and $\lambda$ is the warping parameter.

## Advantages over Conventional FIR

- **Lower order**: A 16th-order WFIR can match the performance of a 128th-order FIR at low frequencies
- **Tunable resolution**: The warping parameter $\lambda$ controls the trade-off between low-frequency and high-frequency resolution
- **Computational efficiency**: Suitable for low-power real-time ANC implementations

## Related Concepts

- [[../concepts/frequency-warping|Frequency Warping]]
- [[../concepts/all-pass-filter|All-Pass Filter]]

## Related Sources

- [[../sources/seo-2016-feedback-anc-constrained-optimization|Seo et al. 2016: Feedback ANC via Constrained Optimization]]
