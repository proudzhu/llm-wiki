---
type: source
created: 2026-05-26
updated: 2026-05-26
sources:
  - raw/papers/martin-2001-noise-psd-estimation-optimal-smoothing/full-text.md
  - https://doi.org/10.1109/89.928915
  - zotero://select/items/0_SUKHAUHG
tags:
  - noise-estimation
  - minimum-statistics
  - speech-enhancement
  - optimal-smoothing
  - power-spectral-density
---

# Martin 2001: Noise Power Spectral Density Estimation Based on Optimal Smoothing and Minimum Statistics

| Field | Details |
|-------|---------|
| **Authors** | [[entities/rainer-martin|Rainer Martin]] |
| **Institution** | Institute of Communication Systems and Data Processing, Aachen University of Technology (RWTH Aachen) |
| **Venue** | IEEE Transactions on Speech and Audio Processing, Vol. 9, No. 5, pp. 504–512 |
| **Year** | 2001 |
| **Type** | Journal article |
| **DOI** | [10.1109/89.928915](https://doi.org/10.1109/89.928915) |
| **Zotero** | [Link](zotero://select/items/0_SUKHAUHG) |

## Summary

This paper presents a method to estimate the noise power spectral density (PSD) from noisy speech signals without requiring a voice activity detector (VAD). The approach tracks spectral minima in each frequency band and derives an optimal time-varying smoothing parameter by minimizing a conditional mean square error criterion. Based on the optimally smoothed PSD and an analysis of the statistics of spectral minima, an unbiased noise estimator with bias compensation is developed. A local minimum search extension is introduced to improve tracking of nonstationary noise. The method is evaluated in the context of speech enhancement and low bit rate speech coding, demonstrating improved intelligibility and quality over VAD-based approaches.

## Problem Formulation

A noisy speech signal is modeled as $y(i) = s(i) + n(i)$, where $s(i)$ and $n(i)$ are statistically independent zero-mean signals. The signal is transformed into the frequency domain via a sliding-window FFT of size $L = 256$ with $R = 128$ sample shift, producing frequency-domain coefficients $Y(\lambda, k)$ at frame index $\lambda$ and frequency bin $k$.

The periodogram $|Y(\lambda, k)|^2$ is exponentially distributed with mean $\sigma_N^2(\lambda,k) + \sigma_S^2(\lambda,k)$. During speech pause ($\sigma_S^2 \equiv 0$), the mean equals the noise PSD $\sigma_N^2(\lambda,k)$.

The core problem is to estimate $\sigma_N^2(\lambda,k)$ from $Y(\lambda,k)$ without a VAD, by tracking the minimum of a recursively smoothed periodogram within a finite window of length $D$.

### Key Equations

**Recursive smoothing of the periodogram:**

$$P(\lambda,k) = \alpha(\lambda,k) P(\lambda-1,k) + (1-\alpha(\lambda,k)) |Y(\lambda,k)|^2 \tag{4}$$

**Optimal smoothing parameter (derived from MSE minimization):**

$$\alpha_{\text{opt}}(\lambda,k) = \frac{1}{1 + (P(\lambda-1,k)/\sigma_N^2(\lambda,k) - 1)^2} \tag{7}$$

**Unbiased noise estimator via minimum statistics:**

$$\hat{\sigma}_N^2(\lambda,k) = B_{\min}(D, Q_{\text{eq}}(\lambda,k)) \cdot P_{\min}(\lambda,k) \tag{19}$$

## Methodology

### Optimal Time-Varying Smoothing

The smoothing parameter $\alpha(\lambda,k)$ is optimized each frame by minimizing the conditional mean square error $E\{(P(\lambda,k) - \sigma_N^2(\lambda,k))^2 \mid P(\lambda-1,k)\}$ under the assumption of speech pause. The resulting optimal parameter depends on the smoothed a posteriori SNR $\bar{\gamma}(\lambda,k) = P(\lambda-1,k)/\sigma_N^2(\lambda,k)$:

- When $\bar{\gamma} \approx 1$ (noise only), $\alpha_{\text{opt}} \approx 1$ — heavy smoothing
- When $\bar{\gamma} \gg 1$ (speech present), $\alpha_{\text{opt}} \approx 0$ — fast tracking

![[raw/papers/martin-2001-noise-psd-estimation-optimal-smoothing/figures/ffb897b7f0485d11672c561ac4906074d4b7f3d45c75f297a00c57497a17534a.jpg|Optimal smoothing parameter as a function of the smoothed a posteriori SNR]]

*Figure 1: The optimal smoothing parameter $\alpha_{\text{opt}}$ as a function of the smoothed a posteriori SNR $\bar{\gamma}(\lambda,k)$. When $\bar{\gamma}=1$, $\alpha_{\text{opt}}=1$ (maximum smoothing); when $\bar{\gamma}$ deviates from 1, $\alpha$ decreases for faster tracking.*

An **error monitoring** mechanism compares the frequency-averaged smoothed PSD to the average periodogram to detect tracking errors:

$$\tilde{\alpha}_c(\lambda) = \frac{1}{1 + \big(\sum_k P(\lambda-1,k)/\sum_k |Y(\lambda,k)|^2 - 1\big)^2}$$

The correction factor $\alpha_c(\lambda)$ is smoothed over time and multiplied with the optimal smoothing parameter.

### Statistics of Minimum Power Estimates

The minimum of correlated short-term PSD estimates $P_{\min}(\lambda,k)$ is always smaller than the mean noise PSD. The bias depends on:
- The search window length $D$
- The equivalent degrees of freedom $Q_{\text{eq}}(\lambda,k)$ (inverse normalized variance)

The bias correction factor is approximated by:

$$B_{\min}(\lambda,k) \approx 1 + (D-1) \frac{2}{\tilde{Q}_{\text{eq}}(\lambda,k)}$$

where $\tilde{Q}_{\text{eq}}$ is a scaled version of $Q_{\text{eq}}$.

The variance of the smoothed PSD is tracked via recursive first and second moment estimation with $\beta(\lambda,k) = \alpha^2(\lambda,k)$.

### Efficient Minimum Search

The search window of length $D = U \cdot V$ is divided into $U$ subwindows of $V$ samples. A tree search strategy enables:
- Update of the minimum every $V$ frames
- Computational cost of $1 + (U-1)/V$ comparisons per frame per bin
- Worst-case delay of $D + V$ frames when responding to rising noise

**Local minimum tracking for nonstationary noise:** Subwindow minima within an adaptive range (0.8–9 dB, depending on variance) of the overall minimum are accepted, enabling faster tracking of increasing noise floors.

## Experimental Setup

| Parameter | Setting |
|-----------|---------|
| Sampling rate | 8 kHz |
| FFT size $L$ | 256 |
| Frame shift $R$ | 128 (50% overlap) |
| Smoothing window | $T_{\text{SM}} = 0.2$ s equivalent |
| Minimum search window | $D = 96$ frames ($U=8$, $V=12$) |
| Noise types | White Gaussian, vehicular, street noise |
| Speech material | 6 male + 6 female speakers |
| Test conditions | Speech pause only; SNR = 15 dB (continuous speech) |
| Evaluation metrics | Relative estimation error (%), error variance; DAM quality test; DRT intelligibility test |

## Results

### Estimation Error During Speech Pause

| Algorithm | White noise | Vehicular noise | Street noise |
|-----------|-------------|-----------------|--------------|
| [7] with $\alpha = 0.6$ | 0.059% (0.11) | 0.062% (0.13) | –0.15% (0.21) |
| New (with eq. 15) | –0.007% (0.041) | –0.018% (0.041) | –0.28% (0.13) |
| New (with eq. 17) | –0.006% (0.041) | –0.016% (0.041) | –0.27% (0.13) |

### Estimation Error During Speech Activity (SNR = 15 dB, No Pauses)

| Algorithm | White noise | Vehicular noise | Street noise |
|-----------|-------------|-----------------|--------------|
| [7] with $\alpha = 0.6$ | 0.64% (0.77) | 0.77% (1.04) | 0.59% (1.9) |
| New (with eq. 15) | –0.07% (0.14) | 0.04% (0.17) | –0.22% (0.27) |
| New (with eq. 17) | –0.04% (0.14) | 0.02% (0.17) | –0.20% (0.28) |

*Values show mean relative estimation error with variance in parentheses.*

### Listening Test Results

- **DAM quality test** (vehicular noise, ~10 dB SNR): The minimum statistics approach scored ~1.4 DAM points higher than the VAD/soft-decision baseline (s.e. ≈ 0.9)
- **DRT intelligibility test**: Slightly improved for vehicular noise; significantly improved for highly nonstationary helicopter noise
- The method preserved weak voiced sounds (especially consonants like /m/ and /n/) much better than the alternative
- Dramatic improvements when input was music signal
- In highly nonstationary noise, the alternative algorithm produced smoother residual noise

## Key Contributions

1. **VAD-free noise estimation** — The first widely-adopted noise PSD estimation method that operates without a voice activity detector, instead tracking spectral minima in each frequency band independently
2. **Optimal time-varying smoothing parameter** — Derivation of $\alpha_{\text{opt}}(\lambda,k)$ by minimizing a frame-wise conditional MSE criterion, enabling the smoothed PSD to balance tracking speed and variance
3. **Bias compensation for minimum statistics** — Systematic analysis of the bias of correlated minimum PSD estimates and development of practical closed-form approximations ($B_{\min}$ factor) suitable for real-time implementation
4. **Variance tracking per frequency band** — Recursive estimation of PSD variance via first/second moment smoothing, enabling frequency-dependent bias compensation
5. **Local minimum search for nonstationary noise** — Subwindow-based tree search with adaptive acceptance threshold that speeds up tracking of rising noise floors without compromising noise-only estimates
6. **Comprehensive experimental validation** — Quantitative error analysis and formal listening tests (DAM, DRT) demonstrating improved quality and intelligibility

## Related Concepts

- [[concepts/minimum-statistics|Minimum Statistics]]
- [[concepts/voice-activity-detection|Voice Activity Detection (VAD)]]
- [[concepts/spectrogram-analysis|Spectrogram Analysis]]
- [[concepts/wiener-filter|Wiener Filter]]
- [[concepts/kalman-filter|Kalman Filter]]
- [[concepts/signal-processing|Signal Processing]]

## Related Synthesis

- [[synthesis/ai-driven-anc|AI-Driven ANC]] — noise estimation is a component of speech enhancement in ANC systems
