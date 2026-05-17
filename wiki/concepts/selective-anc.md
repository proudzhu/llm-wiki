---
type: concept
created: 2026-05-17
updated: 2026-05-17
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

## Advantages

- Improved robustness (pre-tuned filters are validated offline)
- Reduced computational complexity (no real-time adaptation)
- Fast response to changing noise conditions

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/generative-fixed-filter-anc|Generative Fixed-Filter ANC (GFANC)]]

## Related Sources

- [[sources/lu-2021-survey-active-noise-control-linear|Lu et al. 2021: Survey on ANC — Part I: Linear Systems]]
