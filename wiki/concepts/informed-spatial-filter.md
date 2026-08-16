---
type: concept
created: 2026-08-16
updated: 2026-08-16
sources:
  - raw/papers/taseska-2018-informed-spatial-filters/full-text.md
tags:
  - spatial-filter
  - speech-enhancement
  - beamforming
  - statistical-model
  - data-dependent
  - online-estimation
---

# Informed Spatial Filter (ISF)

An **Informed Spatial Filter (ISF)** is a data-dependent spatio-temporal filter whose coefficients are re-computed at each Short-Time Fourier Transform (STFT) time-frequency (TF) bin using *second-order statistics (SOS)* and propagation vectors that are estimated *online* from the microphone signals in a supervised manner. The "informed" qualifier denotes that a **narrowband signal detector** — rather than a blind or fixed scheme — decides, per TF bin, which source is dominant, and that decision drives the estimation of the desired/undesired PSD matrices and Relative Transfer Function (RTF) vectors substituted into the optimal filter expression. The paradigm was developed and unified by Taseska & Habets across noise reduction, interference reduction, acoustic spotforming, and blind source separation.

## Motivation

Optimal spatial filters (MVDR, MWF, LCMV) require the SOS of the desired and undesired signals. In practice these are *unavailable and time-varying* (moving sources, changing noise). Fixed beamformers (e.g., delay-and-sum) cannot adapt; robust adaptive beamformers trade distortion for robustness. ISFs aim for **invariable quality in dynamic scenarios** by continuously re-estimating the SOS from the data using an accurate per-bin detector.

## Five-Step Structure

All ISF frameworks share:

1. **Feature extraction** — a TF-dependent spatial feature (CDR, narrowband DOA, narrowband position) is computed from the microphone signals.
2. **Detector design** — a statistical model-based detector uses the feature to decide the dominant source at each TF bin (desired speech / interferer / noise).
3. **TF-bin association** — each bin is associated to its dominant source.
4. **Statistics update** — the PSD matrices and RTF vectors of the dominant source are updated recursively (e.g., via SPP-controlled recursive averaging).
5. **Filter computation** — the optimal filter (MVDR/MWF) or adaptive structure (GSC) is computed using the updated statistics.

The speech-sparsity assumption in the STFT domain (each TF bin dominated by one source, valid for 32–64 ms frames) is the cornerstone that makes per-bin detection meaningful.

## Filter Forms

The informed MVDR filter using the estimated undesired-signal PSD matrix $\boldsymbol{\Phi}_{\mathbf{u}}$ and desired RTF vector $\mathbf{g}$:

$$
\mathbf{w}_{\mathrm{mvdr}}(t,k) = \frac{\boldsymbol{\Phi}_{\mathbf{u}}^{-1}(t,k)\,\mathbf{g}(t,k)}{\mathbf{g}^{\mathrm{H}}(t,k)\,\boldsymbol{\Phi}_{\mathbf{u}}^{-1}(t,k)\,\mathbf{g}(t,k)}.
$$

The ISF can equivalently be implemented as an [[concepts/informed-gsc|informed GSC]] (adaptive, no matrix inversion), or extended to a Parametric Multichannel Wiener Filter (PMWF) with an SPP-based trade-off parameter. Because the statistics are re-estimated per bin, ISFs adapt *almost instantaneously* to changing source locations and noise statistics.

## Key Property

Unlike the MPDR beamformer (which uses the microphone PSD matrix $\boldsymbol{\Phi}_{\mathbf{y}}$ and suffers signal distortion under RTF mismatch), the ISF uses the *undesired*-signal PSD matrix $\boldsymbol{\Phi}_{\mathbf{u}}$, estimated only when the desired signal is detected as absent. This makes ISFs less sensitive to array calibration errors and DOA mismatch.

## Related Concepts

- [[concepts/doa-informed-source-extraction|DOA-Informed Source Extraction]]
- [[concepts/informed-gsc|Informed GSC]]
- [[concepts/multichannel-mcra|Multichannel MCRA]]
- [[concepts/acoustic-spotforming|Acoustic Spotforming]]
- [[concepts/tf-mask-estimation|TF Mask Estimation]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/multi-channel-wiener-filter|Multichannel Wiener Filter]]
- [[concepts/relative-transfer-function|Relative Transfer Function (RTF)]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/coherent-to-diffuse-power-ratio|Coherent-to-Diffuse Power Ratio (CDR)]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Related Sources

- [[sources/taseska-2018-informed-spatial-filters|Taseska 2018: Informed Spatial Filters for Speech Enhancement]]
