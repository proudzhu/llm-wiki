---
type: entity
created: 2026-05-12
updated: 2026-09-13
tags:
  - researcher
  - speech-enhancement
  - virtual-microphone
  - time-domain
  - convolutional-neural-network
---

# Ashutosh Pandey

**Affiliation**: Meta Reality Labs Research (formerly Ohio State University)
**Role**: Researcher
**Research Focus**: Multichannel speech enhancement, neural beamforming, time-domain speech processing, ultra-low-compute architectures.

## Key Contributions

- Proposed AECNN framework: time-domain CNN trained with frequency-domain STFT magnitude loss, avoiding invalid STFT problem ([[sources/pandey-2019-cnn-speech-enhancement-time-domain|Pandey & Wang 2019]])
- Co-authored Spatial-Magnifier for spatial upsampling in multichannel speech enhancement ([[sources/lee-2026-spatial-magnifier-spatial-upsampling|Lee et al. 2026]])
- Co-authored NeuralPMWF: a tiny neural network fully controlling the PMWF for low-compute multichannel speech enhancement, built on his spatial-processing-block and SplitGRU-based MaskDNN design lineage ([[sources/grinstein-2025-tiny-param-mwf|Grinstein et al. 2025]])
- First author of "Ultra Low-Compute Complex Spectral Masking for Multichannel Speech Enhancement" (ICASSP 2025 (IEEE International Conference on Acoustics, Speech and Signal Processing), 2025) — introduced TinyGRU, an ultra-low-compute complex spectral masking model with MCWF integration (54 MMACs/s, 8-ch) — [[sources/pandey-2025-ultra-low-compute|Pandey & Azcarreta 2025]]


## Related Sources

- [[sources/pandey-2019-cnn-speech-enhancement-time-domain|Pandey & Wang 2019: CNN-Based Speech Enhancement in the Time Domain]]
- [[sources/lee-2026-spatial-magnifier-spatial-upsampling|Lee et al. 2026: Spatial-Magnifier]]
- [[sources/grinstein-2025-tiny-param-mwf|Grinstein et al. 2025: Controlling the PMWF Using a Tiny Neural Network]]
- [[sources/pandey-2025-ultra-low-compute|Pandey & Azcarreta 2025: Ultra Low-Compute Complex Spectral Masking for Multichannel Speech Enhancement]]


## Related Concepts

- [[concepts/time-domain-speech-enhancement|Time-Domain Speech Enhancement]]
- [[concepts/frequency-domain-loss|Frequency Domain Loss for Time-Domain Networks]]
- [[concepts/neuralpmwf|NeuralPMWF]]
