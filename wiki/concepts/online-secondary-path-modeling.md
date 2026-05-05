---
type: concept
created: 2026-04-10
updated: 2026-04-27
sources:
  - raw/papers/akhtar-2006-vss-lms-online-spm/full-text.txt
tags:
- active-noise-control
- online-modeling
- system-identification
---

# Online Secondary-Path Modeling

## Overview

**Online secondary-path modeling** identifies the secondary path S(z) while the ANC system is actively canceling noise. This contrasts with [[offline-secondary-path-modeling|Offline Secondary-Path Modeling]], where S(z) is estimated during a training phase before ANC operation begins.

## Why Online Modeling?

Offline modeling assumes S(z) is time-invariant, which is often violated in practice:
- Temperature changes affect loudspeaker characteristics
- Airflow speed changes in ducts
- Headset wearing position shifts
- Component aging

## The Challenge

During ANC operation, the error signal contains both:
1. **Residual primary noise** (what we want to cancel)
2. **Contribution from the secondary source** (the anti-noise)

To identify S(z), we need to know what the secondary source contributes — but this is mixed with the primary noise.

## Standard Approach: Auxiliary Noise Injection

Inject a low-power white noise signal v(n) into the system:

```
y(n) + v(n) → [S(z)] → error mic
```

Then identify Ŝ(z) using the known v(n) as the excitation signal. The key insight: v(n) is uncorrelated with the primary noise, so standard system identification techniques work.

### Trade-off

- **Too much v(n)**: Interferes with noise cancellation performance
- **Too little v(n)**: Slow or inaccurate identification

## Techniques to Reduce Interference

1. **Power-controlled injection**: Dynamically adjust v(n) power based on identification accuracy needs
2. **Intermittent injection**: Only inject v(n) when Ŝ(z) drift is detected
3. **Correlation-based methods**: Use the known correlation properties of v(n) to separate it from the primary noise

## Two-Filter vs Three-Filter Methods

### Three-Filter Methods (Eriksson, Bao, Kuo, Zhang)
Existing methods for online secondary path modeling use three adaptive filters: noise control filter, modeling filter, and a third filter to reduce cross-interference. Zhang's cross-updated method (2001) gives the best performance among three-filter methods.

### Two-Filter Method (Akhtar 2006)
Akhtar et al. proposed using only two adaptive filters:
- **Control filter**: adapted via Modified-FxLMS (MFxLMS), which allows larger step sizes than standard FxLMS
- **Modeling filter**: adapted via a novel [[variable-step-size-lms|Variable Step Size LMS]] algorithm with an inverse strategy — small step size initially (when disturbance is large), increasing as disturbance decreases

This two-filter structure achieves better or comparable performance to three-filter methods with reduced design complexity.

## Alternative: Natural Excitation

Some methods exploit the fact that the controller output y(n) itself can serve as an excitation signal if the primary noise has sufficient spectral content. This avoids the need for auxiliary noise injection but requires careful signal separation.

## Related Concepts

- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[active-noise-control|Active Noise Control]]
- [[multi-channel-anc|Multi-Channel ANC]] — Online modeling is even more critical in multi-channel (O(M·N) paths to identify)
- [[offline-secondary-path-modeling|Offline Secondary-Path Modeling]]
- [[variable-step-size-lms|Variable Step Size LMS]]
- [[deep-secondary-path-estimation|Deep Secondary Path Estimation]]

## Related Sources

- [[../sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] — Section VI: Online Secondary-Path Modeling
- [[../sources/akhtar-2006-vss-lms-online-spm|Akhtar 2006: VSS LMS for Online Secondary Path Modeling]]
