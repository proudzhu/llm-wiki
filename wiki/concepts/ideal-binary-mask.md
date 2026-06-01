---
type: concept
created: 2026-06-01
updated: 2026-06-01
tags:
  - speech-separation
  - time-frequency-masking
  - training-target
---

# Ideal Binary Mask (IBM)

The Ideal Binary Mask (IBM) is a binary time-frequency mask that labels each T-F unit as either target-dominated (1) or interference-dominated (0). It was the first training target used in supervised speech separation and is inspired by the auditory masking phenomenon and the exclusive allocation principle in auditory scene analysis.

## Definition

$$IBM(t,f) = 1 if SNR(t,f) > LC, else 0$$

where $SNR(t,f)$ is the local signal-to-noise ratio within the T-F unit, and $LC$ is the local criterion (threshold, typically 0 dB).

## Properties

- **Binary nature**: Treats speech separation as a binary classification problem
- **Intelligibility benefit**: IBM masking dramatically improves speech intelligibility for both normal-hearing and hearing-impaired listeners
- **Cost function**: Cross-entropy is commonly used for IBM estimation

## Related Concepts

- [[concepts/ideal-ratio-mask|Ideal Ratio Mask (IRM)]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask (cIRM)]]
- [[concepts/permutation-invariant-training|Permutation Invariant Training (PIT)]]
- [[concepts/deep-clustering-speech-separation|Deep Clustering for Speech Separation]]

## Related Sources

- [[sources/wang-2018-supervised-speech-separation-deep-learning-overview|Wang & Chen 2018: Supervised Speech Separation Based on Deep Learning: An Overview]]
