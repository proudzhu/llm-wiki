---
type: concept
created: 2026-09-30
updated: 2026-09-30
sources:
  - raw/papers/hoshuyama-1999-robust-adaptive-beamformer-ccaf/full-text.md
  - raw/papers/sun-2024-lightweight-hybrid-speech-extraction/full-text.txt
tags:
  - beamforming
  - adaptive-filtering
  - microphone-arrays
  - gsc
---

# Adaptive Blocking Matrix (ABM)

**Category**: Component of the generalized sidelobe canceller

## Definition

In a [[concepts/gsc-beamformer|generalized sidelobe canceller (GSC)]] the **blocking matrix (BM)** produces $M$ reference signals that should contain interference only — its job is to reject the target so that the downstream canceller has a target-free reference. A **fixed** blocking matrix (the classical Griffiths–Jim form, or an RTF-difference form such as $[1, -W_s]$) relies on the assumed [[concepts/steering-vector-error|steering vector]] being correct. An **adaptive blocking matrix (ABM)** replaces those fixed coefficients with adaptive filters that are updated from the data, so the null toward the target is re-formed as the true target direction drifts.

The ABM is the natural place to attack [[concepts/target-signal-cancellation|target-signal cancellation]], because that is where target energy first leaks into the reference path. Its difficulty is that the ABM must simultaneously (a) track the target across the expected direction-error range and (b) *not* adapt toward interference, which would starve the canceller of reference signal.

## Key Formulations

**CCAF-based ABM (Hoshuyama, Sugiyama & Hirano 1999).** Each branch is an adaptive noise canceller whose input is the fixed-beamformer output $d(k)$ (the common reference) and whose output is subtracted from a delayed microphone signal:

$$y_m(k) = x_m(k-P) - H_m^T(k)D(k)$$

The coefficients $H_m(k)$ are updated by NLMS with a **per-coefficient clamp** to a box region derived from the target-minimizing coefficient trajectories over a chosen DOA sector — see [[concepts/coefficient-constrained-adaptive-filter|CCAF]]. The constraint is what makes the tracking *bounded*: inside the sector the ABM follows the target; outside it, adaptating toward interference is impossible. The paper reports the maximum allowable target-direction error as a design parameter swept over roughly 4°–20°, and — counter-intuitively — a *larger* residual interference at the ABM outputs (because the constrained filter cannot minimize interference) is beneficial, since that residual becomes the canceller's reference.

**DNN-gated NLMS ABM (Sun et al. 2024).** The ABM is updated by NLMS but only during frames the target is active, gated by a [[concepts/directional-vad|directional VAD (DVAD)]] label; the complementary gate drives the adaptive interference canceller during target-silent frames, when the noise reference is free of target leakage. This is the learned, multi-speaker-safe generalization of the SIR-based adaptation control used by Hoshuyama et al.

**RTF-form ABM (informed GSC).** The RTF-based blocking-matrix form is estimated online per time-frequency bin, under the control of a narrowband signal detector — see [[concepts/informed-gsc|Informed GSC]]. A pre-modeled (non-adaptive) RTF blocking matrix is the alternative when the source–array geometry is quasi-fixed, as in Bluetooth headsets ([[concepts/atf-gsc|ATF-GSC]]).

## Adaptation Control

Because the target is the signal the ABM *wants* to cancel, the ABM must adapt under the opposite condition to the canceller: **high target-to-interference ratio** for the ABM (or, equivalently, target-active frames), and **low** SIR for the canceller. Hoshuyama et al. draw the explicit analogy to double-talk detection in [[concepts/acoustic-echo-cancellation|acoustic echo cancellation]]; Sun et al. replace the SIR estimate with a directional VAD, which is what makes the scheme robust to interfering speakers rather than just to one target.

## Practical Notes

- The ideal ABM would need more than 1000 taps per branch to reject the target in a reverberant room; with realistic 16-tap filters the blocking is always incomplete, so a norm-constrained or otherwise restrained canceller is a practical necessity rather than an optional refinement.
- Blocking capability is frequency dependent: highly correlated low-frequency components of a colored interference are easily absorbed by the ABM, after which the canceller cannot suppress them.

## Related Concepts

- [[concepts/gsc-beamformer|Generalized Sidelobe Canceller (GSC)]]
- [[concepts/coefficient-constrained-adaptive-filter|Coefficient-Constrained Adaptive Filter (CCAF)]]
- [[concepts/norm-constrained-adaptive-filter|Norm-Constrained Adaptive Filter (NCAF)]]
- [[concepts/directional-vad|Directional VAD (DVAD)]]
- [[concepts/target-signal-cancellation|Target-Signal Cancellation]]
- [[concepts/steering-vector-error|Steering-Vector Error]]
- [[concepts/atf-gsc|ATF-GSC]]
- [[concepts/informed-gsc|Informed GSC]]
- [[concepts/relative-transfer-function|Relative Transfer Function (RTF)]]

## Related Sources

- [[sources/hoshuyama-1999-robust-adaptive-beamformer-ccaf|Hoshuyama, Sugiyama & Hirano 1999: A Robust Adaptive Beamformer with a Blocking Matrix Using Constrained Adaptive Filters]] — introduces the CCAF-based adaptive blocking matrix
- [[sources/sun-2024-lightweight-hybrid-speech-extraction|Sun et al. 2024: A Lightweight Hybrid Multi-Channel Speech Extraction System with Directional VAD]] — DVAD-gated NLMS adaptation of the ABM/AIC pair
- [[sources/taseska-2018-informed-spatial-filters|Taseska 2018: Informed Spatial Filters for Speech Enhancement]] — detector-controlled RTF-based blocking matrix
- [[sources/yan-2014-dual-mic-bt-noise-reduction|Yan, Qiu & Lu 2014: Dual-Mic Noise Suppression for Bluetooth Headsets]] — pre-modeled RTF blocking matrix
