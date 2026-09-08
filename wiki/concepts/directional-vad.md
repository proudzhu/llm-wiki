---
type: concept
created: 2026-09-08
updated: 2026-09-08
sources:
  - raw/papers/sun-2024-lightweight-hybrid-speech-extraction/full-text.txt
tags:
  - voice-activity-detection
  - spatial-audio
  - multi-channel
  - target-speaker-extraction
  - deep-learning
---

# Directional Voice Activity Detection (DVAD)

**Directional Voice Activity Detection (DVAD)** generalizes [[concepts/voice-activity-detection|voice activity detection]] from a binary "is any speech present?" decision to a **per-zone spatial activity map**: the horizontal plane around a microphone array is partitioned into $N$ disjoint angular zones (according to the array's beam-width), and the DVAD system estimates the instantaneous speech activity of speakers in each zone, $\hat{P}(l) \in \mathbb{R}^{N}$, one probability per zone per frame. Introduced by [[sources/sun-2024-lightweight-hybrid-speech-extraction|Sun et al. 2024]], DVAD makes VAD **direction-aware and multi-speaker-safe**, in contrast to energy- or RNN-based VAD assists for adaptive GSCs that assume a single speaker and degrade with interfering speakers.

## Key Formulations

The DVAD of Sun et al. 2024 is a lightweight CRN adapted from [[concepts/direction-of-arrival-estimation|DOA-estimation]] CRNs:

- **Input features**: linear-frequency log-power spectrograms $\mathrm{LinSpec}(k,l) = \log_{10}|\mathbf{Y}(k,l)|^2 \in \mathbb{R}^{M}$ concatenated with sin inter-channel phase differences $\mathrm{sinIPD}(k,l) = \sin(\arg[Y_1^*(k,l)Y_{2:M}(k,l)]) \in \mathbb{R}^{M-1}$, giving a $(2M-1) \times F \times T$ tensor.
- **Architecture**: 3 CNN layers → 4 disconnected parallel GRUs (grouped RNN) → tanh → FC → sigmoid; ~33K parameters, 31M MACs/s.
- **Training**: recall-weighted binary cross-entropy over the $N$ zone classes ($\gamma = 10$ emphasizes recall so active zones are rarely missed), with ground-truth labels obtained by running rVAD on each speaker's reverberant speech before mixing; random channel-axis rolling exploits the circular array's spatial symmetry as augmentation.
- **Binarization**: the target-zone probability $\hat{P}_1(l)$ is thresholded ($P_{threshold} = 0.5$; measured precision 94% / recall 95%) into a hard VAD label $\delta(l)$.

## Dual Use: GSC Adaptation Control + Post-Filter Conditioning

DVAD's value comes from serving two consumers simultaneously:

1. **Gating robust-GSC adaptation** — $\delta(l)$ gates the NLMS update of the adaptive blocking matrix (update during target-active frames, so it learns to block target speech) and its complement $\bar{\delta}(l) = 1-\delta(l)$ gates the adaptive interference canceller (update during target-silent frames, when the noise reference is free of target leakage). See [[concepts/gsc-beamformer|GSC]].
2. **Auxiliary input to the neural post-filter** — the soft full-zone DVAD is concatenated to the encoder output of a DPCRN post-filter, letting the network identify the target speaker in overlapping-speech segments. The full $N$-zone DVAD generalizes better to real-world recordings than the target-zone-only signal (DNSMOS SIG 3.205 vs 2.813), because the complete activity distribution preserves spatial information through post-filtering.

## Distinction from Related Activity-Detection Tasks

| Task | Output | Conditioning |
|:-----|:-------|:-------------|
| Standard [[concepts/voice-activity-detection|VAD]] | "any speech present?" per frame | none |
| [[concepts/target-speaker-vad|TS-VAD]] | "is the *target* speaker active?" | enrollment / speaker embedding |
| DVAD | per-zone activity map over $N$ angular zones | array geometry + known target zone |
| [[concepts/side-talk-detection|Side-Talk Detection]] | wearer / bystander / non-speech | device-relative roles |

DVAD is *spatially* conditioned rather than *identity*-conditioned: it does not need to know who the target speaker is, only which zone they occupy — making it enrollment-free and suitable for video-conferencing-type scenarios where the talker direction is known.

## Related Concepts

- [[concepts/voice-activity-detection|Voice Activity Detection]] — single-channel, direction-agnostic ancestor
- [[concepts/target-speaker-vad|Target-Speaker VAD (TS-VAD)]] — identity-conditioned counterpart
- [[concepts/side-talk-detection|Side-Talk Detection]] — role-conditional VAD variant
- [[concepts/gsc-beamformer|Generalized Sidelobe Canceller (GSC)]] — primary consumer of the binarized DVAD
- [[concepts/target-speaker-extraction|Target Speaker Extraction]] — task context (spatial-clue TSE)
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]] — CRN backbone heritage
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network (CRN)]] — network family
- [[concepts/multi-channel-speech-presence-probability|Multi-Channel Speech Presence Probability]] — soft spatial-detection relative in the informed-spatial-filter lineage

## Related Sources

- [[sources/sun-2024-lightweight-hybrid-speech-extraction|Sun, Lei & Zhang et al. 2024: A Lightweight Hybrid Multi-Channel Speech Extraction System with Directional Voice Activity Detection]] — introduces DVAD and demonstrates its dual use
- [[sources/zmolikova-2023-neural-target-speech-extraction-overview|Zmolikova 2023: Neural Target Speech Extraction Overview]] — surveys activity-detection variants of TSE (TS-VAD) that DVAD complements with spatial conditioning
- [[sources/taseska-2018-informed-spatial-filters|Taseska 2018: Informed Spatial Filters]] — earlier detector-controlled GSC adaptation (DOA-model-based bin-wise detector), the single-speaker-lineage predecessor of DVAD-gated adaptation
