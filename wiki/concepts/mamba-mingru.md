---
type: concept
created: 2026-07-10
updated: 2026-07-10
sources:
  - raw/papers/ostergaard-2026-own-voice-cancellation/full-text.md
tags:
  - neural-network
  - linear-rnn
  - state-space-model
  - speech-enhancement
  - low-latency
  - mamba
  - mingru
---

# Mamba-MinGRU

**Mamba-MinGRU** is a compute-efficient neural network architecture for time-domain audio processing that combines **Mamba blocks** (selective state-space model structure) with **[[concepts/mingru|MinGRU]]** as the temporal mixer. It was proposed by Østergaard et al. (2026) for [[concepts/own-voice-cancellation|own-voice cancellation (OVC)]] and achieves performance comparable to ConvTasNet-based baselines at a fraction of the computational cost, with only 2 ms algorithmic latency in causal configurations.

## Architecture

Each Mamba-MinGRU block is a pre-norm residual block consisting of:

1. **LayerNorm** — input normalization
2. **Linear expansion** — expand by factor $K$, split into $y, z$
3. **Causal depthwise 1-D conv + SiLU** — short temporal convolution for local context
4. **[[concepts/mingru|MinGRU]] recurrence** — time mixing via linear recurrence
5. **Gating** — $y \odot \text{SiLU}(z)$
6. **Linear projection** — back to input channels

The full network consists of an initial normalization layer, a projection to $d_{\mathrm{model}}$, $N$ Mamba-MinGRU blocks, and a final projection to the encoder dimension with a Sigmoid non-linearity.

## MinGRU Recurrence

The MinGRU recurrence is given by:

$$\mathbf{h}_{t} = (1 - \mathbf{z}_{t}) \odot \mathbf{h}_{t-1} + \mathbf{z}_{t} \odot \tilde{\mathbf{h}}_{t}$$

where $\mathbf{z}_t$ is a gate and $\tilde{\mathbf{h}}_t$ is the candidate state. This can be rewritten as a **linear recurrence**:

$$\mathbf{h}_{t} = \text{gates} \odot \mathbf{h}_{t-1} + \text{tokens}$$

where $\text{gates} = (1 - \mathbf{z}_t)$ and $\text{tokens} = \mathbf{z}_t \odot \tilde{\mathbf{h}}_t$. This enables efficient parallel training via a **parallel associative scan** ($O(\log T)$ vs $O(T)$ sequential).

Bidirectionality is implemented using **Hydra** bidirectionality.

## Advantages

| Property | Benefit |
|----------|---------|
| Linear recurrence | Parallel training, causal streaming inference |
| Global temporal context | Maintains long-range dependencies |
| Compute efficiency | 0.33 GMAC/s vs 4.97 GMAC/s for ConvTasNet (15× reduction) |
| Low latency | 2 ms algorithmic latency in causal mode |
| Scalability | "Small" variant (half parameters) runs below real-time (RTF 0.82) |

## Configuration

| Variant | $d_{\mathrm{model}}$ | Blocks | Adaptation after | Params (main) | MACs (main) |
|---------|----------------------|--------|-------------------|---------------|-------------|
| Base | 192 | 15 | 8th block | 4.72 M | 0.33 G/s |
| Small | 128 | 15 | 8th block | 2.17 M | 0.18 G/s |

Expansion factor $K = 2.0$ for both variants. The auxiliary network (speaker embedding) can be either ConvTasNet-based or a bidirectional linear RNN (5 blocks).

## Related Concepts

- [[concepts/mingru|MinGRU]]
- [[concepts/linear-recurrent-unit|Linear Recurrent Unit]]
- [[concepts/state-space-model|State-Space Model]]
- [[concepts/own-voice-cancellation|Own-Voice Cancellation (OVC)]]
- [[concepts/td-speakerbeam|TD-SpeakerBeam]]
- [[concepts/time-domain-speech-enhancement|Time-Domain Speech Enhancement]]
- [[concepts/speaker-embedding|Speaker Embedding]]

## Related Sources

- [[sources/ostergaard-2026-own-voice-cancellation|Østergaard et al. 2026: Don't Listen to Me — Own-Voice Cancellation]]
