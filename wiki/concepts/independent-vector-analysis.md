---
type: concept
created: 2026-05-21
updated: 2026-10-05
sources:
  - raw/papers/hu-2023-gc-auxiva-iss-realistic/full-text.md
  - raw/papers/li-2020-geometrically-constrained-iva/full-text.md
  - raw/papers/li-2020-online-gciva/full-text.md
  - raw/papers/guo-2023-iva-survey/full-text.md
  - raw/papers/dong-2026-spatially-regularized-switching-iva/full-text.md
  - raw/papers/nakatani-2022-switching-iva/full-text.md
  - raw/papers/ruan-2024-speech-extraction-low-snr/full-text.md
  - raw/papers/scheibler-2020-fast-independent-vector-extraction/full-text.md
  - raw/papers/kang-2019-low-complexity-permutation-alignment/full-text.md
  - raw/papers/ansari-2023-ai-bss-survey/full-text.md
  - raw/papers/goto-2022-offline-iss-gciva/full-text.md
  - raw/papers/goto-2022-iss-gciva/full-text.md
  - raw/papers/scheibler-2021-log-quadratically-penalized-iva/full-text.md
  - raw/papers/ono-2011-stable-fast-update-rules-iva/full-text.md
  - raw/papers/scheibler-2020-fast-stable-bss-rank-1-updates/full-text.md
  - raw/papers/brendel-2020-spatially-guided-iva/full-text.md
tags:
  - blind-source-separation
  - audio-source-separation
  - optimization-algorithms
---

# Independent Vector Analysis

**Independent Vector Analysis (IVA)** is a multivariate extension of Independent Component Analysis (ICA) for frequency-domain [[concepts/blind-source-separation|blind source separation]] of convolutive audio mixtures. IVA models each source as a random vector spanning all frequency bins and exploits inter-frequency statistical dependencies to jointly estimate unmixing matrices, thereby inherently resolving the permutation ambiguity that plagues per-bin ICA.

## Problem Setting

Given $M$ microphone observations in the STFT domain:

$$\mathbf{x}^{(k)}[z] = \mathbf{A}^{(k)}\mathbf{s}^{(k)}[z], \quad k = 1, \ldots, K$$

IVA seeks unmixing matrices $\mathbf{W}^{(k)}$ for all frequency bins simultaneously by minimizing:

$$\mathcal{I}_{\mathrm{IVA}} = \sum_n E_{\mathbf{y}_n}\log g(\mathbf{y}_n) - 2\sum_k \log|\det\mathbf{W}^{(k)}| - \text{const.}$$

where $\mathbf{y}_n = [y_n^{(1)}, \ldots, y_n^{(K)}]^T$ is the estimated source vector of source $n$ across all frequency bins.

## Key Properties

1. **Permutation-free**: By modeling joint distributions $g(\mathbf{y}_n)$ across frequency bins, the separated sources are automatically aligned — no post-hoc permutation alignment is needed. This remains IVA's structural advantage over per-bin ICA even now that [[concepts/permutation-alignment|post-hoc alignment]] itself can be made low-complexity: [[sources/kang-2019-low-complexity-permutation-alignment|Kang, Yang & Yang 2019]] cut the alignment stage to 7.3 s (vs. 39–51 s for Sawada/MBMC) at equal separation quality, showing the gap is narrower than commonly assumed when alignment efficiency is optimized.
2. **Source prior flexibility**: Common choices include multivariate Laplacian, Gaussian mixture models, Student-t mixtures, and deep-learning-based priors.
3. **Separation vs. extraction**: Full IVA separates all sources simultaneously; [[concepts/independent-vector-extraction|Independent Vector Extraction (IVE)]] targets a single source of interest — and at extremely low SNR, the choice of optimization parameter (mixing vs. demixing vector) becomes decisive ([[concepts/ogive|OGIVE]]).

## Three Assumptions

1. Elements in a source vector are independent of elements in other source vectors.
2. Within a source vector, dependencies exist among elements (across frequency bins).
3. The number of sources $N \leq M$ (number of microphones).

## Optimization Methods

Six main families of update rules have been developed for IVA:

