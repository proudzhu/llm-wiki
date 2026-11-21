---
type: entity
created: 2026-08-15
updated: 2026-11-21
sources:
  - raw/papers/tashev-2008-sound-capture-spatial-filter/full-text.md
tags:
  - researcher
  - speech-enhancement
  - microphone-array
  - beamforming
  - audio-signal-processing
---

# Ivan Tashev

**Affiliation**: Microsoft Research, One Microsoft Way, Redmond, WA 98052, USA
**Role**: Researcher
**Research Focus**: Microphone-array sound capture, speech enhancement and spatial filtering for small mobile devices; beamformer design and non-linear post-processing for hands-free communication.

## Key Contributions

- Lead author of "Sound Capture System and Spatial Filter for Small Devices" (2008) — proposed a back-to-back unidirectional two-microphone array (9.6 mm baseline) with a front-back-difference-maximizing beamformer and a probability-based non-linear spatial filter, achieving 10.43 dB SNR and 0.39 PESQ-MOS improvement — [[sources/tashev-2008-sound-capture-spatial-filter|Tashev et al. 2008]]
- Author of "Microphone Array for Headset with Spatial Noise Suppressor" (IWAENC 2005) — earlier spatial-noise-suppressor work cited as ref. [3] in the 2008 paper
- Author of "Microphone Array Post-Processor Using Instantaneous Direction of Arrival" (IWAENC 2006) — direct estimation of the probability the sound comes from the desired direction, cited as ref. [4] in the 2008 paper
- Co-author of "A Consolidated View of Loss Functions for Supervised Deep Learning-Based Speech Enhancement" (Proc. 44th International Conference on Telecommunications and Signal Processing (TSP 2021), Brno, Czech Republic, pp. 72–76) — controlled comparison of 17 spectral training losses for a real-time FF+GRU gain predictor on reverberant CHiME-2 data — establishes that magnitude+complex mixtures always help, that power-law-compressed losses win, and that phase-sensitive SI-SDR gains require linear-domain losses — [[sources/braun-2021-loss-functions-speech-enhancement|Braun & Tashev 2021]]


## Related Sources

- [[sources/braun-2021-loss-functions-speech-enhancement|Braun & Tashev 2021: A Consolidated View of Loss Functions for Supervised Deep Learning-Based Speech Enhancement]]
