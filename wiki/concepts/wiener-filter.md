---
type: concept
created: 2026-04-12
updated: 2026-09-19
sources:
  - raw/papers/pan-2026-array-self-awareness/full-text.md
  Controllers.md
  - raw/papers/tashev-2008-sound-capture-spatial-filter/full-text.md
  - raw/papers/xiang-2025-wiener-gain-reverberant/full-text.md
  - raw/papers/kim-2014-doa-based-snr-estimation/full-text.txt
  - raw/papers/pan-2025-data-driven-acoustics/full-text.md
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

## Joint SNR–CDR Wiener Gain (Xiang et al. 2025)

Xiang, Chen, Benesty, Lei & Pan 2025 observe that classical Wiener gain formulations are driven by either the SNR alone (noise-only environments) or the CDR alone (reverberation-only environments), and unify the two degenerate gains into a single post-filter for environments where both interferers coexist (see [[concepts/snr-cdr-wiener-gain|SNR–CDR Wiener gain]]):

$$
G(n,k) = \frac{1}{1 + \beta_1\frac{\alpha_R(k)}{\mathrm{CDR}(n,k)} + \beta_2\frac{\alpha_V(k)}{\mathrm{SNR}(n,k)}}
$$

where $\alpha_R(k)$ and $\alpha_V(k)$ are the coherence-weighted leakage of reverberation and noise through the spatial filter, and the two hyperparameters $\beta_1, \beta_2$ separately govern reverberation suppression (DRR) and noise reduction (SNR gain) — decoupling the two suppression axes that single-ratio gains conflate. Setting $\beta_2 = 0$ recovers a CDR-style gain, $\beta_1 = 0$ an SNR-style gain. Applied after a robust superdirective beamformer, the joint gain achieves the best SNR gain (11.4 dB) and DRR (9.3 dB) and ties the best LSD against SNR-, CDR-, TSNR-, HRNR-based, and WPE-based baselines, and — unlike AWPE — degrades gracefully as input SNR drops. The gain floor $G \leftarrow \max\{G, G_{\min}\}$ controls musical noise; a kurtosis-ratio analysis identifies $G_{\min} = 0.1$ as a stable operating point.

## Self-Awareness Wiener Filter (Pan et al. 2026)

In multichannel source extraction with coherence-matrix-defined components, each source is extracted by the Wiener gain $H_n(t) = \phi_{X,n}(t)/\sum_i \phi_{X,i}(t)$ built from its estimated variance. [[sources/pan-2026-array-self-awareness|Pan, Chen & Benesty 2026]] derive the Wiener filter for an *unknown, newly emerging* source,

$$
H_{\xi}(t) = \frac{\phi_{\xi}(t)}{\phi_{\xi}(t) + \sum_{n=1}^{N+1}\phi_{X,n}(t)},
$$

where $\phi_{\xi}(t)$ follows from the [[concepts/covariance-matrix-residual-model|residual model]] of the covariance matrix, and gate it with an a priori term from the first estimation stage:

$$
H_{\mathrm{SA}}(t) = H_{\xi}(t)\left(1 - \max_{n} H_n(t)\right)
$$

The gate suppresses onset false alarms caused by direct-path and early-reflection leakage of known sources into the residual model; $H_{\mathrm{SA}}(t) \in [0,1]$ behaves as a per-time-frequency-bin detection probability for the new source while doubling as its extraction gain (see [[concepts/array-self-awareness|Array Self-Awareness]]).

## Data-Driven Wiener Gain Estimation (Pan 2025)

[[sources/pan-2025-data-driven-acoustics|Pan 2025]] treats the Wiener gain as the **supervised target of a neural network** within the STFT analysis–filter–reconstruction framework: since the optimal gain is a real number in $[0,1]$ per frequency band, the network output $\hat{\bm{h}}(t)$ (sigmoid layer) can be trained against it directly with **binary cross-entropy**,

$$
\mathcal{J}_{1} = -\sum_{t}\left\{\bm{h}^{T}(t)\ln\hat{\bm{h}}(t) + [1-\bm{h}^{T}(t)]\ln[1-\hat{\bm{h}}(t)]\right\},
$$

where the $k$-th element of $\hat{\bm{h}}(t)$ approximates the optimal Wiener gain of the $k$-th band. The tutorial's worked example (Han et al. 2015): $2Q{+}1$ concatenated log-magnitude frames (16 kHz, 20 ms window, 161 bands, $Q=5$ → 1771-dim input) → three FC layers with 1600 units and ReLU → 161-dim sigmoid — estimating the Wiener gain from multi-frame context at the cost of a $Q$-frame algorithmic delay.

## Related Concepts

- [[concepts/snr-cdr-wiener-gain|SNR–CDR Wiener Gain]] — joint formulation unifying the SNR and CDR degenerate gains
- [[concepts/array-self-awareness|Array Self-Awareness]] — the Wiener filter for an unknown new source, gated by an a priori term from the known sources' filters
- [[concepts/coherent-to-diffuse-power-ratio|Coherent-to-Diffuse Power Ratio]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[feedback-anc|Feedback ANC]]
- [[internal-model-control|Internal Model Control]]
- [[minimum-variance-control|Minimum Variance Control]]
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[kalman-filter|Kalman Filter]]

## Related Sources

- [[sources/pan-2026-array-self-awareness|Pan, Chen & Benesty 2026: Microphone Array Self-Awareness via a Residual Model of the Covariance Matrix]] — the self-awareness Wiener filter for unknown new sources, gated by $1 - \max_n H_n(t)$

- [[sources/welch-2006-kalman-filter-intro|Welch & Bishop 2006: Introduction to the Kalman Filter]]
- [[sources/pawelczyk-1997-anc-feedback-fixed-adaptive|Pawelczyk 1997: ANC Feedback Fixed/Adaptive]]
- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]]
- [[sources/tashev-2008-sound-capture-spatial-filter|Tashev et al. 2008: Sound Capture System and Spatial Filter for Small Devices]] — uses the Wiener gain as an offline supervised target for tuning a probability-based spatial filter's parameters
- [[sources/kim-2014-doa-based-snr-estimation|Kim & Kim 2014: DOA-Based SNR Estimation for Dual-Microphone Speech Enhancement]] — Wiener spectral gain driven by a spatial-cue (DOA-based) SNR estimate instead of a noise-variance-based one
- [[sources/xiang-2025-wiener-gain-reverberant|Xiang, Chen, Benesty, Lei & Pan 2025: Design of the Wiener Gain in Noisy and Reverberant Environments]] — joint SNR–CDR Wiener gain with two trade-off hyperparameters
- [[sources/pan-2025-data-driven-acoustics|Pan 2025: Fundamentals of Data-Driven Approaches to Acoustic Signal Detection, Filtering, and Transformation]] — the Wiener gain as a BCE-trained supervised target of a neural network (Section 7.2.1)
