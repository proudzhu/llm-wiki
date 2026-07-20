---
type: source
created: 2026-07-20
updated: 2026-07-20
sources:
  - raw/papers/chen-2023-ultra-dual-path-compression/full-text.md
  - https://doi.org/10.21437/Interspeech.2023-2302
  - zotero://select/items/0_VNWWREC6
tags:
  - speech-enhancement
  - acoustic-echo-cancellation
  - noise-suppression
  - deep-learning
  - real-time
  - model-compression
  - dual-path-transformer
---

# Chen, Yu, Luo, Gu, Li, Lu & Weng 2023: Ultra Dual-Path Compression for Joint Echo Cancellation and Noise Suppression

| Field | Value |
|-------|-------|
| **Authors** | [[entities/hangting-chen\|Hangting Chen]], [[entities/jianwei-yu\|Jianwei Yu]], [[entities/yi-luo\|Yi Luo]], [[entities/rongzhi-gu\|Rongzhi Gu]], [[entities/weihua-li\|Weihua Li]], [[entities/zhuocheng-lu\|Zhuocheng Lu]], [[entities/chao-weng\|Chao Weng]] |
| **Institution** | Tencent AI Lab, Audio and Speech Signal Processing Oteam |
| **Published** | Interspeech 2023, pp. 2048–2052 |
| **Type** | Conference paper |
| **DOI** | [10.21437/Interspeech.2023-2302](https://doi.org/10.21437/Interspeech.2023-2302) |
| **arXiv** | [2308.11053](http://arxiv.org/abs/2308.11053) |
| **Zotero** | [VNWWREC6](zotero://select/items/0_VNWWREC6) |

## Summary

This paper introduces **time-frequency dual-path compression** for the joint acoustic echo cancellation (AEC) and noise suppression (NS) task, building on an online streaming variant of [[concepts/dpt-fsnet\|DPT-FSNet]]. Two orthogonal compression axes are explored: **frequency compression** (replacing hand-designed ERB/Mel filters with trainable Mel-scale filters) and **time compression** (frame-skipped prediction with a lightweight post-processing network). Combining both axes — **dual-path compression** — covers compression ratios from 4× to 32× with model sizes held below ~500K parameters, and achieves competitive quality against Fast FullSubNet and DeepFilterNet at lower MACs/s and fewer parameters. The presented models span 57M–1822M MACs/s, giving practitioners a flexible compression-knob without resizing the backbone.

## Problem Formulation

Joint AEC + NS takes three input signals — the microphone signal $d$, the far-end reference $x$, and the linear-AEC error signal $\hat{e}$ — and estimates a clean near-end speech signal. Existing neural approaches suffer from two deployment problems:

1. **High computational cost** — most published AEC+NS networks report RTFs of 0.05–0.5 without detailed MACs/s, and still exceed mobile-platform budgets.
2. **Inflexible complexity tuning** — methods like DeepFilterNet couple model size to the compression hyper-parameter, so scaling complexity also resizes storage; the result is that "tuning their computational cost is risky".

The paper poses the question: can a single base architecture be compressed over a wide ratio range (4×–32×) **without changing model size materially** and **without sacrificing too much quality**?

The base architecture is online DPT-FSNet: a 2D-conv encoder → dual-path transformer (linear attention + GRU) → 2D-conv decoder, operating on stacked real/imaginary spectra of shape $2C \times T \times F$. Uncompressed it has 109K parameters and 1822M MACs/s.

## Methodology

### Online DPT-FSNet

The offline [[concepts/dpt-fsnet\|DPT-FSNet]] is redesigned for streaming:

- **Multi-signal input**: the input layer accepts $d$, $x$, and $\hat{e}$ from a state-space linear AEC.
- **Individual masks per input**: the output layer produces one mask per input; the final output is the sum of all masked signals.
- **Linear attention** replaces softmax attention for $\mathcal{O}(T)$ memory.
- **Single GRU after the first attention layer** replaces stacked LSTM layers in the dual-path transformer.
- **Unidirectional subband** (online) + **bidirectional fullband** (chunk-level) attention.

The feature dimension $E$ is fixed at 48; the model has ~109K parameters.

### Frequency Compression

Three variants are compared:

**Fixed triangle filters (ERB / Mel).** Compress along $F$ via a fixed filter bank $W[b, f]$:

$$Z[c, t, b] = \log\Big(\sum_{f=\text{low}[b]}^{\text{high}[b]} |X[c, t, f]| \times W_c[b, f]\Big)$$

Decompression uses the Moore–Penrose pseudo-inverse of $W$. Both [[concepts/erb-scale\|ERB]] and Mel scales are evaluated as fixed filter shapes.

**Trainable filters (TrainMel).** Replace the fixed triangle weights with a learnable linear transformation per band:

$$Z[:, t, b] = \text{Flatten}\big(X[0:C, t, \text{low}[b]:\text{high}[b]]\big) \times W, \quad W \in \mathbb{R}^{(\triangle B[b] \times C) \times E}$$

The $1 \times 1$ input convolution becomes redundant and is removed; decompression uses a separate linear transform back to $4C \times \triangle B[b]$. Trainable filters add ~300K parameters but yield >0.1 WB-PESQ improvement at 8× and 16×.

### Time Compression

**Skip prediction.** Run the heavy mask estimator once every $r$ frames and copy the predicted mask to the $r-1$ skipped frames. The compressed feature has $T' = T/r$ frames.

**Post-processing network (PostNet).** Skip prediction suffers from unmatched masks on skipped frames. A light post-processing network — feature compression → 1-layer GRU → feature decompression → stacked $1 \times 1$ convs with sigmoid — performs full-sequence refinement on the copied masks. PostNet has only 67K parameters and 15M MACs/s. It takes both the previous-stage output and the linear-AEC error $\hat{e}$ log-power spectra as input (dimension $2 \times T \times F$, with frequency compression ratio 2).

### Dual-Path Compression

Combine time and frequency compression. For a target total ratio $R$ with base 2, the search space is the set of factorizations $R = r_t \times r_f$. A grid search over $(r_t, r_f)$ finds the optimal split. The paper notes that the order (T-then-F vs. F-then-T) has little impact; they adopt time-compress → frequency-compress → frequency-decompress → time-decompress (Figure 2 of the paper).

![[raw/papers/chen-2023-ultra-dual-path-compression/figures/425f3eb977a3a22fff19e22de26bbc90a50ba327061e5d56b36e8f1c3e1c0840.jpg|Dual-path compression and decompression pipeline]]

*Figure 2: Dual-path compression and decompression.*

### Architectural Pipeline

![[raw/papers/chen-2023-ultra-dual-path-compression/figures/da3e599f9643031b179fb749648dd6e417df3ec88d576db14e62d2c881906ea6.jpg|Joint echo and noise suppression pipeline with optional compression modules]]

*Figure 1: Joint echo and noise suppression pipeline. Dashed boxes are optional compression modules.*

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Sampling rate | 16 kHz |
| STFT window | 20 ms |
| Hop size | 10 ms |
| Linear AEC | state-space Kalman-style filter (Kuech et al. 2014; Enzner & Vary 2006) |
| Encoder/decoder | 2-layer 2D convolution |
| Dual-path attention | 4 layers, linear attention |
| Dual-path GRU | 1 layer |
| Feature dim $E$ | 48 |
| Uncompressed model | 109K params, 1822M MACs/s |
| PostNet band count $B$ | 80 |
| Optimizer | Adam, 8-GPU, batch 80, 105K iterations |
| Model averaging | checkpoints at 95K / 100K / 105K |
| Training set | 530 h simulated (LibriSpeech train-clean-100/360 + DNS-Challenge noise + simulated RIRs) |
| Validation / eval | 10 h / 10 h |
| Eval echo source | real-recorded from AEC-Challenge (covers various devices & delays) |
| Scenarios | ST-FE, ST-NE, DT |
| SER / SNR | uniformly −5 to 15 dB (train/val); {−5, 5, 15, +∞} dB (eval) |
| Metrics | ERLE (ST-FE), SI-SNR / WB-PESQ / STOI (ST-NE, DT) |

## Results

### Compression Comparison (Table 1, DT scenario)

| Method | T×F Ratio | Params | MACs/s | Compr. | DT SI-SNR | DT WB-PESQ | DT STOI | ST-FE ERLE |
|--------|----------|-------:|-------:|-------:|----------:|-----------:|--------:|-----------:|
| Fast FullSubNet | — | 7601K | 1433M | — | 11.33 | 2.68 | 87.05 | 40.66 |
| DeepFilterNet | — | 2000K | 289M | — | 10.96 | 2.68 | 86.90 | 44.49 |
| Uncompressed | 1×1 | 109K | 1822M | 1.0 | 12.14 | 2.78 | 87.96 | 46.82 |
| FixedERB | 1×2 | 109K | 910M | 2.0 | 10.10 | 2.54 | 85.14 | 43.99 |
| FixedMel | 1×2 | 109K | 910M | 2.0 | 11.18 | 2.69 | 86.82 | 44.33 |
| TrainMel | 1×2 | 413K | 937M | 1.9 | 11.89 | 2.73 | 87.73 | 44.68 |
| SkipPred | 2×1 | 109K | 917M | 2.0 | 11.31 | 2.68 | 86.80 | 40.44 |
| +PostNet | 2×1 | 177K | 931M | 2.0 | 11.86 | 2.75 | 87.66 | 43.83 |
| TrainMel | 1×4 | 408K | 484M | 3.8 | 11.44 | 2.69 | 86.97 | 42.13 |
| SkipPred+PostNet | 4×1 | 177K | 477M | 3.8 | 10.88 | 2.61 | 85.98 | 38.35 |
| **DualPath** | **2×2** | **481K** | **486M** | **3.7** | **11.59** | **2.72** | **87.44** | **42.63** |
| TrainMel | 1×8 | 398K | 257M | 7.1 | 10.66 | 2.56 | 85.36 | 41.10 |
| SkipPred+PostNet | 8×1 | 178K | 250M | 7.3 | 9.78 | 2.47 | 84.35 | 36.64 |
| **DualPath** | **2×4** | **476K** | **261M** | **7.0** | **11.26** | **2.68** | **86.82** | **42.06** |
| TrainMel | 1×16 | 381K | 142M | 12.8 | 9.78 | 2.40 | 83.37 | 40.48 |
| SkipPred+PostNet | 16×1 | 181K | 136M | 13.4 | 9.03 | 2.42 | 83.68 | 35.73 |
| **DualPath** | **4×4** | **477K** | **140M** | **13.0** | **10.41** | **2.56** | **85.73** | **39.34** |
| TrainMel | 1×32 | 354K | 84M | 21.7 | 8.57 | 2.24 | 81.16 | 34.46 |
| SkipPred+PostNet | 32×1 | 185K | 79M | 23.1 | 8.47 | 2.40 | 83.19 | 32.81 |
| **DualPath** | **4×8** | **467K** | **83M** | **22.0** | **9.73** | **2.47** | **84.72** | **38.54** |

### Key Findings

1. **TrainMel > FixedMel > FixedERB** at every ratio on WB-PESQ. The Mel scale emphasises low frequencies that WB-PESQ weights; ERB wins on SI-SNR at large ratios because SI-SNR weights all frequencies equally.
2. **PostNet recovers >0.2 WB-PESQ** across 4×–32×, with only 67K extra parameters and 15M MACs/s. It is the single most cost-effective addition in the time-compression family.
3. **DualPath outperforms single-path at 8× and 16×** by ~0.1 WB-PESQ and ~0.5 dB SI-SNR at similar MACs/s. Splitting the compression burden across both axes avoids the information loss incurred by compressing one axis excessively.
4. **DualPath's weakness: ERLE.** The PostNet in the time path drags down ST-FE ERLE (e.g., 32× DualPath 38.54 vs. TrainMel-only 34.46 — actually comparable; but at 4× DualPath 42.63 vs. TrainMel 42.13 — close; at 16× DualPath 39.34 vs. TrainMel 40.48 — TrainMel wins). The authors flag this as future work.
5. **Vs. Fast FullSubNet**: TrainMel at 2× compression (937M MACs/s, 413K params) beats Fast FullSubNet (1433M MACs/s, 7601K params) on every metric while being ~17× smaller in parameters.
6. **Vs. DeepFilterNet**: DualPath(2×4) at 476K params / 261M MACs/s matches DeepFilterNet (2000K params / 289M MACs/s) on quality, at **1/4 the storage**.

### Compression Ratio Coverage

The 4×–32× range yields MACs/s from ~486M down to ~83M, spanning an order of magnitude in compute cost with model size held near 0.5M parameters. The authors note that compression ratios >32× are left for future work because the compression/decompression modules themselves begin to dominate cost.

## Key Contributions

1. **Dual-path compression framework** — a grid-search-based combination of time and frequency compression that, under a fixed total ratio, consistently outperforms either axis alone by sharing the information-loss burden across both axes.
2. **Trainable Mel-scale frequency compression** — replacing hand-designed ERB/Mel triangle filters with learnable linear transforms yields >0.1 WB-PESQ gain at 8× and 16× with ~300K extra parameters, and allows the input $1 \times 1$ conv to be removed.
3. **Frame-skip prediction + lightweight post-processing network (PostNet)** — PostNet recovers most of the quality lost from skip prediction at only 67K params / 15M MACs/s, making time compression practical.
4. **Wide-range complexity tuning without model resize** — a single 109K-parameter base architecture covers 57M–1822M MACs/s by changing only the compression ratio, unlike DeepFilterNet where tuning complexity resizes the model.
5. **Quantitative comparison showing 4× parameter reduction vs. DeepFilterNet** at matched quality (DualPath(2×4) at 476K vs. DeepFilterNet at 2000K).

## Related Concepts

- [[concepts/dpt-fsnet\|DPT-FSNet]]
- [[concepts/dual-path-compression\|Dual-Path Compression]]
- [[concepts/trainable-frequency-compression\|Trainable Frequency Compression]]
- [[concepts/frame-skip-prediction\|Frame-Skip Prediction]]
- [[concepts/post-processing-network\|Post-Processing Network]]
- [[concepts/erb-scale\|ERB Scale]]

## Related Synthesis

- [[synthesis/joint-multitask-ultra-low-latency-se\|Joint Multi-Task Speech Enhancement & Ultra-Low-Latency Realtime Paradigm]] — Chen et al. 2023 provides an early (2023) data point on the compression-ratio flexibility axis, complementing later compression strategies (HALO frame-rate reduction, RT-Tango FRS, Castelli's stage-wise embedded compression).

## Related Sources

- [[sources/indenbom-2023-deepvqe\|Indenbom et al. 2023: DeepVQE]] — co-evaluated AEC challenge work; DeepVQE uses a shared-backbone multi-task strategy at 7.5M params (vs. Chen's compressed 0.5M)
- [[sources/schroter-2022-deepfilternet\|Schröter et al. 2022: DeepFilterNet]] — explicit baseline; Chen matches DeepFilterNet's quality at 1/4 the parameters via dual-path compression
- [[sources/valin-2021-percepnet-joint-echo-control\|Valin et al. 2021: PercepNet Joint Echo Control]] — earlier hybrid AEC + PercepNet-style joint residual echo/noise suppression at 8M params / 800M MACs/s; Chen et al. operate in the same joint AEC+NS regime with two orders of magnitude smaller models
- [[sources/castelli-2025-embedded-joint-aec-ns\|Castelli 2024: Embedded Joint AEC and NS]] — later deployment-focused work that compresses a DeepVQE-s backbone onto a HiFi4 DSP; orthogonal compression strategy (per-stage surgical cuts) to Chen's grid-searched dual-path compression
