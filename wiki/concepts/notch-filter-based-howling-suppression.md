---
type: concept
created: 2026-08-07
updated: 2026-08-07
sources:
  - raw/papers/vanwaterschoot-2011-fifty-years-afc/full-text.md
  - raw/papers/mounir-2025-robust-early-howling-detection-sparsity/full-text.md
  - raw/papers/williams-2014-acoustic-feedback-elimination/full-text.md
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

### A Concrete Patent Instance: Williams 2014

[[sources/williams-2014-acoustic-feedback-elimination|Williams 2014]] (US 8,634,575 B2, assigned to Harman International) is a concrete two-rate NHS patent for PA/sound-reinforcement systems that maps cleanly onto the pipeline above:

- **Step 3 (candidate selection)** is instantiated as [[concepts/ballistics-based-howling-detection|ballistics-based howling detection]] — each FFT magnitude-squared bin is passed through an asymmetric per-bin filter (gradual attack, zero release) so that persistent tones (feedback) accumulate into "prominences" while transient music releases instantly. A frequency-dependent time constant (200 ms high / 2 s low) further discriminates sustained bass notes from fast-building high-frequency feedback.
- **Steps 4–6 (feature computation + thresholding + notch design)** are replaced by a closed-loop verification: a 6 dB trial notch is inserted at the candidate frequency, and after a 500 ms test window the bin-magnitude reduction is compared to TESTDROP = 3 dB. Only candidates whose reduction confirms feedback are kept and deepened in 6 dB steps; the rest are bypassed. See [[concepts/trial-and-verify-notch-insertion|Trial-and-Verify Notch Insertion]].

The trial-and-verify twist is notable because it sidesteps the **sustained-tone ambiguity** that pure open-loop HD features face: a held violin note is spectrally indistinguishable from feedback in the open-loop microphone signal, but only feedback is sustained by the loop, so the post-notch response differs. The cost is 500 ms of latency per candidate and a brief 6 dB intrusion on wanted tones that happen to be candidates.

## Related Concepts

- [[concepts/howling-detection|Howling Detection]] — the critical front-end component of NHS
- [[concepts/howling-detection-features|Howling Detection Features]] — spectral and temporal features used in the HD stage
- [[concepts/ninosp2-transposed|NINOS²-T]] — a sparsity-based HD feature that removes the candidate-selection requirement
- [[concepts/ballistics-based-howling-detection|Ballistics-Based Howling Detection]] — a temporal-persistence candidate-selection front end (Williams 2014)
- [[concepts/trial-and-verify-notch-insertion|Trial-and-Verify Notch Insertion]] — a closed-loop verification paradigm that replaces open-loop feature thresholding (Williams 2014)
- [[concepts/acoustic-howling-suppression|Acoustic Howling Suppression]] — broader AHS context including AFC and deep-learning approaches
- [[concepts/acoustic-feedback|Acoustic Feedback]] — the problem NHS addresses
- [[concepts/maximum-stable-gain|Maximum Stable Gain]] — NHS effectively increases the operable gain above the passive MSG

## Related Sources

- [[sources/vanwaterschoot-2011-fifty-years-afc|van Waterschoot & Moonen 2011]] — the comprehensive survey of acoustic feedback control including NHS; formalizes the two-stage NHS structure, the six HD features, and the pole-zero-placement notch-filter design
- [[sources/mounir-2025-robust-early-howling-detection-sparsity|Mounir, Bernardi & van Waterschoot 2025]] — proposes NINOS²-T for the HD stage and a modified NHS scheme without candidate selection
- [[sources/williams-2014-acoustic-feedback-elimination|Williams 2014]] — Harman patent (US 8,634,575 B2) instantiating NHS as a two-rate system with ballistics-based candidate detection and trial-and-verify notch insertion
- Waterschoot & Moonen 2010, "Comparative evaluation of howling detection criteria in notch-filter-based howling suppression" (J. Audio Eng. Soc.) — the reference survey of NHS HD features
