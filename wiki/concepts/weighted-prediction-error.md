---
type: concept
created: 2026-09-26
updated: 2026-09-26
sources:
  - raw/papers/haeb-umbach-2024-microphone-array-deep-learning/full-text.md
tags:
  - dereverberation
  - speech-enhancement
  - linear-prediction
  - multichannel
---

# Weighted Prediction Error (WPE)

**Weighted Prediction Error (WPE)** is a model-based blind dereverberation method (Yoshioka, Nakatani, Miyoshi & Okuno 2011) that models late reverberation as a multichannel auto-regressive (linear prediction) process over past observation frames, and subtracts its prediction from the current observation. It is the dominant blind multichannel-linear-prediction dereverberation approach and was adopted as a CHiME-6/7 challenge baseline component ([[sources/haeb-umbach-2024-microphone-array-deep-learning|Haeb-Umbach et al. 2024]]; see also the historical account in [[sources/richard-2023-audio-signal-processing-21st-century|Richard et al. 2023]]).

## Formulation

In the STFT domain, the reverberant observation splits into an early component (direct path + early reflections, the desired signal) and late reverberation, the latter approximated by an AR model over past frames:

$$
\mathbf{y}_{t,f} = \mathbf{x}_{t,f}^{(\mathrm{early})} + \sum_{\tau=\Delta}^{L-1} \mathbf{G}_{\tau,f}\,\mathbf{y}_{t-\tau,f}
$$

with prediction matrices $\mathbf{G}_{\tau,f} \in \mathbb{C}^{D\times D}$. The dereverberated signal is estimated by subtracting the predicted late reverberation:

$$
\hat{\mathbf{x}}_{t,f}^{(\mathrm{early})} = \mathbf{y}_{t,f} - \sum_{\tau=\Delta}^{L'-1} \hat{\mathbf{G}}_{\tau,f}\,\mathbf{y}_{t-\tau,f}
$$

The **prediction lag** $\Delta$ is the defining design choice: speech is itself an AR process, and $\Delta$ keeps the predictor from modeling (and whitening) speech's own correlations — only lags beyond $\Delta$ are attributed to reverberation.

WPE is derived as maximum-likelihood estimation under the assumption that $\mathbf{x}_{t,f}^{(\mathrm{early})}$ is zero-mean complex Gaussian with a **time-varying, channel-independent variance** $\lambda_{t,f}$ (a nonstationary Gaussian source model). An iterative algorithm alternates estimates of $\mathbf{G}$ and $\lambda_{t,f}$.

## Properties and Hybrid Extensions

- Model-based: parameters estimated from the signal being enhanced, no training stage, adapts within seconds — but iterative/batch by default (online variants exist).
- **Neural PSD estimation** (Class 2 hybrid): the iterative estimation of $\lambda_{t,f}$ can be replaced by a neural network, avoiding the alternating loop (Kinoshita et al. 2017) — one of the canonical examples of joint model-based + data-driven parameter estimation in Haeb-Umbach et al. 2024.
- Related multichannel-linear-prediction dereverberation via a state-space/Kalman EM view (Schwartz, Gannot & Habets 2014) treats the same CTF model with a Kalman filter E-step.
- The wiki's [[concepts/mclp|MCLP]] page covers the multi-channel linear prediction family; WPE is its best-known instance.

## Related Concepts

- [[concepts/dereverberation|Dereverberation]]
- [[concepts/mclp|MCLP (Multi-Channel Linear Prediction)]]
- [[concepts/kalman-filter|Kalman Filter]]
- [[concepts/hybrid-speech-enhancement|Hybrid Speech Enhancement]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Related Sources

- [[sources/haeb-umbach-2024-microphone-array-deep-learning|Haeb-Umbach et al. 2024: Microphone Array Signal Processing and Deep Learning for Speech Enhancement]] — formulation (Eqs. 18–20), CHiME baseline evidence, neural-PSD hybrid extension
- [[sources/richard-2023-audio-signal-processing-21st-century|Richard et al. 2023: Audio Signal Processing in the 21st Century]] — positions WPE as the dominant blind MCLP approach
- [[sources/xiang-2025-wiener-gain-reverberant|Xiang et al. 2025: Design of the Wiener Gain in Noisy and Reverberant Environments]] — AWPE (the WPE-style baseline) outperformed in jointly noisy and reverberant conditions
