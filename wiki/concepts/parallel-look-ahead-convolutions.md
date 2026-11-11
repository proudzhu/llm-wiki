---
type: concept
created: 2026-11-11
updated: 2026-11-11
sources:
  - raw/papers/fu-2026-one-model-many-latencies/full-text.md
tags:
  - speech-enhancement
  - real-time
  - low-latency
  - mixture-of-experts
  - streaming
---

# Parallel Look-Ahead Convolutions

**Parallel look-ahead convolutions** are a latency-control mechanism for streaming speech enhancement: instead of one convolutional layer whose padding is reconfigured at inference time, the model holds **one parallel convolutional branch per look-ahead setting**, trains with one branch sampled per step, and lets the *user* choose the branch at inference from the latency budget.

## Why not just change padding

Look-ahead frames are set by the left/right padding of the convolutional stack. A kernel-$k$ convolution realizes $N$ look-ahead frames with left padding $P_L$ and right padding $P_R$ such that the receptive field covers $N$ future frames; a kernel-3 example:

| Look-ahead | Left pad | Right pad |
|---|---|---|
| 0 | 2 | 0 |
| 1 | 1 | 1 |
| 2 | 0 | 2 |

Reusing one layer with three padding configurations fails to specialize, because convolution is **translation equivariant**:

$$f(T(x)) = T(f(x))$$

i.e. shifting the input shifts the output identically — the layer's learned kernel is shared across all shifts, so a single set of weights cannot encode "how much to trust the current frame vs. future frames" differently for each budget. The optimization is therefore forced into a single compromise kernel that is suboptimal for every setting.

## The fix: MoE-shaped branching without a router

The paper adopts the mixture-of-experts *structure* — parallel branches — but not its *routing*: there is no gate network and no soft combination. Selection is explicit and external (the user's latency budget), which has two practical consequences:

- **No routing loss or load-balancing term** is needed, unlike conventional MoE.
- At deployment the unselected branches are deleted, so the shipped model has the footprint of a single-look-ahead specialized model — the branching is a training-time memory/compute multiplier only.

Training samples the branch per step, so all branches see the full data distribution and stay interoperable with every exit depth of the shared trunk.

## Cost and benefit (Fu et al. 2026, URGENT 2025)

Adding the branch bank to an early-exit model costs roughly 0.03–0.05 PESQ at a matched exit depth, and buys algorithmic-latency control that plain early exit cannot provide at all — a conventional early-exit model has no valid configuration at look-ahead = 1 (reported as N/A in the paper's Table I).

| Config | Specialized (upper bound) | Early-exit only | + Parallel conv | + Multiple decoders |
|---|---|---|---|---|
| Exit 8, LA 0, PESQ | 2.19 | 2.13 | 2.13 | 2.15 |
| Exit 8, LA 0, CAcc | 83.71 | 81.84 | 82.72 | 83.10 |
| Exit 8, LA 1, PESQ | 2.27 | N/A | 2.21 | 2.24 |
| Exit 8, LA 1, CAcc | 84.93 | N/A | 84.06 | 84.62 |

## Related Concepts

- [[concepts/early-exit-speech-enhancement|Early-Exit Speech Enhancement]] — the orthogonal computational-latency knob
- [[concepts/universal-speech-enhancement|Universal Speech Enhancement]] — the setting that motivates latency control
- [[concepts/audio-latency|Audio Latency]] — algorithmic vs. computational latency
- [[concepts/causality|Causality]] — the underlying streaming-convolution constraint

## Related Sources

- [[sources/fu-2026-one-model-many-latencies|Fu et al. 2026: One Model, Many Latencies]] — origin of the mechanism
