---
type: concept
created: 2026-10-03
updated: 2026-10-03
sources:
  - raw/papers/huang-2026-undf-configurable-directivity/full-text.md
  - raw/papers/huang-2026-neural-directional-filtering/full-text.md
  - raw/papers/uphaus-2026-directivity-low-latency/full-text.md
tags:
  - neural-directional-filtering
  - deep-learning
  - conditioning
  - spatial-audio
---

# FiLM-JNF

FiLM-JNF is a steerable neural directional filtering architecture: the [[concepts/joint-nonlinear-filtering|FT-JNF]] backbone (frequency-axis BiLSTM → causal time-axis UniLSTM → complex mask) extended with a [[concepts/film-layer|FiLM]] conditioning layer, injected between the frequency BiLSTM and the time UniLSTM. It was introduced in [[sources/huang-2026-undf-configurable-directivity|Huang, Chetupalli & Habets 2026]] (arXiv:2510.20253) as the conditioning mechanism of [[concepts/undf|UNDF]] — replacing the discrete one-hot conditioning of [[concepts/steerable-neural-directional-filtering|SNDF]] — where the conditioning input is a user-defined **pattern vector** ($L=72$ samples) rather than a steering angle. The comprehensive journal-style NDF paper (Huang, Chetupalli, Halimeh, Thiergart & Habets, arXiv 2026) reuses the same architecture for arbitrary continuous steering (a single-angle pattern being a special case of the pattern vector) and provides the in-depth analysis.

## Conditioning Mechanism

Two conditioning inputs exist in the FiLM-JNF family, both mapped by two linear layers to per-feature affine parameters $\boldsymbol{\alpha},\boldsymbol{\beta}\in\mathbb{R}^{512}$ with the FiLM layer applying $\mathbf{y}=\boldsymbol{\alpha}\odot\mathbf{x}+\boldsymbol{\beta}$ between the F-BiLSTM and the T-UniLSTM, shared across time and frequency:

1. **User-defined pattern vector** ($L=72$ uniformly sampled pattern values, the introducing form of [[concepts/undf|UNDF]]) — enables arbitrary user-defined patterns, including time-varying ones, at inference.
2. **Steering angle** $\theta_{\mathrm{s}}$ (continuous, radians) — mapped to a **sinusoidal embedding** (the transformer positional encoding applied to the angle instead of a discrete position):

$$
\mathbf{e}_{\theta_{\mathrm{s}}}[2i]=\sin\!\Big(\tfrac{\theta_{\mathrm{s}}}{10000^{2i/d_{\mathrm{emb}}}}\Big), \quad
\mathbf{e}_{\theta_{\mathrm{s}}}[2i+1]=\cos\!\Big(\tfrac{\theta_{\mathrm{s}}}{10000^{2i/d_{\mathrm{emb}}}}\Big), \quad d_{\mathrm{emb}}=72.
$$

Because the conditioning input is a continuous function of $\theta_{\mathrm{s}}$, the model steers to directions **never seen in training** (e.g., 32.5° / 67.5° off the 5° training grid) with steering-invariant, frequency-invariant pattern quality and consistent SDR. The introducing study further shows FiLM conditioning generalizes to unseen pattern **orders**, **scalings**, and steering directions where an initial-state-conditioned variant (PV-JNF) collapses — up to 11 dB SDR difference on unseen patterns.

## Comparison with One-Hot Conditioning

| | SNDF (one-hot) | FiLM-JNF |
|---|---|---|
| Conditioning input | one-hot vector over $M=360°/\vartheta$ discrete classes | sinusoidal embedding of a continuous angle |
| Injection point | F-BiLSTM initial states (per time frame) | FiLM layer between F-BiLSTM and T-UniLSTM |
| Steering resolution | limited to the training grid | arbitrary continuous directions |
| Complexity | 874 K params, 14.116 GMACs/s | 948 K params, 14.121 GMACs/s |

## Role as a Baseline

FiLM-JNF (948–950 K parameters, 32 ms window) is the relaxed-latency baseline in the low-latency binaural NDF study of [[sources/uphaus-2026-directivity-low-latency|Uphaus et al. 2026]]: shortening its STFT window from 32 ms to 8 ms drops PESQ from 2.10 to 1.72 — the sequence-length sensitivity of the broadband LSTM that the [[concepts/film-osn|FiLM-OSN]] architecture (frequency convolutions + Mamba temporal blocks) is designed to avoid, while both share the FiLM conditioning principle for directivity control.

## Related Concepts

- [[concepts/neural-directional-filtering|Neural Directional Filtering]]
- [[concepts/undf|UNDF]]
- [[concepts/steerable-neural-directional-filtering|Steerable Neural Directional Filtering]]
- [[concepts/joint-nonlinear-filtering|Joint Nonlinear Filtering]]
- [[concepts/film-layer|FiLM Layer]]
- [[concepts/film-osn|FiLM-OSN]]

## Related Sources

- [[sources/huang-2026-undf-configurable-directivity|Huang, Chetupalli & Habets 2026: UNDF]] — the introducing study: pattern-vector FiLM conditioning for user-defined directivity; PV-JNF vs FiLM-JNF generalization comparison
- [[sources/huang-2026-neural-directional-filtering|Huang et al. 2026: Neural Directional Filtering with a Compact Microphone Array]] — comprehensive treatment: continuous steering with FiLM-JNF, complexity analysis, reverberant and user-defined pattern experiments
- [[sources/uphaus-2026-directivity-low-latency|Uphaus et al. 2026: Directivity-Conditioned Low-Latency Neural Filtering]] — uses FiLM-JNF as the relaxed-latency baseline
