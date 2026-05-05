---
type: entity
created: 2026-04-12
updated: 2026-04-17
tags:
- machine-learning
- researcher
sources: []
---
# Nicolas Zucchet

Nicolas Zucchet is a researcher specializing in Recurrent Neural Networks (RNNs) and biologically inspired learning algorithms. He is a PhD student at ETH Zürich (as of 2024-2025).

## Research Focus

His work focuses on finding efficient alternatives to **[[../concepts/backpropagation-through-time|Backpropagation Through Time]] (BPTT)** for training recurrent systems. He explores algorithms that can compute gradients forward in time, which are more memory-efficient and biologically plausible than standard backpropagation.

### Forward Propagation of Errors Through Time (FPTT)
Zucchet (2026) derived an exact forward-propagation algorithm for RNN gradients. His key contribution was identifying a fundamental limitation of such forward-error methods: they are numerically unstable for stable linear systems (systems that "forget"). This result suggests that BPTT remains the most numerically sound method for training standard RNNs and State-Space Models.

## Key Publications / Works

- **"Forward Propagation of Errors Through Time"** (2026) — Blog post and research demonstrating the limits of forward-gradient methods.
- Work on **Invertible RNNs** as a stable alternative for gradient computation.

## Related Concepts

- [[../concepts/backpropagation-through-time|Backpropagation Through Time]]
- [[../concepts/real-time-recurrent-learning|Real-Time Recurrent Learning]]
- [[../concepts/linear-recurrent-unit|Linear Recurrent Unit]]

## Related Sources

- [[../sources/zucchet-2026-forward-propagation-errors-through-time|Zucchet 2026: Forward Propagation of Errors Through Time]]

## Related Entities
