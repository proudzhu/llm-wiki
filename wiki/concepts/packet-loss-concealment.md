---
type: concept
created: 2026-08-14
updated: 2026-10-24
sources:
  - raw/papers/lee-2016-dnn-plc/full-text.md
  - raw/papers/valin-2022-real-time-plc/full-text.md
  - raw/papers/valin-2018-lpcnet/full-text.md
  - raw/papers/nguyen-2023-predictive-plc/full-text.md
  - raw/papers/westhausen-2022-tplcnet/full-text.md
  - raw/papers/mezza-2024-hybrid-plc/full-text.md
tags:
  - packet-loss-concealment
  - networked-music-performance
  - blind-plc
  - full-band
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

### Informed vs. Blind PLC

PLC algorithms divide into **informed** PLC, which receives prior information about which audio packets were lost (the loss mask), and **blind** PLC (audio in-painting), which recovers the lossy signal without loss traces (Kegler, Beckmann & Cernak, Interspeech 2020). Blind operation suits deployments where packet metadata may not be readily available, and — because it does not require alignment between the audio input and its packet stream — it handles **arbitrary packet sizes**. Most existing PLC methods, informed or blind, operate at 16 kHz; extending blind PLC to full-band 48 kHz with causal, real-time processing is the contribution of [[sources/nguyen-2023-predictive-plc|Nguyen, Nguyen & Khong 2023]] (FRN).

### Neural PLC

Deep neural network (DNN) techniques have been investigated for PLC, including:

- DNN regression on log-power spectra + phase — [[sources/lee-2016-dnn-plc|Lee & Chang 2016]], the earliest DNN-based PLC: two feed-forward DNNs regress the missing frame's spectral features from 11 preceding good frames (see [[concepts/dnn-regression-plc|DNN Regression PLC]])
- End-to-end ConcealNet (Mohamed & Schuller, 2020)
- Adaptive recurrent neural network speech prediction (Lotfidereshgi & Gournay, 2018)
- WaveNetEQ — autoregressive WaveRNN-based PLC (Stimberg et al., Asilomar 2020)
- Time-domain convolutional recurrent network (Lin et al., ICASSP 2021)
- Adversarial auto-encoding for PLC (Pascual, Serrà & Pons, 2021)
- Hybrid generative + predictive model — [[sources/valin-2022-real-time-plc|Valin et al. 2022]]
- Full-band recurrent network (FRN) — [[sources/nguyen-2023-predictive-plc|Nguyen, Nguyen & Khong 2023]]: real-time *blind* PLC at 48 kHz whose predictor reuses the previous enhanced output (see [[concepts/full-band-recurrent-network|FRN]])
- tPLCnet — [[sources/westhausen-2022-tplcnet|Westhausen & Meyer 2022]]: seq2one on-demand time-domain BGRU predicting a lost 10 ms frame from a short context buffer, triggered only at loss time (3rd place Interspeech 2022 PLC Challenge; see [[concepts/tplcnet|tPLCnet]])

Two inference regimes exist within neural PLC: **continuous inference**, where the model processes every incoming frame to update its state (Lotfidereshgi & Gournay 2018; Lin et al. 2021; FRN), and **on-demand (seq2one) inference**, where the model is triggered only when a loss is actually detected and predicts the whole missing frame from a fixed context buffer (tPLCnet, [[sources/westhausen-2022-tplcnet|Westhausen & Meyer 2022]]). On-demand inference scales compute with the actual loss rate instead of the full audio stream, at the price of a bounded temporal context (6–7 frames suffice; longer buffers are detrimental).

A third split cuts across that dichotomy: **what the network predicts**. Most systems predict the waveform (or its spectral features) directly; [[concepts/parcnet|PARCnet]] ([[sources/mezza-2024-hybrid-plc|Mezza et al. 2024]]) instead predicts only the nonlinear **residual of an online linear AR predictor**, leaving the quasi-harmonic short-time structure to the classical model. This keeps the network feed-forward, tiny (416 k parameters) and seam-smooth at the same time.

### Hybrid Generative + Predictive (Valin et al. 2022)

