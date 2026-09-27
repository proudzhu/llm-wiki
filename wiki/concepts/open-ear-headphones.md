---
type: concept
created: 2026-09-27
updated: 2026-09-27
sources:
  - raw/papers/watanabe-2026-low-frequency-harmonic-control/full-text.md
tags:
  - open-ear-headphones
  - hearables
  - audio-playback
  - speech-intelligibility
---

# Open-Ear Headphones

**Open-ear headphones** are wearable audio devices whose design does not occlude the ear canal — sitting outside or barely touching the ear (e.g., near-ear conductors, air-conduction open designs) — providing breathability and long-term comfort. Because the ear canal stays open, they have relatively high **acoustic transparency**: real-world sounds can be heard clearly alongside (or mixed with) the device's playback.

## Signal-Processing Consequences

The unoccluded design drives two coupled constraints that shape all processing on such devices:

1. **Weak low-frequency output**: to achieve the unoccluded form factor, open-ear headphones employ small speaker units. The smaller the speaker, the higher its lowest resonant frequency, and the weaker its output below resonance. Example (Watanabe et al. 2026): the "nwm wired" open-ear earphone has its lowest resonance near 290 Hz, with sharply attenuated output below.
2. **Unattenuated ambient noise enters freely**: the same openness that provides transparency means environmental noise reaches the ear unimpeded. Urban and bustle noise — with large low-frequency components (−6 dB/oct. Brown-like tilt) — masks the already-weak low-frequency playback.

The combined effect: when real-world noise is loud, open-ear playback becomes difficult to hear, especially in the low-frequency range. Remedies must avoid naive low-frequency amplification (speaker distortion; nonlinear-distortion compensation is too complex for the small in-device DSP), and any processing must be lightweight for real-time use (e.g., web conferencing) on the in-housing DSP.

Approaches addressing these constraints include [[concepts/low-frequency-harmonic-control|Low-Frequency Harmonic Control]] (reallocate harmonic energy rather than amplify), open-ear ANC (see [[synthesis/application-specific-anc|application-specific ANC]]), and perceptual equalization against ambient noise.

## Relation to Related Device Classes

- Unlike sealed headphones with a [[concepts/transparency-mode|transparency mode]] (which uses microphones and processing to *synthesize* openness), open-ear devices are passively transparent; their challenge is making *playback* intelligible, not replicating ambient sound.
- They are the consumer-audio analog of open hearing-aid fittings, where [[concepts/open-fitting-noise-leakage|open-fitting noise leakage]] similarly lets ambient noise bypass all processing.
- They form one hardware class within [[concepts/hearables|hearables]], which also covers sealed earbuds with ANC and sensing.

## Related Concepts

- [[concepts/low-frequency-harmonic-control|Low-Frequency Harmonic Control]]
- [[concepts/hearables|Hearables]]
- [[concepts/transparency-mode|Transparency Mode]]
- [[concepts/open-fitting-noise-leakage|Open-Fitting Noise Leakage]]
- [[concepts/ear-canal-occlusion-effect|Ear-Canal Occlusion Effect]]

## Related Sources

- [[sources/watanabe-2026-low-frequency-harmonic-control|Watanabe et al. 2026: Low-Frequency Harmonic Control for Speech Intelligibility in Open-Ear Headphones]]
