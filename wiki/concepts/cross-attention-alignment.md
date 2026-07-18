---
type: concept
created: 2026-06-06
updated: 2026-07-18
tags:
  - deep-learning
  - attention
  - acoustic-echo-cancellation
---

# Cross-Attention Alignment

**Cross-attention alignment** is a mechanism for soft-aligning microphone and far-end reference signals in feature space for acoustic echo cancellation. Unlike DSP-based delay compensators, it learns a delay distribution directly from deep time-frequency features.

## Mechanism

Given microphone features $\mathbf{X}_M \in \mathbb{R}^{c \times t \times f}$ and far-end features $\mathbf{X}_F \in \mathbb{R}^{c \times t \times f}$:

1. **Query/Key projection**: Point-wise convolutions produce $\mathbf{Q} \in \mathbb{R}^{h \times t \times f}$ and $\mathbf{K} \in \mathbb{R}^{h \times t \times f}$

2. **Key unfolding**: Unfold $\mathbf{K}$ along time axis creating delay dimension: $\mathbf{K}_u \in \mathbb{R}^{h \times t \times d_{\max} \times f}$

3. **Similarity computation**: Dot product on frequency axis yields $\mathbf{Z} \in \mathbb{R}^{h \times t \times d_{\max}}$

4. **Convolutional stabilization**: Convolutional layer ($5 \times 3$ kernel) combines $h$ similarity channels into single attention head

5. **Delay distribution**: Softmax on delay axis produces $\mathbf{D} \in \mathbb{R}^{t \times d_{\max}}$

6. **Aligned features**: Weighted sum with delay probabilities produces aligned far-end features $\underline{\mathbf{X}}_F$

## Key Innovation

The convolutional layer in the time-delay map stabilizes the delay distribution and enhances AEC performance, improving upon prior cross-attention methods.

## Advantages over DSP Alignment

- Learns alignment from deep features rather than raw signals
- Handles time-varying delays naturally
- No explicit delay estimation required
- End-to-end trainable

## Related Concepts

- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]]
- [[concepts/complex-convolving-mask|Complex Convolving Mask]]

## Related Sources

- [[sources/indenbom-2023-deepvqe|Indenbom et al. 2023: DeepVQE]]
