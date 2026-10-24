---
type: concept
created: 2026-10-24
updated: 2026-10-24
sources:
  - raw/papers/chiba-2027-wideband-anc-coaxial-loudspeaker/full-text.txt
tags:
  - active-noise-control
  - loudspeaker-design
  - open-ear-headphones
  - secondary-path-delay
---

# Coaxial Two-Way Secondary Source

A **coaxial offset 2-way secondary source** is a loudspeaker arrangement for ANC secondary paths in which a woofer and a tweeter are mounted on a common axis with the **tweeter placed in front of the woofer**, so that the tweeter is closer to the error microphone while the woofer's larger diaphragm provides low-frequency radiation capability. Introduced for wideband open-ear headphone ANC by [[sources/chiba-2027-wideband-anc-coaxial-loudspeaker|Chiba et al. 2027]] and realized in the nwm ONE open-ear headphone (woofer 35 mm, tweeter 12 mm, 13 mm coaxial offset).

## Why Coaxial and Offset

The two geometric features serve complementary delay terms of the [[concepts/causality|secondary-path delay budget]]:

- **Coaxial placement** keeps both drivers' outputs aligned on the loudspeaker axis at the ear-canal entrance (where the error microphone sits), so both can address the same cancellation zone.
- **Forward offset** gives the tweeter a short acoustic path (≈2 mm ≈ 6 µs) versus the woofer's (≈15 mm ≈ 44 µs) — beneficial at high frequencies where the quarter-period causality margin $\Delta\tau_q(f) = 1/(4f)$ shrinks.

The cost: the small tweeter has a higher fundamental resonance (≈300 Hz vs the woofer's ≈150 Hz), so its mechanical group delay is elevated up to ~500 Hz — precisely where the woofer should carry the control band. This complementarity motivates [[concepts/delay-oriented-driver-allocation|delay-oriented driver allocation]].

## Control Configurations

The band split (first-order Butterworth high-pass, $f_c = 500$ Hz in Chiba et al. 2027) can be realized in three ways:

| Configuration | Branches | Filter placement | Output-path delay | Cost |
|---------------|----------|------------------|-------------------|------|
| Dual-filter background | 2 adaptive | gradient path only | **none** (delayless) | ≈ 2R N MACs/sample |
| Dual-filter foreground | 2 adaptive | output branches | $\tau_{H_W}, \tau_{H_T}$ added | ≈ 2R N MACs/sample |
| Single-filter composite | 1 adaptive | after summed output | crossover delay in composite path | ≈ R N MACs/sample |

Measured-path results (48 kHz FxNLMS, 104 µs virtual electronic delay, pink noise): background dual-filter **Du-BpHp-Bg** 8.01 dB and single-filter **Xo-BpHp** 7.58 dB band-limited reduction over 100–2000 Hz, versus 5.94 dB (woofer only) and 5.02 dB (tweeter only).

## Relation to Audio Crossovers

In conventional 2-way speakers the crossover allocates bands for **flat spectral response**; here the allocation is driven by **delay minimization under a causality constraint**. In most ANC applications the control objective concentrates at low frequencies where a single woofer suffices; the open-ear case is exceptional because passive attenuation does not relax the requirement over the target band, extending it into the mid range where the tweeter's delay advantage matters.

## Related Concepts

- [[concepts/delay-oriented-driver-allocation|Delay-Oriented Driver Allocation]]
- [[concepts/open-ear-headphones|Open-Ear Headphones]]
- [[concepts/feedforward-anc|Feedforward ANC]]
- [[concepts/causality|Causality in ANC]]

## Related Sources

- [[sources/chiba-2027-wideband-anc-coaxial-loudspeaker|Chiba, Kamado, Kako & Noguchi 2027: Wideband ANC for Open-Ear Headphones via Low-Delay Acoustic Design with a Coaxial Loudspeaker]]
