---
type: concept
created: 2026-10-24
updated: 2026-10-24
sources:
  - raw/papers/mezza-2024-hybrid-plc/full-text.md
tags:
  - evaluation-metric
  - audio-quality
  - perceptual-model
---

# PEAQ (ITU-R BS.1387)

**PEAQ** (Perceptual Evaluation of Audio Quality, ITU-R BS.1387) is the ITU standard for objective measurement of perceived audio quality. It compares a test signal against a reference through a psychoacoustic model (outer/middle-ear filtering, Bark-scale excitation patterns, masking, temporal pooling) and outputs a **Objective Difference Grade (ODG)** on a −4…0 scale:

| ODG | Impairment |
|-----|------------|
| 0.0 | Imperceptible |
| −1.0 | Perceptible, but not annoying |
| −2.0 | Slightly annoying |
| −3.0 | Annoying |
| −4.0 | Very annoying |

The **Basic** version uses fewer psychoacoustic features and is the one usually implemented in open-source (e.g. P. Kabal's MATLAB implementation used in [[sources/mezza-2024-hybrid-plc|Mezza et al. 2024]]); the Advanced version uses the full model plus artifactual-error descriptors.

## Use and Caveats in PLC / Music Work

PEAQ was designed to grade impairments introduced by *lossy audio codecs*, not missing-packet substitution, and the literature debates its suitability for PLC. Two practical notes from the music-PLC study of [[sources/mezza-2024-hybrid-plc|Mezza et al. 2024]]:

- PEAQ requires **48 kHz** input, so 32 kHz test material is resampled before scoring (PLCMOS analogously requires 16 kHz).
- Evaluated over non-overlapping 10-second windows, PEAQ's mean ODG tracked MUSHRA listener scores closely — Pearson $r=0.957$ ($P=1.8\times10^{-4}$) across eight PLC methods — making it the best-correlated of the four objective measures in that study, ahead of [[concepts/plcmos|PLCMOS]] ($r=0.899$).

## Related Concepts

- [[concepts/mushra-listening-test|MUSHRA Listening Test]] — subjective reference PEAQ is validated against
- [[concepts/pesq|PESQ]] — the speech-oriented analog for objective quality (ITU-T P.862)
- [[concepts/plcmos|PLCMOS]] — learned PLC-specific quality proxy
- [[concepts/packet-loss-concealment|Packet Loss Concealment]]

## Related Sources

- [[sources/mezza-2024-hybrid-plc|Mezza, Amerena, Bernardini & Sarti 2024]] — PEAQ ODG as the top-correlating objective metric; PARCnet is the only method whose segments all fall in the "perceptible but not annoying" band
