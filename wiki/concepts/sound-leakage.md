---
type: concept
created: 2026-11-12
updated: 2026-11-12
sources:
  - raw/papers/chiba-2026-open-back-enclosure-leakage/full-text.md
tags:
  - open-ear-headphones
  - wearable-audio
  - privacy
  - acoustic-enclosure-design
---

# Sound Leakage

**Sound leakage** is the outward radiation of reproduced audio from a wearable device into the surrounding environment, where it is audible to bystanders. It is the mirror image of *sound isolation*: with sound isolation the concern is noise entering the ear; with leakage the concern is audio leaving the device. Because the term is used loosely for both, the precise definition is worth stating — leakage is the part of the radiated sound that escapes to the environment instead of reaching the listener's ear.

The condition is structural to [[concepts/open-ear-headphones|open-ear headphones]]: the open gap between enclosure and ear canal that provides transparency and avoids the [[concepts/ear-canal-occlusion-effect|occlusion effect]] is also the exit for playback audio. Leakage therefore scales with how open the design is, and it is the main reason open-ear devices are awkward in shared spaces (trains, offices, libraries).

## Mitigation Routes

| Route | Mechanism | Cost |
|---|---|---|
| Signal-side | Control object-audio gains/positions to limit leakage-prone frequencies | Timbre and loudness changes |
| Loudspeaker arrays | Parametric/ultrasonic emitters, evanescent-wave arrays, linear/circular arrays, end-fire wearable arrays | Many drivers; prohibitive in a compact headphone |
| Enclosure-less opposite-phase array | Add a second driver radiating in anti-phase to cancel leakage by interference (Fukui et al. 2024) | Two drivers, precise positioning |
| **Open-back enclosure** | Vent the single driver's own rear (opposite-phase) radiation through side-openings, Helmholtz-tuned ([[concepts/open-back-enclosure\|Chiba et al. 2026]]) | Passive, single driver; band-limited (~1–7 kHz), loses to sealed designs above ~7 kHz |
| Active leakage control | Adaptive/non-adaptive ANC-like control of the external field (Cha et al. 2012; Lee et al. 2013) | Microphones, DSP, stability |

## Evaluation

Leakage must be measured **normalized by the listening level**, because enclosure changes that cut leakage often also change how loud the device plays at the ear — an absolute-only comparison would credit designs that simply got quieter. Standard practice in the dummy-head literature:

$$L^{\text{norm}}_{A,\text{mean}}(f) = W_A(f) + \frac{1}{N_\Phi}\sum_{\phi \in \Phi}\big(L(f,\phi) - L_{\text{ref}}(f)\big)$$

with A-weighting $W_A$, leakage SPL $L(f,\phi)$ on a semicircular arc behind the listener (typically 150 mm radius, 0°–180° in 15° steps), and $L_{\text{ref}}$ the SPL at the ear-canal entrance. Band averages are taken over the interference-viable 1–7 kHz range.

## Two-Sided Design Constraint

Leakage suppression and transparency pull in opposite directions, and the trade-off has a frequency shape: opposite-phase cancellation is effective at low and mid frequencies where the wavelength is long relative to the enclosure, and fails at high frequencies where small geometric deviations desynchronize the phase. A passive open-back design thus needs a deliberate high-frequency roll-off of the cancelling path; a sealed design leaks less above ~7 kHz but loses transparency entirely.

Leakage signals also carry device-identifying and ear-shape-dependent information (they have been used for personal authentication), so leakage characteristics are partly individual rather than a property of the enclosure alone.

## Related Concepts

- [[concepts/open-back-enclosure|Open-Back Enclosure]]
- [[concepts/dipole-acoustic-radiation|Dipole Acoustic Radiation]]
- [[concepts/open-ear-headphones|Open-Ear Headphones]]
- [[concepts/ear-canal-occlusion-effect|Ear-Canal Occlusion Effect]]

## Related Sources

- [[sources/chiba-2026-open-back-enclosure-leakage|Chiba, Kako & Harada 2026: Designing an Open-Back Enclosure to Mitigate Sound Leakage for Open-Ear Headphones]] — 7.6 dB normalized leakage reduction over 1–7 kHz with a single driver, no DSP
