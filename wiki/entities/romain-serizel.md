---
type: entity
created: 2026-07-10
updated: 2026-07-16
tags:
  - researcher
  - speech-enhancement
  - binaural
  - hearing-aid
  - multi-channel
  - quantization
---

# Romain Serizel

**Romain Serizel** is a researcher at Université de Lorraine, CNRS, Inria, LORIA, Nancy, France. He is a senior researcher in multi-channel speech enhancement, binaural processing, and hearing-aid applications, and is the senior/corresponding author of the [[concepts/tango-framework|Tango]] line of distributed binaural speech enhancement frameworks.

## Research Areas

- Distributed and binaural speech enhancement
- Multi-channel speech enhancement for hearing aids
- DNN-based mask estimation and spatial filtering
- Low-latency real-time speech enhancement
- Low-rank (GEVD-based) multichannel Wiener filtering for cochlear implants

## Notable Contributions

- Tango: DNN-based mask estimation for distributed speech enhancement in spatially unconstrained microphone arrays (IEEE/ACM TASLP 2021) — the baseline two-stage distributed binaural framework
- RT-Tango: real-time distributed binaural speech enhancement for low-power hearing aid devices (arXiv 2026, senior author)
- Quantized TANGO / MN-TANGO: low-precision inference for a hybrid distributed binaural SE system; introduces MN-TANGO and W8A8 QAT (arXiv 2026, senior author)
- BinauRec binaural dataset for evaluating speech enhancement with measured room impulse responses (EUSIPCO 2023)
- Frequency-weighted training losses for phoneme-level DNN-based speech enhancement (MMSP 2025)
- Low-rank approximation based multichannel Wiener filter algorithms for noise reduction with application in cochlear implants (IEEE/ACM TASLP 2014)

## Affiliations

- Université de Lorraine, CNRS, Inria, LORIA, F-54000 Nancy, France

## Related Concepts

- [[concepts/distributed-binaural-speech-enhancement|Distributed Binaural Speech Enhancement]]
- [[concepts/tango-framework|Tango Framework]]
- [[concepts/mn-tango|MN-TANGO]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/gevd-spatial-filtering|GEVD-Based Spatial Filtering]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/quantization-aware-training|Quantization-Aware Training (QAT)]]

## Related Sources

- [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|Benslimane et al. 2026: RT-Tango]]
- [[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al. 2026: Quantized TANGO / MN-TANGO]]