| Family | Key idea | Convergence |
|--------|----------|-------------|
| [[concepts/natural-gradient\|Natural Gradient]] | Step-size-based Riemannian descent (premultiply by $\mathbf{W}^{\mathrm{H}}\mathbf{W}$) | Slow; step-size sensitive |
| FastIVA | Newton fixed-point iteration | Fast; no step-size |
| AuxIVA | Auxiliary function (majorize-minimize) | Monotonic; stable |
| EM | Expectation-maximization for latent variables | Handles noise models |
| BCD (IP/ISS/IPA) | Block coordinate descent with closed-form updates | Widely used; efficient |
| EVD | Eigenvalue decomposition for extraction ([[concepts/fast-independent-vector-extraction\|FIVE]]) | Very fast for single source |

AuxIVA ([[sources/ono-2011-stable-fast-update-rules-iva|Ono 2011]]) is the most widely adopted baseline due to its guaranteed monotonic convergence without tuning parameters.

Within the BCD family, the update rules differ in how much of the demixing matrix they touch per step. [[concepts/iterative-projection|IP]] ([[sources/ono-2011-stable-fast-update-rules-iva|Ono 2011]]) replaces one demixing filter per step; IP2 (Ono 2018) updates two at a time via a $2\times 2$ generalized eigenvalue problem; [[concepts/iterative-source-steering|ISS]] ([[sources/scheibler-2020-fast-stable-bss-rank-1-updates|Scheibler & Ono 2020]]) applies rank-1 steering updates to all rows without matrix inversion. All three freeze the not-currently-updated sources until a later step. [[concepts/iterative-projection-with-adjustment|IPA]] ([[sources/scheibler-2021-log-quadratically-penalized-iva|Scheibler 2021]]) removes this limitation: it replaces one demixing filter while *jointly adjusting all the others* along its direction via a multiplicative rank-2 perturbation, with each step solved exactly through the new [[concepts/log-quadratically-penalized-quadratic-minimization|LQPQM]] problem (global minimum = largest zero of a secular equation). This yields faster convergence than IP, ISS, and IP2 both per iteration and per unit runtime — more than twice as fast for four and five sources — and the improvement is expected to transfer to AuxVA descendants that reuse the IP/ISS machinery (ILRMA, overdetermined IVA, geometrically constrained variants).

