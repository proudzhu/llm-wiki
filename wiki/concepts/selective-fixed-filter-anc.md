---
type: concept
created: 2026-04-30
updated: 2026-08-21
sources:
  - raw/papers/wang-2026-predictive-dsfanc-crnn/full-text.md
  - raw/papers/yin-2023-selective-fixed-filter-anc-headphones/full-text.md
  - raw/papers/wang-2026-directional-sfanc-reverberant/full-text.md
  - raw/papers/zhang-2014-causality-feedforward-anc-headset/full-text.md
  - raw/papers/bai-2026-feedback-guided-anc/full-text.md
tags:
  - active-noise-control
  - fixed-filter-anc
  - deep-learning
  - direction-of-arrival
  - filter-selection
---

# Selective Fixed-Filter ANC

**Selective Fixed-Filter ANC (SFANC)** is an ANC strategy that pre-trains a library of control filters for various noise conditions and selects the most appropriate one in real time, avoiding the convergence and stability issues of adaptive algorithms.

## Overview

Unlike adaptive ANC (e.g., FxLMS) which updates filter coefficients online, SFANC pre-computes a set of fixed control filters offline and uses a selection mechanism to switch between them. This provides:
- **Instant response**: No convergence time needed; filter switching is immediate
- **Stability**: No risk of divergence since filters are pre-validated
- **Low online complexity**: Selection is computationally cheaper than adaptive updates

## Variants

### Noise-Type SFANC
Selects filters based on the **type** of noise (e.g., broadband, tonal, impulsive). Uses CNNs for noise classification from reference signals.

### Directional SFANC (D-SFANC)
Selects filters based on the **Direction-of-Arrival (DoA)** of the noise source. Incorporates spatial information into the selection process, accounting for the fact that ANC performance depends on source direction. This direction-dependence was quantitatively established by Zhang & Qiu (2014), who showed that a typical feedforward ANC headset is causal at 0° but non-causal at 90°, with both narrowed attenuation bandwidth and reduced maximum noise reduction at lateral angles.

**Free-field D-SFANC** (Su et al. 2025; Toyooka et al. 2025): Uses traditional signal processing for DoA estimation, limited to free-field conditions.

**Reverberant D-SFANC** (Wang et al. 2026): Uses a CNN with multi-task learning to estimate azimuth and elevation from multi-reference STFT spectrograms in reverberant environments. The CNN simultaneously classifies 6 azimuth classes and 3 elevation classes, achieving ~96% and ~91% accuracy respectively with only 0.03M parameters. Pre-trained control filters are organized by spatial grid (6 azimuths × 3 elevations = 18 directions, 13 unique filters due to symmetry).

**Limitation**: D-SFANC reacts to the current DoA with a one-frame lag, causing degraded performance during source transitions for moving sources.

### Predictive Directional SFANC (PD-SFANC)
Wang et al. (2026) extend D-SFANC with a CRNN that predicts the next-frame DoA from multi-frame temporal context. The predicted DoA enables proactive filter selection, eliminating the reactive lag.

$$\hat{v} = \text{CRNN}(\mathbf{R}) \quad \triangleright \text{Next-frame DoA prediction}$$
$$\mathbf{w}' \leftarrow \mathbf{w}^{[\theta_{\hat{v}}]} \quad \triangleright \text{Control filter pre-selection}$$

### Dynamic Factor Graph SFANC (DFG-SFANC)
Su et al. (2025) use a dynamic factor graph for control filter pre-selection. Requires manual tuning of key parameters (observation node weight, observation length).

### Frequency Response Matching SFANC (FRM-SFANC)
Yin et al. (2023) propose a non-neural selection mechanism that uses **online frequency response matching** to compare the estimated primary path frequency response against pre-trained filter profiles. Unlike CNN-based methods, FRM-SFANC requires no training data or neural network inference, making it suitable for resource-constrained embedded platforms.

### Generative Fixed-Filter ANC (GFANC)
Instead of selecting from a discrete library, GFANC uses a generative model to synthesize custom control filters, enabling better generalization to untrained noise conditions.

### Feedback-Guided Controller Fusion (Bai 2026)
A contrasting framework rather than a SFANC variant: [[feedback-guided-controller-fusion|Bai et al. 2026]] observe that SFANC and GFANC determine the controller primarily from **reference-side noise features**, which characterize input noise but not the actual control outcome under the current acoustic system. Their framework instead drives a gating network with reference $\mathbf{x}(n)$, control $\mathbf{y}(n)$, and delayed residual-error $\mathbf{e}(n-1)$ signals to dynamically fuse multiple pre-trained FIR experts (one per acoustic path) with a WaveNet baseline. The feedback path closes the loop on the actual acoustic condition, improving robustness to acoustic-path mismatch without online parameter updates. On the CCF-AATC headphone ANC dataset, the 10-expert streaming model attains 19.00 dB average NR (50 Hz–5 kHz) with negligible 1–8 kHz amplification.

## Comparison of SFANC Variants

| Variant | Selection Basis | Predictive? | Auto-tuned? | Moving source | Reverberant |
|---------|----------------|-------------|-------------|---------------|-------------|
| SFANC | Noise type | No | N/A | No | — |
| FRM-SFANC | Frequency response matching | No | N/A | No | — |
| D-SFANC (free-field) | Current DoA | No | N/A | One-frame lag | No |
| D-SFANC (reverberant) | Current DoA (CNN) | No | N/A | One-frame lag | **Yes** |
| DFG-SFANC | DoA + temporal context | Partial | Manual tuning | Struggles with acceleration | — |
| **PD-SFANC** | Predicted DoA | **Yes** | **Fully learned** | **Robust** | — |
| GFANC | Generated filter | No | N/A | No | — |

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]] — parent domain
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — adaptive alternative; used to pre-train SFANC filters
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]] — spatial information for D-SFANC and PD-SFANC
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — neural architecture for filter selection and DoA prediction
- [[concepts/moving-source-tracking|Moving Source Tracking]] — core challenge addressed by PD-SFANC
- [[concepts/generative-fixed-filter-anc|Generative Fixed-Filter ANC]] — GFANC and E2E-CFG: generative approaches beyond discrete selection
- [[concepts/end-to-end-differentiable-anc|End-to-End Differentiable ANC]] — differentiable training paradigm for unsupervised GFANC and E2E-CFG
- [[concepts/frequency-response-matching|Frequency Response Matching]] — non-neural selection mechanism used in FRM-SFANC
- [[concepts/feedback-guided-controller-fusion|Feedback-guided Controller Fusion]] — contrasting framework that uses residual-error feedback (rather than reference-only selection)

## Related Sources

- [[sources/wang-2026-predictive-dsfanc-crnn|Wang 2026: Predictive Directional SFANC via CRNN]] — PD-SFANC with CRNN-based DoA prediction
- [[sources/wang-2026-directional-sfanc-reverberant|Wang 2026: Directional SFANC in Reverberant Environments]] — CNN-based DoA estimation for reverberant conditions
- [[sources/luo-2026-hybrid-gfanc-fxnlms|Luo 2026: Hybrid GFANC-FxNLMS]] — generative filter selection with adaptive refinement
- [[sources/yin-2023-selective-fixed-filter-anc-headphones|Yin 2023: Selective Fixed-Filter ANC Based on Frequency Response Matching in Headphones]] — FRM-SFANC algorithm
- [[sources/zhang-2014-causality-feedforward-anc-headset|Zhang 2014: Causality Study on Feedforward ANC Headset]] — foundational work establishing direction-dependent causality in feedforward ANC headsets
