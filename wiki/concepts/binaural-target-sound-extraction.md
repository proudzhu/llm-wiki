---
type: concept
created: 2026-09-27
updated: 2026-09-27
sources:
  - raw/papers/veluri-2023-semantic-hearing/full-text.md
tags:
  - target-sound-extraction
  - binaural-processing
  - neural-network
  - spatial-audio
---

# Binaural Target Sound Extraction

**Binaural target sound extraction** (BTSE) is the task of extracting one or more target sound classes from a two-channel (left/right ear) mixture while preserving the spatial cues — [[concepts/interaural-time-difference|interaural time differences]] (ITD) and [[concepts/interaural-level-difference|interaural level differences]] (ILD) — of the target sounds in the binaural output. Veluri et al. (UIST 2023) presented the first neural network achieving BTSE in real time on a smartphone.

## Problem Setup

Given binaural input $s \in \mathbb{R}^{2 \times T}$ and a class query $q$, produce $\hat{s} \in \mathbb{R}^{2 \times T}$ containing only target-class sounds, with the interaural differences of each target matching those of the true binaural target signal. Evaluation metrics combine signal quality (SI-SNRi, computed per channel and averaged) with spatial-cue accuracy (ΔITD via cross-correlation limited to ±1 ms; ΔILD in dB, both measured against ground-truth binaural signals).

## Framework Variants

| Framework | Description | Trade-off |
|-----------|-------------|-----------|
| **Dual-channel** (Veluri 2023) | Both ears mapped to one shared latent representation by the input convolution; a single mask estimator produces a jointly-applied mask. | ~50% lower runtime; best ΔILD (shared representation preserves inter-channel amplitude relations). |
| **Parallel** (Han et al. 2020) | Separate per-ear branches with cross-communication; originally proposed for binaural speech separation. | Slightly better ΔITD/SI-SNRi, but ~2× runtime and worse ΔILD. |
| **Single-channel ×2** | One monaural model applied independently to each ear. | No inter-channel communication → poor ΔILD; 2× runtime. |

## Architecture (Veluri et al. 2023)

A causal, streaming encoder–decoder built on a modified [[concepts/waveformer|Waveformer]]: a dilated-causal-convolution encoder (10 layers, Fast WaveNet streaming) processes chunks with a 1–1.5 s past-only receptive field; a transformer decoder conditioned on a label embedding estimates the latent mask; the mask is applied to the shared binaural latent representation and a transposed convolution reconstructs the binaural output. The scale-sensitive SNR loss averaged over the two channels prevents inter-channel gain collapse (a problem observed when training Conv-TasNet with SI-SNR-containing losses in the binaural setting).

![[raw/papers/veluri-2023-semantic-hearing/figures/dfd312fe1d1bb484883e8f5b8cea6ab6d72794d1ff78f94c12c11832b65978e5.jpg|Binaural target sound extraction network architecture]]
*Figure 6: Binaural extraction framework and mask estimation network (Veluri et al. 2023).*

## Key Results (Veluri et al. 2023)

- Dual-channel D=128: 7.17 dB SI-SNRi, ΔITD 87.77 µs, ΔILD 0.88 dB, 6.56 ms runtime per 10 ms chunk on iPhone 11 (0.52 M params).
- In-the-wild spatial-cue study: perceived-direction median error 9° vs 5° for clean sounds; 90th percentile 42° vs 38°.
- Robust to listener/source motion at 30–90 °/s.

## Related Concepts

- [[concepts/target-sound-extraction|Target Sound Extraction]]
- [[concepts/semantic-hearing|Semantic Hearing]]
- [[concepts/waveformer|Waveformer]]
- [[concepts/interaural-time-difference|Interaural Time Difference (ITD)]]
- [[concepts/interaural-level-difference|Interaural Level Difference (ILD)]]
- [[concepts/head-related-transfer-function|Head-Related Transfer Function (HRTF)]]

## Related Sources

- [[sources/veluri-2023-semantic-hearing|Veluri et al. 2023: Semantic Hearing]]
