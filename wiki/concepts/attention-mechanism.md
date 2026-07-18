---
type: concept
created: 2026-07-18
updated: 2026-07-18
sources:
  - raw/papers/mienye-2024-rnn-comprehensive-review/full-text.md
tags:
  - deep-learning
  - attention
  - sequence-modeling
  - transformer
---

# Attention Mechanism

The **attention mechanism** allows a neural network to selectively focus on relevant parts of the input sequence when producing each output, addressing the limitations of [[concepts/recurrent-neural-network\|RNNs]] in modeling long-range dependencies. Integrated into RNNs, attention improves performance on tasks such as machine translation and text summarization.

## Formulation

Given a sequence of hidden states $\{\mathbf{h}_1, \dots, \mathbf{h}_T\}$ from the encoder, attention computes a context vector $\mathbf{c}_t$ as a weighted sum:

$$
\mathbf{a}_t = \text{softmax}(\mathbf{u}_t), \tag{1}
$$

$$
\mathbf{c}_t = \sum_{i=1}^T \mathbf{a}_{t,i} \mathbf{h}_i, \tag{2}
$$

where $\mathbf{a}_t$ is the attention weight vector and $\mathbf{u}_t$ is a score function (e.g., dot product, additive, or location-based).

## Self-Attention (Transformer)

The transformer architecture (Vaswani et al., 2017) replaces recurrence entirely with **self-attention**, processing sequences in parallel:

$$
\text{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{softmax}\left(\frac{\mathbf{Q}\mathbf{K}^T}{\sqrt{d_k}}\right)\mathbf{V}, \tag{3}
$$

where $\mathbf{Q}$, $\mathbf{K}$, $\mathbf{V}$ are the query, key, and value matrices, and $d_k$ is the key dimension.

## Variants

- **Bahdanau attention** (additive) — Bahdanau et al. 2014: neural machine translation with RNN+attention
- **Luong attention** (global and local) — Luong et al. 2015: enhanced seq-to-seq performance
- **Self-attention** — Vaswani et al. 2017: transformer, fully attention-based, no recurrence
- **Hybrid RNN+Transformer** — Yang et al. 2017: integrate RNNs into transformer for sequential dependencies + parallel efficiency

## RNN + Attention vs. Transformer

| Property | RNN + Attention | Transformer |
|----------|-----------------|-------------|
| Long-range dependencies | Improved over plain RNN, but still bounded by recurrence | Excellent — direct access to any position |
| Parallelization | Limited (sequential) | Full (parallel) |
| Computational cost | $O(T)$ per step | $O(T^2)$ per layer |
| Resource-constrained settings | Preferred (lower compute) | Resource-intensive |
| Streaming/online | Native | Requires adaptations |

## Applications in the Wiki

Attention mechanisms appear throughout the llm-wiki:
- [[concepts/attention-gate\|Attention Gate]] — used in U-Net-style architectures
- [[concepts/cross-attention-alignment\|Cross-Attention Alignment]] — used in DeepVQE for AEC
- [[concepts/adaptive-time-frequency-attention\|Adaptive Time-Frequency Attention]] — attention in time-frequency speech enhancement
- [[concepts/iterative-attentional-feature-fusion\|Iterative Attentional Feature Fusion]] — multi-stage attention fusion
- [[concepts/self-attentive-recurrent-neural-network\|Self-Attentive RNN]] — RNN augmented with self-attention
- [[concepts/densely-gated-convolutional-attention-network\|Densely Gated Convolutional Attention Network]]

## Related Concepts

- [[concepts/recurrent-neural-network\|Recurrent Neural Network]]
- [[concepts/long-short-term-memory\|Long Short-Term Memory (LSTM)]]
- [[concepts/neural-networks\|Neural Networks]]
- [[concepts/attention-gate\|Attention Gate]]
- [[concepts/cross-attention-alignment\|Cross-Attention Alignment]]

## Related Sources

- [[sources/mienye-2024-rnn-comprehensive-review\|Mienye, Swart & Obaido 2024: RNN Comprehensive Review]] — Section 5.4 covers RNNs with attention mechanisms
- [[sources/indenbom-2023-deepvqe\|Indenbom et al. 2023: DeepVQE]] — uses cross-attention for AEC
