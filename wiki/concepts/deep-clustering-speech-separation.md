---
type: concept
created: 2026-06-01
updated: 2026-06-01
tags:
  - speech-separation
  - speaker-separation
  - deep-learning
  - clustering
---

# Deep Clustering for Speech Separation

Deep clustering is a speaker-independent speech separation approach that combines DNN-based feature learning with spectral clustering (Hershey et al. 2016).

## Formulation

The DNN learns high-dimensional embeddings for each time-frequency unit such that units belonging to the same speaker have similar embeddings. Training minimizes the Frobenius norm difference between the estimated and true affinity matrices.

## Inference

1. Mixture is segmented into overlapping windows
2. DNN computes embedding vectors for each T-F unit
3. K-means clusters T-F units into speaker groups
4. Each group constructs a mask for speaker separation

## Key Properties

- **Speaker-independent**: No assumption about which speakers are present
- **Flexible**: Naturally handles mixtures with more than two speakers
- **Extension**: Deep attractor network improves results by creating attractor points for each speaker

## Related Concepts

- [[concepts/permutation-invariant-training|Permutation Invariant Training (PIT)]]
- [[concepts/ideal-binary-mask|Ideal Binary Mask (IBM)]]
- [[concepts/ideal-ratio-mask|Ideal Ratio Mask (IRM)]]

## Related Sources

- [[sources/wang-2018-supervised-speech-separation-deep-learning-overview|Wang & Chen 2018: Supervised Speech Separation Based on Deep Learning: An Overview]]
