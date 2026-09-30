---
type: concept
created: 2026-09-30
updated: 2026-09-30
sources:
  - raw/papers/hoshuyama-1999-robust-adaptive-beamformer-ccaf/full-text.md
tags:
  - beamforming
  - microphone-arrays
  - robust-beamforming
---

# Target-Signal Cancellation

**Category**: Failure mode of adaptive beamforming

## Definition

**Target-signal cancellation** (also *signal self-cancellation*, *target cancellation*, or *desired-signal cancellation*) is the unwanted suppression of the desired source by an adaptive beamformer that mistakes it for interference. It is the dominant failure mode of adaptive microphone-array processing: the output sounds attenuated and distorted — subjectively heard as loss of high-frequency content — and the degradation is not recoverable by post-filtering, because the target has been removed from the reference path.

## Mechanisms

The same symptom arises from several distinct causes, which matters because each demands a different remedy.

| Mechanism | Where it appears | What happens |
|:----------|:-----------------|:-------------|
| **Steering-vector error** | GSC, MPDR, MVDR | The assumed look direction does not match the true target transfer function, so the target is not fully blocked and leaks into the adaptive reference path — see [[concepts/steering-vector-error|Steering-Vector Error]] |
| **Snapshot deficiency** | MPDR, MVDR | With fewer frames than microphones the sample [[concepts/spatial-covariance-matrix|SCM]] is ill-conditioned, the [[concepts/white-noise-gain|WNG]] collapses, and the beamformer places a null on the target |
| **RTF mismatch** | Informed / statistics-driven GSC | The noise canceller is updated with statistics that still contain target energy, so it learns to cancel the target — see [[concepts/informed-gsc|Informed GSC]] |
| **Misadjustment / leakage in a reverberant room** | GSC | Blocking is frequency dependent and never complete; leakage plus filter misadjustment gives the canceller a target-correlated reference |
| **Burst (non-stationary) targets** | Target-tracking beamformers | Speech onsets and silences defeat tracking loops, producing "breathing" noise and transient cancellation |

## GSC-Specific Formulation

In the [[concepts/gsc-beamformer|generalized sidelobe canceller]] the mechanism is explicit. The blocking matrix is supposed to produce reference signals $y_m(k)$ containing interference only; the multiple-input canceller then minimizes the output power

$$z(k) = d(k-Q) - \sum_m W_m^T(k)Y_m(k)$$

If any target energy appears in $y_m(k)$, minimizing output power is equivalent to cancelling the target. The classical Griffiths–Jim blocking matrix fails at the first sign of steering-vector error, which is why an entire robust-beamforming literature exists.

## Remedies

| Remedy | Mechanism | Cost |
|:-------|:----------|:-----|
| Leakage, noise injection, [[concepts/norm-constrained-adaptive-filter\|norm constraint]] in the canceller | Restrain coefficient growth so weak target components are not cancelled | Also restrains interference reduction when a large direction error must be tolerated |
| Improved spatial filters in the blocking matrix | Reject the target over a wider angular range | Consume degrees of freedom or require more microphones |
| [[concepts/coefficient-constrained-adaptive-filter\|Coefficient-constrained]] adaptive blocking matrix | Clamp each tap so target tracking is bounded and interference is deliberately *preserved* for the canceller | Constraint region must be designed per array and sector |
| Target tracking / calibration | Follow the target DOA explicitly | Mistracks burst signals such as speech; needs matrix products |
| [[concepts/diagonal-loading\|Diagonal loading]] / WNG constraint | Condition the SCM so the weight norm cannot blow up | Reduces directivity |
| RTF-based steering ([[concepts/relative-transfer-function\|RTF]]) | Model the true transfer function instead of a free-field steering vector | RTF estimation is hard at low SNR and in non-stationary scenes |
| Detector-gated statistics updates | Update the canceller only when the target is absent | Needs a reliable detector or [[concepts/directional-vad\|directional VAD]] |
| [[concepts/output-based-speech-enhancement\|Output-based]] selection | Search over candidate steering directions instead of committing to one | Extra computation; needs a selection criterion |

## Symptoms and Detection

- Frequency-selective attenuation of the target (high frequencies suffer most in practice), not a uniform gain error.
- Output power during target-active intervals *lower* than the fixed beamformer's — the diagnostic used by Hoshuyama et al. when comparing beamformers (Fig. 10 of the source paper).
- Subjective degradation disproportionate to the measured interference reduction; mean-opinion-score testing with an explicit instruction that cancellation should score low is the standard subjective instrument.

## Related Concepts

- [[concepts/beamforming|Beamforming]]
- [[concepts/gsc-beamformer|Generalized Sidelobe Canceller (GSC)]]
- [[concepts/steering-vector-error|Steering-Vector Error]]
- [[concepts/adaptive-blocking-matrix|Adaptive Blocking Matrix (ABM)]]
- [[concepts/coefficient-constrained-adaptive-filter|Coefficient-Constrained Adaptive Filter (CCAF)]]
- [[concepts/norm-constrained-adaptive-filter|Norm-Constrained Adaptive Filter (NCAF)]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/diagonal-loading|Diagonal Loading]]
- [[concepts/condition-number|Condition Number]]
- [[concepts/mpdr-beamformer|MPDR Beamformer]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/relative-transfer-function|Relative Transfer Function (RTF)]]
- [[concepts/output-based-speech-enhancement|Output-Based Speech Enhancement]]

## Related Sources

- [[sources/hoshuyama-1999-robust-adaptive-beamformer-ccaf|Hoshuyama, Sugiyama & Hirano 1999: A Robust Adaptive Beamformer with a Blocking Matrix Using Constrained Adaptive Filters]] — canonical taxonomy of steering-vector-error cancellation and its remedies; coefficient-constrained blocking matrix as the fix that costs no degrees of freedom
- [[sources/mittal-2026-adaptive-diagonal-loading-beamforming|Mittal et al. 2026: Adaptive Diagonal Loading for Norm Constrained Beamforming]] — snapshot-deficiency route to WNG collapse and cancellation
- [[sources/apostolidis-2026-listen-first-output-based-multi-microphone|Apostolidis et al. 2026: Listen-First Output-Based Multi-Microphone Speech Enhancement]] — output-based steering search as an alternative to committing to a single steering vector
- [[sources/taseska-2018-informed-spatial-filters|Taseska 2018: Informed Spatial Filters for Speech Enhancement]] — canceller updated only when the desired signal is absent
- [[sources/yan-2014-dual-mic-bt-noise-reduction|Yan, Qiu & Lu 2014: Dual-Mic Noise Suppression for Bluetooth Headsets]] — leakage under wearing-angle mismatch framed as speech-distortion trade-off
- [[sources/pan-2020-microphone-array-beamforming|Pan, Huang & Chen 2020: Microphone Array Beamforming Methods for Speech Communication and Interaction]] — survey of adaptive beamforming and its parameter-estimation bottleneck
