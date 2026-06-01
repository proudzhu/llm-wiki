---
type: concept
created: 2026-06-01
updated: 2026-06-01
tags:
  - speech-separation
  - speaker-separation
  - deep-learning
  - training-strategy
---

# Permutation Invariant Training (PIT)

Permutation Invariant Training (PIT) is a training strategy for speaker-independent multi-talker speech separation. It resolves the output-speaker assignment ambiguity by dynamically selecting the best permutation of DNN outputs during training.

## Problem

In standard DNN-based speaker separation, each output of the network is tied to a specific speaker. For speaker-independent separation where speakers are unseen during training, this assignment is unknown.

## Solution

PIT unties DNN outputs from speaker identity. The cost function is computed for all possible permutations of output-to-speaker assignments, and the minimum error is used for backpropagation.

## Key Properties

- **Speaker-independent**: DNN outputs are not tied to any specific speaker
- **Segment-level processing**: PIT typically operates on multi-frame segments

## Comparison

PIT offers a simpler alternative to [[concepts/deep-clustering-speech-separation|Deep Clustering]] with matching performance.

## Related Concepts

- [[concepts/deep-clustering-speech-separation|Deep Clustering for Speech Separation]]
- [[concepts/ideal-binary-mask|Ideal Binary Mask (IBM)]]
- [[concepts/ideal-ratio-mask|Ideal Ratio Mask (IRM)]]

## Related Sources

- [[sources/wang-2018-supervised-speech-separation-deep-learning-overview|Wang & Chen 2018: Supervised Speech Separation Based on Deep Learning: An Overview]]
