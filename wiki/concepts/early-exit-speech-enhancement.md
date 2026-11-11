---
type: concept
created: 2026-11-11
updated: 2026-11-11
sources:
  - raw/papers/fu-2026-one-model-many-latencies/full-text.md
tags:
  - speech-enhancement
  - real-time
  - early-exit
  - model-compression
---

# Early-Exit Speech Enhancement

**Early exit** is a training and inference paradigm in which a network emits predictions from **intermediate layers**, not only from its last layer, so that inference depth (and therefore computational latency) becomes a runtime choice. Introduced for generic deep networks as BranchyNet (Teerapittayanon et al. 2016) and applied to speech enhancement across a line of work from 2021 onward.

## Role in real-time SE

Early exit addresses only the *computational* half of the latency budget — it lets a fixed-architecture model run shallower on slower hardware or in tighter budgets. It does not change [[concepts/audio-latency|algorithmic latency]], which is set by the receptive field/look-ahead of the front end. Fu et al. 2026 pair it with [[concepts/parallel-look-ahead-convolutions|parallel look-ahead convolutions]] to control both halves in one model.

## Exit-criterion vs. exit-depth-as-budget

Most prior SE work (Li et al. 2021 progressive SE; Chen et al. 2021 multi-channel CASS with early-exit transformers; Bloom-Net 2022; Dynamic-NsNet2 2023; probabilistic early exits for speech separation 2025) designs an **exit criterion** — when can this frame stop? Fu et al. instead treat the exit layer as a **deployment constant**, selected offline from the hardware's compute budget, which removes the need for a confidence estimator and makes latency deterministic (no data-dependent jitter — a requirement for RTF $<1$ guarantees).

## The shared-decoder problem and two-stage training

A model trained with a single shared decoder across all exits underperforms a model trained for one fixed depth, because every intermediate layer must also serve all deeper layers. Fu et al. report an initially counter-intuitive experimental finding: **independent per-exit decoders trained from scratch are worse than a shared decoder**, since the shared decoder enforces a consistent representation space across depths. Their two-stage schedule gets both properties:

1. **Shared decoder stage** — one decoder for all exits, exit layer sampled uniformly per training step (here 3–12).
2. **Multiple decoder stage** — after convergence, instantiate one decoder per exit layer, initialized from the shared decoder, and fine-tune the pre-decoder trunk (encoder + sequence model) at a reduced learning rate (here $2\times10^{-5}$ vs. $2\times10^{-4}$).

This keeps shallow exits in a representation space compatible with deep ones while letting each optimize its own output. On the URGENT 2025 test set the second stage raised CAcc from 81.13 → 81.86 (exit 4), 81.84 → 83.10 (exit 8), and 82.62 → 83.25 (exit 12), at the cost of a consistent small NISQA regression.

## Open problem

The residual gap between shallow and deep exits is not closed (0.03–0.07 PESQ at exit 4 in Fu et al.); knowledge distillation from deep to shallow exits — inspired by LLM compression — is the named remedy and remains untested in SE.

## Related Concepts

- [[concepts/parallel-look-ahead-convolutions|Parallel Look-Ahead Convolutions]] — the orthogonal algorithmic-latency knob
- [[concepts/universal-speech-enhancement|Universal Speech Enhancement]]
- [[concepts/audio-latency|Audio Latency]]
- [[concepts/stateful-streaming-inference|Stateful Streaming Inference]] — the other streaming-compute-cost axis (state memory)

## Related Sources

- [[sources/fu-2026-one-model-many-latencies|Fu et al. 2026: One Model, Many Latencies]] — two-stage shared→multiple decoder training; 2.0M–3.7M parameter exit range
