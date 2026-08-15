---
type: source
created: 2026-08-15
updated: 2026-08-15
sources:
  - raw/papers/tashev-2008-sound-capture-spatial-filter/full-text.md
  - https://www.microsoft.com/en-us/research/publication/sound-capture-system-and-spatial-filter-for-small-devices/
  - zotero://select/items/0_79EJS2D7
tags:
  - speech-enhancement
  - multi-channel-speech-enhancement
  - beamforming
  - spatial-filter
  - microphone-array
  - back-to-back-microphone-array
  - probability-based-spatial-filter
  - statistical-model
  - vad
  - small-device
  - mobile-phone
  - mmse
  - wiener-filter
  - gcc-phat
  - pesq
---

# Tashev, Mihov, Gleghorn & Acero 2008: Sound Capture System and Spatial Filter for Small Devices

| Field | Value |
|-------|-------|
| **Authors** | [[entities/ivan-tashev\|Ivan Tashev]], [[entities/slavy-mihov\|Slavy Mihov]], [[entities/tyler-gleghorn\|Tyler Gleghorn]], [[entities/alex-acero\|Alex Acero]] |
| **Institution** | Microsoft Research (Redmond, WA, USA); Technical University of Sofia (Bulgaria); Microsoft Corporation (Redmond, WA, USA) |
| **Published** | 2008 (conference paper) |
| **Type** | Conference Paper |
| **URL** | [microsoft.com/en-us/research/publication](https://www.microsoft.com/en-us/research/publication/sound-capture-system-and-spatial-filter-for-small-devices/) |
| **Zotero** | [79EJS2D7](zotero://select/items/0_79EJS2D7) |

## Summary

This paper proposes a two-microphone **sound capture system for small mobile devices** (cell phones, PDAs, ultra-mobile PCs) that must capture speech from ~1 m (arm's length) in noisy environments. The hardware geometry pairs two **unidirectional microphones placed back-to-back** (9.6 mm apart, pointing in opposite directions) inside a cell-phone mock-up. The processing chain combines (i) a pair of **front/rear beamformers optimized for maximum front-back difference** (rather than for maximum SNR) and (ii) a **non-linear [[concepts/probability-based-spatial-filter\|probability-based spatial filter]]** that fuses four statistical features (per-frame level difference, per-bin level difference, per-frame delay, per-bin delay) into a posterior probability that the signal comes from the desired direction, applied as a real-time suppression gain. On a 16 kHz / 512-sample frame pipeline, the system achieves **10.43 dB SNR improvement** and **0.39 MOS improvement (PESQ)**, with the beamformer and spatial filter each contributing roughly half of the gain.

## Problem Formulation

Mobile phones and small handheld devices need to capture speech from ~1 m (arm's length, e.g. when the user is reading the screen) and up to 3 m (video capture) in increasingly adverse noise. The default single omnidirectional microphone picks up too much ambient noise and reverberation. Three baseline options all fall short:

- **One unidirectional microphone**: improves SNR by ~4.3 dB but worsens audio quality during video recording (camera is on the opposite side of the phone).
- **Two microphones + classical beamforming**: limited by the small inter-microphone distance forced by the device (30–50 mm) and by the need to keep the microphones far from the loudspeaker — classic beamforming has low efficiency at such small bases.
- **Linear processing alone** is insufficient once the input SNR drops below 5–10 dB; the stationary noise suppressor [1] becomes ineffective.

The proposed design addresses these by exploiting the *directional* nature of the microphones (instead of trying to form a sharp beam from omnidirectional mics) and by using a **non-linear post-filter** that estimates, per frame and per frequency bin, the probability that the captured signal originates from the desired direction.

![[raw/papers/tashev-2008-sound-capture-spatial-filter/figures/951a0b8c23bfa402f41061f812bc9602631ff6ae0b78177e49042c5734fe6c74.jpg|Figure 1 — Block diagram of the processing algorithm.]]
*Figure 1: Block diagram of the processing algorithm. Two unidirectional microphones (front/back, back-to-back) feed two beamformers optimized for maximum front-back difference; the beam outputs feed a feature extractor supervised by a binary VAD; statistical models (front/rear/noise) yield a per-bin posterior probability used as the suppression gain.*

## Methodology

### Microphone Array Geometry: Back-to-Back Unidirectional Capsules

The hardware contribution is the use of two **unidirectional** (subcardioid-measured) microphones placed **back-to-back**, 9.6 mm apart, in a cell-phone mock-up. Unlike [[concepts/differential-microphone-array\|differential microphone arrays]] (which use closely-spaced omnidirectional capsules and exploit differential pressure), this geometry uses the directional response of each capsule as the primary cue and treats the front/back beamformer outputs as the signal on which statistics are computed. The small 9.6 mm baseline is what forces the design away from classical time-delay beamforming toward a level-difference-dominated post-filter (see Results).

### Beamformer Design (Front-Back Difference Maximization)

For each frequency bin $f$ and incident angle $\theta$, the front/rear microphone directivity patterns $U_F(f,\theta)$ and $U_R(f,\theta)$ are measured in an anechoic chamber (36 rotations of $10^\circ$ each). The beamformer computes two output beams:

$$
\begin{aligned}
\mathbf{Y}_F^{(n)} &= \mathbf{W}_{FF}\,\mathbf{X}_F^{(n)} + \mathbf{W}_{FR}\,\mathbf{X}_R^{(n)} \\
\mathbf{Y}_R^{(n)} &= \mathbf{W}_{RF}\,\mathbf{X}_F^{(n)} + \mathbf{W}_{RR}\,\mathbf{X}_R^{(n)}
\end{aligned}
$$

The weights are obtained by **maximizing the ratio of the integrated beam energy in the desired $\pm\Delta\theta$ cone to the energy in the opposite $\pm\Delta\theta$ cone**, subject to unity-gain and zero-phase-shift constraints in the desired direction (enforced via punishing functions). With $\Delta\theta = 30^\circ$, the front beam is optimized for signals in $[-30^\circ, +30^\circ]$ and the rear beam for $[150^\circ, -150^\circ]$. The reference source distance is $\rho = 1$ m (typical working distance); each microphone signal is modeled as distance-attenuated, phase-shifted, and shaped by the measured directivity:

$$
X_F(f,\theta) \approx \frac{1}{\|\rho - d_F\|}\,\exp\!\left(-j2\pi f \frac{\|\rho - d_F\|}{c}\right)\,U_F(f,\theta)
$$

![[raw/papers/tashev-2008-sound-capture-spatial-filter/figures/9a1f6b189159bf6e4d349dba473b6ae97ae274a69feb3c29730a5493d0189c72.jpg|Figure 2 — Directivity pattern of the front microphone (measured subcardioid).]]
*Figure 2: Directivity pattern of the front microphone — a measured subcardioid pattern, before beamforming.*

![[raw/papers/tashev-2008-sound-capture-spatial-filter/figures/a64fb8513387a7634f7aff9a5355785771968febde61df37c07eea5bf0c541d9.jpg|Figure 3 — Directivity pattern of the front beam.]]
*Figure 3: Directivity pattern of the front beam — substantially more directional than the raw microphone pattern in Figure 2, confirming the beamformer's front-back separation objective.*

### Voice Activity Detector

A simple **energy-based binary [[concepts/voice-activity-detection\|VAD]]** is applied to the front beam output. It uses minimum-energy tracking implemented as a state machine with thresholds for switching between "noise" and "voice" states. The VAD gates the noise-model updates so that the noise statistics are only adapted during non-voiced frames (the asymmetric PDF parameters for the front/rear speech models are estimated during voiced frames).

### Features and Statistical Models

Four features are extracted from the front/rear beam pair, each associated with its own statistical model updated in real time:

**1. Level difference per frame** — the difference $\Delta L^{(n)}$ in RMS levels between the front and rear beams. During noise-only frames, a Gaussian model of the fluctuation is tracked with mean $L_C$ and variance $\sigma_W$ (recursive, time constant $\tau_W$). During voiced frames the level difference is modeled with an **asymmetric PDF**: exponential for positive differences (front source), Gaussian for negative differences (rear source):

$$
p_{FW}(\Delta L_W \mid \theta_{FW},\sigma_W) =
\begin{cases}
\dfrac{1}{\theta_{FW}}\exp\!\left(-\dfrac{\Delta L_W}{\theta_{FW}}\right) & \Delta L_W > 0 \\[6pt]
\dfrac{1}{\theta_{FW}}\exp\!\left(-\dfrac{\Delta L_W^2}{2\sigma_W^2}\right) & \text{otherwise}
\end{cases}
$$

**2. Level difference per frequency bin** — same statistical model as above, estimated per bin $k$ with adaptation time constant $\tau_{Wb}$.

**3. Time delay per frame** — estimated with the **PHAT-weighted Generalized Cross-Correlation (GCC-PHAT)** method [6]:

$$
\mathbf{C}_{FR}(\tau) = \mathrm{iFFT}\!\left[\frac{\mathbf{X}_F \cdot \mathbf{X}_R^{*}}{|\mathbf{X}_F|\,|\mathbf{X}_R|}\right]
$$

with quadratic interpolation for sub-sample resolution. Three Gaussian models (noise / front-voiced / rear-voiced) are tracked with means fixed from the microphone geometry and only the variance adapted (time constant $\tau_D$).

**4. Time delay per frequency bin** — estimated from the phase difference of the two microphone spectra:

$$
D_b(k) = \frac{\mathrm{norm}\!\left[\arg(X_F(k)) - \arg(X_R(k))\right]}{2\pi f}
$$

normalized to $[-\pi, +\pi]$, with adaptation time constant $\tau_{Db}$.

### Posterior Probability and Feature Fusion

For each feature $i$, the posterior probability that the current frame/bin is dominated by a signal from the desired (front) direction is computed via Bayesian competition across the front, rear, and noise PDFs. For the per-frame level feature:

$$
\hat{P}_{FW}^{(n)} = \frac{p_{FW}(\Delta L_W^{(n)})}
{p_{FW}(\Delta L_W^{(n)}) + p_{RW}(\Delta L_W^{(n)}) + p_{NW}(\Delta L_W^{(n)})}
$$

The four per-feature posteriors are **fused multiplicatively**, with per-feature gains $G_i$ acting as on/off weights (gain = 1 disables the feature; gain = 0 gives it full weight):

$$
P_k^{(n)} = \prod_{i=1}^{4} \left((1-G_i)\,\hat{P}_i^{(n)}(k) + G_i\right)
$$

The fused probability $P_k^{(n)}$ is then **applied directly as the suppression gain** on the corresponding time-frequency bin. The authors note this is an MMSE estimator for the time-domain waveform [7].

### Parameter Optimization (Wiener-Reference MSE)

The eight non-estimable parameters ($\tau_W, \tau_{Wb}, \tau_D, \tau_{Db}$ and the four feature gains $G_i$) are tuned offline via **steepest-gradient descent** minimizing the MSE between the estimated suppression probability and an *oracle Wiener gain*:

$$
H_w^{(n)}(k) = \frac{|X_k^{(n)}|^2}{|X_k^{(n)}|^2 + |N_k^{(n)}|^2}
$$

computed from separately recorded clean-speech and noise-only signals (the mixture is created by summation, so the per-bin clean and noise components are available). Because the probability estimator (12) is also an MMSE estimator, minimizing $\sum_{n,k}(H_w - \hat{P})^2$ drives the parameter-tunable probability estimator toward the optimal Wiener gain, while penalizing functions keep the gains and time constants in their admissible ranges. The training/test split is 80/20 per file; optimization stops when the test-set criterion does not improve for five consecutive iterations (anti-overfitting).

## Experimental Setup

| Item | Value |
|------|-------|
| **Hardware** | Cell-phone mock-up with two unidirectional microphones, **9.6 mm** spacing, back-to-back |
| **Sampling rate** | 16 kHz |
| **Frame size** | 512 samples |
| **Directivity measurement** | Anechoic chamber, chirp signals, 36 rotations of $10^\circ$ |
| **Beamformer optimization** | Steepest gradient descent; $\Delta\theta = 30^\circ$ (i.e. front cone $[-30^\circ, +30^\circ]$, rear cone $[150^\circ, -150^\circ]$) |
| **Parameter optimization** | 16 files (various voices and input SNRs), ~1 min each; 80% train / 20% test |
| **Stopping criterion** | No test-set improvement for 5 iterations (anti-overfitting) |
| **Evaluation set** | Held-out recordings not used in optimization |
| **Metrics** | SNR improvement (dB); MOS improvement via [[concepts/pesq\|PESQ]] [8] |
| **Processing framework** | Frequency-domain, Hann weighting, overlap-add |

## Results

### Per-Feature Ablation (Table 1)

| Features combination | $G_\text{Lev/fr}$ | $G_\text{Lev/bin}$ | $G_\text{Del/fr}$ | $G_\text{Del/bin}$ | Av. SNR improv. (dB) |
|---|---|---|---|---|---|
| All four (optimized) | 0.00 | 0.00 | 0.89 | 0.99 | 11.06 |
| Lev/bin & fr, Del/fr | 0.02 | 0.00 | 0.68 | — | 10.82 |
| Lev/bin & fr | 0.00 | 0.19 | — | — | 10.43 |
| Lev/bin, Del/fr | — | 0.00 | 0.48 | — | 4.83 |
| Lev/fr | 0.00 | — | — | — | 5.25 |
| Lev/bin | — | 0.00 | — | — | 5.12 |
| Del/fr | — | — | 0.00 | — | 6.21 |
| Del/bin | — | — | — | 0.00 | 1.96 |

**Key finding from ablation**: The optimizer effectively **disables the two delay-based features** ($G_\text{Del/fr} = 0.89$, $G_\text{Del/bin} = 0.99$, both near 1). The authors attribute this to the very small 9.6 mm baseline — at 16 kHz this corresponds to roughly one quarter of the sampling period, making time-delay estimation unreliable. The system relies on **level-difference features only**, and these two features alone achieve 10.43 dB — virtually the same as all four features together (11.06 dB).

### Processing-Stage Breakdown (Table 2)

| Processing stage | Beamformer (BF) | Spatial filter (SF) | Total |
|---|---|---|---|
| Av. SNR improv. (dB) | 5.12 | 5.31 | **10.43** |
| MOS improv. (PESQ) | 0.15 | 0.24 | **0.39** |

The beamformer and the non-linear spatial filter contribute roughly equal SNR improvement (5.12 vs 5.31 dB), while the spatial filter contributes the majority of the perceptual (MOS) improvement (0.24 vs 0.15).

### Statistical-Model Verification

![[raw/papers/tashev-2008-sound-capture-spatial-filter/figures/e399766963dbc9a0163581c2b08185bc0dc2bdba051bbf624f4dffc3d1aba3c0.jpg|Figure 4 — Modeled vs. actual probability distributions for level difference per frame.]]
*Figure 4: Modeled (asymmetric exponential + Gaussian) vs. actual probability distributions for the per-frame level-difference feature. The estimated models cover the real distribution well, validating the asymmetric-PDF choice.*

## Key Contributions

1. **Back-to-back unidirectional microphone-array geometry** for small devices: two unidirectional capsules pointing in opposite directions, 9.6 mm apart, exploiting the directional response of each capsule as the primary cue. Distinct from classical [[concepts/differential-microphone-array\|differential microphone arrays]] that use omnidirectional capsules.
2. **Front-back-difference-maximizing beamformer**: a constrained optimization criterion that maximizes the ratio of beam energy in the desired cone to the energy in the opposite cone, rather than the usual maximum-SNR / minimum-variance criteria.
3. **[[concepts/probability-based-spatial-filter\|Probability-based non-linear spatial filter]]**: a Bayesian posterior over the source direction (front / rear / noise) per frame and per frequency bin, applied directly as the suppression gain. Each of the four features (per-frame level, per-bin level, per-frame delay, per-bin delay) has its own front/rear/noise PDFs and contributes a posterior; the four posteriors are fused multiplicatively with per-feature gains.
4. **Asymmetric statistical model** for level-difference features: exponential PDF for positive (front-source) differences, Gaussian PDF for negative (rear-source) differences, with the noise model updated during VAD-flagged non-voiced frames.
5. **Wiener-reference parameter-optimization framework**: non-estimable parameters (adaptation time constants, per-feature gains) are tuned offline by minimizing the MSE between the probability-based gain and an *oracle* [[concepts/wiener-filter\|Wiener gain]] computed from separately recorded clean speech and noise. Since both estimators are MMSE, this drives the tunable estimator toward the optimum.
6. **Empirical finding**: on a 9.6 mm baseline at 16 kHz, the optimizer disables the delay-based features (they correspond to only ~1/4 of the sampling period) and the system relies on **level-difference features only** — a quantitative justification for the back-to-back directional-microphone geometry over an omni-mic differential array.

## Related Concepts

- [[concepts/back-to-back-microphone-array\|Back-to-Back Microphone Array]]
- [[concepts/probability-based-spatial-filter\|Probability-Based Spatial Filter]]
- [[concepts/beamforming\|Beamforming]]
- [[concepts/differential-microphone-array\|Differential Microphone Array]]
- [[concepts/voice-activity-detection\|Voice Activity Detection]]
- [[concepts/multi-channel-speech-enhancement\|Multi-Channel Speech Enhancement]]
- [[concepts/speech-enhancement\|Speech Enhancement]]
- [[concepts/wiener-filter\|Wiener Filter]]
- [[concepts/pesq\|PESQ]]

## Related Synthesis

(None — no existing synthesis page covers small-device multi-microphone speech enhancement specifically; this is a single-system paper and does not provide new cross-source comparison data.)
