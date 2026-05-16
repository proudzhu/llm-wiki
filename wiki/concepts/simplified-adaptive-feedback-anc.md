---
type: concept
created: 2026-04-10
updated: 2026-04-10
sources:
tags:
- active-noise-control
- adaptive-feedback
- signal-processing
---

# Simplified Adaptive Feedback ANC

## Overview

The **Simplified Adaptive Feedback (SimpAFB) ANC** system, proposed by Wu, Qiu, and Guo (2014), is an adaptive feedback [[active-noise-control|Active Noise Control]] architecture that uses the **error signal directly as the reference signal**, eliminating the convolution operation required in the conventional [[internal-model-control|Internal Model Control]] (IMC) based system.

## Core Idea

```
SimpAFB:   X_sa(z) = E(z)           (error signal directly)
IMC-based: X(z)  = E(z) - Ŝ(z)·Y(z)  (requires convolution)
```

## Why This Simplification Works

1. **Practical limitation**: Real ANC systems only achieve limited attenuation (~10 dB), so the error signal always contains primary noise components
2. **Initial adaptation**: At the start, noise reduction is small, so error signal ≈ primary noise
3. **Imperfect estimation**: In practice, Ŝ(z) ≠ S(z), so the IMC system's reference signal quality is similar to the SimpAFB's

## Closed-Loop Transfer Function

```
H_sa(z) = E(z)/D(z) = 1 / [1 - S(z)·W_sa(z)]
```

This is equivalent to the non-adaptive feedback system transfer function — the SimpAFB system can be seen as its **adaptive version**.

## Stability Condition

```
|∠S(e^jω) - ∠[1 - S(e^jω)·W_sa(e^jω)] - ∠Ŝ(e^jω)| < π/2,  ∀ω
```

This condition is **worse** than the IMC system's stability because the `∠[1 - S(e^jω)·W_sa(e^jω)]` term always exists, even with perfect secondary path estimation.

## Implementation

- Uses the [[leaky-fxlms-algorithm|Leaky FxLMS Algorithm]] (not standard FxLMS) to limit filter gain and maintain stability
- Can be implemented by simply connecting the error sensor output to the reference input of a commercial adaptive feedforward ANC controller — no major hardware/software modifications needed

## Performance

| Condition | SimpAFB | IMC-based | Gap |
|-----------|---------|-----------|-----|
| Perfect Ŝ(z) | ~10 dB | ~15 dB | 5 dB |
| Small errors in Ŝ(z) | comparable | comparable | ~2 dB |
| Large errors in Ŝ(z) | comparable | comparable | ~2 dB |

## Experimental Results

- Tested in a 200 cm duct with TMS320C6747 DSP at 16 kHz
- 250–300 Hz narrow band noise: **~10 dB** reduction
- 250–350 Hz narrow band noise: **~7 dB** reduction (wider bandwidth → less predictable → worse performance)

## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[internal-model-control|Internal Model Control]]
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[leaky-fxlms-algorithm|Leaky FxLMS Algorithm]]

## Related Sources

- [[sources/wu-2014-simplified-adaptive-feedback-anc|Wu 2014: Simplified Adaptive Feedback ANC]] — Original paper
