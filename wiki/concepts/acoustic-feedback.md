---
type: concept
created: 2026-04-10
updated: 2026-04-27
sources:
  - raw/papers/miran-2026-imu-feedback-cancellation/full-text.txt
tags:
- acoustic
- active-noise-control
- feedback
---

# Acoustic Feedback

## Overview

**Acoustic feedback** in ANC systems occurs when the anti-noise signal from the canceling loudspeaker radiates **upstream** back to the reference microphone, corrupting the reference signal. This is analogous to the "howling" feedback in public address systems.

## The Problem

In a [[broad-band-feedforward-anc|Broad-Band Feedforward ANC]] system:

```
Loudspeaker (anti-noise) → radiates upstream → Reference microphone → corrupted x(n)
```

The corrupted reference signal becomes:

```
x'(n) = x(n) + f(n) * y(n)
```

where f(n) is the **feedback path** from loudspeaker to reference microphone.

This creates a **closed loop** that can become unstable if the open-loop phase lag reaches 180° while the gain exceeds unity.

## Optimal Transfer Function with Feedback

When feedback is present, the optimal controller becomes an **IIR function**:

```
W(z) = P(z) / [S(z) + F(z)·P(z)]
```

This has both poles and zeros, making it fundamentally different from the FIR solution without feedback.

## Solutions

### 1. Feedback Neutralization

Use a separate **feedback cancellation filter** to subtract the estimated feedback component:

```
x_clean(n) = x'(n) - f̂(n) * y(n)
```

- The feedback neutralization filter f̂(n) must be estimated **offline** (during ANC idle periods)
- Similar to **acoustic echo cancellation** in telephony
- Must be inhibited during ANC operation (like "double talk" detection)

### 2. Adaptive IIR Filters (Filtered-U LMS)

Model the optimal IIR solution directly using the **filtered-U recursive LMS** algorithm:
- Lower order than FIR equivalent (poles make it more efficient)
- **Disadvantage**: IIR filters are not unconditionally stable

### 3. High-Order FIR with Smaller Step Size

Approximate the IIR solution with a sufficiently high-order FIR filter:
- Requires a **smaller step size** for stability
- Slower convergence but unconditionally stable

### 4. Adaptive Feedback Cancellation (AFC) in Hearing Aids

In hearing aids, AFC uses an adaptive filter (typically PEM-NLMS) to estimate and subtract the feedback component. The step-size dilemma is central:
- **Large step size**: Fast convergence after path changes (e.g., hat on/off, phone near ear) but high steady-state error
- **Small step size**: Low steady-state error but slow convergence → whistling artifacts during transitions

**Audio-only VSS methods** (shadow filter, VSS-NLMS) are biased by input audio characteristics and cannot reliably distinguish feedback path changes from input signal changes.

**IMU-based step-size control** (Miran et al. 2026): Uses head movement acceleration from an integrated IMU to detect feedback path changes. When motion is detected → large step size; when stationary → small step size. Outperforms audio-only methods in steady-state by avoiding audio-induced biases, but cannot detect path changes from external objects that precede head movement.

## Impact on Different ANC Types

| ANC Type | Feedback Impact |
|----------|----------------|
| Broad-band feedforward | Severe — corrupts reference signal |
| Narrow-band feedforward | None — reference signals internally generated |
| Feedback ANC | N/A — no reference sensor exists |

## Related Concepts

- [[broad-band-feedforward-anc|Broad-Band Feedforward ANC]]
- [[narrow-band-feedforward-anc|Narrow-Band Feedforward ANC]]
- [[internal-model-control|Internal Model Control]]
- [[simplified-adaptive-feedback-anc|Simplified Adaptive Feedback ANC]]
- [[variable-step-size-lms|Variable Step Size LMS]]

## Related Sources

- [[../sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] — Section II-D: Feedback Effects and Solutions
- [[../sources/miran-2026-imu-feedback-cancellation|Miran 2026: IMU-Based Acoustic Feedback Cancellation]]

## Related Entities

- [[../entities/sen-m-kuo|Sen M. Kuo]] — Comprehensive treatment of feedback neutralization techniques
- [[../entities/henning-schepker|Henning Schepker]] — AFC in hearing aids, shadow filter and beamformer approaches
