---
type: concept
created: 2026-07-17
updated: 2026-07-17
sources:
  - raw/papers/valin-2021-percepnet-joint-echo-control/full-text.md
tags:
  - deep-learning
  - model-compression
  - low-complexity
  - neural-network
---

# Structured Sparsity

Structured sparsity is a neural network compression technique in which entire sub-blocks of weight matrices are forced to zero (rather than individual weights), preserving the regular memory layout needed for efficient SIMD (single instruction, multiple data) vectorization on modern CPUs. Unlike unstructured pruning, structured sparsity maintains computational efficiency at inference time.

## Use in PercepNet

The [[concepts/percepnet|PercepNet]] AEC system (Valin et al. 2021) applies structured sparsity with **16×4 sub-blocks** to reduce the DNN complexity while maintaining real-time performance:

| Layer | Density | Rationale |
|-------|--------:|-----------|
| Fully-connected layers | 100% (dense) | Kept dense for quality |
| First conv layer | 100% (dense) | Kept dense for quality |
| Second conv layer | 50% | Partial sparsity tolerated |
| GRU new-state matrices | 40% | Most useful gate, kept denser |
| GRU update gate matrices | 20% | Less useful, more sparsity |
| GRU reset gate matrices | 10% | Least useful, most sparsity |

The unequal density reflects the observation that the different gates of a GRU have unequal usefulness — the new-state computation is most important, while the reset gate can be aggressively pruned.

## Sparse Model Variants

- **Full model**: 8M weights, 8-bit quantized
- **Sparse (25%)**: 2.1M non-zero weights — quality comparable to full model
- **Ultra-sparse (10%)**: 800k non-zero weights — graceful quality degradation, ~1.5% CPU

Training uses the sparsification schedule of Zhu & Gupta (2017).

## Related Concepts

- [[concepts/percepnet|PercepNet]]
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/valin-2021-percepnet-joint-echo-control|Valin et al. 2021: Joint Neural Echo Control and Speech Enhancement Based On PercepNet]]
