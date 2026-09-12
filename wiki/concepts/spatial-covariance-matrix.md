---
type: concept
created: 2026-04-29
updated: 2026-09-12
sources:
  - raw/papers/zhang-2026-feedback-path-mitigation-mcanc/full-text.md
  - raw/papers/grinstein-2025-tiny-param-mwf/full-text.md
  - raw/papers/li-2022-embedding-beamforming/full-text.md
  - raw/papers/zhang-2021-adl-mvdr/full-text.md
tags:
  - array-processing
  - spatial-statistics
  - speech-enhancement
  - active-noise-control
---

# Spatial Covariance Matrix

The **Spatial Covariance Matrix (SCM)** captures the second-order statistics of multi-channel signals across microphone arrays.

## Definition

For a multi-channel signal $x \in \mathbb{C}^M$:

$$\Phi_x = \mathbb{E}[xx^H]$$

## Role in Speech Enhancement

- **Clean-speech SCM** ($\Phi_x$): Characterizes spatial properties of target speech
- **Noise SCM** ($\Phi_n$): Characterizes spatial properties of interference/noise
- Used in MWF, MVDR, GEV beamformer, and VSLF weight computation

## Estimation

SCMs can be estimated via:
- Sample covariance from noise-only periods
- DNN-based prediction (e.g., HVSF architecture)
- Voice activity detection-guided updates
- **Mask-derived estimates with learned smoothing** ([[sources/grinstein-2025-tiny-param-mwf|Grinstein et al. 2025]]): a tiny DNN estimates a multi-channel complex T-F mask $\mathbf{G}$; the masked observation $\hat{\mathbf{S}}_0=\mathbf{G}\odot\mathbf{Y}$ and its complement $\hat{\mathbf{N}}_0=\mathbf{Y}-\hat{\mathbf{S}}_0$ feed per-bin outer products accumulated by exponential smoothing, $\Phi_{ss}[t,w]=(1-\alpha_{ss}[w])\Phi_{ss}[t-1,w]+\alpha_{ss}[w]\hat{\mathbf{S}}_0\hat{\mathbf{S}}_0^H$ (likewise for $\Phi_{nn}$), with the smoothing speeds $\alpha_{ss}, \alpha_{nn}$ *learned per frequency* during end-to-end training and fixed at inference. The learned values satisfy $\alpha_{ss}>\alpha_{nn}$, recovering the classical assumption that speech statistics change faster than noise, and trained frequency-dependent smoothing marginally beat SPP-driven and fixed alternatives.

## SCM Reconstruction via Normalized Decomposition

Liu et al. (2026) propose decomposing the **normalized** SCM as a linear combination of predefined coherence matrices:

$$\Gamma_y = \sum_{i=1}^{I} \psi_i \Gamma_i + \psi_R \Gamma_d + \psi_V I_M$$

where $\psi_i, \psi_R, \psi_V$ are **variance ratios** (non-negative, sum to 1), $\Gamma_i$ are source coherence matrices (from RTF or DOA), $\Gamma_d$ is the diffuse-field coherence matrix, and $I_M$ is the identity matrix. The variance ratios are estimated via a lightweight multiplicative update algorithm with KL-divergence regularization, achieving $\mathcal{O}(M^2(I+2))$ complexity.

### Key Insight

Normalization by trace transforms the SCM estimation problem from estimating absolute variances to estimating **relative variance ratios** — a simpler constrained optimization with non-negativity and unity-sum constraints, solvable by multiplicative updates.

## Implicit Embeddings vs. Explicit SCM (Li et al. 2022)

[[sources/li-2022-embedding-beamforming|Li et al. 2022]]'s [[concepts/eabnet|EaBNet]] provides a controlled head-to-head between explicit SCM usage and a purely learned spatial representation: their EaBNet* variant estimates speech/noise complex masks, computes the corresponding SCMs, and concatenates them as input to the beamforming network — while the main EaBNet replaces this entire stage with a learned 3-D spectral-spatial embedding tensor. The implicit embedding *wins* (avg. PESQ 3.52 vs. 3.46; ESTOI 85.91% vs. 84.67%). The authors' explanations: the SCM is sparse and often redundant/unnecessary for spectral-temporal representation, is less robust in real scenarios than a compact embedding, and — being second-order statistics — cannot capture the higher-order spatial statistics the data-driven embedding can potentially learn. This motivates rethinking the role of signal-theory operations (SCM computation and inversion) inside end-to-end neural beamformers.

## Covariance Subtraction for Component Isolation

An SCM is normally *decomposed* into target and noise contributions under the assumption that the components are uncorrelated. In system identification the same additivity is used in reverse, as an operator that isolates one component by differencing two measured SCMs. [[concepts/covariance-subtraction|Covariance subtraction]] exploits this: with a primary-only measurement $\boldsymbol{\Phi}^{(\mathrm{Pri})}$ and a total measurement $\boldsymbol{\Phi}^{(\mathrm{Tot})}$ (secondary loudspeakers probing, primary still present),

$$
\boldsymbol{\Phi}^{(\mathrm{Sec})} = \boldsymbol{\Phi}^{(\mathrm{Tot})} - \boldsymbol{\Phi}^{(\mathrm{Pri})},
$$

