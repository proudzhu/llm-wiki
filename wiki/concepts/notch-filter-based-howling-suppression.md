---
type: concept
created: 2026-08-07
updated: 2026-08-08
sources:
  - raw/papers/vanwaterschoot-2011-fifty-years-afc/full-text.md
  - raw/papers/mounir-2025-robust-early-howling-detection-sparsity/full-text.md
  - raw/papers/williams-2014-acoustic-feedback-elimination/full-text.md
  - raw/papers/gil-cacho-2009-regularized-adaptive-notch-filters/full-text.md
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

## ANF-Based One-Stage Variant: Regularized Adaptive Notch Filter (RANF)

The two-stage FFT-based pipeline above is not the only NHS architecture. **Adaptive notch filter (ANF)-based NHS** is a one-stage alternative in which a parametric second-order IIR notch filter adapts sample-by-sample to track and suppress a howling tone simultaneously — no FFT and no separate detection block. ANF-based methods have minimum processing delay and low complexity, and track howling frequency on a sample-by-sample basis, but historically lacked a reliable howling-detection mechanism because no power-spectrum information is available.

[[sources/gil-cacho-2009-regularized-adaptive-notch-filters|Gil-Cacho et al. 2009]] introduced the [[concepts/regularized-adaptive-notch-filter|Regularized Adaptive Notch Filter (RANF)]] to close this gap: three direct-form ANFs run in parallel with signed regularization ($+\lambda$, $0$, $-\lambda$). The sign of the regularization drives the three frequency estimates to **diverge** when no howling is present and to **converge** to a common value when howling is present, so coefficient convergence itself becomes a detection criterion — giving the ANF approach a detection capability comparable to FFT-based methods without their delay/complexity. The method fails for howling near $0$ or $f_s/2$ due to direct-form ANF instability at frequency extremes (a limitation lattice ANFs do not satisfactorily fix for coloured speech/music inputs). See [[concepts/regularized-adaptive-notch-filter|RANF]] for the full formulation.

## Related Concepts

- [[concepts/howling-detection|Howling Detection]] — the critical front-end component of NHS
- [[concepts/howling-detection-features|Howling Detection Features]] — spectral and temporal features used in the HD stage
- [[concepts/ninosp2-transposed|NINOS²-T]] — a sparsity-based HD feature that removes the candidate-selection requirement
- [[concepts/ballistics-based-howling-detection|Ballistics-Based Howling Detection]] — a temporal-persistence candidate-selection front end (Williams 2014)
- [[concepts/trial-and-verify-notch-insertion|Trial-and-Verify Notch Insertion]] — a closed-loop verification paradigm that replaces open-loop feature thresholding (Williams 2014)
- [[concepts/acoustic-howling-suppression|Acoustic Howling Suppression]] — broader AHS context including AFC and deep-learning approaches
- [[concepts/acoustic-feedback|Acoustic Feedback]] — the problem NHS addresses
- [[concepts/maximum-stable-gain|Maximum Stable Gain]] — NHS effectively increases the operable gain above the passive MSG
- [[concepts/regularized-adaptive-notch-filter|Regularized Adaptive Notch Filter (RANF)]] — the ANF-based one-stage NHS variant (Gil-Cacho et al. 2009)

## Related Sources

- [[sources/vanwaterschoot-2011-fifty-years-afc|van Waterschoot & Moonen 2011]] — the comprehensive survey of acoustic feedback control including NHS; formalizes the two-stage NHS structure, the six HD features, and the pole-zero-placement notch-filter design
- [[sources/mounir-2025-robust-early-howling-detection-sparsity|Mounir, Bernardi & van Waterschoot 2025]] — proposes NINOS²-T for the HD stage and a modified NHS scheme without candidate selection
- [[sources/williams-2014-acoustic-feedback-elimination|Williams 2014]] — Harman patent (US 8,634,575 B2) instantiating NHS as a two-rate system with ballistics-based candidate detection and trial-and-verify notch insertion
- Waterschoot & Moonen 2010, "Comparative evaluation of howling detection criteria in notch-filter-based howling suppression" (J. Audio Eng. Soc.) — the reference survey of NHS HD features
- [[sources/gil-cacho-2009-regularized-adaptive-notch-filters|Gil-Cacho et al. 2009]] — introduces the ANF-based one-stage NHS variant RANF with signed-regularization convergence detection
