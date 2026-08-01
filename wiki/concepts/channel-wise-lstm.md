---
type: concept
created: 2026-08-01
updated: 2026-08-01
sources:
  - raw/papers/liu-2021-igcrn/full-text.md
tags:
  - neural-network
  - recurrent-network
  - lstm
  - speech-enhancement
  - multi-channel
  - inplace-model
---

# Channel-wise LSTM with Model Reuse

The **channel-wise LSTM** (sometimes abbreviated chLSTM) is the recurrent bottleneck used in [[concepts/igcrn|IGCRN]] (Liu & Zhang, Interspeech 2021) and inherited by [[concepts/iccrn|ICCRN]] (Liu & Zhang, ICASSP 2023). Unlike the conventional [[concepts/convolutional-recurrent-network|CRN]] LSTM, which processes the entire flattened frequency × channel feature as a single time series, the channel-wise LSTM processes **each frequency bin independently** — the frequency dimension is folded into the batch dimension so the LSTM only sees the per-bin channel feature at each time step. Combined with the **model reuse mechanism** (a single LSTM shared across all frequency bins), this makes the inplace-CRN family extremely compact while preserving per-bin spatial cues.

## Motivation

In a multi-channel speech enhancement system, the spatial information that the array provides lives in the per-frequency-bin channel dimension (the relative phase and amplitude between microphones). A [[concepts/beamforming|beamformer]] applies a per-bin spatial filter, and the spatial filter for a given look direction depends only on the per-bin channel feature — not on neighboring frequency bins.

A conventional CRN's full-band LSTM, by contrast, mixes information across all frequency bins at every time step. While this is useful for capturing harmonic structure in single-channel SE, it obscures the per-bin spatial information that a multi-channel system needs to act like a beamformer.

The channel-wise LSTM restores the per-bin processing: each frequency bin is processed by its own (virtual) LSTM, so the spatial information in each bin is processed independently — exactly as a beamformer would.

## Model Reuse Mechanism

A naive channel-wise LSTM would use a separate LSTM per frequency bin, which is parameter-prohibitive (256 frequency bins × LSTM parameters). IGCRN exploits a key physical observation to avoid this:

> The time delay for a given look direction is the same across all frequency bins — only the phase compensation differs, and the LSTM does not need phase compensation (it analyzes spatial cues via time delay directly).

Therefore, **one LSTM can be reused for all frequency bins**. In IGCRN this means a single 2-layer Bi-LSTM with hidden size 64 processes all 256 frequency bins (by folding the frequency dimension into the batch dimension), instead of the conventional CRN's single LSTM with hidden size 1024 over the flattened feature.

## Mathematical / Implementation View

Given an encoder output feature of shape `[Batch, Channel, Frequency, Time]`, the channel-wise LSTM:

1. **Reshapes** to `[Batch × Frequency, Time, Channel]` — folding the frequency dimension into the batch dimension.
2. **Applies a (bidirectional) LSTM** to the time dimension, processing each (batch, frequency) pair independently.
3. **Reshapes** back to `[Batch, Channel', Frequency, Time]`.

In IGCRN, the LSTM is a 2-layer Bi-LSTM with hidden size 64 (input channel 64, output 128), followed by a linear projection back to channel 64. The reuse mechanism means the same LSTM weights are applied to all 256 frequency bins — the network learns a single per-bin spatial filter that generalizes across frequencies.

## Parameter Efficiency

The reuse mechanism is the main source of IGCRN's compactness:

| Model | LSTM hidden | Params (M) | MAC (G) |
|-------|-------------|------------|---------|
| GCRN (conventional) | 1024 | 71.8 | 28.8 |
| **IGCRN64** (proposed) | 64 | 1.4 | 19.9 |

IGCRN has ~50× fewer parameters and ~30 % fewer MACs than GCRN, despite being the larger-performing model on dual-channel SE. The savings come from (a) skipping the frequency-downsampling channel expansion that downsampling CRNs require and (b) sharing one 64-hidden LSTM across all 256 frequency bins instead of one 1024-hidden LSTM over the flattened feature.

## Use in the Inplace-CRN Family

- **[[concepts/igcrn|IGCRN]]** (Liu & Zhang 2021) — introduces the channel-wise LSTM with model reuse as the bottleneck of the inplace CRN. Two-layer Bi-LSTM, hidden 64, frequency-fold-into-batch reshape.
- **[[concepts/iccrn|ICCRN]]** (Liu & Zhang 2023) — inherits the channel-wise LSTM design but uses it in two roles:
    - **F-chBLSTM** (frequency-channel-wise BLSTM) at the encoder projection, lifting the 2-channel input to a higher-dimensional feature.
    - **T-chLSTM** (time-channel-wise LSTM) at the bottleneck, computing a mask multiplied with the encoder output (a 2-layer T-chLSTM with hidden $2c$).
    - **Ceps-chBLSTM** (cepstral-channel-wise BLSTM) inside the [[concepts/cepstral-frequency-block|Cepstral Frequency Block]], processing cepstral bins (instead of frequency bins) as a sequence within each frame.

The "channel-wise" terminology in the ICCRN paper is therefore overloaded: in IGCRN it means per-frequency-bin; in ICCRN it means per-(frequency|cepstral)-bin depending on the block, but the design principle — process each bin independently and reuse the LSTM across bins — is the same.

## Related Concepts

- [[concepts/igcrn|IGCRN]] — the model that introduces the channel-wise LSTM with model reuse
- [[concepts/inplace-convolution|Inplace Convolution]] — the encoder/decoder design that makes channel-wise LSTM effective (preserves per-bin spatial cues)
- [[concepts/iccrn|ICCRN]] — successor that uses channel-wise LSTMs in three roles
- [[concepts/cepstral-frequency-block|Cepstral Frequency Block (CFB)]] — ICCRN's novel block that uses a Ceps-chBLSTM variant
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — the conventional CRN that uses a full-band LSTM
- [[concepts/beamforming|Beamforming]] — the per-frequency-bin processing that motivates the design
- [[concepts/long-short-term-memory|Long Short-Term Memory]] — the underlying recurrent cell

## Related Sources

- [[sources/liu-2021-igcrn|Liu & Zhang 2021: IGCRN — Inplace Gated Convolutional Recurrent Neural Network]]
- [[sources/liu-2023-iccrn|Liu & Zhang 2023: ICCRN — Inplace Cepstral Convolutional Recurrent Neural Network]]
