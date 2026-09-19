---
type: concept
created: 2026-06-01
updated: 2026-09-19
sources:
  - raw/papers/ansari-2023-ai-bss-survey/full-text.md
  - raw/papers/pan-2025-data-driven-acoustics/full-text.md
tags:
  - speech-separation
  - speaker-separation
  - deep-learning
  - clustering
---

# Deep Clustering for Speech Separation

Deep clustering is a speaker-independent speech separation approach that combines DNN-based feature learning with spectral clustering (Hershey et al. 2016).

## Formulation

The DNN learns high-dimensional embeddings for each time-frequency unit such that units belonging to the same speaker have similar embeddings. Training minimizes the Frobenius norm difference between the estimated and true affinity matrices.

## Loss Formulation (Pan 2025)

[[sources/pan-2025-data-driven-acoustics|Pan 2025]] writes the objective explicitly with $\bm{V} \in \mathbb{R}^{L \times KT}$ the per-TF-bin embedding matrix (reshaped from a $K \times T \times L$ tensor) and $\bm{U}$ the one-hot source-assignment matrix:

$$
\mathcal{J}_{2} = \|\bm{V}^{T}\bm{V} - \bm{U}^{T}\bm{U}\|^{2}
$$

— the $(i,j)$ entry of $\bm{V}^{T}\bm{V}$ is the inner product of TF-bin embeddings, and $\bm{U}^{T}\bm{U}$ is 1 only for same-source TF pairs, so minimization drives different sources' embeddings toward orthogonality. It is combined with a [[concepts/permutation-invariant-training|PIT]] mask-estimation loss, $\mathcal{J}_{3} = \beta \mathcal{J}_{2} + \mathcal{J}_{\text{PIT-mask}}$, trading off the two terms ($\beta \geq 0$). Because same-source embeddings cluster tightly, the **clustering center can serve as that source's voiceprint**, usable as a conditioning prior for extracting a specified source (Wavesplit) — linking deep clustering to [[concepts/target-speaker-extraction|target speaker extraction]].

## Inference

1. Mixture is segmented into overlapping windows
2. DNN computes embedding vectors for each T-F unit
3. K-means clusters T-F units into speaker groups
4. Each group constructs a mask for speaker separation

## Key Properties

- **Speaker-independent**: No assumption about which speakers are present
- **Flexible**: Naturally handles mixtures with more than two speakers
- **Extension**: Deep attractor network improves results by creating attractor points for each speaker

## Related Concepts

- [[concepts/permutation-invariant-training|Permutation Invariant Training (PIT)]]
- [[concepts/ideal-binary-mask|Ideal Binary Mask (IBM)]]
- [[concepts/ideal-ratio-mask|Ideal Ratio Mask (IRM)]]
- [[concepts/target-speaker-extraction|Target Speaker Extraction (TSE)]] — clustering centers double as voiceprint priors

## Related Sources

- [[sources/wang-2018-supervised-speech-separation-deep-learning-overview|Wang & Chen 2018: Supervised Speech Separation Based on Deep Learning: An Overview]]
- [[sources/ansari-2023-ai-bss-survey|Ansari et al. 2023: AI Approaches in BSS Survey]] — classifies deep clustering as one of the surveyed DL-based BSS methods (Refs. [97, 137, 160]).
- [[sources/pan-2025-data-driven-acoustics|Pan 2025: Fundamentals of Data-Driven Approaches to Acoustic Signal Detection, Filtering, and Transformation]] — explicit affinity-matching loss and its combination with PIT mask losses (Section 8.6)
