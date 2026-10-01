---
type: concept
created: 2026-10-01
updated: 2026-10-01
sources:
  - raw/papers/cheng-2026-anc-gain-constraint/full-text.txt
tags:
  - active-noise-control
  - loudspeaker
  - hardware-limits
---

# Mechanical Over-Excursion

**Mechanical over-excursion** is the physical failure mode of a (micro-)loudspeaker whose diaphragm displacement exceeds its mechanical limits, introducing nonlinear distortion and, in ANC applications, degrading the loudspeaker's service life. For the micro-loudspeakers of compact devices (smartphones, smart glasses, hearables), it is triggered mainly by **low-frequency** content, because these transducers have a strongly **rolled-off low-frequency response** and correspondingly limited reproduction capability.

## Why ANC Control Filters Cause It

An unconstrained ANC control filter — e.g. the Wiener–Hopf solution $\mathbf{w}_{\mathrm{opt}} = -\mathbf{R}_{x'}^{-1}\mathbf{r}_{dx'}$ — minimizes the error-signal MSE and therefore develops **high gain wherever the disturbance has energy and the secondary path is weak**, which for pink-like noise and a rolled-off micro-loudspeaker means excessive low-frequency gain ([[sources/cheng-2026-anc-gain-constraint|Cheng et al. 2026]]). The result:

- The control signal demands more diaphragm excursion than the transducer can physically deliver — neither linear nor nonlinear ANC algorithms can supply the missing mechanical momentum, so cancellation fails.
- Driving beyond the physical limit produces nonlinear distortion and accelerates wear, degrading service life.
- The wasted dynamic range at low frequencies compresses the range available in the effective cancellation band.

## Distinction from Output Saturation

Mechanical over-excursion is the **transducer-side** limit, distinct from the **amplifier-side** [[concepts/output-saturation-effect|output saturation effect]] (clipping of the secondary-path power amplifier). The two phenomena motivate different constraint targets:

| Phenomenon | Dominant source | Constraint target | Mitigation |
|:-----------|:---------------|:-------------------|:-----------|
| Output saturation | Power amplifier beyond rated output | Output **power/amplitude** | [[concepts/output-constraint-anc-algorithms\|output constraint ANC algorithms]] (online) |
| Mechanical over-excursion | Diaphragm displacement beyond mechanical limit, mainly at low frequency | Filter **frequency-response gain** at low frequencies | [[concepts/frequency-response-constrained-anc\|ANC-FRC]] (design time), high-pass cascade |

## Mitigation Strategies

| Strategy | Mechanism | Drawback |
|:---------|:----------|:---------|
| High-pass / band-stop cascade | Removes low-frequency output power at runtime | Added group delay → phase distortion, lower NR upper bound |
| Clipping | Hard limit on the output signal | Generates high-frequency components |
| Frequency-response gain constraint ([[concepts/frequency-response-constrained-anc|ANC-FRC]]) | Bounds low-frequency filter gain at design time | None at runtime — no added delay |

## Related Concepts

- [[concepts/frequency-response-constrained-anc|Frequency-Response Constrained ANC (ANC-FRC)]]
- [[concepts/output-saturation-effect|Output Saturation Effect]]
- [[concepts/output-constraint-anc-algorithms|Output Constraint ANC Algorithms]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/wiener-filter|Wiener Filter]]

## Related Sources

- [[sources/cheng-2026-anc-gain-constraint|Cheng, Zhou, Liu, Zhao & Shi 2026: Active Noise Control With a Gain Constraint for Micro-Loudspeakers]]
