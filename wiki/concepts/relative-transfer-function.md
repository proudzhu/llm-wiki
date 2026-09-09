---
type: concept
created: 2026-05-26
updated: 2026-09-09
sources:
  - raw/papers/yan-2014-dual-mic-bt-noise-reduction/full-text.md
  - raw/papers/xiao-2023-spatially-selective-anc/full-text.md
  - raw/papers/grumiaux-2022-ssl-deep-learning-survey/full-text.txt
tags:
  - spatial-filtering
  - beamforming
  - acoustic-modeling
  - transfer-function
---

# Relative Transfer Function (RTF)

The **Relative Transfer Function (RTF)** describes the acoustic propagation from a source to each microphone relative to a reference microphone. Unlike the absolute transfer function (ATF), the RTF captures only the relative differences between channels, eliminating the common source excitation and making it directly useful for spatial filtering.

## Definition

For a source at direction $\theta$ with ATF $\mathbf{h}(k,\theta) \in \mathbb{C}^{M}$ across $M$ microphones, the RTF with respect to the reference microphone $r$ is:

$$
\mathbf{a}(k,\theta) = \frac{\mathbf{h}(k,\theta)}{h_r(k,\theta)}
$$

where $h_r(k,\theta)$ is the ATF at the reference microphone. The RTF is normalized so that the $r$-th entry equals 1.

## Estimation via Covariance Whitening

The covariance whitening (CW) method is a popular approach for RTF estimation. Given noise-only frames $\mathcal{V}_n$:

$$
\hat{\mathbf{\Phi}}_{\mathbf{nn}}(k) = \frac{1}{|\mathcal{V}_n|} \sum_{l \in \mathcal{V}_n} \mathbf{y}(l,k) \mathbf{y}^{\mathrm{H}}(l,k)
$$

The whitened signal is:

$$
\mathbf{y_w}(l,k) = \hat{\mathbf{\Phi}}_{\mathbf{nn}}^{-1/2}(k) \mathbf{y}(l,k)
$$

For a set of target-only frames $\mathcal{V}_t$, the whitened covariance is:

$$
\hat{\mathbf{\Phi}}_{\mathbf{y_w y_w}}^{(\mathcal{V}_t)}(k) = \hat{\mathbf{\Phi}}_{\mathbf{nn}}^{-1/2}(k) \hat{\mathbf{\Phi}}_{\mathbf{yy}}^{(\mathcal{V}_t)}(k) (\hat{\mathbf{\Phi}}_{\mathbf{nn}}^{-1/2})^{\mathrm{H}}(k)
$$

The RTF is obtained from the dominant eigenvector $\hat{\bm{\psi}}^{(t)}$ of this whitened covariance:

$$
\hat{\mathbf{a}}^{(t)}(k) = \frac{ \hat{\mathbf{\Phi}}^{\mathrm{H}/2}_{\mathbf{nn}}(k) \hat{\bm{\psi}}^{(t)} }{ \mathbf{e}^{\top}_{\mathrm{ref}} \hat{\mathbf{\Phi}}^{\mathrm{H}/2}_{\mathbf{nn}}(k) \hat{\bm{\psi}}^{(t)} }
$$

where $\mathbf{e}_{\mathrm{ref}}$ is the selection vector for the reference microphone.

## Importance in Beamforming

The RTF captures both direct-path and reverberant propagation effects. RTF-based beamforming yields improved speech quality compared with approaches relying solely on direct-path (steering vector) models, particularly in reverberant environments.

## Pre-modeled RTF for Near-Field Wearables

For near-field devices where the source-microphone geometry is quasi-fixed — e.g., a Bluetooth headset with the mouth 3–4 cm from the reference microphone — the RTF can be pre-modeled once in a quiet environment and reused. [[sources/yan-2014-dual-mic-bt-noise-reduction|Yan et al. 2014]] show such a pre-modeled RTF (used as the GSC blocking matrix $[1, -W_s]$) is robust to wearing-angle mismatch (0°/45°/90°) and inter-user variation, since the near-field transfer path is dominated by geometry rather than room acoustics — in contrast to noise-environment adaptive RTF estimation, which degrades at low SNR. This is the near-field, single-RTF antecedent of the far-field RTF dictionaries below.

## RTF Dictionaries for Output-based Beamformer Selection

Apostolidis et al. (2026) construct a pre-enrolled dictionary of $N$ time-invariant candidate RTF vectors $\mathbf{d}_\theta(k) = \{\mathbf{d}_{\theta_1}(k), \ldots, \mathbf{d}_{\theta_N}(k)\}$, each corresponding to a candidate target direction at a fixed distance. Each candidate RTF parameterizes a candidate [[concepts/mpdr-beamformer|MPDR]] beamformer, and the [[concepts/output-based-speech-enhancement|output-based]] wrapper selects the candidate whose output maximizes [[concepts/glimpse-proportion|Glimpse Proportion]]. The system remains robust to RTF mismatch: significant SNR/ESTOI gains over an input-based [[concepts/mvdr-beamformer|MVDR]] baseline persist when the dictionary is coarse (15° spacing) or non-individualized (HATS-measured RTFs).

## Relative Impulse Responses in Spatially Selective ANC

In the time domain, the RTF counterpart is the **relative impulse response (ReIR)**. [[sources/xiao-2023-spatially-selective-anc|Xiao, Xu & Zhao 2023]] use ReIRs as the building block of [[concepts/spatially-selective-anc|spatially selective ANC]]: $\mathbf{H}$ stacks the Toeplitz matrices of the ReIRs between each microphone and a reference microphone (closest to the desired source), and the constraint vector $\mathbf{f} = \mathbf{h}_K$ (the error-microphone ReIR) fixes the desired-direction response so the physical desired wave is preserved at the error microphone rather than reconstructed. Unlike beamforming-side RTF estimation, these ReIRs are design-time quantities (pre-measured per desired direction), and later soft-constrained SSANC variants use **acausal** ReIRs with a delayed-impulse target $\boldsymbol{\delta}_\Delta$.

## Related Concepts

- [[concepts/lcmv-beamformer|LCMV Beamformer]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/room-transfer-function|Room Transfer Function]]
- [[concepts/room-impulse-response|Room Impulse Response]]
- [[concepts/generalized-eigenvalue-decomposition|Generalized Eigenvalue Decomposition]]
- [[concepts/mpdr-beamformer|MPDR Beamformer]]
- [[concepts/output-based-speech-enhancement|Output-based Speech Enhancement]]

## Related Sources

- [[sources/zaidel-2026-linearly-constrained-deep-beamformer|Zaidel et al. 2026: Linearly Constrained Deep Beamformer]]
- [[sources/apostolidis-2026-listen-first-output-based-multi-microphone|Apostolidis et al. 2026: Listen first — output-based multi-microphone speech enhancement]]
- [[sources/xiao-2023-spatially-selective-anc|Xiao 2023: Spatially Selective Active Noise Control Systems]] — ReIRs as design-time spatial constraints
