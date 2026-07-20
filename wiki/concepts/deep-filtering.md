---
type: concept
created: 2026-06-07
updated: 2026-06-07
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

## Applications

- [[sources/schroter-2022-deepfilternet|DeepFilterNet]] (Schröter et al., ICASSP 2022) — two-stage speech enhancement using ERB gains + DF
- CLCNet (Schröter et al., ICASSP 2020) — complex linear coding for hearing aid noise reduction
- DCCRN+ (Lv et al., INTERSPEECH 2021) — channel-wise subband DCCRN with DF

## Related Concepts

- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[concepts/erb-scale|ERB Scale]]
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[concepts/trainable-frequency-compression|Trainable Frequency Compression]] — complementary axis: DF learns a per-band temporal filter, trainable frequency compression learns a per-band frequency filter

## Related Sources

- [[sources/schroter-2022-deepfilternet|Schröter et al. 2022: DeepFilterNet]]
- [[sources/chen-2023-ultra-dual-path-compression|Chen et al. 2023: Ultra Dual-Path Compression]] — matches DeepFilterNet quality at 1/4 the parameters by combining time and frequency compression on a DPT-FSNet backbone
