---
type: concept
created: 2026-05-01
updated: 2026-05-01
sources:
  - raw/papers/yin-2023-selective-fixed-filter-anc-headphones/full-text.md
tags:
  - active-noise-control
  - signal-processing
  - frequency-domain
  - filter-selection
---

# Frequency Response Matching

**Frequency Response Matching (FRM)** is a technique used in selective fixed-filter ANC to select the most appropriate pre-trained control filter by comparing the estimated primary path frequency response against stored filter profiles.

## Overview

In the FRM-SFANC algorithm, the primary path frequency response is estimated online using an adaptive modelling approach. This estimated response is then compared with the frequency response profiles associated with each pre-trained control filter in the database. The filter whose profile best matches the estimated response is selected for noise cancellation.

## How It Works

1. **Online modelling**: An auxiliary adaptive filter estimates the primary path transfer function $\hat{P}(z)$ in real time
2. **Profile comparison**: The estimated frequency response $|\hat{P}(e^{j\omega})|$ is compared against pre-stored profiles $\{|P_i(e^{j\omega})|\}_{i=1}^{M}$ associated with each pre-trained control filter
3. **Filter selection**: The control filter $\mathbf{w}_i$ whose associated profile minimizes the matching error is selected:

$$i^* = \underset{i \in \{1, \ldots, M\}}{\arg\min} \sum_\omega \left| |\hat{P}(e^{j\omega})| - |P_i(e^{j\omega})| \right|^2$$

## Advantages over CNN-based Selection

- **No training data required**: FRM does not need labeled noise datasets for training a classifier
- **No neural network inference**: Avoids the computational overhead and latency of CNN forward passes
- **Interpretable**: The matching criterion is transparent — it directly compares frequency responses
- **Lightweight**: Suitable for resource-constrained embedded platforms

## Limitations

- **Discrete filter library**: Limited to selecting from pre-trained filters; cannot generalize to untrained noise conditions
- **Matching accuracy**: Depends on the quality of the online primary path estimate
- **Response time**: Requires sufficient observation time for accurate frequency response estimation

## Related Concepts

- [[../concepts/selective-fixed-filter-anc|Selective Fixed-Filter ANC]] — the ANC framework using FRM
- [[../concepts/active-noise-control|Active Noise Control]] — parent domain
- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — used for online modelling and pre-training

## Related Sources

- [[../sources/yin-2023-selective-fixed-filter-anc-headphones|Yin 2023: Selective Fixed-Filter ANC Based on Frequency Response Matching in Headphones]] — introduces FRM-SFANC
