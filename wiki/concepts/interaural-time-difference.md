---
type: concept
created: 2026-09-27
updated: 2026-09-27
sources:
  - raw/papers/veluri-2023-semantic-hearing/full-text.md
tags:
  - acoustics
  - spatial-audio
  - binaural-processing
---

# Interaural Time Difference (ITD)

The **interaural time difference** (ITD) is the difference in arrival time of a sound at the two ears, caused by the finite separation of the ears and the path-length difference around the head. Together with the [[concepts/interaural-level-difference|interaural level difference]] (ILD), it is a primary binaural cue for horizontal localization of sound sources.

## Role in Binaural Sound Extraction

In [[concepts/binaural-target-sound-extraction|binaural target sound extraction]], a target sound's ITD must be preserved in the output so listeners perceive the sound from its true direction. Veluri et al. (2023) measure ΔITD — the error between output and ground-truth ITD, computed via cross-correlation limited to ±1 ms — and report 87.77 µs for their dual-channel model (vs 670 µs for a Conv-TasNet parallel baseline). Their spatial-cue user study showed perceived-direction errors nearly unchanged relative to clean playback (median 9° vs 5°).

ITD dominates localization at low frequencies (below ~1.5 kHz, where the wavelength exceeds the head size and level differences are small); ILD dominates at high frequencies.

## Related Concepts

- [[concepts/interaural-level-difference|Interaural Level Difference (ILD)]]
- [[concepts/head-related-transfer-function|Head-Related Transfer Function (HRTF)]]
- [[concepts/binaural-target-sound-extraction|Binaural Target Sound Extraction]]
- [[concepts/sound-source-localization|Sound Source Localization]]

## Related Sources

- [[sources/veluri-2023-semantic-hearing|Veluri et al. 2023: Semantic Hearing]]
