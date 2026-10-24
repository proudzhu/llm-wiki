---
type: concept
created: 2026-10-24
updated: 2026-10-24
sources:
  - raw/papers/westhausen-2022-tplcnet/full-text.md
tags:
  - packet-loss-concealment
  - seq2one
  - recurrent-neural-network
  - gated-recurrent-unit
  - time-domain-model
  - real-time
  - low-complexity
  - neural-network-architecture
---

# tPLCnet

**tPLCnet** is a time-domain neural network for real-time [[concepts/packet-loss-concealment|packet loss concealment]], introduced by [[sources/westhausen-2022-tplcnet|Westhausen & Meyer 2022]] (Interspeech 2022). Its defining feature is the **sequence-to-one (seq2one)** operating mode: instead of running continuous inference on every incoming audio frame, the model is **triggered only when a packet loss is detected** and predicts the entire missing 10 ms frame from a short context buffer in one shot.

## Key Formulations

The model reads a context buffer of $n$ non-overlapping 10 ms frames (160 samples at 16 kHz; $n = 6$ chosen) and predicts one 320-sample (2 × 10 ms) frame, which is Hann-windowed and overlap-added into the output stream. During consecutive losses, the current output frame is **written back to the context buffer**, so subsequent predictions consume earlier predictions.

Training uses a combined magnitude + complex mean-absolute-error loss in the time-frequency domain applied to the whole enhanced utterance:

$$
\mathrm{MAE_{comb}}=(1-\alpha)\big||\hat{X}|-|X|\big|+\alpha|\hat{X}-X|, \qquad \alpha=0.1,
$$

with an STFT window of 32 ms at 50 % overlap (best PLC-MOS among tested configurations). A pure time-domain MAE was clearly inferior (PLC-MOS 3.30 vs. 3.90).

## Architecture

Per frame: FC encoding (512 units, ReLU — mapping to a non-negative feature space following TasNet) → FC embedding (128/256/512 for Small/Medium/Large, Leaky-ReLU); then along the buffer: two Conv1D layers (kernels 4 and 2, zero-padded) → two **bidirectional GRU** layers (64/128/256 units) whose final hidden state feeds two FC mapping layers (512, Leaky-ReLU) and a linear FC decoding layer (320 outputs). The topology adapts the [[concepts/nsnet2|NSNet2]] FC+GRU pattern and the time-domain convolutional recurrent network of Lin et al. (ICASSP 2021) to the seq2one task; the BGRUs let the model use information from the whole buffer despite predicting a single frame.

| Configuration | MACs per 10 ms frame | Execution time (Intel i5-7267U) | PLC-MOS (known test set) |
|---------------|----------------------|-------------------------------|---------------------------|
| FF baseline (flatten + 3×FC-512) | 2.49 M | 0.47 ms | 3.81 |
| Small | 2.96 M | 0.57 ms | 3.86 |
| Medium | 7.85 M | 1.41 ms | 3.90 |
| Large | 26.18 M | 3.95 ms | 3.95 |

## Key Findings

- **On-demand inference** — because the network runs only at loss time, the compute cost scales with the actual loss rate rather than the full audio stream, suiting battery-powered devices.
- **Short context suffices** — performance peaks at 6–7 buffer frames (~60–70 ms) and *degrades* for long buffers (15–20 frames); PLC-relevant information is temporally localized around the lost frame.
- **Complexity saturation** — the feed-forward baseline already achieves robust PLC (3.81), so most of the gain comes from the general approach + training setup; the model size can be matched to device resources.
- **Mixed-context training** — sampling the most recent buffer frames from degraded audio and older frames from clean audio during training improves robustness to imperfect (previously concealed) buffer content.

## Position in PLC Evolution

tPLCnet is the **informed, 16 kHz, on-demand prediction** entry in the neural PLC lineage: it ranked 3rd (tied) in the Interspeech 2022 Audio Deep PLC Challenge with the second-best PLC-MOS (3.976). Compared with [[concepts/dnn-regression-plc|DNN regression PLC]] (Lee & Chang 2016 — feed-forward regression of spectral features), it predicts raw time-domain frames with a recurrent sequence model; compared with the hybrid vocoder approach of Valin et al. 2022 (2nd place, same challenge) it is vocoder-free and event-triggered; the later blind full-band [[concepts/full-band-recurrent-network|FRN]] (Nguyen, Nguyen & Khong 2023) showed that a continuous-inference model without loss metadata can outperform it at 48 kHz — at higher complexity.

## Related Concepts

- [[concepts/packet-loss-concealment|Packet Loss Concealment]] — the umbrella task
- [[concepts/gated-recurrent-unit|Gated Recurrent Unit]] — the bidirectional sequence-modeling core
- [[concepts/frequency-domain-loss|Frequency Domain Loss]] — the TF-domain training objective for the time-domain model
- [[concepts/nsnet2|NSNet2]] — architectural inspiration (FC+GRU topology)
- [[concepts/dnn-regression-plc|DNN Regression PLC]] — earlier frame-regression PLC paradigm
- [[concepts/full-band-recurrent-network|Full-Band Recurrent Network (FRN)]] — later blind full-band PLC that benchmarks against tPLCnet
- [[concepts/time-domain-speech-enhancement|Time-Domain Speech Enhancement]] — broader context

## Related Sources

- [[sources/westhausen-2022-tplcnet|Westhausen & Meyer 2022: tPLCnet — Real-Time Deep Packet Loss Concealment in the Time Domain]] — introduces the architecture
- [[sources/nguyen-2023-predictive-plc|Nguyen, Nguyen & Khong 2023: Full-Band Blind Packet-Loss Concealment With Predictive Network]] — reimplements tPLCnet as the informed baseline
- [[sources/valin-2022-real-time-plc|Valin et al. 2022: Real-Time Packet Loss Concealment]] — the 2nd-place hybrid vocoder system from the same challenge
