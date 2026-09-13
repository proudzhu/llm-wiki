---
type: concept
created: 2026-07-01
updated: 2026-09-13
sources:
  - raw/papers/zhan-2026-joint-afc-rfs/full-text.md
tags:
  - hearing-aids
  - feedback-cancellation
  - deep-learning
  - complex-spectrum-mapping
---

# Deep Marginal Feedback Cancellation

**Deep Marginal Feedback Cancellation (DeepMFC)** is a deep learning approach that treats hearing aid feedback cancellation as an interference suppression task, using [[concepts/complex-spectrum-mapping|complex spectrum mapping]] to estimate feedback-free speech directly from the microphone signal.

## Core Idea

Unlike [[concepts/hearing-aid-feedback-cancellation|adaptive feedback cancellation (AFC)]] which estimates the feedback path, DeepMFC directly estimates the desired speech signal in the T-F domain. The term "marginal" refers to operating near the [[concepts/maximum-stable-gain|maximum stable gain (MSG)]] boundary where traditional AFC methods struggle.

## Original DeepMFC (Zheng et al. 2022)

- Uses complex spectrum mapping with parallel real/imaginary decoders
- Trained in open-loop with simulated marginal feedback mixtures
- Applied in closed-loop during estimation
- Achieves significant MSG improvement but computationally intensive (9.83M params, 4.83 G/s at 10 ms latency)

## L3C-DeepMFC Extension (Hao et al. 2025)

The [[sources/hao-2025-l3c-deepmfc|L3C-DeepMFC]] variant addresses the latency and complexity limitations:

| Aspect | DeepMFC | L3C-DeepMFC |
|:-------|:--------|:------------|
| Parameters | 9.83M | 0.31M |
| MACs | 4.83 G/s (10ms) | 0.43 G/s (4ms) |
| Latency | 10 ms | 4 ms |
| Architecture | Fully convolutional | Full- and sub-band recurrent |
| Representation | Parallel RI decoders | Gain-shape (cos, sin, log|·|) |
| Training | Open-loop only | Open-loop + closed-loop fine tuning |

### Key Innovations

1. **Gain-shape representation**: Decouples magnitude and phase for broader dynamic range
2. **Full- and sub-band recurrent modeling**: Shared sub-band LSTM + full-band GLSTM for efficient spectro-temporal modeling
3. **Low-latency overlap-add**: Modified OLA with tapered window, 2-frame synthesis → 4 ms latency
4. **Closed-loop fine tuning**: Addresses training-estimation mismatch with dynamic feedback mixtures

## Comparison with AFC Methods

| Aspect | AFC (PEM-based) | DeepMFC |
|:-------|:----------------|:--------|
| Approach | Estimate feedback path | Estimate desired speech directly |
| High-gain stability | Poor (biased estimation) | Good (interference suppression) |
| Decorrelation needed | Yes (PEM, FS, probe noise) | No |
| Computational cost | Low (adaptive filter) | Higher (DNN inference) |
| Integration | Standalone | Can combine with AFC |

## Position in the DeepAFS Paradigm

Zhan et al. (2026) classify DeepMFC-style direct suppression as **DeepAFS** (deep acoustic feedback suppression), contrasted with **DeepAFC** (deep enhancement of adaptive cancellation, e.g. step-size control or direct coefficient prediction). DeepAFS methods are robust at high gain but computationally heavy; DeepAFC methods converge fast but degrade when the feedback path changes. [[concepts/jointdfc|JointDFC]] unifies the two paradigms, using a compact 1-layer full-sub-band suppression network (RFSNet) as the second stage after deep PEM-AFC cancellation — matching DeepAFS robustness at 0.227 G MACs/s while inheriting AFC's fast convergence. In its evaluation, a standalone DeepAFS baseline (2-layer FSB, 0.319 G MACs/s) showed better scene generalization than DeepPEM-AFC but no advantage at high gain.

## Related Concepts

- [[concepts/hearing-aid-feedback-cancellation|Hearing Aid Feedback Cancellation]]
- [[concepts/acoustic-feedback|Acoustic Feedback]]
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[concepts/closed-loop-fine-tuning|Closed-Loop Fine Tuning]]
- [[concepts/maximum-stable-gain|Maximum Stable Gain]]

## Related Sources

- [[sources/hao-2025-l3c-deepmfc|Hao et al. 2025: L3C-DeepMFC]]
- [[sources/zhan-2025-deeppem-afc|Zhan 2025: DeepPEM-AFC]]
- [[sources/zhan-2026-joint-afc-rfs|Zhan, Moore, Li & Zheng 2026: JointDFC]] — situates DeepMFC-style suppression in the DeepAFS paradigm and integrates a compact FSB suppression stage (RFSNet) with deep PEM-AFC
