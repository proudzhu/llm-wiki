---
type: concept
created: 2026-05-21
updated: 2026-08-26
sources:
  - raw/papers/guo-2023-iva-survey/full-text.md
  - raw/papers/dong-2026-spatially-regularized-switching-iva/full-text.md
  - raw/papers/richard-2023-audio-signal-processing-21st-century/full-text.md
  - raw/papers/ansari-2023-ai-bss-survey/full-text.md
  - raw/papers/ruan-2024-speech-extraction-low-snr/full-text.md
  - raw/papers/scheibler-2020-fast-independent-vector-extraction/full-text.md
  - raw/papers/kang-2019-low-complexity-permutation-alignment/full-text.md
tags:
  - signal-processing
  - audio-source-separation
  - unsupervised-methods
  - machine-learning
  - deep-learning
  - evolutionary-algorithms
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

## AI-Based BSS Taxonomy

[[sources/ansari-2023-ai-bss-survey|Ansari et al. 2023]] propose a distinctive three-way taxonomy of **AI-based BSS approaches**, complementing the classical statistical BSS lineage (ICA/IVA/ILRMA/FastMNMF) tabulated above. The survey consolidates ~60 surveyed papers (2003–2023) into:

| Approach | Representative algorithms | Surveyed references |
|----------|---------------------------|---------------------|
| **Classical machine learning** | FNN, variational Bayes / VB-EM, customized EM, MLP, WMM-MAP, MAP, DBSCAN, K-means, AP, SVM, fuzzy c-means, RBF, CSKC, BNN, ANN, KAM, RF, IBM, K-hyperline clustering, CFSFDP, bigradient neural network | [89, 102–109, 111–113, 115–123, 135, 149–161, 174] |
| **Deep learning** | DNN, RNN, CNN, Conv-TasNet, BLSTM, DRNN, GAN, DAN, deep clustering, GRU, LSTM, deep fully CDAE, BRNN, mixed-type detection hierarchical DNN, VAE, GAN+VAEM, Transformer-based networks (SepFormer, Demucs) | [86, 97, 124–126, 129–137, 162–172] |
| **Evolutionary / swarm intelligence** | PSO, GA, CGA, BCO, ACO, DE, ABC, HEPSO, QPSO, BCC, BCA, DNPSO, quantum GA, FPA, cat swarm | [138–140, 142–148, 173–182] |

The survey benchmarks these methods across audio, speech, music, voice, and source separation applications (Tables 1, 5, 6) and contrasts their computational complexity (Tables 7, 8). Key cross-method findings:

- **DL dominates when labeled data is abundant** but at substantially higher computational cost than classical statistical methods.
- **Classical ML reaches strong SIR/SDR on synthetic data** (e.g., FastICA with ML contrast: SDR 49.70 dB / SIR 51.33 dB / SAR 54.76 dB), but performance is data-specific.
- **Evolutionary methods** are most often used to optimize ICA / FastICA contrast functions or solve nonlinear BSS; their performance is problem-dependent (MABC+covariance-ratio reaches SNR 25.84 dB on speech/music, while ABC permutation alignment reaches only SDR 1.85 dB).
- **Heterogeneous metrics across studies** make fair cross-study comparison difficult; the survey calls for a standardized perceptual evaluation framework and explicit Big-O complexity reporting.
- **Open challenges**: speed/accuracy trade-off, multipurpose BSS models, robustness/scalability, underdetermined convolutive cases, non-harmonic instruments, nonlinear mixing, hybrid ML models, edge/mobile/on-device deployment, and transfer learning for data-scarce domains.

## Key Challenges

- **Permutation ambiguity**: Each frequency bin is solved independently in ICA, so source ordering may differ across bins. Post-hoc [[concepts/permutation-alignment|permutation alignment]] resolves it — and can be made cheap: a confidence-thresholded local-first scheme matches state-of-the-art alignment quality at 4–5× lower runtime ([[sources/kang-2019-low-complexity-permutation-alignment|Kang, Yang & Yang 2019]]); IVA/ILRMA-class methods avoid the problem by construction.
- **Scaling ambiguity**: Source magnitudes are not identifiable without additional constraints.
- **Underdetermined mixtures**: When sources outnumber microphones ($N > M$), full separation requires sparse/structured priors.
- **Computational cost**: Joint optimization over all frequency bins is expensive; efficient update rules (IP, ISS, AuxIVA) are critical — for single-source extraction, FIVE's global auxiliary-function minimization reaches peak performance in a handful of iterations (Scheibler & Ono 2020).

## Applications

- Meeting transcription (multi-speaker separation)
- Hearing aids and hearables
- Robot audition
- Music source separation

## Historical Context

[[sources/richard-2023-audio-signal-processing-21st-century|Richard et al. 2023]] trace the 25-year evolution of audio BSS along two branches. The **determined case** moved from frequency-domain ICA (with its permutation/scaling ambiguities resolved by spatial and spectral source information) through TRINICON (an information-theoretic cost exploiting nonwhiteness, nongaussianity, and nonstationarity), IVA, ILRMA (combining ICA spatial info with NMF spectral structure), to the DNN-augmented multichannel VAE (MVAE). The **monophonic / underdetermined case** moved from trained NMF dictionaries, through W-disjoint-orthogonality binary masking and deep clustering, to discriminative mask-prediction networks (now dominant, spanning on-device enhancers and offline music-separation models used in award-winning Beatles restorations). Open questions highlighted by the retrospective include universal separators, limited-data learning, and out-of-distribution generalization.

## Related Concepts

- [[concepts/permutation-alignment|Permutation Alignment]]
- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/blind-source-extraction|Blind Source Extraction]]
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
- [[sources/ansari-2023-ai-bss-survey|Ansari et al. 2023: AI Approaches in BSS Survey]] — three-way taxonomy of AI-based BSS (Classical ML / DL / Evolutionary) complementing the statistical lineage above
- [[sources/scheibler-2020-fast-independent-vector-extraction|Scheibler & Ono 2020: Fast Independent Vector Extraction]] — fast single-source extraction via iterative SINR maximization
- [[sources/kang-2019-low-complexity-permutation-alignment|Kang, Yang & Yang 2019: A Low-Complexity Permutation Alignment Method for Frequency-Domain BSS]] — makes the post-hoc alignment route computationally competitive with permutation-free methods
