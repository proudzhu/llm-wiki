---
type: concept
created: 2026-05-05
updated: 2026-10-31
sources:
  - wiki/sources/liebich-2018-doa-dependency-anc-headphones.md
  - wiki/sources/liebich-2022-occlusion-effect-cancellation.md
  - raw/papers/chiba-2027-wideband-anc-coaxial-loudspeaker/full-text.txt
  - raw/papers/zhang-2020-coherence-mcanc-noise-reduction/full-text.txt
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
5. **Amplitude underestimation is forgiving**: With the amplitude *underestimated* ($\Delta A_{\mathrm{rel}} < 0$ dB), attenuation is still achieved for phase deviations beyond 60°; conversely, with perfect phase, amplitude deviation up to ~6 dB still attenuates (Liebich & Vary 2022, contour version of the bound)

## Delay-Induced Phase Error Under Optimal Amplitude (Chiba et al. 2027)

[[sources/chiba-2027-wideband-anc-coaxial-loudspeaker|Chiba et al. 2027]] extend the tonal bound to the case where the phase deviation comes from **excess secondary-path delay**: with $\Delta\theta(f) = 2\pi f \Delta\tau(f)$ and optimal amplitude ratio $\Delta A^\star = \cos\Delta\theta$ (constrained to $\Delta A \geq 0$), the minimum residual over the first phase-error interval $0 \leq \Delta\theta < \pi/2$ is

$$\beta_{\min}(f) = 20\log_{10}|\sin(2\pi f \Delta\tau(f))|$$

which vanishes at the quarter-period boundary $\Delta\tau_q(f) = 1/(4f)$ — the "90° boundary" where positive attenuation disappears. This is the same mechanism as observation 3 above (time delay compounds phase error with frequency), now inverted into a *design target*: because $\Delta\tau_q$ shrinks with frequency, each µs of delay reduction buys bandwidth at the top of the control band, motivating delay-minimizing loudspeaker design (see [[concepts/delay-oriented-driver-allocation|Delay-Oriented Driver Allocation]]).

## Implications for ANC Design

- The bound explains why [[feedforward-anc|Feedforward ANC]] is sensitive to [[primary-path-variability|Primary Path Variability]]: even moderate DOA-induced deviations in $P(z)$ can significantly reduce attenuation
- It motivates [[hybrid-anc|Hybrid ANC]] architectures where the [[feedback-anc|Feedback ANC]] component (which does not depend on $P(z)$) compensates for feedforward degradation
- It provides a quantitative criterion for when adaptive or direction-dependent filter switching becomes necessary

## Statistical/System-Level Bound (Zhang et al. 2020)

The bounds above constrain the *signal-level* match between anti-noise and disturbance. Complementary to them, [[sources/zhang-2020-coherence-mcanc-noise-reduction|Zhang et al. 2020]] derive a **statistical system-level bound**: the minimum residual energy of a multichannel feedforward system decomposes into a coherence term, a filter term (zero at the optimum), and a null-space term — see [[concepts/anc-nr-potential-decomposition|ANC NR-Potential Decomposition]]. Where the Liebich/Chiba bounds ask "how precisely must the anti-noise match the disturbance at one point", the Zhang bound asks "how much of the disturbance field is reachable and predictable at all, given the transducer configuration".

## Related Concepts

- [[primary-path-variability|Primary Path Variability]]
- [[feedforward-anc|Feedforward ANC]]
- [[feedback-anc|Feedback ANC]]
- [[hybrid-anc|Hybrid ANC]]
- [[device-specific-hrtf|Device-Specific HRTF (DHRTF)]]
- [[concepts/anc-nr-potential-decomposition|ANC NR-Potential Decomposition]] — the statistical/system-level counterpart bound

## Related Sources

- [[sources/liebich-2018-doa-dependency-anc-headphones|Liebich 2018: DOA Dependency of ANC Headphones]]
- [[sources/liebich-2022-occlusion-effect-cancellation|Liebich & Vary 2022: Occlusion Effect Cancellation in Headphones and Hearing Devices]] — journal version with the contour presentation
- [[sources/chiba-2027-wideband-anc-coaxial-loudspeaker|Chiba, Kamado, Kako & Noguchi 2027: Wideband ANC for Open-Ear Headphones with a Coaxial Loudspeaker]] — optimal-amplitude residual under delay-induced phase error; quarter-period (90°) relaxed boundary as the design limit
- [[sources/zhang-2020-coherence-mcanc-noise-reduction|Zhang, Murata, Maeno, Samarasinghe, Abhayapala & Mitsufuji 2020: Coherence-Based Performance Analysis on Noise Reduction in Multichannel ANC]] — the statistical counterpart: algorithm-independent maximum NR via residual-energy decomposition
