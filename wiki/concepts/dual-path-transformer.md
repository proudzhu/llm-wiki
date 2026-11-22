---
type: concept
created: 2026-11-22
updated: 2026-11-22
sources:
  - raw/papers/dang-2022-dpt-fsnet/full-text.md
tags:
  - speech-enhancement
  - speech-separation
  - transformer
  - dual-path
  - deep-learning
---

# Dual-Path Transformer

The **dual-path transformer (DPT)** family applies the [[concepts/dprnn|dual-path]] local/global decomposition with transformer blocks instead of RNNs: elements interact directly through self-attention along each of two axes of a 2D representation. Introduced as **DPTNet** by Chen, Mao & Liu (Interspeech 2020) for end-to-end monaural speech separation, alongside variants such as TransMask (Zhang et al., ICASSP 2021).

## Improved Transformer Block

The family's signature modification (DPTNet, adopted by [[concepts/dpt-fsnet|DPT-FSNet]]): the transformer encoder keeps **multi-head self-attention** but replaces the first fully-connected layer of the position-wise feed-forward network with a **GRU**, and drops positional encoding entirely — positional encodings were found unsuitable for dual-path networks, while recurrence tracks order information naturally (after Sperber et al. 2018):

$$\mathrm{FFN}(Z) = \mathrm{ReLU}(\mathrm{GRU}(Z))W_1 + b_1, \qquad d_{ff} = 4d$$

Each sub-module is followed by residual connection and normalization (LayerNorm in the DPT-FSNet text; GroupNorm in its Fig. 1).

## Axis Assignments Across the Family

| Model | Domain | Intra path | Inter path |
|:------|:-------|:-----------|:-----------|
| DPTNet (Chen et al. 2020) | Time (segmented waveform) | Within-chunk (local) | Across-chunk (global) |
| [[concepts/dpt-fsnet\|DPT-FSNet]] (Dang et al. 2022) | STFT T-F map | Per frequency bin, over $T$ frames (**sub-band**) | Per frame, over $F$ bins (**full-band**) |
| Online DPT-FSNet ([[sources/chen-2023-ultra-dual-path-compression\|Chen et al. 2023]]) | STFT, streaming | Unidirectional sub-band, linear attention | Bidirectional full-band (chunk-level) |
| [[concepts/cie-mdptnet\|CIE-mDPTNet]] (Yang et al. 2024) | STFT, TSE | Context interaction between enrollment and mixture directly in the STFT domain | — |

DPT-FSNet's controlled ablation is the family's clearest evidence that **the input representation matters**: at matched parameters, complexity, and latency, STFT input beats TSTNN-style time-domain segmentation by +0.36 WB-PESQ (2.97 → 3.33) on VoiceBank+DEMAND.

## Cost and Operator Alternatives

Softmax attention on both paths makes offline DPTs compute-heavy — the online DPT-FSNet redesign reports 1822M MACs/s at only 109K parameters, motivating [[concepts/dual-path-compression|dual-path compression]]. Later work swaps operators per axis rather than compressing: [[concepts/rnnformer|RNNFormer]] (time GRU + frequency MHSA) ablates against both DPRNN and DPT alternatives in FastEnhancer, and the [[concepts/ftf-transformer|FTF transformer]] shares parameters across the non-modeled axis to shrink three-stage dual-path blocks.

## Related Concepts

- [[concepts/dprnn|Dual-Path RNN (DPRNN)]] — the recurrent predecessor
- [[concepts/dpt-fsnet|DPT-FSNet]] — frequency-domain instantiation for SE
- [[concepts/full-band-sub-band-fusion|Full-Band and Sub-Band Fusion]] — the paradigm DPT-FSNet realizes inside the DPT
- [[concepts/cie-mdptnet|CIE-mDPTNet]] — TSE backbone in this family
- [[concepts/rnnformer|RNNFormer]] · [[concepts/ftf-transformer|FTF Transformer]] — operator-sharing alternatives
- [[concepts/attention-mechanism|Attention Mechanism]]
- [[concepts/dual-path-compression|Dual-Path Compression]]

## Related Sources

- [[sources/dang-2022-dpt-fsnet|Dang, Chen & Zhang 2022: DPT-FSNet]] — T-F-domain DPT with sub-band/full-band axis assignment and the input-representation ablation
- [[sources/chen-2023-ultra-dual-path-compression|Chen et al. 2023: Ultra Dual-Path Compression]] — streaming linear-attention redesign of DPT-FSNet
- [[sources/ahn-2026-fastenhancer|Ahn et al. 2026: FastEnhancer]] — ablates DPT alternatives against RNNFormer's axis-operator assignment