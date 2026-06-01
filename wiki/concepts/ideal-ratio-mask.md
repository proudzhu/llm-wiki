---
type: concept
created: 2026-06-01
updated: 2026-06-01
tags:
  - speech-separation
  - time-frequency-masking
  - training-target
---

# Ideal Ratio Mask (IRM)

The Ideal Ratio Mask (IRM) is a soft-mask training target for supervised speech separation, representing the proportion of target speech energy within each time-frequency unit.

## Definition

$$IRM(t,f) = (S^2 / (S^2 + N^2))^beta$$

where beta is a scaling parameter (commonly 0.5).

## Properties

- **Soft masking**: Provides a continuous mask, reducing musical noise artifacts
- **Relation to Wiener filter**: Without the square root (beta=1), equivalent to the classical Wiener filter
- **Cost function**: Mean squared error (MSE) is typically used

## Comparison

The IRM emerged as one of the preferred training targets. Masking-based targets outperform mapping-based targets for intelligibility (STOI).

## Related Concepts

- [[concepts/ideal-binary-mask|Ideal Binary Mask (IBM)]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask (cIRM)]]
- [[concepts/permutation-invariant-training|Permutation Invariant Training (PIT)]]

## Related Sources

- [[sources/wang-2018-supervised-speech-separation-deep-learning-overview|Wang & Chen 2018: Supervised Speech Separation Based on Deep Learning: An Overview]]
