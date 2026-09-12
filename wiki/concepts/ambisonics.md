---
type: concept
created: 2026-09-09
updated: 2026-09-12
sources:
  - raw/papers/grumiaux-2022-ssl-deep-learning-survey/full-text.txt
  - raw/papers/tervo-2009-sound-intensity-direction/full-text.md
tags:
  - ambisonics
  - spatial-audio
  - microphone-array
  - sound-source-localization
---

# Ambisonics

Ambisonics is a spherical-harmonic-based spatial audio format representing a sound field independent of the recording array geometry. First-order Ambisonics (FOA) uses four components (W, X, Y, Z — omnidirectional plus three dipole axes); higher-order Ambisonics (HOA) adds spherical harmonic components of order > 1 for finer spatial resolution.

## Role in DL-based SSL

Per the Grumiaux et al. 2022 survey, Ambisonics is one of the seven input-feature families for neural [[concepts/sound-source-localization|sound source localization]]:

- **Array-agnostic representation**: because Ambisonic signals encode the sound field rather than a specific microphone layout, networks trained on them generalize across recording setups — a remedy for the array-dependence of most DL-based SSL (a key flexibility perspective of the survey).
- **Standard for DCASE SELD**: the DCASE 2019–2021 SELD datasets provide FOA format alongside tetrahedral microphone signals; many systems use FOA log-Mel spectra, FOA [[concepts/sound-intensity-vector|intensity vectors]] (active/real and reactive/imaginary), or FOA phase/IPD features.
- **Caveat**: the spatial response of Ambisonic microphones is approximately frequency-independent only within a bandwidth dictated by the HOA order — spatial aliasing at high frequencies and noise amplification at low frequencies (Zotter & Frank 2019).

HOA magnitude+phase spectrograms are also used directly as CRNN inputs (e.g. Poschadel et al. 2021).

## Related Concepts

- [[concepts/sound-source-localization|Sound Source Localization]]
- [[concepts/sel-d|SELD]]
- [[concepts/sound-intensity-vector|Sound Intensity Vector]] — FOA intensity vectors as SSL/SELD features
- [[concepts/room-impulse-response|Room Impulse Response]]

## Related Sources

- [[sources/grumiaux-2022-ssl-deep-learning-survey|Grumiaux et al. 2022: A Survey of SSL with Deep Learning Methods]]
- [[sources/tervo-2009-sound-intensity-direction|Tervo 2009: Direction Estimation Based on Sound Intensity Vectors]]

