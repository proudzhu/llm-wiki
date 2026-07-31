---
type: source
created: 2026-07-31
updated: 2026-07-31
sources:
  - raw/papers/choi-2021-trunet-real-time-speech-enhancement/full-text.md
  - https://doi.org/10.1109/ICASSP39728.2021.9414852
  - zotero://select/items/0_CZEIF8BU
tags:
  - speech-enhancement
  - lightweight-model
  - real-time
  - dereverberation
  - denoising
  - u-net
  - complex-mask
  - icassp-2021
---

# Choi, Park, Lee, Heo, Jeon & Lee 2021: Real-Time Denoising and Dereverberation with Tiny Recurrent U-Net

**Authors**: [[entities/hyeong-seok-choi|Hyeong-Seok Choi]], [[entities/sungjin-park|Sungjin Park]], [[entities/jie-hwan-lee|Jie Hwan Lee]], [[entities/hoon-heo|Hoon Heo]], [[entities/dongsuk-jeon|Dongsuk Jeon]], [[entities/kyogu-lee|Kyogu Lee]]
**Affiliations**: Department of Intelligence and Information, Artificial Intelligence Institute, Seoul National University; Supertone Inc.
**Venue**: ICASSP 2021, pp. 5771–5775
**Type**: Conference Paper
**DOI**: [10.1109/ICASSP39728.2021.9414852](https://doi.org/10.1109/ICASSP39728.2021.9414852)
**Zotero**: [CZEIF8BU](zotero://select/items/0_CZEIF8BU)

---

## Summary

**Tiny Recurrent U-Net (TRU-Net)** is a lightweight online speech enhancement architecture that decouples frequency-axis and time-axis computations in a U-Net backbone, achieving competitive performance against state-of-the-art models with orders of magnitude fewer parameters. The quantized INT8 version occupies only 362 KB, making it deployable on edge devices. Combined with a novel **phase-aware β-sigmoid mask (PHM)** that enforces a quadrilateral constraint in the complex STFT domain, TRU-Net performs single-stage simultaneous denoising and dereverberation in real time with 0 ms lookahead.

## Problem Formulation

A noisy-reverberant mixture is modeled by decomposing the room impulse response (RIR) $h$ into a direct path $h^{(d)}$ and a reflection part $h^{(r)}$:

$$
\boldsymbol{x} = \boldsymbol{h}^{(d)} \circledast \boldsymbol{y} + \boldsymbol{h}^{(r)} \circledast \boldsymbol{y} + \boldsymbol{y}^{(n)} = \boldsymbol{y}^{(d)} + \boldsymbol{y}^{(r)} + \boldsymbol{y}^{(n)}
$$

where $\boldsymbol{y}^{(d)}$, $\boldsymbol{y}^{(r)}$, and $\boldsymbol{y}^{(n)}$ denote the direct-path speech, reverberation, and additive noise, respectively. The goal is to separate the mixture $x$ into three components in the STFT domain, where $X_{t,f} \in \mathbb{C}$ and $Y_{t,f}^{(k)} \in \mathbb{C}$ for $k \in \{d, r, n\}$.

This three-way decomposition distinguishes TRU-Net from prior speech enhancement models that target only denoising ($y^{(d)}+y^{(r)}$ vs. $y^{(n)}$) — TRU-Net additionally removes late reverberation while preserving the direct-path source.

## Methodology

### TRU-Net Architecture

![[raw/papers/choi-2021-trunet-real-time-speech-enhancement/figures/3046d6709e16e3643da88822fd90e26bb43a7068ee5934aa06a7b2a13f9b5cdb.jpg|TRU-Net architecture]]

*Figure 1: Network architecture of TRU-Net. Frequency-axis 1D-CNN encoder + FGRU bottleneck + TGRU + 1D-TrCNN decoder.*

TRU-Net is a **frequency-axis U-Net** — convolution kernels do not span the time-axis, enabling causal online inference. The architecture comprises:

1. **Input feature**: Channel-wise concatenation of log-magnitude spectrogram, trainable Per-channel Energy Normalization (PCEN) spectrogram, and real/imaginary parts of the demodulated phase.
2. **Encoder**: Six 1D-CNN blocks (pointwise + depthwise convolution, MobileNet-style) downsampling the frequency axis from 256 to 16. Configuration: `EncoderConfig = {1st: (5,2,64), 2nd: (3,1,128), 3rd: (5,2,128), 4th: (3,1,128), 5th: (5,2,128), 6th: (3,2,128)}`.
3. **FGRU block**: A **bidirectional GRU along the frequency axis** (64 hidden units per direction) followed by pointwise convolution, batch normalization, and ReLU. The FGRU enlarges the receptive field (1,750 Hz) without stacking more 1D-CNN blocks.
4. **TGRU block**: A **unidirectional GRU along the time axis** (128 hidden units, shared across frequency indices) followed by pointwise convolution, BN, and ReLU — aggregating temporal context causally.
5. **Decoder**: Six 1D-TrCNN blocks mirroring the encoder. Each block concatenates the previous output with a skip tensor from the encoder, projects to a smaller channel size ($256 \to 64$) via pointwise convolution, then applies 1D transposed convolution. Configuration: `DecoderConfig = {1st: (3,2,128), 2nd: (5,2,64), 3rd: (3,1,64), 4th: (5,2,64), 5th: (3,1,64), 6th: (5,2,10)}`.

**Key design choice**: Depthwise convolution is used in the encoder but **not** in the decoder — the authors empirically observed it significantly drops performance when used in the decoding stage.

Total parameter count: **0.38 M** (FP32 = 1.45 MB; INT8 quantized = 0.36 MB / 362 KB).

### Phase-aware β-sigmoid Mask (PHM)

The proposed **PHM** is a complex-valued mask that guarantees the mixture equals the sum of the estimated target source and the remaining components: $X_{t,f} = Y_{t,f}^{(k)} + Y_{t,f}^{(\neg k)}$, where $k \in \{d, r, n\}$.

**Step 1 — Magnitude mask with flexible range**: The network outputs two magnitude masks via a sigmoid scaled by a learnable $\beta_{t,f}$:

$$
|M_{t,f}^{(k)}| = \beta_{t,f} \cdot \sigma^{(k)}(z_{t,f}) = \beta_{t,f} \cdot \left(1 + e^{-(z_{t,f}^{(k)} - z_{t,f}^{(\neg k)})}\right)^{-1}
$$

where $\beta_{t,f} = 1 + \text{softplus}((\psi_\beta(\phi))_{t,f})$ extends the magnitude range beyond $[0, 1]$. The $\beta$ coefficient is designed so the masks satisfy the triangle inequalities required for a valid phase reconstruction.

**Step 2 — Phase mask via law of cosines**: Given the three magnitudes as triangle sides, the cosine of the absolute phase difference $\Delta\theta_{t,f}^{(k)}$ between the mixture and source $k$ is:

$$
\cos(\Delta\theta_{t,f}^{(k)}) = \frac{1 + |M_{t,f}^{(k)}|^2 - |M_{t,f}^{(\neg k)}|^2}{2|M_{t,f}^{(k)}|}
$$

The rotational direction $\xi_{t,f} \in \{1, -1\}$ is estimated via a two-class straight-through Gumbel-softmax, yielding the phase mask $e^{j\theta_{t,f}^{(k)}} = \cos(\Delta\theta_{t,f}^{(k)}) + j\xi_{t,f}\sin(\Delta\theta_{t,f}^{(k)})$. The final complex mask is $M_{t,f}^{(k)} = |M_{t,f}^{(k)}| \cdot e^{j\theta_{t,f}^{(k)}}$, applied as $\hat{Y}_{t,f}^{(k)} = M_{t,f}^{(k)} \cdot X_{t,f}$.

### Quadrilateral Masking for Joint Denoising + Dereverberation

![[raw/papers/choi-2021-trunet-real-time-speech-enhancement/figures/4ec22ea430998abf9d5c7c809b19a420fb56ad94b751cefc89074b859c87b138.jpg|PHM quadrilateral illustration]]

*Figure 2: Quadrilateral masking. Two pairs of PHMs separate the mixture into {direct, rest} and {noise, reverberant source}. The fourth side (reverberation) is uniquely determined by the other three.*

To extract both the direct source and reverberation, **two pairs of PHMs** are produced simultaneously:
- Pair 1: $M_{t,f}^{(d)}$ and $M_{t,f}^{(\neg d)}$ separate the mixture into direct source vs. the rest.
- Pair 2: $M_{t,f}^{(n)}$ and $M_{t,f}^{(\neg n)}$ separate the mixture into noise vs. reverberant source.

Since each PHM pair forms a triangle in the complex STFT domain, the two triangles together form a **quadrilateral** whose fourth side $M_{t,f}^{(r)}$ (reverberation) is uniquely determined by the three other sides and the two side angles. This geometric construction enables single-stage joint denoising and dereverberation.

### Multi-Scale Objective

Combines waveform-domain cosine similarity (proxy for SDR) and spectral-domain L2 with power-law compression (exponent 0.3, replacing the log transformation):

$$
\mathcal{L}_{wav}^{(k)} = \sum_j \frac{1}{M_j} \sum_{i=1}^{M_j} C\left(\boldsymbol{y}_{[g_j(i-1):g_j i]}^{(k)}, \hat{\boldsymbol{y}}_{[g_j(i-1):g_j i]}^{(k)}\right)
$$

with segment lengths $g_j \in \{4064, 2032, 1016, 508\}$ samples, and

$$
\mathcal{L}_{spec}^{(k)} = \sum_i \left\| \left|\text{STFT}_i(\boldsymbol{y}^{(k)})\right|^{0.3} - \left|\text{STFT}_i(\hat{\boldsymbol{y}}^{(k)})\right|^{0.3} \right\|^2
$$

with FFT sizes $\{1024, 512, 256\}$ at 75% overlap. The final loss is $\mathcal{L}_\text{final} = \sum_{k \in \{d, r, n\}} \mathcal{L}_{wav}^{(k)} + \mathcal{L}_{spec}^{(k)}$.

### INT8 Quantization

Uniform symmetric quantization (zero-point restricted to 0) applied to all layers with full-precision biases. Activation scales for encoder/decoder layers are fixed at the average of training-time observed min/max; GRU layers are dynamically quantized at inference time due to the large dynamic range of internal activations.

## Experimental Setup

| Component | Setting |
|-----------|---------|
| **Sampling rate / STFT** | 16 kHz; window 512 (32 ms), hop 128 (8 ms) |
| **Training data** | pyroomacoustics-simulated reverberation with random absorption, room size, source/mic position; 2 s segments; SNR uniform in $[-5, 25]$ dB |
| **Test sets** | CHiME2 (ablation), DNS Challenge synthetic dev sets (denoising), WHAMR! min subset (dereverberation), DNS Challenge blind test (listening test) |
| **Optimizer** | AdamW, initial LR $4 \times 10^{-4}$, halved on 3-epoch validation plateau |
| **Input features** | Log-magnitude + PCEN + real/imag of demodulated phase |
| **Quantization** | INT8 uniform symmetric; weights/activations/inputs quantized, biases FP32, masking & feature extraction FP32 |
| **Metrics** | PESQ (P.862.1 and P.862.2), CBAK, COVL, CSIG, SI-SDR, STOI, ITU-T P.808 MOS |
| **Compute targets** | Single-frame RTF on 2.7 GHz Intel i5-5257U and 2.6 GHz i7-6700HQ; 0 ms lookahead |

## Results

### Denoising on DNS Challenge (Table 1)

| Method | Size (M / MB) | RT | PESQ1 (no reverb / reverb) | PESQ2 (no reverb / reverb) | SI-SDR (no reverb / reverb) | STOI (no reverb / reverb) |
|--------|--------------:|:--:|---------------------------:|---------------------------:|----------------------------:|--------------------------:|
| Noisy | — / — | — | 2.45 / 2.75 | 1.58 / 1.82 | 9.07 / 9.03 | 91.52 / 86.62 |
| NSnet (1.27 M) | 1.27 / 4.84 | ✓ | 2.68 / 2.45 | 1.81 / 1.52 | 12.47 / 9.18 | 90.56 / 82.15 |
| [[concepts/dtln\|DTLN]] (0.99 M) | 0.99 / 3.78 | ✓ | 3.04 / 2.70 | — / — | 16.34 / 10.53 | 94.76 / 84.68 |
| ConvTasNet (5.08 M) | 5.08 / 19.38 | ✘ | — / — | 2.73 / 2.71 | — / — | — / — |
| PoCoNet1 (50 M) | 50 / 190.73 | ✘ | — / — | 2.71 / 2.83 | — / — | — / — |
| PoCoNet2 (50 M) | 50 / 190.73 | ✘ | — / — | 2.75 / — | — / — | — / — |
| DCCRN-E (3.7 M) | 3.7 / 14.11 | ✓ | 3.27 / 3.08 | — / — | — / — | — / — |
| DCCRN-CL (3.7 M) | 3.7 / 14.11 | ✘ | 3.26 / 3.10 | — / — | — / — | — / — |
| **TRU-Net (FP32)** | **0.38 / 1.45** | **✓** | **3.36 / 3.35** | **2.86 / 2.74** | **17.55 / 14.87** | **96.32 / 91.29** |
| **TRU-Net (INT8)** | **0.38 / 0.36** | **✓** | **3.35 / 3.31** | **2.84 / 2.70** | **17.23 / 14.47** | **96.12 / 91.01** |

TRU-Net achieves the best PESQ1 on the Synthetic without Reverb set and remains competitive (within 0.01–0.09 PESQ1) on the Synthetic with Reverb set, while using **~8× fewer parameters than DCCRN and ~130× fewer than PoCoNet**.

### Ablation on CHiME2 (Table 2, average SDR across SNRs −6 to 9 dB)

| Variant | Description | Size (M) | Avg. SDR (dB) |
|---------|-------------|---------:|--------------:|
| TRU-Net-A | Full proposed | 0.38 | **15.73** |
| TRU-Net-B | − multi-scale objective | 0.38 | 15.56 |
| TRU-Net-C | − PCEN feature | 0.38 | 15.42 |
| TRU-Net-D | − FGRU block | 0.31 | 15.28 |
| TLSTM (FP32, [24]) | baseline | 0.97 | 13.70 |
| PTLSTM (INT8, [24]) | baseline | 0.33 | 13.18 |
| Wilson et al. [16] | large baseline | 65 | 15.37 |

All three components (PCEN, multi-scale objective, FGRU) contribute positively; the **FGRU block contributes the most** (−0.45 dB SDR when removed). TRU-Net-A outperforms the 65 M-parameter Wilson et al. baseline with 170× fewer parameters.

### Simultaneous Denoising + Dereverberation on WHAMR! (Table 3)

| Method | Size (M / MB) | PESQ1 | SI-SDR | STOI |
|--------|--------------:|------:|-------:|-----:|
| Noisy | — / — | 1.83 | −2.73 | 73.00 |
| NSnet [17] | 1.27 / 4.84 | 1.91 | 0.34 | 73.02 |
| [[concepts/dtln\|DTLN]] [18] | 0.99 / 3.78 | 2.23 | 2.12 | 80.40 |
| **TRU-Net (FP32)** | **0.38 / 1.45** | **2.51** | **3.51** | **81.22** |
| **TRU-Net (INT8)** | **0.38 / 0.36** | **2.49** | **3.03** | **80.56** |

TRU-Net achieves the best results across all metrics, demonstrating parameter efficiency for simultaneous denoising and dereverberation.

### Listening Test (Table 4, ITU-T P.808 MOS on DNS Challenge blind test)

| Method | Size (M / MB) | Singing | Tonal | Non-English | English | Emotional | Overall |
|--------|--------------:|--------:|------:|------------:|--------:|----------:|--------:|
| Noisy | — / — | 2.96 | 3.00 | 2.96 | 2.80 | 2.67 | 2.86 |
| NSnet2 [30] | 2.8 / 10.68 | 3.10 | 3.25 | 3.28 | 3.30 | 2.88 | 3.21 |
| **TRU-Net** | **0.38 / 1.45** | **3.08** | **3.38** | **3.43** | **3.41** | **2.88** | **3.32** |

TRU-Net wins the overall MOS (3.32 vs 3.21 for NSnet2) with ~7× fewer parameters, and was submitted to the 2021 ICASSP DNS Challenge Track 1. Average single-frame compute time: **1.97 ms** on i5-5257U and **1.3 ms** on i7-6700HQ (including FFT, iFFT, and DRC).

## Key Contributions

1. **TRU-Net architecture**: A frequency-axis U-Net with 1D-CNN encoder, FGRU bottleneck (bidirectional frequency-axis GRU), TGRU decoder (unidirectional time-axis GRU), and 1D-TrCNN decoder — decoupling frequency and time computations for causal online inference at 0.38 M parameters.
2. **Phase-aware β-sigmoid mask (PHM)**: A complex-valued mask enforcing the triangle inequality between mixture, target, and rest via a learnable $\beta$ coefficient (softplus-activated) and law-of-cosines phase reconstruction with straight-through Gumbel-softmax rotational direction.
3. **Quadrilateral masking**: A geometric construction using two PHM pairs to enable single-stage simultaneous denoising and dereverberation — the reverberation mask is uniquely determined by the other three sides of the quadrilateral.
4. **INT8 quantization with minimal quality loss**: Quantized model (362 KB) loses only 0.01–0.04 PESQ1 and 0.32–0.40 dB SI-SDR vs FP32, demonstrating deployability on embedded devices.
5. **Empirical finding on depthwise convolution**: Depthwise convolution helps in the encoder but significantly degrades performance in the decoder — a design recommendation for future lightweight U-Net speech enhancers.

## Related Concepts

- [[concepts/trunet|Tiny Recurrent U-Net (TRU-Net)]]
- [[concepts/phase-aware-beta-sigmoid-mask|Phase-aware β-sigmoid Mask (PHM)]]
- [[concepts/dereverberation|Dereverberation]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/dtln|Dual-signal Transformation LSTM Network (DTLN)]]
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask (cRM)]]
- [[concepts/power-law-compression|Power-law Compression]]
- [[concepts/gated-recurrent-unit|Gated Recurrent Unit (GRU)]]
- [[concepts/quantization-aware-training|Quantization-aware Training]]
- [[concepts/dns-challenge|DNS Challenge]]
- [[concepts/room-impulse-response|Room Impulse Response]]

## Related Synthesis

- [[synthesis/joint-multitask-ultra-low-latency-se|Joint Multi-Task Speech Enhancement & Ultra-Low-Latency Realtime Paradigm]] — TRU-Net is an early (2021) precursor to the 2023–2026 multi-task SE trend, performing joint denoising + dereverberation within a single backbone at sub-2 ms single-frame latency.
