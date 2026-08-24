---
type: source
created: 2026-08-24
updated: 2026-08-24
sources:
  - raw/papers/scheibler-2020-fast-independent-vector-extraction/full-text.md
  - https://doi.org/10.1109/ICASSP40776.2020.9053066
  - https://arxiv.org/abs/1910.10654
  - zotero://select/items/0_P4LS24WL
tags:
  - blind-source-extraction
  - independent-vector-extraction
  - fast-independent-vector-extraction
  - maximum-sinr-beamforming
  - auxiliary-function
  - convergence-analysis
  - speech-enhancement
---

# Scheibler & Ono 2020: Fast Independent Vector Extraction

**Authors**: [[entities/robin-scheibler|Robin Scheibler]], [[entities/nobutaka-ono|Nobutaka Ono]]
**Institution**: Tokyo Metropolitan University, Hino, Japan (Ono Lab)
**Venue**: IEEE ICASSP 2020, Barcelona, Spain (conference paper)
**DOI**: [10.1109/ICASSP40776.2020.9053066](https://doi.org/10.1109/ICASSP40776.2020.9053066)
**arXiv**: [1910.10654](https://arxiv.org/abs/1910.10654)
**Funding**: JSPS KAKENHI 17F17049, 16H01735; JST CREST JPMJCR19A3
**Code**: <https://github.com/onolab-tmu/code_2020ICASSP_five>

## Summary

This paper proposes **FIVE** (Fast Independent Vector Extraction), an algorithm that blindly extracts a single non-Gaussian source from a Gaussian background by iteratively applying maximum-SINR beamforming: each iteration re-estimates the background covariance with a weight function that suppresses target-dominated frames, then solves a generalized eigenvalue problem for the new beamformer. The authors prove that this deceptively simple procedure minimizes the same negative log-likelihood as OverIVA via the auxiliary-function technique — but unlike related methods, the auxiliary function is **globally minimized at every iteration** through an exact eigendecomposition. Experiments show FIVE reaches peak SDR improvement in one to three iterations — roughly five times faster than OverIVA and at least an order of magnitude faster than full AuxIVA — giving it high potential for real-time applications.

## Problem Formulation

[[concepts/blind-source-extraction|Blind source extraction]] (BSE) separates a single target signal from background noise without prior information. In the STFT domain with $M$ microphones, the signal model is

$$x_{mfn} = s_{mfn} + b_{mfn}, \qquad \boldsymbol{x}_{fn} \in \mathbb{C}^{M}$$

Frequency-domain processing avoids convolutive mixing but introduces the permutation ambiguity of per-bin ICA; the [[concepts/independent-vector-extraction|IVE]] paradigm resolves this by modeling the target with a multivariate (inter-frequency-dependent) non-Gaussian prior against a Gaussian background.

The maximum-SINR beamformer maximizes

$$\mathsf{SINR}_{f}[\boldsymbol{w}] = \frac{\boldsymbol{w}^{\mathsf{H}}\boldsymbol{\Sigma}^{(s)}_{f}\boldsymbol{w}}{\boldsymbol{w}^{\mathsf{H}}\boldsymbol{\Sigma}^{(b)}_{f}\boldsymbol{w}} \approx \frac{\boldsymbol{w}^{\mathsf{H}}\boldsymbol{C}_{f}\boldsymbol{w}}{\boldsymbol{w}^{\mathsf{H}}\boldsymbol{V}_{f}\boldsymbol{w}}$$

where $\boldsymbol{C}_{f} = \frac{1}{N}\sum_{n}\boldsymbol{x}_{fn}\boldsymbol{x}_{fn}^{\mathsf{H}}$ is the sample covariance and $\boldsymbol{V}_{f} \sim \boldsymbol{\Sigma}^{(b)}_{f}$ a (scaled) background covariance estimate. The optimizer is the generalized eigenvector of the pair $(\boldsymbol{C}_{f}, \boldsymbol{V}_{f})$ with the largest generalized eigenvalue. The practical obstacle is obtaining a good $\boldsymbol{V}_{f}$ — the starting point of FIVE.

## Methodology

### Algorithm (informal view)

Given an initial target estimate $\hat{s}_{fn}$ (e.g., one microphone signal):

1. Compute the (frequency-aggregated) magnitude $r_{n} = \sqrt{\sum_{f}|\hat{s}_{fn}|^{2}}$.
2. Estimate the background covariance with frame weights $\varphi_{n}(r_{n})$ — a strictly decreasing function, so **target-dominated frames are down-weighted and background-dominated frames emphasized**:

$$\boldsymbol{V}_{f} = \frac{1}{N}\sum_{n}\varphi_{n}(r_{n})\,\boldsymbol{x}_{fn}\boldsymbol{x}_{fn}^{\mathsf{H}}$$

3. Solve the generalized eigenvalue problem $\boldsymbol{C}_{f}\boldsymbol{w} = \lambda\boldsymbol{V}_{f}\boldsymbol{w}$ for the maximum-SINR beamformer $\boldsymbol{w}_{f}$.
4. Update $\hat{s}_{fn} \leftarrow \boldsymbol{w}_{f}^{\mathsf{H}}\boldsymbol{x}_{fn}$ and repeat until convergence.

Pre-whitening the input ($\boldsymbol{C}_{f} = \boldsymbol{Q}_{f}^{\mathsf{H}}\boldsymbol{Q}_{f}$, applied once) reduces step 3 to computing the **smallest eigenpair** of $\widetilde{\boldsymbol{V}}_{f} = \boldsymbol{Q}_{f}^{-\mathsf{H}}\boldsymbol{V}_{f}\boldsymbol{Q}_{f}^{-1}$, with $\boldsymbol{w}_{f} = \lambda_{M}^{-1/2}\boldsymbol{r}_{M}$.

### Maximum-likelihood derivation

**Theorem 1** — under (i) statistical independence of target and background, (ii) a spherical super-Gaussian source prior $p_{S_{n}} \sim e^{-G_{n}(r)}$ with $G_{n}^{\prime}(r)/r$ strictly decreasing, and (iii) a Gaussian background with arbitrary cross-channel covariance but uncorrelated across frequencies, FIVE with

$$\varphi_{n}(r) = \frac{G^{\prime}_{n}(r)}{2r}$$

is guaranteed to converge to a stationary point of the negative log-likelihood of the observed signal.

The proof uses the auxiliary-function (majorization-minimization) technique: a majorizer of the non-quadratic source term is constructed via the super-Gaussian inequality $G_{n}(r) \leq G^{\prime}_{n}(r_{0})\frac{r^{2}}{2r_{0}} + G_{n}(r_{0}) - \frac{r_{0}}{2}G^{\prime}_{n}(r_{0})$, giving a quadratic auxiliary cost. Setting its gradient to zero yields the stationarity system

$$\begin{bmatrix}\boldsymbol{w}^{\mathsf{H}}\\ \boldsymbol{J}^{\mathsf{H}}\end{bmatrix}\begin{bmatrix}\boldsymbol{V}\boldsymbol{w} & \boldsymbol{C}\boldsymbol{J}\end{bmatrix} = \begin{bmatrix}1 & \boldsymbol{0}^{\mathsf{T}}\\ \boldsymbol{0} & \boldsymbol{B}\end{bmatrix}$$

— a special case of the hybrid exact-approximate diagonalization (HEAD) problem where $M-1$ columns share the same matrix. Although HEAD has no known closed form for $M>2$ in general, **this special case is solved exactly** (Proposition 1): the $M$ stationary points are $\boldsymbol{w} = \lambda_{k}^{-1/2}\boldsymbol{Q}^{-1}\boldsymbol{r}_{k}$, $k = 1,\ldots,M$, and the **global minimum is the smallest eigenvalue** $k = M$ (Proposition 2, by maximization of $\det(\boldsymbol{W})$). This is what distinguishes FIVE from related methods: AuxIVA-style updates and OverIVA's orthogonality constraints only *partially* minimize the auxiliary function, whereas FIVE minimizes it **globally at every iteration**. Moreover, the background demixing matrix $\boldsymbol{J}$ and covariance $\boldsymbol{B}$ never need to be computed — knowledge of $\boldsymbol{B}$ is moot.

Two source models instantiate the weighting function:

$$\varphi^{\text{Lap}}_{n}(r) = (2r)^{-1} \quad\text{(time-invariant Laplace)}, \qquad \varphi^{\text{Gau}}_{n}(r) = (r^{2}/F)^{-1} \quad\text{(time-varying Gaussian)}$$

## Experimental Setup

| Item | Setting |
|------|---------|
| Simulation | pyroomacoustics; 100 random rectangular rooms, walls 6–10 m, ceiling 2.8–4.5 m |
| Reverberation | $T_{60} \in [60, 540]$ ms (see Fig. 1 histogram) |
| Array | Circular regular, 2 / 3 / 5 / 8 microphones, 2 cm inter-element spacing |
| Sources | Target at $[d_{\text{crit}}, d_{\text{crit}}+1]$ m ($d_{\text{crit}} = 0.057\sqrt{V/T_{60}}$); $Q=10$ interferers at $\geq d_{\text{crit}}+1$ m |
| SNR regime | $\mathsf{SINR} = \sigma_{T}^{2}/(Q\sigma_{I}^{2}+\sigma_{w}^{2}) = 5$ dB; uncorrelated noise = 1% of noise+interference |
| STFT | 4096 points, half-overlap, Hamming window |
| Baselines | OverIVA; full AuxIVA (strongest output channel); OGIVE (gradient ascent, 4000 iterations, step size 0.1); FIVE/OverIVA/AuxIVA run 50 iterations |
| Source models | Time-invariant Laplace; time-varying Gaussian |
| Scale restoration | Projection back onto first microphone |
| Metrics | SDR, SDR improvement, SIR (mir_eval toolbox) |

![[raw/papers/scheibler-2020-fast-independent-vector-extraction/figures/fig1.png|Room setup and reverberation-time histogram]]

*Figure 1: Right — room setup for the simulation (target, interferers, circular array). Left — histogram of simulated reverberation times (60–540 ms).*

## Results

**Convergence speed (Fig. 2)**: FIVE (Laplace) is the fastest, reaching peak $\Delta$SDR in **one to three iterations** with over 4 dB SDR improvement; $\Delta$SDR then slightly decreases before convergence — not a contradiction since the cost function is the likelihood, not the SDR (conjectured: model mismatch). FIVE (Gauss) is close behind and stably attains a larger $\Delta$SDR. OverIVA behaves similarly in $\Delta$SDR but converges about **5× slower**. Full AuxIVA achieves better $\Delta$SDR (better modeling of the background as independent sources) but is **at least 10× slower**, worsening with more microphones. Gradient-based OGIVE converges much more slowly, eventually reaching similar $\Delta$SDR outside the plotted range.

**Separation after three iterations (Fig. 3)**: box-plots of $\Delta$SDR / $\Delta$SIR show FIVE dominating, OverIVA behind, AuxIVA last (and three AuxIVA iterations take about ten times longer). The time-varying Gauss model achieves higher $\Delta$SDR; the Laplace model higher $\Delta$SIR.

**Background-model mismatch (Fig. 4)**: with $\mathsf{SINR}=0$ dB and 3 microphones, varying the number of interferers (success = $\Delta\mathsf{SIR} \geq 1$ dB): with a single interferer all algorithms fail ~half the time or more (without prior information, which of the two sources is the target is unidentifiable); as interferers increase and the background approaches Gaussianity, success rates rise. FIVE and OverIVA behave similarly; AuxIVA — which assumes no specific background model — performs markedly better under mismatch.

**Limitation**: the Gaussian-background assumption is the algorithm's Achilles' heel — performance degrades, sometimes significantly, when the background is sparse (few interferers). The authors identify a more flexible background model as the crucial next step.

## Key Contributions

1. **FIVE algorithm**: a new [[concepts/independent-vector-extraction|IVE]] method — iterative maximum-SINR beamforming with a target-suppressing reweighted background covariance — describable in a few lines yet rigorously founded.
2. **Global auxiliary-function minimization**: proof that the iterative SINR maximization minimizes the same negative log-likelihood as OverIVA, with the auxiliary function *globally* minimized at every iteration (unlike AuxIVA/OverIVA) — the source of the speed.
3. **Exact solution of a special HEAD case**: closed-form solution of the stationary system as a special case of the hybrid exact-approximate diagonalization problem, with the global minimum at the smallest eigenvalue of the whitened weighted covariance.
4. **Convergence guarantee** (Theorem 1) to a stationary point of the likelihood under a spherical super-Gaussian source model and Gaussian background.
5. **Empirical speed evidence**: peak SDR improvement within 1–3 iterations, an order of magnitude faster than full IVA — establishing high potential for real-time BSE — plus a quantified robustness boundary under background-model mismatch.

## Related Concepts

- [[concepts/fast-independent-vector-extraction|Fast Independent Vector Extraction (FIVE)]]
- [[concepts/independent-vector-extraction|Independent Vector Extraction]]
- [[concepts/blind-source-extraction|Blind Source Extraction]]
- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/ogive|OGIVE]]
- [[concepts/generalized-eigenvalue-decomposition|Generalized Eigenvalue Decomposition]]
- [[concepts/blind-source-separation|Blind Source Separation]]

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
