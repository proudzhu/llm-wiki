---
type: concept
created: 2026-07-01
updated: 2026-07-01
tags:
  - deep-learning
  - training-strategy
  - hearing-aids
  - feedback-cancellation
---

# Closed-Loop Fine Tuning

**Closed-loop fine tuning** is a training strategy that addresses the mismatch between open-loop training and closed-loop estimation in deep learning systems, particularly for [[concepts/deep-marginal-feedback-cancellation|feedback cancellation]] in hearing aids.

## The Problem

Many deep learning methods for feedback cancellation are trained in an **open-loop** manner using simulated mixtures, but deployed in a **closed-loop** system. This creates two key discrepancies:

1. **Frame buffer updates**: In closed-loop estimation, the overlap-add stage updates frame buffers based on each frame's output, which differs from the open-loop training assumption
2. **Feedback concealment**: During closed-loop estimation, acoustic coupling is eliminated, so the received signal consists only of feedback from the current frame plus desired speech — unlike the training mixtures

## The Solution

Closed-loop fine tuning involves:

1. **Initial open-loop training**: Train the model on simulated mixtures with marginal feedback
2. **Closed-loop fine tuning**: Continue training using a simulated hearing aid system with dynamically generated feedback mixtures
3. **Larger gain during fine tuning**: Use higher gain values to push the system closer to instability, improving robustness

## Results

In [[sources/hao-2025-l3c-deepmfc|L3C-DeepMFC]], closed-loop fine tuning:
- Recovers the performance gap between open-loop DeepMFC and closed-loop estimation
- Achieves comparable WB-PESQ and HASQI-V2 to full DeepMFC at 32× fewer parameters
- Significantly improves the [[concepts/maximum-stable-gain|maximum stable gain (MSG)]]

## General Applicability

This strategy is applicable to any system where:
- Training uses simulated/open-loop data
- Deployment operates in a closed-loop or feedback configuration
- The mismatch between training and deployment conditions degrades performance

## Related Concepts

- [[concepts/deep-marginal-feedback-cancellation|Deep Marginal Feedback Cancellation]]
- [[concepts/hearing-aid-feedback-cancellation|Hearing Aid Feedback Cancellation]]
- [[concepts/maximum-stable-gain|Maximum Stable Gain]]

## Related Sources

- [[sources/hao-2025-l3c-deepmfc|Hao et al. 2025: L3C-DeepMFC]]
