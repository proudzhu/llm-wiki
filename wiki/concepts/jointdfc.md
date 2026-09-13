---
type: concept
created: 2026-09-13
updated: 2026-09-13
sources:
  - raw/papers/zhan-2026-joint-afc-rfs/full-text.md
tags:
  - hearing-aids
  - feedback-cancellation
  - deep-learning
  - joint-optimization
  - low-latency
aliases:
  - JointDFC
---

# JointDFC

**JointDFC** is a two-stage deep learning framework for acoustic feedback control in hearing aids that jointly optimizes **linear feedback cancellation (LFC)** and **residual feedback suppression (RFS)** — the first deep learning instantiation of the integrated cancellation-plus-suppression paradigm ([[sources/zhan-2026-joint-afc-rfs|Zhan, Moore, Li & Zheng 2026]]).

## Motivation: Unifying DeepAFS and DeepAFC

Learning-based hearing-aid feedback control splits into two paradigms with complementary failures:

| Paradigm | Mechanism | Strength | Weakness |
|:---------|:----------|:---------|:---------|
| **DeepAFS** (direct suppression) | $\hat{s}(t) = \mathrm{NN}(y(t))$ — e.g. [[concepts/deep-marginal-feedback-cancellation|DeepMFC]] / AHS | Handles nonlinear artifacts and whistling; robust at high gain | High compute; limited high-gain effectiveness |
| **DeepAFC** (enhanced AFC) | $\hat{f}(t) = \hat{f}(t-1) + \mathrm{NN}(\cdot)$ — step-size or coefficient prediction | Cheap; accurate at steady state | Degrades during convergence / re-convergence after path changes |

JointDFC cascades both: the cancellation stage removes most linear feedback; the suppression stage removes residual feedback and noise. This mirrors hybrid cancellation+suppression designs in [[concepts/acoustic-echo-cancellation|acoustic echo cancellation]] and traditional feedback control, where combining the two beats either alone — and answers the 2011 survey's prediction that joint designs would outperform decoupled hybrids ([[concepts/adaptive-feedback-cancellation|AFC]]).

## Architecture

$$e(t) = u(t) * \big(f(t) - \mathrm{NN}_c(u(t), e^*(t), y(t))\big) + s(t), \qquad \hat{s}(t) = \mathrm{NN}_s(e(t), y(t))$$

- **LFCNet** ($\mathrm{NN}_c$): the deep PEM-AFC of [[sources/zhan-2025-deeppem-afc|DeepPEM-AFC]] — PEM whitening, stacked GRU convergence-state modeling, per-T-F-bin step-size and error masks, frequency-domain PEM-AFC update
- **RFSNet** ($\mathrm{NN}_s$): a compact full-sub-band (FSB) recurrent network estimating the target by [[concepts/complex-spectral-mapping|complex spectral mapping]] from the compressed RI features of $e(t)$ and $y(t)$, with a **global causal time-frequency attention (cTFA)** module (parallel time/frequency paths) that characterizes post-cancellation spectro-temporal states so residual feedback is suppressed without over-suppressing speech

## Three-Step Training Strategy

Closed-loop training of a two-module cascade is unstable if done naively:

1. **Closed-loop pre-training of LFCNet**, with a frozen pre-trained denoising network (structurally identical to RFSNet) after the cancellation
2. **Parallel-data generation + open-loop RFSNet training**: the frozen pre-trained LFCNet generates (residual feedback + noise, clean) pairs from the closed loop
3. **Joint closed-loop fine-tuning** of both modules

This generalizes [[concepts/closed-loop-fine-tuning|closed-loop fine-tuning]] from a single suppression network to a cancellation + suppression cascade. A common 4 ms frame shift (equal to the cancellation filter length, with a regular analysis window and short synthesis window) keeps both stages synchronized; the algorithmic latency is 8 ms.

## Performance Profile

- **0.396M parameters, 0.227 G MACs/s** — between DeepPEM-AFC (0.060 G) and DeepAFS (0.319 G)
- Excels exactly where the single paradigms fail: at **high excess gain** (WB-PESQ > 4.0 even at 11 dB above the canceler-free MSG, where DeepPEM-AFC collapses to negative SI-SDR) and under **feedback-path changes** (best overall on the inter-user test set)
- Ablations: removing global cTFA costs up to 0.12 WB-PESQ; removing joint training (separate cascade) costs more, especially at low gain — evidence that joint optimization, not just architecture, drives performance

## Related Concepts

- [[concepts/hearing-aid-feedback-cancellation|Hearing Aid Feedback Cancellation]] — application domain
- [[concepts/adaptive-feedback-cancellation|Adaptive Feedback Cancellation (AFC)]] — the cancellation-stage algorithmic root
- [[concepts/deep-marginal-feedback-cancellation|Deep Marginal Feedback Cancellation]] — the DeepAFS paradigm member
- [[concepts/prediction-error-method|Prediction Error Method]] — decorrelation inside LFCNet
- [[concepts/complex-spectral-mapping|Complex Spectral Mapping]] — RFSNet estimation principle
- [[concepts/closed-loop-fine-tuning|Closed-Loop Fine Tuning]] — the training paradigm extended to cascades
- [[concepts/maximum-stable-gain|Maximum Stable Gain]] — evaluation gains are excess over the canceler-free MSG
- [[concepts/normalized-euclidean-system-distance|Normalized Euclidean System Distance]] — LFCNet loss term
- [[concepts/acoustic-howling-suppression|Acoustic Howling Suppression]] — the direct-suppression task family

## Related Sources

- [[sources/zhan-2026-joint-afc-rfs|Zhan, Moore, Li & Zheng 2026: JointDFC — Joint Deep Feedback Control for Hearing Aids]] — the proposing paper
- [[sources/zhan-2025-deeppem-afc|Zhan, Hao, Li & Zheng 2025: DeepPEM-AFC]] — LFCNet's method of origin
- [[sources/hao-2025-l3c-deepmfc|Hao et al. 2025: L3C-DeepMFC]] — the closest DeepAFS relative; RFSNet's efficiency target
