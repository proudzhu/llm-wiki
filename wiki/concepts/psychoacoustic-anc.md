---
type: concept
created: 2026-05-17
updated: 2026-05-17
tags:
  - active-noise-control
  - psychoacoustics
  - perceptual-audio
---

# Psychoacoustic ANC

## Overview

**Psychoacoustic ANC (PANC)** incorporates models of human hearing perception into [[concepts/active-noise-control|Active Noise Control]] systems. Instead of minimizing raw sound pressure level (SPL), PANC minimizes **perceived annoyance** or **loudness** — a perceptually weighted metric.

## Motivation

Human hearing has selective sensitivity across frequencies. Minimizing SPL equally at all frequencies wastes computational resources on inaudible or less annoying components while leaving perceptually salient noise uncanceled.

## Structure

PANC uses a structure similar to the FxFeLMS algorithm but with a perceptually designed error filter $H(z)$ that weights reference and error signals according to psychoacoustic principles:

- Loudness-based cost function (not SPL)
- Perceptual weighting filters derived from equal-loudness contours
- Psychoacoustic masking thresholds

## Key Methods

- **Hybrid PANC** (Wang, Gan & Chong 2012): Controls both uncorrelated disturbance and correlated primary noise
- **Subband PANC with masking**: Integrates subband processing with psychoacoustic masking for reduced computational cost and improved perceptual quality at high frequencies

## Performance Metric

PANC systems typically use **loudness** rather than SPL or ANR (Averaged Noise Reduction) as the evaluation metric.

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]

## Related Sources

- [[sources/lu-2021-survey-active-noise-control-linear|Lu et al. 2021: Survey on ANC — Part I: Linear Systems]]
