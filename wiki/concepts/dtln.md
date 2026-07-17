---
type: concept
created: 2026-07-17
updated: 2026-07-17
sources:
  - raw/papers/seidel-2024-bark-scale-nn-residual-suppression/full-text.md
tags:
  - speech-enhancement
  - acoustic-echo-cancellation
  - deep-learning
  - neural-network-architecture
  - real-time
---

# DTLN (Dual-Signal Transformation LSTM Network)

The **Dual-signal Transformation LSTM Network (DTLN)** is a fully data-driven (non-hybrid) neural network for acoustic echo cancellation and speech enhancement, introduced by Westhausen & Meyer (ICASSP 2021). It is a common baseline in the AEC literature due to its strong fully-neural performance and moderate complexity.

## Architecture

DTLN processes the input through two stacked LSTM-based stages, each operating in a different signal representation:

1. **Stage 1**: LSTM operating on a learned feature representation (separation network) — typically 256 units per layer.
2. **Stage 2**: LSTM operating on a complementary representation (e.g., complex spectrum or a different feature transform) — combines with stage 1 to refine the estimate.

The canonical DTLN-AEC configuration (as used in [[sources/seidel-2024-bark-scale-nn-residual-suppression\|Seidel et al. 2024]]) is:

- **4 consecutive LSTM layers**, 256 units each
- Followed by a **fully connected layer with sigmoid activation**
- Output: a masking filter applied to the input STFT

## Role as an AEC Baseline

DTLN is widely used as a **fully data-driven baseline** in AEC challenges and benchmarks. In [[sources/seidel-2024-bark-scale-nn-residual-suppression\|Seidel et al. 2024]] it is one of the reference methods, where it achieves:

- The highest ERLE score on STFE (68.78 dB) — strong echo suppression.
- However, with **3.16M parameters** and **408 MMACs/s**, it is significantly more expensive than the proposed Bark-scale postfilter (1.58M / 235 MMACs/s) and has a borderline real-time factor (RTF 0.97 on an Intel i9-10850K).

## Distinction from Hybrid Approaches

Unlike hybrid AEC systems (e.g., [[sources/seidel-2024-bark-scale-nn-residual-suppression\|Seidel 2024]], [[sources/shetu-2024-hybrid-low-complexity-aenr\|Shetu 2024]], [[sources/li-2025-echofree-neural-aec\|EchoFree]]), DTLN does **not** use a classical linear adaptive filter (LMS/NLMS/Kalman) for echo cancellation. The neural network performs the entire AEC task end-to-end. This simplifies the pipeline but loses the interpretability and convergence guarantees of classical adaptive filtering.

| Property | DTLN | Hybrid (e.g., Seidel 2024) |
|----------|------|---------------------------|
| Linear front-end | None | [[concepts/subband-adaptive-filter\|Subband NLMS]] LEC |
| NN stage | 4× LSTM + FC sigmoid | NSNet2-style FC+GRU |
| Params | 3.16M | 1.58M |
| MACs/s | 408M | 235M |
| ERLE (Seidel 2024 test) | **68.78 dB** | 60.10 dB |
| RTF (Intel i9) | 0.97 | 0.22 |

## Related Concepts

- [[concepts/acoustic-echo-cancellation\|Acoustic Echo Cancellation]]
- [[concepts/nsnet2\|NSNet2]]
- [[concepts/speech-enhancement\|Speech Enhancement]]
- [[concepts/subband-adaptive-filter\|Subband Adaptive Filter]]

## Related Sources

- [[sources/seidel-2024-bark-scale-nn-residual-suppression\|Seidel, Mowlaee & Fingscheidt 2024]] — uses DTLN as a fully-data-driven reference baseline (4 LSTM 256 + FC sigmoid)
