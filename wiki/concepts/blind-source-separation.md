---
type: concept
created: 2026-05-21
updated: 2026-05-21
sources:
  - raw/papers/guo-2023-iva-survey/full-text.md
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

## Related Concepts

- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/fastmnmf|FastMNMF]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/cross-talk-reduction|Cross-Talk Reduction]]

## Related Sources

- [[sources/guo-2023-iva-survey|Guo, Luo & Li 2023: IVA Survey]]
- [[sources/nishikori-2026-fast-multichannel-nmf-block-diagonal-scm-bss|Nishikori et al. 2026: Distributed FastMNMF for BSS]]
- [[sources/wang-2026-cross-talk-speech-reduction-separation|Wang & Cornell 2026: Cross-Talk Speech Reduction]]
