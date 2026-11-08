---
type: concept
created: 2026-11-08
updated: 2026-11-08
sources:
  - raw/papers/huang-2026-integrated-anc-hear-through/full-text.md
tags:
  - active-noise-control
  - hear-through
  - transparency-mode
  - speech-clarity
  - in-ear-headphones
---

# Acoustic Equalization System (AES)

**Acoustic Equalization System (AES)** — introduced by [[entities/chong-rui-huang|Chong-Rui Huang]], [[entities/cheng-yuan-chang|Cheng-Yuan Chang]], and [[entities/sen-m-kuo|Sen M. Kuo]] ([[sources/huang-2026-integrated-anc-hear-through|Huang, Chang & Kuo 2026]]) — is a headphone control architecture that integrates feedforward ANC and hear-through (HT) within a **single signal path**, rather than switching between mutually exclusive operating modes. Its unifying idea is **frequency-band allocation**: the ANC branch is confined below an adjustable crossover, the HT branch above it, and both can act simultaneously with independently tunable gains.

## Architecture

The synthesized output combines two parallel branches driven by the same external-microphone reference $x(n)$:

$$E(z) = D(z) + S(z) \, [\, g_h H(z) C(z) + g_a \tilde{W}(z) L(z) \,] X(z)$$

| Component | Role | Realization |
|:----------|:-----|:------------|
| $\tilde{W}(z)$ | Feedforward ANC filter (offline FxLMS-trained, balanced-truncation reduced IIR) | 50th-order IIR, 25 cascaded SOSs |
| $L(z)$ | Low-pass filter confining the ANC branch to the low-frequency band | 1st-order IIR, cutoff $f_c = 3$ kHz |
| $H(z)$ | Hear-through filter compensating passive isolation (analytically derived, low-order) | 350-tap FIR |
| $C(z)$ | Bandpass shaping filter confining the HT branch | 6th-order IIR, $f_L$–4 kHz ($f_L$ adjustable 300–700 Hz) |
| $g_a \in [0,1]$ | User gain for ANC strength (larger in low-frequency-dominated environments, e.g. aircraft cabins) | scalar |
| $g_h \in [0,1]$ | User gain for ambient-sound transparency (larger outdoors) | scalar |

Three operating modes emerge from the gains alone: **ANC** ($g_h=0$), **HT** ($g_a=0$), and **ANC+HT** (both free) — mode switching is replaced by continuous blending, and the eardrum response targets $e(t) \approx \hat{s}(t)$ (desired sound restored, low-frequency noise removed) in the integrated mode.

## Design Rationale

- **Passive-isolation-anchored band allocation**: measured passive isolation of an in-ear headphone is ineffective below ~500 Hz (so active control is needed there), significant and DOA-stable from 500 Hz–4 kHz (so HT compensation is reliable there), and DOA-sensitive above 4 kHz (so HT compensation is deliberately limited).
- **Causality/compute awareness**: fixed filters trained offline (no on-line adaptation loop), 37 μs hardware group delay, and a 24× multiplication reduction from balanced truncation (see [[concepts/balanced-truncation-model-reduction|Balanced Truncation Model Reduction]]) — compatible with the short reference-mic-to-loudspeaker path of in-ear headphones.
- **Tunable trade-off**: $g_a$, $g_h$, and the crossover $f_L$ let users trade noise reduction against environmental awareness per acoustic environment, rather than accepting a fixed factory tuning.

## Relation to Other Integrated Approaches

The AES is the fixed-filter, band-allocated counterpart of other unified controllers: [[sources/serizel-2010-integrated-anc-nr-hearing-aids|Serizel et al. 2010]] integrate ANC with statistical noise reduction (FxMWF) for open-fitting hearing aids, and [[sources/rao-2026-keep-speech-anc|Rao et al. 2026]] achieve speech preservation via a neural reference-enhancement front end — whereas the AES keeps the conventional filter structure and obtains speech selectivity from the spectral band allocation alone.

## Related Concepts

- [[concepts/hear-through-frequency-band-allocation|Hear-Through Frequency-Band Allocation]]
- [[concepts/transparency-mode|Transparency Mode]]
- [[concepts/feedforward-anc|Feedforward ANC]]
- [[concepts/speech-preserving-anc|Speech-Preserving ANC]]
- [[concepts/balanced-truncation-model-reduction|Balanced Truncation Model Reduction]]
- [[concepts/causality|Causality in ANC]]

## Related Sources

- [[sources/huang-2026-integrated-anc-hear-through|Huang, Chang & Kuo 2026: Integrated ANC and Hear-Through for Speech Clarity]]
