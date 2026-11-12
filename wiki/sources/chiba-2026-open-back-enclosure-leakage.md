---
type: source
created: 2026-11-12
updated: 2026-11-12
sources:
  - raw/papers/chiba-2026-open-back-enclosure-leakage/full-text.md
  - https://doi.org/10.1109/ACCESS.2025.3648340
  - zotero://select/items/0_Q4JSYTD8
tags:
  - open-ear-headphones
  - sound-leakage
  - acoustic-enclosure-design
  - dipole-radiation
  - helmholtz-resonator
  - near-field-reproduction
  - passive-acoustics
  - wearable-audio
---

# Chiba, Kako & Harada 2026: Designing an Open-Back Enclosure to Mitigate Sound Leakage for Open-Ear Headphones

**Authors**: [[entities/hironobu-chiba|Hironobu Chiba]], [[entities/tatsuya-kako|Tatsuya Kako]], [[entities/noboru-harada|Noboru Harada]]
**Affiliation**: NTT Inc., Tokyo, Japan
**Venue**: IEEE Access, vol. 14
**Year**: 2026
**Type**: Journal article
**DOI**: [10.1109/ACCESS.2025.3648340](https://doi.org/10.1109/ACCESS.2025.3648340)
**Zotero**: [Q4JSYTD8](zotero://select/items/0_Q4JSYTD8)

## Summary

Open-ear headphones avoid the occlusion effect and preserve acoustic transparency, but the open gap between enclosure and ear canal radiates sound outward — **sound leakage** — which makes them awkward in public spaces. Rather than adding speakers (the enclosure-less array approach) or DSP, this paper turns a **single** driver's own back radiation into the cancellation source: a back air cavity plus four symmetric side-openings forms an acoustic dipole whose opposite-phase wave is delayed and low-passed by a [[concepts/open-back-enclosure|Helmholtz-tuned back cavity]], so that the leaked positive-phase wave is cancelled in the far field while the dipole's near-field proximity effect preserves low-frequency level at the listener's ear. FEM (Actran) and dummy-head measurements on the five enclosure variants show the side-opening design reduces the angle-averaged, listening-level-normalized A-weighted [[concepts/sound-leakage|sound leakage]] by **7.6 dB vs. a sealed enclosure and 7.3 dB vs. a back-opening enclosure over 1,000–7,000 Hz**, with the 2.0 mm opening width best below 7 kHz.

## Problem Formulation

### Leakage as a path-mismatch cancellation problem

The sound pressure at an external observation point $r$ is the sum of the front (positive-phase) and back (opposite-phase) contributions, each being an internal enclosure path cascaded with an external radiation path:

$$Y(f,r) = H_{+,o}(f,r)H_{+,i}(f)S_+(f) + H_{-,o}(f,r)H_{-,i}(f)S_-(f)$$

Cancellation means minimizing $Y$; with $S_+(f) \approx -S_-(f)$ over the target band, the **ideal** opposite-phase internal transfer function is

$$H_{-,i}(f) = \frac{H_{+,o}(f,r)H_{+,i}(f)}{H_{-,o}(f,r)}$$

$H_{\pm,o}$ are fixed by head and pinna geometry (uncontrollable) and $H_{+,i}$ should stay $\approx 1$ to preserve listening quality, so the entire design freedom sits in $H_{-,i}$. Two requirements follow:

1. **Delay compensation** — at a leakage point behind the listener the front path is *longer* than the back path, so $H_{-,i}$ must add the corresponding delay to the opposite-phase wave.
2. **High-frequency low-pass** — above ~10 kHz the wavelength is short enough that phase-based cancellation is fragile and can turn *constructive*; $H_{-,i}$ must roll off instead of following the mismatch.

The paper's claim is that both requirements are realizable **purely mechanically**, by the geometry of the back cavity and its openings.

### Dipole near/far-field split

Modeling the front and back of the driver as two opposite-phase point sources separated by $D$, the dipole-to-monopole pressure ratio is

$$\frac{|p_u|}{|p_u^{(\text{mono})}|} = kD|\cos\theta_u|\sqrt{1+\frac{1}{k^2r_u^2}} \qquad \text{(near-field listening point } u)$$

$$\frac{|p_v|}{|p_v^{(\text{mono})}|} = kD|\cos\theta_v| \qquad \text{(far-field leakage point } v)$$

The proximity term $\sqrt{1+1/(k^2r_u^2)}$ — the pressure-gradient-microphone proximity effect — is significant only when $kr_u \ll 1$. Because the listener's ear is in that regime but the surrounding people are not, a dipole **boosts** the low frequencies where needed and **attenuates** them everywhere else, which is precisely the open-ear requirement that a monopole cannot meet.

## Methodology

### Enclosure geometry

A 20-mm-diameter cylindrical housing holds one 16.2-mm driver. Front radiation exits a 7.0-mm-diameter opening toward the ear; the back of the driver drives an air cavity of fixed volume $V \approx 583\ \mathrm{mm}^3$ that vents through **four side-openings** at 90° intervals, each 3.5 mm tall and $d$ wide, duct length $L = 1.6$ mm.

![[raw/papers/chiba-2026-open-back-enclosure-leakage/figures/94127587faedd34737f12a774d4939e96a67a739e667868922f0ab6b249ead2f.jpg|Sealed (left) vs. proposed open-back enclosure (right)]]

*Figure 1: A conventional open-ear headphone with a fully sealed enclosure (left) and the proposed enclosure (right), whose back air cavity of volume $V$ vents opposite-phase waves through side-openings of total area $S$.*

Three design decisions carry the physics:

- **Opening separation** sets the dipole length $D$: closer openings cancel harder in the far field but start cancelling in the near field too, eating the listener's low-frequency response — so an intermediate distance is optimal.
- **Opening orientation** sets the dipole axis: dipole radiation peaks *along* the axis, so side-openings put the axis roughly vertical and keep the radiation minimum in the horizontal plane where bystanders are.
- **Four-fold symmetry** averages out wearing-position and ear-shape variation rather than relying on one preferred orientation.

![[raw/papers/chiba-2026-open-back-enclosure-leakage/figures/ee4ba4a3af10a6d2e9c95d467b966b7816ed86012ac9c7d750d29f2a194691fa.jpg|Enclosure design: front and side views]]

*Figure 3: Front (left) and side (right) views. The 7.0-mm front opening radiates toward the ear; $d$ is the width of the side-openings that emit the opposite-phase wave.*

### Helmholtz tuning of the opposite-phase path

The back cavity plus its openings is a Helmholtz resonator,

$$f_H = \frac{c}{2\pi}\sqrt{\frac{S}{V(L+\delta)}}, \qquad \delta = \sqrt{S}, \qquad S \approx N_S h d$$

with $N_S = 4$ openings of height $h = 3.5$ mm. $V$ and $L$ are pinned by the enclosure envelope, leaving the **opening width $d$** as the one mechanical control knob for $f_H$. The resonator supplies exactly the two properties the ideal $H_{-,i}$ needs:

- **Rapid phase change around $f_H$** → the group delay that compensates the front/back path-length mismatch, so the two waves arrive near anti-phase;
- **Low-pass above $f_H$** → attenuation of the opposite-phase wave where cancellation is unreliable, preventing high-frequency constructive interference.

Small $d$ (low $f_H$) therefore delays earlier and rolls off earlier; large $d$ (high $f_H$) does both later. Table 1 confirms the model against FEM:

| $d$ | 2.0 mm | 4.0 mm | 6.0 mm |
|---|---|---|---|
| Theoretical $f_H$ (Eqs. 5–6) | 4,517 Hz | 5,565 Hz | 6,260 Hz |
| Simulated $f_H$ (FEM peak of opposite-phase wave) | 4,559 Hz | 5,744 Hz | 6,752 Hz |

### Five enclosure variants

$d = 0.0$ mm (sealed reference), 2.0, 4.0, 6.0 mm (side-openings), and a 4.0 mm **back-opening** model that has identical opening area and hence identical $f_H$ — isolating the effect of opening *position* from opening *area*.

![[raw/papers/chiba-2026-open-back-enclosure-leakage/figures/5fea6056b1b53d8517ecc9241d36305ca2f152d56a67f38752ab51bffb6d109b.jpg|Five enclosure models compared in simulation and measurement]]

*Figure 4 (top): the five enclosure models — sealed, side-opening $d$ = 2.0/4.0/6.0 mm, and back-opening 4.0 mm.*

![[raw/papers/chiba-2026-open-back-enclosure-leakage/figures/8b079588441129bffa68ce737f555ede46d6be949f14175ee9df8c28f15de1b1.jpg|Leakage observation geometry on a dummy head]]

*Figure 4 (middle): the enclosure mounted at the right ear of a dummy head; leakage observation points lie on a semicircular horizontal plane 150 mm behind the enclosure.*

### Evaluation metrics

Because the enclosures differ in absolute listening level, the primary metric is **listening-level-normalized** leakage. With $W_A$ the A-weighting, $L(f,\phi)$ the leakage SPL at angle $\phi$, and $L_{\text{ref}}(f)$ the SPL at the (blocked) ear-canal entrance:

$$L^{\text{norm}}_{A,\text{mean}}(f) = W_A(f) + \frac{1}{N_\Phi}\sum_{\phi\in\Phi}\big(L(f,\phi) - L_{\text{ref}}(f)\big)$$

averaged over $\phi = 0°, 15°, \dots, 180°$, then band-averaged over $F = \{1000 + 250k\ \text{Hz},\ k = 0..24\}$ — i.e. 1–7 kHz, the band where interference cancellation is viable.

## Experimental Setup

| Item | Detail |
|------|--------|
| FEM solver | Actran, 2.8 mm mesh |
| FEM excitation | Velocity FRF from an equivalent circuit fitted to the driver's amplitude response at 0.5 Vrms; back radiation assumed equal to front radiation in the simulation |
| FEM head model | Mean male head model (Digital Human Technology); ear canal blocked, so no canal/eardrum acoustics |
| Measurement room | Anechoic chamber |
| Dummy head | SAMREC 2700Pro (ear microphone provides $L_{\text{ref}}$) |
| Enclosure / jig fabrication | Formlabs Form3 SLA printer; ear-hook jig positions the 16.2-mm driver consistently |
| Excitation | Time-stretched pulse (TSP) |
| Microphone / analyzer | dbx RTA-M / APx517B with APx500 v6.0 |
| Observation grid | 0°–180° at 5° (simulation) / 15° (metric averaging), 150 mm behind the enclosure |
| Variants | Sealed ($d$ = 0), side-opening $d$ = 2/4/6 mm, back-opening 4 mm |
| Additional sweep | $d$ = 3.0 and 5.0 mm added in measurement (Appendix C) |

## Results

### Simulation (head-attached)

- Below ~4 kHz the sealed enclosure leaks **significantly more** than every open variant at all angles — the opposite-phase wave works.
- The opposite-phase level peaks and its phase **inverts near $f_H$**, bringing the pair close to anti-phase; the residual leakage peak sits exactly at resonance, where the opposite-phase wave is strongest. A lower $f_H$ both delays earlier and rolls off earlier, which helps where interference alone cannot.
- Generated listening level (Fig. 5): lowest for side-opening, then back-opening, then sealed — the ordering predicted by $D$ in the dipole model, plus a local listening-level bump at $f_H$ (the same resonance is audible to the wearer, which is why a shallow $f_H$ peak matters for timbre).
- Side-openings beat back-openings **at the same $f_H$** below 7 kHz: shorter front-to-back source separation ⇒ lower far-field level.

![[raw/papers/chiba-2026-open-back-enclosure-leakage/figures/f9c9a33a78af90bf5e49190b70e7ff2de0a3110a3c91ed42c552747354ebcb0f.jpg|Simulated leakage level and positive/negative-wave phase vs angle]]

*Figure 6: Simulated leakage for the five models at 0°/45°/90°/135°/180°, columns = mixed wave, positive wave, opposite-phase wave, and their phase difference.*

### Measurement (dummy head)

- Same qualitative ordering: the sealed enclosure leaks most below ~4 kHz at every angle; side-openings beat back-openings at high frequencies.
- The sharp resonance peaks of the simulation are **damped and broadened** in measurement — viscous losses at the openings, enclosure absorption, atmospheric absorption, and non-ideal driver behaviour above ~10 kHz. Simulation stays predictive for trends and resonance frequency below 10 kHz but not for peak heights.
- $d = 2.0$ mm gives the lowest leakage below 7 kHz in both absolute and normalized terms.
- Above 7 kHz the **sealed** enclosure leaks least: open enclosures radiate more there, and only a low $f_H$ low-pass (plus optional sound-absorbing material) suppresses it.

![[raw/papers/chiba-2026-open-back-enclosure-leakage/figures/416d16350c048ad9b8a74facadda7abaa00d6116c3a5397eaeeeee43786d1e7b.jpg|Measured leakage vs angle for the five models]]

*Figure 9: Measured leakage levels, rows = 0°/45°/90°/135°/180° behind the dummy head.*

![[raw/papers/chiba-2026-open-back-enclosure-leakage/figures/f51eaf3fdf3085ae65c29249f2ed8d7c2a74e4489144864212cdbec532f72d72.jpg|Angle-averaged leakage, simulation (left) vs measurement (right)]]

*Figure 10: Angle-averaged A-weighted leakage (top) and listening-level-normalized leakage (bottom); simulation left, measurement right.*

### Headline numbers

![[raw/papers/chiba-2026-open-back-enclosure-leakage/figures/ab212784a6d01e1d6c3bc0397fb4252c53637e8f964d115aa63e5cc71d50c6b6.jpg|Band-averaged leakage over 1–7 kHz]]

*Figure 11: Frequency-band means (1–7 kHz) of A-weighted and normalized leakage; triangles = simulation, circles = measurement, black = mean over all angles.*

| Comparison (1,000–7,000 Hz, normalized, measured) | Reduction |
|---|---|
| Side-opening $d$ = 2.0 mm **vs. sealed** ($d$ = 0) | **7.6 dB** |
| Side-opening $d$ = 2.0 mm **vs. back-opening 4.0 mm** | **7.3 dB** |
| Best model overall | $d$ = 2.0 mm side-opening (absolute and normalized) |

### Listening-path integrity

The opposite-phase path barely perturbs the wanted signal in the measured band: comparing the driver's front and back radiation (Appendix B, Table 2, 100 Hz–7 kHz) gives a median level difference of **0.35 dB** (Q1 −0.84, Q3 1.09) and a median phase difference of **179.50°** (Q1 174.04, Q3 185.64) — i.e. near-equal amplitude and near-perfect anti-phase, the assumption $S_+ \approx -S_-$ behind the whole design. Measured listening SPL does not fall off below 1 kHz, confirming the proximity-effect low-frequency boost; the residual spectral imprint of the back enclosure is small enough that equalization by the player or device DSP covers it.

![[raw/papers/chiba-2026-open-back-enclosure-leakage/figures/6df94b74cf1b57adbf651dccc5ce1cffc8b9f26c91ef4fce77afe291bf48b2e0.jpg|Measured listening-point SPL for the five models]]

*Figure 8: Measured listening-point SPL under head-attached conditions — no low-frequency droop below 1 kHz, broadened rather than sharpened resonance.*

### Sensitivity to the opening width

![[raw/papers/chiba-2026-open-back-enclosure-leakage/figures/7810040176879719c8c99ecbc62b4683fb7f8a800546ee3eb6ec52c1490528e9.jpg|Measured leakage vs opening width d = 2–6 mm]]

*Figure 14: Measured angle-averaged leakage for $d$ = 2.0, 3.0, 4.0, 5.0, 6.0 mm — the optimum and the resonance-related features shift smoothly with $d$.*

$d$ is a **continuous** tuning parameter, not a binary choice: as the width varies, both the frequency of maximum leakage reduction and the overall level move smoothly, so an enclosure can be trimmed to the intended wearing geometry without changing its size, volume, or driver.

### Dipole model validation (Appendix A/D)

![[raw/papers/chiba-2026-open-back-enclosure-leakage/figures/00b16ba17e2ab25a68f40419da69ce505fca2bd608ba1cb200971cb01982d752.jpg|Monopole vs dipole and the near/far magnitude ratios]]

*Figure 12: Monopole (a) vs dipole (b) radiation, and the listening/leakage ratios of Eqs. 1–2 versus distance, angle, and source separation.*

Free-field simulation and measurement (Appendix D) reproduce the same ordering in the absence of head/pinna effects: sealed leaks more below ~3–4 kHz, side-openings beat back-openings, and leakage grows as the observation point approaches the dipole axis at 90° — confirming the mechanism is the dipole, not a head-shadowing artifact.

## Key Contributions

1. **Single-driver passive leakage cancellation.** Introduces an [[concepts/open-back-enclosure|open-back enclosure]] — back air cavity plus four side-openings — that radiates the driver's own opposite-phase wave to cancel leakage, replacing the enclosure-less **two-driver** array of Fukui et al. with one driver and no DSP/analog electronics. The size of the enclosure need not grow.
2. **Path-mismatch formulation of leakage cancellation.** Poses the problem as matching $H_{-,i} = H_{+,o}H_{+,i}/H_{-,o}$ under $S_+ \approx -S_-$, which decomposes the acoustic design into a delay requirement and a high-frequency attenuation requirement — an explicit target for a purely mechanical design.
3. **Helmholtz resonator as the acoustic implementation of that transfer function.** Shows that the back cavity's resonance supplies both the group delay (phase rotation at $f_H$) and the required low-pass (above $f_H$), with opening width $d$ as the single tuning knob; theoretical and FEM resonance frequencies agree to within 1–8%.
4. **Quantified, listening-normalized benefit under realistic wearing.** Dummy-head measurements over 1–7 kHz: **7.6 dB** normalized leakage reduction vs. sealed and **7.3 dB** vs. back-opening at equal resonance frequency, with the side-opening/back-opening gap attributable to dipole source separation. Listening level is preserved (no sub-1 kHz droop) and the front/back radiation asymmetry is ~0.35 dB / 179.5° over 100 Hz–7 kHz.
5. **Design guidance and its limits.** Side-openings orient the dipole axis vertically to protect the horizontal plane; four-fold symmetry averages worn-position variation; the approach works up to ~7 kHz and *loses* to a sealed enclosure above it, where a lower $f_H$ and/or absorbing material is the remedy.

## Caveats

- All leakage numbers are **dummy-head** results; individual ear shape is known to modulate leakage signals (the paper cites ear-shape-based authentication from leakage), so per-user variation is unquantified.
- Simulation and measurement diverge on resonance peak height (idealized damping) and above 10 kHz (geometry detail, diaphragm breakup), so absolute peak levels are not predictable from FEM.
- No subjective/listening-test evaluation of timbre or perceived leakage; the sound-quality argument rests on SPL spectra at the blocked ear-canal entrance.
- The study is passive only — no comparison against active leakage control (Cha et al., Lee et al.) or against the two-driver enclosure-less array it generalizes.

## Related Concepts

- [[concepts/open-ear-headphones|Open-Ear Headphones]]
- [[concepts/sound-leakage|Sound Leakage]]
- [[concepts/dipole-acoustic-radiation|Dipole Acoustic Radiation]]
- [[concepts/open-back-enclosure|Open-Back Enclosure]]
- [[concepts/ear-canal-occlusion-effect|Ear-Canal Occlusion Effect]]
- [[concepts/hearables|Hearables]]
- [[concepts/coaxial-two-way-secondary-source|Coaxial Two-Way Secondary Source]] — the same research group's driver-side design for open-ear ANC
- [[concepts/active-noise-control|Active Noise Control]] — the active counterpart to passive leakage control

## Related Synthesis

- [[synthesis/modern-headphone-anc-systems|Modern Headphone ANC Systems]]
- [[synthesis/personal-sound-zones-evolution-and-optimization|Personal Sound Zones: Evolution and Optimization]]
