---
type: source
created: 2026-10-04
updated: 2026-10-04
sources:
  - raw/papers/li-2020-online-gciva/full-text.md
  - https://doi.org/10.21437/Interspeech.2020-1484
  - zotero://select/items/0_8GP29RZG
tags:
  - speech-enhancement
  - blind-source-separation
  - independent-vector-analysis
  - online-processing
  - beamforming
  - direction-of-arrival
---

# Li, Koishida & Makino 2020: Online Directional Speech Enhancement Using Geometrically Constrained IVA

**Authors**: [[entities/li-li|Li Li]]¹, [[entities/kazuhito-koishida|Kazuhito Koishida]]², [[entities/shoji-makino|Shoji Makino]]¹
**Affiliations**: ¹University of Tsukuba, Japan; ²Microsoft Corporation, USA
**Venue**: Interspeech 2020 (21st Annual Conference of the International Speech Communication Association)
**Year**: 2020
**Type**: Conference paper
**DOI**: [10.21437/Interspeech.2020-1484](https://doi.org/10.21437/Interspeech.2020-1484)
**Zotero**: [Open in Zotero](zotero://select/items/0_8GP29RZG)

## Summary

This paper extends the offline **GCAV-IVA** algorithm (geometrically constrained IVA via the auxiliary-function approach and vectorwise coordinate descent, proposed by the first two authors at ICASSP 2020) to an **online algorithm (oGCAV-IVA)** by replacing the full-sample expectation in the auxiliary variable with an autoregressive recursion over short blocks, enabling frame-wise real-time updates. In a dual-microphone directional speech enhancement system whose interference channel is nulled toward the known target DOA, the online algorithm runs in real time (< 16 ms per 16 ms frame on a desktop CPU) and outperforms online AuxIVA in both spatially stationary and moving-interference conditions, including an underdetermined noisy scenario where online AuxIVA almost fails (SDR 6.86 dB vs. 1.70 dB).

## Problem Formulation

Determined BSS setting: $I$ sources observed by $I$ microphones, STFT-domain observations $\boldsymbol{x}(\omega,t) \in \mathbb{C}^I$, estimated sources $\boldsymbol{y}(\omega,t) = \boldsymbol{W}(\omega)\boldsymbol{x}(\omega,t)$. IVA estimates the demixing matrices by minimizing

$$
J_{\mathrm{IVA}}(\mathcal{W}) = \sum_{j=1}^{J} \mathbb{E}\left[ G(\boldsymbol{y}_j(t)) \right] - \sum_{\omega=1}^{\Omega} \log|\det \boldsymbol{W}(\omega)|,
$$

with the spherical contrast function $G(\boldsymbol{y}_j) = G_R(r_j)$, $r_j(t) = \|\boldsymbol{y}_j(t)\|_2$. The geometric constraint restricts the far-field response of the $j$-th demixing filter at direction $\theta$:

$$
J_c(\mathcal{W}) = \sum_{j=1}^{J} \lambda_j \sum_{\omega=1}^{\Omega} \left| \boldsymbol{w}_j^{\mathsf{H}}(\omega)\, \boldsymbol{d}_j(\omega,\theta) - c_j \right|^2,
$$

(the linear-constraint family of the LCMV beamformer; $c_j = 1$ distortionless response, $c_j \approx 0$ spatial null / blocking-matrix behavior), and the GCAV-IVA objective is $J(\mathcal{W}) = J_{\mathrm{IVA}}(\mathcal{W}) + J_c(\mathcal{W})$.

**Motivation for the online extension.** Offline and blockwise ICA/IVA approaches update parameters per block, incurring estimation delay that grows with block size; online approaches update per frame but typically suffer from insufficient statistics. The online blockwise compromise computes statistics from the current frame plus several past frames. Prior online AuxIVA (Taniguchi et al. 2014) showed that an autoregressive approximation of the auxiliary variable lets an auxiliary-function-based IVA work online with good performance — this paper applies the same idea to GCAV-IVA, motivated by real-time applications (speech recognition interfaces, hearing aids, teleconferencing).

## Methodology

### Offline GCAV-IVA Recap

In the auxiliary-function framework, the constraint terms (being linear in $\boldsymbol{w}_j$) are simply appended to the AuxIVA auxiliary function:

$$
J^{+}(\mathcal{W},\mathcal{V}) = \sum_{j=1}^{J}\sum_{\omega=1}^{\Omega} \left\{ \tfrac{1}{2}\boldsymbol{w}_j^{\mathsf{H}}(\omega)\boldsymbol{V}_j(\omega)\boldsymbol{w}_j(\omega) - \log|\det\boldsymbol{W}(\omega)| \right\} + J_c(\mathcal{W}),
$$

where the weighted covariance is $\boldsymbol{V}_j(\omega) = \mathbb{E}\left[\frac{G_R'(r_j(t))}{r_j(t)}\boldsymbol{x}(\omega)\boldsymbol{x}^{\mathsf{H}}(\omega)\right]$ (with the source model $G_R(r_j) = r_j$, $\boldsymbol{V}_j = \mathbb{E}[\boldsymbol{x}\boldsymbol{x}^{\mathsf{H}}/r_j]$). Using vectorwise-coordinate-descent cofactor expansion, the per-row update with $\boldsymbol{D}_j = \boldsymbol{V}_j + \lambda_j\boldsymbol{d}_j\boldsymbol{d}_j^{\mathsf{H}}$ is

$$
\boldsymbol{u}_j = \boldsymbol{D}_j^{-1}\boldsymbol{W}^{-1}\boldsymbol{e}_j, \quad
\hat{\boldsymbol{u}}_j = \lambda_j c_j \boldsymbol{D}_j^{-1}\boldsymbol{d}_j, \quad
h_j = \boldsymbol{u}_j^{\mathsf{H}}\boldsymbol{D}_j\boldsymbol{u}_j, \quad
\hat{h}_j = \boldsymbol{u}_j^{\mathsf{H}}\boldsymbol{D}_j\hat{\boldsymbol{u}}_j,
$$

$$
\boldsymbol{w}_j = \frac{\hat{h}_j}{2h_j}\left[-1 + \sqrt{1 + \frac{4h_j}{|\hat{h}_j|^2}}\right]\boldsymbol{u}_j + \hat{\boldsymbol{u}}_j
\quad \left(\boldsymbol{w}_j = \tfrac{1}{\sqrt{h_j}}\boldsymbol{u}_j + \hat{\boldsymbol{u}}_j \text{ if } \hat{h}_j = 0\right),
$$

which reduces exactly to AuxIVA when $\lambda_j = 0$.

### Online GCAV-IVA: Autoregressive Auxiliary Variables

Only the statistics $\boldsymbol{V}_j$ require all observed samples, so this is the sole point of modification for the online algorithm. The blockwise version over the latest $L$ frames,

$$
\boldsymbol{V}_j(\omega,t) = \frac{1}{L}\sum_{\tau=t-L+1}^{t} \frac{G_R'(r_j(t))}{r_j(t)}\boldsymbol{x}(\omega,t)\boldsymbol{x}^{\mathsf{H}}(\omega,t),
$$

either retains a large $L$ (costly) or uses insufficient statistics (degrading separation). The proposed autoregressive recursion reuses the previous value:

$$
\boldsymbol{V}_j(\omega,t) = \alpha\,\boldsymbol{V}_j(\omega,t-L) + (1-\alpha)\frac{1}{L}\sum_{\tau=t-L+1}^{t} \frac{G_R'(r_j(t))}{r_j(t)}\boldsymbol{x}(\omega,t)\boldsymbol{x}^{\mathsf{H}}(\omega,t),
$$

with forgetting factor $0 \le \alpha < 1$ ($\alpha = 0$ recovers the blockwise version). A large $\alpha$ keeps long-range statistics (good for fixed sources); a small $\alpha$ reacts quickly to source movement via the blockwise term.

### Dual-Microphone System

Two microphones, target DOA $\theta_t$ known, null constraints ($c_j \approx 0$). Three system variants by interference DOA $\theta_i$ availability:

- **(a)** unknown — no constraint on the target channel (constraint only on the interference channel);
- **(b)** known — null the target channel toward the true interference DOA;
- **(c)** estimated — a separate **online AuxIVA** runs in parallel; since a BSS system behaves as a set of adaptive null-beamformers, its directivity nulls reveal the source directions:

$$
\hat{\theta}_j = \operatorname{argmin}_\theta \sum_{\omega=1}^{\Omega/2}\left|\boldsymbol{w}_j^{\mathsf{H}}(\omega)\boldsymbol{d}(\omega,\theta)\right|, \qquad
\hat{\theta}_i = \operatorname*{argmax}_{j \in \{1,2\}}\left|\hat{\theta}_j - \theta_t\right|.
$$

![[raw/papers/li-2020-online-gciva/figures/462ee93183111e074d905780a2d2da39f73a53f8b8349b9089fed4ae36ced85b.jpg|Structure of the proposed dual-microphone system with DOA estimation (system c)]]
*Figure 1: Structure of the proposed system with DOA estimation (system (c)). A separate online AuxIVA estimates the interference DOA from its directivity-pattern nulls; the target channel of the GCAV-IVA path is then nulled toward it.*

## Experimental Setup

| Item | Setting |
|------|---------|
| Speech data | VCC2018, 4 speakers (2F/2M), 81 sentences each; ~30 s single-speaker concatenations |
| Array | 2 microphones, 5 cm spacing |
| Conditions | (i) 2 spatially fixed sources: 5 DOA pairs, e.g. (30°, 110°), (70°, 100°), (150°, 60°), (40°, 90°), (90°, 150°) (target, interference); (ii) fixed target (30°/90°/140°/150°) + moving interference (120° → ~80°) |
| RIRs | Image method; RT60 = 78 ms and 200 ms (wall reflection coefficients 0.2 / 0.4) |
| Noise | DEMAND diffuse noise (park, office, cafeteria, metro); datasets "S+I" (without) and "S+I+N" (with); input SDR ≈ [−3, 0] dB |
| Mixing | Target-to-interference ratio 0 dB |
| STFT | 16 kHz sampling, 32 ms Hanning window, 16 ms shift |
| Algorithm params | $L = 1$; forgetting factor $\alpha = 0.96$ (both oGCAV-IVA and oAuxIVA); $\lambda = 1$ (both channels, or interference channel only in system (a)); $c = 0.5$ (target channel), $c = 0.2$ (interference channel); 5 iterations over first 5 frames for initialization, then 2 iterations per frame |
| DOA estimation | Grid [0°, 180°], 5° interval |
| Metrics | SDR, SIR, SAR (evaluated per second, averaged over 30 s); GCAV-IVA evaluated at the target channel, AuxIVA best-channel (oracle selection) |
| Hardware | Intel Core i7-7800X CPU @ 3.5 GHz |

![[raw/papers/li-2020-online-gciva/figures/dbce3b8ad24a653163785676fbb112cbad5c6c9a13e7d7598242c5815bb2cdac.jpg|Configurations of microphones and fixed sources]]
*Figure 2: Configurations of microphones and a pair of fixed sources; red and blue marks denote target and interference positions.*

![[raw/papers/li-2020-online-gciva/figures/fda88a90aa5dfe7c79a9fabd4657dabb4ace4eedc6b0623fc57c8412d9f71f6c.jpg|Configurations of sources and microphones for the moving-interference condition]]
*Figure 3: Configurations of sources and microphones for the spatially nonstationary condition; red mark and blue line denote the fixed target source and the trace of the moving interference.*

## Results

**Spatially stationary condition** (Table 1): oGCAV-IVA outperforms oAuxIVA in all variants and both noise conditions. Notably, system (c) with estimated interference DOA beats system (b) with the *true* DOA by more than 4 dB — the AuxIVA-derived DOA estimate points at the direction containing the most statistically independent components, and suppressing that direction yields higher SIR. In the underdetermined "S+I+N" condition (determined assumption violated), oAuxIVA nearly fails (SDR 1.70 dB) while the geometrically constrained methods still achieve ≈ 6.8 dB SDR.

| Method | S+I SDR | S+I SIR | S+I SAR | S+I+N SDR | S+I+N SIR | S+I+N SAR |
|--------|---------|---------|---------|-----------|-----------|-----------|
| oAuxIVA | 8.37 | 12.57 | 12.06 | 1.70 | 4.06 | 8.81 |
| oGCAV-IVA (a) | 11.77 | 15.72 | 14.51 | 6.07 | 8.48 | 12.06 |
| oGCAV-IVA (b) | 10.03 | 12.50 | 14.96 | 4.29 | 5.81 | 12.86 |
| oGCAV-IVA (c) | **14.19** | **18.40** | **16.73** | **6.86** | **9.18** | **13.60** |

**Spatially nonstationary condition** (Table 2): oGCAV-IVA again outperforms oAuxIVA (+1.5 dB SDR without noise, +2.9 dB with noise). Unlike the fixed case, the unconstrained system (a) beats the DOA-estimating system (c) — DOA estimation accuracy degrades for moving sources, and an inappropriate constraint then hurts performance.

| Method | S+I SDR | S+I SIR | S+I SAR | S+I+N SDR | S+I+N SIR | S+I+N SAR |
|--------|---------|---------|---------|-----------|-----------|-----------|
| oAuxIVA | 3.77 | 6.51 | 9.34 | 0.12 | 1.96 | 8.13 |
| oGCAV-IVA (a) | **6.83** | **9.21** | 11.66 | **3.51** | **5.33** | 10.50 |
| oGCAV-IVA (c) | 5.36 | 6.90 | **12.33** | 3.05 | 4.42 | **11.41** |

![[raw/papers/li-2020-online-gciva/figures/0c3a017539ea62d22b466cfb4afa997e5859191dba565d69db8d7ca98cf56675.jpg|Successful example of interference DOA estimation for a moving source]]
![[raw/papers/li-2020-online-gciva/figures/1e64ea6a03b580b71e0a854f77be5f1985fc83d1119abf530f4bcee66d5ddc6b.jpg|Failure example of interference DOA estimation for a moving source]]
*Figure 4: Examples of estimated DOA for the moving source — a successful case (top) and a failure case (bottom); failed DOA estimates produce inappropriate constraints that degrade performance.*

**Real-time capability.** Average per-frame computation was < 16 ms (the window shift): ≈ 5 ms for systems (a)/(b) and ≈ 15 ms for system (c) (which includes the parallel online AuxIVA), confirming real-time operation.

## Key Contributions

1. **Online GCAV-IVA (oGCAV-IVA)**: extends the offline geometrically constrained IVA to frame-wise online updates via an autoregressive approximation of the auxiliary variables (forgetting factor $\alpha$), inheriting the auxiliary-function approach's convergence guarantees and step-size-free updates while achieving real-time computation (< 16 ms/frame on a desktop CPU).
2. **Dual-microphone system with three interference-DOA variants**: (a) no target-channel constraint, (b) known interference DOA, (c) interference DOA estimated from the directivity-pattern nulls of a separate parallel online AuxIVA.
3. **Empirical validation in stationary and nonstationary conditions**: consistent gains over online AuxIVA (up to +5.8 dB SDR in the fixed case; +1.5–2.9 dB with moving interference), robustness in an underdetermined noisy scenario (6.86 vs. 1.70 dB SDR), and the counterintuitive finding that the estimated DOA (system (c)) outperforms the true DOA (system (b)) by > 4 dB for fixed sources — while the reverse holds for moving sources due to DOA-estimation errors.

## Related Concepts

- [[concepts/geometrically-constrained-iva|Geometrically Constrained IVA]]
- [[concepts/online-iva|Online IVA]]
- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/adaptive-blocking-matrix|Adaptive Blocking Matrix]]
- [[concepts/lcmv-beamformer|LCMV Beamformer]]

## Related Synthesis

- (No dedicated synthesis page yet for "geometric constraints / spatial priors in BSS" or "online BSS" — candidate for future synthesis alongside [[concepts/spatial-regularization|spatial regularization]], [[concepts/online-iva|online IVA]], and the spatially informed IVA lineages)
