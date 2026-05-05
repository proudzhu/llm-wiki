---
type: concept
created: 2026-04-12
updated: 2026-04-17
sources:
  to Headphones.md
tags:
- active-noise-control
- hybrid-systems
---

# Hybrid ANC

**Hybrid Active Noise Control (ANC)** is an architecture that combines both [[feedforward-anc|Feedforward ANC]] and [[feedback-anc|Feedback ANC]] structures to achieve superior performance across a wider frequency range and handle different types of noise simultaneously.

## Overview

In a hybrid system, the feedforward component typically targets broad-band noise captured by an external reference microphone, while the feedback component (using the internal error microphone) addresses predictable or narrow-band noise that the feedforward system might miss or amplify (due to [[acoustic-feedback|Acoustic Feedback]] or causality issues).

## Benefits

1. **Broadened Performance**: Combines the wide-spectrum capability of feedforward with the periodic/predictable noise handling of feedback.
2. **Robustness**: If one sensor fails or provides poor coherence (e.g., due to wind noise on the external mic), the other system can still provide some level of cancellation.
3. **Waterbed Mitigation**: The feedforward system can be used to compensate for the "Waterbed effect" (amplification at certain frequencies) typically introduced by feedback systems (Benois 2020).

## Implementation Architectures

### 1. Simple Additive Hybrid
The control signals from the feedforward and feedback controllers are simply summed and sent to the secondary source.
$$ y(n) = y_{ff}(n) + y_{fb}(n) $$

### 2. Pseudo-Cascaded Hybrid
A more integrated approach proposed by Benois (2020) for headphones, where FF, MVC (Optimal Feedback), and IMC (Adaptive Feedback) are combined in a multi-stage optimization framework. This structure allows for:
- Low memory and computational overhead.
- Compensation of the secondary path for both FF and FB components.

## Application: Active Headphones

Most modern high-end ANC headphones use a hybrid approach:
- **Feedforward microphone** (outside the ear cup): Cancels external ambient noise like engine roar or wind.
- **Feedback microphone** (inside the ear cup, near the speaker): Cancels noise that leaked through the seal or was introduced by the feedforward system's modeling errors.

## Related Concepts

- [[feedforward-anc|Feedforward ANC]]
- [[feedback-anc|Feedback ANC]]
- [[active-noise-control|Active Noise Control]]
- [[internal-model-control|Internal Model Control]]
- [[minimum-variance-control|Minimum Variance Control]]
- [[acoustic-feedback|Acoustic Feedback]]

## Related Sources

- [[../sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]]
- [[../sources/benois-2020-hybrid-pseudo-cascaded-anc-headphones|Benois 2020: Hybrid and Pseudo-Cascaded ANC for Headphones]]
