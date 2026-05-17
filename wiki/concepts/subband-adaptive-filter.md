---
type: concept
created: 2026-05-17
updated: 2026-05-17
tags:
  - active-noise-control
  - adaptive-filtering
  - subband-processing
---

# Subband Adaptive Filter

## Overview

The **Subband Adaptive Filter (SAF)** decomposes the input and error signals into multiple frequency subbands using analysis filter banks, performs adaptive filtering independently in each subband, and reconstructs the full-band output. SAFs achieve fast convergence for long channel responses and colored inputs at reduced computational cost.

## Structure

In a multi-band SAF with $N$ subbands:
1. **Analysis filters** $H_i(z), i=0,\dots,N-1$ decompose $d(n)$ and $\boldsymbol{X}(n)$ into subbands
2. **Decimation** by factor $D$ reduces the sampling rate in each subband
3. **Adaptive filters** operate independently in each subband
4. **Error signals** $e_{i,D}(k) = d_{i,D}(k) - y_{i,D}(k)$ drive adaptation

## Delayless SAF

A delayless SAF avoids the aliasing and delay problems of traditional subband processing. The full-band adaptive filter coefficients are updated via frequency-domain transformations of the subband weights. This eliminates secondary path estimation overhead in some configurations.

## Applications in ANC

- Fast convergence for long acoustic paths and colored noise
- Low computational complexity compared to full-band FxLMS
- Suitable for multi-channel and MIMO ANC systems
- GPU-accelerated implementations for parallel subband processing

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/frequency-domain-anc|Frequency-domain ANC]]

## Related Sources

- [[sources/lu-2021-survey-active-noise-control-linear|Lu et al. 2021: Survey on ANC — Part I: Linear Systems]]
