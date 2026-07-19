---
type: concept
created: 2026-07-19
updated: 2026-07-19
tags:
  - deep-learning
  - recurrent-neural-network
  - state-drift
  - complementary-filter
  - low-complexity
---

# Comfi-FastGRNN

**Comfi-FastGRNN** (Complementary Filter FastGRNN) is a parameter-efficient extension of [[concepts/fastgrnn|FastGRNN]] proposed by [[entities/nicolas-arrieta-larraza|Larraza]] & [[entities/niels-de-koeijer|de Koeijer]] (ICASSP 2026) to mitigate the inference-time RNN state drift observed when FastGRNN is applied to long streaming audio sequences (>60 s). It adds two scalar trainable parameters to the FastGRNN state update, inspired by complementary filters used in inertial-sensor (accelerometer–gyroscope) fusion for orientation drift suppression.

## Motivation: FastGRNN State Drift

[[sources/larraza-2026-fast-ulcnet-speech-enhancement|Larraza & de Koeijer 2026]] empirically observed that FastGRNN, applied to >60 s audio signals for speech enhancement, drifts in the forward pass: the mean hidden-state magnitude grows monotonically over time, correlating with measurable degradation in enhancement quality (e.g., BAKMOS drops from 3.95 → 3.62 and SI-SDR from 16.89 → 13.58 on a 90 s DNS Challenge test set).

The root cause is traced to the FastGRNN state update: the coefficients of the candidate update $\tilde{h}_t$ and the previous state $h_{t-1}$ do not satisfy a sum-to-one constraint, so the state lacks a contraction guarantee over extended inference horizons. The original FastGRNN stability guarantee applies to training (BPTT) and not to the inference-time forward pass.

## Formulation

Comfi-FastGRNN extends the FastGRNN state $h_t$ with a trainable complementary filter:

$$
h_{t\,\text{comfi}} = \gamma h_t + (1 - \gamma) \lambda
$$

with two scalar trainable parameters $\lambda, \gamma \in \mathbb{R}$:

- $\lambda$ — scalar modulation factor compensating for state drift
- $\gamma$ — controls the relative contribution of the hidden state and the drift-correction term

Recommended initialization: $\gamma = 0.999$, $\lambda = 0.0$ (near-identity at the start of training, so the network starts as plain FastGRNN and learns the correction).

## Properties

- **Parameter-efficient**: Adds only 2 scalar parameters per FastGRNN layer, leaving the model size and MACs essentially unchanged.
- **Effective**: Fully recovers long-sequence performance in the Fast-ULCNet evaluation. On the 90 s DNS test set, Fast-ULCNet<sub>comfi</sub> achieves DNSMOS slightly above ULCNet and SI-SDR within 0.41 dB of ULCNet, whereas plain Fast-ULCNet collapses.
- **Complementary-filter analogy**: In inertial-sensor fusion, a high-pass filter on the gyroscope (drift-prone but precise in the short term) is fused with a low-pass filter on the accelerometer (drift-free but noisy) to suppress orientation drift. Comfi-FastGRNN applies the same principle to the FastGRNN hidden-state trajectory.

## Significance

This is, to the authors' knowledge, **the first reported use of a trainable complementary filter to mitigate RNN state drift**. It identifies a class of failure modes — training-stable RNNs that drift at inference over long sequences — that is otherwise under-documented in the deep-learning literature, where length-invariance claims are typically validated only on short sequences.

## Related Concepts

- [[concepts/fastgrnn|FastGRNN]]
- [[concepts/fast-ulcnet|Fast-ULCNet]]
- [[concepts/ulcnet|ULCNet]]
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/larraza-2026-fast-ulcnet-speech-enhancement|Larraza & de Koeijer 2026: Fast-ULCNet]]
