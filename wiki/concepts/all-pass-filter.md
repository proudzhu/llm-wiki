---
type: concept
created: 2026-05-20
updated: 2026-05-20
tags:
  - signal-processing
  - filter-design
---

# All-Pass Filter

An **all-pass filter** is a signal processing filter whose magnitude response is unity (0 dB) at all frequencies, but whose phase response is non-trivial. In the context of frequency warping, all-pass elements replace unit delays to modify the frequency resolution of a system:

$$\tilde{z}^{-1} = \frac{z^{-1} - \lambda}{1 - \lambda z^{-1}}$$

where $\lambda \in (-1, 1)$ is the warping parameter.

## Related Concepts

- [[concepts/frequency-warping|Frequency Warping]]
- [[concepts/warped-fir-filter|Warped FIR Filter]]
