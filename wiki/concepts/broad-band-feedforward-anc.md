---
type: concept
created: 2026-04-10
updated: 2026-10-31
sources:
  - raw/papers/zhang-2026-feedback-path-mitigation-mcanc/full-text.md
  - raw/papers/zhang-2020-coherence-mcanc-noise-reduction/full-text.txt
  - raw/papers/chiba-2027-wideband-anc-coaxial-loudspeaker/full-text.txt
  - raw/papers/forster-2022-optimal-microphone-positioning/full-text.txt
tags:
- active-noise-control
- broad-band
- feedforward
---

# Broad-Band Feedforward ANC

## Overview

**Broad-band feedforward ANC** is the most common ANC architecture. It uses a **reference sensor** placed upstream of the noise source to capture the primary noise before it reaches the cancellation zone, giving the controller time to compute the appropriate anti-noise signal.

## Architecture

```
Primary noise → [Reference mic] → x(n) → [ANC Controller W(z)] → y(n) → [Loudspeaker]
                                                    ↓
Primary path P(z)                                Error mic → e(n)
```

The reference signal x(n) is processed by the adaptive controller to drive a loudspeaker that emits anti-noise.

## Causality Requirement

The **electrical delay** (processing time) must not exceed the **acoustic delay** from the reference microphone to the canceling loudspeaker. If this condition is violated:

- The controller response is **noncausal**
- The system can only effectively control **narrow-band or periodic noise** (not broad-band random noise)

## Optimal Transfer Function

The adaptive filter must simultaneously model the primary path and inverse-model the secondary path:

```
W(z) = P(z) / S(z)
```

where:
- **P(z)** = primary path (acoustic response from reference sensor to error sensor)
- **S(z)** = secondary path (D/A → reconstruction filter → amplifier → loudspeaker → acoustic path → error mic → preamp → anti-alias filter → A/D)

## Filtered-X LMS

The [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] is the standard adaptive algorithm because the standard LMS becomes unstable when S(z) is present in the loop.

## Performance

The maximum noise reduction depends on the **coherence** between reference and primary noise signals:

```
NR_max(f) = -10·log₁₀[1 - γ²_xd(f)]
```

High coherence at frequencies with significant disturbance energy is essential.

The multi-reference generalization is the [[concepts/multiple-coherence-function|Multiple Coherence Function (MCF)]]: the fraction of disturbance power linearly explainable by all $J$ references, bounding attenuation at $-10\log_{10}(1-\eta_{ud}^2)$. [[sources/forster-2022-optimal-microphone-positioning|Forster, Fabry & Jax 2022]] note that this bound ignores causality — on their 12-microphone headphone it credits contralateral references that causal filters cannot actually exploit (see [[concepts/reference-microphone-positioning|Reference Microphone Positioning]]).

For the fully general multichannel case ($P$ references, $L$ sources, $Q$ error microphones), [[sources/zhang-2020-coherence-mcanc-noise-reduction|Zhang et al. 2020]] show the bound decomposes into parallel eigen channels: per channel, the multiple coherence between the projected primary signal and the reference eigen components sets the coherence floor $E_{T1}$, while the secondary-path rank adds a null-space floor $E_{T3}$ when $Q > \mathrm{rank}(\mathbf{G})$ — see [[concepts/anc-nr-potential-decomposition|ANC NR-Potential Decomposition]]. The single-channel formula above is the scalar special case.

## Feedback Problem

The anti-noise radiates **upstream** to the reference microphone, corrupting the reference signal. Solutions include [[acoustic-feedback|Acoustic Feedback]] neutralization, adaptive IIR filters, or using a sufficiently high-order FIR filter.

## Secondary-Path Delay as the Broadband Bottleneck (Chiba et al. 2027)

For open-ear headphones — where passive attenuation does not relax the requirement above ~1 kHz — the broadband reach is set by the **secondary-path delay budget**: electronic (reducible to tens of µs) + acoustic propagation + loudspeaker mechanical group delay (elevated near the compact driver's resonance in the hundreds of Hz). [[sources/chiba-2027-wideband-anc-coaxial-loudspeaker|Chiba et al. 2027]] show that a [[concepts/coaxial-two-way-secondary-source|coaxial 2-way secondary source]] with [[concepts/delay-oriented-driver-allocation|delay-oriented driver allocation]] extends the controlled band: 8.01 dB band-limited pink-noise reduction over 100–2000 Hz (dual-filter, background placement) versus 5.94 dB for the best single driver, at a 104 µs electronic delay with 3 reference microphones per ear. Their delay sweep confirms the classic expectation quantitatively: added delay degrades the 500 Hz–1 kHz octave bands most (where mechanical delay already consumes the margin), and at ≥ ~190 µs added electronic delay the two-driver advantage collapses — broadband feedforward ANC needs low-delay electronics *and* low-delay acoustics together.

## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[narrow-band-feedforward-anc|Narrow-Band Feedforward ANC]]
- [[acoustic-feedback|Acoustic Feedback]]
- [[multi-channel-anc|Multi-Channel ANC]]
- [[concepts/multiple-coherence-function|Multiple Coherence Function (MCF)]]
- [[concepts/anc-nr-potential-decomposition|ANC NR-Potential Decomposition]] — the multichannel closed form of the coherence limit

## Related Sources

- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] — Section II: Broad-Band Feedforward ANC, FXLMS derivation
- [[sources/zhang-2026-feedback-path-mitigation-mcanc|Zhang, Abhayapala, Samarasinghe & Bastine 2026: Acoustic Feedback Path Mitigation for Multichannel ANC]]
- [[sources/chiba-2027-wideband-anc-coaxial-loudspeaker|Chiba, Kamado, Kako & Noguchi 2027: Wideband ANC for Open-Ear Headphones with a Coaxial Loudspeaker]] — broadband feedforward reach as a secondary-path delay budget; driver-band allocation on a 2-way coaxial secondary source
- [[sources/forster-2022-optimal-microphone-positioning|Forster, Fabry & Jax 2022: Optimal Microphone Positioning for Multi-Channel Feedforward ANC Headphones]] — multi-reference coherence bound meets causality: MCF vs. MSE-TD CF as placement criteria
- [[sources/zhang-2020-coherence-mcanc-noise-reduction|Zhang, Murata, Maeno, Samarasinghe, Abhayapala & Mitsufuji 2020: Coherence-Based Performance Analysis on Noise Reduction in Multichannel ANC]] — proves the single-channel coherence limit is the scalar case of its three-term residual-energy decomposition

## Related Entities

- [[entities/sen-m-kuo|Sen M. Kuo]] — Author of the definitive FXLMS derivation
- [[entities/dennis-r-morgan|Dennis R. Morgan]] — Derived the FXLMS algorithm independently
