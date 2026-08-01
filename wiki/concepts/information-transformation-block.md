---
type: concept
created: 2026-08-01
updated: 2026-08-01
tags:
  - speech-enhancement
  - spiking-neural-networks
  - architecture
---

# Information Transformation Block (ITB)

The ITB is a refinement module in [[concepts/sse-net|SSE-Net]] (Liu et al., IEEE/ACM TASLP 2026 — [[sources/liu-2026-sse-net|Liu et al. 2026]]) that **converts discrete spike features back into continuous signals** at the decoder output, compensating for spike quantization effects. It functions as a two-branch gating/refinement block, similar in spirit to ANN gating modules.

## Structure

Given decoder output $Z_k$ (spike-domain features over K time steps):

- **Branch 1 (self-gate)**: Conv2D → Conv2D → Sigmoid → Conv2D → ReLU:
  $$\hat{F}_1 = \phi(\mathrm{Conv2d}(\sigma(\mathrm{Conv2d}(\mathrm{Conv2d}(Z_k)))))$$
- **Branch 2 (pooled context)**: AvgPool (integrating across the spiking time dimension) → Conv2D → Sigmoid → Conv2D → ReLU:
  $$\hat{F}_2 = \phi(\mathrm{Conv2d}(\sigma(\mathrm{Conv2d}(\mathrm{AvgPool}(Z_k)))))$$
- **Fusion** (gating):
  $$\hat{F} = (\hat{F}_1 \otimes Z_k) \oplus (\hat{F}_2 \otimes (1 - \hat{F}_1))$$

with $\sigma$ = Sigmoid, $\phi$ = ReLU, $\otimes$ element-wise multiplication, $\oplus$ element-wise addition. The ITB also integrates spiking information across the K temporal dimensions and reconstructs the original feature size before the final mask-estimation Conv2D.

## Why It Matters

The naive alternative — average-sampling along the spiking time dimension — causes heavy information loss. The ITB's gated two-branch structure instead refines feature granularity and recovers speech information lost by binary activation (verified by feature-map visualization: less pixelation, finer detail, recovered features in regions where information was missing).

## Evidence

In the SSE-Net ablation (VoiceBank+DEMAND): removing the ITB drops PESQ 2.89 → 2.81; replacing it with a plain Conv2D also drops to 2.80 — showing the gated structure is not equivalent to a simple conv layer.

## Related Concepts

- [[concepts/sse-net|SSE-Net]]
- [[concepts/spiking-feature-extraction-block|Spiking Feature Extraction Block (SFEB)]]
- [[concepts/spiking-neural-networks|Spiking Neural Networks]]

## Related Sources

- [[sources/liu-2026-sse-net|Liu et al. 2026: SSE-Net]]
