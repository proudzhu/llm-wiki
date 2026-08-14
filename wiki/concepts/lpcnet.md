---
type: concept
created: 2026-08-14
updated: 2026-08-14
sources:
  - raw/papers/valin-2022-real-time-plc/full-text.md
tags:
  - neural-vocoder
  - speech-synthesis
  - lpcnet
  - low-complexity
  - real-time
  - autoregressive
---

# LPCNet

**LPCNet** is an autoregressive neural speech vocoder that improves on WaveRNN by incorporating linear prediction. Introduced by [[entities/jean-marc-valin|Jean-Marc Valin]] and Skoglund (ICASSP 2019), it splits synthesis into a frame-rate network operating on acoustic features at 100 Hz and a sample-rate network that autoregressively generates 16 kHz speech samples conditioned on the frame-rate network's output.

## Architecture

- **Frame-rate network** — operates at 100 Hz on acoustic feature vectors. The original LPCNet uses two 3×1 convolutional layers configured to use two feature vectors *ahead* of the frame being synthesized; this extra context improves synthesis quality at the cost of 25 ms added algorithmic latency. For real-time / packet-loss-concealment use, a strictly causal variant (no look-ahead) is used.
- **Sample-rate network** — autoregressively generates 16 kHz speech samples conditioned on the frame-rate network's output. Uses a $\mathrm{GRU_{A}}$ (gated recurrent unit). The improved low-complexity variant (Valin, Isik, Smaragdis & Krishnaswamy, ICASSP 2022) reduces the $\mathrm{GRU_{A}}$ to 640 units at 15% density while meeting real-time constraints on a laptop CPU.

### Acoustic Features

Each 10-ms synthesized speech segment corresponds to the center of a 20-ms analysis window (5 ms algorithmic delay). The feature vector per frame contains:

- **18 Bark-frequency cepstral coefficients (BFCCs)** — a [[concepts/bark-scale-spectral-features|Bark-scale]] cepstral representation of the spectral envelope
- **Pitch period** (always present, even for unvoiced frames — hence noisy)
- **Pitch correlation** (a periodicity measure; cf. [[concepts/pitch-coherence|pitch coherence]] in PercepNet)

## Use in Packet Loss Concealment

In [[sources/valin-2022-real-time-plc|Valin et al. 2022]], LPCNet is the generative backbone of a hybrid PLC architecture: a predictive RNN estimates the LPCNet feature vectors during loss, and LPCNet synthesizes the missing samples. This decouples short-time sample synthesis from long-time spectral-trajectory control, addressing the drift problem of purely autoregressive PLC.

Key adaptations for PLC:

- **Causal feature model** — the original 2-frame look-ahead is removed because future features are unavailable during loss.
- **Sign randomization in training** — the sign of each training sequence is explicitly randomized so the algorithm works for any polarity of the speech signal.
- **State seeding from known samples** — before synthesis, the LPCNet state is updated using known samples $\left[t-15\,\mathrm{ms},t-5\,\mathrm{ms}\right]$ alongside the most recent features, so the autoregressive model is conditioned on actual preceding audio.

## Complexity

LPCNet dominates the complexity of the Valin 2022 PLC system; the feature-prediction RNN contributes less than 20% of the total. On an Intel i7-10810U laptop CPU, steady-state (known frame $K$ or unknown frame $U$) processing of a 10-ms frame takes 1.34–1.38 ms, i.e. 13–14% of one CPU core.

## Distinction from PercepNet

LPCNet and [[concepts/percepnet|PercepNet]] are sibling Valin-lab hybrid DSP/DNN real-time systems, both sharing the low-complexity, perceptually-motivated design philosophy:

- **LPCNet** (2019) — neural *vocoder* for sample-level waveform synthesis. Bark-scale cepstral features condition an autoregressive sample-rate network.
- **PercepNet** (2020/2021) — neural *post-filter* for speech enhancement and acoustic echo cancellation. ERB-scale (32-band) features condition a DNN that predicts per-band gains and comb-filter strengths.

LPCNet generates speech samples; PercepNet filters an existing noisy/echoed signal. They share the [[entities/jean-marc-valin|Valin]] / [[entities/arvindh-krishnaswamy|Krishnaswamy]] / [[entities/paris-smaragdis|Smaragdis]] authorship line and the hybrid-DSP/DNN design pattern, but operate at different stages of the speech pipeline.

## Related Concepts

- [[concepts/packet-loss-concealment|Packet Loss Concealment]] — primary application of LPCNet in Valin 2022
- [[concepts/percepnet|PercepNet]] — sibling Valin-lab hybrid system for speech enhancement / AEC
- [[concepts/bark-scale-spectral-features|Bark-Scale Spectral Features]] — LPCNet's 18 BFCC inputs
- [[concepts/gated-recurrent-unit|Gated Recurrent Unit]] — backbone of the sample-rate network
- [[concepts/opus-codec|Opus Audio Codec]] — codec integration context for PLC

## Related Sources

- [[sources/valin-2022-real-time-plc|Valin et al. 2022: Real-Time Packet Loss Concealment With Mixed Generative and Predictive Model]] — uses the improved low-complexity LPCNet variant with causal features
