---
type: concept
created: 2026-11-08
updated: 2026-11-08
sources:
  - raw/papers/huang-2026-integrated-anc-hear-through/full-text.md
tags:
  - active-noise-control
  - model-order-reduction
  - iir-filters
  - fixed-filter-anc
  - real-time-dsp
---

# Balanced Truncation Model Reduction

**Balanced truncation (BT)** is a model-order-reduction technique that approximates a high-order (typically FIR) digital filter by a much lower-order IIR filter while preserving the dominant input–output energy of the original system. In ANC, it enables real-time implementation of long offline-trained FIR control filters on compact DSP platforms.

## Core Idea

Given the FIR filter's state-space realization, BT applies a similarity transformation that makes the system **balanced** — the controllability and observability Gramians become equal and diagonal. The diagonal entries (Hankel singular values) rank the states by their contribution to the input–output energy. Truncating the states associated with the smallest singular values yields a reduced-order model that approximates the frequency response over the frequency range of interest.

## Application in ANC (Huang, Chang & Kuo 2026)

In the [[concepts/acoustic-equalization-system|AES]] of [[sources/huang-2026-integrated-anc-hear-through|Huang, Chang & Kuo 2026]], the ANC filter is obtained as:

1. **Offline training**: a 3000-tap FIR filter trained with the FxLMS algorithm on synchronized recordings of reference $x(n)$ and residual $d(n)$, using secondary-path estimate $\hat{S}(z)$;
2. **Reduction**: BT approximation as a 50th-order IIR filter;
3. **Implementation**: 25 cascaded second-order sections (SOS / biquad form),

$$\tilde{W}(z) = g \prod_{i=1}^{K} \frac{b_{0,i} + b_{1,i} z^{-1} + b_{2,i} z^{-2}}{a_{0,i} + a_{1,i} z^{-1} + a_{2,i} z^{-2}},$$

which cuts the computational cost from ~3000 to ~125 multiplications per sample (144 → 6 million multiplications per second at 48 kHz) — a 24× reduction, feasible for a real-time in-ear DSP platform (TMS320C6713, 37 μs hardware group delay).

Notably, the HT filter in the same system is *not* reduced: it starts from an analytically derived low-order FIR (Huang et al. 2022), already suitable for real-time operation — BT is applied only where the offline training produces a high-order filter.

## Relation to Other IIR-Fitting Approaches

BT is one member of a family of techniques for obtaining low-order IIR models from measured or trained responses — see the synthesis page [[synthesis/iir-filter-fitting-frequency-response|IIR Filter Fitting of Frequency Responses]] for vector fitting, least-squares frequency-domain identification, Hankel-SVD, and SOS parameterizations. BT's distinguishing property is the energy-ranked state truncation (via Hankel singular values), which is equivalent in spirit to Hankel-SVD low-order approximation; it preserves stability of the original system by construction.

## Related Concepts

- [[concepts/acoustic-equalization-system|Acoustic Equalization System (AES)]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/selective-anc|Selective ANC]]
- [[concepts/state-space-model|State-Space Model]]

## Related Sources

- [[sources/huang-2026-integrated-anc-hear-through|Huang, Chang & Kuo 2026: Integrated ANC and Hear-Through for Speech Clarity]]
