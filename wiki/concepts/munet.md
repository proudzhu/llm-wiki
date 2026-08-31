---
type: concept
created: 2026-08-31
updated: 2026-08-31
sources:
  - raw/papers/shetu-2026-munet/full-text.md
tags:
  - neural-network
  - speech-enhancement
  - noise-suppression
  - low-complexity
  - low-latency
  - embedded-dsp
  - quantization
---

# μNet

**μNet** (Shetu et al., 2026) is an ultra-low-memory, low-complexity, low-latency end-to-end DNN for speech enhancement targeting embedded digital signal processors. It requires only **46 K parameters, 28 MMACs, and 90 KB of static memory**, supports algorithmic latencies down to **4 ms** via an asymmetric analysis–synthesis window pair, quantizes fully to **int8**, and runs in real-time on a Cadence Tensilica HiFi 4 DSP (NXP RT685) at 70 MHz. It extends the [[concepts/ulcnet|ULCNet]] two-stage backbone (magnitude-mask stage + [[concepts/complex-ratio-mask|complex ratio mask]] stage) with [[concepts/power-law-compression|power-law compressed]] magnitude/phase inputs, a hybrid feature reorientation, shared subband GRU, and a shared linear projection.

## Architecture

Two-stage backbone (stage 1: magnitude mask $\widetilde{\mathbf{M}}_{\mathrm{m}}$; stage 2: CRM refinement):

1. **Input preprocessing**: PF-compressed ($\alpha=0.3$) magnitude + phase from the STFT (sqrt-Hann 32 ms analysis window, shorter Hann synthesis window)
2. **Hybrid feature reorientation**: [[concepts/channel-wise-feature-reorientation|C-SubFR]] (2 subbands × 43 bins) combined with sampling-based C-SamFR (factor 6 → 6 sub-sampled sets of 43 bins), giving $\mathbb{R}^{B\times T\times 43\times 8}$
3. **Conv block**: 4 layers, 32 filters, kernel (1,3); frequency downsampling ×2 in the last 3 layers; BN + ReLU — **standard convolutions instead of depthwise separable** for better hardware utilization and quantization support on DSPs
4. **Pointwise conv** (24 filters) → flatten → 144-dim
5. **Shared subband GRU**: 2 subbands processed by one weight-shared GRU (64 hidden units) → 128-dim latent $\mathbf{h}$
6. **Shared linear projection**: $\mathbf{h}$ split into 4 overlapping segments (length 40: [0,40], [24,64], [56,96], [88,128]); each passed through the *same* linear layer + sigmoid; concatenated → $\widetilde{\mathbf{M}}_{\mathrm{m}}\in\mathbb{R}^{256}$
7. **Stage-2 CNN**: 2 conv layers (32 filters) + pointwise conv (8 channels) on $[M_m\cos(X_p),\,M_m\sin(X_p)]$ → CRM-multiplication + power-law decompression

For the full flow diagram, see [[sources/shetu-2026-munet#Model-Structure,-Inputs,-and-Outputs|the source page]].

## Computational Profile

| Metric | Value |
|--------|-------|
| Parameters | 46 K |
| Complexity | 28 MMACs |
| Static memory | 90 KB |
| Latency | 4–16 ms (configurable) |
| Quantization | int8 (TFLite post-training) |
| Platform | Cadence Tensilica HiFi 4 (NXP RT685, 70 MHz); also compatible with ARM Cortex M, ADI SHARC, Qualcomm Hexagon, HiFi 5, Airoha AB159x neural accelerator |

## Performance (DNS non-reverb test set)

- **Best BAK 4.03** (μNet MSE variant) — most aggressive noise suppression in comparison
- **Best PESQ 2.27** with [[concepts/noise-attenuation-control|noise attenuation control]] at −30 dB
- **Highest MUSHRA 77.78** vs. GTCRN 74.24 (float32, 16 ms latency)
- At 16 ms latency, int8 quantization has no adverse effect; at 4 ms, int8 ΔSI-SDR degrades to 0.50 dB (attributed to GRU state drift from more frequent updates)

## Design Rationale

| Choice | Reason |
|--------|--------|
| Standard convs over depthwise separable | Depthwise separable convs fragment memory access on DSPs → poor hardware utilization; standard convs quantize cleanly |
| Shared subband GRU | Learns common temporal dynamics across subbands; large parameter savings |
| Shared linear projection with overlapping segments | Parameter sharing while ensuring spectral consistency during upsampling |
| Asymmetric window pair | Analysis window (32 ms) decoupled from synthesis window; latency governed by the shorter synthesis window |

## Relation to ULCNet Family

- Inherits the two-stage backbone, power-law compression, and channel-wise feature reorientation from [[concepts/ulcnet|ULCNet]] (Shetu et al., ICASSP 2024)
- [[concepts/fast-ulcnet|Fast-ULCNet]] (Larraza & de Koeijer 2026) is a parallel descendant that replaces GRUs with FastGRNN on embedded ARM targets; μNet instead targets integer DSPs and neural accelerators, and trades depthwise separable convs back for standard convolutions

## Related Concepts

- [[concepts/ulcnet|ULCNet]]
- [[concepts/fast-ulcnet|Fast-ULCNet]]
- [[concepts/channel-wise-feature-reorientation|Channel-Wise Feature Reorientation]]
- [[concepts/power-law-compression|Power-Law Compression]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask (cRM)]]
- [[concepts/noise-attenuation-control|Noise Attenuation Control]]
- [[concepts/gated-recurrent-unit|Gated Recurrent Unit (GRU)]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/gtcrn|GTCRN]]

## Related Sources

- [[sources/shetu-2026-munet|Shetu et al. 2026: μNet]]
- [[sources/rong-2024-gtcrn-speech-enhancement-ultralow|Rong et al. 2024: GTCRN]] — main baseline
