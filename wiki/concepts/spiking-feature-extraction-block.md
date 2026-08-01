---
type: concept
created: 2026-08-01
updated: 2026-08-01
tags:
  - speech-enhancement
  - spiking-neural-networks
  - architecture
---

# Spiking Feature Extraction Block (SFEB)

The SFEB is the core building block of [[concepts/sse-net|SSE-Net]] (Liu et al., IEEE/ACM TASLP 2026 — [[sources/liu-2026-sse-net|Liu et al. 2026]]). A **three-branch residual block** that converts features to spike streams via LIF neurons while preserving a continuous (non-spiked) feature path, mitigating the information loss caused by discrete binary activation.

## Structure

Given input $A_k$ at spiking time step $k$ (after an initial Conv2D feature projection):

- **Branch 1 (spiking)**: LIF → Conv2D(3×1) → GroupNorm, applied twice:
  $$\hat{X}_{k1} = \mathrm{GN}(\mathrm{Conv2D}(\mathrm{LIF}(\mathrm{GN}(\mathrm{Conv2D}(\mathrm{LIF}(A_k))))))$$
- **Branch 2 (continuous)**: Conv2D → GroupNorm:
  $$\hat{X}_{k2} = \mathrm{GN}(\mathrm{Conv2D}(A_k))$$
- **Fusion**: element-wise addition of both branches with the original input:
  $$\hat{X}_k = A_k \oplus \hat{X}_{k1} \oplus \hat{X}_{k2}$$

The spiking branch operates on 0/1 spikes (LIF fires when the membrane potential crosses the threshold); the continuous branch preserves information that binary quantization would discard; the residual connection gives gradients a clean path.

## SFEG

A **Spiking Feature Extraction Group (SFEG)** = N SFEBs + a DownSampling Block (LIF → Conv2D → GroupNorm), forming one encoder stage. The decoder mirrors this with SFEB + UpSampling.

## Evidence

In the SSE-Net ablation (VoiceBank+DEMAND), replacing SFEB with a plain LIF module drops PESQ from 2.89 → 2.70 and STOI 94.0% → 93.5%, demonstrating the residual spiking structure preserves critical information even under binary input.

## Related Concepts

- [[concepts/sse-net|SSE-Net]]
- [[concepts/information-transformation-block|Information Transformation Block (ITB)]]
- [[concepts/spiking-neural-networks|Spiking Neural Networks]] — LIF neuron model

## Related Sources

- [[sources/liu-2026-sse-net|Liu et al. 2026: SSE-Net]]
