---
type: concept
created: 2026-10-27
updated: 2026-10-27
sources:
  - raw/papers/baek-2025-geometry-invariant-doa-estimation/full-text.md
tags:
  - multi-channel
  - deep-learning
  - microphone-arrays
  - geometry-invariant
  - attention-mechanism
---

# Channel-Wise Softmax Aggregation (CWSA)

**Channel-Wise Softmax Aggregation (CWSA)** is a permutation-invariant operator that collapses the channel axis of a multichannel latent tensor into a **single** channel by combining an attention-weighted *sum* with an attention-weighted *standard deviation*. Introduced by Baek, Chang & Cohen (2025) inside [[sources/baek-2025-geometry-invariant-doa-estimation|GI-DOAEnet]], where it both improves DOA accuracy and is the main reason the model's cost grows only **linearly** with the microphone count.

## Formulation

For a tensor $\mathbf{Y}^{\text{CWSA}} \in \mathbb{R}^{C \times M}$ (one frame):

$$\mathbf{Y}^{\text{Softmax}} = \mathrm{Softmax}_{\text{channel}}\left(\mathbf{Y}^{\text{CWSA}}\right) \odot \mathbf{Y}^{\text{CWSA}}$$

$$\mathbf{Y}^{\text{sum}} = \sum_{c=1}^{C} \mathbf{Y}^{\text{Softmax}}_c, \qquad
\mathbf{Y}^{\text{std}} = \sqrt{\frac{1}{C-1}\sum_{c=1}^{C}\left(\mathbf{Y}^{\text{Softmax}}_c - \frac{\mathbf{Y}^{\text{sum}}}{C}\right)^2}$$

$$\mathbf{Y}^{\text{GRU,in}} = \begin{bmatrix} \mathbf{Y}^{\text{sum}} \\ \mathbf{Y}^{\text{std}}\end{bmatrix} \in \mathbb{R}^{2M}$$

The Softmax is applied **along the channel dimension** (per feature element), so each latent dimension independently decides which microphone to trust — a form of channel attention that reuses no extra parameters. Sum and standard deviation are both permutation-invariant, so the operator is invariant to microphone ordering, which is a prerequisite for [[concepts/array-invariant-speech-enhancement|array invariance]].

## Why the Standard Deviation?

A plain mean/sum aggregation discards *channel disagreement*. The std branch keeps a scalar-per-feature measure of how much the channels disagree — precisely the quantity that carries inter-microphone phase/level discrepancy, and hence spatial information. In the ablation, removing the std branch shrinks the aggregated feature from $2M$ to $M$ and degraded every dataset for the PM variant (Dynamic MAE 14.59° → 17.68°) — although the FM variant occasionally improved, so the branch is cheap insurance rather than a strict requirement.

## Why It Also Saves Compute

CWSA is applied **between** the channel-wise attention block and the frame-wise GRU. Collapsing $C \times M$ to $2M$ before the recurrent stage means:

- the FW-GRUs and the spatial-spectrum heads never see the channel dimension, so their cost is independent of $C$;
- the only $\mathcal{O}(C^2)$ component left is the channel-wise multi-head self-attention (CW-MHSA), applied per frame and once per dual-path block;
- net effect: FLOPS, memory and inference time grow roughly **linearly** in $C$ (0.46 → 0.85 → 1.25 GFLOPS for 4 → 8 → 12 channels; GPU latency 2.60 → 2.69 ms), whereas pair-wise-feature pipelines (SRP-PHAT, Neural-SRP) grow quadratically.

Removing the Softmax from CWSA was the worst CWSA ablation in the paper (Dynamic MAE 14.59° → 19.43° for PM), so the attention weighting — not only the std branch — is doing real work.

## Related Concepts

- [[concepts/array-invariant-speech-enhancement|Array-Invariant Speech Enhancement]]
- [[concepts/permutation-invariant-training|Permutation Invariant Training (PIT)]] — the wider family of permutation-invariant operators (mean/sum/std/Softmax/MHSA)
- [[concepts/channel-wise-feature-reorientation|Channel-Wise Feature Reorientation]] — a different strategy for mixing information across channels while keeping channel-count invariance
- [[concepts/attention-mechanism|Attention Mechanism]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/complexity-gradual-training|Complexity Gradual Training (CGT)]] — the training scheme used alongside CWSA on the same model

## Related Sources

- [[sources/baek-2025-geometry-invariant-doa-estimation|Baek, Chang & Cohen 2025: DNN-Based Geometry-Invariant DOA Estimation With Microphone Positional Encoding and Complexity Gradual Training]]