which recovers the secondary-only contribution exactly when the components are mutually independent — **without ever silencing the primary source**. [[sources/zhang-2026-feedback-path-mitigation-mcanc|Zhang et al. 2026]] use the resulting auto-covariance $\boldsymbol{\Phi}_{\mathrm{RR}}^{(\mathrm{Sec})}$ and cross-covariance $\boldsymbol{\Phi}_{\mathrm{FR}}^{(\mathrm{Sec})}$ between two microphone groups to estimate a [[concepts/relative-transfer-matrix|Relative Transfer Matrix]] for acoustic-feedback neutralization in multichannel ANC. Their ablation shows the subtraction is decisive rather than cosmetic: estimating the same matrix from total-field SCMs collapses noise reduction to ≈ −2 dB, because the persistent primary field dominates the pseudo-inverse $\boldsymbol{\Phi}_{\mathrm{FR}}^{(\mathrm{Sec})^{\dagger}}$.

## Frame-Level SCMs via cRF, Inverted by GRU Networks (Zhang et al. 2021)

[[sources/zhang-2021-adl-mvdr|Zhang et al. 2021]]'s [[concepts/adl-mvdr|ADL-MVDR]] estimates **frame-level** SCMs — deliberately *not* summing over time, so each frame keeps its own statistics — from complex ratio filters (3×3 cRF) applied to the multi-channel mixture, with the cRF center mask used for normalization. The inversion of the noise SCM and the PCA of the speech SCM (steering-vector extraction) are then replaced by two GRU networks that recursively accumulate covariance information across frames without heuristic updating factors. This resolves the numerical instability of closed-form matrix inversion during joint NN training. Read together with [[sources/li-2022-embedding-beamforming|Li et al. 2022]]'s EaBNet finding (explicit SCM *computation* reinserted into an all-neural beamformer hurts), ADL-MVDR's success suggests the unstable or limiting stage is the closed-form inversion/eigendecomposition — not the SCM as an input representation, which ADL-MVDR retains and exploits.

## Related Concepts

- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/mpdr-beamformer|MPDR Beamformer]]
- [[concepts/variable-span-linear-filter|Variable Span Linear Filter]]
- [[concepts/spatial-coherence|Spatial Coherence]]
- [[concepts/variance-ratio-estimation|Variance Ratio Estimation]]
- [[concepts/diagonal-loading|Diagonal Loading]]
- [[concepts/condition-number|Condition Number]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/virtual-microphone-estimation|Virtual Microphone Estimation]]
- [[concepts/distributed-binaural-speech-enhancement|Distributed Binaural Speech Enhancement]]
- [[concepts/asymmetric-stft|Asymmetric STFT]]
- [[concepts/rank-constrained-spatial-covariance-matrix-estimation|Rank-Constrained Spatial Covariance Matrix Estimation (RCSCME)]]
- [[concepts/covariance-subtraction|Covariance Subtraction]] — using SCM additivity as a subtraction operator for system identification
- [[concepts/relative-transfer-matrix|Relative Transfer Matrix (ReTM)]] — estimated from primary-only vs total-field SCM differences
- [[concepts/neuralpmwf|NeuralPMWF]] — mask-derived SCMs with learned frequency-dependent exponential smoothing
- [[concepts/eabnet|EaBNet]] — learned spectral-spatial embedding that empirically beats explicit SCM computation
- [[concepts/adl-mvdr|ADL-MVDR]] — frame-level cRF-derived SCMs whose inversion/PCA is replaced by GRU networks

## Related Sources

- [[sources/oviste-2026-neural-vslf-speech-enhancement|Oviste 2026: Neural VSLF for Speech Enhancement]]
- [[sources/liu-2026-scm-reconstruction-speech-enhancement|Liu 2026: SCM Reconstruction for Speech Enhancement]]
- [[sources/mittal-2026-adaptive-diagonal-loading-beamforming|Mittal et al. 2026: Adaptive Diagonal Loading for Norm Constrained Beamforming]]
- [[sources/lee-2026-spatial-magnifier-spatial-upsampling|Lee et al. 2026: Spatial-Magnifier]]
- [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|Benslimane et al. 2026: RT-Tango]]
- [[sources/ishikawa-2025-real-time-speech-extraction|Ishikawa et al. 2025: Real-Time RCSCME-based Speech Extraction]]
- [[sources/zhang-2026-feedback-path-mitigation-mcanc|Zhang, Abhayapala, Samarasinghe & Bastine 2026: Acoustic Feedback Path Mitigation for Multichannel ANC]] — SCMs over two microphone groups, differenced to isolate the secondary-only field for feedback neutralization
- [[sources/grinstein-2025-tiny-param-mwf|Grinstein et al. 2025: Controlling the PMWF Using a Tiny Neural Network]] — mask-derived SCM estimation with learned per-frequency exponential smoothing
- [[sources/li-2022-embedding-beamforming|Li et al. 2022: Embedding and Beamforming]] — implicit spectral-spatial embedding empirically beats explicit SCM computation in end-to-end neural beamforming
- [[sources/zhang-2021-adl-mvdr|Zhang et al. 2021: ADL-MVDR]] — frame-level SCMs estimated from cRF filters; inversion and PCA replaced by GRU networks
