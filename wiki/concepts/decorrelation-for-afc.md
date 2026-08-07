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
  - bias
aliases:
  - AFC Decorrelation
---

# Decorrelation for AFC

**Decorrelation for AFC** refers to the family of techniques used in [[concepts/adaptive-feedback-cancellation|adaptive feedback cancellation (AFC)]] to reduce the correlation between the source signal and the loudspeaker signal, which otherwise causes a biased feedback-path estimate and distortion of the feedback-compensated signal. The [[sources/vanwaterschoot-2011-fifty-years-afc|van Waterschoot & Moonen 2011]] survey synthesizes these techniques into a two-axis taxonomy that is the structuring reference for the field.

## The Bias Problem

In AFC, the LS estimate of the feedback-path impulse response is biased because the closed signal loop induces correlation between the source signal $\mathbf{v}$ and the loudspeaker signal $\mathbf{u}$:

$$\mathrm{bias}\{\hat{\mathbf{f}}(t)\} = E\{(\mathbf{U}^T\mathbf{U})^{-1}\mathbf{U}^T\mathbf{v}\} \neq \mathbf{0}$$

The adaptive filter then partially cancels the source signal along with the feedback, distorting the feedback-compensated signal $d[t, \hat{\mathbf{f}}(t)]$. This is a continuous version of the AEC double-talk problem, worsened by source-signal coloration (denser source covariance matrix $\mathbf{R}_v$). Decorrelation aims to break this correlation so the estimate converges to the true feedback path.

## Two-Axis Taxonomy

The 2011 survey distinguishes decorrelation methods along two axes: *where* the decorrelating operation is inserted, and *what* the operation is.

### Axis 1 — In the closed signal loop vs. in the adaptive filtering circuit

| Location | Loudspeaker signal distorted? | Bias–quality tradeoff? |
|----------|------------------------------|------------------------|
| **In the closed signal loop** | Yes — operation is in the forward path | Yes: strong decorrelation is audible; weak decorrelation leaves bias |
| **In the adaptive filtering circuit** | No — operation only touches the signals fed to the adaptive filter | No: stronger decorrelation → *better* sound quality |

The second location is strictly preferable for sound quality and is the basis of the AFC-PF variant that wins the survey's comparative evaluation.

### Axis 2 — The decorrelating operation

**In the closed signal loop:**

- **Noise injection (NI)** — add a (psychoacoustically shaped) white noise signal $n(t)$ to the feedback-compensated signal before amplification. The adaptive filter uses either $u(t)$ (reduced but nonzero bias) or $n(t)$ (unbiased but slow convergence) as input. Audible noise is unavoidable; A-weighting / psychoacoustic noise shaping reduce audibility at the cost of decorrelation effectiveness.
- **Time-varying processing** — insert an LPTV filter in the forward path. The [[concepts/phase-modulating-feedback-control|PFC]] filters (FS, PM, DM) double as decorrelators; FS is acceptable for speech but perceptually inadequate for audio. Beneficial side effect: the LPTV filter also stabilizes the loop by smoothing the loop gain.
- **Nonlinear processing** — halfwave rectification (borrowed from stereo AEC), applied in the forward path.
- **Processing delay** — insert a delay $q^{-d_1}$; effective for source signals with rapidly decaying autocorrelation (e.g., voiceless speech).

**In the adaptive filtering circuit:**

- **Adaptive-filter delay** — exploit the feedback-path initial delay ("dead time") $d_2 T_s$: force the first $d_2$ coefficients of $\hat{F}$ to zero so the biased terms drop out of the LS estimate. Requires a priori knowledge of the dead time.
- **Decorrelating prefilters (PF)** — prefilter the loudspeaker and microphone signals with the inverse $\hat{H}^{-1}(q,t)$ of an estimated source-signal model $H(q,t)$ before feeding them to the adaptive filter. This is an unbiased system-identification approach: the source model captures the source correlation structure, leaving the prefiltered input whitened. The source model is estimated concurrently with the feedback path using a **prediction-error method (PEM-AFROW)**. For speech, $H(q,t)$ is a cascade of a three-tap fractional pitch predictor $1/A(q,t)$ and an all-pole vocal-tract model $1/C(q,t)$; for polyphonic audio, a constrained pole-zero model $B(q,t)/A(q,t)$ is added. This is the **AFC-PF** variant.

## Why AFC-PF Wins

The survey's comparative evaluation shows AFC-PF delivers ~9 dB mean / ~12 dB max ΔMSG with the lowest signal distortion (mean SD 2.4 dB speech / 3.7 dB audio) and robust behavior after feedback-path changes. The reason is structural: because the decorrelation operates *only* on the signals inside the adaptive filtering circuit, the loudspeaker signal is never distorted, and stronger decorrelation monotonically improves quality — unlike in-loop methods, which face an unavoidable bias–quality tradeoff.

## Tradeoffs and Open Problems

- In-loop decorrelation requires tuning to a bias–quality sweet spot; the survey notes "a perceptible signal distortion is unavoidable" either from the decorrelation itself (strong) or from residual bias (weak).
- Decorrelating prefilters require a concurrent source-signal model estimate; the model order, pitch-lag search range, and window length are application-specific.
- The concurrent estimation of the feedback-path initial delay *and* its coefficients is an open problem — only the delay-or-coefficients cases have been studied.
- Fast RLS / fast APA algorithms rely on shift-invariance of the loudspeaker-signal vector, which generally breaks under nonlinear or time-varying decorrelation, so cheap fast variants may not apply.

## Related Concepts

- [[concepts/adaptive-feedback-cancellation|Adaptive Feedback Cancellation (AFC)]] — the method this decorrelation taxonomy serves
- [[concepts/prediction-error-method|Prediction Error Method]] — PEM-AFROW, the realization of decorrelating prefilters
- [[concepts/phase-modulating-feedback-control|Phase-Modulating Feedback Control (PFC)]] — PFC filters double as in-loop decorrelators
- [[concepts/frequency-shift-feedback-cancellation|Frequency Shift Feedback Cancellation]] — FS as in-loop decorrelation (AFC-FS)
- [[concepts/acoustic-feedback|Acoustic Feedback]] — the underlying problem
- [[concepts/maximum-stable-gain|Maximum Stable Gain]] — the metric improved by reducing bias

## Related Sources

- [[sources/vanwaterschoot-2011-fifty-years-afc|van Waterschoot & Moonen 2011]] — the survey that synthesizes the two-axis decorrelation taxonomy and identifies in-circuit decorrelation (AFC-PF) as superior
- [[sources/zhan-2025-deeppem-afc|Zhan 2025: DeepPEM-AFC]] — deep-learning extension of PEM-AFROW decorrelation for hearing aids
