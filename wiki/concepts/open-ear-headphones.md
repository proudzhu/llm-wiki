---
type: concept
created: 2026-09-27
updated: 2026-11-12
sources:
  - raw/papers/watanabe-2026-low-frequency-harmonic-control/full-text.md
  - raw/papers/yuan-2026-open-ear-anc-smart-glasses/full-text.md
  - raw/papers/chiba-2027-wideband-anc-coaxial-loudspeaker/full-text.txt
  - raw/papers/chiba-2026-open-back-enclosure-leakage/full-text.md
tags:
  - open-ear-headphones
  - hearables
  - audio-playback
  - speech-intelligibility
  - sound-leakage
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

A complementary, **hardware-side** route addresses the causality bottleneck directly: [[sources/chiba-2027-wideband-anc-coaxial-loudspeaker|Chiba et al. 2027]] equip the nwm ONE open-ear headphone with a [[concepts/coaxial-two-way-secondary-source|coaxial 2-way secondary source]] (35 mm woofer + forward-mounted 12 mm tweeter) and apply [[concepts/delay-oriented-driver-allocation|delay-oriented driver allocation]] — the woofer controls low frequencies where its lower fundamental resonance (≈150 Hz) gives smaller mechanical group delay, the tweeter controls higher frequencies where its ≈6 µs acoustic path beats the woofer's ≈44 µs. In a measured-path offline evaluation this raised broadband pink-noise reduction over 100–2000 Hz from 5.94 dB (best single driver) to 8.01 dB at 104 µs electronic delay. Notably, this design assumes an error microphone at the ear-canal entrance (as in Serizel-style hearing-aid ANC) — the acoustic-domain complement to Yuan et al.'s sensing-domain solution.

## Sound Leakage

The same openness that keeps playback transparent also radiates it outward: the gap between enclosure and ear canal is an exit for audio, so [[concepts/sound-leakage|sound leakage]] — playback audible to bystanders — is structural rather than incidental. Two properties of the open form factor define the design problem. First, leakage is *not* a defect of one component: suppressing it by brute force (sealing, adding loudspeakers, DSP arrays) destroys the transparency, lightness, and cost advantages that motivate the form factor. Second, the constraint is frequency-shaped — long wavelengths relative to the enclosure permit interference-based suppression below ~7 kHz, short ones do not.

The passive route works with the driver rather than against it: [[sources/chiba-2026-open-back-enclosure-leakage|Chiba, Kako & Harada 2026]] vent the **single** driver's own rear (opposite-phase) radiation through four Helmholtz-tuned side-openings, giving the enclosure a [[concepts/dipole-acoustic-radiation|dipole]] pattern — loud along the near field and weak in the far field. The [[concepts/open-back-enclosure|back air cavity]] supplies the group delay and high-frequency roll-off the cancellation needs, tunable by opening width alone. On a dummy head this cut listening-level-normalized leakage by 7.6 dB vs. a sealed enclosure and 7.3 dB vs. a back-opening one over 1,000–7,000 Hz, while preserving the low-frequency listening level through the dipole proximity effect. Above ~7 kHz the sealed enclosure leaks less, so the open-back advantage is deliberately band-limited.

This is the mirror image of [[concepts/open-fitting-noise-leakage|open-fitting noise leakage]] in hearing aids: there, ambient noise enters through the open fitting and must be cancelled actively at the tympanic membrane; here, playback exits and is cancelled passively in the radiation field. Both are the price of not occluding the ear.

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
- [[concepts/coaxial-two-way-secondary-source|Coaxial Two-Way Secondary Source]] — hardware-side route: complementary woofer/tweeter delays for wideband open-ear feedforward ANC
- [[concepts/delay-oriented-driver-allocation|Delay-Oriented Driver Allocation]] — design principle assigning control bands to drivers by delay characteristics
- [[concepts/sound-leakage|Sound Leakage]] — the outward-radiation cost of the open form factor
- [[concepts/open-back-enclosure|Open-Back Enclosure]] — passive single-driver answer: vented rear radiation as a Helmholtz-tuned dipole
- [[concepts/dipole-acoustic-radiation|Dipole Acoustic Radiation]] — the near/far-field split that lets leakage be cut without losing listening level

## Related Sources

- [[sources/watanabe-2026-low-frequency-harmonic-control|Watanabe et al. 2026: Low-Frequency Harmonic Control for Speech Intelligibility in Open-Ear Headphones]]
- [[sources/yuan-2026-open-ear-anc-smart-glasses|Yuan, Liu & Xiao 2026: Active Noise Cancellation on Open-Ear Smart Glasses]] — first working open-ear ANC: virtual in-ear sensing replaces the in-ear error microphone, 11.2 dB mean reduction (100–1000 Hz) with per-user calibration
- [[sources/chiba-2027-wideband-anc-coaxial-loudspeaker|Chiba, Kamado, Kako & Noguchi 2027: Wideband ANC for Open-Ear Headphones with a Coaxial Loudspeaker]] — hardware-side wideband open-ear feedforward ANC via a delay-budgeted coaxial woofer/tweeter secondary source (8.01 dB over 100–2000 Hz)
- [[sources/chiba-2026-open-back-enclosure-leakage|Chiba, Kako & Harada 2026: Designing an Open-Back Enclosure to Mitigate Sound Leakage for Open-Ear Headphones]] — passive leakage mitigation: single-driver Helmholtz-tuned side-openings, 7.6 dB normalized leakage reduction over 1–7 kHz
