---
type: concept
created: 2026-11-22
updated: 2026-11-22
sources:
  - raw/papers/abdulatif-2024-cmgan/full-text.md
tags:
  - speech-enhancement
  - conformer
  - attention
  - dual-path
  - architecture
---

# Two-Stage Conformer

A **Two-Stage Conformer (TS-Conformer)** factorizes time-frequency sequence modeling into a temporal Conformer followed by a frequency Conformer. In [[concepts/cmgan|CMGAN]], it forms a four-block bottleneck between the shared convolutional encoder and the two reconstruction decoders.

The design combines the Conformer's global self-attention with convolutional local-feature extraction while avoiding one attention operation over all time–frequency positions.

## Factorized Formulation

Given $D\in\mathbb{R}^{B\times T\times F'\times C}$, the first stage treats each frequency channel as an independent temporal sequence:

$$D^T\in\mathbb{R}^{BF'\times T\times C},\qquad
D_o^T=D^T+\operatorname{Conformer}_{T}(D^T).$$

The output is reshaped to $D^F\in\mathbb{R}^{BT\times F'\times C}$ and processed along frequency:

$$D_o^F=D^F+\operatorname{Conformer}_{F}(D^F).$$

Finally, the tensor is restored to $B\times T\times F'\times C$. CMGAN stacks four such blocks with $C=64$ and $F'=101$.

Each individual Conformer uses:

1. two half-step feed-forward networks;
2. four-head multi-head self-attention between them;
3. a convolution module containing layer normalization, pointwise convolution, GLU, 1-D depthwise convolution with Swish, a second pointwise convolution, and dropout;
4. a residual connection from block input to output.

![[raw/papers/abdulatif-2024-cmgan/figures/3573763c33ddbff77f1ff18483c25edf98dd7f1ecf53c68428f9a18937b0498c.jpg|CMGAN architecture with two-stage Conformer detail]]

*The TS-Conformer appears in panel (b): temporal processing precedes frequency processing (TASLP Fig. 2).*

## Evidence from CMGAN Ablations

| Variant | PESQ | SSNR (dB) | Interpretation |
|:--------|-----:|----------:|:---------------|
| **Sequential time → frequency** | **3.41** | **11.10** | Full CMGAN design |
| Parallel time and frequency | 3.35 | 10.63 | Lower scores; the authors suggest redundant or conflicting patterns |
| Sequential frequency → time | 3.39 | 10.84 | Competitive but consistently slightly below time → frequency |

Block depth is reported graphically rather than as a table. Moving from zero to one TS-Conformer block improves PESQ by approximately 0.4; performance continues to improve through four blocks and then saturates. This supports the chosen depth but does not establish that four blocks are optimal on other datasets or model widths.

## Scope

The TS-Conformer is a **dual-path factorization**, not a new attention primitive: its novelty lies in how standard Conformer blocks are reshaped and ordered inside CMGAN. The published model is non-causal because temporal attention can access the whole utterance; the ablations do not establish suitability for streaming enhancement.

## Related Concepts

- [[concepts/cmgan|CMGAN]] — the architecture using four TS-Conformer blocks
- [[concepts/metricgan|MetricGAN]] — the training scheme paired with this backbone
- [[concepts/complex-spectral-mapping|Complex Spectral Mapping]] — the magnitude/phase representation refined by the bottleneck
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/abdulatif-2024-cmgan|Abdulatif, Cao & Yang 2024: CMGAN]] — architecture definition, ordering ablation, and block-depth study
