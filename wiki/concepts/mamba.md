---
type: concept
created: 2026-08-03
updated: 2026-08-03
sources:
  - raw/papers/chao-2024-mamba-speech-enhancement/full-text.md
tags:
  - neural-network
  - state-space-model
  - deep-learning
  - sequence-modeling
  - selective-ssm
  - linear-time
---

# Mamba

**Mamba** is a selective state-space model (SSM) architecture introduced by Gu & Dao (2023) that addresses the key limitation of earlier structured state-space models (such as [[concepts/s4nd|S4]]): the inability to perform **input-dependent (content-based) filtering**. While S4's parameters are fixed after training, Mamba makes the SSM parameters a function of the input, allowing it to selectively remember or forget information based on content — analogous to the gating mechanism in [[concepts/long-short-term-memory|LSTMs]] but with linear-time scaling. Mamba has become a popular attention-free alternative to Transformers for long-sequence modeling, scaling linearly in sequence length rather than quadratically.

## Mathematical Formulation

Mamba operates by mapping an input sequence $x$ to an output $y$ through a higher-dimensional latent state $h$ via the structured state-space recurrence:

$$h_n = \bar{\mathbf{A}}\, h_{n-1} + \bar{\mathbf{B}}\, x_n, \qquad y_n = \mathbf{C}\, h_n$$

where $(\bar{\mathbf{A}}, \bar{\mathbf{B}})$ are the **discretized** state matrices obtained from continuous parameters $(\Delta, \mathbf{A}, \mathbf{B})$ via a zeroth-order hold discretization:

$$\bar{\mathbf{A}} = \exp(\Delta \mathbf{A}), \qquad \bar{\mathbf{B}} = (\Delta \mathbf{A})^{-1}(\exp(\Delta \mathbf{A}) - \mathbf{I}) \cdot \Delta \mathbf{B}$$

### The selection mechanism

The defining innovation of Mamba is that the SSM parameters — in particular $\mathbf{B}$, $\mathbf{C}$, and the step size $\Delta$ — are made **input-dependent** (i.e., functions of $x_n$), rather than fixed:

$$\mathbf{B} = \text{Linear}_B(x_n), \qquad \mathbf{C} = \text{Linear}_C(x_n), \qquad \Delta = \text{softplus}(\text{Linear}_\Delta(x_n))$$

This means the model can:
- **Variable $\Delta$**: Adjust the "resolution" at which it samples the input — small $\Delta$ ignores fine details (compression), large $\Delta$ reconstructs individual tokens (precise recall).
- **Variable $\mathbf{B}, \mathbf{C}$**: Selectively write to or read from the latent state based on content, enabling long-range filtering.

### Hardware-aware scan

Because the input-dependent parameters break the time-invariance that made S4's FFT convolution possible, Mamba instead computes the recurrence via a **parallel associative scan** that scales linearly, $O(N)$, with sequence length $N$ — and is implemented in a hardware-aware (SRAM-aware) CUDA kernel that avoids the I/O bottleneck of materializing the full state tensor in HBM.

## Architecture

A Mamba block integrates components from the H3 architecture with a gated MLP into a stacked structure:

1. **Linear expansion** — project the input into a higher-dimensional representation
2. **Conv1D** — short temporal convolution for local context
3. **SiLU activation**
4. **Selective SSM** — the input-parameterized recurrence above
5. **Gated multiplication** with a SiLU-gated branch
6. **Linear projection** back to the input dimension
7. **Residual connection**

Most parameters live in the linear projections, while the inner SSM is parameter-light. The block uses standard LayerNorm and residual connections.

## Properties

| Property | Value |
|----------|-------|
| Time complexity (training) | $O(N)$ — linear in sequence length |
| Time complexity (inference) | $O(1)$ per token (no KV cache) |
| Memory | Stateful, $O(1)$ inference memory per token |
| Selection | Input-dependent, content-based filtering |
| Causality | Causal by default; bidirectional via Hydra/flip-and-concat |

## Relation to Other Sequence Models

- **vs. Transformer**: Mamba avoids the $O(N^2)$ self-attention cost; scales linearly; no KV cache at inference. In practice it has been shown to match or exceed Transformer quality on long-context tasks (language, genomics) and, in [[concepts/semamba|SEMamba]], to match Conformer PESQ at lower FLOPs for speech enhancement.
- **vs. [[concepts/s4nd|S4]]/S4ND**: S4 is a structured SSM with fixed parameters; it cannot perform input-dependent filtering. Mamba generalizes S4 by adding the selection mechanism.
- **vs. [[concepts/long-short-term-memory|LSTM]]**: LSTMs also use input-dependent gating, but they use saturating nonlinearities ($\tanh$) and scale $O(N)$ with bounded state size. Mamba uses linear gates and a high-dimensional state, with parallel training via associative scan.
- **vs. [[concepts/linear-recurrent-unit|LRU]]/MinGRU**: LRU and [[concepts/mingru|MinGRU]] are linear-recurrence architectures that, like Mamba, enable parallel training via scan; Mamba adds the input-dependent selection that LRU/MinGRU lack. [[concepts/mamba-mingru|Mamba-MinGRU]] combines Mamba blocks with MinGRU recurrence.

## Use in Speech Enhancement

[[concepts/semamba|SEMamba]] (Chao et al., IEEE SLT 2024) is the **first work to apply Mamba to speech enhancement**. It deploys Mamba in both a basic magnitude-mapping architecture and an advanced magnitude-phase architecture (replacing MP-SENet's Conformer), achieving a new state-of-the-art PESQ of 3.69 on the VoiceBank-DEMAND benchmark. See [[concepts/semamba|SEMamba]] for details.

## Related Concepts

- [[concepts/state-space-model|State-Space Model]] — the broader SSM family
- [[concepts/s4nd|S4ND]] — predecessor structured SSM (no selection)
- [[concepts/semamba|SEMamba]] — first Mamba-based speech enhancement system
- [[concepts/mamba-mingru|Mamba-MinGRU]] — Mamba + MinGRU hybrid for own-voice cancellation
- [[concepts/long-short-term-memory|LSTM]] — recurrent baseline with input-dependent gating
- [[concepts/linear-recurrent-unit|Linear Recurrent Unit]] — linear-recurrence alternative
- [[concepts/mingru|MinGRU]] — minimal GRU linear recurrence

## Related Sources

- [[sources/chao-2024-mamba-speech-enhancement|Chao et al. 2024: An Investigation of Incorporating Mamba for Speech Enhancement]]
