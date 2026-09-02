---
type: concept
created: 2026-04-10
updated: 2026-09-02
sources:
  - raw/papers/vanwaterschoot-2011-fifty-years-afc/full-text.md
  - raw/papers/miran-2026-imu-feedback-cancellation/full-text.txt
  - raw/papers/williams-2014-acoustic-feedback-elimination/full-text.md
  - raw/papers/hoshuyama-2026-sound-object-echo-control/full-text.md
tags:
- acoustic
- active-noise-control
- feedback
---

# Acoustic Feedback

## Overview

**Acoustic feedback** in ANC systems occurs when the anti-noise signal from the canceling loudspeaker radiates **upstream** back to the reference microphone, corrupting the reference signal. This is analogous to the "howling" feedback in public address systems.

## The Problem

In a [[broad-band-feedforward-anc|Broad-Band Feedforward ANC]] system:

```
Loudspeaker (anti-noise) → radiates upstream → Reference microphone → corrupted x(n)
```

The corrupted reference signal becomes:

```
x'(n) = x(n) + f(n) * y(n)
```

where f(n) is the **feedback path** from loudspeaker to reference microphone.

This creates a **closed loop** that can become unstable if the open-loop phase lag reaches 180° while the gain exceeds unity.

## Optimal Transfer Function with Feedback

When feedback is present, the optimal controller becomes an **IIR function**:

```
W(z) = P(z) / [S(z) + F(z)·P(z)]
```

This has both poles and zeros, making it fundamentally different from the FIR solution without feedback.

## PA-System Closed-Loop Formalization

In a public address (PA) / sound-reinforcement system, the same closed-loop physics produces the [[concepts/acoustic-howling-suppression|howling]] artifact. Van Waterschoot & Moonen (2011) formalize the single-channel PA system as:

$$\bar{\mathbf{y}}(t) = \mathbf{F}(q,t)\bar{\mathbf{u}}(t) + \bar{\mathbf{v}}(t), \qquad \bar{\mathbf{u}}(t) = \mathbf{G}[\bar{\mathbf{y}}(t),t]$$

with closed-loop frequency response $U/V = G/(1 - GF)$, where $G(\omega,t)F(\omega,t)$ is the **loop response**. The **Nyquist stability criterion** states the loop is unstable iff $|GF| \geq 1$ *and* $\angle GF = n \cdot 2\pi$; this is the common root from which all four categories of automatic feedback control are derived:

- **Phase modulation** ([[concepts/phase-modulating-feedback-control|PFC]]) — bypasses the phase condition via an LPTV forward-path filter.
- **Gain reduction** ([[concepts/notch-filter-based-howling-suppression|NHS]], AGC, AEQ) — breaks the magnitude condition by reducing gain at critical frequencies.
- **Spatial filtering** — beamforming to reduce the loop gain.
- **Room modeling** ([[concepts/adaptive-feedback-cancellation|AFC]]) — estimates and subtracts the feedback component, removing the coupling.

The achievable amplification is bounded by the [[concepts/maximum-stable-gain|MSG]]; Schroeder's statistical room-acoustics result sets a ~10 dB upper bound for loop-gain-smoothing methods, while AFC is not bound by it.

### Inter-Terminal Loops and Object-Identity Gating

All four categories above assume the loop can be modeled or attenuated **locally**. A distinct regime arises in multi-terminal conferencing: the feedback path traverses the **communication server and network** (microphone A2 → codec → server → loudspeaker A1 → back to A2), with delay variation, nonlinear in-device processing, and user-mute fragmentation, making path estimation infeasible (Hoshuyama 2026). [[concepts/sound-object-based-echo-control|Sound-object-based echo control]] bypasses the loop model altogether: default mute with pass only when the signal is judged *not identical* to recently observed sound objects breaks the magnitude condition by construction, without path knowledge — a fifth, non-path-based control category extending [[concepts/voice-switched-half-duplex|voice-switched half-duplex]] to conditional half-duplex.

## Solutions

### 1. Feedback Neutralization

Use a separate **feedback cancellation filter** to subtract the estimated feedback component:

```
x_clean(n) = x'(n) - f̂(n) * y(n)
```

- The feedback neutralization filter f̂(n) must be estimated **offline** (during ANC idle periods)
- Similar to **acoustic echo cancellation** in telephony
- Must be inhibited during ANC operation (like "double talk" detection)

### 2. Adaptive IIR Filters (Filtered-U LMS)

Model the optimal IIR solution directly using the **filtered-U recursive LMS** algorithm:
- Lower order than FIR equivalent (poles make it more efficient)
- **Disadvantage**: IIR filters are not unconditionally stable

### 3. High-Order FIR with Smaller Step Size

Approximate the IIR solution with a sufficiently high-order FIR filter:
- Requires a **smaller step size** for stability
- Slower convergence but unconditionally stable

### 4. Adaptive Feedback Cancellation (AFC) in Hearing Aids

In hearing aids, AFC uses an adaptive filter (typically PEM-NLMS) to estimate and subtract the feedback component. The step-size dilemma is central:
- **Large step size**: Fast convergence after path changes (e.g., hat on/off, phone near ear) but high steady-state error
- **Small step size**: Low steady-state error but slow convergence → whistling artifacts during transitions

**Audio-only VSS methods** (shadow filter, VSS-NLMS) are biased by input audio characteristics and cannot reliably distinguish feedback path changes from input signal changes.

