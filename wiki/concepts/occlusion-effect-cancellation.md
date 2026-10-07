---
type: concept
created: 2026-10-07
updated: 2026-10-07
sources:
  - wiki/sources/liebich-2022-occlusion-effect-cancellation.md
tags:
  - active-noise-control
  - occlusion-effect
  - hear-through
  - feedback-control
  - headphones
  - hearing-aids
---

# Occlusion Effect Cancellation

**Occlusion Effect Cancellation (OEC)** is the active compensation of the [[concepts/ear-canal-occlusion-effect|ear canal occlusion effect]] using the same digital signal processing machinery as [[concepts/active-noise-control|Active Noise Cancellation]] (ANC) — a combined feedforward-feedback control structure with an inner (in-ear) and an outer microphone, operating at ultra-low latency (20–40 μs). While ANC targets *silence* (maximum attenuation of ambient sound), OEC targets *natural own-voice perception*: it must balance attenuating amplified body-conducted (BC) sound against restoring attenuated air-conducted (AC) sound.

## Problem Decomposition

The occlusion effect splits into two subproblems addressed by the two control components:

| Symptom | Frequency range | Component | Sensor |
|---------|----------------|-----------|--------|
| Amplified body-conducted sound (own voice, chewing) | mainly < 700 Hz | Feedback controller $K(z)$ | Inner microphone |
| Attenuated air-conducted sound | mainly > 1 kHz | Hear-through feedforward filter $W(z)$ | Outer microphone |

Passive alternatives (vents/open fittings, deep insertion) trade the occlusion effect for acoustic feedback risk, leakage, limited gain, or physical discomfort.

## Key Formulations

### Overall Transfer Function with Correction Filter

The distinctive structure of Liebich & Vary inserts a **correction filter** $\hat{G}(z) = G(z)$, driven by the hear-through signal $u_W(n)$, into the feedback controller input:

$$E = \underbrace{X\left(\frac{P}{1 + KG}\right)}_{\text{primary AC}} - \underbrace{X\left(GW\frac{1 + K\hat{G}}{1 + KG}\right)}_{\text{equalized AC}} + \underbrace{D_{\mathrm{BC}}\left(\frac{1}{1 + KG}\right)}_{\text{BC contr.}}$$

For $\hat{G} = G$ the hear-through filter and feedback controller designs are **decoupled** — the principal advantage over Kuo's hybrid correction (whose correction filter is driven by the control signal $u(n)$ and alters the feedback loop, requiring a different controller).

### Filter Designs

- **Feedback controller** $K(z)$: robust $\mathcal{H}_\infty$ mixed-sensitivity synthesis under secondary-path uncertainty; the [[concepts/sensitivity-function|sensitivity function]] $S(z) = \frac{1}{1+GK}$ should approximate the *inverse occlusion function* over 50–700 Hz. The unavoidable amplification at 1.5–4 kHz is the [[concepts/waterbed-effect|waterbed effect]].
- **Hear-through filter** (transparent transmission target $\frac{E}{X} \stackrel{!}{=} z^{-\tau}$):

$$W(z) = \frac{P(z)S(z) - z^{-\tau}}{G(z)}$$

realized as a causal FIR approximation via the Wiener-Hopf equation. Qualitatively $W(z)$ inverts the primary path, re-amplifying the attenuated AC components (see [[concepts/transparency-mode|Transparency Mode]]).

### Adaptive Factor α

An adaptive factor scales the loop gain (sensitivity $S_\alpha = \frac{1}{1 + G\alpha K}$) from the normalized cross-correlation between the corrected error signal and an estimated compensation signal (IIR-smoothed, $\beta = 0.999$ at 48 kHz):

$$\alpha = 1 - \hat{\Psi}_{e\hat{y}}(n), \quad 0 \leq \alpha \leq 2$$

$0 \leq \alpha < 1$ improves stability; $1 < \alpha \leq 2$ increases performance.

### Switching Between ANC and OEC

The same structure supports both modes by exchanging filter coefficients:

| Filter | ANC mode | OEC mode |
|--------|----------|----------|
| $W(z)$ | $P(z)/G(z)$ | $(P(z)S(z) - z^{-\tau})/G(z)$ |
| $K(z)$ | $K_{\mathrm{ANC}}(z)$ (max attenuation) | $K_{\mathrm{OEC}}(z)$ (inverse occlusion function) |
| $\hat{G}(z)$ | 0 | $G(z)$ |

## Key Empirical Findings (Liebich & Vary 2022)

- **Feedback control alone is insufficient**: only the feedback component improved own-voice naturalness marginally (Δη = 0.37, p < 0.0127); hear-through alone achieved Δη = 1.02; the combination reached Δη = 1.59, and individually tuned FB+HT reached Δη = 1.67 (22/23 participants preferred it over the passive earplug).
- Objective occlusion functions $\widetilde{OE}(f)$ become nearly spectrally flat with the tuned full system — both low-frequency amplification and high-frequency attenuation compensated.
- The combined feedforward-feedback ANC mode of the same hardware performs comparably to commercial solutions (stronger than Bose electronics in 330–700 Hz).

## Related Concepts

- [[concepts/ear-canal-occlusion-effect|Ear Canal Occlusion Effect]]
- [[concepts/transparency-mode|Transparency Mode]] — hear-through as the feedforward component
- [[concepts/hybrid-anc|Hybrid ANC]] — shared feedforward-feedback architecture
- [[concepts/sensitivity-function|Sensitivity Function]]
- [[concepts/waterbed-effect|Waterbed Effect]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/robust-control|Robust Control]]
- [[concepts/open-fitting-noise-leakage|Open-Fitting Noise Leakage]] — the passive alternative's cost

## Related Sources

- [[sources/liebich-2022-occlusion-effect-cancellation|Liebich & Vary 2022: Occlusion Effect Cancellation in Headphones and Hearing Devices]]
