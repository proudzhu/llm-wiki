---
type: concept
created: 2026-04-10
updated: 2026-04-10
sources:
tags:
- active-noise-control
- feedforward
- narrow-band
---

# Narrow-Band Feedforward ANC

## Overview

**Narrow-band feedforward ANC** is a variant of feedforward control where the reference signals are **synthesized internally** rather than picked up by a reference microphone. This eliminates the acoustic feedback problem entirely.

## How It Works

Instead of using a reference microphone, the reference signals are generated from a **tachometer** (RPM sensor) or frequency estimator. For each harmonic frequency ω:

```
x₁(n) = sin(ωn)
x₂(n) = cos(ωn)
```

These signals are fed to the adaptive filter as reference inputs. Since they are internally generated, they are **not influenced by the control field** — no feedback contamination.

## Sinusoidal ANC (SANC)

The algorithm for narrow-band ANC using synthesized sinusoidal references is called **SANC**. For multiple harmonics, the reference vector is expanded:

```
x(n) = [sin(ωn), cos(ωn), sin(2ωn), cos(2ωn), ..., sin(Kωn), cos(Kωn)]
```

## Key Advantage: No Feedback Problem

Since the reference signals are internally generated (not from a microphone), the anti-noise cannot corrupt them. This is a significant advantage over [[broad-band-feedforward-anc|Broad-Band Feedforward ANC]] where acoustic feedback from the loudspeaker to the reference microphone is a major concern.

## Secondary Path Simplification

When the secondary path is approximately a **pure delay** (common in narrow-band applications), the FXLMS algorithm simplifies to the **standard LMS** algorithm — no filtering of the reference signal is needed.

## Applications

- Rotating machinery (engines, fans, compressors) where a tachometer signal is available
- Periodic noise with known fundamental frequency
- Situations where reference microphone placement is impractical

## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[broad-band-feedforward-anc|Broad-Band Feedforward ANC]]
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]

## Related Sources

- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] — Section III: Narrow-Band Feedforward ANC
