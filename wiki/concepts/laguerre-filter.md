---
type: concept
created: 2026-11-01
updated: 2026-11-01
sources:
  - raw/papers/klatt-2025-laguerre-feedback-anc/full-text.md
tags:
  - filter-design
  - signal-processing
  - active-noise-control
  - system-identification
---

# Laguerre Filter

A **Laguerre filter** (or Laguerre network) is an IIR filter built as a weighted sum of discrete-time Laguerre basis functions, realized as a chain of all-pass sections behind a first-order low-pass input stage. It generalizes the FIR transversal structure: the coefficient vector multiplies a **generalized delay operator** rather than tapped delays, allowing a low-order Laguerre filter to reproduce the frequency response of a much higher-order FIR filter when the target response is concentrated at low frequencies.

## Key Formulations

Any discrete-time system $Q_0(z)$ can be represented by the Laguerre series

$$
Q_\ell(z) = \sum_{m=0}^{\infty} q_m(\alpha)\, \Lambda_m(z, \alpha), \qquad
\Lambda_m(z, \alpha) = \sqrt{1 - \alpha^2}\, \frac{(z^{-1} - \alpha)^m}{(1 - \alpha z^{-1})^{m+1}},
$$

where $\Lambda_m(z, \alpha)$ is the z-Transform of the m-th discrete-time Laguerre polynomial and $\alpha \in (-1, 1)$ is the **Laguerre parameter** — the pole position shared by the all-pass sections. In practice the series is truncated to order $M$ (a network of $M$ stages), giving coefficients $\mathbf{q}(\alpha) = [q_0(\alpha), \ldots, q_M(\alpha)]^{\mathsf{T}}$ that behave like transversal filter coefficients:

$$
Q_\ell(z) = \mathbf{q}^{\mathsf{T}} \boldsymbol{\Lambda}(z, \alpha).
$$

Key structural properties:

- **$\alpha = 0$ reduces to FIR**: the network degenerates to an M-th order FIR filter
- **$\alpha \to 1$ → strong low-pass character**: $\alpha$ is the pole of the input-stage low-pass, so values close to 1 concentrate the basis's spectral resolution at low frequencies
- **Affine in $\mathbf{q}$**: on the unit circle, $Q_\ell(\mathrm{e}^{\mathrm{j}\Omega_k}) = \mathbf{q}^{\mathsf{T}} \boldsymbol{\Lambda}(\mathrm{e}^{\mathrm{j}\Omega_k}, \alpha)$ is affine in the coefficient vector — a property that preserves convexity of optimization problems (e.g. IMC controller synthesis) when replacing an FIR filter
- The truncated network is **IIR** (recursive all-pass sections), but the design freedom is FIR-like: only $\mathbf{q}$ is optimized, with $\alpha$ chosen in advance

## Choosing the Laguerre Parameter

In classical system identification, $\alpha$ is optimized against the target frequency response (Oliveira e Silva 1995). In feedback ANC with the IMC topology, [[sources/klatt-2025-laguerre-feedback-anc|Klatt & Martin 2025]] show via a 36-controller grid study ($\alpha \in \{0, 0.25, 0.5, 0.75, 0.925, 0.95\}$, $M \in \{15, \ldots, 95\}$) that the $W_d$-weighted mean sensitivity improves monotonically with $\alpha$ and converges for $0.75 \le \alpha < 1$ — so $\alpha$ should be chosen **close to 1** whenever the control band is at low frequencies (sub-1-kHz for ANC), where the low-pass-shaped basis pre-emphasizes exactly the relevant spectrum.

## Comparison with Frequency-Warped FIR Filters

The Laguerre network is closely related to [[concepts/warped-fir-filter|warped FIR (WFIR) filters]] — both replace the unit delay with an all-pass element $\frac{z^{-1} - \lambda}{1 - \lambda z^{-1}}$ whose pole position ($\alpha$ vs $\lambda$) reallocates frequency resolution toward low frequencies. The connection runs deeper: the m-th Laguerre basis function $\Lambda_m$ is the impulse response of the m-fold cascade of the all-pass with a first-order low-pass pre-filter, so a Laguerre network is a low-pass-filtered WFIR-like expansion with orthonormal basis functions. Practical differences in the ANC context:

| Aspect | WFIR (Seo 2016) | Laguerre (Klatt & Martin 2025) |
|:-------|:-----------------|:-------------------------------|
| Structure | FIR coefficients on all-pass delays | Coefficients on orthonormal Laguerre basis |
| Optimization | Warped-domain constrained SQP | Same convex IMC program as FIR (affine in $\mathbf{q}$) |
| Reported ANC result | 16th-order WFIR ≈ 128th-order FIR | 17th-order Laguerre ≈ 255th-order FIR |
| High-frequency behavior | Depends on regularization | Inherently bounded (low-pass basis) |

## Computational Complexity

A Laguerre filter of order $M$ costs $2 + 4M$ MAC operations per sample (vs $M_{\mathrm{FIR}}$ for an FIR of order $M_{\mathrm{FIR}}$). When $M \ll M_{\mathrm{FIR}}$ — e.g. $M = 17$ vs $M_{\mathrm{FIR}} = 255$ in Klatt & Martin 2025 — the net per-sample cost is substantially lower.

## Applications

- **Feedback ANC control filter design**: the $Q$ filter in [[concepts/internal-model-control|Internal Model Control]] — the central application of [[sources/klatt-2025-laguerre-feedback-anc|Klatt & Martin 2025]]; earlier Laguerre-ANC work (Yuan 2007; Veena & Narasimhan 2007) used non-IMC adaptive topologies
- **System identification**: Laguerre models offer lower-order fits than FIR with comparable approximation errors (Wahlberg 1991), used for modeling systems with slowly decaying impulse responses
- **Secondary path modeling**: proposed as future work in Klatt & Martin 2025 — using Laguerre filters to model the secondary path itself

## Related Concepts

- [[concepts/internal-model-control|Internal Model Control]]
- [[concepts/feedback-anc|Feedback ANC]]
- [[concepts/warped-fir-filter|Warped FIR Filter]]
- [[concepts/frequency-warping|Frequency Warping]]
- [[concepts/all-pass-filter|All-Pass Filter]]
- [[concepts/system-identification|System Identification]]

## Related Sources

- [[sources/klatt-2025-laguerre-feedback-anc|Klatt & Martin 2025: Laguerre Filter-based Robust Feedback Active Noise Control]]
- [[sources/seo-2016-feedback-anc-constrained-optimization|Seo, Park & Youn 2016: Feedback ANC via Constrained Optimization for Headphones]] — the WFIR counterpart approach
