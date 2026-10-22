---
type: concept
created: 2026-09-27
updated: 2026-10-22
sources:
  - raw/papers/watanabe-2026-low-frequency-harmonic-control/full-text.md
  - raw/papers/yuan-2026-open-ear-anc-smart-glasses/full-text.md
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

## Open-Ear ANC

The unoccluded design also long made **ANC seem infeasible** on open-ear devices: with no in-ear error microphone, no adaptation loop can close at the ear, and the secondary path from a frame-mounted speaker to the ear canal varies strongly across wearers. [[sources/yuan-2026-open-ear-anc-smart-glasses|Yuan, Liu & Xiao 2026]] demonstrate the first working ANC on open-ear smart glasses by replacing the physical error sensor with [[concepts/virtual-in-ear-sensing|virtual in-ear sensing]]: a network estimates the in-ear residual from 8 frame microphones and regenerates 2048-tap control filters every 200 ms, with a per-user ESS secondary-path calibration (+1.6 dB, 9.6→11.2 dB mean reduction over 100–1000 Hz) absorbing anatomical variability. This complements the playback-intelligibility goal of LFHC: ANC removes the masking noise so that the weak low-frequency playback remains audible.

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
- [[concepts/virtual-in-ear-sensing|Virtual In-Ear Sensing]] — replaces the missing in-ear error microphone for open-ear ANC

## Related Sources

- [[sources/watanabe-2026-low-frequency-harmonic-control|Watanabe et al. 2026: Low-Frequency Harmonic Control for Speech Intelligibility in Open-Ear Headphones]]
- [[sources/yuan-2026-open-ear-anc-smart-glasses|Yuan, Liu & Xiao 2026: Active Noise Cancellation on Open-Ear Smart Glasses]] — first working open-ear ANC: virtual in-ear sensing replaces the in-ear error microphone, 11.2 dB mean reduction (100–1000 Hz) with per-user calibration
