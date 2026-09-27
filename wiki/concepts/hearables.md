---
type: concept
created: 2026-09-27
updated: 2026-09-27
sources:
  - raw/papers/veluri-2023-semantic-hearing/full-text.md
tags:
  - hearables
  - audio-signal-processing
  - realtime-processing
---

# Hearables

**Hearables** are in-ear or on-ear wearable audio devices — earbuds, headsets, and headphones with sensing and computation — used by hundreds of millions of people. Beyond audio playback, modern hearables integrate [[concepts/active-noise-control|active noise cancellation]], acoustic transparency, in-ear health sensing, and voice assistants.

## Signal-Processing Constraints

Hearable audio processing is among the most constrained real-time signal-processing settings:

- **Latency**: end-to-end budget of 20–50 ms to keep output synced with vision; ~10 ms algorithmic budgets in hearing aids (see [[concepts/audio-latency|audio latency]]).
- **Compute**: on-device inference only (no cloud round trip within the latency budget), on phone-class processors at best — motivating small causal models and, prospectively, embedded GPUs or custom silicon.
- **Binaural realism**: outputs must preserve [[concepts/interaural-time-difference|ITD]] / [[concepts/interaural-level-difference|ILD]] cues shaped by per-user [[concepts/head-related-transfer-function|HRTFs]].

## Applications

- **[[concepts/semantic-hearing|Semantic hearing]]** (Veluri et al. 2023): program the acoustic scene by sound class on a noise-canceling headset.
- Speech enhancement for telephony (e.g., ClearBuds binaural earbuds, 44.8 ms lookahead, 109 ms latency — too slow for in-ear augmented audio).
- Health sensing (blood pressure, ear-based activity) and interaction (ultrasonic head tracking, on-face touch).

## Related Concepts

- [[concepts/semantic-hearing|Semantic Hearing]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/audio-latency|Audio Latency]]
- [[concepts/binaural-target-sound-extraction|Binaural Target Sound Extraction]]

## Related Sources

- [[sources/veluri-2023-semantic-hearing|Veluri et al. 2023: Semantic Hearing]]
