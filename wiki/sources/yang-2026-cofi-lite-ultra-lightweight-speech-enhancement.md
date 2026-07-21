---
type: source
created: 2026-07-21
updated: 2026-07-21
sources:
  - raw/papers/yang-2026-cofi-lite-ultra-lightweight-speech-enhancement/full-text.md
  - https://doi.org/10.1109/LSP.2026.3712291
  - zotero://select/items/0_NUV4VYRE
tags:
  - speech-enhancement
  - lightweight-model
  - convolutional-recurrent-network
  - dual-path
  - ieee-spl-2026
---

# Yang, Wang, Rong, Zhao & Lu 2026: CoFi-Lite — Pushing the Limits of Ultra-Lightweight Speech Enhancement

**Authors**: [[entities/leyan-yang|Leyan Yang]], [[entities/dahan-wang|Dahan Wang]], [[entities/xiaobin-rong|Xiaobin Rong]], [[entities/jiadong-zhao|Jiadong Zhao]], [[entities/jing-lu|Jing Lu]]
**Affiliations**: Key Laboratory of Modern Acoustics, Nanjing University
**Venue**: IEEE Signal Processing Letters, 2026
**Type**: Journal Article (Letter)
**DOI**: [10.1109/LSP.2026.3712291](https://doi.org/10.1109/LSP.2026.3712291)
**Zotero**: [Open in Zotero](zotero://select/items/0_NUV4VYRE)

## Summary

[[concepts/cofi-lite|CoFi-Lite]] is an ultra-lightweight speech enhancement model requiring only **12.87M MACs/s and 83.12k parameters** — yet it outperforms the previous ultralightweight baseline [[sources/rong-2024-gtcrn-speech-enhancement-ultralow|GTCRN]] (PESQ 2.16 vs. 2.07 on DNS3) at just **40.26% of its computational cost** and 34% lower RTF. The key idea is to *decouple* spectral modeling into two parallel, symmetric encoder-decoder paths: a deeply compressed **coarse path** that enhances the full-band magnitude envelope, and a high-resolution **fine path** restricted to low frequencies (below 2 kHz) that recovers detail lost to compression. A novel [[concepts/cross-path-fusion|Cross-Path Fusion (CPF)]] module bridges the two paths at their bottlenecks, providing a +0.14 PESQ gain in ablation. A scaled-up variant, CoFi-Lite (Large), matches the SOTA ultra-lightweight AdaptCRN with 19.34% fewer MACs.

## Problem Formulation

Given a noisy mixture $x$, STFT yields the complex spectrum $\mathbf{X} \in \mathbb{C}^{T \times F}$. The task is to restore the clean magnitude spectrum; the enhanced complex spectrum reuses the noisy phase $\angle \mathbf{X}$ followed by iSTFT. Phase is deliberately not modeled — ultra-lightweight models lack the capacity for accurate phase modeling, and magnitude-only processing gives a better performance-complexity trade-off (at the cost of an upper bound on theoretical performance).

**The motivating observation**: a straightforward way to push a [[concepts/convolutional-recurrent-network|CRN]]-based SE model below ~30M MACs/s is uniform downscaling (fewer layers, channels, spectral resolution), but the authors' preliminary experiments show this degrades performance rapidly — particularly in **low-frequency bands**, where noise is insufficiently suppressed. Pushing the complexity limit therefore requires *allocating modeling capacity asymmetrically across frequency regions* rather than shrinking the whole network.

Prior work does not solve this: full/sub-band and multi-scale methods lack explicit emphasis on low-frequency recovery; cascaded coarse-to-fine two-stage designs (Dang et al. 2023) suffer from error accumulation and one-way information flow; parallel dual-branch designs with cross-domain interaction had only been explored in multi-channel SE, not ultra-lightweight monaural SE.

## Methodology

### Overall Architecture

![[raw/papers/yang-2026-cofi-lite-ultra-lightweight-speech-enhancement/figures/44ad400d7063952cadcbc305668a927c65634d5419d0809afa3c58ea54b46e24.jpg|CoFi-Lite architecture]]

*Figure 1: (a) CoFi-Lite overall diagram — two parallel coarse/fine encoder-decoder paths bridged by the CPF module; (b) the MB block; (c) the CPF module.*

CoFi-Lite comprises two parallel paths built on the standard CRN framework (encoder, decoder, and two inter-frame RNNs as bottleneck enhancers), bridged by the CPF module. Each path predicts an [[concepts/ideal-ratio-mask|ideal ratio mask]]; the two masks are applied **sequentially** — the coarse mask $\mathbf{M}_\mathrm{c}$ restores the full-band envelope, and the fine mask $\mathbf{M}_\mathrm{f}$ refines only the low-frequency region:

$$|\tilde{\mathbf{S}}(t,f)| = \begin{cases} |\mathbf{X}(t,f)| \otimes \mathbf{M}_\mathrm{c}(t,f) \otimes \mathbf{M}_\mathrm{f}(t,f), & f \leq f_\text{low} \\ |\mathbf{X}(t,f)| \otimes \mathbf{M}_\mathrm{c}(t,f), & f > f_\text{low} \end{cases}$$

with cutoff index $f_\text{low} = 65$ corresponding to 2 kHz.

### Coarse Path (Full-Band Envelope)

The coarse input compresses sparse high-frequency content with the [[concepts/erb-scale|ERB]]-based Band Merging (BM) module inherited from [[concepts/gtcrn|GTCRN]], keeping the first 65 bands unaltered and merging 192 high-frequency bands into 64:

$$\mathbf{I}_\mathrm{c} = \mathcal{F}_\text{SFE}\left(\log_{10}\left(\mathcal{F}_\text{ERB}\left(|\mathbf{X}|\right)\right)\right)$$

where $\mathcal{F}_\text{SFE}$ is GTCRN's Subband Feature Extraction module. The encoder stacks three **MB blocks** (derived from UL-UNAS: point-wise conv → depth-wise conv → point-wise conv, integrated with GTCRN's Temporal Recurrent Attention instead of the original causal T-F attention), each halving the frequency resolution — a total full-band compression ratio of 16. The decoder is symmetric with transposed convolutions and skip connections, followed by sigmoid and Band Splitting (the inverse of BM) to produce $\mathbf{M}_\mathrm{c}$.

### Fine Path (Low-Frequency Detail)

Because deep compression sacrifices low-frequency modeling capacity, the fine path re-models the bands below $f_\text{low}$ at high resolution, using both magnitude and phase information with [[concepts/power-law-compression|power-law compression]] (exponent 0.7):

$$\mathbf{I}_\mathrm{f} = \mathcal{F}_\text{SFE}\left(\left[\log_{10}|\mathbf{X}^\mathrm{l}|,\ \frac{\mathbf{X}_\mathrm{r}^\mathrm{l}}{|\mathbf{X}^\mathrm{l}|^{0.7}},\ \frac{\mathbf{X}_\mathrm{i}^\mathrm{l}}{|\mathbf{X}^\mathrm{l}|^{0.7}}\right]\right)$$

where $\mathbf{X}^\mathrm{l}$ is $\mathbf{X}$ truncated at $f_\text{low}$. Only a **single** MB block with stride (1,2) is used, preserving the fine-grained resolution essential to low-frequency detail (compression ratio 2) while keeping compute manageable. The mirrored decoder outputs $\mathbf{M}_\mathrm{f}$ via sigmoid.

### Cross-Path Fusion (CPF)

[[concepts/cross-path-fusion|CPF]] enables mutual feature interaction between the two paths at their bottlenecks. The pre-bottleneck representations $\mathbf{E}_\mathrm{c}$ and $\mathbf{E}_\mathrm{f}$ are reshaped to $T \times (C_i \cdot F_i')$, concatenated into $\mathbf{E}_\text{in} \in \mathbb{R}^{T \times D}$, compressed by an FC layer into an $H$-dimensional latent space, processed by layer normalization + ELU + a (grouped) GRU for temporal modeling, expanded back to $D$ by a second FC, then split, reshaped, and combined with skip connections to yield the enhanced features $\mathbf{D}_\mathrm{c}$ and $\mathbf{D}_\mathrm{f}$ fed to each path's second Inter-RNN.

Training uses the same multi-domain loss as GTCRN.

## Experimental Setup

| Parameter | Setting |
|-----------|---------|
| Dataset | DNS3 + DiDiSpeech (Mandarin) |
| Training pairs | 72,000 noisy-clean pairs, 10 s each (200 h) |
| Validation / Test pairs | 1,000 / 1,000 |
| SNR range | −5 to 15 dB (uniform) |
| Reverberation | Random RIR; target = speech with early reverb (first 100 ms) |
| Generalization test | Official DNS Challenge 2020 test set (non-reverb + reverb) |
| Sampling rate | 16 kHz |
| STFT | 32 ms sqrt-Hanning window, 16 ms hop, 512 FFT |
| $f_\text{low}$ | 65 (= 2 kHz) |
| Coarse path | BM (192 → 64 ERB bands above 65) + 3 MB blocks; total compression ×16; kernels (3,5),(1,5),(1,5) |
| Fine path | 1 MB block, kernel (3,3), stride (1,2); compression ×2 |
| Channels | 6 (all MB blocks); Large: [6,12,14] coarse, 14 fine |
| CPF | Grouped GRU (2 groups), latent $H$ = 76 (Large: 102) |
| Inter-RNN | GRU |
| Optimizer | Adam, linear warmup (1e-6 → 1e-3 over 25k iters) + cosine annealing |
| Training | 200 epochs × 1,250 iters, batch size 8 |
| Baselines | GTCRN, LiSenNet, UL-UNAS, AdaptCRN (+ proportionally scaled-down Small variants) |
| Metrics | PESQ, ESTOI, SI-SNR, DNSMOS P.808, DNSMOS P.835 (OVRL/SIG/BAK), RTF (ONNX Runtime, Intel i5-14600KF, streaming, zero algorithmic delay) |

## Results

### DNS3 Simulated Test Set (Table I)

Level I (< 20M MACs/s) — CoFi-Lite clearly leads all scaled-down baselines:

| Model | Params (k) | MACs/s (M) | RTF | PESQ | ESTOI (×100) | SI-SNR | P.808 | OVRL | SIG | BAK |
|-------|-----------|------------|-----|------|--------------|--------|-------|------|-----|-----|
| GTCRN (Small) | 7.91 | 13.63 | 0.040 | 1.88 | 72.18 | 10.07 | 3.38 | 2.53 | 2.88 | 3.76 |
| LiSenNet (Small) | 12.46 | 15.57 | 0.031 | 1.94 | 72.74 | 10.49 | 3.36 | 2.58 | 2.93 | 3.80 |
| UL-UNAS (Small) | 56.43 | 13.63 | 0.054 | 2.05 | 74.87 | 11.16 | 3.47 | 2.60 | 2.94 | 3.81 |
| AdaptCRN (Small) | 34.98 | 12.97 | 0.047 | 2.06 | 75.15 | 11.19 | 3.50 | 2.65 | 2.99 | 3.85 |
| **CoFi-Lite** | **83.12** | **12.87** | **0.033** | **2.16** | **76.10** | **11.80** | **3.53** | **2.70** | **3.05** | **3.85** |

Level II (> 30M MACs/s) — CoFi-Lite (Large) matches AdaptCRN with 19.34% fewer MACs and one of the lowest RTFs:

| Model | Params (k) | MACs/s (M) | RTF | PESQ | ESTOI (×100) | SI-SNR | P.808 | OVRL | SIG | BAK |
|-------|-----------|------------|-----|------|--------------|--------|-------|------|-----|-----|
| GTCRN | 23.67 | 31.97 | 0.050 | 2.07 | 75.11 | 11.30 | 3.48 | 2.63 | 2.98 | 3.81 |
| LiSenNet | 36.78 | 55.77 | 0.035 | 2.17 | 76.19 | 11.74 | 3.53 | 2.69 | 3.03 | 3.85 |
| UL-UNAS | 171.33 | 34.91 | 0.066 | 2.25 | 77.69 | 12.07 | 3.55 | 2.69 | 3.01 | 3.86 |
| AdaptCRN | 134.51 | 40.80 | 0.053 | 2.30 | 78.15 | 12.35 | 3.59 | 2.75 | 3.08 | 3.88 |
| **CoFi-Lite (Large)** | **221.31** | **32.91** | **0.036** | **2.30** | **77.94** | **12.43** | 3.56 | **2.75** | **3.09** | **3.88** |

Headline comparison: CoFi-Lite (Level I, 12.87M MACs/s) **beats the full GTCRN (Level II, 31.97M MACs/s)** — PESQ +0.09, OVRL +0.07, SIG +0.07 — at 40.26% of its compute and 34% lower RTF. Note the parameter count is *higher* than GTCRN (83.12k vs. 23.67k); the authors argue this remains acceptable for edge deployment.

### DNS Challenge 2020 Test Set (Table II)

Non-intrusive metrics only (intrusive metrics excluded due to anechoic reference mismatch with the early-reverb training target). Trends match DNS3: CoFi-Lite is best in Level I (OVRL 3.15 no-reverb / 2.48 reverb), and CoFi-Lite (Large) is statistically on par with AdaptCRN in Level II (OVRL 3.19 vs. 3.20 no-reverb; 2.50 vs. 2.51 reverb).

### Ablation Study (Table III)

**Parallel paths + CPF** (matched complexity by adjusting Inter-RNN hidden size):

| ID | Config | Params (k) | MACs/s (M) | PESQ |
|----|--------|-----------|------------|------|
| 1 | Coarse path only (×16) | 19.71 | 12.37 | 1.97 |
| 2 | Fine path only (×2) | 9.24 | 12.05 | 1.53 |
| 3 | Both paths, no CPF | 21.23 | 12.24 | 2.02 |
| 4 | ID3 scaled to ID5's params | 90.80 | 13.44 | 2.06 |
| 5 | Both paths + CPF (proposed) | 83.12 | 12.87 | **2.16** |

Dual paths alone beat either single path; CPF adds +0.14 PESQ over ID3, and +0.10 over the parameter-matched ID4 — showing the two paths' features are highly complementary and their *interaction* (not just added capacity) drives the gain.

**Compression asymmetry**: increasing the fine-path ratio $R_\mathrm{f}$ from 2 → 4 → 8 steadily degrades PESQ (2.16 → 2.12 → 2.09) — deep compression destroys the low-frequency detail the fine path exists to model. Conversely, changing the coarse ratio $R_\mathrm{c}$ to 8 or 32 gives no improvement over 16 — envelope enhancement does not need fine spectral detail. This asymmetry validates the core design principle.

**Cutoff frequency**: raising $f_\text{low}$ from 17 → 33 → 65 monotonically improves PESQ (2.08 → 2.11 → 2.16), but 97 gives no further gain (2.15) — salient speech structure concentrates below 2 kHz.

## Key Contributions

1. **CoFi-Lite architecture**: decouples spectral modeling into two parallel, symmetric encoder-decoder paths — a deeply compressed coarse path (full-band magnitude envelope via ERB band merging) and a high-resolution fine path (low-frequency magnitude + compressed phase below 2 kHz) — achieving 12.87M MACs/s and 83.12k parameters
2. **Cross-Path Fusion (CPF) module**: a lightweight bottleneck fusion module (concat → FC bottleneck → grouped GRU → FC → split, with skip connections) that enables mutual feature interaction between paths, worth +0.14 PESQ in ablation
3. **Asymmetric capacity allocation principle**: coarse envelope modeling tolerates aggressive compression (×16) while fine detail modeling requires high resolution (×2); uniform downscaling is shown to fail specifically in low-frequency bands
4. **New efficiency frontier**: outperforms GTCRN at 40.26% of its MACs and 34% lower RTF; the Large variant matches SOTA AdaptCRN with 19.34% fewer MACs
5. **Systematic design studies**: ablations over path configurations, compression ratios, and cutoff frequency, identifying 2 kHz as the natural split point for salient speech structure

**Limitations / future work**: magnitude-only processing (no phase recovery) caps theoretical performance; RTF measured on a desktop CPU may not reflect real deployment on ARM Cortex-M / DSP targets — closing this measurement gap is stated future work.

## Related Concepts

- [[concepts/cofi-lite|CoFi-Lite]]
- [[concepts/cross-path-fusion|Cross-Path Fusion (CPF)]]
- [[concepts/gtcrn|Grouped Temporal Convolutional Recurrent Network (GTCRN)]]
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network (CRN)]]
- [[concepts/dprnn|Dual-Path RNN (DPRNN)]]
- [[concepts/ideal-ratio-mask|Ideal Ratio Mask (IRM)]]
- [[concepts/erb-scale|ERB Scale]]
- [[concepts/power-law-compression|Power-Law Compression]]
- [[concepts/dns-challenge|DNS Challenge]]
- [[concepts/pesq|PESQ]]

## Related Synthesis

- [[synthesis/computational-efficiency-evolution|Computational Efficiency Evolution]]
