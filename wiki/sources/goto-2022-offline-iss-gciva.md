---
type: source
created: 2026-10-04
updated: 2026-10-04
sources:
  - raw/papers/goto-2022-offline-iss-gciva/full-text.md
  - https://doi.org/10.23919/EUSIPCO55093.2022.9909912
  - zotero://select/items/0_M4TBPPAI
tags:
  - blind-source-separation
  - independent-vector-analysis
  - speech-enhancement
  - computational-efficiency
  - direction-of-arrival
---

# Goto, Ueda, Li, Yamada & Makino 2022: GC-IVA with Auxiliary Function Approach and Iterative Source Steering

**Authors**: [[entities/kana-goto|Kana Goto]]¹, [[entities/tetsuya-ueda|Tetsuya Ueda]]¹, [[entities/li-li|Li Li]]², [[entities/takeshi-yamada|Takeshi Yamada]]¹, [[entities/shoji-makino|Shoji Makino]]³
**Affiliations**: ¹University of Tsukuba, Japan; ²NTT Communication Science Laboratories, Nippon Telegraph and Telephone Corporation, Japan; ³Waseda University, Japan
**Venue**: 30th European Signal Processing Conference (EUSIPCO 2022)
**Year**: 2022
**Type**: Conference paper
**DOI**: [10.23919/EUSIPCO55093.2022.9909912](https://doi.org/10.23919/EUSIPCO55093.2022.9909912)
**Zotero**: [Open in Zotero](zotero://select/items/0_M4TBPPAI)

## Summary

This paper derives **GC-AuxIVA-ISS**, an offline (batch) algorithm for [[concepts/geometrically-constrained-iva|geometrically constrained IVA]] that replaces the vectorwise-coordinate-descent (VCD) updates of GCAV-IVA — which require a per-source, per-frequency matrix inversion — with [[concepts/iterative-source-steering|iterative source steering (ISS)]] rank-1 updates, folding the geometric constraints directly into the closed-form ISS coefficients. The result is inverse-free, numerically stable, and retains the auxiliary-function advantages (monotonic convergence, no step-size tuning). On 2–4 source determined separation with oracle DOAs, GC-AuxIVA-ISS matches or exceeds GC-AuxIVA-VCD in SDR/SIR, achieves 100% output-order accuracy, avoids the block permutation failure of plain AuxIVA-ISS, and cuts per-iteration runtime by 34–53% (less than half of VCD at 4 channels). This is the offline predecessor that the authors' online extension ([[sources/goto-2022-iss-gciva|Goto et al. 2022, APSIPA ASC]]) builds on.

## Problem Formulation

Determined BSS setting: $J$ sources observed by $I = J$ microphones; STFT observations $\boldsymbol{x}_{fn} \in \mathbb{C}^I$ are separated by $\boldsymbol{y}_{fn} = \boldsymbol{W}_f \boldsymbol{x}_{fn}$ with demixing matrix $\boldsymbol{W}_f = [\boldsymbol{w}_{1f}, \dots, \boldsymbol{w}_{Jf}]^{\mathsf{H}}$. IVA minimizes the negative log-likelihood

$$
\mathcal{L}_{\mathrm{IVA}}(\mathcal{W}) = \sum_{j=1}^{J} \mathbb{E}\left[ G(\boldsymbol{y}_{jn}) \right] - \sum_{f=1}^{F} \log|\det \boldsymbol{W}_f|,
$$

with the spherical contrast function $G(\boldsymbol{y}_{jn}) = G_R(r_{jn})$, $r_{jn} = \|\boldsymbol{y}_{jn}\|_2$. The auxiliary-function upper bound introduces the weighted covariance $\boldsymbol{\Sigma}_{jf} = \sum_n \varphi(r_{jn})\, \boldsymbol{x}_{fn}\boldsymbol{x}_{fn}^{\mathsf{H}}$, $\varphi(r) = G_R'(r)/r$. Geometric constraints restrict the far-field response of the demixing filters over a set of directions $\Theta$:

$$
\mathcal{L}_{\mathrm{GC}}(\mathcal{W}) = \sum_{j=1}^{J} \sum_{\theta \in \Theta} \lambda_{j\theta} \sum_{f=1}^{F} \left| \boldsymbol{w}_{jf}^{\mathsf{H}} \boldsymbol{d}_{f\theta} - c_{j\theta} \right|^2,
$$

where $\boldsymbol{d}_{f\theta}$ is the steering vector toward $\theta$, $c_{j\theta} = 1$ forces a distortionless (delay-and-sum) response and small $c_{j\theta}$ a spatial null. The GCAV-IVA objective is $\mathcal{L}(\boldsymbol{\Sigma}, \mathcal{W}) = \mathcal{L}_{\mathrm{AuxIVA}}(\boldsymbol{\Sigma}, \mathcal{W}) + \mathcal{L}_{\mathrm{GC}}(\mathcal{W})$.

**Motivation.** The GCAV-IVA update rules require $\boldsymbol{D}_{jf}^{-1}$ with $\boldsymbol{D}_{jf} = \boldsymbol{\Sigma}_{jf} + \sum_\theta \lambda_{j\theta} \boldsymbol{d}_{f\theta}\boldsymbol{d}_{f\theta}^{\mathsf{H}}$ for every source, frequency, and iteration — computationally expensive ($O(M^3)$) and a source of numerical instability. ISS (Scheibler & Ono 2020) removed the inversions for plain AuxIVA; the question is whether the linear geometric constraints can survive inside the ISS closed-form updates.

## Methodology

### GC-AuxIVA-ISS: Rank-1 Updates with Constraints in the Coefficients

Instead of updating one row of $\boldsymbol{W}_f$ at a time (VCD), ISS performs a rank-1 update of the whole demixing matrix per source:

$$
\boldsymbol{W}_f \leftarrow \boldsymbol{W}_f - \boldsymbol{v}_{jf} \boldsymbol{w}_{jf}^{\mathsf{H}},
$$

with $\boldsymbol{v}_{jf} \in \mathbb{C}^I$ the new unknown. Substituting the rank-1 update into the GCAV-IVA objective and setting the partial derivatives w.r.t. $v_{ijf}^{*}$ to zero yields closed-form updates.

**Off-diagonal elements ($i \neq j$):**

$$
v_{ijf} = \frac{\sum_n \varphi(r_{in})\, y_{in} y_{jn}^{*} + 2 \sum_{\theta \in \Theta} \lambda_{i\theta}\, g_{jf\theta}^{*} (g_{if\theta} - c_{i\theta})}{\sum_n \varphi(r_{in})\, |y_{jn}|^2 + 2 \sum_{\theta \in \Theta} \lambda_{i\theta} |g_{jf\theta}|^2},
$$

where $g_{jf\theta} = \boldsymbol{w}_{jf}^{\mathsf{H}} \boldsymbol{d}_{f\theta}$ is the current far-field response — the geometric terms enter the numerator (pulling the response toward $c_{i\theta}$) and the denominator (normalization) directly.

**Diagonal element ($i = j$):** with

$$
\alpha_j = \sum_n \varphi(r_{jn})\, |y_{jn}|^2 + 2 \sum_{\theta \in \Theta} \lambda_{j\theta} |g_{jf\theta}|^2, \qquad
\beta_j = \sum_{\theta \in \Theta} \lambda_{j\theta} c_{j\theta} g_{jf\theta},
$$

the stationarity condition splits on $\beta_j$ (the $\mp$ sign ambiguity is resolved in the paper's Appendix A by taking the positive root, which yields the smaller objective):

$$
v_{jjf} = \begin{cases} 1 - \alpha_j^{-1/2} & (\beta_j = 0), \\[4pt] 1 - \beta_j^{*} \dfrac{|\beta_j| + \sqrt{|\beta_j|^2 + \alpha_j}}{\alpha_j\, |\beta_j|} & (\beta_j \neq 0). \end{cases}
$$

(The online extension of [[sources/goto-2022-iss-gciva|Goto et al. 2022 (APSIPA)]] renames these scalars $p_{jfn}$, $q_{jfn}$ and adds the frame index.)

After computing $\boldsymbol{v}_{jf}$, the outputs and responses are updated by the same rank-1 algebra,

$$
\boldsymbol{y}_{n} \leftarrow \boldsymbol{y}_{n} - \boldsymbol{v}_{j} y_{jn}, \qquad
\boldsymbol{w}_{i}^{\mathsf{H}} \boldsymbol{d}_{\theta} \leftarrow \boldsymbol{w}_{i}^{\mathsf{H}} \boldsymbol{d}_{\theta} - v_{ij}\, \boldsymbol{w}_{j}^{\mathsf{H}} \boldsymbol{d}_{\theta},
$$

both purely scalar operations — no matrix inversion appears anywhere, and the responses $g_{jf\theta}$ never need to be recomputed from $\boldsymbol{W}_f$.

### Constraint Designs

With $\Theta$ containing all $J$ source DOAs and a $J \times J$ constraint-weight matrix $\boldsymbol{\Lambda}$ (entry $(j,\theta)$ = $\lambda_{j\theta}$), three designs are compared, each with a single tuned weight $\lambda$:

| Design | $c_{j\theta}$ setting | $\boldsymbol{\Lambda}$ |
|--------|----------------------|------------------------|
| UR (unit response) | $c = 1$ at each channel's own target DOA (diagonal) | $\lambda \mathbf{I}$ |
| Null | $c = 0$ at all interference DOAs (off-diagonal) | $\lambda(\mathbf{J} - \mathbf{I})$ |
| Double | both UR and null | $\lambda \mathbf{J}$ |

($\mathbf{J}$ = all-ones matrix.) The optimal $\lambda$ differs drastically between algorithms: e.g., in the 2-source null-constraint condition, GC-AuxIVA-VCD uses $\lambda = 0.8$ while GC-AuxIVA-ISS needs $\lambda = 80000$ — the ISS parameterization rescales the constraint weight.

## Experimental Setup

| Item | Setting |
|------|---------|
| Speech data | ATR Japanese Speech Database, 6 speakers (3M/3F); 48 random mixtures per source count |
| Sources / mics | 2, 3, and 4 sources; mic count = source count, 2 cm spacing |
| DOAs | 2 src: 20°, 70°; 3 src: +120°; 4 src: +170° (Θ = all source DOAs, **assumed known**) |
| RIRs | Simulated with pyroomacoustics; RT60 ≈ 100 ms and 300 ms |
| STFT | 16 kHz; Hanning window, 512 samples (32 ms) / 256 samples (16 ms) shift |
| Algorithm params | 50 iterations; $\lambda$ tuned per method/condition from several values |
| Compared methods | AuxIVA-ISS (Scheibler & Ono 2020), GC-AuxIVA-VCD (= GCAV-IVA, Li & Koishida 2020), GC-AuxIVA-ISS (proposed) |
| Metrics | SDR, SIR (Vincent et al. 2006); output-order accuracy (best permutation by SIR) |

![[raw/papers/goto-2022-offline-iss-gciva/figures/3357f071120b1dac51efcc5cc1ffc980f49933a2886ae9d39d5f2aef380f27f7.jpg|Layout of sound sources and microphones]]
*Figure 1: Layout of sound sources and microphones.*

## Results

**Separation performance (Table I, average over 48 samples).** GC-AuxIVA-ISS matched or exceeded both baselines in nearly every condition, with the largest gain in the difficult 4-channel case under the UR constraint (8.84 dB SDR vs. GC-AuxIVA-VCD's 5.68 dB; AuxIVA-ISS 8.64 dB):

| Condition | Method | Best constraint | SDR [dB] | SIR [dB] | Order acc. [%] |
|-----------|--------|-----------------|----------|----------|----------------|
| 2 ch | AuxIVA-ISS | — | 10.19 | 12.20 | — |
| 2 ch | GC-AuxIVA-VCD | null (λ=0.8) | 11.05 | 13.26 | 100 |
| 2 ch | GC-AuxIVA-ISS | null (λ=80000) | **11.07** | **13.30** | 100 |
| 3 ch | GC-AuxIVA-VCD | null (λ=5) | 10.62 | 12.74 | 100 |
| 3 ch | GC-AuxIVA-ISS | null (λ=90000) | **10.63** | **12.76** | 100 |
| 4 ch | GC-AuxIVA-VCD | double (λ=2) | **9.52** | **11.79** | 100 |
| 4 ch | GC-AuxIVA-ISS | null (λ=8000) | 9.17 | 11.35 | 100 |

(UR-only results: GC-AuxIVA-ISS 10.96 / 8.84 dB SDR for 2/4 ch vs. GC-AuxIVA-VCD 10.09 / 5.68 dB — the ISS variant is far more robust to the UR-only constraint design; only in the 4-channel double-constraint condition does VCD retain a slight edge.)

**Output order.** Both geometrically constrained methods achieved 100% output-order accuracy in all conditions (no permutation of output channels), confirming that the constraints pin the output order when the weights are set appropriately.

**Block permutation avoidance (Fig. 3).** With 4 sources, target at 70°, RT60 = 300 ms, plain AuxIVA-ISS exhibits the block permutation problem — the low- and high-frequency bands are steered to different sources — while GC-AuxIVA-ISS with the double constraint keeps a consistent beam pattern across the whole spectrum. Spatial information is thus effective for avoiding block permutation even within the ISS update family (in addition to its known benefit under VCD).

![[raw/papers/goto-2022-offline-iss-gciva/figures/a49c72929bfb8adddbd59f8b9eae5ee96a8dda27ca69b3dd559152f0189df65e.jpg|Beam patterns of AuxIVA-ISS]]
![[raw/papers/goto-2022-offline-iss-gciva/figures/c29fa005d3688c3e90468c437a303a14f44206eb49ecce16bea2c0fccc7be285.jpg|Beam patterns of GC-AuxIVA-ISS]]
*Figure 3: Beam patterns of (a) AuxIVA-ISS and (b) GC-AuxIVA-ISS with double constraint (4 sources, target 70°, RT60 = 300 ms). Block permutation occurs between the low- and high-frequency bands in (a) but is avoided in (b).*

![[raw/papers/goto-2022-offline-iss-gciva/figures/ac50c2462ad9504c9553c0dc2a76045f946a68fe8a549b3a4d60b802cbf20674.jpg|Average SDR, RT60 = 100 ms]]
![[raw/papers/goto-2022-offline-iss-gciva/figures/8cbce96e8f4dc15f207a3820a280ea7376744e636a3061aa5b1de7f0400b825a.jpg|Average SDR, RT60 = 300 ms]]
*Figure 2: Average SDR [dB] under reverberant conditions RT60 = 100 ms (left) and RT60 = 300 ms (right).*

**Runtime (Table II, per iteration, 10 s signal).** GC-AuxIVA-ISS runs at essentially the same cost as unconstrained AuxIVA-ISS — the geometric constraints add only ~2% — while GC-AuxIVA-VCD costs 1.5–2.2× more:

| Method | 2 ch [ms] | 3 ch [ms] | 4 ch [ms] |
|--------|-----------|-----------|-----------|
| AuxIVA-ISS | 33.02 | 62.31 | 99.06 |
| GC-AuxIVA-VCD | 51.12 | 120.83 | 217.84 |
| GC-AuxIVA-ISS (proposed) | **33.60** | **63.16** | **101.60** |

At 4 channels the ISS-based methods take less than half the runtime of GC-AuxIVA-VCD.

## Key Contributions

1. **Offline GC-AuxIVA-ISS**: the first inverse-free algorithm for geometrically constrained IVA — ISS rank-1 updates whose closed-form coefficients ($v_{ijf}$, $\alpha_j$, $\beta_j$) absorb the geometric-constraint terms directly, eliminating the per-source/per-frequency matrix inversions of GCAV-IVA while preserving monotonic convergence, fast convergence, and step-size-free operation.
2. **Block permutation analysis**: beam-pattern evidence that geometric constraints prevent the low/high-band block permutation failure of AuxIVA-ISS, extending the known anti-permutation benefit of spatial constraints to the ISS update family.
3. **Empirical validation**: equal or better SDR/SIR than GC-AuxIVA-VCD across 2–4 channels and two reverberation conditions, 100% output-order accuracy, and per-iteration runtime equal to unconstrained AuxIVA-ISS (34–53% faster than GC-AuxIVA-VCD).

## Related Concepts

- [[concepts/geometrically-constrained-iva|Geometrically Constrained IVA]]
- [[concepts/iterative-source-steering|Iterative Source Steering]]
- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/permutation-alignment|Permutation Alignment]]
- [[concepts/online-iva|Online IVA]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Related Synthesis

- (No dedicated synthesis page yet; the offline→online GC-IVA-ISS pair contributes to the emerging picture of ISS as the low-cost backbone for constrained BSS — candidate topics: computational efficiency of BSS optimization algorithms, spatial priors in BSS.)
