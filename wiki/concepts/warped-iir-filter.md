---
type: concept
created: 2026-07-23
updated: 2026-07-23
sources:
  - raw/papers/harma-2000-frequency-warped-signal-processing/full-text.md
tags:
  - signal-processing
  - filter-design
  - frequency-warping
  - iir-filters
---

# Warped IIR Filter

**Warped IIR (WIIR) filters** are infinite impulse response filters operating in a warped frequency domain, where unit delays in a conventional IIR structure are replaced by first-order all-pass elements $D(z)$. Like [[concepts/warped-fir-filter|WFIR filters]], WIIRs provide nonuniform frequency resolution (typically enhanced at low frequencies for auditory applications), but with the recursive structure of IIR filters.

## Key Formulations

The general transfer function of a WIIR filter is:

$$H_{\mathrm{WIR}}(z) = \frac{\sum_{i=0}^{M} \beta_i [D(z)]^i}{1 + \sum_{i=1}^{R} \alpha_i [D(z)]^i}$$

where $D(z) = \frac{z^{-1} - \lambda}{1 - \lambda z^{-1}}$ is the [[concepts/all-pass-filter|all-pass]] warping element and $\lambda$ is the warping parameter.

### The Delay-Free Loop Problem

A direct implementation of the WIIR contains **delay-free recursive loops** — the denominator's $D(z)$ elements feed back without an intervening delay, making the filter unrealizable as-is. [[sources/harma-2000-frequency-warped-signal-processing|Härmä et al. 2000]] present two solutions:

1. **Two-step technique**: The output is first computed using a modified difference equation, then the inner states are updated using the computed output value. This is computationally more expensive but necessary when coefficients are updated each sample.

2. **Modified structure** (Fig. 13b): A coefficient transformation from $\alpha_i$ to $\sigma_i$ eliminates the delay-free loops, yielding a directly realizable filter. This is more efficient than the two-step approach when coefficients are held constant over several hundred sample periods.

The same delay-free loop issue and solution apply to the **WIIR lattice filter** (Fig. 14), where coefficients $c_i$ are computed from reflection coefficients $k_i$ via a recursive algorithm.

### Pole-Zero Mapping

An ordinary IIR filter's poles $p_k$ and zeros $m_k$ can be mapped explicitly to the warped $\tilde{z}$ domain:

$$\tilde{p}_k = \frac{p_k + \lambda}{1 + p_k \lambda}, \qquad \tilde{m}_k = \frac{m_k + \lambda}{1 + m_k \lambda}$$

This is useful when designing a WIIR from an existing IIR specification.

## Advantages and Tradeoffs

- **Order reduction**: Warping can reduce filter order by a factor of ~5 or more compared to conventional IIR/FIR designs for auditory-frequency applications.
- **Computational cost**: WIIRs are typically 2–2.5× slower per order than conventional IIRs on DSP processors, but the order reduction more than compensates.
- **Quantization robustness**: Warped filters are less sensitive to coefficient quantization because poles that cluster near the unit circle at low frequencies are spread more uniformly in the warped domain.
- **Dewarping limit**: Mapping a warped filter back to a traditional IIR form works for orders below ~20, but fails above ~30 even in double precision due to pole clustering.

## Applications

- **Loudspeaker equalization**: Order-24 WIIR (warped Prony design) achieves equalization comparable to order-105 FIR, with better low-frequency matching.
- **Guitar body physical modeling**: WIIR with denominator order 100–200 matches FIR quality at order 2000–5000.
- **Binaural (HRTF) filter design**: WIIR with $\lambda = 0.65$ achieves lower filter order with acceptable perceptual tradeoff (enhanced low-frequency fit, reduced high-frequency matching).

## Related Concepts

- [[concepts/frequency-warping|Frequency Warping]] — the underlying methodology
- [[concepts/all-pass-filter|All-Pass Filter]] — the warping building block
- [[concepts/warped-fir-filter|Warped FIR Filter]] — the FIR counterpart

## Related Sources

- [[sources/harma-2000-frequency-warped-signal-processing|Härmä et al. 2000: Frequency-Warped Signal Processing for Audio Applications]] — introduces the modified WIIR structures and surveys applications
- [[sources/seo-2016-feedback-anc-constrained-optimization|Seo et al. 2016: Feedback ANC via Constrained Optimization]] — applies warped filter concepts to headphone ANC
