---
type: concept
created: 2026-11-12
updated: 2026-11-12
sources:
  - raw/papers/chiba-2026-open-back-enclosure-leakage/full-text.md
tags:
  - acoustics
  - sound-radiation
  - open-ear-headphones
  - near-field
---

# Dipole Acoustic Radiation

**Dipole acoustic radiation** is the field produced by two closely spaced point sources of equal strength and opposite phase, separated by a distance $D$. For a loudspeaker it is the natural model of a driver radiating from both its front and its back when the rear wave is neither sealed nor absorbed.

Its defining property is a **near-field/far-field split**: the pressure falls off as $1/r^2$ at low $kr$ but the two sources partially cancel at large distance, so the far field is a **high-pass** radiator while the near field is boosted. Expressed as a ratio to a monopole of the same center,

$$\frac{|p_u|}{|p_u^{(\text{mono})}|} = kD|\cos\theta_u|\sqrt{1+\frac{1}{k^2 r_u^2}} \qquad \text{(near field } kr_u \ll 1)$$

$$\frac{|p_v|}{|p_v^{(\text{mono})}|} = kD|\cos\theta_v| \qquad \text{(far field)}$$

where $k$ is the wavenumber and $\theta$ the angle from the dipole axis. The factor $\sqrt{1+1/(k^2r^2)}$ is the **proximity effect** — the same term that gives pressure-gradient microphones their low-frequency boost, applied in reverse as a radiation property.

## Why It Matters for Wearables

Dipole radiation is the physical basis of [[concepts/open-back-enclosure|open-back enclosures]] and of near-field reproduction for [[concepts/open-ear-headphones|open-ear headphones]]: the wearer's ear sits inside $kr \ll 1$ (a few centimeters at audio frequencies) and receives the boosted low-frequency response, while bystanders at $r \gtrsim 0.5$ m see only the $kD|\cos\theta|$ high-pass term, so low-frequency leakage is attenuated without any signal processing or extra drivers:

- **Radiation pattern**: strongest *along* the dipole axis, minimal perpendicular to it — so the axis is oriented away from the plane containing bystanders.
- **Source separation $D$**: smaller $D$ improves far-field cancellation but starts cancelling in the near field, eating the wearer's bass; the optimum is intermediate. Chiba et al. exploit this quantitatively — a side-opening enclosure ($D$ = opening separation) beats a back-opening one with identical resonance frequency.
- **Band limit**: the $\cos\theta$ null pattern and the phase match degrade as the wavelength approaches $D$; above ~7 kHz the cancellation turns unreliable and an open-back design can leak *more* than a sealed one.

## Related Concepts

- [[concepts/open-back-enclosure|Open-Back Enclosure]]
- [[concepts/sound-leakage|Sound Leakage]]
- [[concepts/open-ear-headphones|Open-Ear Headphones]]

## Related Sources

- [[sources/chiba-2026-open-back-enclosure-leakage|Chiba, Kako & Harada 2026: Designing an Open-Back Enclosure to Mitigate Sound Leakage for Open-Ear Headphones]] — derives the near/far ratio model, validates it in free-field FEM and dummy-head measurement
