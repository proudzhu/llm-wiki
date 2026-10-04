---
type: source
created: 2026-10-04
updated: 2026-10-04
sources:
  - raw/papers/goto-2022-iss-gciva/full-text.md
  - https://doi.org/10.23919/APSIPAASC55919.2022.9980301
  - zotero://select/items/0_IABC9JVN
tags:
  - speech-enhancement
  - blind-source-separation
  - independent-vector-analysis
  - online-processing
  - computational-efficiency
  - direction-of-arrival
---

# Goto, Ueda, Li, Yamada & Makino 2022: Accelerating Online GC-IVA with Iterative Source Steering

**Authors**: [[entities/kana-goto|Kana Goto]]¹, [[entities/tetsuya-ueda|Tetsuya Ueda]]², [[entities/li-li|Li Li]]³, [[entities/takeshi-yamada|Takeshi Yamada]]¹, [[entities/shoji-makino|Shoji Makino]]¹²
**Affiliations**: ¹University of Tsukuba, Japan; ²Waseda University, Japan; ³NTT Communication Science Laboratories, Nippon Telegraph and Telephone Corporation, Japan
**Venue**: APSIPA Annual Summit and Conference 2022 (APSIPA ASC 2022)
**Year**: 2022
**Type**: Conference paper
**DOI**: [10.23919/APSIPAASC55919.2022.9980301](https://doi.org/10.23919/APSIPAASC55919.2022.9980301)
**Zotero**: [Open in Zotero](zotero://select/items/0_IABC9JVN)

## Summary

This paper derives **online GC-AuxIVA-ISS**, an alternative online algorithm for [[concepts/geometrically-constrained-iva|geometrically constrained IVA]] that replaces the vectorwise coordinate descent (VCD) update of [[sources/li-2020-online-gciva|online GC-AuxIVA-VCD]] with [[concepts/iterative-source-steering|iterative source steering (ISS)]], eliminating the per-source, per-frequency matrix inversions and yielding an inverse-free, numerically stable rank-1 update. In a fixed-target/moving-interference speech enhancement scenario, it achieves enhancement performance comparable to online GC-AuxIVA-VCD while reducing execution time by 25–75% depending on the DOA-estimation regime. The paper additionally replaces the assumed-known interference DOAs with DOAs estimated by MUSIC applied to projection-back source images, finding that temporally smoothed estimates ("MUSIC smooth") work best.

## Problem Formulation

Determined BSS setting: $J$ sources observed by $I = J$ microphones, STFT-domain observation $\boldsymbol{x}_{fn} \in \mathbb{C}^I$, estimate $\boldsymbol{y}_{fn} = \boldsymbol{W}_f \boldsymbol{x}_{fn}$ with demixing matrix $\boldsymbol{W}_f = [\boldsymbol{w}_{1f}, \dots, \boldsymbol{w}_{Jf}]^{\mathsf{H}}$. IVA minimizes the negative log-likelihood

$$
\mathcal{L}_{\mathrm{IVA}}(\mathcal{W}) = \sum_{j=1}^{J} \mathbb{E}\left[ G(\boldsymbol{y}_{jn}) \right] - \sum_{f=1}^{F} \log|\det \boldsymbol{W}_f|,
$$

with the spherical contrast function $G(\boldsymbol{y}_{jn}) = G_R(r_{jn})$, $r_{jn} = \|\boldsymbol{y}_{jn}\|_2$. Geometric constraints restrict the far-field response of the demixing filters over a set of directions $\Theta$:

$$
\mathcal{L}_{\mathrm{GC}}(\mathcal{W}) = \sum_{f=1}^{F} \sum_{j=1}^{J} \sum_{\theta \in \Theta} \lambda_{j\theta} \left| \boldsymbol{w}_{jf}^{\mathsf{H}} \boldsymbol{d}_{f\theta} - c_{j\theta} \right|^2,
$$

where $\boldsymbol{d}_{f\theta}$ is the steering vector, $c_{j\theta} = 1$ forces a distortionless (delay-and-sum) response toward $\theta$ and small $c_{j\theta}$ creates a spatial null. The auxiliary-function upper bound of $\mathcal{L}_{\mathrm{IVA}}$ plus $\mathcal{L}_{\mathrm{GC}}$ constitutes the GC-AuxIVA objective, with weighted covariance $\boldsymbol{\Sigma}_{jf} = \sum_n \varphi(r_{jn})\, \boldsymbol{x}_{fn}\boldsymbol{x}_{fn}^{\mathsf{H}}$, $\varphi(r) = G_R'(r)/r$.

**Motivation.** The VCD-based update (online or offline) requires a matrix inversion $\boldsymbol{D}_{jf}^{-1}$ with $\boldsymbol{D}_{jf} = \boldsymbol{\Sigma}_{jf} + \sum_\theta \lambda_{j\theta} \boldsymbol{d}_{f\theta}\boldsymbol{d}_{f\theta}^{\mathsf{H}}$ for every frequency, source, and iteration — computationally expensive and numerically unstable. Additionally, GC-IVA assumes DOAs are known in advance, which is impractical; the heuristic interference-DOA estimator of Li et al. 2020 (beam-pattern power of a parallel AuxIVA system) depends on the chosen frequency range and is unclear how to extend to more sources.

## Methodology

### Online GC-AuxIVA-ISS

The online covariance recursion (as in [[concepts/online-iva|online IVA]]) is

$$
\boldsymbol{\Sigma}_{jfn} = \alpha\, \boldsymbol{\Sigma}_{jf(n-1)} + (1-\alpha)\, \varphi(r_{jn})\, \boldsymbol{x}_{fn}\boldsymbol{x}_{fn}^{\mathsf{H}},
$$

with forgetting factor $0 \le \alpha < 1$. Instead of updating demixing rows alternately (VCD), ISS performs a rank-1 update of the whole demixing matrix per source:

$$
\boldsymbol{W}_{fn} \leftarrow \boldsymbol{W}_{fn} - \boldsymbol{v}_{jfn} \boldsymbol{w}_{jfn}^{\mathsf{H}},
$$

where $\boldsymbol{v}_{jfn} \in \mathbb{C}^I$ is estimated instead of the demixing matrix. Substituting the rank-1 update into the online GC-AuxIVA objective (with time-varying look directions $\Theta_n$, allowing the geometric constraints to follow estimated DOAs) and setting $\partial \mathcal{L}(\boldsymbol{v}_{jfn}) / \partial v_{ijfn}^{*} = 0$ yields closed-form updates:

$$
v_{ijfn} = \frac{\boldsymbol{w}_{ifn} \boldsymbol{\Sigma}_{ifn} \boldsymbol{w}_{jfn}^{\mathsf{H}} + 2 \sum_{\theta \in \Theta_n} \lambda_{i\theta} g_{jf\theta n}^{*} (g_{if\theta n} - c_{i\theta})}{\boldsymbol{w}_{jfn} \boldsymbol{\Sigma}_{ifn} \boldsymbol{w}_{jfn}^{\mathsf{H}} + 2 \sum_{\theta \in \Theta_n} \lambda_{i\theta} |g_{jf\theta n}|^2},
$$

$$
v_{jjfn} = \begin{cases} 1 - p_{jfn}^{-1/2} & (q_{jfn} = 0), \\ 1 - q_{jfn}^{*} \dfrac{|q_{jfn}| + \sqrt{|q_{jfn}|^2 + p_{jfn}}}{p_{jfn}\,|q_{jfn}|} & \text{(o.w.)}, \end{cases}
$$

with

$$
g_{jf\theta n} = \boldsymbol{w}_{jfn}^{\mathsf{H}} \boldsymbol{d}_{f\theta}, \quad
p_{jfn} = \boldsymbol{w}_{jfn} \boldsymbol{\Sigma}_{jfn} \boldsymbol{w}_{jfn}^{\mathsf{H}} + 2 \sum_{\theta \in \Theta_n} \lambda_{j\theta} |g_{jf\theta n}|^2, \quad
q_{jfn} = \sum_{\theta \in \Theta_n} \lambda_{j\theta} c_{j\theta} g_{jf\theta n}.
$$

The geometric-constraint terms enter the off-diagonal numerator/denominator of $v_{ijfn}$ and the $p$, $q$ scalars of the diagonal update $v_{jjfn}$ — no matrix inversion appears anywhere. $\Theta_n$ can be time-varying (constraints adapt to estimated DOAs) or time-invariant (manual control). The algorithm retains all advantages of the auxiliary-function approach (fast convergence, no stepsize tuning) and of ISS (low complexity, numerical stability, efficient handling of moving sources), and reduces to online AuxIVA-ISS without constraints.

### Related Work

- The authors' **offline GC-AuxIVA-ISS** ([[sources/goto-2022-offline-iss-gciva|Goto, Ueda, Li, Yamada & Makino 2022, EUSIPCO]]) already replaced VCD with ISS offline, achieving comparable or better enhancement with 34–53% per-iteration runtime reduction; the present work extends it online.
- **Online AuxIVA-ISS** (Nakashima & Ono, APSIPA 2022) performs the offline-to-online ISS extension without geometric constraints; the proposed method can be viewed as online AuxIVA-ISS plus geometric constraints.

### Interference DOA Estimation with MUSIC

To avoid assuming known interference DOAs, the classic subspace method MUSIC is applied. MUSIC decomposes the covariance $\boldsymbol{R}_f = \mathbb{E}[\boldsymbol{x}_{fn}\boldsymbol{x}_{fn}^{\mathsf{H}}]$ into signal and noise subspaces (assuming $I > J$) and defines the spatial spectrum

$$
P_{f\theta} = \frac{1}{\sum_{i=J+1}^{I} \left| \boldsymbol{d}_{f\theta}^{\mathsf{H}} \boldsymbol{u}_{if} \right|^2},
$$

peaked at source directions ($\boldsymbol{u}_{if}$: noise-subspace eigenvectors of $\boldsymbol{R}_f$). To estimate *interference* DOAs specifically, the **projection back** technique first converts each temporarily separated signal into a multichannel source image $\tilde{\boldsymbol{y}}_{jfn} = \boldsymbol{W}_f^{-1} \boldsymbol{e}_j\, y_{jfn}$, which becomes the input of MUSIC; for the first frame (no estimate yet), each observed signal is projected back instead, and the DOAs except the one closest to the given target DOA are selected as interference DOAs. Three estimation regimes are compared:

- **MUSIC normal** — use the per-frame DOA estimate directly;
- **MUSIC smooth** — moving average of the estimates over the last few frames;
- **MUSIC block** — blockwise DOA estimation (every few frames).

## Experimental Setup

| Item | Setting |
|------|---------|
| Speech data | ATR Japanese Speech Database, 6 speakers (3M/3F); 20 random 2-speaker mixtures, 60 s each |
| Array | 2 microphones, 2 cm spacing |
| Geometry | Target fixed at 45° for all 60 s; interference at 90° (first 20 s), moving on an arc 90° → 150° (next 20 s), fixed at 150° (last 20 s) |
| RIRs | Simulated (image-method signal generator); RT60 = 200 ms |
| STFT | 16 kHz sampling; Hanning window, 1024 samples (64 ms) / 512 samples (32 ms) shift |
| Algorithm params | $\alpha = 0.99$; $\boldsymbol{\Sigma}_{jf0}$, $\boldsymbol{W}_{f0}$ initialized as identity; null constraints $c_{j\theta} = 0$ toward estimated interference DOAs; $\lambda_{\mathrm{null}}$ tuned experimentally |
| DOA estimation | MUSIC spatial spectrum per frequency bin, 500–4000 Hz, peak of the frequency-averaged spectrum; moving average / block size = 5 frames (source moves ≈ 0.4° over 5 frames); "Correct" DOAs also evaluated as upper bound |
| Compared methods | oGC-AuxIVA-VCD [Li et al. 2020], oGC-AuxIVA-ISS (proposed), oAuxIVA-ISS (blind baseline) |
| Metrics | SDR, SIR (Vincent et al. 2006) |

![[raw/papers/goto-2022-iss-gciva/figures/f3cdebb775493375f7e1bb1da51ad7fa7696112eb9bb961e41d3b8edc863eeb2.jpg|Layout of sound sources and microphones]]
*Figure 1: Layout of sound sources and microphones — fixed target at 45°, interference moving on an arc from 90° to 150°.*

## Results

**DOA-estimation regime (Table I).** With oGC-AuxIVA-ISS, "MUSIC smooth" outperformed "MUSIC normal" and "MUSIC block" by more than 0.7 dB SDR and 0.6 dB SIR:

| DOA estimation approach | SDR [dB] | SIR [dB] |
|------------------------|----------|----------|
| MUSIC normal | 7.45 | 13.67 |
| MUSIC smooth | **8.33** | **14.34** |
| MUSIC block | 7.59 | 13.74 |

The reason is estimation stability: per-frame ("normal") and blockwise estimates fluctuate more than the smoothed ones (Fig. 2), and constraint directions that jitter from frame to frame degrade the enhancement.

![[raw/papers/goto-2022-iss-gciva/figures/5b1a2a964170cad08719734cc425dcc08a9858dd5c09ad4a37962ccbb2dc293c.jpg|DOA estimates, MUSIC normal]]
![[raw/papers/goto-2022-iss-gciva/figures/90e1da27e64a4e94322de3beb843bbde7ad9f8f616091381527e3ec18b1b4c19.jpg|DOA estimates, MUSIC smooth]]
![[raw/papers/goto-2022-iss-gciva/figures/82467d02855b547c957f9345a2bc1277ae8a843d65cb5d6ac90e252e53fe3871.jpg|DOA estimates, MUSIC block]]
*Figure 2: DOA of the moving source estimated by MUSIC under the three regimes (normal / smooth / block, top to bottom); blue lines are the correct DOA. "Smooth" tracks the arc with far less frame-to-frame variation.*

**Enhancement performance (Fig. 3).** Using "MUSIC smooth", the proposed oGC-AuxIVA-ISS achieved SDR almost equivalent to oGC-AuxIVA-VCD throughout the 60 s. SDR drops immediately after the interference starts moving (≈ 20 s), but both geometrically constrained methods recover faster than the blind oAuxIVA-ISS. Performance with MUSIC-estimated DOAs is close to that with the correct DOAs, demonstrating the system's effectiveness for moving sources. With an appropriate $\lambda_{\mathrm{null}}$, both oGC-AuxIVA-VCD and oGC-AuxIVA-ISS achieved 100% output-order accuracy (no channel-selection errors — a key practical benefit of geometric constraints).

![[raw/papers/goto-2022-iss-gciva/figures/5abeaeae49de0418bf7b2c3eb8482d08e0dd70ccfbbbb4551c991d154a6e5067.jpg|Average SDR of each method every 2 s]]
*Figure 3: Average SDR of the (fixed) target source per 2 s interval for each method; error bars denote 1.96 standard errors. VCD/ISS in the legend denote oGC-AuxIVA-VCD and oGC-AuxIVA-ISS (proposed).*

**Runtime (Table II).** For separating 60 s of audio, oGC-AuxIVA-ISS reduced execution time relative to oGC-AuxIVA-VCD by ≈ 75% with correct DOAs (25.25 s → 6.24 s), ≈ 25% with per-frame/smoothed MUSIC (75.32 → 56.04 s, 73.96 → 55.99 s), and ≈ 55% with blockwise MUSIC (35.58 → 16.16 s). DOA-estimation cost is identical for both separators, so the reduction is largest where DOA estimation is cheapest (fewer estimations → separation dominates the runtime).

| DOA estimation approach | oGC-AuxIVA-VCD [s] | oGC-AuxIVA-ISS (proposed) [s] |
|------------------------|--------------------|-------------------------------|
| Correct | 25.25 | **6.24** |
| MUSIC normal | 75.32 | **56.04** |
| MUSIC smooth | 73.96 | **55.99** |
| MUSIC block | 35.58 | **16.16** |

## Key Contributions

1. **Online GC-AuxIVA-ISS**: the first online algorithm for geometrically constrained IVA based on iterative source steering — an inverse-free rank-1 update in which the geometric-constraint terms enter the closed-form ISS coefficients ($v_{ijfn}$, $p_{jfn}$, $q_{jfn}$) directly, eliminating the per-frequency/per-source matrix inversions of online GC-AuxIVA-VCD while keeping the auxiliary-function advantages (fast convergence, no stepsize tuning) and numerical stability.
2. **MUSIC-based interference DOA estimation for GC-IVA**: replaces the assumed-known interference DOAs (and the frequency-range-dependent beam-pattern heuristic of Li et al. 2020) with MUSIC applied to projection-back source images, enabling time-varying constraint directions $\Theta_n$ that track moving sources.
3. **Empirical validation**: comparable enhancement to oGC-AuxIVA-VCD (SDR within noise, 100% output-order accuracy) with 25–75% runtime reduction, and the finding that temporally smoothed DOA estimates ("MUSIC smooth", moving average over 5 frames) outperform both per-frame and blockwise estimates by > 0.7 dB SDR.

## Related Concepts

- [[concepts/geometrically-constrained-iva|Geometrically Constrained IVA]]
- [[concepts/iterative-source-steering|Iterative Source Steering]]
- [[concepts/online-iva|Online IVA]]
- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Related Synthesis

- (No dedicated synthesis page yet — candidate topics: computational efficiency of BSS optimization algorithms, or spatial priors in BSS alongside [[concepts/spatial-regularization|spatial regularization]])
