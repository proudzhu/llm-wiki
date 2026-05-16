---
type: concept
created: 2026-04-12
updated: 2026-04-17
sources:
- raw/articles/Forward propagation of errors through time.md
tags:
- machine-learning
- neural-networks
- optimization
---

# Real-Time Recurrent Learning

**Real-Time Recurrent Learning (RTRL)** is an online algorithm for computing exact gradients in Recurrent Neural Networks (RNNs) without the need for unrolling through time.

## Overview

Unlike [[backpropagation-through-time|Backpropagation Through Time]] (BPTT), which propagates errors backward after a sequence is processed, RTRL propagates the **sensitivity of the state with respect to parameters** forward in time. This allows the network to learn while it processes data, making it suitable for continuous, lifelong learning tasks.

## Complexity

The primary drawback of RTRL is its high computational and memory cost:
- **Memory**: $O(N^3)$ (storing the Jacobian of the state with respect to all weights).
- **Time**: $O(N^4)$ per time step for a fully connected RNN with $N$ neurons.

Because of this $O(N^4)$ scaling, exact RTRL is only feasible for very small networks.

## Approximations and Modern Variations

- **Diagonal/Sparse RTRL**: Reducing the number of tracked sensitivities to improve efficiency (e.g., $O(N^2)$), though this makes the gradients inexact.
- **SnAp (Sparse n-step Approximation)**: A middle ground between BPTT and RTRL.
- **FPTT (Forward Propagation of Errors Through Time)**: A recent attempt to achieve exact forward gradients with $O(N^3)$ complexity by reversing the BPTT equation. However, it is fundamentally unstable in networks that exhibit "forgetting" (Zucchet 2026).

## Comparison with BPTT

| Feature | BPTT | RTRL |
|---------|------|------|
| **Direction** | Backward | Forward |
| **Timing** | Offline / Truncated | Real-time / Online |
| **Memory** | $O(T)$ | $O(N^3)$ |
| **Gradients** | Exact | Exact |

## Related Concepts

- [[backpropagation-through-time|Backpropagation Through Time]]
- [[linear-recurrent-unit|Linear Recurrent Unit]]
- [[state-space-model|State-Space Model]]

## Related Sources

- [[sources/zucchet-2026-forward-propagation-errors-through-time|Zucchet 2026: Forward Propagation of Errors Through Time]]
