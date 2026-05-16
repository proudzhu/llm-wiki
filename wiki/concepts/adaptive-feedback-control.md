---
type: concept
created: 2026-04-10
updated: 2026-04-10
sources:
tags:
- active-noise-control
- adaptive-control
- feedback
aliases:
- Adaptive Feedback Control
---

# Adaptive Feedback Control

## Overview

**Adaptive feedback control** in [[active-noise-control|Active Noise Control]] refers to systems where the controller adapts automatically using only the error signal, without a dedicated reference sensor. This contrasts with [[broad-band-feedforward-anc|Broad-Band Feedforward ANC]] which requires an upstream reference microphone.

## Classification

Feedback ANC systems fall into two categories:

### Non-Adaptive Feedback
- Fixed controller designed with high gain at frequencies of interest
- Designed via optimization (H2/H∞ methods)
- **Problem**: Vulnerable to changing conditions (non-stationary noise, uncertain secondary path)
- Requires repeated attempts and experience to get a satisfactory controller

### Adaptive Feedback
- Controller adapts automatically to changing conditions
- More robust and stable under varying conditions
- Two main approaches:
  1. **[[internal-model-control|Internal Model Control]] (IMC) based**: Regenerates reference signal using secondary path estimate
  2. **[[simplified-adaptive-feedback-anc|Simplified Adaptive Feedback ANC]] (SimpAFB)**: Uses error signal directly as reference

## Why Adaptive Feedback?

Used when:
- Primary noise cannot be directly observed
- Too many primary noise sources to economically obtain reference signals
- The noise environment is time-varying

Typical applications: headsets, headrests, headphones, double-glazed windows, ducts.

## Comparison with Feedforward

| Aspect | Feedforward | Feedback |
|--------|------------|----------|
| Reference sensor | Required (upstream) | Not needed |
| Broad-band noise control | Excellent | Limited |
| Narrow-band noise control | Excellent | Good |
| Feedback problem | Acoustic feedback to reference mic | Not applicable |
| Causality | Must satisfy delay constraint | Not applicable |

## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[internal-model-control|Internal Model Control]]
- [[simplified-adaptive-feedback-anc|Simplified Adaptive Feedback ANC]]
- [[broad-band-feedforward-anc|Broad-Band Feedforward ANC]]
- [[acoustic-feedback|Acoustic Feedback]]
- [[hearing-aid-feedback-cancellation|Hearing Aid Feedback Cancellation]]
- [[prediction-error-method|Prediction Error Method]]

## Related Sources

- [[../sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] — Section IV: Adaptive Feedback ANC
- [[../sources/wu-2014-simplified-adaptive-feedback-anc|Wu 2014: Simplified Adaptive Feedback ANC]] — Proposes simplified adaptive feedback architecture
- [[../sources/zhan-2025-deeppem-afc|Zhan 2025: DeepPEM-AFC]] — Deep learning-based PEM-AFC for hearing aids
