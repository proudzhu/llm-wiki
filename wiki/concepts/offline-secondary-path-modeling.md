---
type: concept
created: 2026-04-11
updated: 2026-04-11
sources:
tags:
- active-noise-control
- secondary-path
- system-identification
---

# Offline Secondary-Path Modeling

**Offline secondary-path modeling** identifies the secondary path $S(z)$ during a **training phase before ANC operation begins**. This contrasts with [[online-secondary-path-modeling|Online Secondary-Path Modeling]], which identifies $S(z)$ while the system is actively canceling noise.

## Method

The standard approach (Kuo 1999, Section VI):

1. **Inject white noise** $v(n)$ through the secondary path (loudspeaker)
2. **Record the error sensor** output $d(n) = S(z) * v(n)$
3. **Identify $\hat{S}(z)$** using the LMS algorithm:

$$\hat{s}(n+1) = \hat{s}(n) + \rho \cdot e_s(n) \cdot v(n)$$

where $e_s(n) = d(n) - \hat{s}(n) * v(n)$ is the modeling error.

## Advantages

- **No bias**: The injected noise is uncorrelated with primary noise, so convergence is unbiased
- **Fast convergence**: All processing power goes to identification — no interference from ANC operation
- **Simple implementation**: Standard LMS with white noise input converges quickly

## Disadvantages

- **Requires downtime**: System must be taken offline for training
- **Cannot track changes**: If $S(z)$ drifts (temperature, headphone fit, ear canal changes), the model becomes stale
- **Inconvenient for users**: Training noise is audible

## Accuracy Requirements

The [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] tolerates moderate modeling errors:
- Under slow adaptation, FXLMS can tolerate **~90° phase error** between $S(z)$ and $\hat{S}(z)$
- Within 40° phase error, convergence speed is nearly unaffected

## When to Use

| Scenario | Offline | Online |
|----------|---------|--------|
| Fixed, known hardware | ✅ | — |
| Lab / controlled environment | ✅ | — |
| Headphones (fit varies per user) | — | ✅ |
| Ear canal changes during use | — | ✅ |
| Long secondary paths (many coefficients) | — | ✅ (if adaptive) |

## Related

- [[online-secondary-path-modeling|Online Secondary-Path Modeling]] — Identifying $S(z)$ during active ANC operation
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — Requires $\hat{S}(z)$ for reference signal filtering
- [[multi-channel-anc|Multi-Channel ANC]] — Offline modeling is impractical when $O(M \times N)$ paths must be identified
- [[active-noise-control|Active Noise Control]] — Core system architecture

## Sources

- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] — Section VI: Online Secondary-Path Modeling (describes offline as baseline)
- [[sources/wu-2014-simplified-adaptive-feedback-anc|Wu 2014: Simplified Adaptive Feedback ANC]] — Uses offline secondary path modeling

## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[online-secondary-path-modeling|Online Secondary-Path Modeling]]
- [[system-identification|System Identification]]
- [[multi-channel-anc|Multi-Channel ANC]]

## Related Sources

- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]]
- [[sources/wu-2014-simplified-adaptive-feedback-anc|Wu 2014: Simplified Adaptive Feedback ANC]]
