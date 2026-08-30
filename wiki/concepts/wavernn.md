---
type: concept
created: 2026-08-30
updated: 2026-08-30
sources:
  - raw/papers/valin-2018-lpcnet/full-text.md
tags:
  - neural-vocoder
  - speech-synthesis
  - autoregressive
  - deep-learning
  - efficiency
---

# WaveRNN

**WaveRNN** (Kalchbrenner et al., "Efficient Neural Audio Synthesis", ICML 2018) is an autoregressive neural vocoder that generates speech one sample at a time as a discrete probability distribution. It is the direct predecessor of [[concepts/lpcnet|LPCNet]], which is formulated as a WaveRNN variant with the spectral-envelope modeling delegated to [[concepts/linear-prediction|linear prediction]].

## Architecture

The model takes the previous audio sample $s_{t-1}$ and conditioning parameters $\mathbf{f}$, and outputs a discrete distribution $P(s_t)$. It consists of a [[concepts/gated-recurrent-unit|gated recurrent unit]] (GRU) followed by two fully-connected layers ending in a softmax:

$$
\mathbf{x}_{t}=\left[s_{t-1};\mathbf{f}\right]
$$

$$
\mathbf{u}_{t}=\sigma\left(\mathbf{W}^{(u)}\mathbf{h}_{t-1}+\mathbf{U}^{(u)}\mathbf{x}_{t}\right),\qquad
\mathbf{r}_{t}=\sigma\left(\mathbf{W}^{(r)}\mathbf{h}_{t-1}+\mathbf{U}^{(r)}\mathbf{x}_{t}\right)
$$

$$
\widetilde{\mathbf{h}}_{t}=\tanh\left(\mathbf{r}_{t}\circ\left(\mathbf{W}^{(h)}\mathbf{h}_{t-1}\right)+\mathbf{U}^{(h)}\mathbf{x}_{t}\right),\qquad
\mathbf{h}_{t}=\mathbf{u}_{t}\circ\mathbf{h}_{t-1}+\left(1-\mathbf{u}_{t}\right)\circ\widetilde{\mathbf{h}}_{t}
$$

$$
P\left(s_{t}\right)=\mathrm{softmax}\left(\mathbf{W}_{2}\,\mathrm{relu}\left(\mathbf{W}_{1}\mathbf{h}_{t}\right)\right)
$$

with $\sigma(x)=1/(1+e^{-x})$ and $\circ$ the element-wise product (biases omitted). The output sample is obtained by sampling from $P(s_t)$.

Two efficiency mechanisms distinguish WaveRNN from WaveNet-class models:

- **Discrete output** — the original model quantizes to 16 bits, split into 8 coarse + 8 fine bits (a coarse/fine split omitted in the LPCNet summary and unused there).
- **Sparse GRU matrices** — the GRU weight matrices use [[concepts/structured-sparsity|structured sparsity]] with non-zero blocks of size 4×4 or 16×1, chosen so the matrix products remain vectorizable on CPUs/GPUs.

## Relation to LPCNet

[[concepts/lpcnet|LPCNet]] (Valin & Skoglund 2018) starts from WaveRNN and (i) predicts the linear-prediction **excitation** instead of the sample, (ii) replaces the two fully-connected output layers with a [[concepts/dual-fc-layer|DualFC]] layer (also swapping the ReLU layer for a small second GRU, $\mathrm{GRU_{B}}$), (iii) uses 8-bit $\mu$-law with pre-emphasis rather than 16 bits, and (iv) adds $\mu$-law embeddings with precomputed weight products. The LPCNet paper's ablation baseline **WaveRNN+** includes all of these improvements except the LPC part, isolating the contribution of linear prediction itself.

## Complexity Context

Interpreting the WaveRNN paper's data, the sparse mobile version costs roughly 10 GFLOPS as a speaker-dependent model — versus ≈2.8 GFLOPS for speaker-independent LPCNet, ≈16 GFLOPS for FFTNet, and ≈50 GFLOPS (estimated) for SampleRNN.

## Related Concepts

- [[concepts/lpcnet|LPCNet]] — WaveRNN variant with linear prediction
- [[concepts/linear-prediction|Linear Prediction]] — the classical technique LPCNet layers on top of WaveRNN
- [[concepts/gated-recurrent-unit|Gated Recurrent Unit]] — the recurrent backbone
- [[concepts/structured-sparsity|Structured Sparsity]] — block-sparse GRU matrices

## Related Sources

- [[sources/valin-2018-lpcnet|Valin & Skoglund 2018: LPCNet]] — summarizes the WaveRNN architecture and equations (Section 2), and uses WaveRNN+ as the quality/complexity baseline
