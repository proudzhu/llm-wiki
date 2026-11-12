---
type: concept
created: 2026-11-12
updated: 2026-11-12
sources:
  - raw/papers/chiba-2026-open-back-enclosure-leakage/full-text.md
tags:
  - acoustic-enclosure-design
  - open-ear-headphones
  - sound-leakage
  - wearable-audio
---

# Open-Back Enclosure

An **open-back enclosure** for a wearable loudspeaker is a housing whose back cavity is deliberately vented, so that the driver's opposite-phase rear radiation escapes into the environment instead of being trapped or absorbed. Vented rear radiation converts the driver from a monopole into an **acoustic dipole**, which radiates a strong near field and a weak far field — the property exploited to keep playback level at the wearer's ear while cutting [[concepts/sound-leakage|sound leakage]] to bystanders.

Introduced for small single-driver [[concepts/open-ear-headphones|open-ear headphones]] by [[sources/chiba-2026-open-back-enclosure-leakage|Chiba, Kako & Harada 2026]] (IEEE Access), building on the enclosure-less two-driver array of Fukui et al. (2024).

## Design Parameters

| Parameter | Sets | Effect |
|---|---|---|
| Back-cavity volume $V$ | Helmholtz resonance with the opening area | Fixed by the enclosure envelope; larger $V$ lowers $f_H$ |
| Total opening area $S \approx N_S h d$ | Helmholtz resonance | The practical tuning knob ($d$ = opening width) |
| Duct length $L$ | Helmholtz resonance | Fixed by wall thickness |
| Opening **position** (side vs. back) | Dipole axis and source separation $D$ | Side-openings orient the axis vertically and shorten $D$ |

The cavity-plus-openings is a Helmholtz resonator,

$$f_H = \frac{c}{2\pi}\sqrt{\frac{S}{V(L+\delta)}}, \qquad \delta = \sqrt{S}$$

used here for two acoustic jobs rather than for bass extension:

1. **Group delay** — the rapid phase rotation around $f_H$ delays the opposite-phase wave by the amount needed to compensate the front-vs-back path-length mismatch at the leakage point, bringing the two waves near anti-phase.
2. **Low-pass** — above $f_H$ the resonance attenuates the opposite-phase wave, suppressing constructive interference at high frequencies where phase-based cancellation is geometrically fragile.

The two roles are why an enclosure (not merely an open grille) matters: the tuning moves the cancellation band and its depth without changing enclosure size, driver, or electronics.

## Geometric Rules

- **Opening separation** trades near-field listening level against far-field cancellation: too close and cancellation eats the wearer's low-frequency response; too far and the dipole becomes an ineffective far-field radiator.
- **Dipole axis orientation**: radiation peaks along the axis and is minimal perpendicular to it, so the axis should be aimed away from the plane occupied by bystanders (vertical for headphones).
- **Symmetry**: four openings at 90° average out wearing-position and ear-shape variation instead of relying on one preferred orientation.

## Measured Effect

On a dummy head, 1,000–7,000 Hz, listening-level-normalized A-weighted leakage: side-opening enclosure ($d$ = 2.0 mm) is **7.6 dB** below a sealed enclosure and **7.3 dB** below a back-opening enclosure with the same resonance frequency. Above ~7 kHz the sealed enclosure leaks *less* — the open-back advantage is band-limited and must be traded against high-frequency roll-off.

## Related Concepts

- [[concepts/dipole-acoustic-radiation|Dipole Acoustic Radiation]]
- [[concepts/sound-leakage|Sound Leakage]]
- [[concepts/open-ear-headphones|Open-Ear Headphones]]
- [[concepts/ear-canal-occlusion-effect|Ear-Canal Occlusion Effect]]

## Related Sources

- [[sources/chiba-2026-open-back-enclosure-leakage|Chiba, Kako & Harada 2026: Designing an Open-Back Enclosure to Mitigate Sound Leakage for Open-Ear Headphones]] — single-driver side-opening enclosure, Helmholtz-tuned; 7.6 dB normalized leakage reduction over 1–7 kHz
