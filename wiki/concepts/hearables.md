---
type: concept
created: 2026-09-27
updated: 2026-10-24
sources:
  - raw/papers/veluri-2023-semantic-hearing/full-text.md
  - raw/papers/watanabe-2026-low-frequency-harmonic-control/full-text.md
  - raw/papers/ohlenbusch-2026-pas-se/full-text.md
  - raw/papers/yuan-2026-open-ear-anc-smart-glasses/full-text.md
  - raw/papers/chiba-2027-wideband-anc-coaxial-loudspeaker/full-text.txt
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
- **Open-ear ANC** ([[sources/yuan-2026-open-ear-anc-smart-glasses|Yuan, Liu & Xiao 2026]]): the first working ANC on open-ear smart glasses, with no in-ear error microphone — [[concepts/virtual-in-ear-sensing|virtual in-ear sensing]] estimates the in-ear residual from 8 frame microphones, regenerating control filters every 200 ms on the glasses' CPU and applying them via [[concepts/hybrid-partitioned-convolution|hybrid partitioned convolution]] on the DSP at 113 µs end-to-end (11.2 dB mean reduction 100–1000 Hz with per-user calibration).
- **Wideband open-ear ANC via loudspeaker design** ([[sources/chiba-2027-wideband-anc-coaxial-loudspeaker|Chiba et al. 2027]]): a [[concepts/coaxial-two-way-secondary-source|coaxial 2-way secondary source]] with [[concepts/delay-oriented-driver-allocation|delay-oriented driver allocation]] widens the feedforward control band from the loudspeaker side — the woofer carries low frequencies (low mechanical delay), the tweeter higher frequencies (short acoustic path) — 8.01 dB over 100–2000 Hz in measured-path evaluation, a hardware-design route complementary to the sensing-side virtual in-ear approach.
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
- [[concepts/virtual-in-ear-sensing|Virtual In-Ear Sensing]] — error-microphone-free ANC for open-ear glasses
- [[concepts/hybrid-partitioned-convolution|Hybrid Partitioned Convolution]] — real-time long-filter replay on hearable DSPs
- [[concepts/coaxial-two-way-secondary-source|Coaxial Two-Way Secondary Source]] — loudspeaker-side enabler of wideband open-ear ANC
- [[concepts/delay-oriented-driver-allocation|Delay-Oriented Driver Allocation]] — driver-band assignment by delay characteristics

## Related Sources

- [[sources/veluri-2023-semantic-hearing|Veluri et al. 2023: Semantic Hearing]]
- [[sources/watanabe-2026-low-frequency-harmonic-control|Watanabe et al. 2026: Low-Frequency Harmonic Control]]
- [[sources/ohlenbusch-2026-pas-se|Ohlenbusch, Kegler & Stamenovic 2026: PAS-SE]] — own-voice pickup with in-ear microphone + enrollment personalization
- [[sources/yuan-2026-open-ear-anc-smart-glasses|Yuan, Liu & Xiao 2026: Active Noise Cancellation on Open-Ear Smart Glasses]] — error-microphone-free ANC on open-ear smart glasses: network-generated filters on a 200 ms refresh, hybrid partitioned convolution at 113 µs end-to-end
- [[sources/chiba-2027-wideband-anc-coaxial-loudspeaker|Chiba, Kamado, Kako & Noguchi 2027: Wideband ANC for Open-Ear Headphones with a Coaxial Loudspeaker]] — wideband open-ear feedforward ANC via delay-budgeted coaxial 2-way loudspeaker design
