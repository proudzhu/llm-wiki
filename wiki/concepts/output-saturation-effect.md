---
type: concept
created: 2026-08-10
updated: 2026-08-10
sources:
  - raw/papers/guo-2024-anc-saturation-survey/full-text.md
tags:
  - active-noise-control
  - nonlinear-systems
  - adaptive-filtering
  - output-saturation
---

# Output Saturation Effect

## Overview

The **output saturation effect** in [[active-noise-control|Active Noise Control]] refers to the nonlinear distortion introduced when the **power amplifier in the secondary path** is driven beyond its rated output power. Once the amplifier enters its nonlinear region, the control signal is clipped, which both deforms the anti-noise output and — more importantly — destabilises the adaptive filter coefficients of the controller, eventually causing them to diverge.

## Origin

The survey [[sources/guo-2024-anc-saturation-survey|Guo et al. 2024]] traces the secondary-path nonlinearity in ANC systems to a single dominant source — the output amplifier — by ruling out two alternatives:

1. **Error microphone / signal-conditioning circuit**: clipping occurs only if disturbance SPL exceeds the input range. Modern microphones cover ANC disturbance levels (40–90 dBA), so proper circuit design prevents this.
2. **Acoustic propagation**: large-amplitude waves induce nonlinear acoustic propagation, but ANC disturbance levels (< 100 dBA) are too low to trigger it.
3. **Actuator (output amplifier + loudspeaker)**: the dominant source. When desired output power exceeds the amplifier's rated output, the amplifier enters a saturation mode that clips the control signal.

## Narrow-band Saturation

For a sinusoidal disturbance $d(n) = D\sin(\omega_o n)$ with amplifier threshold $V_\mathrm{thr}$ and secondary-path gain $A_s$:

- $D \in [0, V_\mathrm{thr}]$: disturbance fully cancelled.
- $D \in [V_\mathrm{thr}, 4A_s V_\mathrm{thr}/\pi]$: disturbance cancelled but high-frequency harmonics appear; the residual error becomes a function of $3\omega_o, 5\omega_o, \dots$
- $D > 4A_s V_\mathrm{thr}/\pi$: fundamental cannot be fully attenuated; control filter coefficients overrun.

## Broadband Saturation

The saturation is modelled by an S-shaped nonlinear function $f[\cdot]$ cascaded after the control filter:

$$e(n) = d(n) - \sum_{l=0}^{L-1} s_l\, f[y(n-l)]$$

with the FxLMS update

$$\mathbf{w}(n+1) = \mathbf{w}(n) + \mu e(n)\mathbf{x}'(n).$$

When the disturbance cannot be fully cancelled because of the output limitation, the residual error retains the same phase as the filtered reference $\mathbf{x}'(n)$, so the magnitude of the control filter grows without bound:

$$\lim_{n\to\infty} \mathbb{E}[\mathbf{w}(n+1)] = \infty.$$

This divergence result is the analytical motivation for all saturation-mitigation algorithms: unconstrained linear (and even nonlinear) adaptive filters cannot remain stable once the amplifier is driven into severe saturation.

## Mitigation Strategies

The mitigation strategies split into two complementary families, each addressing the saturation from the opposite direction:

| Family | Strategy | Algorithms |
|:-------|:---------|:-----------|
| [[output-constraint-anc-algorithms|Output constraint]] | Limit output power to keep amplifier linear | 2-GD FxLMS, Re-scaling FxLMS, [[leaky-fxlms-algorithm|Leaky FxLMS]], MOV FxLMS, OLFxLMS, MOV-Modified FxLMS |
| [[nonlinear-active-noise-control|Nonlinear adaptive]] | Pre-distort control signal to cancel harmonic distortion | 2nd-VFxLMS, BFxLMS, FLANN-FsLMS, THF-FxLMS, MLPNN-FxLMS |

The two families correspond to distinct operating regimes: NANC is advantageous under **mild saturation** (only harmonics remain), while output constraint is required under **severe saturation** (fundamental not fully cancelable; unconstrained filters diverge).

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/output-constraint-anc-algorithms|Output Constraint ANC Algorithms]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/leaky-fxlms-algorithm|Leaky FxLMS Algorithm]]
- [[concepts/nonlinear-active-noise-control|Nonlinear Active Noise Control]]
- [[concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/minimum-variance-control|Minimum Variance Control]] — related but distinct concept

## Related Sources

- [[sources/guo-2024-anc-saturation-survey|Guo et al. 2024: ANC Algorithms Overcoming Output Saturation]]
