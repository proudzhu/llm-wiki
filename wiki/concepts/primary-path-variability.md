---
type: concept
created: 2026-05-05
updated: 2026-08-27
sources:
  - wiki/sources/liebich-2018-doa-dependency-anc-headphones.md
  - wiki/sources/guldenschuh-2014-secondary-path-irregularities.md
tags:
  - active-noise-control
  - direction-of-arrival
  - headphones
---

# Primary Path Variability

**Primary path variability** refers to changes in the acoustic transfer function $P(z)$ between the outer (reference) microphone and the inner (error) microphone of an ANC headphone, caused by variations in the direction of arrival (DOA) of the incident sound.

## Definition

The primary path $P(z)$ describes how sound propagates from the outer microphone to the inner microphone of a headphone. For a given direction $i$, the primary path is denoted $P_i(z)$. The deviation from a nominal primary path $P_n(z)$ is quantified as:

**Relative magnitude deviation:**

$$\Delta P_{\text{rel}}(z) = \left|\frac{P_i(z) - P_n(z)}{P_n(z)}\right|$$

**Phase deviation:**

$$\Delta\angle P(z) = |\angle P_i(z) - \angle P_n(z)|$$

## Causes

1. **Diffraction around the head**: Sound arriving from different angles interacts differently with the head and pinnae
2. **Headphone housing resonances**: The headphone shell creates direction-dependent resonances, especially at contralateral angles
3. **Acoustic shadow effects**: The head blocks sound from the opposite side, altering the transfer function

## Impact on ANC

Since the optimal feedforward filter is $\hat{W}_{\text{opt}}(z) = P(z)/G(z)$, any change in $P(z)$ with DOA means a filter optimized for one direction will be suboptimal for others. The resulting magnitude and phase deviations in the anti-noise signal directly degrade attenuation, as quantified by the [[anc-attenuation-bounds|ANC Attenuation Bounds]].

## Frequency-Dependent Behavior

| Frequency | Variability | ANC Impact |
|-----------|------------|------------|
| < 200 Hz | Negligible | Feedforward ANC robust across all DOAs |
| 200 Hz – 1 kHz | Moderate | Some DOAs show degraded performance |
| > 1 kHz | Severe | Feedforward ANC highly DOA-dependent; resonance effects |

## Comparison: In-Ear vs. On-Ear

In-ear headphones show less primary path variability than on-ear headphones (cf. Guldenschuh), because:
- The two microphones are in closer proximity
- The housing is more compact and acoustically sealed

## Contrast with Secondary-Path Variability

Primary-path variability is DOA-driven and attacks **high frequencies** (>1 kHz, housing resonances), degrading feedforward performance but not stability. Its sibling, [[secondary-path-variability|secondary-path variability]], is fit-driven (leaks, lifting) and attacks **low frequencies** (<300 Hz), where it threatens both adaptation and feedback-loop stability — see [[sources/guldenschuh-2014-secondary-path-irregularities|Guldenschuh & de Callafon 2014]].

## Related Concepts

- [[device-specific-hrtf|Device-Specific HRTF (DHRTF)]]
- [[anc-attenuation-bounds|ANC Attenuation Bounds]]
- [[feedforward-anc|Feedforward ANC]]
- [[uncertainty-modeling-for-anc|Uncertainty Modeling for ANC]]
- [[secondary-path-variability|Secondary Path Variability]]

## Related Sources

- [[sources/liebich-2018-doa-dependency-anc-headphones|Liebich 2018: DOA Dependency of ANC Headphones]]
- [[sources/guldenschuh-2014-secondary-path-irregularities|Guldenschuh & de Callafon 2014: Detection of Secondary-Path Irregularities in ANC Headphones]]
