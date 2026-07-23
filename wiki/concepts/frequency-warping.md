---
type: concept
created: 2026-05-13
updated: 2026-07-23
sources:
  - raw/papers/harma-2000-frequency-warped-signal-processing/full-text.md
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

## Bark Bilinear Mapping

Smith and Abel (1999) derived an analytic expression for $\lambda$ that best matches the [[concepts/bark-scale-spectral-features|Bark scale]] for a given sampling frequency $f_s$:

$$\lambda_{f_s} \approx 1.0674 \left[\frac{2}{\pi} \arctan(0.06583 f_s)\right]^{1/2} - 0.1916$$

At $f_s = 44.1$ kHz this yields $\lambda = 0.756$. The resulting mapping is called **Bark bilinear mapping** (or Bark warping). A slightly higher value ($\lambda \approx 0.78$) best matches Greenwood's cochlear frequency-position function at low frequencies. The first-order all-pass mapping is a good approximation but cannot exactly match the Bark, ERB, or Greenwood scales globally — exact matches require higher-order all-pass filter banks.

The **turning-point frequency** $f_{tp}$ (where warping leaves frequency unchanged) is:

$$f_{tp} = \pm \frac{f_s}{2\pi} \arccos(\lambda)$$

## Applications

- **Active Noise Control**: Enables low-order WFIR filters to achieve performance comparable to high-order FIR filters, especially at low frequencies
- **Audio Signal Processing**: Frequency-warped DSP for audio coding, loudspeaker equalization, physical modeling, and HRTF design — [[sources/harma-2000-frequency-warped-signal-processing|Härmä et al. 2000]]
- **Warped Linear Prediction**: WLP achieves ~6 dB (1 bit/sample) residual SNR savings over conventional LPC at wideband rates

## Related Concepts

- [[concepts/warped-fir-filter|Warped FIR Filter]]
- [[concepts/warped-iir-filter|Warped IIR Filter]]
- [[concepts/warped-linear-prediction|Warped Linear Prediction]]
- [[concepts/all-pass-filter|All-Pass Filter]]
- [[concepts/erb-scale|ERB Scale]]

## Related Sources

- [[sources/harma-2000-frequency-warped-signal-processing|Härmä et al. 2000: Frequency-Warped Signal Processing for Audio Applications]] — the canonical tutorial surveying frequency-warping methodology and audio applications
- [[sources/seo-2016-feedback-anc-constrained-optimization|Seo et al. 2016: Feedback ANC via Constrained Optimization]]
