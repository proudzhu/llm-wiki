---
type: concept
created: 2026-04-26
updated: 2026-09-12
sources:
  - raw/papers/serizel-2010-integrated-anc-nr-hearing-aids/full-text.md
  - wiki/sources/shen-2023-advanced-anc.md
  - raw/papers/zhang-2014-causality-feedforward-anc-headset/full-text.md
  - raw/papers/xiao-2023-spatially-selective-anc/full-text.md
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
- **Feedback ANC bypasses causality**: Since feedback ANC uses only the error signal, it does not require a time-advanced reference — but it is subject to the [[concepts/feedback-anc|waterbed effect]] instead

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

## Hearing Aids: The Extreme Case (Serizel et al. 2010)

In hearing aids the causality margin is structured as: the acoustic delay from the noise source to the ear-canal (error) microphone must exceed the *sum* of the source-to-reference-microphone delay, the hearing-aid processing delay, the algorithmic delay, and the secondary-path acoustic delay. The surplus — the **degree of causality** $\nu$, in samples — bounds the usable ANC bandwidth; performance vanishes quickly once the criterion is violated. Because the microphone–loudspeaker distance in a hearing aid is a few centimeters, the margin is only a few samples at standard sampling rates (ν = 2 measured for a 270° noise DOA by Serizel et al.).

When ANC is combined with noise reduction, the *topology* determines whether the NR delay consumes this margin:

- **Cascaded NR + ANC**: the NR delay (half the NR filter length, e.g. 32 samples) must fit inside ν, forcing an NR/ANC performance trade-off that is generally impossible at hearing-aid margins.
- **Integrated ([[concepts/filtered-x-mwf|FxMWF]])**: the filter decomposes into an NR part and an ANC part that does not depend on the NR delay, so only overall-system causality is required — no trade-off. The integrated scheme keeps >10 dB SNR improvement at ν = 2 where the cascade yields ~1 dB.

## Neural ABSE and the STFT Delay Problem (Hu et al. 2026)

[[concepts/abse-net|ABSE-NET]] (Hu et al. 2026) illustrates how neural ANC-style methods can appear to bypass the causality constraint while actually deferring it. Its leakage-cancellation pipeline (STFT with 320-sample window / 160 hop at 16 kHz → BMVDR → LNN → iSTFT) incurs **≥ 20–40 ms algorithmic delay**, while the physical margin — external noise → vent → ear-canal vs. loudspeaker → ear-canal, both a few cm — is on the order of 0.1–0.2 ms (cf. Serizel's ν = 2 samples). The constraint is violated by 2–3 orders of magnitude for broadband leakage.

The reported results sidestep this because evaluation is offline simulation: the ear-canal sum $e_L = g_L\hat{u} + d_L$ is synthesized with sample-level time alignment, so the algorithm's latency never enters a real-time acoustic loop. The network learns a *predictive* mapping (target $-d_L/g_L$ implicitly pre-inverts the secondary path, as in DeepANC), which can only cancel the *predictable* component of the leakage — vent leakage is low-frequency dominated and NOISEX-92 noises are stationary, i.e., the narrowband/predictable-noise regime where delay is not the binding constraint. Whether the broadband leakage component (unforecastable over a 20–40 ms horizon) survives real-time deployment is untested; the paper cites Xiao & Doclo 2024 on delay effects in open-fitting hearables but performs no delay-budget analysis, and its cascaded BSE→ANC topology is exactly the structure Serizel et al. 2010 showed to collapse (~1 dB) at hearing-aid causality margins.

## Solutions to Causality Violations

1. **Wireless Reference ANC** (Shen 2023): Place reference microphones near noise sources and transmit wirelessly, providing "look-ahead" time
2. **Reduce loop delay**: Faster ADCs/DACs, shorter filter lengths, efficient DSP implementations
3. **Prediction-based approaches**: Use signal predictability to compensate for delay (effective for periodic noise)
4. **Multiple reference microphones**: Place additional reference microphones on the headset to ensure causal reference for noise from any direction (Zhang & Qiu 2014)

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/feedforward-anc|Feedforward ANC]]
- [[concepts/feedback-anc|Feedback ANC]]
- [[concepts/hybrid-anc|Hybrid ANC]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/wiener-filter|Wiener Filter]]
- [[concepts/selective-fixed-filter-anc|Selective Fixed-Filter ANC]] — direction-dependent causality motivates D-SFANC
- [[concepts/filtered-x-mwf|Filtered-x MWF (FxMWF)]] — topology that decouples ANC performance from the NR delay

## Related Sources

- [[sources/shen-2023-advanced-anc|Shen 2023: Advanced ANC Headphone]] — Wireless Reference ANC to overcome causality constraints
- [[sources/zhang-2014-causality-feedforward-anc-headset|Zhang 2014: Causality Study on Feedforward ANC Headset]] — systematic analysis of direction-dependent causality
- [[sources/serizel-2010-integrated-anc-nr-hearing-aids|Serizel, Moonen, Wouters & Jensen 2010: Integrated ANC and NR in Hearing Aids]] — degree of causality in hearing aids; two-sample realistic margin
- [[sources/hu-2026-abse-net|Hu et al. 2026: ABSE-NET]] — neural ABSE whose STFT pipeline (≥ 20–40 ms delay) violates the hearing-aid causality margin; offline simulation defers rather than solves the constraint
- [[sources/xiao-2023-spatially-selective-anc|Xiao, Xu & Zhao 2023: Spatially Selective Active Noise Control Systems]]

