---
type: concept
created: 2026-05-20
updated: 2026-07-23
sources:
  - raw/papers/harma-2000-frequency-warped-signal-processing/full-text.md
tags:
  - signal-processing
  - filter-design
---

# All-Pass Filter

An **all-pass filter** is a signal processing filter whose magnitude response is unity (0 dB) at all frequencies, but whose phase response is non-trivial. In the context of [[concepts/frequency-warping|frequency warping]], all-pass elements replace unit delays to modify the frequency resolution of a system:

$$D(z) = \frac{z^{-1} - \lambda}{1 - \lambda z^{-1}}$$

where $\lambda \in (-1, 1)$ is the warping parameter. For $\lambda = 0$ the filter reduces to a single unit delay with linear phase and constant group delay.

## Phase and Group Delay

The phase response of $D(z)$ determines the frequency mapping:

$$\omega' = \arctan \frac{(1 - \lambda^2) \sin(\omega)}{(1 + \lambda^2)\cos(\omega) - 2\lambda}$$

For positive $\lambda$, the group delay is large at low frequencies (e.g., ~6 samples for $\lambda = 0.723$) and small at high frequencies (< 0.2 sample), causing low-frequency components to propagate slower through an all-pass chain — the basis of Bark bilinear mapping.

## Role in Warped DSP

Cascading $N$ first-order all-pass filters forms an **all-pass chain** — the core building block of frequency-warped signal processing. Replacing unit delays in FIR/IIR/FFT/LPC structures with $D(z)$ yields [[concepts/warped-fir-filter|WFIR]], [[concepts/warped-iir-filter|WIIR]], warped FFT, and [[concepts/warped-linear-prediction|warped LP]] systems, respectively.

## Related Concepts

- [[concepts/frequency-warping|Frequency Warping]]
- [[concepts/warped-fir-filter|Warped FIR Filter]]
- [[concepts/warped-iir-filter|Warped IIR Filter]]

## Related Sources

- [[sources/harma-2000-frequency-warped-signal-processing|Härmä et al. 2000: Frequency-Warped Signal Processing for Audio Applications]] — presents the all-pass chain as the unified building block for frequency-warped DSP
