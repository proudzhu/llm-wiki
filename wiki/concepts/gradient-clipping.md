---
type: concept
created: 2026-07-18
updated: 2026-07-18
sources:
  - raw/papers/mienye-2024-rnn-comprehensive-review/full-text.md
tags:
  - deep-learning
  - optimization
  - training
  - gradient
---

# Gradient Clipping

**Gradient clipping** is a technique used to prevent gradients from becoming too large during training, which can destabilize the training of [[concepts/recurrent-neural-network\|recurrent neural networks]] (especially the exploding gradient problem).

## Formulation

Given a gradient $\mathbf{g}$ and a threshold $\tau$, gradient clipping rescales the gradient if its norm exceeds $\tau$:

$$
\mathbf{g} \leftarrow \frac{\mathbf{g}}{\max\left(1, \frac{\|\mathbf{g}\|}{\tau}\right)}. \tag{1}
$$

If $\|\mathbf{g}\| \leq \tau$, the gradient is unchanged. If $\|\mathbf{g}\| > \tau$, the gradient is rescaled to have norm $\tau$, preserving its direction.

## Variants

- **Norm clipping** (above) — rescales by global norm; most common
- **Value clipping** — clips each element of the gradient to $[-c, c]$ independently
- **Adaptive clipping** — adjusts threshold based on training statistics

## Use in RNN Training

Gradient clipping is commonly used when training [[concepts/long-short-term-memory\|LSTM]], [[concepts/gated-recurrent-unit\|GRU]], and vanilla [[concepts/recurrent-neural-network\|RNNs]] with [[concepts/backpropagation-through-time\|BPTT]] to mitigate exploding gradients. It is often combined with the [[concepts/adam-optimizer\|Adam optimizer]] and is a standard feature in deep learning frameworks (e.g., `torch.nn.utils.clip_grad_norm_`).

## Distinction from Gated Architectures

Gradient clipping addresses only the **exploding** gradient problem. The **vanishing** gradient problem requires architectural solutions such as LSTM/GRU gating, [[concepts/independently-recurrent-neural-network\|IndRNN]]'s element-wise recurrence, or [[concepts/linear-recurrent-unit\|Linear Recurrent Units]] with constrained eigenvalues.

## Related Concepts

- [[concepts/recurrent-neural-network\|Recurrent Neural Network]]
- [[concepts/vanishing-gradient-problem\|Vanishing/Exploding Gradient Problem]]
- [[concepts/backpropagation-through-time\|Backpropagation Through Time]]
- [[concepts/adam-optimizer\|Adam Optimizer]]
- [[concepts/long-short-term-memory\|Long Short-Term Memory (LSTM)]]

## Related Sources

- [[sources/mienye-2024-rnn-comprehensive-review\|Mienye, Swart & Obaido 2024: RNN Comprehensive Review]] — Section 5.3 covers gradient clipping as an advanced optimization technique for RNNs