Beyond the six unconstrained families, IVA can be steered directionally by augmenting the objective with geometric constraints: [[concepts/geometrically-constrained-iva|Geometrically Constrained IVA (GCIVA)]] adds LCMV-style linear penalties on the far-field responses of the demixing filters. [[sources/li-2020-geometrically-constrained-iva|Li & Koishida 2020]] show that the resulting constrained stationarity equation is no longer solvable as a HEAD problem, but a closed-form, monotonic AuxIVA-style update (GCAV-IVA) exists via the vectorwise-coordinate-descent cofactor expansion — reducing exactly to AuxIVA at zero constraint weight and retaining its no-step-size-tuning property, while forcing designated output channels toward a target direction or a spatial null. The same authors with Makino extend GCAV-IVA to a real-time **online** algorithm (oGCAV-IVA) via an [[concepts/online-iva|autoregressive approximation of the auxiliary variables]] ([[sources/li-2020-online-gciva|Li, Koishida & Makino 2020]]), updating per frame at < 16 ms per 16 ms frame and outperforming online AuxIVA in both stationary and moving-interference conditions. The update can be made **inverse-free** by replacing VCD with [[concepts/iterative-source-steering|ISS]] rank-1 updates, with the geometric constraints entering the closed-form ISS coefficients directly — first offline (GC-AuxIVA-ISS, [[sources/goto-2022-offline-iss-gciva|Goto et al. 2022, EUSIPCO]] — equal-or-better separation than GCAV-IVA at the runtime of unconstrained AuxIVA-ISS, and beam-pattern evidence that the constraints prevent AuxIVA-ISS's block permutation failure), then online (oGC-AuxIVA-ISS, [[sources/goto-2022-iss-gciva|Goto et al. 2022, APSIPA ASC]] — 25–75% runtime reduction at equal enhancement quality). The GC-AuxIVA-ISS line was subsequently reproduced and validated on **real recordings** (anechoic, outdoor, and RT60 ≈ 600 ms meeting-room scenes) by [[sources/hu-2023-gc-auxiva-iss-realistic|Hu & Chen 2023]], confirming its separation and output-order-control behavior in low-reverberation conditions and exposing its failure boundary under combined strong reverberation and diffuse noise — where the IVA maximum-likelihood criterion can no longer ignore the noise because it is "not Gaussian enough".

A complementary soft-probabilistic route to the same goal is [[concepts/spatially-guided-iva|spatially guided IVA]] ([[sources/brendel-2020-spatially-guided-iva|Brendel, Haubner & Kellermann 2020]]): a MAP generalization of IVA that places a DOA-uncertainty-aware Gaussian prior directly on the demixing matrices. Because the prior is quadratic, it simply adds to the AuxIVA weighted covariance ($\mathbf{V} + \mathbf{P}$) and the MM update rules retain AuxIVA's stepsize-free monotonic convergence — on measured RIRs the constrained algorithm converges at nearly identical speed to plain AuxIVA, reaches higher SIR than the gradient-based GC-IVA of Khan et al. 2015 in all tested conditions, and resolves the outer permutation problem algorithmically, where unconstrained IVA needs an oracle to do so.

## Relationship to ILRMA and FastMNMF

IVA can also be extended along the *time-varying* axis: when the microphone surplus $M - N$ is small in diffuse noise, the determined point-source simplification fails and IVA's accuracy seriously degrades. [[concepts/switching-independent-vector-analysis|Switching IVA]] ([[sources/nakatani-2022-switching-iva|Nakatani et al. 2022]]) restores accuracy with 2–3 microphones by clustering time frames into groups, each handled by its own separation matrix, with matrices and switches jointly optimized by ML; its convolutional extension [[concepts/switching-civa|swCIVA]] adds jointly optimized switching WPE dereverberation.

IVA combined with Nonnegative Matrix Factorization gives **[[concepts/independent-low-rank-matrix-analysis|Independent Low-Rank Matrix Analysis (ILRMA)]]**, which uses NMF to model source spectral structure. [[concepts/multichannel-nmf|MNMF]] generalizes the rank-1 spatial model of ILRMA to a full-rank per-source spatial property matrix, and [[concepts/fastmnmf|FastMNMF]] further imposes joint diagonalizability of these spatial covariances for computational efficiency. The dual derivation of ILRMA from the IVA cost function (this page) and the MNMF Gaussian likelihood is unified in [[sources/sawada-2019-bss-ilrma-review|Sawada et al. 2019]].

## Related Concepts

- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/permutation-alignment|Permutation Alignment]]
- [[concepts/blind-source-extraction|Blind Source Extraction]]
- [[concepts/independent-vector-extraction|Independent Vector Extraction]]
- [[concepts/ogive|OGIVE]]
- [[concepts/fast-independent-vector-extraction|Fast Independent Vector Extraction]]
- [[concepts/natural-gradient|Natural Gradient]]
- [[concepts/independent-low-rank-matrix-analysis|Independent Low-Rank Matrix Analysis]]
- [[concepts/multichannel-nmf|Multichannel NMF]]
- [[concepts/fastmnmf|FastMNMF]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/switching-independent-vector-analysis|Switching Independent Vector Analysis]]
- [[concepts/iterative-source-steering|Iterative Source Steering]]
- [[concepts/iterative-projection|Iterative Projection]]
- [[concepts/iterative-projection-with-adjustment|Iterative Projection with Adjustment]]
- [[concepts/log-quadratically-penalized-quadratic-minimization|Log-Quadratically Penalized Quadratic Minimization]]
- [[concepts/spatial-regularization|Spatial Regularization]]
- [[concepts/geometrically-constrained-iva|Geometrically Constrained IVA]]
- [[concepts/spatially-guided-iva|Spatially Guided IVA]]
- [[concepts/online-iva|Online IVA]]

## Related Sources

