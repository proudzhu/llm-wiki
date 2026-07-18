---
type: concept
created: 2026-07-18
updated: 2026-07-18
sources:
  - raw/papers/mienye-2024-rnn-comprehensive-review/full-text.md
tags:
  - deep-learning
  - machine-learning
  - neural-networks
  - sequential-data
---

# Recurrent Neural Network

A **Recurrent Neural Network (RNN)** is a class of deep learning models designed to process **sequential data** by maintaining an internal hidden state that captures information about previous inputs. Unlike feedforward neural networks, RNNs have recurrent connections that allow information to cycle within the network, making them suited for tasks where context and order matter: natural language processing, speech recognition, time-series forecasting, and related domains.

## Basic Architecture

At each time step $t$, the RNN takes an input vector $\mathbf{x}_t$ and updates its hidden state $\mathbf{h}_t$ using:

$$
\mathbf{h}_t = \sigma_h(\mathbf{W}_{xh}\mathbf{x}_t + \mathbf{W}_{hh}\mathbf{h}_{t-1} + \mathbf{b}_h), \tag{1}
$$

$$
\mathbf{y}_t = \sigma_y(\mathbf{W}_{hy}\mathbf{h}_t + \mathbf{b}_y), \tag{2}
$$

where $\mathbf{W}_{xh}$ is the input-to-hidden weight matrix, $\mathbf{W}_{hh}$ is the recurrent weight matrix, $\mathbf{W}_{hy}$ is the hidden-to-output weight matrix, $\mathbf{b}_h, \mathbf{b}_y$ are bias vectors, and $\sigma_h, \sigma_y$ are activation functions (typically tanh, ReLU, or sigmoid).

Training is performed via [[concepts/backpropagation-through-time\|Backpropagation Through Time (BPTT)]], which unrolls the network across time steps and applies standard backpropagation.

## Key Variants

| Variant | Key feature | Reference |
|---------|-------------|-----------|
| [[concepts/long-short-term-memory\|LSTM]] | Input/forget/output gates regulate cell state | Hochreiter & Schmidhuber 1997 |
| [[concepts/gated-recurrent-unit\|GRU]] | Update/reset gates; merged cell/hidden state | Cho et al. 2014 |
| [[concepts/bidirectional-lstm\|BiLSTM]] / BiRNN | Forward + backward passes for full context | Schuster & Paliwal 1997 |
| Stacked (Deep) RNN | Multiple recurrent layers | — |
| [[concepts/peephole-lstm\|Peephole LSTM]] | Gates have direct access to cell state | Gers & Schmidhuber 2000 |
| [[concepts/echo-state-network\|Echo State Network]] | Fixed random reservoir; only output trained | Jaeger 2001 |
| [[concepts/independently-recurrent-neural-network\|IndRNN]] | Element-wise recurrent weights for deep stacks | Li et al. 2018 |

## Major Challenges

- **Vanishing/exploding gradients** during BPTT — addressed by gated variants (LSTM/GRU), [[concepts/gradient-clipping\|gradient clipping]], and modern alternatives like [[concepts/linear-recurrent-unit\|Linear Recurrent Units]].
- **Sequential bottleneck** — RNNs cannot be parallelized across time as easily as [[concepts/attention-mechanism\|transformers]], limiting scalability on long sequences.
- **Memory cost** — BPTT requires $O(T)$ memory to store hidden states.

## Modern Descendants (not covered in the source review)

The 2024 review by [[sources/mienye-2024-rnn-comprehensive-review\|Mienye et al.]] does not cover more recent efficient RNN variants that have emerged from the state-space model literature:

- [[concepts/linear-recurrent-unit\|Linear Recurrent Unit (LRU)]] — purely linear recurrence parallelizable via associative scan
- [[concepts/mingru\|MinGRU]] — minimal gated recurrence
- [[concepts/mamba-mingru\|Mamba-MinGRU]] — used for own-voice cancellation at 2 ms latency
- [[concepts/state-space-model\|State-Space Models]] (S4, Mamba) — continuous-time linear recurrence discretized for sequence modeling

## Applications

RNNs have been applied across seven major domains surveyed in [[sources/mienye-2024-rnn-comprehensive-review\|Mienye et al. 2024]]: NLP (text generation, sentiment analysis, machine translation), speech recognition, time-series forecasting, signal processing, bioinformatics, autonomous vehicles, and anomaly detection. Within the llm-wiki, RNN-based systems appear in:

- [[concepts/percepnet\|PercepNet]] (Valin et al. 2021) — GRU-based neural post filter for AEC
- [[concepts/nsnet2\|NSNet2]] — FC+GRU speech enhancement baseline
- [[concepts/convolutional-recurrent-network\|Convolutional Recurrent Network (CRN)]] — CNN+RNN hybrid for speech enhancement
- [[concepts/grouped-recurrent-neural-network\|Grouped RNN]] — partitioned hidden state for efficiency
- [[concepts/self-attentive-recurrent-neural-network\|Self-Attentive RNN]] — attention-augmented RNN

## Related Concepts

- [[concepts/long-short-term-memory\|Long Short-Term Memory (LSTM)]]
- [[concepts/gated-recurrent-unit\|Gated Recurrent Unit (GRU)]]
- [[concepts/bidirectional-lstm\|Bidirectional LSTM]]
- [[concepts/backpropagation-through-time\|Backpropagation Through Time]]
- [[concepts/vanishing-gradient-problem\|Vanishing/Exploding Gradient Problem]]
- [[concepts/activation-functions\|Activation Functions]]
- [[concepts/echo-state-network\|Echo State Network]]
- [[concepts/independently-recurrent-neural-network\|Independently Recurrent Neural Network]]
- [[concepts/attention-mechanism\|Attention Mechanism]]
- [[concepts/neural-networks\|Neural Networks]]
- [[concepts/linear-recurrent-unit\|Linear Recurrent Unit]] — modern efficient descendant
- [[concepts/convolutional-recurrent-network\|Convolutional Recurrent Network]]

## Related Sources

- [[sources/mienye-2024-rnn-comprehensive-review\|Mienye, Swart & Obaido 2024: RNN Comprehensive Review]] — the comprehensive review that anchors this concept page
- [[sources/zucchet-2026-forward-propagation-errors-through-time\|Zucchet 2026: Forward Propagation of Errors Through Time]] — deeper analysis of BPTT alternatives
- [[sources/valin-2021-percepnet-joint-echo-control\|Valin et al. 2021: PercepNet]] — RNN-based AEC system
