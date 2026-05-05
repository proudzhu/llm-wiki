---
type: concept
created: 2026-04-10
updated: 2026-04-10
sources:
tags:
- active-noise-control
- broad-band
- feedforward
---

# Broad-Band Feedforward ANC

## Overview

**Broad-band feedforward ANC** is the most common ANC architecture. It uses a **reference sensor** placed upstream of the noise source to capture the primary noise before it reaches the cancellation zone, giving the controller time to compute the appropriate anti-noise signal.

## Architecture

```
Primary noise → [Reference mic] → x(n) → [ANC Controller W(z)] → y(n) → [Loudspeaker]
                                                    ↓
Primary path P(z)                                Error mic → e(n)
```

The reference signal x(n) is processed by the adaptive controller to drive a loudspeaker that emits anti-noise.

## Causality Requirement

The **electrical delay** (processing time) must not exceed the **acoustic delay** from the reference microphone to the canceling loudspeaker. If this condition is violated:

- The controller response is **noncausal**
- The system can only effectively control **narrow-band or periodic noise** (not broad-band random noise)

## Optimal Transfer Function

The adaptive filter must simultaneously model the primary path and inverse-model the secondary path:

```
W(z) = P(z) / S(z)
```

where:
- **P(z)** = primary path (acoustic response from reference sensor to error sensor)
- **S(z)** = secondary path (D/A → reconstruction filter → amplifier → loudspeaker → acoustic path → error mic → preamp → anti-alias filter → A/D)

## Filtered-X LMS

The [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] is the standard adaptive algorithm because the standard LMS becomes unstable when S(z) is present in the loop.

## Performance

The maximum noise reduction depends on the **coherence** between reference and primary noise signals:

```
NR_max(f) = -10·log₁₀[1 - γ²_xd(f)]
```

High coherence at frequencies with significant disturbance energy is essential.

## Feedback Problem

The anti-noise radiates **upstream** to the reference microphone, corrupting the reference signal. Solutions include [[acoustic-feedback|Acoustic Feedback]] neutralization, adaptive IIR filters, or using a sufficiently high-order FIR filter.

## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[narrow-band-feedforward-anc|Narrow-Band Feedforward ANC]]
- [[acoustic-feedback|Acoustic Feedback]]
- [[multi-channel-anc|Multi-Channel ANC]]

## Related Sources

- [[../sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] — Section II: Broad-Band Feedforward ANC, FXLMS derivation

## Related Entities

- [[../entities/sen-m-kuo|Sen M. Kuo]] — Author of the definitive FXLMS derivation
- [[../entities/dennis-r-morgan|Dennis R. Morgan]] — Derived the FXLMS algorithm independently
