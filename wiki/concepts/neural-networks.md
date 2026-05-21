---
type: concept
created: 2026-04-18
updated: 2026-05-21
sources:
  - raw/papers/kim-2021-broadcasted-residual-learning/full-text.md
  - raw/papers/cai-2024-tf-sepnet/full-text.md
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
- **CNNs**: Weight sharing for grid-like data such as images and spectrograms; efficient audio variants include [[concepts/bc-resnet|BC-ResNet]] and [[concepts/broadcasted-residual-learning|Broadcasted Residual Learning]]
- **RNNs**: Temporal processing via hidden state; LSTM/GRU for long-range dependencies
- **Transformers**: Self-attention mechanism; parallel processing of sequences

## Relationship to SNNs

ANNs achieve superior accuracy but are energy-intensive. SNNs trade some accuracy for:
- Event-driven, sparse computation
- Native temporal processing
- Deployment on [[neuromorphic-computing|neuromorphic hardware]] at milliwatt scale

ANN-to-SNN conversion bridges the gap: train with backpropagation, deploy as spikes.

## Related Concepts

- [[concepts/spiking-neural-networks|Spiking Neural Networks]]
- [[concepts/neuromorphic-computing|Neuromorphic Computing]]
- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]
- [[concepts/backpropagation-through-time|Backpropagation Through Time]]
- [[concepts/real-time-recurrent-learning|Real-Time Recurrent Learning]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/acoustic-scene-classification|Acoustic Scene Classification]]
- [[concepts/keyword-spotting|Keyword Spotting]]
- [[concepts/bc-resnet|BC-ResNet]]
- [[concepts/broadcasted-residual-learning|Broadcasted Residual Learning]]

## Related Sources

- [[sources/yamazaki-2022-spiking-nn-review|Yamazaki 2022: Spiking Neural Networks Review]]
- [[sources/kim-2021-broadcasted-residual-learning|Kim, Chang, Lee & Sung 2021: Broadcasted Residual Learning]]
- [[sources/cai-2024-tf-sepnet|Cai, Zhang & Li 2024: TF-SepNet]]
