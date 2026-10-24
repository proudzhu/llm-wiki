---
type: concept
created: 2026-10-24
updated: 2026-10-24
sources:
  - raw/papers/mezza-2024-hybrid-plc/full-text.md
tags:
  - networked-music-performance
  - audio-signal-processing
  - real-time
  - packet-loss-concealment
---

# Networked Music Performance

**Networked Music Performance (NMP)** is the practice of remote musicians playing together in real time over packet-switched networks. It is the application domain that makes [[concepts/packet-loss-concealment|packet loss concealment]] a *fidelity* problem rather than an intelligibility problem, and it imposes a different set of constraints than VoIP.

## Constraints That Distinguish NMP from VoIP

| Constraint | VoIP | NMP |
|------------|------|-----|
| **Quality criterion** | Intelligibility, word error rate | Fidelity, timbral continuity, absence of clicks |
| **Sample rate** | 16 kHz wideband, occasionally 48 kHz full-band | 32–48 kHz with full musical bandwidth |
| **Latency budget** | ~20 ms PLC latency tolerated | Strict — simultaneous interaction between musicians bounds *total* end-to-end delay |
| **Signal character** | Speech (source–filter) | Polyphonic/solo instruments, quasi-harmonic sustained notes, sharp attack transients |
| **Evaluation** | CMOS / WAcc / PLCMOS | MUSHRA-style listening tests with musically trained assessors |

Because interaction requires tight synchronization, PLC in NMP must be causal, cheap, and must not add perceptual artifacts: a click that would be masked in a speech call is immediately audible as a musical defect. The demands also explain why music-oriented evaluation cannot rely on speech-trained proxies such as [[concepts/plcmos|PLCMOS]] or on cepstral distances built for source–filter signals.

## Modeling Consequences

Sustained portions of notes produced by a solo instrument are quasi-harmonic outside attack transients, so a short-time music signal is well represented by an all-pole system of sufficiently high order — a fact that makes high-order [[concepts/linear-prediction|linear prediction]] an unusually strong NMP-PLC baseline, and it is what [[concepts/parcnet|PARCnet]] exploits by learning only the linear predictor's residual. Classical PLC (pitch-period repetition, G.711-style waveform substitution) and speech-oriented neural PLC alike underperform this simple AR baseline on piano signals.

## Related Concepts

- [[concepts/packet-loss-concealment|Packet Loss Concealment]]
- [[concepts/parcnet|PARCnet]]
- [[concepts/linear-prediction|Linear Prediction]]
- [[concepts/mushra-listening-test|MUSHRA Listening Test]] — the standard subjective protocol for music-quality assessment
- [[concepts/audio-latency|Audio Latency]]

## Related Sources

- [[sources/mezza-2024-hybrid-plc|Mezza, Amerena, Bernardini & Sarti 2024: Hybrid Packet Loss Concealment for Real-Time Networked Music Applications]] — frames NMP-PLC as a high-fidelity, 32 kHz, low-latency problem and evaluates PARCnet under it
