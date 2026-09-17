---
type: source
created: 2026-09-17
updated: 2026-09-17
sources:
  - raw/papers/wang-2021-kronecker-adaptive-beamforming/full-text.txt
  - https://ieeexplore.ieee.org/document/9689635
  - zotero://select/items/0_47M4ZPJH
tags:
  - beamforming
  - microphone-arrays
  - kronecker-product
  - mvdr
  - adaptive-beamforming
---

# Wang, Huang, Cohen, Benesty & Chen 2021: Kronecker Product Adaptive Beamforming for Microphone Arrays

**Authors**: [[entities/xuehan-wang|Xuehan Wang]], [[entities/gongping-huang|Gongping Huang]], [[entities/israel-cohen|Israel Cohen]], [[entities/jacob-benesty|Jacob Benesty]], [[entities/jingdong-chen|Jingdong Chen]]
**Affiliations**: CIAIC and Shaanxi Provincial Key Laboratory of Artificial Intelligence, Northwestern Polytechnical University, Xi'an, China; Faculty of Electrical and Computer Engineering, Technion — Israel Institute of Technology, Haifa, Israel; INRS-EMT, University of Quebec, Montreal, Canada
**Venue**: APSIPA Annual Summit and Conference 2021 (APSIPA-ASC), Tokyo, Japan, Dec. 14–17, 2021, pp. 50–54
**Type**: Conference paper
**DOI**: [10.23919/APSIPAASC52927.2021.9689635](https://doi.org/10.23919/APSIPAASC52927.2021.9689635)
**Zotero**: [47M4ZPJH](zotero://select/items/0_47M4ZPJH)
**Funding**: National Key R&D Program of China 2018AAA0102200; NSFC Key Program 61831019

## Summary

This paper generalizes [[concepts/kronecker-product-beamforming|Kronecker product beamforming]] from special array geometries (linear, rectangular, cubic — which can be straightforwardly decomposed into subarrays) to **arbitrary three-dimensional array geometries**, by reformulating the beamforming filter as a **sum of $P$ Kronecker products** of shorter subfilters (following the Kronecker decomposition used in system identification). Based on this framework, an alternating iterative algorithm derives the **Kronecker MVDR (KMVDR) beamformer**, whose subfilters are each obtained by a closed-form MVDR-like update on a reduced-dimension problem. Simulations show that KMVDR outperforms the conventional [[concepts/mvdr-beamformer|MVDR beamformer]] in output SINR, especially with limited snapshots and dynamic interferers — this is the first Kronecker adaptive beamformer applicable to arbitrary geometries, later extended to $N$-way decompositions by [[sources/zhu-2025-kronecker-superdirective-beamforming|Zhu et al. 2025]].

## Problem Formulation

A microphone array with an arbitrary geometry in 3-D space has $M = M_1 M_2$ sensors, the $m$th located at $\mathbf{p}_m = [x_m\; y_m\; z_m]^T$. A far-field plane wave arrives from direction $\vartheta_s = (\theta_s, \varphi_s)$ (elevation, azimuth) with wavenumber $\mathbf{k}_s = \frac{\omega}{c}[\sin\theta_s \cos\varphi_s,\; \sin\theta_s \sin\varphi_s,\; \cos\theta_s]^T$ ($c = 340$ m/s). With desired signal, interference, and ambient noise co-existing, the frequency-domain observation is

$$\mathbf{y} = \mathbf{x} + \mathbf{u} + \mathbf{v} = \mathbf{d}(\vartheta_s) X + \mathbf{u} + \mathbf{v}$$

with the phase (steering) vector $\mathbf{d}(\vartheta_s) = [e^{-j\mathbf{k}_s^T \mathbf{p}_1},\; e^{-j\mathbf{k}_s^T \mathbf{p}_2},\; \dots,\; e^{-j\mathbf{k}_s^T \mathbf{p}_M}]^T$. The beamformer applies a spatial filter $Z = \mathbf{h}^H \mathbf{y}$, with output variance $\phi_Z = \mathbf{h}^H \boldsymbol{\Lambda}_{\mathbf{y}} \mathbf{h}$ where $\boldsymbol{\Lambda}_{\mathbf{y}} = E(\mathbf{y}\mathbf{y}^H)$, subject to the distortionless constraint $\mathbf{h}^H \mathbf{d}(\vartheta_s) = 1$. Minimizing the output variance under this constraint gives the classical [[concepts/mvdr-beamformer|MVDR beamformer]]:

$$\mathbf{h}_{\mathrm{MVDR}} = \frac{\boldsymbol{\Lambda}_{\mathbf{y}}^{-1} \mathbf{d}(\vartheta_s)}{\mathbf{d}^H(\vartheta_s) \boldsymbol{\Lambda}_{\mathbf{y}}^{-1} \mathbf{d}(\vartheta_s)}$$

The limitation motivating this work: existing Kronecker product beamformers were tied to geometries that decompose naturally into subarrays, restricting the framework to a small range of arrays.

## Methodology

### Sum-of-Kronecker-products filter representation

The key reformulation writes the length-$M$ beamforming filter as a **sum of $P$ Kronecker products** of subfilters of lengths $M_1$ and $M_2$:

$$\mathbf{h} = \sum_{p=1}^{P} \mathbf{h}_{1,p} \otimes \mathbf{h}_{2,p}$$

where $P$ ranges from $1$ to $\min(M_1, M_2)$. Unlike the single Kronecker product of earlier formulations (which required the physical array to decompose into subarrays), this sum representation can approximate *any* length-$M$ filter regardless of geometry — it is a property of the filter, not of the array — so the framework applies to any 3-D geometry as long as the sensor positions are known. Using the identity

$$\mathbf{h}_{1,p} \otimes \mathbf{h}_{2,p} = (\mathbf{h}_{1,p} \otimes \mathbf{I}_{M_2})\,\mathbf{h}_{2,p} = (\mathbf{I}_{M_1} \otimes \mathbf{h}_{2,p})\,\mathbf{h}_{1,p}$$

the filter becomes $\mathbf{h} = \sum_p \mathbf{H}_{1,p} \mathbf{h}_{2,p} = \sum_p \mathbf{H}_{2,p} \mathbf{h}_{1,p}$ with $\mathbf{H}_{1,p} = \mathbf{h}_{1,p} \otimes \mathbf{I}_{M_2}$ ($M \times M_2$) and $\mathbf{H}_{2,p} = \mathbf{I}_{M_1} \otimes \mathbf{h}_{2,p}$ ($M \times M_1$).

### Alternating MVDR optimization

With $\mathbf{h}_{1,p}$ fixed, the output becomes $Z = \mathbf{h}_2^H \mathbf{y}_1$ with stacked quantities $\mathbf{h}_2 = [\mathbf{h}_{2,1}^T, \dots, \mathbf{h}_{2,P}^T]^T$ and $\mathbf{y}_1 = [\mathbf{y}_{1,1}^T, \dots, \mathbf{y}_{1,P}^T]^T$ ($\mathbf{y}_{1,p} = \mathbf{H}_{1,p}^H \mathbf{y}$), so the output variance is $\phi_Z(\mathbf{h}_2 | \mathbf{h}_1) = \mathbf{h}_2^H \boldsymbol{\Lambda}_{\mathbf{y}_1} \mathbf{h}_2$ with the $PM_2 \times PM_2$ block covariance $[\boldsymbol{\Lambda}_{\mathbf{y}_1}]_{ij} = \mathbf{H}_{1,i}^H \boldsymbol{\Lambda}_{\mathbf{y}} \mathbf{H}_{1,j}$, and the distortionless constraint reduces to $\mathbf{h}_2^H \mathbf{d}_1(\vartheta_s) = 1$ with $\mathbf{d}_1(\vartheta_s) = [\mathbf{d}_{1,1}^T(\vartheta_s), \dots, \mathbf{d}_{1,P}^T(\vartheta_s)]^T$, $\mathbf{d}_{1,p}(\vartheta_s) = \mathbf{H}_{1,p}^H \mathbf{d}(\vartheta_s)$. The constrained minimum is again MVDR-like:

$$\mathbf{h}_2 = \frac{\boldsymbol{\Lambda}_{\mathbf{y}_1}^{-1} \mathbf{d}_1(\vartheta_s)}{\mathbf{d}_1^H(\vartheta_s) \boldsymbol{\Lambda}_{\mathbf{y}_1}^{-1} \mathbf{d}_1(\vartheta_s)}$$

With $\mathbf{h}_{2,p}$ fixed instead, the symmetric derivation gives $\mathbf{h}_1 = \boldsymbol{\Lambda}_{\mathbf{y}_2}^{-1} \mathbf{d}_2(\vartheta_s) / [\mathbf{d}_2^H(\vartheta_s) \boldsymbol{\Lambda}_{\mathbf{y}_2}^{-1} \mathbf{d}_2(\vartheta_s)]$ with the $PM_1 \times PM_1$ block covariance built from $\mathbf{H}_{2,p}$.

### Algorithm 1: KMVDR beamformer

1. Estimate $\boldsymbol{\Lambda}_{\mathbf{y}}$; initialize $\mathbf{h}_{2,p}$, $p = 1, \dots, P$.
2. Repeat until performance stops improving or the beamformer no longer changes:
   - compute $\mathbf{H}_{2,p}$; form $\boldsymbol{\Lambda}_{\mathbf{y}_2}$ and $\mathbf{d}_2(\vartheta_s)$; update $\mathbf{h}_1$;
   - compute $\mathbf{H}_{1,p}$; form $\boldsymbol{\Lambda}_{\mathbf{y}_1}$ and $\mathbf{d}_1(\vartheta_s)$; update $\mathbf{h}_2$.
3. Return $\mathbf{h}_{\mathrm{KMVDR}} = \sum_{p=1}^{P} \mathbf{h}_{1,p} \otimes \mathbf{h}_{2,p}$.

Each iteration inverts matrices of size $PM_1$ and $PM_2$ instead of $M$ — the same dimension-reduction mechanism later quantified for superdirective beamforming by [[sources/zhu-2025-kronecker-superdirective-beamforming|Zhu et al. 2025]].

## Experimental Setup

| Item | Value |
|:-----|:------|
| Array | Uniform linear, $M = 16$ microphones, spacing $\delta = 3$ cm, at $(x, 4, 2)$ with $x = 5 : 0.03 : 5.45$ |
| Room | $10 \times 8 \times 4$ m; image-method RIRs, $T_{60} \approx 90$ ms |
| Desired source | $(8, 4, 2)$; (1) stationary AR process from white noise through $1/(1 - 0.9z^{-1})$, or (2) clean speech at 48 kHz |
| Interference | White Gaussian; (1) static at $(5, 7, 2)$, or (2) dynamic moving $(5, 7, 2) \to (2, 7, 2)$ at 20 cm/s (3 m path, 3000 positions, RIR updated every 5 ms) |
| Ratios | iSNR = 20 dB; stationary case iSIR = 0 dB; speech case iSIR $\in \{-10, -5, 0, 5, 10, 15\}$ dB |
| KMVDR settings | $M_1 = M_2 = 4$, $P \in \{1, 2, 3, 4\}$, $n = 20$ iterations, initialization $\mathbf{h}_{2,p} = \mathbf{e}_p$ (unit vectors of $\mathbf{I}_{M_2}$) |
| Covariance estimation | Stationary case: averaging over $K$ snapshots; speech case: entropy-based VAD to identify unvoiced snapshots + recursive estimation |
| STFT | 256-point frames, 75% overlap, Kaiser window; beamformer designed per subband |
| Metric | Output SINR (oSINR) |

## Results

- **Snapshots** (Fig. 3, stationary source): oSINR of all beamformers increases with the number of snapshots $K$, since the covariance estimate improves; KMVDR consistently produces higher oSINR than MVDR for both static and dynamic interference. With a dynamic interferer, oSINR saturates — beyond a certain point more snapshots no longer help — and is lower than with the static interferer.
- **Input SIR** (Fig. 4, speech source): KMVDR outperforms MVDR across iSIR $\in \{-10, \dots, 15\}$ dB for both static and dynamic interference.
- **Rank effect**: the *best* oSINR is obtained with **$P = 1$** — the single Kronecker-product term — even though larger $P$ enlarges the representable filter family. The paper attributes the advantage of the Kronecker structure to the implicit regularization of the constrained (low-parameter) filter space under limited/corrupted covariance estimates.

## Key Contributions

1. **Arbitrary-geometry Kronecker beamforming framework** — reformulates the beamforming filter as a sum of $P$ Kronecker products of shorter subfilters, explicitly removing the geometry restriction of prior Kronecker product beamformers (limited to linear/rectangular/cubic arrays that decompose into subarrays); applicable to any 3-D geometry given sensor positions.
2. **KMVDR algorithm** — an alternating iterative optimization where each subfilter update is a closed-form MVDR-like solution on a reduced-dimension ($PM_1$- or $PM_2$-dimensional) covariance/constraint pair derived from the current estimate of the other subfilter.
3. **Simulation evidence of robustness** — KMVDR outperforms the conventional MVDR in output SINR under limited snapshots and dynamic interference, with the strongest performance at rank $P = 1$, indicating that the Kronecker structure regularizes the adaptive filter.

## Related Concepts

- [[concepts/kmvdr-beamformer|KMVDR Beamformer]]
- [[concepts/kronecker-product-beamforming|Kronecker Product Beamforming]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/voice-activity-detection|Voice Activity Detection]]
- [[concepts/image-source-method|Image Source Method]]

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
