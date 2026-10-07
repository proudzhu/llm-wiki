---
type: concept
created: 2026-05-05
updated: 2026-10-07
sources:
  - wiki/sources/liebich-2018-doa-dependency-anc-headphones.md
  - wiki/sources/guldenschuh-2014-secondary-path-irregularities.md
  - raw/papers/rout-2012-pso-anc-without-secondary-path/full-text.txt
  - wiki/sources/liebich-2022-occlusion-effect-cancellation.md
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

The journal extension ([[sources/liebich-2022-occlusion-effect-cancellation|Liebich & Vary 2022]]) reports percentile plots of the same 4608-direction DHRTF campaign and formalizes both primary- and secondary-path deviations as multiplicative uncertainties $P(z) = \Delta_P(z) P_n(z)$, $G(z) = \Delta_G(z) G_n(z)$, showing that attenuation requires $|1 - \Delta_G/\Delta_P| < |1/P|$ — i.e., the deviation *ratio* should approach 1 — and that the feedback controller reduces the deviation influence wherever $|S| < 1$.

## Frequency-Dependent Behavior

| Frequency | Variability | ANC Impact |
|-----------|------------|------------|
| < 200 Hz | Negligible | Feedforward ANC robust across all DOAs |
| 200 Hz – 1 kHz | Moderate | Some DOAs show degraded performance |
| > 1 kHz | Severe | Feedforward ANC highly DOA-dependent; resonance effects |

## Abrupt Primary-Path Changes

DOA variability is gradual and continuous; the complementary case is an **abrupt** primary-path change — e.g., a door or window suddenly opening in a room or vehicle cabin — which invalidates a converged controller instantly. A gradient-based controller can re-track the new path, but a converged population-based optimizer has lost its diversity and remains stuck at the old optimum. The [[concepts/conditional-reinitialized-pso|conditional reinitialized PSO]] of [[sources/rout-2012-pso-anc-without-secondary-path|Rout, Das & Panda 2012]] addresses exactly this case: the gbest squared-error jump triggers re-randomization of the swarm, recovering the global minimum after every change (verified over ten independent runs).

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
- [[concepts/conditional-reinitialized-pso|Conditional Reinitialized PSO]] — handles abrupt (not DOA-driven) primary-path changes

## Related Sources

- [[sources/liebich-2018-doa-dependency-anc-headphones|Liebich 2018: DOA Dependency of ANC Headphones]]
- [[sources/liebich-2022-occlusion-effect-cancellation|Liebich & Vary 2022: Occlusion Effect Cancellation in Headphones and Hearing Devices]] — multiplicative-uncertainty formalization
- [[sources/guldenschuh-2014-secondary-path-irregularities|Guldenschuh & de Callafon 2014: Detection of Secondary-Path Irregularities in ANC Headphones]]
- [[sources/rout-2012-pso-anc-without-secondary-path|Rout, Das & Panda 2012: PSO-Based ANC Without Secondary Path Identification]] — abrupt (door/cabin) primary-path changes handled by CRPSO reinitialization
