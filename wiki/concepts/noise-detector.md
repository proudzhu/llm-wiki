---
type: concept
created: 2026-11-01
updated: 2026-11-01
sources:
  - raw/papers/yan-2025-lisennet/full-text.md
tags:
  - speech-enhancement
  - noise-detection
  - computational-efficiency
  - real-time
---

# Noise Detector (adaptive SE gating)

A **noise detector (ND)** is a lightweight front-end classifier that makes frame-level noisy/clean decisions so that a speech-enhancement back-end runs **only on noisy frames**, making the system's computational cost **proportional to the noise content** rather than constant. Introduced as an optional module of [[concepts/lisennet|LiSenNet]] (Yan et al., ICASSP 2025), it targets *instantaneous noise* scenarios — noise whose duration is much shorter than the speech length, where continuously-on SE wastes resources.

## Mechanism (LiSenNet instantiation)

- **Input**: 64-dimensional Mel spectrogram of the noisy signal (Mel reduction removes input redundancy).
- **Architecture**: Conv blocks with channels {4, 8, 16, 32}; Sigmoid output layer.
- **Output**: per-frame binary value (0 = clean, 1 = noisy) at the STFT frame rate.
- **Routing**: only noisy frames are sent to the SE back-end; clean frames bypass it.
- **Training**: binary cross-entropy loss, trained on the WSJ0+ESC50 dataset (4-s WSJ0 clips with 0.5–2 s of ESC50 noise, SNR −10 to 5 dB).

## Cost–Quality Trade-off

| Configuration | Params | MACs/s | RTF | PESQ (WSJ0+ESC50) |
|----------------|--------|--------|-----|--------------------|
| LiSenNet | 37k | 56M | 0.028 | 3.08 |
| LiSenNet+ND | 55k | 15M~70M | 0.020 | 3.00 |

The compute range 15–70M MACs/s spans the all-clean extreme (only the detector runs: 15M) to the all-noisy case (detector + full back-end: 70M). The savings are largest when the noise proportion is low. The cost is a slight PESQ decay (−0.08) attributed to (i) imprecision of the noise detection and (ii) information loss in clean regions that are not re-processed.

## Relation to Other Gating / Skipping Mechanisms

The noise detector is an **input-conditional, learned gate** — distinct from:

- **[[concepts/voice-activity-detection|VAD]]** — which detects *speech presence* (the complementary signal) and is typically used for statistics accumulation or pipeline control, not for gating the enhancer itself on noise content.
- **[[concepts/fixed-rate-skipping|Fixed-Rate Skipping]]** (RT-Tango, 2026) — a *schedule-based* skip of the mask estimator at 1/2 or 1/4 rate, independent of input content; FRS commits to a fixed schedule to avoid decision overhead, whereas the noise detector's schedule is signal-dependent.
- **Frame-skip prediction** (Chen et al. 2023) — compresses T-F features within the backbone with a learned refinement (PostNet); the ND instead skips whole frames at the system level.

All four exploit the same underlying resource — **temporal redundancy / sparsity of the enhancement task** — but differ in whether the gating decision is learned vs. fixed and whether it operates at frame or feature level. The ND is the only one conditioned on *noise* rather than speech presence or time.

## Related Concepts

- [[concepts/lisennet|LiSenNet]]
- [[concepts/voice-activity-detection|Voice Activity Detection]]
- [[concepts/fixed-rate-skipping|Fixed-Rate Skipping]]
- [[concepts/frame-skip-prediction|Frame-Skip Prediction]]
- [[concepts/speech-presence-probability|Speech Presence Probability]]

## Related Sources

- [[sources/yan-2025-lisennet|Yan, Zhang, Fan, Zhou & Liu 2025: LiSenNet]]