**IMU-based step-size control** (Miran et al. 2026): Uses head movement acceleration from an integrated IMU to detect feedback path changes. When motion is detected → large step size; when stationary → small step size. Outperforms audio-only methods in steady-state by avoiding audio-induced biases, but cannot detect path changes from external objects that precede head movement.

## Impact on Different ANC Types

| ANC Type | Feedback Impact |
|----------|----------------|
| Broad-band feedforward | Severe — corrupts reference signal |
| Narrow-band feedforward | None — reference signals internally generated |
| Feedback ANC | N/A — no reference sensor exists |

**DeepPEM-AFC** (Zhan et al. 2025): Combines PEM de-correlation with GRU-based step-size prediction. Uses frequency-domain PEM for reduced complexity and a simulated path generation scheme for generalization. FS+DeepPEM-AFC achieves optimal performance across all speech quality metrics.

## Related Concepts

- [[broad-band-feedforward-anc|Broad-Band Feedforward ANC]]
- [[narrow-band-feedforward-anc|Narrow-Band Feedforward ANC]]
- [[internal-model-control|Internal Model Control]]
- [[simplified-adaptive-feedback-anc|Simplified Adaptive Feedback ANC]]
- [[variable-step-size-lms|Variable Step Size LMS]]
- [[prediction-error-method|Prediction Error Method]]
- [[online-feedback-path-modeling|Online Feedback-Path Modeling]] — adaptive compensation of the time-varying FBP during ANC operation
- [[supporting-filter-anc|Supporting Filter in ANC]] — auxiliary filter for decoupling OFBPM/OSPM from the controller
- [[auxiliary-noise-scaling|Auxiliary Noise Scaling]] — AWGN power scheduling shared by OFBPM and OSPM
- [[hearing-aid-feedback-cancellation|Hearing Aid Feedback Cancellation]]
- [[frequency-shift-feedback-cancellation|Frequency Shift Feedback Cancellation]]
- [[maximum-stable-gain|Maximum Stable Gain]]
- [[phase-modulating-feedback-control|Phase-Modulating Feedback Control (PFC)]] — PA-system feedback control via loop-gain smoothing
- [[adaptive-feedback-cancellation|Adaptive Feedback Cancellation (AFC)]] — PA/HA feedback control via feedback-path modeling
- [[decorrelation-for-afc|Decorrelation for AFC]] — bias reduction for AFC identification
- [[acoustic-howling-suppression|Acoustic Howling Suppression]] — the howling artifact of PA-system acoustic feedback
- [[concepts/sound-object-based-echo-control|Sound-Object-Based Echo Control]] — non-path-based control for inter-terminal feedback loops

## Related Concepts

- [[concepts/deep-marginal-feedback-cancellation|Deep Marginal Feedback Cancellation]]
- [[concepts/closed-loop-fine-tuning|Closed-Loop Fine Tuning]]
- [[concepts/ballistics-based-howling-detection|Ballistics-Based Howling Detection]] — PA-system HD front end exploiting persistence of feedback vs transience of music
- [[concepts/trial-and-verify-notch-insertion|Trial-and-Verify Notch Insertion]] — PA-system NHS verification by probing the closed loop with a trial notch

## Related Sources

- [[sources/vanwaterschoot-2011-fifty-years-afc|van Waterschoot & Moonen 2011]] — the canonical PA-system closed-loop formalization, the Nyquist stability criterion, the four-category taxonomy of feedback control, and the comparative evaluation of PFC/NHS/AFC
- [[sources/hao-2025-l3c-deepmfc|Hao et al. 2025: L3C-DeepMFC]] — Low-latency low-complexity deep marginal feedback cancellation
- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] — Section II-D: Feedback Effects and Solutions
- [[sources/miran-2026-imu-feedback-cancellation|Miran 2026: IMU-Based Acoustic Feedback Cancellation]]
- [[sources/zhan-2025-deeppem-afc|Zhan 2025: DeepPEM-AFC]] — Deep learning-based PEM-AFC with GRU step-size prediction
- [[sources/ma-2027-robust-ffanc-online-path-modeling|Ma 2027: Robust FFANC with Simultaneous OSPM and OFBPM]] — performs OFBPM adaptively during ANC operation; demonstrates that an SF-driven global AWGN scaling and a second supporting filter $H_2(z)$ keep the residual-AWGN floor low even under abrupt FBP changes
- [[sources/mounir-2025-robust-early-howling-detection-sparsity|Mounir, Bernardi & van Waterschoot 2025]] — formalizes the PA/hearing-aid closed-loop model with the Nyquist stability criterion (loop gain ≥ 1 and loop phase = $n2\pi$) and the MSG definition; the same closed-loop instability physics underlies ANC and acoustic-howling feedback
- [[sources/williams-2014-acoustic-feedback-elimination|Williams 2014]] — Harman patent (US 8,634,575 B2) for a two-rate NHS system: ballistics-based candidate detection + trial-and-verify notch insertion in PA/sound-reinforcement systems
- [[sources/hoshuyama-2026-sound-object-echo-control|Hoshuyama 2026]] — inter-terminal feedback loops traversing the communication server, and object-identity gating as a non-path-based control category

## Related Entities

- [[entities/sen-m-kuo|Sen M. Kuo]] — Comprehensive treatment of feedback neutralization techniques
- [[entities/henning-schepker|Henning Schepker]] — AFC in hearing aids, shadow filter and beamformer approaches
- [[entities/chengshi-zheng|Chengshi Zheng]] — DeepPEM-AFC, frequency shift analysis for hearing aids
- [[entities/xiaofan-zhan|Xiaofan Zhan]] — DeepPEM-AFC
