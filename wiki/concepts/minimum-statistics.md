---
type: concept
created: 2026-05-26
updated: 2026-05-26
tags:
  - noise-estimation
  - speech-enhancement
  - power-spectral-density
  - signal-processing
---

# Minimum Statistics

**Minimum Statistics** is a noise power spectral density (PSD) estimation method that tracks the spectral minima of a noisy signal across frequency bands, without requiring a voice activity detector (VAD). The method exploits the observation that speech energy frequently decays to the noise floor between words and syllables, making the minimum of a smoothed periodogram a useful estimate of the underlying noise PSD.

## Algorithm Overview

The minimum statistics approach comprises four key components:

### 1. Time-Varying Optimal Smoothing

The noisy periodogram $|Y(\lambda, k)|^2$ is recursively smoothed:

$$P(\lambda, k) = \alpha(\lambda, k) P(\lambda-1, k) + (1-\alpha(\lambda, k)) |Y(\lambda, k)|^2$$

where the smoothing parameter $\alpha(\lambda, k)$ is optimized each frame by minimizing the conditional mean square error between the smoothed estimate and the true noise PSD:

$$\alpha_{\text{opt}}(\lambda, k) = \frac{1}{1 + (P(\lambda-1,k)/\sigma_N^2(\lambda,k) - 1)^2}$$

This yields $\alpha \approx 1$ during speech pauses (heavy smoothing) and $\alpha \approx 0$ during speech activity (fast tracking).

An error monitoring mechanism compares the smoothed PSD against the average periodogram to detect tracking errors.

### 2. Bias Compensation

The minimum of a set of random variables is always smaller than their mean, so a bias correction factor $B_{\min}$ is applied:

$$\hat{\sigma}_N^2(\lambda, k) = B_{\min}(D, Q_{\text{eq}}(\lambda, k)) \cdot P_{\min}(\lambda, k)$$

where:
- $D$ is the length of the minimum search window
- $Q_{\text{eq}}(\lambda, k)$ is the equivalent degrees of freedom of the smoothed PSD
- $P_{\min}(\lambda, k)$ is the minimum PSD within the search window

The bias correction is approximated by:

$$B_{\min}(\lambda, k) \approx 1 + (D-1) \frac{2}{\tilde{Q}_{\text{eq}}(\lambda, k)}$$

### 3. Variance Tracking

The variance of the smoothed PSD is estimated via recursive first and second moment estimation:

$$\bar{P}(\lambda, k) = \beta \bar{P}(\lambda-1, k) + (1-\beta) P(\lambda, k)$$
$$\overline{P^2}(\lambda, k) = \beta \overline{P^2}(\lambda-1, k) + (1-\beta) P^2(\lambda, k)$$
$$\widehat{\text{var}}\{P(\lambda, k)\} = \overline{P^2}(\lambda, k) - \bar{P}^2(\lambda, k)$$

with $\beta(\lambda, k) = \alpha^2(\lambda, k)$ limited to ≤ 0.8.

### 4. Subwindow Minimum Search

To improve tracking of nonstationary noise, the search window of length $D = U \cdot V$ is divided into $U$ subwindows of $V$ samples each. Local minima within subwindows that fall within an adaptive range (0.8–9 dB) of the global minimum are accepted, enabling faster tracking of rising noise floors.

## Key Formulations

**Spectral analysis model:** The noisy signal $y(i) = s(i) + n(i)$ is transformed via sliding-window FFT. Periodogram bins $|Y(\lambda, k)|^2$ are exponentially distributed with mean $\sigma_N^2(\lambda, k) + \sigma_S^2(\lambda, k)$.

**Optimal smoothing parameter derivation:** Minimizing $E\{(P(\lambda,k) - \sigma_N^2(\lambda,k))^2 \mid P(\lambda-1,k)\}$ yields:

$$\alpha_{\text{opt}}(\lambda, k) = \frac{1}{1 + (\bar{\gamma}(\lambda,k) - 1)^2}$$

where $\bar{\gamma}(\lambda,k) = P(\lambda-1,k)/\sigma_N^2(\lambda,k)$ is the smoothed a posteriori SNR.

**Unbiased noise estimator:**
$$\hat{\sigma}_N^2(\lambda, k) = B_{\min}(D, Q_{\text{eq}}(\lambda, k)) \cdot P_{\min}(\lambda, k)$$

## Advantages

- **No VAD required** — avoids the tuning difficulties and clipping issues of threshold-based voice activity detectors
- **Updates during speech activity** — can track changing noise conditions even when speech is present
- **Real-time capable** — uses simple recursive operations and precomputed lookup tables
- **Frequency-selective** — operates independently in each frequency band

## Limitations

- **Tracking delay** — responds to increasing noise power with a delay proportional to the search window length
- **Variance penalty** — the minimum estimator has 2–4× the variance of a moving average estimator with an ideal VAD
- **Bias in nonstationary noise** — tends to underestimate highly nonstationary noise floors
- **Computational cost** — higher than simple VAD-based approaches due to per-bin variance tracking

## Related Concepts

- [[concepts/voice-activity-detection|Voice Activity Detection (VAD)]]
- [[concepts/spectrogram-analysis|Spectrogram Analysis]]
- [[concepts/wiener-filter|Wiener Filter]]
- [[concepts/kalman-filter|Kalman Filter]]

## Related Sources

- [[sources/martin-2001-noise-psd-estimation-optimal-smoothing|Noise Power Spectral Density Estimation Based on Optimal Smoothing and Minimum Statistics (Martin 2001)]]
