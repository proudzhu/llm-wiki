---
type: concept
created: 2026-07-17
updated: 2026-08-30
sources:
  - raw/papers/valin-2021-percepnet-joint-echo-control/full-text.md
  - raw/papers/valin-2018-lpcnet/full-text.md
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

## Use in LPCNet

The original [[concepts/lpcnet|LPCNet]] vocoder (Valin & Skoglund 2018) applies structured sparsity to its main GRU ($\mathrm{GRU_{A}}$) with **16×1 non-zero blocks** — one of the block shapes proposed by WaveRNN (4×4 or 16×1) — at density $d = 0.1$:

| System | Block shape | Density | Notes |
|--------|------------|--------:|-------|
| [[concepts/percepnet\|PercepNet]] AEC (2021) | 16×4 | 10–50% per gate | Unequal per-gate densities (see above) |
| [[concepts/lpcnet\|LPCNet]] vocoder (2018) | 16×1 (+ diagonal) | 10% | All diagonal terms retained |

Training starts from **dense matrices** and progressively forces the lowest-magnitude blocks to zero until the target sparsity is reached. LPCNet additionally keeps **all diagonal terms** explicitly: the diagonal is the most likely place for non-zero weights, and although diagonal elements do not align with the 16×1 blocks, they reduce to an element-wise multiply with the vector operand — cheap to vectorize — avoiding the waste of an entire block on a single diagonal element. With $N_A = 384$ units at 10% density, the sparse GRU carries the same non-zero weight count as a dense 122-unit GRU (the paper also evaluates 192 and 640 units, dense-equivalent 61 and 203).

## Related Concepts

- [[concepts/percepnet|PercepNet]]
- [[concepts/lpcnet|LPCNet]]
- [[concepts/wavernn|WaveRNN]] — introduced the 4×4 / 16×1 block shapes LPCNet draws from
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/valin-2021-percepnet-joint-echo-control|Valin et al. 2021: Joint Neural Echo Control and Speech Enhancement Based On PercepNet]]
- [[sources/valin-2018-lpcnet|Valin & Skoglund 2018: LPCNet]] — 16×1 block-sparse $\mathrm{GRU_{A}}$ with retained diagonal, dense-start progressive pruning
