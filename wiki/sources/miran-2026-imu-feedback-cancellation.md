---
type: source
created: 2026-04-27
updated: 2026-04-27
sources:
  - raw/papers/miran-2026-imu-feedback-cancellation/full-text.txt
  - https://ieeexplore.ieee.org/abstract/document/11462231
  - zotero://select/items/0_W4JYT982
tags:
  - acoustic-feedback-cancellation
  - hearing-aids
  - inertial-sensor
  - imu
  - multimodal
  - adaptive-filtering
  - icassp
---

# Miran, Schepker, Merks & McKinney 2026: IMU-Based Acoustic Feedback Cancellation

**Authors**: [[../entities/sina-miran|Sina Miran]], [[../entities/henning-schepker|Henning Schepker]], [[../entities/ivo-merks|Ivo Merks]], [[../entities/martin-mckinney|Martin McKinney]]
**Institutions**: Starkey Hearing Technologies, Eden Prairie, MN, USA
**Published**: ICASSP 2026, pp. 15172–15176
**Type**: Conference Paper
**DOI**: [10.1109/ICASSP55912.2026.11462231](https://doi.org/10.1109/ICASSP55912.2026.11462231)
**Zotero**: [W4JYT982](zotero://select/items/0_W4JYT982)

---

## Summary

This paper proposes using an **inertial measurement unit (IMU)** integrated in a hearing aid to adjust the step size of the PEM-NLMS adaptive feedback cancellation (AFC) algorithm. When the IMU detects strong head acceleration (indicating a likely feedback path change), the step size is increased for rapid adaptation; when little motion is detected, a smaller step size improves steady-state accuracy. The IMU-based approach outperforms audio-only step-size methods (VSS, shadow filter) particularly in steady-state conditions, as it avoids audio-induced biases. However, it cannot detect path changes caused by external objects (e.g., phone approaching) that precede head movement, motivating a future multi-modal combination of audio and IMU signals.

---

## Problem Formulation

### Acoustic Feedback in Hearing Aids

Acoustic feedback occurs when the receiver output leaks back to the microphone through the acoustic path $F(z)$, creating a closed loop that limits maximum gain and causes whistling/howling artifacts.

### Adaptive Feedback Cancellation (AFC)

An adaptive filter $\hat{F}(z)$ estimates the feedback path and subtracts it from the microphone signal. The **PEM-NLMS** algorithm is commonly used, where a prediction error method provides prewhitening to reduce bias.

### The Step-Size Dilemma

- **Large step size** $\mu_L$: Fast convergence after path changes, but high steady-state error and potential instability
- **Small step size** $\mu_S$: Low steady-state error, but slow convergence after path changes

Existing audio-only VSS methods are **biased by input audio characteristics** — they cannot reliably distinguish between feedback path changes and changes in the input signal.

---

## Methodology

### IMU-Based Step-Size Control

The algorithm uses a 3-axis accelerometer integrated in the BTE hearing aid:

1. **Bandpass filter** (1–15 Hz, 10th-order Butterworth) the acceleration magnitude to isolate head movement
2. **Smooth** the filtered signal with asymmetric time constants:
   - Rising edge: $\kappa_R = 1$ (no smoothing, instant response)
   - Falling edge: $\kappa_F = 0.0096$ (1 s time constant, gradual decay)
3. **Threshold** the smoothed signal at $T_0$ to detect significant motion
4. **Switch** step size:
   - Motion detected → $\mu = \mu_L = 0.04$ (fast adaptation)
   - No motion → $\mu = \mu_S = 0.004$ (accurate estimation)

### ROC Analysis for Threshold Selection

Using measured dynamic feedback paths and IMU data from 5 subjects × 5 activities × 2 trials:
- **True positives**: Chewing, phone near ear, hat on/off, head shaking (activities causing path changes)
- **False positives**: Standing up/sitting down (activity without significant path change)
- Threshold $T_0 = 150$ provides a good balance between sensitivity and specificity

---

## Experimental Setup

| Parameter | Value |
|:----------|:------|
| Hearing aid | BTE with open fitting |
| Subjects | 5 |
| Activities | Chewing, phone, hat, head shake, stand/sit |
| Trial length | 32 s × 2 trials each |
| Sample rate (audio) | 20 kHz |
| Sample rate (IMU) | 104 Hz |
| Forward path gain | $G = 25$ dB |
| Processing delay | $d_P = 4$ ms |
| Adaptive filter length | $L_{\hat{h}} = 60$ |
| Prewhitening filter order | 16 |
| Input signal | Classical music (challenging for AFC) |

**Performance metric**: Normalized misalignment (MIS):

$$\text{MIS}[k] = 10\log_{10}\frac{\|\mathbf{h}[k] - \hat{\mathbf{h}}[k]\|_2^2}{\|\mathbf{h}[k]\|_2^2}$$

---

## Results

### Comparison with Baselines

| Method | Path Change Response | Steady-State MIS | Audio Bias |
|:-------|:--------------------|:-----------------|:-----------|
| Fast Filter ($\mu_L$ fixed) | Fast | High (~−10 dB) | N/A |
| Slow Filter ($\mu_S$ fixed) | Slow (whistling!) | Low (~−20 dB) | N/A |
| Shadow Filter | Moderate | Biased toward $\mu_L$ | Moderate |
| VSS (Tran 2016) | Moderate | Biased toward $\mu_L$ | High |
| **IMU AFC** | **Fast** | **Low (~−20 dB)** | **None** |

### Key Observations

1. **IMU AFC follows Fast Filter during path changes** and **Slow Filter during steady state** — achieving the best of both
2. **Audio-based methods (VSS, Shadow) are biased toward large step size**, failing to achieve small MIS in steady state
3. **Limitation**: When path change precedes head movement (e.g., phone moved close by hand before head turns), IMU AFC has a detection delay
4. **False positive risk**: Activities like standing/sitting may trigger large step size without actual path change (lower specificity → more false positives)

---

## Key Contributions

1. **First use of IMU for AFC step-size control**: Demonstrates that head movement acceleration is a reliable predictor of feedback path changes
2. **Outperforms audio-only methods in steady state**: IMU-based switching avoids audio-induced biases that plague VSS and shadow filter approaches
3. **Practical algorithm**: Simple threshold-based switching with asymmetric smoothing, implementable on hearing aid DSP
4. **Multi-modal motivation**: Results encourage combining IMU and audio signals for optimal step-size adjustment

---

## Limitations and Future Work

- **Detection delay**: External objects (phone, hand) can change the feedback path before head movement occurs
- **False positives**: Non-path-changing activities may trigger unnecessary fast adaptation
- **Future**: Multi-modal approach combining IMU and audio-based step-size control for robust performance in all scenarios

---

## Related Concepts

- [[../concepts/acoustic-feedback|Acoustic Feedback]]
- [[../concepts/variable-step-size-lms|Variable Step Size LMS]]
- [[../concepts/active-noise-control|Active Noise Control]]

## Related Sources

- [[../sources/akhtar-2006-vss-lms-online-spm|Akhtar 2006: VSS LMS for Online Secondary Path Modeling]] — Classical VSS approach for ANC (different domain, same step-size dilemma)

## Related Entities

- [[../entities/sina-miran|Sina Miran]]
- [[../entities/henning-schepker|Henning Schepker]]
- [[../entities/ivo-merks|Ivo Merks]]
- [[../entities/martin-mckinney|Martin McKinney]]
