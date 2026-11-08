---
type: concept
created: 2026-11-08
updated: 2026-11-08
sources:
  - raw/papers/huang-2026-integrated-anc-hear-through/full-text.md
tags:
  - active-noise-control
  - hear-through
  - speech-clarity
  - model-order-reduction
  - in-ear-headphones
---

# Hear-Through Frequency-Band Allocation

**Hear-through frequency-band allocation** is the design methodology introduced by [[sources/huang-2026-integrated-anc-hear-through|Huang, Chang & Kuo 2026]] for dividing the audible spectrum between an ANC branch and a hear-through (HT) branch in an integrated headphone controller (their [[concepts/acoustic-equalization-system|AES]]). Instead of treating noise suppression and ambient-sound preservation as competing objectives over the full band, each is assigned the frequency region where the *physics of passive isolation* makes it reliable.

## The Allocation Rule

The bands are anchored to measured passive isolation (open-ear condition as 0 dB reference, KEMAR right ear, DOA sweep $0^\circ$–$315^\circ$ in $45^\circ$ steps):

| Band | Range | Justification |
|:-----|:------|:--------------|
| **ANC band** | ~100–500 Hz (nominal; crossover $f_L$ adjustable 300–700 Hz) | Passive isolation ineffective below ~500 Hz — active control needed; also the dominant region of low-frequency environmental noise (aircraft cabins etc.) |
| **HT band** | 500 Hz–4 kHz | Passive isolation significant but DOA-stable — compensation with a fixed filter is reliable across incidence directions |
| **Above 4 kHz** | no HT compensation | Acoustic response increasingly DOA-sensitive — compensating with a fixed filter would amplify excessively at unmodeled directions |

The key measurement: passive isolation is "relatively ineffective below 500 Hz" while exhibiting "relatively limited variation across the measured DOAs" from 500 Hz–4 kHz — so the crossover sits where isolation *starts working*, and the HT ceiling sits where DOA variability *starts growing*.

## Why It Is a Trade-Off, Not a Separation

The authors are explicit that this is "a practical engineering approximation rather than a strict spectral separation between speech and noise":

- Voiced-speech fundamental-frequency and harmonic components overlap the ANC band — the ANC branch necessarily suppresses some speech energy.
- Perceptually important consonant cues (fricatives, plosives) extend beyond the 4 kHz HT ceiling.

The crossover $f_L$ is therefore an explicit **tunable parameter**: its appropriate value depends on the spectral relationship between desired speech and ambient noise in the current environment. A beneficial side effect in low-frequency-dominated environments: suppressing dominant low-frequency noise also reduces its upward spread of masking on higher-frequency speech components.

## Robustness Across DOA

With $f_L = 700$ Hz (extended ANC band), the integrated ANC+HT mode shows attenuation below 700 Hz that *varies with DOA but remains noticeable for all DOAs*, while the HT band stays close to the open-ear condition from 700 Hz–4 kHz across DOAs. The allocation thus inherits feedforward ANC's DOA dependence below the crossover but keeps the HT branch DOA-robust — see [[concepts/feedforward-anc|Feedforward ANC]] (DOA dependency discussion).

## Related Concepts

- [[concepts/acoustic-equalization-system|Acoustic Equalization System (AES)]]
- [[concepts/transparency-mode|Transparency Mode]]
- [[concepts/feedforward-anc|Feedforward ANC]]
- [[concepts/speech-preserving-anc|Speech-Preserving ANC]]

## Related Sources

- [[sources/huang-2026-integrated-anc-hear-through|Huang, Chang & Kuo 2026: Integrated ANC and Hear-Through for Speech Clarity]]
