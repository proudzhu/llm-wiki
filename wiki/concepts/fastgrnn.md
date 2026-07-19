---
type: concept
created: 2026-07-19
updated: 2026-07-19
tags:
  - deep-learning
  - recurrent-neural-network
  - gated-rnn
  - low-complexity
---

# FastGRNN

**FastGRNN** is a lightweight gated recurrent neural network architecture proposed by Kusupati et al. (NeurIPS 2018) that achieves accuracy comparable to GRUs and LSTMs at 2–4× fewer parameters and faster inference. Its central idea is a **weighted residual connection** that reuses the same weight matrices for both the candidate hidden-state update and the gating operation, halving the recurrent parameter count relative to a GRU at the same hidden size.

## State Update Equations

For input $x_t$ and previous hidden state $h_{t-1}$, with shared weight matrices $W$, $U$, biases $b_z, b_h$, nonlinearity $\sigma$, and two scalar trainable parameters $\zeta, \nu \in [0, 1] \in \mathbb{R}$:

$$
z_t = \sigma(W x_t + U h_{t-1} + b_z)
$$

$$
\tilde{h}_t = \tanh(W x_t + U h_{t-1} + b_h)
$$

$$
h_t = (\zeta (1 - z_t) + \nu) \odot \tilde{h}_t + z_t \odot h_{t-1}
$$

The gate $z_t$ and candidate $\tilde{h}_t$ share the same $W x_t + U h_{t-1}$ projection (with different biases), reducing parameters and promoting well-conditioned gradients.

## Properties

- **Training stability**: Provably stable training, independent of sequence length (under the original paper's assumptions).
- **Small footprint**: Originally targeted at kilobyte-sized RNNs for resource-constrained edge deployment.
- **Length-invariance claim**: The original evaluation validated performance only on sequences up to 1.63 s.

## Known Failure Mode: Inference-Time State Drift on Long Sequences

[[sources/larraza-2026-fast-ulcnet-speech-enhancement|Larraza & de Koeijer 2026]] report that FastGRNN, when applied to >60 s audio signals for speech enhancement, exhibits a monotonic growth of the mean hidden-state magnitude over time during inference, with measurable degradation in enhancement quality. The drift is traced to the state update equation: the coefficients of $\tilde{h}_t$ and $h_{t-1}$ do **not** satisfy a sum-to-one constraint, so the state lacks a contraction guarantee over long inference horizons. The provable training-time stability does **not** transfer to the inference-time forward pass.

This motivated the proposed [[concepts/comfi-fastgrnn|Comfi-FastGRNN]] extension, which adds a trainable complementary filter to mitigate the drift.

## Related Concepts

- [[concepts/comfi-fastgrnn|Comfi-FastGRNN]]
- [[concepts/fast-ulcnet|Fast-ULCNet]]
- [[concepts/ulcnet|ULCNet]]
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/larraza-2026-fast-ulcnet-speech-enhancement|Larraza & de Koeijer 2026: Fast-ULCNet]]
