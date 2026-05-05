---
type: concept
created: 2026-04-26
updated: 2026-05-05
sources:
  - wiki/sources/shen-2023-advanced-anc.md
  - raw/papers/zhang-2014-causality-feedforward-anc-headset/full-text.md
tags:
  - active-noise-control
  - control-theory
  - causality
---

# Causality in ANC

**Causality** in Active Noise Control refers to the requirement that the anti-noise signal must arrive at the cancellation point at the same time as (or before) the primary noise. If the total delay through the controller and secondary path exceeds the acoustic propagation delay from the noise source to the error sensor, the system cannot achieve cancellation.

## The Causality Constraint

For a feedforward ANC system, the causality condition requires:

$$\tau_{controller} + \tau_{secondary} \leq \tau_{acoustic}$$

where:
- $\tau_{controller}$: processing delay of the digital controller (ADC + DSP + DAC)
- $\tau_{secondary}$: propagation delay through the secondary path (loudspeaker → acoustic path → microphone)
- $\tau_{acoustic}$: propagation delay of the primary noise from the reference sensor to the error sensor

## Implications

- **Broadband ANC is delay-limited**: The maximum cancellation bandwidth is inversely proportional to the total loop delay. Typical headphone ANC systems have ~0.5 ms loop delay, limiting effective broadband cancellation to ~1 kHz
- **Narrowband ANC is not delay-limited**: Periodic noise can be predicted from past samples, so causality is not a constraint for narrow-band feedforward ANC
- **Feedback ANC bypasses causality**: Since feedback ANC uses only the error signal, it does not require a time-advanced reference — but it is subject to the [[../concepts/feedback-anc|waterbed effect]] instead

## Direction-Dependent Causality (Zhang & Qiu 2014)

The causality condition of a feedforward ANC headset depends on the noise arrival direction. Zhang & Qiu (2014) demonstrated that for a typical headset:

- **0° source** (frontal): $\Delta_p = 7 > \Delta_s = 6$ → **causal**, good broadband cancellation
- **90° source** (lateral): $\Delta_p = 5 < \Delta_s = 6$ → **non-causal**, significantly degraded performance

The primary path delay varies with source direction according to:

$$\Delta_p = [(l_2 - l_1)/c + t_a]f_s$$

where $l_1$ is the source-to-reference distance, $l_2$ is the source-to-error distance, and $t_a$ is the earmuff delay. When the source moves from 0° to 90°, the reference microphone becomes closer to the source than the error microphone, reducing $\Delta_p$ and potentially violating causality.

### Non-Causal Performance Degradation

For band-limited noise, non-causal delay degrades performance in **two ways** (not just overall reduction):

1. **Narrowed attenuation bandwidth** — the frequency range of effective cancellation shrinks
2. **Decreased maximum noise reduction** — the peak cancellation level drops

Increasing the control filter length **cannot** compensate for non-causality, because the front part of the ideal impulse response is missing and cannot be recovered by a longer filter.

### Systematic Prediction Method

Zhang & Qiu developed a Wiener-filter-based method (Eqs. 9–14 in their paper) that predicts ANC performance with measured primary and secondary paths in arbitrary sound fields, going beyond simplified pure-delay models. Validated in both anechoic and reverberant chambers.

## Solutions to Causality Violations

1. **Wireless Reference ANC** (Shen 2023): Place reference microphones near noise sources and transmit wirelessly, providing "look-ahead" time
2. **Reduce loop delay**: Faster ADCs/DACs, shorter filter lengths, efficient DSP implementations
3. **Prediction-based approaches**: Use signal predictability to compensate for delay (effective for periodic noise)
4. **Multiple reference microphones**: Place additional reference microphones on the headset to ensure causal reference for noise from any direction (Zhang & Qiu 2014)

## Related Concepts

- [[../concepts/active-noise-control|Active Noise Control]]
- [[../concepts/feedforward-anc|Feedforward ANC]]
- [[../concepts/feedback-anc|Feedback ANC]]
- [[../concepts/hybrid-anc|Hybrid ANC]]
- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[../concepts/wiener-filter|Wiener Filter]]
- [[../concepts/selective-fixed-filter-anc|Selective Fixed-Filter ANC]] — direction-dependent causality motivates D-SFANC

## Related Sources

- [[../sources/shen-2023-advanced-anc|Shen 2023: Advanced ANC Headphone]] — Wireless Reference ANC to overcome causality constraints
- [[../sources/zhang-2014-causality-feedforward-anc-headset|Zhang 2014: Causality Study on Feedforward ANC Headset]] — systematic analysis of direction-dependent causality
