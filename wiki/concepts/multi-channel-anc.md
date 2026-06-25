---
type: concept
created: 2026-04-10
updated: 2026-06-25
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

## ANC Casing Application

An **ANC casing** is a practical multi-channel ANC application — a noise source enclosed in a sound-proof shield with an opening for ventilation. Control sources (loudspeakers) are distributed at the opening to transmit anti-noise. Error microphones must be placed near the control sources (to avoid protuberance), but the target ZoQ is farther away, requiring [[concepts/virtual-sensing|virtual sensing]].

A representative implementation[^shi2020] uses a (1,4,4) configuration: 1 reference microphone inside the casing, 4 loudspeakers, 4 monitoring microphones near the speakers, and 4 virtual microphones (used only during tuning). This configuration highlights the **spatial coverage** motivation — a single-channel system cannot form a large enough ZoQ at the desired location.

For multi-channel systems, virtual sensing is more challenging than single-channel because cross-channel acoustic paths introduce errors in the relative path models. All VS methods show reduced performance in multi-channel relative to single-channel configurations, but the [[concepts/relative-path-virtual-sensing|RP-VS]] method achieves the best average noise reduction.

[^shi2020]: [[sources/shi-2020-active-noise-control-casing-virtual-sensing|Shi, Jia, Xie & Li 2020: ANC Casing with RP-VS]]

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

## PINN-Assisted Multi-Channel ANC

In the PINN-assisted ANC system ([[sources/zhang-2024-active-noise-control-soundfield-interpolation-pinn|Zhang et al. 2024]]), the standard multiple-point FxLMS is modified so that the error signals driving the weight update are the **interpolated virtual microphone signals** rather than the physical monitoring microphone signals. A [[concepts/physics-informed-neural-network|PINN]] trained on $Q = 8$ monitoring microphones with the wave equation PDE loss interpolates the soundfield at $V = 2$ virtual ear positions. This means the controller minimizes noise at the *listener's ears* rather than at the monitoring microphones, achieving −13 dB more noise reduction than the baseline multiple-point system.

## Related Sources

- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] — Section V: Multiple-Channel ANC
- [[sources/zhang-2024-active-noise-control-soundfield-interpolation-pinn|Zhang et al. 2024: ANC with PINN-based Soundfield Interpolation]]
