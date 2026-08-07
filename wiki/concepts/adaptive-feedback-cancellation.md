---
type: concept
created: 2026-08-07
updated: 2026-08-07
sources:
  - raw/papers/vanwaterschoot-2011-fifty-years-afc/full-text.md
tags:
  - acoustic-feedback
  - adaptive-filters
  - system-identification
  - sound-reinforcement
  - hearing-aids
aliases:
  - AFC
---

# Adaptive Feedback Cancellation (AFC)

**Adaptive feedback cancellation (AFC)** is an [[concepts/acoustic-feedback|acoustic feedback]] control method that estimates the acoustic feedback path with an adaptive filter and subtracts the predicted feedback component from the microphone signal, thereby removing the acoustic loudspeaker–microphone coupling and breaking the closed loop. It is the "room modeling" category of the [[sources/vanwaterschoot-2011-fifty-years-afc|van Waterschoot & Moonen 2011]] taxonomy and is widely considered the most promising solution to the acoustic feedback problem.

> **Not to be confused with** [[concepts/adaptive-feedback-control|Adaptive Feedback Control]] (ANC feedback control), which refers to feedback ANC architectures (IMC, SimpAFB) that adapt a controller without a reference sensor. AFC here refers specifically to adaptive *cancellation* of the acoustic feedback path in sound-reinforcement / hearing-aid systems.

## Principle

The loudspeaker signal $u(t)$ is filtered by an adaptive model $\hat{F}(q,t)$ of the feedback path, producing a feedback estimate that is subtracted from the microphone signal $y(t)$:

$$d[t, \hat{\mathbf{f}}(t)] = y(t) - \mathbf{u}^T(t)\hat{\mathbf{f}}(t)$$

The closed-loop frequency response becomes

$$\frac{U(\omega,t)}{V(\omega,t)} = \frac{G(\omega,t)}{1 - G(\omega,t)[F(\omega,t) - \hat{F}(\omega,t)]}$$

so the achievable [[concepts/maximum-stable-gain|MSG]] depends on the *residual* $F - \hat{F}$ at critical frequencies: the better the fit, the larger the MSG. If $\hat{F} \equiv F$, the loop is broken and the MSG is infinite. Reported MSG increases are 15–20 dB theoretically; 9–12 dB in practice with decorrelating prefilters (AFC-PF).

## The Closed-Loop Identification Bias Problem

Although AFC is conceptually similar to acoustic echo cancellation (AEC), the closed-loop nature of the system creates a fundamental problem. The LS estimate of the feedback-path impulse response is **biased**:

$$\mathrm{bias}\{\hat{\mathbf{f}}(t)\} = E\{(\mathbf{U}^T\mathbf{U})^{-1}\mathbf{U}^T\mathbf{v}\} \neq \mathbf{0}$$

because the source signal $\mathbf{v}$ and the loudspeaker signal $\mathbf{u}$ are correlated *through the loop*. The adaptive filter therefore does not only cancel the feedback component but also (part of) the source signal, distorting the feedback-compensated signal $d$. The problem is a continuous version of the AEC double-talk situation, worsened by source-signal coloration. A **decorrelation** procedure is essential — see [[concepts/decorrelation-for-afc|Decorrelation for AFC]].

## Adaptive Algorithms

| Algorithm | Cost / sample | Notes |
|-----------|---------------|-------|
| RLS | $O(n_{\hat{F}}^2)$ | Exponential forgetting; matrix-inversion lemma avoids explicit inversion |
| Fast RLS | $O(n_{\hat{F}})$ | Relies on shift-invariance — breaks under nonlinear/time-varying decorrelation |
| APA | $O(M n_{\hat{F}})$ | Projection order $M$; decorrelates $M$th-order all-pole inputs |
| **NLMS** | $O(n_{\hat{F}})$ ($4n_{\hat{F}}+6$) | Preferred for real-time; $M=1$ special case of APA |

Typical NLMS step sizes: $\mu \in [0.01, 0.05]$ for speech, $\mu \approx 0.005$ for audio. The adaptive filter order $n_{\hat{F}}$ should match the feedback-path impulse response length $n_F$ — undermodeling ($n_{\hat{F}} < n_F$) adds bias and variance.

## Robustness Features

