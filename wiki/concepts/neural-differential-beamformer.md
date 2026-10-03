---
type: concept
created: 2026-10-03
updated: 2026-10-03
sources:
  - raw/papers/huang-2026-dual-mic-steerable-neural-beamformer/full-text.md
tags:
  - neural-directional-filtering
  - differential-microphone-array
  - beam-steering
  - deep-learning
  - directivity-pattern
---

# Neural Differential Beamformer

A neural differential beamformer (NDBF) is a DNN-based beamformer that reproduces classical [[concepts/differential-microphone-array|differential microphone array (DMA)]] beampatterns from a compact array — using a network to estimate **complex beamforming weights** applied to the microphone signals, rather than the single-channel complex mask of [[concepts/neural-directional-filtering|neural directional filtering (NDF)]]. It was introduced by Huang & Habets (arXiv 2026) for the most constrained DMA geometry: a **dual-microphone linear array** of closely spaced (3 cm) omnidirectional microphones, for which classical differential beamforming is restricted to first order and provably non-steerable.

## Motivation

For a linear array of $Q$ omnidirectional microphones, classical differential beamformers are bounded to order $Q-1$; a dual-mic array can only realize first-order patterns, and first-order LDMAs cannot steer off endfire at all ([[concepts/steerable-ldma|Steerable LDMA]]). Moreover, small spacing causes white-noise amplification at low frequencies and spatial aliasing above $c/2d$ (5.7 kHz for 3 cm). NDF-style mask-based neural filtering had only been studied for circular arrays, and masking a single reference microphone under-exploits the scarce spatial degrees of freedom of a dual-mic array.

## Key Properties (Huang & Habets 2026)

- **Steerable**: the beampattern keeps the same shape across look directions 0°–180° in the semicircular plane (linear-array steerability definition of Jin et al. 2021) — achieved with a dual-mic array where classical designs are non-steerable.
- **High-order and frequency-invariant**: 3rd-order cardioid patterns (classically needing a 4-microphone array) are learned from only 2 microphones, without spatial aliasing for broadband speech.
- **Outperforms mask-based NDF**: on the same dual-mic data, NDBF attains slightly higher SDR (25.93 vs 25.85 dB first-order; 23.24 vs 23.13 dB third-order) with stronger null suppression, which the authors attribute to the weight-vector output exploiting both microphone channels instead of masking one reference.
- **Stereo recording**: two parallel NDBF models steered to 135° (left) and 45° (right) reproduce an X-Y stereo recording — matching a pair of [[concepts/virtual-directional-microphone|virtual directional microphones]] including inter-channel level differences — a capability no classical or prior neural beamformer offered with two closely spaced omni mics.

## Formulation

The target of the NDBF is a steerable high-order DMA beampattern $\Lambda_{\theta_{\mathrm{s}}}(\theta_{\mathrm{n}})$ applied at the array center:

$$
Z_{\theta_{\mathrm{s}}}(f,t)=\sum_{n=1}^{N}\Lambda_{\theta_{\mathrm{s}}}(\theta_{\mathrm{n}})\,H_{\mathbf{p}_{\mathrm{c}},n}(f)\,X_{n}(f,t)
$$

with the simplified $J$th-order DMA pattern $\Lambda(\theta)=(\mu+(1-\mu)\cos(\theta-\theta_{\mathrm{s}}))^{J}$, where $\mu$ fixes the null position. The network estimates $\mathbf{w}_{\theta_{\mathrm{s}}}(f)$ such that $\widehat{Z}_{\theta_{\mathrm{s}}}(f,t)=\mathbf{w}_{\theta_{\mathrm{s}}}^{H}(f)\,\mathbf{y}(f,t)$.

## Architecture

The backbone is the [[concepts/spatially-selective-nonlinear-filter|JNF-SSF]] (Tesch & Gerkmann 2023) — BiLSTM along frequency, then UniLSTM along time — with the steering-direction conditioning of [[concepts/steerable-neural-directional-filtering|SNDF]] (one-hot $\theta_{\mathrm{s}}$ → linear layer → LSTM initial states per time frame). The single distinguishing modification: the output layer (linear + tanh) produces a **vector of $Q$ complex weights per frequency** instead of a single-channel mask. Training uses the batch-aggregated normalized L1 loss and the scene-reuse-across-steering-targets strategy (each semicircular scene paired with all 36 steering targets at 5° resolution).

## Position Within Neural Spatial Filtering

| Method | Array | Output | Steering | Distinctive capability |
|---|---|---|---|---|
| NDF (Wechsler 2024) | 4-mic UCA | Single-channel mask | Fixed per model | 3rd-order pattern with 4 mics |
| SNDF (Huang 2025) | 4-mic UCA | Single-channel mask | Any direction, one model | 6th-order steerable patterns |
| **NDBF (Huang 2026)** | **2-mic linear** | **Complex weight vector (beamforming)** | **0°–180° semicircle** | **Steerable high-order with 2 mics; stereo X-Y recording** |

## Related Concepts

- [[concepts/neural-directional-filtering|Neural Directional Filtering]]
- [[concepts/steerable-neural-directional-filtering|Steerable Neural Directional Filtering]]
- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/steerable-ldma|Steerable LDMA]]
- [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Non-Linear Filter]]
- [[concepts/frequency-invariant-beamforming|Frequency-Invariant Beamforming]]
- [[concepts/virtual-directional-microphone|Virtual Directional Microphone]]

## Related Sources

- [[sources/huang-2026-dual-mic-steerable-neural-beamformer|Huang & Habets 2026: Dual-Microphone Steerable High-Order Neural Differential Beamformer]] — the introducing paper
- [[sources/wechsler-2024-neural-directional-filtering|Wechsler et al. 2024: Neural Directional Filtering]] — the mask-based predecessor
- [[sources/jin-2021-steering-study-ldma|Jin et al. 2021: Steering Study of Linear Differential Microphone Arrays]] — classical steerability definitions and limits that NDBF transcends
