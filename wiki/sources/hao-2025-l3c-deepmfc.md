---
type: source
created: 2026-07-01
updated: 2026-07-01
sources:
  - raw/papers/hao-2025-l3c-deepmfc/full-text.md
  - https://www.isca-archive.org/interspeech_2025/hao25_interspeech.pdf
  - zotero://select/items/0_FDVXMTIJ
tags:
  - hearing-aids
  - feedback-cancellation
  - deep-learning
  - low-latency
  - complex-spectrum-mapping
---

# Hao, Moore, Zhang, Li & Zheng 2025: L3C-DeepMFC for Hearing Aid Feedback Cancellation

| Field | Value |
|:------|:------|
| **Authors** | [[entities/fengyuan-hao\|Fengyuan Hao]], [[entities/brian-c-j-moore\|Brian C. J. Moore]], [[entities/huiyong-zhang\|Huiyong Zhang]], [[entities/xiaodong-li\|Xiaodong Li]], [[entities/chengshi-zheng\|Chengshi Zheng]] |
| **Institution** | Institute of Acoustics, Chinese Academy of Sciences; University of Cambridge |
| **Venue** | Interspeech 2025 |
| **Year** | 2025 |
| **Type** | Conference paper |
| **URL** | [ISCA Archive](https://www.isca-archive.org/interspeech_2025/hao25_interspeech.pdf) |
| **Zotero** | [FDVXMTIJ](zotero://select/items/0_FDVXMTIJ) |

## Summary

Proposes **L3C-DeepMFC** (Low-Latency Low-Complexity Deep Marginal Feedback Cancellation), a T-F domain method for hearing aid feedback control that employs [[concepts/complex-spectrum-mapping|complex spectrum mapping]] with gain-shape representation to estimate magnitude and phase of feedback-free speech. Achieves 4 ms algorithmic latency with only 0.31M parameters and 0.43 G/s MACs through full- and sub-band recurrent modeling and a modified overlap-add method. Closed-loop fine tuning addresses the training-estimation mismatch inherent in [[concepts/deep-marginal-feedback-cancellation|DeepMFC]].

## Problem Formulation

The microphone signal in a hearing aid with acoustic feedback:

$$y[t] = v[t] + u[t] * f[t] + n[t]$$

where $v[t]$ is desired speech, $f[t]$ is the feedback path, $u[t]$ is the amplified receiver signal, and $n[t]$ is environmental noise. The hearing aid amplification: $g[t] = G \cdot \delta(t - \Delta t)$ where $G$ is gain and $\Delta t$ is system delay. The target signal is $s[t] = G \cdot v[t - \Delta t]$.

## Methodology

### Complex Spectrum Mapping with Gain-Shape Representation

Unlike DeepMFC which uses parallel RI decoders, L3C-DeepMFC decouples magnitude and phase:

$$(\cos\angle\hat{S},\; \sin\angle\hat{S},\; \log|\hat{S}|) = \mathcal{G}(\cos\angle U,\; \sin\angle U,\; \log|U|;\; \Phi)$$

This gain-shape representation covers a broader dynamic range than RI components alone.

### Architecture: Full- and Sub-Band Recurrent Modeling

Three components:
1. **Speech Encoder**: Linear layer → PReLU → instant layer normalization → $D$-dimensional features per T-F unit
2. **Full- and Sub-Band Recurrent Module** ($I$ layers):
   - **Sub-band LSTM**: Shared across frequency groups of size $L$, captures temporal dependencies within each sub-band
   - **Full-band GLSTM**: Group-LSTM on frame-level features for global spectral context
3. **Speech Decoder**: Linear layer reconstructing T-F domain output

### Low-Latency Overlap-Add Method

Modified OLA using tapered analysis window $w_a[t]$ and synthesis using only current + next frames:

$$\hat{s}[M + (k-1)N + t] = w_s^{(1)}[t] \cdot \hat{s}_w[t + M - N, k] + w_s^{(2)}[t] \cdot \hat{s}_w[t + M - 2N, k+1]$$

Algorithmic latency = $2N$ (twice the frame shift). With $N = 2$ ms → **4 ms total latency**.

### Closed-Loop Fine Tuning

Addresses two discrepancies between open-loop training and closed-loop estimation:
1. Frame buffer updates during overlap-add in closed loop
2. Feedback concealment eliminates acoustic coupling during estimation

Fine tuning uses dynamically generated feedback mixtures in a simulated hearing aid system, leading to noticeable MSG improvement.

### Loss Function

Combined magnitude + RI loss with Hanning window for compressed spectra:

$$\mathcal{L}^{\text{Mag+RI}} = 0.5 \cdot \mathcal{L}^{\text{Mag}}(\hat{S}', S) + 0.5 \cdot \mathcal{L}^{\text{RI}}(\hat{S}', S)$$

## Experimental Setup

| Parameter | Value |
|:----------|:------|
| Dataset | AISHELL-3 (Mandarin speech) + DNS Challenge noises |
| Sampling rate | 24 kHz |
| Window size $M$ | 20 ms (480 samples) |
| Hop size $N$ | 2 ms |
| FFT size | 480 |
| Algorithmic latency | 4 ms |
| Model depth $I$ | 3 layers |
| Feature dim $D$ | 8 |
| Sub-band dim $C$ | 8 |
| Group size $L$ | 4 |
| LSTM hidden $H$ | 16 |
| GLSTM hidden | 128 (group size 2) |
| Parameters | 0.31M |
| MACs | 0.43 G/s |
| RTF | 0.623 |
| Buffer size | 25.9 KB |
| Optimiser | AdamW, lr=0.001, 50 epochs |
| Training SNRs | 5–20 dB |
| Evaluation | 150 mixtures, no background noise |

## Results

### Quantitative Comparison (Set A, AISHELL-3)

| Method | Latency | Params | MACs | WB-PESQ (GM=0) | HASQI-V2 (GM=0) |
|:-------|:--------|:-------|:-----|:----------------|:-----------------|
| DeepMFC | 10 ms | 9.83M | 4.83 G/s | 3.15 | 0.795 |
| DeepMFC (4ms, tapered) | 4 ms | 9.83M | 12.04 G/s | 1.93 | 0.552 |
| DeepMFC (4ms, Hanning) | 4 ms | 9.83M | 12.04 G/s | 4.34 | 0.947 |
| **L3C-DeepMFC** | **4 ms** | **0.31M** | **0.43 G/s** | **4.08** | **0.913** |
| AFC+L3C-DeepMFC | 4 ms | — | — | 4.04 | 0.894 |

### Key Findings

1. **Hanning window in loss** is critical: tapered window causes severe spectral leakage → speech distortion
2. **Closed-loop fine tuning** recovers performance gap vs. full DeepMFC while maintaining low complexity
3. **AFC integration** further improves feedback suppression at negative gain margins
4. **Exponential complexity increase** when reducing frame shift for full-convolutional DeepMFC (4.83→12.04 G/s)
5. L3C-DeepMFC achieves **comparable performance** to DeepMFC at **32× fewer parameters** and **11× fewer MACs**

## Key Contributions

1. **Low-latency low-complexity architecture**: Full- and sub-band recurrent modeling reduces complexity from 9.83M/4.83 G/s to 0.31M/0.43 G/s
2. **Modified overlap-add**: 4 ms algorithmic latency using tapered window + 2-frame synthesis
3. **Closed-loop fine tuning**: Dynamic feedback mixture generation addresses training-estimation mismatch
4. **Gain-shape complex spectrum mapping**: Decoupled magnitude/phase estimation with broader dynamic range

## Important Distinctions

- **vs. [[concepts/deep-marginal-feedback-cancellation\|DeepMFC]]**: L3C-DeepMFC uses band-split recurrent modeling (vs. fully convolutional), gain-shape representation (vs. parallel RI decoders), and closed-loop fine tuning (vs. open-loop only)
- **vs. [[concepts/hearing-aid-feedback-cancellation\|AFC methods]]**: L3C-DeepMFC treats feedback cancellation as interference suppression rather than adaptive filter estimation; maintains stability at high gains where AFC struggles
- **vs. [[sources/pandey-2019-cnn-speech-enhancement-time-domain\|AECNN]]**: Both use complex spectrum mapping, but L3C-DeepMFC operates in T-F domain with gain-shape representation while AECNN operates in time domain

## Related Concepts

- [[concepts/deep-marginal-feedback-cancellation|Deep Marginal Feedback Cancellation]]
- [[concepts/hearing-aid-feedback-cancellation|Hearing Aid Feedback Cancellation]]
- [[concepts/acoustic-feedback|Acoustic Feedback]]
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[concepts/closed-loop-fine-tuning|Closed-Loop Fine Tuning]]
- [[concepts/maximum-stable-gain|Maximum Stable Gain]]

## Related Sources

- [[sources/zhan-2025-deeppem-afc|Zhan 2025: DeepPEM-AFC]]
- [[sources/pandey-2019-cnn-speech-enhancement-time-domain|Pandey & Wang 2019: CNN-Based Speech Enhancement in the Time Domain]]
