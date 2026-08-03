---
type: concept
created: 2026-08-03
updated: 2026-08-03
sources:
  - raw/papers/jiang-2026-lightweight-speech-enhancement-ssm-dsc/full-text.md
tags:
  - speech-enhancement
  - psychoacoustics
  - erb-scale
  - computational-efficiency
  - dimensionality-reduction
---

# Auditory-Inspired Spectral Compressor (AISC)

The **Auditory-Inspired Spectral Compressor (AISC)** is a parameter-free dimensionality-reduction module introduced by Jiang, Gao, Wang, Zou & Liu (2026) for lightweight speech enhancement. It mimics the non-linear frequency resolution of the human cochlea by preserving low frequencies at full resolution while projecting high frequencies onto the [[concepts/erb-scale|ERB scale]] via a fixed triangular filter bank.

## Motivation

Speech enhancement models face a fundamental trade-off in spectral resolution:

- **Aggressive full-band compression** discards perceptually vital information, especially in speech-critical low frequencies (harmonics, formants).
- **Full-resolution processing** is computationally wasteful and ignores the non-uniform nature of the human auditory system.
- Industrial psychoacoustic models (PEAQ, PEMO) involve complex nonlinear bio-acoustic simulations that are computationally prohibitive for real-time inference.

AISC is designed as a streamlined, parameter-free compromise: it offloads the task of learning perceptual frequency resolution from the neural backbone to a fixed-parameter module.

## Mathematical Formulation

The AISC is built on the [[concepts/erb-scale|ERB scale]] conversion:

$$
\mathrm{ERB}(f) = 21.4 \log_{10}(0.00437 f + 1)
$$

$$
f(\mathrm{ERB}) = \frac{10^{\mathrm{ERB}/21.4} - 1}{0.00437}
$$

### Operation

1. **Split**: The input magnitude spectrogram $(X_m)^c \in \mathbb{R}^{B \times 1 \times F \times T}$ is partitioned along the frequency axis into:
   - **Low-frequency band** $X_{\mathrm{low}} \in \mathbb{R}^{B \times 1 \times F_L \times T}$ — frequencies below 1.5 kHz, preserved at full resolution to ensure high fidelity where human hearing is most sensitive (fundamental frequency, harmonics, formants).
   - **High-frequency band** $X_{\mathrm{high}} \in \mathbb{R}^{B \times 1 \times F_H \times T}$ — frequencies above 1.5 kHz, where human hearing perceives sounds via energy integration within critical bands rather than fine spectral resolution.

2. **Project high frequencies onto ERB scale**: A fixed, non-trainable triangular ERB filter bank matrix $W_{\mathrm{ERB}} \in \mathbb{R}^{F_{\mathrm{ERB}} \times F_H}$ (with $F_{\mathrm{ERB}} \ll F_H$) is applied:
   $$ X_{\mathrm{ERB, high}} = W_{\mathrm{ERB}} \times X_{\mathrm{high}} $$
   This projects high-frequency details onto the perceptually-relevant ERB scale, simulating frequency masking effects where the auditory system aggregates energy within critical bands.

3. **Concatenate**: The final AISC output is
   $$ X_{\mathrm{ERB}} = [X_{\mathrm{low}}, X_{\mathrm{ERB, high}}] \in \mathbb{R}^{B \times 1 \times (F_L + F_{\mathrm{ERB}}) \times T} $$
   reducing the effective frequency dimension from $F$ to $F' = F_L + F_{\mathrm{ERB}}$.

4. **Decoder inversion**: After the decoder, the process is reversed via transposed projection: $\hat{X}_{\mathrm{high}} = W_{\mathrm{ERB}}^T \times X_{\mathrm{ERB, high}}$. The differentiability of these operations enables end-to-end training with stable gradient propagation.

## Efficiency Impact

Since the computational complexity of the subsequent encoder (depthwise separable convolutions) scales linearly with the input feature size, this dimensionality reduction directly translates to a significant decrease in MACs **without increasing the neural network's parameter count**.

| Configuration | Params (M) | MACs (G) | PESQ | STOI |
|---|---|---|---|---|
| w/o AISC (full resolution) | 1.63 | 1.32 | 3.28 | 0.955 |
| AISC (500 Hz cutoff) | 1.65 | 0.34 | 2.87 | 0.937 |
| AISC (1 kHz cutoff) | 1.65 | 0.42 | 3.20 | 0.951 |
| **AISC (1.5 kHz cutoff, default)** | **1.65** | **0.50** | **3.32** | **0.956** |
| AISC (2 kHz cutoff) | 1.65 | 0.59 | 3.32 | 0.956 |

AISC delivers a **2.6× MACs reduction** (1.32 → 0.50 G) with only 0.04 PESQ loss vs. full-resolution processing. The 1.5 kHz cutoff is the sweet spot — too low (500 Hz) discards critical speech information; too high (2 kHz) gains little over full resolution.

## Relation to Prior ERB-Based Compression

AISC joins a family of ERB-based spectral compression schemes in lightweight SE, but with a distinctive design choice:

| System | ERB Application | Trainable? | Cutoff Strategy |
|---|---|---|---|
| [[concepts/gtcrn|GTCRN]] | First 65 low-freq bins + 64 ERB bands | No (fixed) | Hard split at 2 kHz |
| [[concepts/adaptcrn|AdaptCRN]] | Reuses GTCRN scheme | No (fixed) | Hard split at 2 kHz |
| [[concepts/cofi-lite|CoFi-Lite]] | Asymmetric coarse/fine path | No (fixed) | ×16 coarse / ×2 fine |
| DeepFilterNet | 32 ERB bands full-band | No (fixed) | Full ERB |
| **AISC** | 1.5 kHz split + ERB on high only | **No (fixed)** | **Perceptual split: full-res low + ERB-compressed high** |

AISC's distinctive feature is the **perceptually-motivated low/high split** — full resolution where cochlear sensitivity is highest (below 1.5 kHz) and ERB compression where the ear integrates energy within critical bands. This is similar in spirit to CoFi-Lite's asymmetric coarse/fine path decoupling but implemented as a single fixed matrix multiplication rather than a dual-path architecture.

## Related Concepts

- [[concepts/erb-scale|ERB Scale]] — psychoacoustic basis for AISC
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]] — encoder that benefits from AISC's dimensionality reduction
- [[concepts/gtcrn|GTCRN]] — origin of the ERB band-merging pattern in lightweight SE
- [[concepts/adaptcrn|AdaptCRN]] — reuses GTCRN's ERB compression
- [[concepts/cofi-lite|CoFi-Lite]] — alternative asymmetric frequency-path approach

## Related Sources

- [[sources/jiang-2026-lightweight-speech-enhancement-ssm-dsc|Jiang, Gao, Wang, Zou & Liu 2026: Lightweight SE with SSM and DSConv]] — introduces AISC
