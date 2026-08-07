---
type: concept
created: 2026-08-07
updated: 2026-08-07
sources:
  - raw/papers/vanwaterschoot-2011-fifty-years-afc/full-text.md
  - raw/papers/mounir-2025-robust-early-howling-detection-sparsity/full-text.md
tags:
  - acoustic-howling
  - notch-filter
  - howling-detection
  - signal-processing
---

# Notch-Filter-Based Howling Suppression (NHS)

**Notch-filter-based howling suppression (NHS)** is an [[concepts/acoustic-howling-suppression|acoustic howling suppression]] method that detects howling components and suppresses them using a bank of adjustable narrowband notch filters, achieving narrowband gain reduction around critical frequencies with minimal audio signal distortion.

## Solution Scheme

NHS is a two-stage solution:

1. **Howling detection (HD)** — analyses the microphone signal $y(t)$ to detect howling and estimate its frequency and magnitude, producing a set of notch filter design parameters $\mathcal{D}_H(t)$ (center frequency, bandwidth, notch depth).
2. **Notch filtering** — a bank of adjustable notch filters $H(\omega, t)$ applies narrowband gain reduction around the detected howling frequencies, stabilizing the closed-loop system.

The HD block is the **most critical component** of NHS: its detection precision, speed, and threshold robustness directly determine suppression quality and audibility of howling before detection.

## Position Among AHS Methods

NHS is one of several acoustic feedback control methods, broadly grouped by the width of the frequency band attenuated:

| Method | Bandwidth | Distortion | Speed |
|--------|-----------|------------|-------|
| Automatic gain control | Broadband | High | Reactive |
| Automatic equalization | Subband | Medium | Reactive |
| **NHS** | Narrowband | Low | Reactive |

NHS achieves the **lowest audio signal distortion** because it attenuates only the critical frequencies. However, like most gain-reduction methods, it is **reactive** — howling must be detected before it can be suppressed.

## HD Processing Pipeline

The standard NHS HD pipeline (as surveyed in Waterschoot & Moonen 2010):

1. Frame the microphone signal into overlapping frames of $M$ samples with hop size $P$
2. Apply windowing and compute the STFT
3. **Candidate selection** — peak-pick the magnitude spectrum (sometimes preceded by ballistics) to obtain a small set of candidate howling frequencies
4. Compute one or more discriminating [[concepts/howling-detection-features|HD features]] for each candidate
5. Compare features to a detection threshold (or logical combination thereof)
6. Output notch filter design parameters for detected howling components

Mounir et al. (2025) propose a **modified scheme** that omits the candidate-selection step (step 3), computing features directly on the full STFT. This enables [[concepts/howling-detection|early howling and ringing detection]] that the candidate-based approach structurally excludes.

## Related Concepts

- [[concepts/howling-detection|Howling Detection]] — the critical front-end component of NHS
- [[concepts/howling-detection-features|Howling Detection Features]] — spectral and temporal features used in the HD stage
- [[concepts/ninosp2-transposed|NINOS²-T]] — a sparsity-based HD feature that removes the candidate-selection requirement
- [[concepts/acoustic-howling-suppression|Acoustic Howling Suppression]] — broader AHS context including AFC and deep-learning approaches
- [[concepts/acoustic-feedback|Acoustic Feedback]] — the problem NHS addresses
- [[concepts/maximum-stable-gain|Maximum Stable Gain]] — NHS effectively increases the operable gain above the passive MSG

## Related Sources

- [[sources/vanwaterschoot-2011-fifty-years-afc|van Waterschoot & Moonen 2011]] — the comprehensive survey of acoustic feedback control including NHS; formalizes the two-stage NHS structure, the six HD features, and the pole-zero-placement notch-filter design
- [[sources/mounir-2025-robust-early-howling-detection-sparsity|Mounir, Bernardi & van Waterschoot 2025]] — proposes NINOS²-T for the HD stage and a modified NHS scheme without candidate selection
- Waterschoot & Moonen 2010, "Comparative evaluation of howling detection criteria in notch-filter-based howling suppression" (J. Audio Eng. Soc.) — the reference survey of NHS HD features
