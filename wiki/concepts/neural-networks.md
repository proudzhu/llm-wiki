---
type: concept
created: 2026-04-18
updated: 2026-04-25
sources:
tags:
  - neural-networks
  - deep-learning
  - machine-learning
---

# Neural Networks

Computational systems inspired by biological neural networks, organized into three generations:

1. **First generation**: Perceptrons — binary threshold units (McCulloch-Pitts, Rosenblatt)
2. **Second generation**: ANNs/DNNs — continuous activation functions, backpropagation (sigmoid, ReLU, Transformers)
3. **Third generation**: [[spiking-neural-networks|Spiking Neural Networks]] — spike-based computation, temporal coding

## ANN Fundamentals

Rate-based neuron: $r = f(Wu + b)$, where $f$ is a nonlinear activation function.

Key architectures:
- **CNNs**: Weight sharing for grid-like data (images); shift-invariant features
- **RNNs**: Temporal processing via hidden state; LSTM/GRU for long-range dependencies
- **Transformers**: Self-attention mechanism; parallel processing of sequences

## Relationship to SNNs

ANNs achieve superior accuracy but are energy-intensive. SNNs trade some accuracy for:
- Event-driven, sparse computation
- Native temporal processing
- Deployment on [[neuromorphic-computing|neuromorphic hardware]] at milliwatt scale

ANN-to-SNN conversion bridges the gap: train with backpropagation, deploy as spikes.

## Related Concepts

- [[spiking-neural-networks|Spiking Neural Networks]]
- [[neuromorphic-computing|Neuromorphic Computing]]
- [[deep-learning-for-signal-processing|Deep Learning for Signal Processing]]
- [[backpropagation-through-time|Backpropagation Through Time]]
- [[real-time-recurrent-learning|Real-Time Recurrent Learning]]
- [[active-noise-control|Active Noise Control]]

## Related Sources

- [[sources/yamazaki-2022-spiking-nn-review|Yamazaki 2022: Spiking Neural Networks Review]]
