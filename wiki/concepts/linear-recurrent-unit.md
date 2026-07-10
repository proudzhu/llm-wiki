---
type: concept
created: 2026-04-12
updated: 2026-04-17
sources:
- raw/articles/Forward propagation of errors through time.md
tags:
- machine-learning
- neural-networks
- ssm
---

# Linear Recurrent Unit

The **Linear Recurrent Unit (LRU)** is a specialized recurrent layer designed to handle long-range dependencies efficiently while avoiding the vanishing and exploding gradient problems typical of standard RNNs.

## Overview

The LRU is part of a broader class of models known as **Linear Recurrent Networks** or **State-Space Models (SSMs)**. Unlike standard RNNs that use nonlinear activations (like `tanh` or `ReLU`) inside the recurrence, the LRU uses a purely **linear recurrence**:
$$ h_t = A h_{t-1} + B x_t $$
$$ y_t = C h_t + D x_t $$
Nonlinearity is typically added outside the recurrence (e.g., in a gated MLP block).

## Key Features

1. **Stability**: By constraining the eigenvalues of the state-transition matrix $A$ to be within the unit circle ($|\lambda| < 1$), the model is guaranteed to be stable and avoid exploding gradients.
2. **Parallelization**: Because the recurrence is linear, it can be computed extremely efficiently on GPUs using a **parallel associative scan**, reducing the $O(T)$ sequential bottleneck to $O(\log T)$.
3. **Continuous-Time Foundation**: LRUs are often derived from discretizing continuous-time linear differential equations, allowing them to handle irregular sampling or high-resolution data effectively.
4. **Numerical Precision**: Modern LRUs use complex-valued diagonal matrices for $A$, which helps in capturing oscillating patterns and reduces the number of parameters.

## Relationship to FPTT

Research by Zucchet (2026) suggests that for stable linear systems like the LRU (where $|A| < 1$), forward error propagation (FPTT) is fundamentally **numerically unstable**. This is because FPTT requires inverting the transition matrix ($A^{-1}$), which causes any small error to be exponentially amplified by $\lambda^{-T}$. This reinforces [[backpropagation-through-time|Backpropagation Through Time]] (BPTT) as the only numerically sound exact gradient method for such "forgetting" systems.

## Related Recurrent Architectures

[[concepts/mingru|MinGRU]] is a related minimal gated recurrence that can also be expressed as a linear recurrence and parallelized via associative scan. It is used as the temporal mixer in the [[concepts/mamba-mingru|Mamba-MinGRU]] architecture for [[concepts/own-voice-cancellation|own-voice cancellation]], achieving 2 ms algorithmic latency with compute efficiency far exceeding ConvTasNet-based baselines.

## Related Concepts

- [[concepts/mingru|MinGRU]]
- [[concepts/mamba-mingru|Mamba-MinGRU]]
- [[backpropagation-through-time|Backpropagation Through Time]]
- [[state-space-model|State-Space Model]]
- [[real-time-recurrent-learning|Real-Time Recurrent Learning]]

## Related Sources

- [[sources/ostergaard-2026-own-voice-cancellation|Østergaard et al. 2026: Don't Listen to Me — Own-Voice Cancellation]]
- [[sources/zucchet-2026-forward-propagation-errors-through-time|Zucchet 2026: Forward Propagation of Errors Through Time]]
