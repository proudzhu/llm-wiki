---
type: concept
created: 2026-08-14
updated: 2026-08-14
sources:
  - raw/papers/valin-2022-real-time-plc/full-text.md
tags:
  - packet-loss-concealment
  - speech-synthesis
  - real-time
  - speech-coding
  - audio-signal-processing
---

# Packet Loss Concealment

**Packet loss concealment (PLC)** is the task of synthesizing audio to replace voice packets that were lost or arrived too late for playback in real-time voice communication over best-effort unreliable transport (RTP/UDP). The receiver attempts to *conceal* the loss so as to limit the quality degradation perceived by the listener.

## Problem Statement

PLC is challenging for three reasons:

1. **Real-time synthesis** — missing audio must be generated within the playback deadline, typically on a CPU.
2. **Frequent transitions** between received and synthesized audio require seamless cross-fades and resynchronization, both at the *start* of a loss (transition unknown, $U_{0}$) and at the *first received packet after* a loss (transition known, $K_{0}$).
3. **Drift / babbling** of purely autoregressive neural vocoders during long bursts — without conditioning beyond the loss start, the synthesis drifts away from plausible speech.

## Approaches

### Classical PLC

The traditional approach (Sanneck, Stenger, Younes & Girod, GLOBECOM 1996) repeats pitch periods from the last received audio. This improves over zero-filling but introduces noticeable artifacts, especially during non-stationary segments (e.g., at the end of a syllable, the last feature vector represents energy centered 10 ms before the loss, so repetition causes an audible energy burst).

### Neural PLC

Deep neural network (DNN) techniques have been investigated for PLC, including:

- End-to-end ConcealNet (Mohamed & Schuller, 2020)
- Adaptive recurrent neural network speech prediction (Lotfidereshgi & Gournay, 2018)
- WaveNetEQ — autoregressive WaveRNN-based PLC (Stimberg et al., Asilomar 2020)
- Time-domain convolutional recurrent network (Lin et al., ICASSP 2021)
- Adversarial auto-encoding for PLC (Pascual, Serrà & Pons, 2021)
- Hybrid generative + predictive model — [[sources/valin-2022-real-time-plc|Valin et al. 2022]]

### Hybrid Generative + Predictive (Valin et al. 2022)

The hybrid approach decouples synthesis across time scales: a *generative* autoregressive [[concepts/lpcnet|LPCNet]] vocoder synthesizes the missing samples, while a *predictive* RNN estimates the acoustic features (BFCCs, pitch period, pitch correlation) that condition the vocoder. The principle: be "creative" in extending missing segments of a phoneme with plausible-sounding audio, but never invent new phonemes or words. This addresses the drift problem of purely autoregressive PLC while avoiding the artifacts of feature repetition.

## Long-Burst Handling

Beyond ~100 ms of continuous loss, concealment is meaningless. Fading too slowly sounds like heavy breathing; too quickly sounds very unnatural. [[sources/valin-2022-real-time-plc|Valin et al. 2022]] fade out by linearly decreasing the first predicted cepstral coefficient $c_{0}$ after 100 ms to mimic the reverberation decay of a small room with $\mathrm{RT}_{60}=120$ ms, so long losses sound like a talker being naturally interrupted.

## Causal vs. Non-Causal vs. Codec-Integrated

Three operating modes are distinguished:

- **Causal PLC** — no look-ahead; the receiver must play samples as they arrive. Cross-fades the synthesized audio with the first received $K_{0}$ packet to avoid discontinuity.
- **Non-causal PLC** — uses 5 ms of look-ahead to extrapolate the speech backwards from the first received post-loss packet, then cross-fades backward and forward extensions. Output is delayed by the look-ahead.
- **Stateful-codec PLC** — when speech is encoded with a stateful codec (e.g., [[concepts/opus-codec|Opus]], AMR-WB), the concealed audio is needed to reconstruct the first post-loss packet's decoder state, so non-causal processing is impossible. The codec's inherent linear prediction avoids discontinuity, so the cross-fade step is unnecessary.

## Evaluation

PLC systems are evaluated with:

- **Subjective quality**: CMOS (Comparison Category Rating, [[concepts/pesq|P.808]] crowdsourcing), MOS ACR (Absolute Category Rating)
- **ASR impact**: Word accuracy (WAcc) on a downstream speech recognizer
- **Objective proxies**: PLCMOS, DNSMOS, PESQ-WB

The Interspeech 2022 Audio Deep Packet Loss Concealment Challenge ([Diener et al. 2022](https://www.interpeech2022.org/)) is the primary public benchmark; it allows up to 20 ms total latency and does not involve a codec. The challenge ranks submissions by an overall score combining CMOS and WAcc.

## Related Concepts

- [[concepts/lpcnet|LPCNet]] — autoregressive neural vocoder used for PLC synthesis
- [[concepts/opus-codec|Opus Audio Codec]] — stateful codec integration target
- [[concepts/burg-spectral-estimation|Burg Spectral Estimation]] — half-frame spectral features for short-time conditioning
- [[concepts/bark-scale-spectral-features|Bark-Scale Spectral Features]] — LPCNet's 18 BFCC features
- [[concepts/pesq|PESQ]] — objective PLC quality metric
- Speech synthesis, real-time processing (related fields)

## Related Sources

- [[sources/valin-2022-real-time-plc|Valin et al. 2022: Real-Time Packet Loss Concealment With Mixed Generative and Predictive Model]] — hybrid generative + predictive architecture, 2nd place Interspeech 2022 PLC Challenge
