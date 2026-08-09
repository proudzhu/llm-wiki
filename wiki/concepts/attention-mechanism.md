---
type: concept
created: 2026-07-18
updated: 2026-08-09
sources:
  - raw/papers/mienye-2024-rnn-comprehensive-review/full-text.md
  - raw/papers/liu-2024-lightweight-dl-survey/full-text.md
tags:
  - deep-learning
  - attention
  - sequence-modeling
  - transformer
  - efficient-deep-learning
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

## Efficient Transformer Taxonomy (per Liu et al. 2024)

Self-attention has $O(N^2)$ complexity in sequence length, creating an efficiency bottleneck for resource-constrained deployment. [[sources/liu-2024-lightweight-dl-survey|Liu et al. 2024]] surveys three efficiency directions for vision transformers (§2.3), with quantitative comparison on ImageNet (Table 3):

| Direction | Representative Models | Mechanism |
|-----------|----------------------|-----------|
| **Efficient self-attention** | Sparse Transformer ($O(N\sqrt{N})$), Linformer ($O(N)$), Reformer ($O(N\log N)$) | Reduces the $O(N^2)$ attention complexity |
| **Token sparsing** | T2T-ViT (soft unfolding), DynamicViT (binary mask), EViT (top-K tokens), A-ViT (adaptive token count) | Prunes less-important tokens to reduce per-layer compute; EViT-DeiT-S (k=0.7) achieves highest throughput (5408 img/s) |
| **Lightweight hybrid models** | DeiT (KD from CNN teacher), MobileViT (MobileNetV2 + MobileViT block), MobileFormer (parallel CNN+transformer + cross-attention) | Combines CNN inductive bias with transformer long-range dependence; Mobile-Former-96M has lowest FLOPs (0.096 G), MobileViT-XS lowest params (2.3 M) |

**Key insight from the survey**: lower FLOPs has greater accuracy impact than lower parameters — challenging the assumption that they correlate. Hybrid models achieve extreme lightness but trade off accuracy (MobileViT-XS: 74.8% top-1 vs. MobileViT-S: 78.4%).

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
- [[sources/liu-2024-lightweight-dl-survey\|Liu et al. 2024: Lightweight Deep Learning for Resource-Constrained Environments]] — §2.3 surveys efficient transformers along three directions (efficient self-attention, token sparsing, lightweight hybrid); notes ViT inference on mobile devices is up to 40× slower than CNN, with MatMul and FFN layers as the bottlenecks