- [[sources/li-2020-geometrically-constrained-iva|Li & Koishida 2020: Geometrically Constrained IVA for Directional Speech Enhancement]] — GCAV-IVA: AuxIVA-style closed-form updates under linear geometric constraints
- [[sources/li-2020-online-gciva|Li, Koishida & Makino 2020: Online Directional Speech Enhancement Using Geometrically Constrained IVA]] — oGCAV-IVA: real-time online GCAV-IVA via autoregressive auxiliary variables
- [[sources/goto-2022-offline-iss-gciva|Goto, Ueda, Li, Yamada & Makino 2022: GC-IVA with Auxiliary Function Approach and Iterative Source Steering]] — GC-AuxIVA-ISS: inverse-free offline GC-IVA via ISS rank-1 updates; block-permutation prevention
- [[sources/goto-2022-iss-gciva|Goto, Ueda, Li, Yamada & Makino 2022: Accelerating Online GC-IVA with Iterative Source Steering]] — oGC-AuxIVA-ISS: inverse-free online GC-IVA via ISS rank-1 updates
- [[sources/hu-2023-gc-auxiva-iss-realistic|Hu & Chen 2023: The Performance of GC-AuxIVA-ISS Method in a Realistic Environment]] — real-recording validation of GC-AuxIVA-ISS; failure boundary under RT60 ≈ 600 ms + 70 dBA diffuse noise
- [[sources/guo-2023-iva-survey|Guo, Luo & Li 2023: IVA Survey]]
- [[sources/nishikori-2026-fast-multichannel-nmf-block-diagonal-scm-bss|Nishikori et al. 2026: Distributed FastMNMF for BSS]]
- [[sources/dong-2026-spatially-regularized-switching-iva|Dong et al. 2026: Spatially-Regularized Switching IVA with ISS]]
- [[sources/nakatani-2022-switching-iva|Nakatani et al. 2022: Switching IVA and Its Extension to Blind and Spatially Guided Convolutional Beamforming]] — the original swIVA/swCIVA: switching mechanism for few-microphone BSS with joint dereverberation
- [[sources/sawada-2019-bss-ilrma-review|Sawada et al. 2019: BSS/ILRMA Review]]
- [[sources/ruan-2024-speech-extraction-low-snr|Ruan, Liao, Chen & Lu 2024: Speech Extraction Under Extremely Low SNR Conditions]]
- [[sources/scheibler-2020-fast-independent-vector-extraction|Scheibler & Ono 2020: Fast Independent Vector Extraction]]
- [[sources/scheibler-2021-log-quadratically-penalized-iva|Scheibler 2021: Independent Vector Analysis via Log-Quadratically Penalized Quadratic Minimization]] — AuxIVA-IPA: joint update of one demixing filter plus adjustment of all others, solved globally via LQPQM; >2x faster convergence for 4-5 sources
- [[sources/ono-2011-stable-fast-update-rules-iva|Ono 2011: Stable and Fast Update Rules for Independent Vector Analysis Based on Auxiliary Function Technique]] — the founding AuxIVA paper: auxiliary-function (MM) updates with the IP rule, monotonic convergence, no step sizes
- [[sources/scheibler-2020-fast-stable-bss-rank-1-updates|Scheibler & Ono 2020: Fast and Stable Blind Source Separation with Rank-1 Updates]] — AuxIVA-ISS: inverse-free rank-1 updates cutting per-iteration cost to O(FM²N)
- [[sources/kang-2019-low-complexity-permutation-alignment|Kang, Yang & Yang 2019: A Low-Complexity Permutation Alignment Method for Frequency-Domain BSS]] — the per-bin-ICA alternative to IVA, with alignment cost largely eliminated
- [[sources/ansari-2023-ai-bss-survey|Ansari, Alatrany, Alnajjar et al. 2023: A Survey of AI Approaches in BSS]]
- [[sources/brendel-2020-spatially-guided-iva|Brendel, Haubner & Kellermann 2020: Spatially Guided Independent Vector Analysis]] — MAP generalization of IVA with a DOA-uncertainty-aware spatial prior; AuxIVA-speed MM updates; outer permutation resolution

