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
  - gating
---

# Cross-Branch Gated Interaction

**Cross-Branch Gated Interaction (CBGI)** is the bidirectional gating module that lets three parallel encoder streams in DBMIF (one AC, one BC, one fusion) modulate each other at every encoder scale. It is the single largest ablation contributor in that system (~6–7 absolute CER points on both ASR backends), and its authors report that a standard Gated Multimodal Unit performed worse — the *bidirectionality* is the point, not gating as such.

## Key Formulations

At encoder stage $s$, with features $\mathbf{x}_a^{(s)}, \mathbf{x}_b^{(s)}, \mathbf{x}_f^{(s)}$ for AC, BC and fusion branches:

**Stage 1 — fusion-to-unimodal modulation.** The fusion stream supplies global context that suppresses irrelevant components in each unimodal branch:

$$
g_{fa}^{(s)} = \sigma\left(\mathcal{F}_{\mathrm{conv}}(\mathrm{x}_f^{(s)})\right), \qquad \tilde{\mathrm{x}}_a^{(s)} = g_{fa}^{(s)} \odot \mathcal{F}_{\mathrm{conv}}(\mathrm{x}_a^{(s)})
$$
$$
g_{fb}^{(s)} = \sigma\left(\mathcal{F}_{\mathrm{conv}}(\mathrm{x}_f^{(s)})\right), \qquad \tilde{\mathrm{x}}_b^{(s)} = g_{fb}^{(s)} \odot \mathcal{F}_{\mathrm{conv}}(\mathrm{x}_b^{(s)})
$$

**Stage 2 — unimodal-to-fusion feedback.** Each unimodal branch gates the fusion stream with its own reliability, and the gated contributions are summed:

$$
g_a^{(s)} = \sigma\left(\mathcal{F}_{\mathrm{conv}}(\mathrm{x}_a^{(s)})\right), \qquad \hat{\mathrm{x}}_{af}^{(s)} = g_a^{(s)} \odot \mathcal{F}_{\mathrm{conv}}(\mathrm{x}_f^{(s)})
$$
$$
\tilde{\mathrm{x}}_f^{(s)} = \hat{\mathrm{x}}_{af}^{(s)} + \hat{\mathrm{x}}_{bf}^{(s)}
$$

All $\mathcal{F}_{\mathrm{conv}}$ are distinct $1\times1$ convolutions, so the module adds no spatial mixing and negligible parameters; $\sigma$ is the logistic sigmoid; $\odot$ is element-wise multiplication.

## Why Bidirectional

| Design | Information flow | Failure mode |
|:-------|:-----------------|:-------------|
| Concatenation | none (one junction) | modality dominance; no recovery after fusion |
| Unidirectional fusion→branch | fusion → unimodal only | fusion never learns which modality is currently trustworthy |
| GMU | learned scalar mix | collapses to a single modality under low SNR |
| **CBGI** | fusion ↔ each branch, closed loop | dominance is continuously renegotiated at every scale |

The closed loop means a degraded AC branch (low gate $g_a$) damps its own contribution to the fusion stream, while the fusion stream's own gate $g_{fa}$ can still pass BC context back into the AC branch — the two mechanisms act on different variables and do not cancel.

In DBMIF, CBGI sits inside the three-branch multi-scale encoder–decoder (channel widths {32, 64, 128, 256} per stage) and is preceded by early [[concepts/deep-iterative-attention-fusion|DIAF]] fusion and followed by the [[concepts/deep-balanced-interaction|DBI]] bottleneck.

## Related Concepts

- [[concepts/deep-iterative-attention-fusion|Deep Iterative Attention Fusion]] — the early-network companion
- [[concepts/deep-balanced-interaction|Deep Balanced Interaction]] — the bottleneck companion
- [[concepts/modality-dominance|Modality Dominance]] — what the bidirectional loop defends against
- [[concepts/attention-gate|Attention Gate]] — the unidirectional gating primitive
- [[concepts/cross-path-fusion|Cross-Path Fusion]] — related multi-path exchange designs
- [[concepts/bcs-guided-speech-enhancement|BCS-Guided Speech Enhancement]] — task context

## Related Sources

- [[sources/wu-2026-dbmif-multimodal-fusion|Wu et al. 2026: DBMIF]] — introduces CBGI; ablation shows it dominates the other two modules
