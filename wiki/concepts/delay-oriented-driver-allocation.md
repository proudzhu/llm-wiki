---
type: concept
created: 2026-10-24
updated: 2026-10-24
sources:
  - raw/papers/chiba-2027-wideband-anc-coaxial-loudspeaker/full-text.txt
tags:
  - active-noise-control
  - causality
  - secondary-path-delay
  - loudspeaker-design
---

# Delay-Oriented Driver Allocation

**Delay-oriented driver allocation** is a design principle for causality-limited broadband feedforward ANC that assigns different frequency bands of the control bandwidth to different loudspeaker drivers according to their **delay characteristics** — rather than their amplitude response alone, as in a conventional audio crossover. Introduced by [[sources/chiba-2027-wideband-anc-coaxial-loudspeaker|Chiba et al. 2027]] for open-ear headphones.

## The Delay Budget

The secondary-path group delay is decomposed as a design budget:

$$\tau_S(f) = \underbrace{\tau_S^E(f)}_{\text{electronic}} + \underbrace{\tau_S^A(f)}_{\text{acoustic}} + \underbrace{\tau_S^M(f)}_{\text{mechanical}}$$

- **Electronic delay** (ADC/DAC, DSP): reducible to tens of µs with oversampling and low-delay conversion
- **Acoustic delay** $\approx l/c$: set by the driver-to-ear distance $l$
- **Mechanical delay**: rises sharply near and below the driver's fundamental resonance $f_0$ (mass–spring group-delay concentration) — compact drivers have $f_0$ of several hundred Hz, so this term is elevated exactly in the band where open-ear ANC is most needed

A single compact driver cannot minimize both acoustic and mechanical delay across a wide band: a large diaphragm (low $f_0$, low mechanical delay) needs source-to-ear distance for acoustic transparency (high acoustic delay), while a small forward-mounted driver has short acoustic delay but high $f_0$.

## Allocation Principle

Allocate each frequency band to the driver with the smaller budget at that frequency:

$$\tau_{\min}(f) = \min(\tau_{S,W}(f), \tau_{S,T}(f))$$

In [[concepts/coaxial-two-way-secondary-source|coaxial 2-way designs]], the woofer is favored at low frequencies (lower $f_0 \approx 150$ Hz → smaller mechanical delay) and the tweeter at higher frequencies (forward placement → ≈6 µs vs ≈44 µs acoustic delay; mechanical terms equalize above ~1 kHz). Representative budgets (500 Hz): woofer ≈ 206 µs subtotal vs tweeter ≈ 418 µs; at 1 kHz the ordering flips (woofer ≈ 106 µs vs tweeter ≈ 68 µs).

## Design Sequence

1. Measure each driver's amplitude response and mechanical group delay in isolation (e.g., JIS C 5532 standard enclosure, subtracting the measurement-distance propagation delay)
2. Estimate the source-to-ear acoustic propagation delay from geometry
3. Include crossover-filter group delay and the electronic-delay budget
4. Select driver bands and filter placement according to the remaining [[concepts/causality|causality]] margin — prefer background (adaptation-path-only) filter placement when output-path causality margin is the dominant constraint; a single-filter composite-path architecture when computation/ storage dominates and crossover delay is acceptable

## Scope and Caveats

- The budget is a **design interpretation**, not an exact decomposition of non-minimum-phase worn-device paths (pinna, reflections) — worn-path group delay cannot be split back into components.
- Allocation complements, but does not replace, low-delay electronics: at large electronic delays (≥ ~190 µs added in the 2027 study), the mid-band advantage of two-driver allocation largely collapses.
- Distinct from vehicle woofer+tweeter arrays (e.g., engine-order cancellation up to 1 kHz), where each secondary source operates over the same range without delay-based band splitting.

## Related Concepts

- [[concepts/coaxial-two-way-secondary-source|Coaxial Two-Way Secondary Source]]
- [[concepts/causality|Causality in ANC]]
- [[concepts/feedforward-anc|Feedforward ANC]]
- [[concepts/open-ear-headphones|Open-Ear Headphones]]
- [[concepts/anc-attenuation-bounds|ANC Attenuation Bounds]]

## Related Sources

- [[sources/chiba-2027-wideband-anc-coaxial-loudspeaker|Chiba, Kamado, Kako & Noguchi 2027: Wideband ANC for Open-Ear Headphones via Low-Delay Acoustic Design with a Coaxial Loudspeaker]]
