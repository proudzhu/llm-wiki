---
type: concept
created: 2026-06-07
updated: 2026-09-15
sources:
  - raw/papers/zhang-2021-adl-mvdr/full-text.md
  - raw/papers/li-2026-realtime-music-separation-dsp/full-text.md
tags:
  - speech-enhancement
  - signal-processing
  - deep-learning
---

# Deep Filtering

Deep filtering (DF) is a speech enhancement technique that applies a learned complex-valued linear filter along the time axis in the STFT domain, rather than a pointwise multiplication with a mask. By incorporating information from neighboring time frames within each frequency band, DF can model quasi-static speech properties and recover signal degradations that pointwise masks cannot address.

## Formulation

Deep filtering is defined by a complex filter applied per frequency bin:

$$
Y(k, f) = \sum_{i=0}^{N} C(k, i, f) \cdot X(k - i + l, f)
$$

where $C$ are the complex coefficients of filter order $N$, $X$ is the input spectrogram, $Y$ is the enhanced spectrogram, and $l$ is an optional look-ahead allowing non-causal taps.

## Key Properties

- **Filter order $N$**: Higher orders capture longer temporal correlations but increase computation. Typical values: $N=3$ to $N=5$.
- **Look-ahead $l$**: Allows incorporating future frames for non-causal filtering. $l=1$ means one future frame is used.
- **Per-band operation**: Filters are applied independently to each frequency band, exploiting local temporal correlations.
- **Alpha blending**: A learned weighting factor $\alpha(k)$ blends DF output with the gain-enhanced output, ensuring DF only affects periodic components.

## Advantages over Complex Masks

- DF outperforms complex ratio masks (CRMs) across all tested FFT sizes (5–30 ms latency)
- Particularly advantageous at low FFT resolutions where CRMs degrade due to insufficient frequency resolution
- Can recover signal degradations like notch-filters or time-frame zeroing that pointwise masks cannot
- DF is a strict generalization of CRM (CRM = DF with $N=1$, $l=0$)

## Two-Dimensional (Time-Frequency) Deep Filtering

[[sources/zhang-2021-adl-mvdr|Zhang et al. 2021]] adopt deep filtering — under the name **complex ratio filtering (cRF)**, from Mack & Habets (2019) — as a 2-D extension: the complex filter spans a $(2K+1)\times(2L+1)$ neighborhood of *both* time and frequency (a 3×3 cRF, $K=L=1$), equivalent to a bank of shifted complex ratio masks. The cRF is applied to the multi-channel mixture to estimate speech and noise components, from which **frame-level** covariance matrices are computed for the [[concepts/adl-mvdr|ADL-MVDR]] beamformer (center-mask normalization, no summation over time). Empirically, cRF consistently outperforms the per-bin [[concepts/complex-ratio-mask|cRM]] (e.g., Si-SNR 12.50 vs. 12.23 dB; WER 22.07 vs. 22.49% for NN systems), and matters most when the downstream consumer recursively derives frame-level statistics from the filtered estimates.

## Causal Gated Deep Filtering as a Latency Knob

[[sources/li-2026-realtime-music-separation-dsp|Li et al. 2026]] use deep filtering *causally* for real-time music source separation on an embedded audio DSP, with three departures from prior (offline/speech) usage:

- **Gated per source**: a small convolutional head predicts, alongside the taps, a gate $G \in (0,1)$ per source and TF bin; the final estimate blends the DF output with a pointwise [[concepts/complex-ratio-mask|complex ratio mask]] estimate, $\hat{S}_t = G \odot \hat{S}^{\mathrm{bb}}_t + (1-G) \odot \hat{S}^{\mathrm{df}}_t$, so the network can *decline* deep filtering. The learned gate reveals where DF pays: blend usage converges to 0.104 for vocals but 0.007 for bass — deep filtering does not pay on a source whose energy already sits in a few bins (forcing the bass gate open only degrades it).
- **Explicit latency control**: the split between $P$ past and $Q$ future taps sets the added algorithmic latency exactly ($Q \cdot H/f_s = 11.6Q$ ms at hop 512 / 44.1 kHz). A *strictly causal* filter ($Q{=}0$) already gains 0.38 dB cSDR over the matched no-DF baseline, on every stem — the gain is complex FIR filtering, not future information.
- **Stability by construction**: the filter is applied to the *mixture* spectrum (so silence maps to silence), and the taps' real/imaginary parts are each $\tanh$-bounded. The tap *predictor* head is itself causally (left-)padded at $Q{=}0$ — without that, the filter would be causal but its taps not.

## Applications

- [[sources/schroter-2022-deepfilternet|DeepFilterNet]] (Schröter et al., ICASSP 2022) — two-stage speech enhancement using ERB gains + DF
- CLCNet (Schröter et al., ICASSP 2020) — complex linear coding for hearing aid noise reduction
- DCCRN+ (Lv et al., INTERSPEECH 2021) — channel-wise subband DCCRN with DF

## Related Concepts

- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[concepts/erb-scale|ERB Scale]]
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[concepts/trainable-frequency-compression|Trainable Frequency Compression]] — complementary axis: DF learns a per-band temporal filter, trainable frequency compression learns a per-band frequency filter

- [[concepts/complex-ratio-mask|Complex Ratio Mask]] — pointwise 1×1 special case
- [[concepts/adl-mvdr|ADL-MVDR]] — 2-D cRF used for frame-level covariance estimation in an all-deep-learning MVDR

## Related Sources

- [[sources/schroter-2022-deepfilternet|Schröter et al. 2022: DeepFilterNet]]
- [[sources/chen-2023-ultra-dual-path-compression|Chen et al. 2023: Ultra Dual-Path Compression]] — matches DeepFilterNet quality at 1/4 the parameters by combining time and frequency compression on a DPT-FSNet backbone
- [[sources/zhang-2021-adl-mvdr|Zhang et al. 2021: ADL-MVDR]] — 2-D (time-frequency) cRF for multi-channel frame-level covariance estimation
- [[sources/li-2026-realtime-music-separation-dsp|Li, Liu, Malsky & Yi 2026: Real-Time Music Source Separation on a Low-Power Audio DSP]] — first *causal, gated* use of DF; past/future tap split as an explicit algorithmic-latency knob (+0.38 dB even strictly causal)
