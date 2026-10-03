---
type: concept
created: 2026-10-03
updated: 2026-10-03
sources:
  - raw/papers/huang-2026-neural-directional-filtering/full-text.md
  - raw/papers/uphaus-2026-directivity-low-latency/full-text.md
tags:
  - neural-directional-filtering
  - deep-learning
  - conditioning
  - spatial-audio
---

# FiLM-JNF

FiLM-JNF is a steerable neural directional filtering architecture: the [[concepts/joint-nonlinear-filtering|FT-JNF]] backbone (frequency-axis BiLSTM → causal time-axis UniLSTM → complex mask) extended with a [[concepts/film-layer|FiLM]] conditioning layer that injects a **continuous steering direction**, replacing the discrete one-hot conditioning of [[concepts/steerable-neural-directional-filtering|SNDF]]. The FiLM-conditioned FT-JNF originates in the companion study "Neural directional filtering with configurable directivity pattern at inference" (Huang, Chetupalli & Habets 2025, arXiv:2510.20253), and the comprehensive journal-style NDF paper (Huang, Chetupalli, Halimeh, Thiergart & Habets, arXiv 2026) proposes it for arbitrary continuous steering and provides the in-depth analysis.

## Conditioning Mechanism

The steering direction $\theta_{\mathrm{s}}$ (in radians, arbitrary/continuous) is mapped to an angle embedding via a **sinusoidal encoding** (the transformer positional encoding applied to the angle instead of a discrete position):

$$
\mathbf{e}_{\theta_{\mathrm{s}}}[2i]=\sin\!\Big(\tfrac{\theta_{\mathrm{s}}}{10000^{2i/d_{\mathrm{emb}}}}\Big), \quad
\mathbf{e}_{\theta_{\mathrm{s}}}[2i+1]=\cos\!\Big(\tfrac{\theta_{\mathrm{s}}}{10000^{2i/d_{\mathrm{emb}}}}\Big), \quad d_{\mathrm{emb}}=72.
$$

Two linear layers derive per-feature affine parameters $\boldsymbol{\alpha},\boldsymbol{\beta}\in\mathbb{R}^{512}$ from the embedding, and the FiLM layer applies $\mathbf{y}=\boldsymbol{\alpha}\odot\mathbf{x}+\boldsymbol{\beta}$ between the F-BiLSTM and the T-UniLSTM, shared across time and frequency. Because the conditioning input is a continuous function of $\theta_{\mathrm{s}}$, the model steers to directions **never seen in training** (e.g., 32.5° / 67.5° off the 5° training grid) with steering-invariant, frequency-invariant pattern quality and consistent SDR.

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
- [[concepts/steerable-neural-directional-filtering|Steerable Neural Directional Filtering]]
- [[concepts/joint-nonlinear-filtering|Joint Nonlinear Filtering]]
- [[concepts/film-layer|FiLM Layer]]
- [[concepts/film-osn|FiLM-OSN]]

## Related Sources

- [[sources/huang-2026-neural-directional-filtering|Huang et al. 2026: Neural Directional Filtering with a Compact Microphone Array]] — comprehensive treatment: continuous steering with FiLM-JNF, complexity analysis, reverberant and user-defined pattern experiments
- [[sources/uphaus-2026-directivity-low-latency|Uphaus et al. 2026: Directivity-Conditioned Low-Latency Neural Filtering]] — uses FiLM-JNF as the relaxed-latency baseline
- Huang, Chetupalli & Habets 2025, "Neural directional filtering with configurable directivity pattern at inference" (arXiv:2510.20253) — the introducing companion study (not yet ingested)
