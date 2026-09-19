---
type: concept
created: 2026-09-19
updated: 2026-09-19
sources:
  - raw/papers/pan-2025-data-driven-acoustics/full-text.md
tags:
  - sound-event-detection
  - audio-processing
  - deep-learning
  - signal-detection
---

# Sound Event Detection (SED)

Sound event detection is a signal **detection** problem that identifies whether specific classes of acoustic events occur in an audio signal, along with the precise timing of their occurrences. Real-world SED systems must detect dozens to hundreds of event classes (e.g., in domestic or urban monitoring) at frame-level temporal resolution.

## Problem Formulation (Pan 2025)

The network input is typically a **Mel spectrogram** (e.g., 40 ms frame length, 20 ms frame shift, 64 Mel bands per frame). For a sample with $T$ slices and $L$ event classes, the network produces:

- a frame-level probability matrix $\hat{\bm{Y}} = [\hat{\bm{y}}_{0}, \ldots, \hat{\bm{y}}_{T-1}] \in [0,1]^{L \times T}$, where $\hat{y}_{t}(\ell)$ is the probability that event $\ell$ occurs at time $t$, and
- a clip-level vector $\hat{\bm{y}} \in [0,1]^{L}$ obtained by an **aggregation layer** $\mathcal{A}(\cdot)$, $\hat{\bm{y}} = \mathcal{A}(\hat{\bm{Y}})$.

Because the output layer is a **multiple-sigmoid** head (each event class an independent binary probability), the loss is binary cross-entropy applied per class; the multi-label nature (several events co-occurring) rules out softmax.

## Aggregation and Weak Labels

When only clip-level labels are available (whether an event occurs anywhere in the clip), the aggregation layer implements a **multiple-instance learning** pooling — e.g., max pooling (any frame active ⇒ clip active) or mean pooling; the choice of pooling function measurably affects detection performance.

## Class Imbalance

With many event types and sparse occurrence, most training slices are negative, so plain BCE converges slowly or not at all. Remedies include **Dice loss** (from image segmentation), which normalizes the loss by the per-batch positive/negative volumes, and related reweighting schemes.

## Typical Network Structures

- **Fully convolutional network**: 4 conv blocks (channels 32/64/128/128, $3\times3$ time-frequency kernels, BN + ReLU) + $1\times1$ conv to $L$ channels + sigmoid; frequency dimension averaged, then aggregated.
- **CRNN**: convolutional feature extraction followed by a gated recurrent layer and a multiple-sigmoid output head — the standard shape for frame-level SED (e.g., the CRNN baseline of the DCASE challenges).

## Related Concepts

- [[concepts/sel-d|SELD]] — joint sound event localization and detection
- [[concepts/acoustic-scene-classification|Acoustic Scene Classification]]
- [[concepts/keyword-spotting|Keyword Spotting]]
- [[concepts/voice-activity-detection|Voice Activity Detection]] — the single-class special case
- [[concepts/spectrogram-analysis|Spectrogram Analysis]]
- [[concepts/activity-coupled-cartesian-doa|ACCDOA]] — couples SED activity with DOA regression

## Related Sources

- [[sources/pan-2025-data-driven-acoustics|Pan 2025: Fundamentals of Data-Driven Approaches to Acoustic Signal Detection, Filtering, and Transformation]] — Sections 3.1 and 5 formulate SED as detection with aggregation and class-imbalance handling
