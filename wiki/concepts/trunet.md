---
type: concept
created: 2026-07-31
updated: 2026-07-31
sources:
  - raw/papers/choi-2021-trunet-real-time-speech-enhancement/full-text.md
tags:
  - neural-network
  - speech-enhancement
  - lightweight-model
  - real-time
  - u-net
  - recurrent-neural-network
---

# Tiny Recurrent U-Net (TRU-Net)

**TRU-Net** (Tiny Recurrent U-Net) is a lightweight online speech enhancement architecture proposed by Choi et al. (ICASSP 2021). It is a **frequency-axis U-Net** that decouples frequency-axis and time-axis computations, enabling causal online inference with only 0.38 M parameters (362 KB when INT8-quantized). Combined with the [[concepts/phase-aware-beta-sigmoid-mask|phase-aware β-sigmoid mask (PHM)]], TRU-Net performs single-stage simultaneous denoising and dereverberation at sub-2 ms single-frame latency.

## Motivation

Conventional U-Net speech enhancers apply 2D convolution kernels across both frequency and time axes. This non-causal structure (a) prevents online inference because future frames are needed to process the current frame, and (b) introduces redundant computation between adjacent frames in both the encoder and decoder paths. TRU-Net addresses both issues by removing the time-axis from convolution kernels and instead using a recurrent layer to aggregate temporal context causally.

## Architecture

![[raw/papers/choi-2021-trunet-real-time-speech-enhancement/figures/3046d6709e16e3643da88822fd90e26bb43a7068ee5934aa06a7b2a13f9b5cdb.jpg|TRU-Net architecture]]

*Figure 1: TRU-Net architecture — 1D-CNN encoder, FGRU bottleneck, TGRU, 1D-TrCNN decoder.*

### Encoder

Six 1D-CNN blocks (MobileNet-style pointwise + depthwise convolution) downsample the frequency axis from 256 to 16:

- `EncoderConfig = {(5,2,64), (3,1,128), (5,2,128), (3,1,128), (5,2,128), (3,2,128)}` (kernel, stride, output channels)
- The first layer uses standard convolution without a preceding pointwise convolution.
- Each block is followed by batch normalization and ReLU.

### FGRU Block (Frequency-axis Gated Recurrent Unit)

A **bidirectional GRU along the frequency axis** (64 hidden units per direction) followed by pointwise convolution + BN + ReLU. The FGRU enlarges the receptive field (1,750 Hz) without stacking more 1D-CNN blocks — ablation shows it is the single most impactful component (−0.45 dB SDR on CHiME2 when removed).

### TGRU Block (Time-axis Gated Recurrent Unit)

A **unidirectional GRU along the time axis** (128 hidden units, shared across all frequency-axis indices to save parameters) followed by pointwise convolution + BN + ReLU. The TGRU aggregates temporal context causally — this is the only component that crosses the time axis, and it does so in a strictly online manner.

### Decoder

Six 1D Transposed CNN (1D-TrCNN) blocks mirror the encoder. Each block:
1. Concatenates the previous layer output with a skip tensor from the encoder.
2. Projects to a smaller channel size ($256 \to 64$) via pointwise convolution.
3. Applies 1D transposed convolution to upsample.

`DecoderConfig = {(3,2,128), (5,2,64), (3,1,64), (5,2,64), (3,1,64), (5,2,10)}`

**Key design choice**: Depthwise convolution is used in the encoder but **not** in the decoder — the authors empirically observed it significantly drops performance when used in the decoding stage.

## Input Features

Channel-wise concatenation of:
- Log-magnitude spectrogram
- Trainable Per-channel Energy Normalization (PCEN) spectrogram (combines dynamic range compression + automatic gain control; suitable for online inference as PCEN's temporal integration is a first-order IIR filter depending only on the previous frame)
- Real and imaginary parts of the demodulated phase

## Quantization

INT8 uniform symmetric quantization (zero-point restricted to 0) applied to all weights, activations, and inputs in convolutional and GRU layers. Biases remain in full precision. Activation scales for encoder/decoder layers are fixed at training-time observed averages; GRU layers use dynamic quantization at inference due to the large dynamic range of internal activations.

| Variant | Size | PESQ1 (DNS, no reverb) | SI-SDR (DNS, no reverb) |
|---------|------|------------------------:|------------------------:|
| FP32 | 1.45 MB | 3.36 | 17.55 |
| INT8 | 0.36 MB (362 KB) | 3.35 | 17.23 |

Quantization costs only ~0.01 PESQ1 and ~0.32 dB SI-SDR.

## Results

| Test set | Metric | TRU-Net (FP32) | TRU-Net (INT8) | Notable baseline |
|----------|--------|---------------:|---------------:|------------------|
| DNS (no reverb) | PESQ1 | **3.36** | 3.35 | DCCRN-E 3.27 (3.7 M) |
| DNS (with reverb) | PESQ1 | **3.35** | 3.31 | DCCRN-CL 3.10 (3.7 M) |
| CHiME2 (avg SDR) | SDR | **15.73 dB** | 15.68 | Wilson et al. 15.37 (65 M) |
| WHAMR! | PESQ1 | **2.51** | 2.49 | DTLN 2.23 (0.99 M) |
| DNS blind (MOS) | P.808 | **3.32** | — | NSnet2 3.21 (2.8 M) |

Single-frame compute: **1.97 ms** on 2.7 GHz Intel i5-5257U, **1.3 ms** on 2.6 GHz Intel i7-6700HQ (including FFT, iFFT, and DRC), with 0 ms lookahead.

## Relation to Prior Work

- **DCU-Net** (Choi et al. 2019, [2] in the paper): The same group's earlier phase-aware speech enhancer; TRU-Net is its lightweight, real-time counterpart.
- **Grzywalski & Drgas 2019** ([32]): Used bidirectional LSTM on frequency and time axes with a 2D-CNN U-Net. TRU-Net differs by using FGRU + unidirectional TGRU to handle online inference combined with a lightweight 1D-CNN (frequency-axis) U-Net.
- **TinyLSTM** (Fedorov et al. 2020, [24]): A contemporaneous lightweight speech enhancer for hearing aids; TRU-Net matches or exceeds its SDR with fewer parameters.

## Legacy

TRU-Net is an early (2021) example of the joint multi-task speech enhancement paradigm — performing denoising and dereverberation in a single neural backbone at sub-2 ms latency. It is frequently cited as a baseline in subsequent lightweight speech enhancement literature (e.g., [[sources/rong-2024-gtcrn-speech-enhancement-ultralow|GTCRN]], [[sources/larraza-2026-fast-ulcnet-speech-enhancement|Fast-ULCNet]]). Its design pattern — frequency-axis U-Net with recurrent temporal mixing — anticipates the 2023–2026 trend toward streaming-friendly SE backbones covered in [[synthesis/joint-multitask-ultra-low-latency-se|Joint Multi-Task Speech Enhancement & Ultra-Low-Latency Realtime Paradigm]].

## Related Concepts

- [[concepts/phase-aware-beta-sigmoid-mask|Phase-aware β-sigmoid Mask (PHM)]]
- [[concepts/dereverberation|Dereverberation]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]]
- [[concepts/gated-recurrent-unit|Gated Recurrent Unit (GRU)]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask (cRM)]]
- [[concepts/power-law-compression|Power-law Compression]]
- [[concepts/quantization-aware-training|Quantization-aware Training]]
- [[concepts/dns-challenge|DNS Challenge]]

## Related Sources

- [[sources/choi-2021-trunet-real-time-speech-enhancement|Choi et al. 2021: Real-Time Denoising and Dereverberation with Tiny Recurrent U-Net]]
