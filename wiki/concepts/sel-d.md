---
type: concept
created: 2026-09-09
updated: 2026-09-09
sources:
  - raw/papers/grumiaux-2022-ssl-deep-learning-survey/full-text.txt
tags:
  - sel-d
  - sound-event-detection
  - sound-source-localization
  - multi-task-learning
  - deep-learning
---

# SELD (Sound Event Localization and Detection)

SELD is the joint task of sound event detection (SED — in practice, classification of event types and their temporal activity) and [[concepts/sound-source-localization|sound source localization]]. The Grumiaux et al. 2022 survey includes SELD methods in its review, focusing on the localization side.

## Architecture Pattern

The vast majority of SELD systems (notably DCASE Challenge candidates) follow a multi-task pattern: a common feature-extraction module (typically CRNN layers over FOA or microphone-array features) followed by two task-specific branches — one for SED, one for SSL. The shared representation is assumed to benefit both tasks. From 2021 onward, the [[concepts/activity-coupled-cartesian-doa|ACCDOA]] output representation allowed joint SED+SSL processing up to the very last model layer.

## DCASE Challenge

The SELD task of the DCASE Challenge (2019, 2020, 2021) standardized datasets and evaluation: 12 sound event types (alarms, barking dog, female/male speech, etc.) with up to three simultaneous overlapping events, in reverberant noisy environments synthesized from real RIRs, provided in two four-microphone spatial formats (tetrahedral microphone array and first-order Ambisonics). The 2020/2021 editions added moving sources and directional interferers. The challenge contributed to making DL-based SSL/SED a popular research topic.

## Related Concepts

- [[concepts/sound-source-localization|Sound Source Localization]]
- [[concepts/ambisonics|Ambisonics]]
- [[concepts/activity-coupled-cartesian-doa|ACCDOA]]

## Related Sources

- [[sources/grumiaux-2022-ssl-deep-learning-survey|Grumiaux et al. 2022: A Survey of SSL with Deep Learning Methods]]
