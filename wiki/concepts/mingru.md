---
type: concept
created: 2026-07-10
updated: 2026-07-10
sources:
  - raw/papers/ostergaard-2026-own-voice-cancellation/full-text.md
tags:
  - neural-network
  - recurrent-neural-network
  - linear-recurrence
  - state-space-model
  - efficient-inference
---

# MinGRU

**MinGRU** is a minimal gated recurrent neural network proposed by Feng et al. (2024) in "Were RNNs All We Needed?". It reduces the classical GRU to its essential components, yielding a recurrence that can be expressed as a **linear recurrence**, enabling efficient parallel training via a parallel associative scan while retaining the streaming capability of classical RNNs.

## Formulation

The MinGRU recurrence is:

$$\mathbf{h}_{t} = (1 - \mathbf{z}_{t}) \odot \mathbf{h}_{t-1} + \mathbf{z}_{t} \odot \tilde{\mathbf{h}}_{t}$$

where:
- $\mathbf{z}_t$ — update gate
- $\tilde{\mathbf{h}}_t$ — candidate hidden state
- $\mathbf{h}_t$ — hidden state

This can be rewritten as a linear recurrence:

$$\mathbf{h}_{t} = \text{gates} \odot \mathbf{h}_{t-1} + \text{tokens}$$

with $\text{gates} = (1 - \mathbf{z}_t)$ and $\text{tokens} = \mathbf{z}_t \odot \tilde{\mathbf{h}}_t$.

## Key Properties

| Property | Description |
|----------|-------------|
| **Linear recurrence** | Can be parallelized via associative scan ($O(\log T)$) |
| **Streaming** | Retains causal, step-by-step inference of classical RNNs |
| **Minimal** | Fewer gates than GRU/LSTM, reducing parameter count |
| **Bidirectional** | Can be made bidirectional (e.g., via Hydra) |

## Relationship to Other Architectures

MinGRU is part of the broader family of [[concepts/linear-recurrent-unit|linear recurrent networks]] and [[concepts/state-space-model|state-space models]] that have emerged as compute-efficient alternatives to transformers. It is used as the **temporal mixer** within the [[concepts/mamba-mingru|Mamba-MinGRU]] architecture, where Mamba blocks provide the overall structure and MinGRU handles temporal mixing.

## Related Concepts

- [[concepts/linear-recurrent-unit|Linear Recurrent Unit]]
- [[concepts/state-space-model|State-Space Model]]
- [[concepts/mamba-mingru|Mamba-MinGRU]]
- [[concepts/own-voice-cancellation|Own-Voice Cancellation (OVC)]]

## Related Sources

- [[sources/ostergaard-2026-own-voice-cancellation|Østergaard et al. 2026: Don't Listen to Me — Own-Voice Cancellation]]
