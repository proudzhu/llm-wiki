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

# Backpropagation Through Time

**Backpropagation Through Time (BPTT)** is the standard algorithm used to train Recurrent Neural Networks (RNNs) by unrolling the network in time and applying the backpropagation algorithm.

## Overview

In an RNN, the hidden state $h_t$ depends on the previous hidden state $h_{t-1}$ and the current input $x_t$:
$$ h_t = f_\theta(h_{t-1}, x_t) $$
BPTT treats the RNN as a deep feedforward network with one layer per time step, where each layer shares the same parameters $\theta$. The gradient of the total loss $L$ is computed by propagating errors backward from the final time step to the beginning.

## Limitations

1. **Memory Constraint**: BPTT requires storing the entire history of hidden states $\{h_0, h_1, \dots, h_T\}$ to compute gradients, which leads to $O(T)$ memory complexity.
2. **Biological Implausibility**: BPTT requires the system to "wait" until the end of a sequence and then propagate information backward in time, which does not match how biological brains or neuromorphic hardware learn.
3. **Vanishing/Exploding Gradients**: Long-term dependencies are difficult to learn because gradients are multiplied by the Jacobian $J_t = \partial_h f_\theta$ at each step, leading to exponential decay or growth.

## Alternatives and Variations

- **Truncated BPTT**: Only backpropagating for a fixed number of steps to save memory and reduce gradient issues (at the cost of losing long-term dependencies).
- **[[real-time-recurrent-learning|Real-Time Recurrent Learning]] (RTRL)**: An online alternative that computes gradients forward in time but has high computational complexity ($O(N^4)$).
- **FPTT (Forward Propagation of Errors Through Time)**: A theoretical proposal to reverse the BPTT equation to compute exact gradients forward in time. However, it is numerically unstable for networks that "forget" (where the Jacobian's eigenvalues are < 1) (Zucchet 2026).
- **[[linear-recurrent-unit|Linear Recurrent Unit]] (LRU)**: A specialized RNN cell that uses linear recurrence to avoid vanishing/exploding gradients while remaining efficient.

## Related Concepts

- [[real-time-recurrent-learning|Real-Time Recurrent Learning]]
- [[linear-recurrent-unit|Linear Recurrent Unit]]
- [[state-space-model|State-Space Model]]

## Related Sources

- [[sources/zucchet-2026-forward-propagation-errors-through-time|Zucchet 2026: Forward Propagation of Errors Through Time]]
