---
type: entity
created: 2026-10-04
updated: 2026-10-05
tags:
  - researcher
  - speech-enhancement
  - blind-source-separation
---

# Tetsuya Ueda

**Affiliation**: Waseda University, Japan
**Role**: Researcher
**Research Focus**: Blind source separation, independent vector analysis, geometrically constrained IVA, online joint optimization of separation and dereverberation.

## Key Contributions

- Co-author of "Accelerating Online Algorithm Using Geometrically Constrained Independent Vector Analysis with Iterative Source Steering" (APSIPA ASC 2022) — online GC-AuxIVA-ISS, an inverse-free online algorithm for geometrically constrained IVA — [[sources/goto-2022-iss-gciva|Goto et al. 2022]]
- Co-author of "Geometrically Constrained Independent Vector Analysis with Auxiliary Function Approach and Iterative Source Steering" (EUSIPCO 2022) — the offline GC-AuxIVA-ISS predecessor (referenced as prior work in [[sources/goto-2022-iss-gciva|Goto et al. 2022]])
- Co-author of "GC-IVA with Auxiliary Function Approach and Iterative Source Steering" (30th European Signal Processing Conference (EUSIPCO 2022), 2022) — first derivation of the inverse-free offline GC-AuxIVA-ISS algorithm (ISS rank-1 updates with geometric constraints in the closed-form coefficients), showing block-permutation avoidance and 34-53% per-iteration runtime reduction over GC-AuxIVA-VCD — [[sources/goto-2022-offline-iss-gciva|Goto, Ueda, Li, Yamada & Makino 2022]]
- First author of "Blind and Spatially-Regularized Online Joint Optimization of Source Separation, Dereverberation, and Noise Reduction" (IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 32, 2024) — first blind online joint optimization of source separation, dereverberation, and noise reduction under a single ML criterion (online-WPE×IVE), extended with scale-regularized spatial alignment (online-WPE×SRIVE) achieving 0% permutation error at 8 ms algorithmic delay — [[sources/ueda-2024-online-joint-optimization|Ueda, Nakatani, Ikeshita, Kinoshita, Araki & Makino 2024]]

## Related Sources

- [[sources/goto-2022-iss-gciva|Goto et al. 2022: Accelerating Online GC-IVA with Iterative Source Steering]]
- [[sources/goto-2022-offline-iss-gciva|Goto, Ueda, Li, Yamada & Makino 2022: GC-IVA with Auxiliary Function Approach and Iterative Source Steering]]
- [[sources/ueda-2024-online-joint-optimization|Ueda, Nakatani, Ikeshita, Kinoshita, Araki & Makino 2024: Blind and Spatially-Regularized Online Joint Optimization of Source Separation, Dereverberation, and Noise Reduction]]
