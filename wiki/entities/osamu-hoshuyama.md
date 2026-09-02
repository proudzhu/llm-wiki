---
type: entity
created: 2026-09-02
updated: 2026-09-02
sources:
  - raw/papers/hoshuyama-2026-sound-object-echo-control/full-text.md
tags:
  - researcher
  - acoustic-echo-cancellation
  - echo-suppression
  - signal-processing
---

# Osamu Hoshuyama

**Affiliation**: NEC Corporation (based on prior publications with Akihiko Sugiyama; not stated in the 2026 preprint)
**Role**: Researcher
**Research Focus**: Acoustic echo control and suppression — nonlinear residual echo modeling, echo canceller robustness, and howling suppression for hands-free communication.

## Key Contributions

- Proposed "An acoustic echo suppressor based on a frequency-domain model of highly nonlinear residual echo" (ICASSP 2006, with [[entities/akihiko-sugiyama|Akihiko Sugiyama]]) — the slow-attach-fast-decay residual echo PSD tracker used as a baseline in later RES work (e.g., Fang 2020)
- Proposed "An echo canceller using smoothed-coefficient filter with adaptive time constant controlled by high-pass errors" (IWAENC 2008) — double-talk-robust coefficient smoothing
- Proposed "An update algorithm for frequency-domain correlation model in a nonlinear echo suppressor" (IWAENC 2012)
- Authored "Acoustic echo control based on sound object identification for suppressing howling caused by complicated acoustic paths" (arXiv 2026) — [[concepts/sound-object-based-echo-control|sound-object-based echo control]], shifting echo control from path estimation to object identification — [[sources/hoshuyama-2026-sound-object-echo-control|Hoshuyama 2026]]

## Related Concepts

- [[concepts/sound-object-based-echo-control|Sound-Object-Based Echo Control]]
- [[concepts/residual-echo-suppression|Residual Echo Suppression]]
- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]]

## Related Sources

- [[sources/hoshuyama-2026-sound-object-echo-control|Hoshuyama 2026: Sound-Object-Based Echo Control]]
- [[sources/fang-2020-robust-residual-echo-suppression|Fang 2020: Robust Residual Echo Suppression]] — uses Hoshuyama & Sugiyama 2006 as baseline
