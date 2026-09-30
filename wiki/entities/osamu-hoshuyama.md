---
type: entity
created: 2026-09-02
updated: 2026-09-30
sources:
  - raw/papers/hoshuyama-2026-sound-object-echo-control/full-text.md
  - raw/papers/hoshuyama-1999-robust-adaptive-beamformer-ccaf/full-text.md
tags:
  - researcher
  - acoustic-echo-cancellation
  - echo-suppression
  - signal-processing
  - beamforming
  - microphone-arrays
  - adaptive-filtering
---

# Osamu Hoshuyama

**Affiliation**: NEC Corporation, Kawasaki, Japan (Multimedia Signal Processing, C&C Media Research Laboratories — per the 1999 paper)
**Role**: Researcher
**Research Focus**: Acoustic echo control and suppression — nonlinear residual echo modeling, echo canceller robustness, and howling suppression for hands-free communication; earlier work on robust adaptive microphone-array beamforming.

## Key Contributions

- Proposed "An acoustic echo suppressor based on a frequency-domain model of highly nonlinear residual echo" (ICASSP 2006, with [[entities/akihiko-sugiyama|Akihiko Sugiyama]]) — the slow-attach-fast-decay residual echo PSD tracker used as a baseline in later RES work (e.g., Fang 2020)
- Proposed "An echo canceller using smoothed-coefficient filter with adaptive time constant controlled by high-pass errors" (IWAENC 2008) — double-talk-robust coefficient smoothing
- Proposed "An update algorithm for frequency-domain correlation model in a nonlinear echo suppressor" (IWAENC 2012)
- Authored "Acoustic echo control based on sound object identification for suppressing howling caused by complicated acoustic paths" (arXiv 2026) — [[concepts/sound-object-based-echo-control|sound-object-based echo control]], shifting echo control from path estimation to object identification — [[sources/hoshuyama-2026-sound-object-echo-control|Hoshuyama 2026]]
- First author of "A robust adaptive beamformer for microphone arrays with a blocking matrix using constrained adaptive filters" (IEEE Transactions on Signal Processing, vol. 47, no. 10, pp. 2677–2684, 1999) — the [[concepts/coefficient-constrained-adaptive-filter|coefficient-constrained adaptive filter (CCAF)]]-based [[concepts/adaptive-blocking-matrix|adaptive blocking matrix]] that makes a [[concepts/gsc-beamformer|GSC]] robust to 20° of [[concepts/steering-vector-error|target-direction error]] without spending interference-reduction degrees of freedom; 19 dB interference reduction and 3.8 MOS in a 0.3-s reverberation room — [[sources/hoshuyama-1999-robust-adaptive-beamformer-ccaf|Hoshuyama, Sugiyama & Hirano 1999]]

## Related Concepts

- [[concepts/sound-object-based-echo-control|Sound-Object-Based Echo Control]]
- [[concepts/residual-echo-suppression|Residual Echo Suppression]]
- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]]
- [[concepts/gsc-beamformer|Generalized Sidelobe Canceller (GSC)]]
- [[concepts/coefficient-constrained-adaptive-filter|Coefficient-Constrained Adaptive Filter (CCAF)]]
- [[concepts/adaptive-blocking-matrix|Adaptive Blocking Matrix (ABM)]]

## Related Sources

- [[sources/hoshuyama-2026-sound-object-echo-control|Hoshuyama 2026: Sound-Object-Based Echo Control]]
- [[sources/fang-2020-robust-residual-echo-suppression|Fang 2020: Robust Residual Echo Suppression]] — uses Hoshuyama & Sugiyama 2006 as baseline
- [[sources/hoshuyama-1999-robust-adaptive-beamformer-ccaf|Hoshuyama, Sugiyama & Hirano 1999: A Robust Adaptive Beamformer with a Blocking Matrix Using Constrained Adaptive Filters]]
