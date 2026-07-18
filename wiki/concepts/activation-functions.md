---
type: concept
created: 2026-07-18
updated: 2026-07-18
sources:
  - raw/papers/mienye-2024-rnn-comprehensive-review/full-text.md
tags:
  - deep-learning
  - neural-networks
  - activation-function
---

# Activation Functions

An **activation function** introduces non-linearity into a neural network, enabling it to learn and represent complex patterns. The choice of activation function $\sigma_h$ significantly affects how well a [[concepts/recurrent-neural-network\|recurrent neural network]] learns dependencies and generalizes to new data.

## Common Activation Functions

### Hyperbolic Tangent (tanh)
Squashes input to $[-1, 1]$; zero-centered, suitable for sequences with both positive and negative values:

$$
\sigma_h(z) = \tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}. \tag{1}
$$

### Rectified Linear Unit (ReLU)
Outputs input directly if positive, otherwise zero. Mitigates vanishing gradient for positive inputs:

$$
\sigma_h(z) = \max(0, z). \tag{2}
$$

### Leaky ReLU
Addresses the "dying ReLU" problem by allowing a small, non-zero gradient when input is negative:

$$
\sigma_h(z) = \begin{cases} z & \text{if } z > 0 \\ \alpha z & \text{otherwise} \end{cases}, \tag{3}
$$

where $\alpha$ is a small constant, typically 0.01.

### Exponential Linear Unit (ELU)
Brings mean activation closer to zero, speeding up learning by reducing bias shifts; allows negative activations:

$$
\sigma_h(z) = \begin{cases} z & \text{if } z > 0 \\ \alpha(e^z - 1) & \text{otherwise} \end{cases}. \tag{4}
$$

### Sigmoid
Squashes input to $[0, 1]$; useful for outputs interpreted as probabilities:

$$
\sigma_h(z) = \frac{1}{1 + e^{-z}}. \tag{5}
$$

### Softmax
Converts raw scores into a probability distribution; commonly used in the output layer of classification networks:

$$
\sigma_h(z_i) = \frac{e^{z_i}}{\sum_j e^{z_j}}. \tag{6}
$$

## Choice Heuristics

| Function | Range | Use case |
|----------|-------|----------|
| tanh | $[-1, 1]$ | Hidden states in RNNs; zero-centered |
| ReLU | $[0, \infty)$ | Hidden layers in deep networks; mitigates vanishing gradient |
| Leaky ReLU | $(-\infty, \infty)$ | Avoids dying ReLU |
| ELU | $(-\alpha, \infty)$ | Faster convergence than ReLU |
| Sigmoid | $[0, 1]$ | Binary classification; gate outputs in LSTM/GRU |
| Softmax | probability distribution | Multi-class classification output |

In [[concepts/long-short-term-memory\|LSTM]] and [[concepts/gated-recurrent-unit\|GRU]] cells, **sigmoid** is used for gates (to produce values in $[0, 1]$ that act as keep/forget ratios) and **tanh** is used for the candidate cell input and hidden state output.

## Related Concepts

- [[concepts/recurrent-neural-network\|Recurrent Neural Network]]
- [[concepts/long-short-term-memory\|Long Short-Term Memory (LSTM)]]
- [[concepts/gated-recurrent-unit\|Gated Recurrent Unit (GRU)]]
- [[concepts/vanishing-gradient-problem\|Vanishing Gradient Problem]]
- [[concepts/neural-networks\|Neural Networks]]

## Related Sources

- [[sources/mienye-2024-rnn-comprehensive-review\|Mienye, Swart & Obaido 2024: RNN Comprehensive Review]] — Section 3.2 covers activation functions used in RNNs
