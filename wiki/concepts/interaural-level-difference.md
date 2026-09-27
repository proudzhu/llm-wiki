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

# Interaural Level Difference (ILD)

The **interaural level difference** (ILD) is the difference in sound level (dB) between the two ears, produced by head shadowing and diffraction: the far ear is acoustically shielded by the head, especially at high frequencies. Together with the [[concepts/interaural-time-difference|interaural time difference]] (ITD), it provides the main binaural cues for horizontal sound localization, dominating at high frequencies where head shadowing is strong.

## Role in Binaural Sound Extraction

In [[concepts/binaural-target-sound-extraction|binaural target sound extraction]], preserving the ILD of target sounds requires the system to maintain the *relative gains* of the two output channels. Veluri et al. (2023) report that:

- Their jointly-processed dual-channel framework achieves ΔILD of 0.88 dB, outperforming parallel (1.08 dB) and independent single-channel (1.32 dB) frameworks, because a shared latent representation maintains inter-channel amplitude relations.
- Scale-sensitive SNR training losses are essential: SI-SNR (scale-invariant) permits one channel's gain to collapse relative to the other — their Conv-TasNet baseline trained with 90% SNR + 10% SI-SNR loss produced a near-silent channel, making ΔILD infinite while the spectrum remained meaningful.

## Related Concepts

- [[concepts/interaural-time-difference|Interaural Time Difference (ITD)]]
- [[concepts/head-related-transfer-function|Head-Related Transfer Function (HRTF)]]
- [[concepts/binaural-target-sound-extraction|Binaural Target Sound Extraction]]
- [[concepts/sound-source-localization|Sound Source Localization]]

## Related Sources

- [[sources/veluri-2023-semantic-hearing|Veluri et al. 2023: Semantic Hearing]]
