---
type: concept
created: 2026-09-27
updated: 2026-10-07
sources:
  - raw/papers/veluri-2023-semantic-hearing/full-text.md
  - raw/papers/watanabe-2026-low-frequency-harmonic-control/full-text.md
  - raw/papers/ohlenbusch-2026-pas-se/full-text.md
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
- **Open-ear playback intelligibility** ([[sources/watanabe-2026-low-frequency-harmonic-control|Watanabe et al. 2026]]): [[concepts/open-ear-headphones|open-ear headphones]] have weak low-frequency output and let noise in freely; [[concepts/low-frequency-harmonic-control|LFHC]] post-filtering improves playback intelligibility with a handful of filter taps.
- **Own-voice pickup** ([[sources/ohlenbusch-2026-pas-se|Ohlenbusch et al. 2026]]): [[concepts/pas-se|PAS-SE]] combines the acoustically shielded in-ear microphone (auxiliary sensor) with enrollment-based personalization to suppress noise and interfering talkers while preserving own-voice quality; in-ear enrollments stay robust down to −10 dB enrollment SNR.
- Health sensing (blood pressure, ear-based activity) and interaction (ultrasonic head tracking, on-face touch).

## Related Concepts

- [[concepts/semantic-hearing|Semantic Hearing]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/audio-latency|Audio Latency]]
- [[concepts/binaural-target-sound-extraction|Binaural Target Sound Extraction]]
- [[concepts/open-ear-headphones|Open-Ear Headphones]]
- [[concepts/low-frequency-harmonic-control|Low-Frequency Harmonic Control]]
- [[concepts/as-se|Auxiliary-Sensor Speech Enhancement (AS-SE)]]
- [[concepts/pas-se|PAS-SE]]

## Related Sources

- [[sources/veluri-2023-semantic-hearing|Veluri et al. 2023: Semantic Hearing]]
- [[sources/watanabe-2026-low-frequency-harmonic-control|Watanabe et al. 2026: Low-Frequency Harmonic Control]]
- [[sources/ohlenbusch-2026-pas-se|Ohlenbusch, Kegler & Stamenovic 2026: PAS-SE]] — own-voice pickup with in-ear microphone + enrollment personalization
