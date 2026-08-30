---
type: concept
created: 2026-08-30
updated: 2026-08-30
sources:
  - raw/papers/valin-2018-lpcnet/full-text.md
tags:
  - deep-learning
  - neural-vocoder
  - output-layer
  - low-complexity
---

# DualFC Layer

The **dual fully-connected (DualFC) layer** is an output layer introduced by [[concepts/lpcnet|LPCNet]] (Valin & Skoglund 2018). It replaces the usual fully-connected layer preceding the output softmax with an element-wise weighted sum of two tanh fully-connected layers:

$$
\mathrm{dual\_fc}(\mathbf{x})=\mathbf{a}_{1}\circ\tanh\left(\mathbf{W}_{1}\mathbf{x}\right)+\mathbf{a}_{2}\circ\tanh\left(\mathbf{W}_{2}\mathbf{x}\right),
$$

where $\mathbf{W}_{1}$ and $\mathbf{W}_{2}$ are weight matrices, $\mathbf{a}_{1}$ and $\mathbf{a}_{2}$ are learnable weighting vectors, and $\circ$ denotes the element-wise product.

## Motivation

LPCNet's output is a distribution over 256 $\mu$-law quantization levels. The intuition for the two-tanh structure: deciding whether a value falls within a certain range (a $\mu$-law quantization interval) requires **two comparisons**, and each fully-connected tanh layer implements the equivalent of one comparison. Visualizing the weights of a trained network supports this interpretation.

## Properties

- Slightly improves quality over a regular fully-connected layer at **equivalent complexity** (the gain is modest but consistent).
- Makes it easier to compute output probabilities without significantly increasing the size of the preceding layer.
- Not strictly necessary for the LPC approach itself — it is an independent architectural improvement also inherited by the WaveRNN+ ablation baseline.

In the LPCNet architecture the DualFC output feeds the softmax that produces $P(e_t)$, the probability of each possible excitation value.

## Related Concepts

- [[concepts/lpcnet|LPCNet]] — the vocoder that introduces the layer
- [[concepts/wavernn|WaveRNN]] — whose two fully-connected output layers (one ReLU, one linear) DualFC replaces

## Related Sources

- [[sources/valin-2018-lpcnet|Valin & Skoglund 2018: LPCNet]] — Section 3.4 defines the layer and its two-comparisons intuition
