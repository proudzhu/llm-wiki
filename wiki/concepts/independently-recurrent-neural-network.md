---
type: concept
created: 2026-07-18
updated: 2026-07-18
sources:
  - raw/papers/mienye-2024-rnn-comprehensive-review/full-text.md
tags:
  - deep-learning
  - recurrent-neural-network
  - deep-network
  - gradient-stability
---

# Independently Recurrent Neural Network (IndRNN)

The **Independently Recurrent Neural Network (IndRNN)**, proposed by Li et al. (2018), is a recurrent architecture that uses **independent recurrent weights** (element-wise rather than matrix-form recurrence) to address the vanishing and exploding gradient problems, making it easier to train very deep RNNs.

## Architecture

In a standard [[concepts/recurrent-neural-network\|RNN]], the recurrent connection uses a full weight matrix $\mathbf{W}_{hh}$ that mixes all hidden units:

$$
\mathbf{h}_t = \sigma(\mathbf{W}_{xh}\mathbf{x}_t + \mathbf{W}_{hh}\mathbf{h}_{t-1} + \mathbf{b}_h).
$$

In IndRNN, the recurrent weight is replaced by a **vector** $\mathbf{u}$ that acts element-wise on the hidden state:

$$
\mathbf{h}_t = \sigma(\mathbf{W}_{xh}\mathbf{x}_t + \mathbf{u} \odot \mathbf{h}_{t-1}), \tag{1}
$$

where $\odot$ denotes element-wise multiplication. Each neuron in the hidden layer interacts only with its own previous state, decoupling neurons from one another across time steps.

## Advantages

1. **Gradient stability** — because the recurrent weight is element-wise, the Jacobian is diagonal, and the eigenvalue product reduces to a scalar product per neuron. This makes it straightforward to constrain $|u_i| < 1$ to prevent exploding gradients and $|u_i| > 0$ to prevent vanishing gradients, enabling training of very deep RNNs.
2. **Decoupled neurons** — each neuron learns its own temporal pattern, increasing interpretability and allowing different timescales across neurons.
3. **Deep stacking** — IndRNNs can be stacked into very deep networks (dozens of layers) without the instability that plagues standard deep RNNs.

## Applications

Per [[sources/mienye-2024-rnn-comprehensive-review\|Mienye et al. 2024]], IndRNN is particularly suited for **long sequence tasks** such as:
- Video sequence analysis
- Long text generation
- Problems requiring very deep recurrent stacks

## Relationship to Other Architectures

IndRNN can be viewed as a precursor to modern efficient RNN variants that also decouple or linearize the recurrence:
- [[concepts/linear-recurrent-unit\|Linear Recurrent Unit (LRU)]] — uses a diagonal (complex-valued) state-transition matrix, conceptually similar to element-wise recurrence but with complex eigenvalues for oscillatory patterns
- [[concepts/mingru\|MinGRU]] — minimal gated recurrence with parallelizable scan
- [[concepts/state-space-model\|State-Space Models]] (S4, Mamba) — also use diagonal/structured state transitions for parallel training

## Related Concepts

- [[concepts/recurrent-neural-network\|Recurrent Neural Network]]
- [[concepts/long-short-term-memory\|Long Short-Term Memory (LSTM)]]
- [[concepts/gated-recurrent-unit\|Gated Recurrent Unit (GRU)]]
- [[concepts/vanishing-gradient-problem\|Vanishing Gradient Problem]]
- [[concepts/linear-recurrent-unit\|Linear Recurrent Unit]] — modern descendant with similar decoupling principle
- [[concepts/state-space-model\|State-Space Model]]

## Related Sources

- [[sources/mienye-2024-rnn-comprehensive-review\|Mienye, Swart & Obaido 2024: RNN Comprehensive Review]] — surveys IndRNN as a notable RNN variant
