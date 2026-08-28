---
type: concept
created: 2026-04-12
updated: 2026-08-28
sources:
  Controllers.md
  - raw/papers/tashev-2008-sound-capture-spatial-filter/full-text.md
  - raw/papers/kim-2014-doa-based-snr-estimation/full-text.txt
tags:
- mathematics
- signal-processing
---

# Wiener Filter

The **Wiener Filter** is an optimal linear filter used to produce an estimate of a desired random process by linear time-invariant (LTI) filtering of an observed noisy process.

## Overview

The Wiener filter minimizes the **Mean Square Error (MSE)** between the filter output and the desired signal. It assumes that the signal and noise are stationary random processes with known spectral characteristics or auto-correlation and cross-correlation functions.

## Optimal Solution

For a discrete-time FIR filter of length $N$, the optimal weights $w_{opt}$ are given by the **Wiener-Hopf Equation**:
$$ w_{opt} = R^{-1} P $$
Where:
- **$R$**: Auto-correlation matrix of the input signal.
- **$P$**: Cross-correlation vector between the input and the desired signal.

## Role in ANC

In **[[active-noise-control|Active Noise Control]]**, the Wiener filter represents the theoretical optimal controller for a given acoustic path.
- **Feedforward ANC**: The optimal $W(z) = P(z)/S(z)$, which is a Wiener filter that models the primary path while compensating for the secondary path.
- **Feedback ANC**: The optimal controller for minimizing the variance of the error signal can be derived as a Wiener filter using the **Internal Model Control (IMC)** structure (Pawelczyk 1997).

## Limitations

- **Stationarity**: The standard Wiener filter assumes the signals are stationary. In real-world ANC, signals are often non-stationary, necessitating **Adaptive Filters** (like LMS or RLS) that iteratively converge toward the Wiener solution.
- **Causality**: The optimal Wiener solution may be non-causal (requiring future information). In practical systems, a causal approximation must be used, which may have lower performance.

## Wiener Gain as Offline Optimization Reference

Tashev et al. (2008) use the Wiener gain as an **offline optimization target** for a non-Wiener estimator. Their [[concepts/probability-based-spatial-filter|probability-based spatial filter]] computes, per frame and per frequency bin, a posterior probability $P_k^{(n)}$ that the signal comes from the desired direction, and applies $P_k^{(n)}$ directly as the suppression gain. Because $P_k^{(n)}$ is an MMSE estimator under the assumed source-distribution model, it can be compared against an **oracle Wiener gain**

$$
H_w^{(n)}(k) = \frac{|X_k^{(n)}|^2}{|X_k^{(n)}|^2 + |N_k^{(n)}|^2}
$$

computed from separately recorded clean speech $X$ and noise $N$ (the mixture is the sum, so the per-bin clean and noise components are known). The eight non-estimable parameters of the post-filter (four adaptation time constants and four feature gains) are tuned offline by steepest-gradient descent minimizing $\sum_{n,k}(H_w - P)^2$, with an 80/20 train/test split and early stopping. The Wiener gain is *not* used at runtime — only as a supervised learning target for parameter optimization.

## Wiener Gain Driven by DOA-Based SNR (Kim & Kim 2014)

In dual-microphone speech enhancement, Kim & Kim (2014) drive the Wiener spectral gain $G = \hat{\xi}/(1+\hat{\xi})$ with an a priori SNR estimated from **spatial cues** rather than from a noise-variance estimate: the phase difference between the time-aligned channels is first converted into a [[concepts/target-to-non-target-directional-signal-ratio|TNR]] estimate ($\cot^2(\Delta\tilde\psi/2)$), which a statistical model-based LRT speech-activity decision and two decision-directed updates then turn into the final SNR (see [[concepts/doa-based-snr-estimation|DOA-based SNR estimation]]). This decouples the Wiener gain from unreliable noise-variance tracking in adverse noise, and the resulting system outperforms single-channel Wiener filtering and dual-channel beamformer/post-filter baselines in SDR and PESQ at 0–20 dB SNR. A Wiener-filtering step is also used *inside* the estimator to obtain the speech-side power for the DOA-based SNR.

## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[feedback-anc|Feedback ANC]]
- [[internal-model-control|Internal Model Control]]
- [[minimum-variance-control|Minimum Variance Control]]
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[kalman-filter|Kalman Filter]]

## Related Sources

- [[sources/welch-2006-kalman-filter-intro|Welch & Bishop 2006: Introduction to the Kalman Filter]]
- [[sources/pawelczyk-1997-anc-feedback-fixed-adaptive|Pawelczyk 1997: ANC Feedback Fixed/Adaptive]]
- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]]
- [[sources/tashev-2008-sound-capture-spatial-filter|Tashev et al. 2008: Sound Capture System and Spatial Filter for Small Devices]] — uses the Wiener gain as an offline supervised target for tuning a probability-based spatial filter's parameters
- [[sources/kim-2014-doa-based-snr-estimation|Kim & Kim 2014: DOA-Based SNR Estimation for Dual-Microphone Speech Enhancement]] — Wiener spectral gain driven by a spatial-cue (DOA-based) SNR estimate instead of a noise-variance-based one