The hybrid approach decouples synthesis across time scales: a *generative* autoregressive [[concepts/lpcnet|LPCNet]] ([[sources/valin-2018-lpcnet|Valin & Skoglund 2018]]) vocoder synthesizes the missing samples, while a *predictive* RNN estimates the acoustic features (BFCCs, pitch period, pitch correlation) that condition the vocoder. The principle: be "creative" in extending missing segments of a phoneme with plausible-sounding audio, but never invent new phonemes or words. This addresses the drift problem of purely autoregressive PLC while avoiding the artifacts of feature repetition.

### Hybrid Linear Autoregressive + Neural Residual (PARCnet)

Music-oriented PLC shifts the balance between model classes. Because sustained notes of a solo instrument are quasi-harmonic outside attack transients, a short-time music signal is well represented by an all-pole system of high order — so a plain $\mathrm{AR}(128)$ predictor fitted online (autocorrelation + Levinson–Durbin on a 100 ms sliding window, with [[concepts/diagonal-loading|diagonal loading]] for conditioning) outperforms every deep baseline in [[sources/mezza-2024-hybrid-plc|Mezza et al. 2024]] on NMSE, PEAQ and PLCMOS, at ~1.8 ms per 10 ms packet. The deep model's role therefore shrinks to what the linear model cannot express: [[concepts/parcnet|PARCnet]] predicts the AR residual with a 416 k-parameter feed-forward network and adds it to the linear forecast,

$$
\hat{\mathbf{y}}=\mathbf{y}_{\mathrm{AR}}+\mathbf{v}\odot f_\theta(\mathbf{x}),
$$

where the envelope $\mathbf{v}$ fades the neural term in over 16 samples so the seam between received and concealed audio stays continuous. This is the residual-prediction idea of Thyssen et al. (1994) revived with frame-wise inference: it runs in real time at 32 kHz (8.1 ms per 10 ms packet in unoptimized Python) and beats all deep baselines, including autoregressive vocoder PLC retrained on the same piano corpus. A related branch of the design space is *codec*-level hybridisation — LPCNet- and CELP-style systems where linear prediction shapes the spectral envelope and a neural network supplies the excitation.

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

- [[concepts/parcnet|PARCnet]] — hybrid linear-AR + neural-residual PLC for music
- [[concepts/networked-music-performance|Networked Music Performance]] — fidelity-first PLC domain (32 kHz, strict latency)
- [[concepts/mushra-listening-test|MUSHRA Listening Test]] — subjective protocol used for music PLC
- [[concepts/lpcnet|LPCNet]] — autoregressive neural vocoder used for PLC synthesis
- [[concepts/opus-codec|Opus Audio Codec]] — stateful codec integration target
- [[concepts/burg-spectral-estimation|Burg Spectral Estimation]] — half-frame spectral features for short-time conditioning
- [[concepts/bark-scale-spectral-features|Bark-Scale Spectral Features]] — LPCNet's 18 BFCC features
- [[concepts/pesq|PESQ]] — objective PLC quality metric
- Speech synthesis, real-time processing (related fields)

## Related Sources

- [[sources/mezza-2024-hybrid-plc|Mezza et al. 2024: Hybrid Packet Loss Concealment for Real-Time Networked Music Applications]] — music/NMP PLC; residual-prediction hybrid (linear AR + feed-forward residual network); shows AR(128) alone beating deep baselines at 32 kHz
- [[sources/lee-2016-dnn-plc|Lee & Chang 2016: DNN-Based Packet Loss Concealment]] — first DNN-regression PLC (log-power spectra + phase, RBM pre-training), evaluated on LSD/PESQ/MOS and network speech recognition
- [[sources/valin-2022-real-time-plc|Valin et al. 2022: Real-Time Packet Loss Concealment With Mixed Generative and Predictive Model]] — hybrid generative + predictive architecture, 2nd place Interspeech 2022 PLC Challenge
- [[sources/valin-2018-lpcnet|Valin & Skoglund 2018: LPCNet]] — the autoregressive neural vocoder whose excitation/LPC division of labor underlies the generative branch
- [[sources/nguyen-2023-predictive-plc|Nguyen, Nguyen & Khong 2023: Full-Band Blind Packet-Loss Concealment With Predictive Network]] — real-time blind 48 kHz PLC with an RNN-transducer-style predictor that reuses the previous output
- [[sources/westhausen-2022-tplcnet|Westhausen & Meyer 2022: tPLCnet — Real-Time Deep Packet Loss Concealment in the Time Domain]] — seq2one on-demand time-domain PLC, 3rd place in the Interspeech 2022 PLC Challenge
