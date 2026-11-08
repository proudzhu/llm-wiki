---
type: concept
created: 2026-05-17
updated: 2026-11-08
tags:
  - active-noise-control
  - signal-processing
  - selective-control
---

# Selective ANC

## Overview

**Selective ANC (SANC)** avoids real-time computation of adaptive filter coefficients by selecting pre-tuned control filters from a predefined set based on temporal or spectral audio features of the incoming noise.

## Motivation

Real-time adaptive filtering is computationally expensive and can suffer from convergence issues under rapidly changing noise conditions. SANC trades memory (storing pre-tuned filters) for computation (no online adaptation).

## Operation

1. Audio features (temporal/spectral) are extracted from the incoming noise
2. A matching pre-tuned filter is selected from a library
3. The selected filter is applied as the controller
4. No real-time weight adaptation is required

## Key Methods

- **Original SANC for open window systems** (Kajikawa et al.): Selects filters based on noise characteristics
- **SANC with virtual microphone** (Saito et al.): Integrates SANC with virtual sensing for improved performance
- **Fixed band-allocated filters (Huang, Chang & Kuo 2026)**: rather than *selecting among* pre-tuned filters by audio features, the [[concepts/acoustic-equalization-system|AES]] fixes one LPF-confined ANC filter + one bandpass-shaped HT filter and obtains selectivity from the [[concepts/hear-through-frequency-band-allocation|frequency-band allocation]] itself — the lowest-complexity member of the selective family (no feature extraction, no filter bank)

## Advantages

- Improved robustness (pre-tuned filters are validated offline)
- Reduced computational complexity (no real-time adaptation)
- Fast response to changing noise conditions

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/generative-fixed-filter-anc|Generative Fixed-Filter ANC (GFANC)]]
- [[concepts/spatially-selective-anc|Spatially Selective ANC]] — selectivity by direction (ReIR constraint) rather than by filter selection; the two are complementary axes of "selective" ANC
- [[concepts/acoustic-equalization-system|Acoustic Equalization System (AES)]] — selectivity by frequency-band allocation
- [[concepts/hear-through-frequency-band-allocation|Hear-Through Frequency-Band Allocation]]

## Related Sources

- [[sources/lu-2021-survey-active-noise-control-linear|Lu et al. 2021: Survey on ANC — Part I: Linear Systems]]
- [[sources/xiao-2023-spatially-selective-anc|Xiao 2023: Spatially Selective Active Noise Control Systems]] — contrasts spatial selection with selective fixed-filter and coherence-based methods
- [[sources/huang-2026-integrated-anc-hear-through|Huang, Chang & Kuo 2026: Integrated ANC and Hear-Through for Speech Clarity]] — fixed band-allocated ANC+HT filters as the lowest-complexity selective scheme
