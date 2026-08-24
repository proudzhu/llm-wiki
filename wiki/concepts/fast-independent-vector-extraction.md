---
type: concept
created: 2026-08-24
updated: 2026-08-24
sources:
  - raw/papers/scheibler-2020-fast-independent-vector-extraction/full-text.md
tags:
  - blind-source-extraction
  - independent-vector-extraction
  - maximum-sinr-beamforming
  - auxiliary-function
  - convergence-analysis
  - optimization-algorithms
---

# Fast Independent Vector Extraction

**FIVE** (Fast Independent Vector Extraction, Scheibler & Ono 2020) is an [[concepts/independent-vector-extraction|IVE]] algorithm that blindly extracts a single super-Gaussian source from a Gaussian background by **iterative maximum-SINR beamforming**: each iteration re-estimates the background covariance with a weight function that suppresses target-dominated frames and solves a [[concepts/generalized-eigenvalue-decomposition|generalized eigenvalue problem]] for the new beamformer. Despite its simple description, it is the maximum-likelihood estimator under a spherical super-Gaussian source + Gaussian background model, and it **globally minimizes the auxiliary function at every iteration** — the property that makes it dramatically faster than its relatives.

## Algorithm

Given an initial target estimate $\hat{s}_{fn}$ (typically one microphone signal), repeat until convergence:

1. **Magnitude estimate**: $r_{n} = \sqrt{\sum_{f}|\hat{s}_{fn}|^{2}}$ for each frame.
2. **Reweighted background covariance**:

$$\boldsymbol{V}_{f} = \frac{1}{N}\sum_{n}\varphi_{n}(r_{n})\,\boldsymbol{x}_{fn}\boldsymbol{x}_{fn}^{\mathsf{H}}$$

where $\varphi_{n}(r)$ is strictly decreasing — target-dominated frames (large $r_n$) are down-weighted, background-dominated frames emphasized.
3. **Max-SINR beamformer**: the generalized eigenvector of $(\boldsymbol{C}_{f}, \boldsymbol{V}_{f})$ with the largest generalized eigenvalue, $\boldsymbol{C}_{f}\boldsymbol{w} = \lambda\boldsymbol{V}_{f}\boldsymbol{w}$.
4. **Update**: $\hat{s}_{fn} \leftarrow \boldsymbol{w}_{f}^{\mathsf{H}}\boldsymbol{x}_{fn}$.

After one-time pre-whitening of the input ($\boldsymbol{C}_{f} = \boldsymbol{Q}_{f}^{\mathsf{H}}\boldsymbol{Q}_{f}$), step 3 reduces to the **smallest eigenpair** of $\widetilde{\boldsymbol{V}}_{f} = \boldsymbol{Q}_{f}^{-\mathsf{H}}\boldsymbol{V}_{f}\boldsymbol{Q}_{f}^{-1}$: $\boldsymbol{w}_{f} = \lambda_{M}^{-1/2}\boldsymbol{r}_{M}$. Only $\boldsymbol{w}$ is ever computed — the background demixing matrix and its covariance are never needed.

## Key Formulations

The likelihood view: FIVE minimizes the negative log-likelihood of a probabilistic model with (i) independent target and background, (ii) spherical super-Gaussian source prior $p_{S_{n}} \sim e^{-G_{n}(r)}$ ($G^{\prime}_{n}(r)/r$ strictly decreasing), (iii) Gaussian background uncorrelated across frequencies. With

$$\varphi_{n}(r) = \frac{G^{\prime}_{n}(r)}{2r}$$

the algorithm is **guaranteed to converge to a stationary point** of the likelihood (Theorem 1 of the paper). The auxiliary function is majorized via the super-Gaussian inequality, and its stationarity system is a special case of the hybrid exact-approximate diagonalization (HEAD) problem that admits an exact closed-form solution: the $M$ stationary points are $\boldsymbol{w} = \lambda_{k}^{-1/2}\boldsymbol{Q}^{-1}\boldsymbol{r}_{k}$, and the **global minimum is the smallest eigenvalue** ($k = M$).

Two instantiations of the weight function:

| Source model | $\varphi_{n}(r)$ | Empirical behavior |
|---|---|---|
| Time-invariant Laplace | $(2r)^{-1}$ | Fastest convergence; higher $\Delta$SIR |
| Time-varying Gaussian | $(r^{2}/F)^{-1}$ | Slightly slower; stably higher $\Delta$SDR |

## Properties

- **Speed**: peak SDR improvement (over 4 dB) within **1–3 iterations**; ~5× faster than OverIVA, ≥10× faster than full AuxIVA; scales to 8 microphones — high real-time potential.
- **Global minimization per iteration**: unlike AuxIVA (row-wise updates) and OverIVA (orthogonality constraints), which only partially minimize the auxiliary function, FIVE solves each iteration to its global minimum via eigendecomposition.
- **Convergence guarantee**: monotone descent to a stationary point of the likelihood, without step sizes (contrast [[concepts/ogive|OGIVE]], which needs step-size tuning and thousands of iterations).
- **Limitation**: the Gaussian-background assumption. With few interferers (non-Gaussian background), performance degrades; model-free full separation (AuxIVA) is markedly more robust in that regime. FIVE (Laplace) can also show a slight SDR *decrease* after its early peak — the likelihood it minimizes is not the SDR.

## Related Concepts

- [[concepts/independent-vector-extraction|Independent Vector Extraction]]
- [[concepts/blind-source-extraction|Blind Source Extraction]]
- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/ogive|OGIVE]]
- [[concepts/generalized-eigenvalue-decomposition|Generalized Eigenvalue Decomposition]]
- [[concepts/natural-gradient|Natural Gradient]]

## Related Sources

- [[sources/scheibler-2020-fast-independent-vector-extraction|Scheibler & Ono 2020: Fast Independent Vector Extraction]]
- [[sources/guo-2023-iva-survey|Guo, Luo & Li 2023: IVA Survey]] — benchmarks FIVE among IVA/IVE optimization families
- [[sources/ruan-2024-speech-extraction-low-snr|Ruan, Liao, Chen & Lu 2024: Speech Extraction Under Extremely Low SNR Conditions]]
