---
type: concept
created: 2026-06-06
updated: 2026-06-06
tags:
  - deep-learning
  - speech-enhancement
  - complex-valued
---

# Complex Convolving Mask (CCM)

The **Complex Convolving Mask (CCM)** is a time-frequency varying complex-valued filter that estimates clean speech by mixing neighboring T-F bins in a learnable fashion. Unlike simple complex ratio masks, CCM applies a convolutional operation in the time-frequency domain.

## Two-Stage Construction

### Stage 1: Complex Mask

Uses three weight components at 120° in the complex plane:

$$\mathbf{v} = (v_1, v_2, v_3) = \left(1, -\frac{1}{2} + j\frac{\sqrt{3}}{2}, -\frac{1}{2} - j\frac{\sqrt{3}}{2}\right)$$

Input $\mathbf{X} \in \mathbb{R}^{c \times t \times f}$ is reshaped to $\mathbf{X}' \in \mathbb{R}^{3 \times \frac{c}{3} \times t \times f}$, then:

$$\mathbf{H} = \mathbf{v} \cdot \mathbf{X}'$$

produces complex mask $\mathbf{H} \in \mathbb{C}^{\frac{c}{3} \times t \times f}$.

The three-vector component (vs. two-vector real/imaginary) provides more stable output, preventing low noise and echo leakage.

### Stage 2: Time-Frequency Convolution

Reshape channel dimension to form convolution kernel $\mathbf{M} \in \mathbb{C}^{(m+1) \times (2n+1) \times t \times f}$ with weights varying over time and frequency.

Clean spectrum estimated as:

$$\hat{\mathbf{X}}(t, f) = \sum_{i=-m}^{0} \sum_{j=-n}^{n} \mathbf{X}(t+i, f+j) \cdot \mathbf{M}(i, j, t, f)$$

The mask is applied causally (only past and current frames).

## Advantages

- Leverages magnitude and phase from neighboring T-F bins
- Learnable filter adapts to signal characteristics
- Provides largest improvement in ablation studies for noise suppression
- Over 10 dB SRR improvement for dereverberation

## Related Concepts

- [[concepts/complex-ratio-mask|Complex Ratio Mask]]
- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]]
- [[concepts/cross-attention-alignment|Cross-Attention Alignment]]

## Related Sources

- [[sources/indenbom-2023-deepvqe|Indenbom et al. 2023: DeepVQE]]
