---
type: concept
created: 2026-08-16
updated: 2026-08-16
sources:
  - raw/papers/taseska-2018-informed-spatial-filters/full-text.md
tags:
  - spatial-filter
  - speech-enhancement
  - gsc
  - adaptive-filter
  - rls
  - signal-cancellation
---

# Informed GSC

An **informed GSC** is a General Sidelobe Canceller whose three components — the Fixed Beamformer (FBF), the Blocking Matrix (BM), and the Noise Canceller (NC) — are adapted *per time-frequency bin* under the control of a narrowband signal detector. It is the adaptive, matrix-inversion-free implementation of an [[concepts/informed-spatial-filter|informed spatial filter]], developed by Taseska, Varzandeh & Habets (IWAENC 2016) using the DOA model-based detector to control the updates.

## Structure

The informed GSC decomposes the informed MVDR filter as:

$$
\mathbf{w}_{\mathrm{gsc}}(t,k) = \mathbf{w}_{\mathrm{fbf}}(t,k) - \mathbf{B}(t,k)\,\mathbf{w}_{\mathrm{nc}}(t,k),
$$

where:

- $\mathbf{w}_{\mathrm{fbf}} = \mathbf{g}_1 / \|\mathbf{g}_1\|^2$ is the Fixed Beamformer, computed from the estimated desired-signal RTF vector $\mathbf{g}_1$ (ensures the desired signal is preserved).
- $\mathbf{B}$ is the Blocking Matrix, whose columns span the null space of $\mathbf{g}_1$ (blocks the desired signal, creating noise references).
- $\mathbf{w}_{\mathrm{nc}}$ is the Noise Canceller, operating on the BM outputs to reduce the undesired signal.

## Bin-Wise Adaptation Control

The signal-cancellation problem of standard GSCs (desired-signal leakage through an imperfect BM) is alleviated by updating the NC **only when the desired signal is absent** — i.e., using the undesired-signal PSD matrix $\boldsymbol{\Phi}_{\mathbf{u}}$ rather than the microphone PSD matrix $\boldsymbol{\Phi}_{\mathbf{y}}$. The DOA model-based detector provides this bin-wise control: it determines, at each TF bin, whether the desired source, an interferer, or noise is dominant, and the FBF/BM/NC are updated accordingly. This is analogous to using $\boldsymbol{\Phi}_{\mathbf{u}}$ (MVDR) vs. $\boldsymbol{\Phi}_{\mathbf{y}}$ (MPDR) in the closed-form filter.

## Recursive (RLS) Implementation

The NC can be implemented via Recursive Least Squares (RLS), avoiding the per-bin matrix inversion required by the closed-form informed MVDR. The RLS update is also controlled by the detector, ensuring the NC adapts only on desired-absent bins.

## Result

Informed GSCs match the closed-form informed MVDR filter's performance without notable loss, validating the GSC as an efficient practical alternative for highly non-stationary scenarios. The BM construction uses the RTF-based form (Gannot et al.) rather than the anechoic Griffiths-Jim form, with the RTF estimated online via the detector.

## Related Concepts

- [[concepts/gsc-beamformer|General Sidelobe Canceller (GSC)]]
- [[concepts/informed-spatial-filter|Informed Spatial Filter (ISF)]]
- [[concepts/doa-informed-source-extraction|DOA-Informed Source Extraction]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/mpdr-beamformer|MPDR Beamformer]]
- [[concepts/relative-transfer-function|Relative Transfer Function (RTF)]]

## Related Sources

- [[sources/taseska-2018-informed-spatial-filters|Taseska 2018: Informed Spatial Filters for Speech Enhancement]] (Chapter 5)
