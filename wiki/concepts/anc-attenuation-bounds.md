---
type: concept
created: 2026-05-05
updated: 2026-05-05
sources:
  - wiki/sources/liebich-2018-doa-dependency-anc-headphones.md
tags:
  - active-noise-control
  - control-theory
  - signal-processing
---

# ANC Attenuation Bounds

**ANC attenuation bounds** are analytical limits on the achievable noise attenuation as a function of the magnitude and phase deviation between the anti-noise signal and the primary disturbance. They quantify how precisely the anti-noise must match the disturbance to achieve a target attenuation level.

## Derivation (Liebich et al. 2018)

For a tonal disturber $A \cos(\omega t)$ and compensation signal $B \cos(\omega t + \Delta\phi)$, the gain (inverse of attenuation) is:

$$\text{Gain} = 1 - 2\Delta A_{\text{rel}} \cos(\Delta\phi) + \Delta A_{\text{rel}}^2$$

where $\Delta A_{\text{rel}} = B/A$ is the relative amplitude of the compensation to the disturbance.

Solving for the relative amplitude deviation at a given phase deviation and target gain:

$$\Delta A_{\text{rel}} = \cos(\Delta\phi) \pm \sqrt{\cos^2(\Delta\phi) - (1 - \text{Gain})}$$

## Key Results

| Target Attenuation | Max Amplitude Deviation | Max Phase Deviation |
|---------------------|------------------------|---------------------|
| 0 dB (no amplification) | 6.02 dB | 60° |
| 5 dB | 2.54 dB | 18.19° |
| 10 dB | 1.49 dB | 10.29° |
| 15 dB | 1.06 dB | 7.18° |
| 20 dB | 0.83 dB | 5.76° |

## Critical Observations

1. **Phase is more critical than amplitude**: A phase deviation >60° causes amplification even with perfect amplitude matching ($\Delta A_{\text{rel}} = 0$ dB)
2. **High attenuation demands extreme precision**: 20 dB attenuation requires <0.83 dB amplitude error and <5.76° phase error
3. **Time delay compounds phase error**: A constant time delay $\Delta t$ translates to increasing phase deviation with frequency ($\Delta\phi = 2\pi f \Delta t$), making high-frequency attenuation increasingly difficult
4. **Frequency independence**: The bound is independent of $\omega$ for tonal signals; the frequency dependence enters only through the time-delay-to-phase conversion

## Implications for ANC Design

- The bound explains why [[feedforward-anc|Feedforward ANC]] is sensitive to [[primary-path-variability|Primary Path Variability]]: even moderate DOA-induced deviations in $P(z)$ can significantly reduce attenuation
- It motivates [[hybrid-anc|Hybrid ANC]] architectures where the [[feedback-anc|Feedback ANC]] component (which does not depend on $P(z)$) compensates for feedforward degradation
- It provides a quantitative criterion for when adaptive or direction-dependent filter switching becomes necessary

## Related Concepts

- [[primary-path-variability|Primary Path Variability]]
- [[feedforward-anc|Feedforward ANC]]
- [[feedback-anc|Feedback ANC]]
- [[hybrid-anc|Hybrid ANC]]
- [[device-specific-hrtf|Device-Specific HRTF (DHRTF)]]

## Related Sources

- [[sources/liebich-2018-doa-dependency-anc-headphones|Liebich 2018: DOA Dependency of ANC Headphones]]
