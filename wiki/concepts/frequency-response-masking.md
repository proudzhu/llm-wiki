---
type: concept
created: 2026-07-23
updated: 2026-07-23
tags:
  - digital-filter-design
  - sharp-transition-bands
  - linear-phase
  - filter-banks
---

# Frequency Response Masking (FRM)

**Frequency Response Masking (FRM)** is a digital filter design technique introduced by Lim (1986) for the synthesis of **linear-phase FIR filters with very sharp transition bands and low complexity**. It is the design technique underlying the [[concepts/fast-filter-bank|Fast Filter Bank (FFB)]] and hence the high selectivity of the [[concepts/constant-q-fast-filter-bank|CQFFB]] and [[concepts/bounded-q-fast-filter-bank|BQFFB]].

## Principle

The technique exploits the observation that the frequency response of an **interpolated filter** of the form $H(z^L)$ is composed of periodic replicas of the frequency response of $H(z)$, each compressed by a factor $L$ along the frequency axis. Each replica therefore exhibits passband-stopband transitions $L$ times sharper than those of $H(z)$.

The design proceeds in two steps:

1. **Interpolated prototype $H(z^L)$**: provides the sharp transitions but creates multiple unwanted periodic images.
2. **Masking filter $G(z)$**: a moderately selective filter that suppresses the undesired images and keeps only the desired passband.

The complexity advantage comes from two facts:

- The interpolated filter $H(z^L)$ has $L$ times fewer nonzero coefficients than its order (most taps are zero).
- The masking filter $G(z)$ does not need stringent specifications — it only has to suppress already-attenuated images.

The overall design is carried out through properly chosen optimization procedures.

## Role in the FFB

The FFT filter bank's tree structure (each channel is the cascade of $L$ instances of a 2-tap kernel $H(z) = 1 + z^{-1}$) is **structurally suited for FRM design** because it is already built from cascaded interpolated filters. The [[concepts/fast-filter-bank|FFB]] modifies the FFT tree by replacing the unique low-order kernel with **distinct higher-order kernels at each level $l$**, designed via FRM so that each interpolated filter is masked by the subsequent cascaded filters.

This produces a filter bank with:

- ~56 dB worst-case sidelobe attenuation (vs. ~13 dB for the FFT),
- linear phase (inherited from the FFT tree),
- only ~2× the FFT computational cost.

## Related Concepts

- [[concepts/fast-filter-bank|Fast Filter Bank (FFB)]]
- [[concepts/constant-q-fast-filter-bank|Constant-Q Fast Filter Bank (CQFFB)]]
- [[concepts/bounded-q-fast-filter-bank|Bounded-Q Fast Filter Bank (BQFFB)]]

## Related Sources

- [[sources/diniz-2006-high-selectivity-filter-banks-spectral-analysis-music|Diniz, Kothe, Netto & Biscainho 2006: High-Selectivity Filter Banks for Spectral Analysis of Music Signals]]
