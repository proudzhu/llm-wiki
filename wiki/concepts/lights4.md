---
type: concept
created: 2026-08-03
updated: 2026-08-03
sources:
  - raw/papers/jiang-2026-lightweight-speech-enhancement-ssm-dsc/full-text.md
tags:
  - deep-learning
  - state-space-model
  - speech-enhancement
  - computational-efficiency
---

# lightS4

**lightS4** is a diagonal-constrained variant of the Structured State-Space Sequence (S4) model introduced by Jiang, Gao, Wang, Zou & Liu (2026) for lightweight speech enhancement. It retains S4's global receptive field via FFT convolution while drastically reducing parameter count and implementation overhead by replacing the Normal Plus Low-Rank (NPLR) decomposition with a strict diagonal constraint on the state transition matrix.

## Motivation

The original S4 (Gu, Goel & Ré 2021) relies on the NPLR decomposition to approximate the continuous-time transition matrix $\mathbf{A}$. While theoretically efficient, the resulting kernel computation involves intricate operations such as **Cauchy kernel matrix-vector multiplication** that impose significant implementation overhead and memory costs compared to simple element-wise operations. Applying standard S4 parameterization to multidimensional time-frequency features also significantly increases parameter count, contradicting the design goal of compact, real-time speech enhancement frameworks.

## Mathematical Formulation

The core innovation is the diagonal constraint on the state transition matrix:

$$
\mathbf{A} = -\mathrm{diag}(\exp(\mathbf{A}_{\log}))
$$

where $\mathbf{A}_{\log}$ is a learnable parameter vector. This design guarantees stable negative eigenvalues and serves as the foundation for efficient and robust implementation.

### Zero-Order Hold (ZOH) Discretization

The diagonal structure enables exact and stable ZOH discretization without computationally expensive matrix operations. The matrix exponential simplifies to an element-wise operation:

$$
\overline{\mathbf{A}} = \exp(\Delta \mathbf{A}) = \mathrm{diag}\left(\exp(\Delta \mathbf{A}_{11}), \exp(\Delta \mathbf{A}_{22}), \ldots, \exp(\Delta \mathbf{A}_{HH})\right)
$$

Similarly, $\overline{\mathbf{B}}$ simplifies to a numerically stable element-wise calculation:

$$
\overline{\mathbf{B}} = (\overline{\mathbf{A}} - \mathbf{I}) \odot \mathbf{A}^{-1} \odot \mathbf{B}
$$

### Global FFT Convolution

The model avoids iterative computations by directly generating the full SSM convolutional kernel $\mathbf{K} \in \mathbb{R}^{C \times L}$ in a single vectorized step:

$$
\mathbf{K} = \left(\overline{\mathbf{C}\mathbf{B}},\; \overline{\mathbf{C}\mathbf{A}\mathbf{B}},\; \ldots,\; \overline{\mathbf{C}\mathbf{A}}^{L-1}\overline{\mathbf{B}}\right)
$$

and applying it as a global convolution using the Fast Fourier Transform (FFT), reducing computational complexity for long sequences from $O(L^2)$ to $O(L \log L)$.

## Dual-Path Architecture for Speech Enhancement

In [[sources/jiang-2026-lightweight-speech-enhancement-ssm-dsc|Jiang et al. 2026]], lightS4 is deployed inside the Featuremask module via a **dual-path architecture** that processes the time and frequency axes independently:

1. Input tensor is reshaped and fed into two parallel branches — one for long-range temporal dependencies, one for frequency dependencies.
2. Outputs are fused via a **cross-gating mechanism**:

$$
G_{\mathrm{time}} = \sigma(Y_{\mathrm{time}} + b_t), \quad G_{\mathrm{freq}} = \sigma(Y_{\mathrm{freq}} + b_f)
$$

$$
Y_{\mathrm{fused}} = (Y_{\mathrm{time}} \odot G_{\mathrm{freq}}) + (Y_{\mathrm{freq}} \odot G_{\mathrm{time}})
$$

3. A final sigmoid produces the mask: $M = \sigma(Y_{\mathrm{fused}})$, applied element-wise to the encoder features.

## Comparison with Alternative Sequence Models

The paper's ablation (Table 3 of the source) compares lightS4 against several alternatives on VoiceBank+DEMAND:

| Sequence Module | Params (M) | MACs (G) | PESQ | STOI |
|---|---|---|---|---|
| **lightS4 (proposed)** | **1.65** | **0.50** | **3.32** | **0.956** |
| Mamba | 2.65 | 0.70 | 3.35 | 0.957 |
| S5 | 1.91 | 0.59 | 3.26 | 0.954 |
| S4 (full NPLR) | 1.69 | 0.53 | 3.22 | 0.952 |
| LSTM | 2.60 | 0.60 | 3.02 | 0.944 |
| GRU | 2.19 | 0.49 | 3.06 | 0.946 |
| Conformer | 1.52 | 1.65 | 3.15 | 0.949 |
| Transformer | 1.77 | 2.51 | 3.18 | 0.950 |

**Key trade-off**: lightS4 is the explicit efficiency–quality compromise. Mamba gives +0.03 PESQ but at 1.6× parameters and 1.4× MACs; lightS4 is preferred when MACs budget is the binding constraint. Compared to full S4 (NPLR), lightS4 saves 0.04 M params and 0.03 G MACs while gaining +0.10 PESQ — confirming the diagonal constraint is a net win at this scale.

## Relation to Other Deep-Learning SSMs

lightS4 joins a family of structured state-space models used in speech enhancement:

- **[[concepts/s4nd|S4ND]]** — multidimensional S4 with independent SSMs along each axis; used by SICRN. More expressive but maintains expensive full-resolution maps.
- **[[concepts/mamba|Mamba]]** — selective SSM with input-dependent parameters; used by [[concepts/semamba|SEMamba]] for SOTA PESQ 3.69 on VoiceBank-DEMAND, but at 32.73 G MACs.
- **[[concepts/sic-block|SIC block]]** — combines S4ND with inplace convolution; SICRN's building block.
- **[[concepts/mamba-mingru|Mamba-MinGRU]]** — selective SSM + linear recurrence for own-voice cancellation.

lightS4 differs by enforcing a strict diagonal structure (vs. S4ND's multidimensional independence or Mamba's input-dependent selectivity), trading expressiveness for implementation simplicity and parameter efficiency.

## Related Concepts

- [[concepts/state-space-model|State-Space Model]] — parent family
- [[concepts/mamba|Mamba]] — selective SSM (efficiency vs. quality trade-off)
- [[concepts/s4nd|S4ND]] — multidimensional S4
- [[concepts/semamba|SEMamba]] — Mamba-based SE (32.73 G MACs vs. lightS4's 0.50 G)
- [[concepts/sicrn|SICRN]] — S4ND-based SE
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]] — complementary local-feature extractor in the same framework

## Related Sources

- [[sources/jiang-2026-lightweight-speech-enhancement-ssm-dsc|Jiang, Gao, Wang, Zou & Liu 2026: Lightweight SE with SSM and DSConv]] — introduces lightS4
