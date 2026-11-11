---
type: concept
created: 2026-11-11
updated: 2026-11-11
sources:
  - raw/papers/fu-2026-one-model-many-latencies/full-text.md
tags:
  - speech-enhancement
  - universal-speech-enhancement
  - real-time
  - low-latency
---

# Universal Speech Enhancement

**Universal speech enhancement (USE)** is speech enhancement with a *single* model that handles heterogeneous input conditions — multiple languages, sampling rates, and degradation types (additive noise, reverberation, clipping, bandwidth limitation, codec artifacts, packet loss, wind noise) — while preserving intrinsic speech attributes such as speaker identity, emotion, and accent. It contrasts with task-specific enhancement, where separate systems are trained per noise type, per sample rate, or per application.

## Two Axes of Universality

USE work differs along which axis of heterogeneity it unifies:

| Axis | What is unified | Mechanism |
|---|---|---|
| **Condition universality** | Degradation types, languages, sampling rates | Broad multi-condition training data; [[concepts/urgent-challenge|URGENT Challenge]] framing |
| **Latency universality** | Real-time operating points (algorithmic + computational budget) | Multiple look-ahead settings, early exit, pruning at deploy time |

The great majority of USE systems (VoiceFixer, score-based diffusion USE, MaskSR, FINALLY, AnyEnhance, Miipher-2, Sidon) unify only the *condition* axis, and do so with non-causal architectures — their latency is not a design variable. [[sources/fu-2026-one-model-many-latencies|Fu et al. 2026]] argue this makes them inapplicable to real-time use, since conversational VoIP tolerates 50–150 ms and streaming ASR 100–200 ms, while a non-causal model's algorithmic latency is effectively unbounded.

## The Latency Budget as a Universality Dimension

Real-time USE must satisfy three constraints simultaneously, and the third is the one most often violated in reporting:

1. **Causality** — architecture is causal or has bounded look-ahead.
2. **Budget** — $l_{\text{Total}} \le l_{\text{budget}}$, application specific.
3. **Real-time processing** — $l_{\text{Compute}} \le h$ (hop size), i.e. RTF $< 1$, so latency does not accumulate.

Because computational latency depends on the deployment hardware, a *single* causal model cannot serve all latency budgets even within one application family — hence the argument for making latency a user-selectable parameter rather than a training-time choice. See [[concepts/audio-latency|Audio Latency]] for the decomposition $l_{\text{Total}} = l_{\text{Algorithmic}} + l_{\text{Computational}}$.

## Achieving Latency-Universal USE

Fu et al. 2026 combine two orthogonal knobs in one checkpoint:

- **Algorithmic latency** via [[concepts/parallel-look-ahead-convolutions|parallel look-ahead convolutions]] (0–2 look-ahead frames → 40/60/80 ms with 40 ms window, 20 ms hop);
- **Computational latency** via [[concepts/early-exit-speech-enhancement|early exit]] (depth 3–12, 2.0M–3.7M parameters).

A single model then spans 30 configurations. Two secondary ingredients make condition universality compatible with this: **sampling-frequency-independent STFT** (fixed 40 ms / 20 ms *time* durations across 8–48 kHz, so frame rate is constant across sampling rates) and a two-stage regression→adversarial training schedule that approximates the quality of a separate generative refiner at a fraction of the compute.

## Design Tension

Depth and look-ahead are not interchangeable. Fu et al. measure that for perceptual quality (UTMOS) extra depth pays better than extra look-ahead, whereas for ASR accuracy (CAcc) **one** look-ahead frame buys most of the available gain and a second frame is marginal — so the optimal latency allocation is task dependent, not universal in itself.

## Related Concepts

- [[concepts/audio-latency|Audio Latency]]
- [[concepts/parallel-look-ahead-convolutions|Parallel Look-Ahead Convolutions]]
- [[concepts/early-exit-speech-enhancement|Early-Exit Speech Enhancement]]
- [[concepts/urgent-challenge|URGENT Challenge]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/mamba|Mamba]]

## Related Sources

- [[sources/fu-2026-one-model-many-latencies|Fu et al. 2026: One Model, Many Latencies]] — introduces latency-universal USE: one checkpoint, 30 latency configurations