- **Adaptation control** — freeze coefficients during source-signal onsets.
- **Foreground/background filtering** — combine good tracking with small steady-state error.
- **Regularization** — Bayesian MMSE framework; Tikhonov (TR, prior mean $\mathbf{f}_0 = \mathbf{0}$) or Levenberg–Marquardt (LMR, $\mathbf{f}_0 = \hat{\mathbf{f}}(t-1)$) variants: TR-RLS, LMR-RLS, LMR-APA, LMR-NLMS. Covariance $\mathbf{R}_f$ built from an initial measurement or room-acoustic parameters.
- **Postfiltering** — spectral subtraction of residual feedback (Janse–Belt; Ortega et al.), or proactive notch filtering from the estimated loop gain (Rombouts et al.).
- **Subband / frequency-domain implementation** — reduces computational load.

## Variants and Comparative Performance

The 2011 survey evaluates three AFC variants differing in decorrelation:

| Variant | Decorrelation | Speech mean ΔMSG | Audio mean ΔMSG | Sound quality |
|---------|--------------|------------------|-----------------|---------------|
| AFC-NI | Noise injection (in loop) | up to 9.8 dB (ΔK=10) | 6.3 dB (ΔK=10) | Poor (SD 13.8–19.9 dB) |
| AFC-FS | Frequency shifting (in loop) | 6.6 dB (ΔK=10) | 5.4 dB (ΔK=10) | Medium (SD 5.6–7.1 dB) |
| **AFC-PF** | Decorrelating prefilters (in circuit) | 9.6 dB (ΔK=10) | 9.0 dB (ΔK=10) | **Best** (SD 2.4–5.3 dB) |

AFC-PF (PEM-AFROW) is the practical state of the art: ~9 dB mean / ~12 dB max ΔMSG with the lowest signal distortion and robust behavior after feedback-path changes, because decorrelation in the adaptive filtering circuit does not distort the loudspeaker signal.

## Challenges and Future Directions

- **Computational complexity**: even with NLMS, the high filter order (e.g., 2048–2646 taps) and high sampling rate for audio make real-time single-channel AFC demanding. IIR / pole-zero or orthogonal-basis (Laguerre, Kautz) feedback-path models — exploiting time-invariant room resonance frequencies — are proposed but unexplored in AFC.
- **Multichannel AFC**: complexity scales with $S \times L$ (microphones × loudspeakers). Shared-denominator IIR models and identifiability under correlated loudspeaker signals are open problems (analogous to multichannel AEC).
- **Hybrid AFC**: combining AFC with postfiltering, gain reduction (ANF/AEQ/NHS), or beamforming. The survey argues existing hybrids are *suboptimal* because the components are designed independently; **joint estimation** of AFC + postfilter / gain-reduction / beamformer coefficients is expected to outperform decoupled designs.

## Related Concepts

- [[concepts/acoustic-feedback|Acoustic Feedback]] — the problem AFC solves
- [[concepts/decorrelation-for-afc|Decorrelation for AFC]] — the bias problem and decorrelation taxonomy
- [[concepts/maximum-stable-gain|Maximum Stable Gain]] — the achievable-amplification metric
- [[concepts/prediction-error-method|Prediction Error Method]] — PEM-AFROW, the AFC-PF realization
- [[concepts/hearing-aid-feedback-cancellation|Hearing Aid Feedback Cancellation]] — HA application domain
- [[concepts/frequency-shift-feedback-cancellation|Frequency Shift Feedback Cancellation]] — FS as an AFC decorrelator (AFC-FS)
- [[concepts/phase-modulating-feedback-control|Phase-Modulating Feedback Control (PFC)]] — competing loop-gain-smoothing method
- [[concepts/notch-filter-based-howling-suppression|Notch-Filter-Based Howling Suppression (NHS)]] — competing gain-reduction method; combined with AFC in hybrid schemes
- [[concepts/adaptive-feedback-control|Adaptive Feedback Control]] — the ANC feedback-control concept (distinct from AFC)

## Related Sources

- [[sources/vanwaterschoot-2011-fifty-years-afc|van Waterschoot & Moonen 2011]] — the survey formalizing AFC, the bias analysis, the decorrelation taxonomy, and the comparative evaluation
- [[sources/zhan-2025-deeppem-afc|Zhan 2025: DeepPEM-AFC]] — deep-learning PEM-AFC extending the PEM-AFROW line for hearing aids
- [[sources/lydaki-2026-deep-feedback-cancellation-hearing-aids|Lydaki 2026: Deep Feedback Cancellation]] — deep-learning DFC for hearing aids
- [[sources/miran-2026-imu-feedback-cancellation|Miran 2026: IMU-Based Acoustic Feedback Cancellation]] — IMU-based step-size control for HA-AFC
