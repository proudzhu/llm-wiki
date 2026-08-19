---
type: concept
created: 2026-05-21
updated: 2026-08-08
sources:
  - raw/papers/guo-2023-iva-survey/full-text.md
  - raw/papers/dong-2026-spatially-regularized-switching-iva/full-text.md
  - raw/papers/richard-2023-audio-signal-processing-21st-century/full-text.md
tags:
  - signal-processing
  - audio-source-separation
  - unsupervised-methods
---

# Blind Source Separation

**Blind Source Separation (BSS)** is the task of recovering individual source signals from observed mixtures without knowledge of the mixing process or the source signals themselves. In audio, BSS aims to separate speech or sound sources from multichannel microphone recordings in reverberant environments.

## Problem Formulation

In the time domain, a convolutive mixture is modeled as:

$$x_m[t] = \sum_{n=1}^N \sum_{\ell=0}^{L-1} a_{mn}[\ell]\, s_n[t-\ell] + b_m[t]$$

where $a_{mn}[\ell]$ are room impulse response coefficients, $s_n$ are source signals, and $b_m$ is sensor noise. In the STFT domain this simplifies to instantaneous mixing per frequency bin:

$$\mathbf{x}^{(k)}[z] = \mathbf{A}^{(k)}\mathbf{s}^{(k)}[z]$$

## Main Approaches

| Method | Model | Permutation handling |
|--------|-------|---------------------|
| Frequency-domain ICA | Per-bin instantaneous | Post-hoc alignment needed |
| [[concepts/independent-vector-analysis\|IVA]] | Multivariate across freq bins | Built into cost function |
| [[concepts/switching-independent-vector-analysis\|SwIVA]] | Multiple demixing matrices | Switching mechanism + spatial regularization |
| ILRMA | IVA + NMF source model | Via NMF spectral structure |
| [[concepts/fastmnmf\|FastMNMF]] | Full-rank SCM + NMF | Joint diagonalization |

## Key Challenges

- **Permutation ambiguity**: Each frequency bin is solved independently in ICA, so source ordering may differ across bins.
- **Scaling ambiguity**: Source magnitudes are not identifiable without additional constraints.
- **Underdetermined mixtures**: When sources outnumber microphones ($N > M$), full separation requires sparse/structured priors.
- **Computational cost**: Joint optimization over all frequency bins is expensive; efficient update rules (IP, ISS, AuxIVA) are critical.

## Applications

- Meeting transcription (multi-speaker separation)
- Hearing aids and hearables
- Robot audition
- Music source separation

## Historical Context

[[sources/richard-2023-audio-signal-processing-21st-century|Richard et al. 2023]] trace the 25-year evolution of audio BSS along two branches. The **determined case** moved from frequency-domain ICA (with its permutation/scaling ambiguities resolved by spatial and spectral source information) through TRINICON (an information-theoretic cost exploiting nonwhiteness, nongaussianity, and nonstationarity), IVA, ILRMA (combining ICA spatial info with NMF spectral structure), to the DNN-augmented multichannel VAE (MVAE). The **monophonic / underdetermined case** moved from trained NMF dictionaries, through W-disjoint-orthogonality binary masking and deep clustering, to discriminative mask-prediction networks (now dominant, spanning on-device enhancers and offline music-separation models used in award-winning Beatles restorations). Open questions highlighted by the retrospective include universal separators, limited-data learning, and out-of-distribution generalization.

## Related Concepts

- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/switching-independent-vector-analysis|Switching Independent Vector Analysis]]
- [[concepts/iterative-source-steering|Iterative Source Steering]]
- [[concepts/spatial-regularization|Spatial Regularization]]
- [[concepts/multichannel-nmf|Multichannel NMF]]
- [[concepts/independent-low-rank-matrix-analysis|Independent Low-Rank Matrix Analysis]]
- [[concepts/fastmnmf|FastMNMF]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/cross-talk-reduction|Cross-Talk Reduction]]

## Related Sources

- [[sources/guo-2023-iva-survey|Guo, Luo & Li 2023: IVA Survey]]
- [[sources/nishikori-2026-fast-multichannel-nmf-block-diagonal-scm-bss|Nishikori et al. 2026: Distributed FastMNMF for BSS]]
- [[sources/wang-2026-cross-talk-speech-reduction-separation|Wang & Cornell 2026: Cross-Talk Speech Reduction]]
- [[sources/dong-2026-spatially-regularized-switching-iva|Dong et al. 2026: Spatially-Regularized Switching IVA with ISS]]
- [[sources/richard-2023-audio-signal-processing-21st-century|Richard et al. 2023: Audio Signal Processing in the 21st Century]] — 25-year retrospective tracing the determined and monophonic BSS lineages
- [[sources/sawada-2019-bss-ilrma-review|Sawada et al. 2019: BSS/ILRMA Review]] — unified tutorial of the ICA and NMF routes converging at ILRMA
