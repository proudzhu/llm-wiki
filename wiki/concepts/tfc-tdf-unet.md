---
type: concept
created: 2026-09-15
updated: 2026-09-15
sources:
  - raw/papers/kim-2021-kuielab-mdx-net/full-text.md
tags:
  - neural-networks
  - music-source-separation
  - u-net
---

# TFC-TDF U-Net

The TFC-TDF U-Net is a spectrogram-domain neural architecture for music source separation, introduced by Choi et al. (ISMIR 2020). Its name comes from its two complementary block types: TFC (Time-Frequency Convolution) blocks, which aggregate information along both time and frequency within a scale, and TDF (Time-Distributed Frequency) blocks, which operate fully along frequency within each frame — explicitly designed so that frequency-axis processing sees the long-range harmonic structure of music. DTTNet (ICASSP 2024) is a lightweight dual-path TFC-TDF variant, and RT-STT (ICME 2025) specialised the lineage for real-time low-latency operation.

Trained weight visualizations of single-layered TDF blocks show *why* frequency-axis linear layers help: each matrix organizes into a linear harmonic pattern ($y=\frac{\alpha}{\beta}x$) matching the timbre of its target instrument, and this structure is robust across scales.

![[raw/papers/kim-2021-kuielab-mdx-net/figures/fig1.png|TDF weight matrices visualization]]

*Figure: Weight matrices of single-layered TDF blocks (one per instrument), each capturing the harmonic pattern of its target source.*

## v2 Efficiency Modifications (Kim et al. 2021)

[[sources/kim-2021-kuielab-mdx-net|Kim et al. 2021]] introduced **TFC-TDF-U-Net v2** — the architecture inside [[concepts/kuielab-mdx-net|KUIELab-MDX-Net]] — with three changes that cut parameters with negligible quality loss, motivated by the MDX Challenge's wall-clock limit:

1. **Multiplicative U-connections**: element-wise multiplication instead of channel-wise concatenation on each encoder–decoder skip connection.
2. **No other skip connections**: dense-block-style skips removed; stacked convolutions with TDFs match dense blocks without them.
3. **Channel scaling**: intermediate channels increase/decrease by a factor of 32 after each down/upsampling layer (v1 kept them constant), making v2 shallower but wider (11 blocks / 3 convs / $bn{=}8$ vs. v1's 9 / 5 / 16).

v2 is also trained with a time-domain $l_1$ loss (instead of v1's loss) and per-source frequency cutoff, allowing $n_{\mathrm{fft}}$ up to 16384 (bass) at fixed input spectrogram size.

## Causal/Streaming Specialization

[[sources/li-2026-realtime-music-separation-dsp|Li et al. 2026]] deployed a causal TFC-TDF U-Net on a commercial audio DSP (SHARC-FX), with design choices dictated by streaming rather than accuracy:

- All convolutions are **depthwise-separable** and **left-padded in time**, so frame $t$ depends only on past samples.
- The input is the real-valued STFT ($n_{\mathrm{fft}}{=}1024$, hop 512, no centre padding); only the lowest $F{=}384$ bins (0–16.5 kHz) are processed, the high band being reconstructed via a per-source gain — the frequency crop is a compute dial, with MAC scaling linearly in $F$.
- The recurrence is a **GRU** rather than an LSTM: the GRU state is a convex combination of bounded terms and stays in $[-1,1]$ by construction, whereas an LSTM cell state is an unbounded running sum that grows without plateau under indefinite streaming (measured 399→962 over 120 s), eventually saturating downstream activations and forcing periodic resets that reintroduce buffering latency.
- The network emits a [[concepts/complex-ratio-mask|complex ratio mask]] on the input spectrum, so silence maps to exactly silence and the idle noise floor is zero by construction.

Deployed sizes: 131 k parameters (501 kB float32) for the full-band variant; a slim $F{=}192$ variant runs at 129 k. Per-frame cost is tracked by the [[concepts/weight-reuse-factor|weight reuse factor]] $\rho \approx 140$–$348$ for this family, because frequency-axis convolution reuses each kernel across all $F$ bins every frame.

## Related Concepts

- [[concepts/music-source-separation|Music Source Separation]]
- [[concepts/kuielab-mdx-net|KUIELab-MDX-Net]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask]]
- [[concepts/gated-recurrent-unit|Gated Recurrent Unit]]
- [[concepts/depthwise-separable-convolution|Depthwise-Separable Convolution]]
- [[concepts/weight-reuse-factor|Weight Reuse Factor]]

## Related Sources

- [[sources/li-2026-realtime-music-separation-dsp|Li, Liu, Malsky & Yi 2026: Real-Time Music Source Separation on a Low-Power Audio DSP]]
- [[sources/kim-2021-kuielab-mdx-net|Kim, Choi, Chung, Lee & Jung 2021: KUIELab-MDX-Net — A Two-Stream Neural Network for Music Demixing]]
