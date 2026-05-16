---
type: concept
created: 2026-04-10
updated: 2026-04-10
sources:
tags:
- active-noise-control
- dsp
- multi-channel
---

# Multi-Channel ANC

## Overview

**Multi-channel ANC** extends single-channel ANC systems to handle multiple reference sensors, multiple secondary sources (loudspeakers/actuators), and multiple error sensors simultaneously.

## Motivation

Single-channel ANC works well at a single point but cannot provide adequate noise reduction over a large spatial region. Multi-channel systems can:
- Attenuate noise over **larger volumes**
- Handle **multiple noise sources**
- Achieve better **spatial coverage**

## Architectures

### Multiple Reference Inputs (MRI)
- Multiple reference sensors, single secondary source, single error sensor
- Example: multiple microphones placed upstream in a duct

### Multiple-Channel Feedforward (MIMO)
- Multiple reference sensors → multiple secondary sources → multiple error sensors
- Uses the **multichannel FxLMS algorithm**

## Multichannel FxLMS Algorithm

For a system with M secondary sources, L filter taps, and N error sensors:

- Each reference signal must be filtered through **each secondary path estimate** to **each error sensor**
- The weight update for each channel uses the sum of contributions from all error sensors
- **Computational complexity**: O(M · L · N)

This grows rapidly: a 4×4 system (4 secondary sources, 4 error sensors) with 256-tap filters requires filtering through 16 secondary paths.

## Computational Challenge

The main challenge is the **explosive growth in computation**. For each error sensor n and each secondary source m, the reference signal must be convolved with Ŝ_{mn}(z). This motivates research into:
- [[frequency-domain-anc|Frequency-Domain ANC]] (FFT-based efficiency)
- [[subband-anc|Subband ANC]] (parallel processing in frequency subbands)
- [[simplified-adaptive-feedback-anc|Simplified Adaptive Feedback ANC]] (reducing computation in feedback systems)

## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[broad-band-feedforward-anc|Broad-Band Feedforward ANC]]
- [[frequency-domain-anc|Frequency-Domain ANC]]
- [[subband-anc|Subband ANC]]
- [[simplified-adaptive-feedback-anc|Simplified Adaptive Feedback ANC]]

## Related Sources

- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] — Section V: Multiple-Channel ANC
