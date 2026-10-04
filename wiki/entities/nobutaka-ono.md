---
type: entity
created: 2026-08-19
updated: 2026-10-04
tags:
  - researcher
  - blind-source-separation
  - independent-vector-analysis
  - optimization-algorithms
---

# Nobutaka Ono

**Affiliation**: Tokyo Metropolitan University, Hino, Japan (formerly National Institute of Informatics, Japan)
**Role**: Professor, Researcher
**Research Focus**: Independent vector analysis, auxiliary-function optimization, music information processing, acoustic signal processing.

## Key Contributions

- Co-authored "A review of blind source separation methods: two converging routes to ILRMA originating from ICA and NMF" (APSIPA Trans. Signal Inf. Process. 2019) — [[sources/sawada-2019-bss-ilrma-review|Sawada et al. 2019: BSS/ILRMA Review]].
- Inventor of AuxIVA (2011), the auxiliary-function-based update rule for Independent Vector Analysis that has become the de-facto standard IVA solver due to its monotonic convergence without step-size tuning.
- Co-authored "Fast independent vector extraction by iterative SINR maximization" (ICASSP 2020) — [[sources/scheibler-2020-fast-independent-vector-extraction|Scheibler & Ono 2020: FIVE]], the iterative max-SINR beamforming algorithm that globally minimizes the auxiliary function at every iteration for real-time blind source extraction.
- Sole author of "Stable and Fast Update Rules for Independent Vector Analysis Based on Auxiliary Function Technique" (IEEE Workshop on Applications of Signal Processing to Audio and Acoustics (WASPAA), New Paltz, NY, 2011, pp. 189–192) — Founding paper of AuxIVA: auxiliary-function (MM) update rules for IVA with no step sizes; the IP update (W V_k)^{-1} e_k plus normalization, with monotonic convergence guarantee — [[sources/ono-2011-stable-fast-update-rules-iva|Ono 2011]]
- First author of "Fast and Stable Blind Source Separation with Rank-1 Updates" (IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Barcelona, Spain, 2020, pp. 236–240) — AuxIVA-ISS: inverse-free rank-1 updates of the demixing matrix (equivalently, steering-vector updates), reducing per-iteration complexity from O(FM^3 max(M,N)) to O(FM^2N) with identical separation quality — [[sources/scheibler-2020-fast-stable-bss-rank-1-updates|Scheibler & Ono 2020]]

## Related Sources

- [[sources/sawada-2019-bss-ilrma-review|Sawada et al. 2019: BSS/ILRMA Review]]
- [[sources/scheibler-2020-fast-independent-vector-extraction|Scheibler & Ono 2020: Fast Independent Vector Extraction]]
- [[sources/ono-2011-stable-fast-update-rules-iva|Ono 2011: Stable and Fast Update Rules for Independent Vector Analysis Based on Auxiliary Function Technique]]
- [[sources/scheibler-2020-fast-stable-bss-rank-1-updates|Scheibler & Ono 2020: Fast and Stable Blind Source Separation with Rank-1 Updates]]
