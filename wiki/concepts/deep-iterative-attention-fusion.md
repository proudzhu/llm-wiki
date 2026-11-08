---
type: concept
created: 2026-11-08
updated: 2026-11-08
sources:
  - wiki/sources/wu-2026-dbmif-multimodal-fusion.md
tags:
  - speech-enhancement
  - bone-conduction
  - multimodal-fusion
  - attention-mechanism
---

# Deep Iterative Attention Fusion

**Deep Iterative Attention Fusion (DIAF)** is the early-stage modality-fusion module of DBMIF (Wu et al. 2026). Unlike single-shot attention or concatenation, it starts from a parameter-free sum of the two modalities and refines the mixture over $K$ rounds of channel attention, so the fusion weights are re-estimated *after seeing the previous fusion* rather than once from independent features.

## Key Formulations

Initialisation without extra parameters:

$$
\mathbf{x}^{(0)} = \mathbf{x}_a^{(0)} + \mathbf{x}_b^{(0)}
$$

Iterative channel-attention refinement, $k = 1,\dots,K$:

$$
\mathrm{w}^{(k)} = \mathrm{CAM}\left(\mathrm{x}^{(k-1)}\right), \qquad
\mathrm{x}^{(k)} = \mathrm{w}^{(k)} \odot \mathrm{x}_a^{(0)} + \left(1-\mathrm{w}^{(k)}\right) \odot \mathrm{x}_b^{(0)}
$$

$\mathrm{w}^{(k)} \in \mathbb{R}^C$ is produced by global average pooling followed by a sigmoid, so each element is interpreted as the per-channel **confidence in the air-conducted (AC) modality**; $1-\mathrm{w}^{(k)}$ weights the bone-conducted (BC) modality. The final quality-aware fusion embedding is $\mathbf{x}_f^{(0)} = \mathbf{x}^{(K)}$; DBMIF uses $K = 3$.

## Why Iterate

A single attention gate is computed from the raw features, which under heavy noise are themselves unreliable — the gate inherits the corrupted evidence. Iterating lets the mask condition on a partially denoised mixture: by round 2 the fusion already contains BC-anchored low frequencies, so the attention can commit to AC for the high bands without being misled by noise in the low ones. The reported behaviour (DBMIF Fig. 9) is exactly this: mean $\mathrm{w}^{(3)}$ grows monotonically with SNR, low subbands stay BC-weighted, high subbands AC-weighted, and the mid band is the most dynamic.

## Relationship to Other Fusion Mechanisms

| Mechanism | Form | Where | Notes |
|:----------|:-----|:------|:------|
| **DIAF** (this page) | Iterative channel attention, soft convex combination | Early (pre-encoder) | $K=3$; conditions on the evolving fusion |
| [[concepts/iterative-attentional-feature-fusion\|iAFF]] | Multi-scale channel attention fusion, two stages | Early + intermediate | Used by Kuang 2025; beats cross attention there on both cost and quality |
| [[concepts/cross-branch-gated-interaction\|CBGI]] | Bidirectional sigmoid gating at every encoder scale | Throughout | Operates on streams, not on a single scalar blend |
| [[concepts/deep-balanced-interaction\|DBI]] | Fixed-point equilibrium over modality states | Bottleneck | Changes the representation, not just the weights |
| [[concepts/attention-gate\|Attention gate]] | Single-shot additive/multiplicative gate | Skip connections | No iteration |

## Related Concepts

- [[concepts/cross-branch-gated-interaction|Cross-Branch Gated Interaction]] — the mid-network companion module
- [[concepts/deep-balanced-interaction|Deep Balanced Interaction]] — the bottleneck companion module
- [[concepts/modality-dominance|Modality Dominance]] — the failure mode DIAF partially mitigates
- [[concepts/quality-aware-speech-enhancement|Quality-Aware Speech Enhancement]] — continuous quality weighting as an alternative to reliability iteration
- [[concepts/iterative-attentional-feature-fusion|Iterative Attentional Feature Fusion]] — the rival iterative fusion design
- [[concepts/bcs-guided-speech-enhancement|BCS-Guided Speech Enhancement]] — task context

## Related Sources

- [[sources/wu-2026-dbmif-multimodal-fusion|Wu et al. 2026: DBMIF]] — introduces DIAF and visualises its SNR- and frequency-dependent weights
