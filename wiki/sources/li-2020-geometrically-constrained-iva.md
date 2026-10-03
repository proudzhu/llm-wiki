---
type: source
created: 2026-10-04
updated: 2026-10-04
sources:
  - raw/papers/li-2020-geometrically-constrained-iva/full-text.md
  - https://doi.org/10.1109/ICASSP40776.2020.9053649
  - zotero://select/items/0_468U4XYN
tags:
  - speech-enhancement
  - blind-source-separation
  - independent-vector-analysis
  - beamforming
  - direction-of-arrival
---

# Li & Koishida 2020: Geometrically Constrained IVA for Directional Speech Enhancement

**Authors**: [[entities/li-li|Li Li]]¹, [[entities/kazuhito-koishida|Kazuhito Koishida]]²
**Affiliations**: ¹University of Tsukuba, Japan; ²Microsoft Corporation, USA
**Venue**: ICASSP 2020 (IEEE International Conference on Acoustics, Speech and Signal Processing)
**Year**: 2020
**Type**: Conference paper
**DOI**: [10.1109/ICASSP40776.2020.9053649](https://doi.org/10.1109/ICASSP40776.2020.9053649)
**Zotero**: [Open in Zotero](zotero://select/items/0_468U4XYN)

## Summary

This paper proposes **geometrically constrained independent vector analysis (GCIVA)**, which augments the IVA blind-separation objective with linear constraints on the far-field responses of the demixing filters, combining BSS separation performance with beamforming-style directional control. A convergence-guaranteed algorithm (**GCAV-IVA**) is derived in the auxiliary-function framework using vectorwise-coordinate-descent closed-form updates, inheriting AuxIVA's fast convergence and freedom from step-size tuning. In a dual-microphone system where the interference channel is nulled toward the (known) target DOA and the target channel is nulled toward an interference DOA estimated by a separate standard AuxIVA, the method outperforms both an MPDR beamformer and standard AuxIVA by a large margin in SDR and SIR.

## Problem Formulation

Consider the determined case: $I$ sources observed by $I$ microphones, with STFT-domain observations $\boldsymbol{x}(\omega,t) \in \mathbb{C}^I$ and estimated sources $\boldsymbol{y}(\omega,t) = \boldsymbol{W}(\omega)\,\boldsymbol{x}(\omega,t)$, where $\boldsymbol{W}(\omega)$ is the per-frequency demixing matrix.

IVA estimates the demixing matrices by minimizing

$$
J_{\mathrm{IVA}}(\mathcal{W}) = \sum_{j=1}^{J} \mathbb{E}\left[ G(\boldsymbol{y}_j(t)) \right] - \sum_{\omega=1}^{\Omega} \log|\det \boldsymbol{W}(\omega)|,
$$

where $\boldsymbol{y}_j(t)$ stacks all frequency bins of source $j$ and the contrast function $G$ follows a spherical multivariate distribution, $G(\boldsymbol{y}_j) = G_R(r_j)$ with $r_j(t) = \|\boldsymbol{y}_j(t)\|_2$.

**Geometric constraint.** The far-field response of the $j$-th demixing filter at direction $\theta$ is constrained via

$$
\mathcal{J}_c(\mathcal{W}) = \sum_{j=1}^{J} \lambda_j \sum_{\omega=1}^{\Omega} \left| \boldsymbol{w}_j^{\mathsf{H}}(\omega)\, \boldsymbol{d}_j(\omega,\theta) - c_j \right|^2,
$$

where $\boldsymbol{d}_j(\omega,\theta)$ is the steering vector, $c_j \geq 0$ the response target, and $\lambda_j \geq 0$ the constraint weight. This is the linear-constraint concept of the LCMV beamformer applied to BSS: $c_j = 1$ forces a delay-and-sum-like distortionless response toward $\theta$; a small $c_j \approx 0$ imposes a spatial **null** at $\theta$, which can also serve as a blocking matrix producing an interference/noise reference. The GCIVA objective is

$$
J(\mathcal{W}) = J_{\mathrm{IVA}}(\mathcal{W}) + \mathcal{J}_c(\mathcal{W}).
$$

**Motivation.** Plain IVA requires a post-hoc target-selection stage (typically DOA-based) and suffers from the block permutation problem between low and high frequency bands. Prior geometrically constrained IVA (Khan et al. 2015) constrained the Euclidean angle between the separation filter and the far-field steering vector, but required a relatively large microphone array and careful step-size tuning of its gradient-based updates — both barriers to practical adoption.

## Methodology

### GCAV-IVA: Auxiliary-Function Algorithm with Closed-Form Updates

Because the linear constraint terms break the solvability of the stationarity equation as a Hybrid Exact-Approximate joint Diagonalization (HEAD) problem, the paper combines the standard AuxIVA auxiliary function with the constraints and adopts the **vectorwise coordinate descent (VCD)** idea (Mitsui et al. 2018): the $\log|\det \boldsymbol{W}|$ term is arranged via cofactor expansion, using the adjugate matrix $\boldsymbol{B} = (\det \boldsymbol{W})\boldsymbol{W}^{-1}$ with $\det \boldsymbol{W} = \boldsymbol{w}_j^{\mathsf{H}}\boldsymbol{b}_j$.

With weighted covariance

$$
\boldsymbol{V}_j(\omega) = \mathbb{E}\left[ \frac{G_R'(r_j(t))}{r_j(t)}\, \boldsymbol{x}(\omega)\boldsymbol{x}^{\mathsf{H}}(\omega) \right]
\quad\text{and}\quad
\boldsymbol{D}_j = \boldsymbol{V}_j + \lambda_j \boldsymbol{d}_j \boldsymbol{d}_j^{\mathsf{H}},
$$

the per-row closed-form update is:

$$
\boldsymbol{u}_j = \boldsymbol{D}_j^{-1}\boldsymbol{W}^{-1}\boldsymbol{e}_j, \qquad
\hat{\boldsymbol{u}}_j = \lambda_j c_j \boldsymbol{D}_j^{-1}\boldsymbol{d}_j,
$$
$$
h_j = \boldsymbol{u}_j^{\mathsf{H}}\boldsymbol{D}_j\boldsymbol{u}_j, \qquad
\hat{h}_j = \boldsymbol{u}_j^{\mathsf{H}}\boldsymbol{D}_j\hat{\boldsymbol{u}}_j,
$$
$$
\boldsymbol{w}_j = \begin{cases}
\dfrac{1}{\sqrt{h_j}}\boldsymbol{u}_j + \hat{\boldsymbol{u}}_j & (\hat{h}_j = 0), \\[6pt]
\dfrac{\hat{h}_j}{2h_j}\left[-1 + \sqrt{1 + \dfrac{4h_j}{|\hat{h}_j|^2}}\right]\boldsymbol{u}_j + \hat{\boldsymbol{u}}_j & \text{otherwise}.
\end{cases}
$$

Properties:

- Reduces exactly to the standard AuxIVA update when $\lambda_j = 0$.
- Monotonic convergence guaranteed by the auxiliary-function (majorize-minimize) framework — **no step-size tuning**.
- Update structure is compatible with autoregressive covariance estimation, enabling online/low-latency extensions.

### Dual-Microphone System

![[raw/papers/li-2020-geometrically-constrained-iva/figures/81f73338ff5366fd508d3d8e398da7f92cee04f691b21eb6c8425ecf7f51975d.jpg|Basic system structure]]

*Figure 1: Dual-microphone GCAV-IVA system. The interference channel applies a null constraint toward the known target DOA $\theta_t$; the target channel applies a null toward an interference DOA estimated by a separate AuxIVA system.*

With only two microphones, null constraints ($c_j \approx 0$) are the practical choice. The system design is:

- **Interference channel**: null constraint toward the target DOA $\theta_t$ (assumed known), so the target is suppressed and this channel outputs an interference/noise reference.
- **Target channel**: three options evaluated —
  1. No constraint;
  2. Null at the oracle interference direction (2-speaker) or a dummy direction (1-speaker) — reference only;
  3. Null at the interference direction **estimated by a separate standard AuxIVA**.

For option 3, the interference DOA is read off the AuxIVA demixing filters' directivity patterns: since a BSS system behaves as a set of adaptive null-beamformers, its directional nulls point at the source directions. The DOA of each output is

$$
\hat{\theta}_j = \underset{\theta}{\operatorname{argmin}} \sum_{\omega=1}^{\Omega/2} \left| \boldsymbol{w}_j^{\mathsf{H}}(\omega)\, \boldsymbol{d}(\omega,\theta) \right|,
$$

and the interference DOA is the estimate farthest from the target: $\hat{\theta}_i = \operatorname{argmax}_j |\hat{\theta}_j - \theta_t|$.

## Experimental Setup

| Item | Setting |
|------|---------|
| Speech data | VCC2018, 4 speakers (2F/2M), 81 sentences each, 3–7 s |
| Array | 2 microphones, 5 cm spacing |
| RIRs | Image method; RT60 ≈ 200 ms (reflection coeff. 0.4) and 470 ms (0.8) |
| Diffuse noise | DEMAND (park, office, cafeteria, metro) |
| Test samples | 1920 (2-speaker), 960 (1-speaker); SNR in [−2, 6] dB (2-spk) and [0, 6] dB (1-spk) |
| Sampling / STFT | 16 kHz; 32 ms Hanning window, 16 ms shift |
| Baselines | MPDR beamformer (far-field steering vectors); AuxIVA ($G_R(r) = r$, best-channel output) |
| Proposed variants | GCAV-IVA systems (1)–(5), see below |
| Metrics | SDR, SIR, SAR (Vincent et al. 2006) |

**GCAV-IVA system variants** (Table 1; $\lambda_0 = 2$, $\lambda_1 = 10$ throughout):

| System | $\theta_i$ | $c_0$ | $c_1$ |
|--------|-----------|-------|-------|
| (1) | No constraint | — | — |
| (2) | Known (oracle) | 0 | 0 |
| (3) | Known (oracle) | 0.5 | 0.2 |
| (4) | Estimated by AuxIVA | 0 | 0 |
| (5) | Estimated by AuxIVA | 0.5 | 0.2 |

![[raw/papers/li-2020-geometrically-constrained-iva/figures/98520da0e1273291537a853321b7d6fe9b8ab445fadbf972780fb0da854dee4f.jpg|Configurations of sources and microphones]]

*Figure 2: Source and microphone configurations. "×" and "△" denote source positions for the 2-speaker and 1-speaker cases; red "×" is the target.*

## Results

### DOA Estimation (AuxIVA as DOA estimator)

![[raw/papers/li-2020-geometrically-constrained-iva/figures/0c5760b866c724ca75a0a25938dd4bd570cf2a1d993d953c803a248d9aa7fd18.jpg|DOA estimation results]]

*Figure 3: DOA histograms from AuxIVA after 3 update iterations under RT60 = 200 ms (upper) and 470 ms (bottom). Red lines: true DOAs.*

With only 3 AuxIVA iterations and a 5°-resolution grid over [0°, 180°], more than 60% of estimated DOAs fall within ±20° of the true direction.

### Speech Enhancement (Tables 2–3)

| Method | SDR (200 ms) | SIR (200 ms) | SDR (470 ms) | SIR (470 ms) |
|--------|-------------|--------------|--------------|--------------|
| Unprocessed | 1.46 | 1.61 | 0.78 | 1.47 |
| MPDR | 3.82 | 4.89 | 3.55 | 5.33 |
| AuxIVA (best channel) | 7.12 | 8.98 | 4.96 | 7.42 |
| GCAV-IVA(1), no target-channel constraint | 8.42 | 11.19 | 6.47 | 10.33 |
| GCAV-IVA(2), oracle DOA, null | 8.71 | 11.50 | 6.51 | 10.34 |
| GCAV-IVA(3), oracle DOA, tuned $c_j$ | 8.75 | 11.62 | 6.55 | 10.50 |
| GCAV-IVA(4), estimated DOA, null | 8.72 | 11.52 | 6.53 | 10.36 |
| **GCAV-IVA(5), estimated DOA, tuned $c_j$** | **8.80** | **11.69** | **6.57** | **10.50** |

*2-speaker case (SDR/SIR in dB; SAR omitted for brevity).*

| Method | SDR (200 ms) | SIR (200 ms) | SDR (470 ms) | SIR (470 ms) |
|--------|-------------|--------------|--------------|--------------|
| Unprocessed | 3.03 | 3.37 | 2.14 | 3.06 |
| MPDR | 1.29 | 2.79 | 2.14 | 4.03 |
| AuxIVA (best channel) | 6.04 | 8.00 | 4.07 | 6.65 |
| GCAV-IVA(1) | 7.00 | 10.20 | 5.47 | 10.20 |
| GCAV-IVA(2) | 7.37 | 10.33 | 5.60 | 10.30 |
| GCAV-IVA(3) | 7.32 | 10.40 | 5.55 | 10.36 |
| GCAV-IVA(4) | 7.39 | 10.27 | 5.71 | 10.41 |
| **GCAV-IVA(5)** | **7.43** | **10.41** | **5.73** | **10.56** |

*1-speaker case. MPDR is worse than unprocessed in SDR at RT60 = 200 ms.*

Key findings:

- GCAV-IVA exceeds MPDR on **all** criteria and AuxIVA on SDR/SIR by a large margin (e.g., +1.7 dB SDR / +2.7 dB SIR over AuxIVA in the 2-speaker, 200 ms case), even though AuxIVA is evaluated with oracle best-channel selection.
- Constraining **both** channels beats constraining only the interference channel — even in the 1-speaker case where no interference speaker exists.
- Carefully tuned $c_j$ (systems (3)/(5)) yields slightly higher SDR/SIR than pure nulls (systems (2)/(4)).
- The system using the **AuxIVA-estimated** interference DOA slightly **outperforms** the oracle-DOA system; the authors hypothesize that the AuxIVA null direction captures the direction containing the most statistically independent components, so suppressing it yields a higher SIR.

## Key Contributions

1. **GCIVA formulation**: combines the IVA objective with linear far-field response constraints on the demixing filters (the LCMV-style constraint family of Parra & Alvino's geometric source separation), enabling explicit spatial control of BSS outputs and potentially better handling of under/over-determined cases via blocking-matrix-style null channels.
2. **GCAV-IVA algorithm**: a convergence-guaranteed, closed-form update derived via the auxiliary-function approach with the vectorwise-coordinate-descent cofactor-expansion trick — retaining AuxIVA's fast convergence and requiring no step-size tuning (the two practical drawbacks of the earlier gradient-based geometrically constrained IVA of Khan et al. 2015), and reducing to AuxIVA when the constraint weights vanish.
3. **Dual-microphone system with BSS-based DOA estimation**: shows that a standard AuxIVA run (3 iterations) can serve as a DOA estimator via its directivity-pattern nulls, and that constraining both channels — target-channel null toward the estimated interference DOA — is the best configuration.
4. **Experimental validation**: on VCC2018 speech with image-method RIRs and DEMAND diffuse noise, the proposed system outperforms MPDR and AuxIVA by a large margin in SDR/SIR in both 2-speaker and 1-speaker cases at two reverberation levels.

## Related Concepts

- [[concepts/geometrically-constrained-iva|Geometrically Constrained IVA]] — the method introduced by this paper
- [[concepts/independent-vector-analysis|Independent Vector Analysis]] — base separation framework; GCAV-IVA reduces to AuxIVA at zero constraint weight
- [[concepts/blind-source-separation|Blind Source Separation]] — geometric constraints steer BSS outputs directionally
- [[concepts/spatial-regularization|Spatial Regularization]] — GCIVA as a constraint-based form of spatial guidance for BSS
- [[concepts/mpdr-beamformer|MPDR Beamformer]] — the conventional beamforming baseline
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]] — AuxIVA directivity-null DOA estimation
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] — application domain (dual-microphone enhancement)
- [[concepts/speech-enhancement|Speech Enhancement]] — application domain

## Related Synthesis

- (No dedicated synthesis page yet for "geometric constraints / spatial priors in BSS" — candidate for future synthesis alongside [[concepts/spatial-regularization|spatial regularization]] and spatially informed IVA lineages)
