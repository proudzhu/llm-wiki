---
type: concept
created: 2026-07-27
updated: 2026-07-27
sources:
  - raw/papers/liu-2026-array-invariant-speech-enhancement/full-text.md
tags:
  - speech-enhancement
  - multi-channel
  - microphone-arrays
  - array-invariant
  - array-agnostic
  - geometry-aware
---

# Array-Invariant Speech Enhancement

**Array-Invariant (or Array-Agnostic) Speech Enhancement** is the subfield of [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] concerned with building models that generalize across microphone arrays with **varying numbers of microphones and arbitrary geometries**, without requiring device-specific retraining. Such models enable dataset merging across devices and cross-device deployment — critical for real-world adoption, since the geometric rigidity of conventional fixed-array SE is the primary obstacle to scaling multi-channel training data.

## Problem Statement

Multi-channel SE theoretically outperforms single-channel SE by exploiting spatial information, but conventional fixed-array methods require a **fixed microphone configuration** during both training and inference. This rigidity causes two practical problems:

1. **Dataset fragmentation**: Multi-channel recordings from different devices cannot be merged into a unified training corpus.
2. **Deployment lock-in**: A model trained for one device must be retrained for any other geometry.

Array-invariant SE addresses both by accepting variable $C$ (channel count) and arbitrary microphone permutations at inference, while still leveraging spatial cues.

## Two Challenges

1. **Variable microphone count** — the model must accept $C_{\text{train}} \neq C_{\text{test}}$.
2. **Arbitrary channel permutations** — microphone ordering in real-world recordings is not standardized; the model must be insensitive to channel reordering (ideally with a mathematical guarantee, not just empirical robustness).

## Approach Categories

| Category | Mechanism | Geometry used? | Representative methods |
|---|---|:---:|---|
| **Batch / reference-channel** | Process channels via batch ops, fuse by reference or average | No | TAC [Luo 2020], TA-C, self-attention SE |
| **Fixed-dimensional transform** | Map arbitrary channels to fixed-dim representation | No | FOA (≥4 mics only), UniArray (VME-based) |
| **Geometry-aware (explicit)** | Condition the model on microphone coordinates | **Yes** | [[concepts/geometry-aware-dynamic-convolution\|Geo-DConv]] (Liu 2026), [[concepts/geometry-conditioned-ssf\|GC-SSF]] (Li 2026, target-speaker extraction) |

The first two categories are often called **array-agnostic** — they handle variable geometry by *ignoring* it. The third category, **geometry-aware** methods, explicitly inject microphone coordinates as additional input, exploiting a free cue that classical methods (e.g., MVDR) and modern DOA estimators have long leveraged.

## Why Geometry-Awareness Matters

Fixed-array methods outperform array-agnostic methods primarily because their cross-channel feature extractors learn a **spatial bias specific to the training array**. Existing array-agnostic methods, lacking any geometry input, must rely on generic time-frequency features and implicit inter-channel correlations, sacrificing this spatial prior. Geometry-aware methods like Geo-DConv restore the prior by making the kernel a function of coordinates, narrowing the gap to the fixed-array upper bound.

## Permutation Equivariance

A defining property of robust array-invariant systems. Given a permutation matrix $\mathbf{P}$ applied to both the input features $\mathbf{X}$ and the coordinates $\mathbf{G}$, the model output should be unchanged (or permuted correspondingly). Methods that achieve this only empirically (TAC, USES2) can be sensitive to channel ordering at deployment; methods with a mathematical guarantee (Geo-DConv via TACT) are provably stable.

## Datasets and Evaluation

- **RealMAN** (real-recorded 32-channel array) — preferred over simulated data due to sim-to-real domain mismatch; supports sub-array extraction for variable-array training.
- **CHiME-4** (6-mic real-world) — common cross-dataset generalization benchmark.
- **Metrics**: SDR, SI-SDR, PESQ, STOI, DNSMOS (P808, SIG, BAK, OVRL).

## Related Concepts

- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/geometry-aware-dynamic-convolution|Geometry-Aware Dynamic Convolution (Geo-DConv)]]
- [[concepts/topology-aware-coordinate-transformer|Topology-Aware Coordinate Transformer (TACT)]]
- [[concepts/virtual-microphone-estimation|Virtual Microphone Estimation]] — UniArray alternative
- [[concepts/geometry-conditioned-ssf|Geometry-Conditioned SSF]] — geometry-conditioning for target speaker extraction
- [[concepts/doa-microphone-positional-encoding|DOA-Microphone Positional Encoding]] — alternative coordinate encoding
- [[concepts/mvdr-beamformer|MVDR Beamformer]] — classical geometry-explicit baseline
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]

## Related Sources

- [[sources/liu-2026-array-invariant-speech-enhancement|Liu, Zhang, Li & Qian 2026: Array-Invariant SE via Geo-DConv]]
