---
type: concept
created: 2026-08-30
updated: 2026-08-30
sources:
  - raw/papers/valin-2024-fargan/full-text.md
tags:
  - deep-learning
  - autoregressive
  - neural-vocoder
  - training
---

# Teacher Forcing and Exposure Bias

**Teacher forcing** is the training scheme for autoregressive sequence models in which the model's inputs at each step are the *ground-truth* previous outputs rather than its own predictions — allowing parallel, stable training but creating a **domain gap** between training and inference. At inference the model must consume its own (imperfect) outputs; errors the model never saw during training can compound step by step. This train/test mismatch is **exposure bias** (Schmidt 2019): a generalization failure specific to generation, not classification.

## Why Autoregressive Vocoders Are Stuck With It

Autoregressive vocoders based on **explicit density estimation** — WaveNet, SampleRNN, [[concepts/wavernn|WaveRNN]], [[concepts/lpcnet|LPCNet]] — synthesize waveforms through *conditional sampling*: each sample (or $\mu$-law excitation level) is drawn from a distribution conditioned on all previous ones. Training such a model means maximizing the likelihood of each ground-truth sample given the preceding ground-truth samples — teacher forcing is structural, not a convenience. Two consequences ([[sources/valin-2024-fargan|Valin et al. 2024]]):

1. **Exposure bias** — the training/inference domain gap "sometimes limits quality."
2. **No direct signal generation** — a density model cannot be trained with losses defined on the generated waveform itself, ruling out adversarial (GAN) training and other advanced losses used by MelGAN, HiFi-GAN and BigVGAN.

The usual mitigations carry costs: noise injection at the input (as LPCNet does, CELP-style) narrows the gap without closing it, and scheduled sampling is an imperfect middle ground.

## Escaping It: Generate Blocks, Unroll

If the generator produces a *block* of samples per forward pass, the autoregressive inputs are whole past blocks, and the model can be trained on sequences it generated itself by **unrolling** — the training-time feedback comes from the synthesized signal, exactly as at inference. [[concepts/fargan|FARGAN]] takes this route at a 2.5-ms (40-sample) granularity, which is what lets an *autoregressive* vocoder be trained adversarially. CARGAN trains adversarially the same way but with 512-sample chunks, still using teacher forcing for its autoregressive component.

A telling data point from the FARGAN paper: several attempts (by its authors and others) to add direct [[concepts/pitch-prediction|pitch prediction]] to [[concepts/lpcnet|LPCNet]] failed — and teacher forcing is the likely culprit, because pitch prediction is maximally sensitive to the discrepancy between the ground-truth history the model trains on and the synthesized history it runs on.

## Related Concepts

- [[concepts/fargan|FARGAN]] — framewise unrolled training that eliminates teacher forcing
- [[concepts/lpcnet|LPCNet]] — density-estimation vocoder that mitigates (not removes) the gap via noise injection
- [[concepts/wavernn|WaveRNN]] — the AR density-estimation family subject to the limitation
- [[concepts/pitch-prediction|Pitch Prediction]] — a mechanism that fails under teacher forcing
- [[concepts/one-step-generative-models|One-Step Generative Models]] — the parallel (non-AR) escape route, with its own trade-offs

## Related Sources

- [[sources/valin-2024-fargan|Valin, Mustafa & Büthe 2024: FARGAN]] — formulates the two structural limitations of density-estimation vocoders and the unrolled framewise escape
