---
type: concept
created: 2026-08-31
updated: 2026-08-31
sources:
  - raw/papers/mustafa-2023-framewise-wavegan/full-text.md
tags:
  - neural-network
  - speech-synthesis
  - convolution
  - low-complexity
---

# Framewise Convolution

**Framewise convolution** is a convolution variant introduced with [[concepts/framewise-wavegan|Framewise WaveGAN]] ([[sources/mustafa-2023-framewise-wavegan|Mustafa et al. 2023]]) in which the kernel elements are **frames** rather than samples. It lets a stack of fully-connected layers behave like a causal temporal convolution over frame-rate representations — capturing short-term (within-a-few-frames) dependencies without any sample-rate computation.

## Key Formulations

At frame index $i$, the fully-connected layer receives a concatenation of $k$ frames at indices $\{i-k+1,\dots,i\}$ from the input tensor, where $k$ is the kernel size; the rest of the operation is the same as a normal convolution (stride and dilation in frame units, padding in frames). A **conditional framewise convolution** additionally concatenates an external conditioning frame to the layer input.

In FWGAN's generator:

| Layer | Kernel | Conditioning | Padding |
|-------|--------|--------------|---------|
| Framewise conv 1 | 3 frames | — (non-conditional) | non-causal, 1 look-ahead frame |
| Framewise convs 2–5 | 2 frames | 1 conditioning frame (from the recurrent stack's latent) | causal |

Because the conditioning frame contributes the same input dimension as one history frame, the conditional and non-conditional layers share the same input dimensionality (e.g., Frame_dim 512 → $3\cdot512=1536$ input dims for the kernel-3 layer). Each layer is a **single fully-connected network** (single-channel) rather than a traditional multi-channel convolution — chosen deliberately to ease efficient implementation and [[concepts/structured-sparsity|sparsification]] of these layers, as done in [[concepts/wavernn|WaveRNN]] and [[concepts/lpcnet|LPCNet]].

## Related Concepts

- [[concepts/framewise-wavegan|Framewise WaveGAN]] — the vocoder built from framewise convolutions
- [[concepts/structured-sparsity|Structured Sparsity]] — the FC-layer sparsification the single-channel design enables
- [[concepts/gated-recurrent-unit|Gated Recurrent Unit]] — the recurrent counterpart capturing long-term dependencies

## Related Sources

- [[sources/mustafa-2023-framewise-wavegan|Mustafa et al. 2023: Framewise WaveGAN]] — introduces and defines the operation (Section 2.2)
