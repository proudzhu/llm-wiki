---
type: source
created: 2026-10-04
updated: 2026-10-04
sources:
  - raw/papers/scheibler-2020-fast-stable-bss-rank-1-updates/full-text.md
  - https://doi.org/10.1109/ICASSP40776.2020.9053556
  - zotero://select/items/0_ZLH97EHW
tags:
  - blind-source-separation
  - independent-vector-analysis
  - optimization-algorithms
  - computational-efficiency
  - audio-source-separation
---

# Scheibler & Ono 2020: Fast and Stable Blind Source Separation with Rank-1 Updates

**Authors**: [[entities/robin-scheibler|Robin Scheibler]], [[entities/nobutaka-ono|Nobutaka Ono]]
**Affiliation**: Tokyo Metropolitan University, Hino, Japan
**Venue**: IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Barcelona, Spain, 2020, pp. 236–240
**Year**: 2020
**Type**: Conference paper
**DOI**: [10.1109/ICASSP40776.2020.9053556](https://doi.org/10.1109/ICASSP40776.2020.9053556)
**Zotero**: [ZLH97EHW](zotero://select/items/0_ZLH97EHW)

## Summary

This paper introduces **AuxIVA-ISS**, an alternative to the ubiquitous AuxIVA-IP ([[sources/ono-2011-stable-fast-update-rules-iva|Ono 2011]]) that minimizes exactly the same cost function but replaces row-by-row demixing-matrix updates with a sequence of **rank-1 updates of the whole matrix**. The resulting rules are **inverse-free** — no matrix inversions at all — and have per-iteration complexity **quadratic** in the number of microphones ($O(FM^2N)$) instead of cubic-plus ($O(FM^3\max(M,N))$). The rank-1 updates are shown to arise from alternate updates of the **steering vectors** (columns of the mixing matrix), hence the name **iterative source steering (ISS)**. Simulations confirm separation performance identical to AuxIVA-IP at lower computational cost.

## Problem Formulation

Determined BSS: $K$ sources on $M=K$ microphones, $\boldsymbol{x}_{fn}=\boldsymbol{A}_f\boldsymbol{s}_{fn}$ in the STFT domain. IVA finds demixing matrices $\boldsymbol{W}_f$ minimizing the negative log-likelihood under source independence and a spherical super-Gaussian distribution, majorized (auxiliary-function / MM technique) by

$$
\mathcal{L}_2=\sum_{f}\sum_{k}\boldsymbol{w}_{kf}^{\mathsf{H}}\boldsymbol{V}_{kf}\boldsymbol{w}_{kf}-2\sum_f\log|\det(\boldsymbol{W}_f)|.
$$

AuxIVA-IP minimizes $\mathcal{L}_2$ alternately per demixing vector $\boldsymbol{w}_{kf}$ in closed form. Drawbacks: it recomputes $M$ covariance matrices and performs $M$ matrix inversions per iteration; complexity is **cubic** in $M$; and matrix inversion is inherently dangerous (instability when some $\boldsymbol{V}_{kf}$ becomes ill-conditioned). A prior close-in-spirit alternative (column-wise updates for IDLMA, Makishima et al. 2019) still requires one matrix inversion per update.

## Methodology

### Rank-1 update rule

Instead of replacing one row of $\boldsymbol{W}_f$, update the whole matrix by a rank-1 subtraction:

$$
\boldsymbol{W}_f\leftarrow\boldsymbol{W}_f-\boldsymbol{v}_{kf}\boldsymbol{w}_{kf}^{\mathsf{H}},
$$

repeated for $k=1,\dots,M$. Plugging into $\mathcal{L}_2$ and using the matrix determinant lemma, the minimization becomes separable in the coefficients $v_{mk}$, with **closed-form solution (Theorem 1)**:

$$
v_{mk}=\begin{cases}\dfrac{\boldsymbol{w}_m^{\mathsf{H}}\boldsymbol{V}_m\boldsymbol{w}_k}{\boldsymbol{w}_k^{\mathsf{H}}\boldsymbol{V}_m\boldsymbol{w}_k}&m\neq k\\[2mm]1-(\boldsymbol{w}_k^{\mathsf{H}}\boldsymbol{V}_k\boldsymbol{w}_k)^{-\frac{1}{2}}&m=k\end{cases}
$$

### Inverse-free implementation

The needed quantities reduce to weighted output-signal statistics,

$$
\boldsymbol{w}_m^{\mathsf{H}}\boldsymbol{V}_m\boldsymbol{w}_k=\sum_n\varphi(r_{mn})\,y_{mn}y_{kn}^{*},
\qquad
\boldsymbol{w}_k^{\mathsf{H}}\boldsymbol{V}_m\boldsymbol{w}_k=\sum_n\varphi(r_{mn})\,|y_{kn}|^2,
$$

and the separated signals update directly as $\boldsymbol{y}_n\leftarrow\boldsymbol{y}_n-\boldsymbol{v}_k y_{kn}$. **The demixing matrix never needs to be stored** — only the output signals — so the offline algorithm runs in-place with $O(1)$ extra memory.

### Steering-vector interpretation (Proposition 1)

By the Sherman–Morrison formula, the rank-1 update of $\boldsymbol{W}$ is equivalent to updating the $k$-th **column of the mixing matrix** (the steering vector of source $k$): $\boldsymbol{a}_k+\boldsymbol{u}=\frac{1}{1-v_{kk}}(\boldsymbol{a}_k+\sum_{m\neq k}v_{mk}\boldsymbol{a}_m)$. Moreover $v_{mk}$ ($m\neq k$) is exactly the minimizer of $\sum_n\varphi(r_{mn})|y_{mn}-vy_{kn}|^2$ — the projection of the *noise in the m-th source estimate onto the k-th source's subspace*. Since $\varphi(r_{mn})$ is small when source $m$ is active, steering vectors are adjusted by contributions from the sources where interference is detected.

### Complexity

$$
\mathcal{C}_{\mathrm{IP}}=O(FM^3\max(M,N))\quad(\text{at least }O(M^4)),\qquad
\mathcal{C}_{\mathrm{ISS}}=O(FM^2N).
$$

ISS's complexity equals that of computing a *single* covariance matrix per iteration — **order-optimal**: no algorithm requiring full covariance information can do better. Online ($N=1$), it is quadratic in microphone count, vs. cubic for online AuxIVA-IP with Sherman–Morrison acceleration (Taniguchi et al. 2014).

## Experimental Setup

| Item | Value |
|------|-------|
| Task | Determined BSS, 2–10 sources (up to 17 for runtime) |
| Simulation | pyroomacoustics, 100 random rooms, walls 6–10 m, ceiling 2.8–4.5 m |
| Reverberation | $T_{60}$ 60–540 ms |
| Array | Circular, 10 mics, radius 3.2 cm (2 cm spacing); ≥50 cm from walls |
| Sources | Beyond critical distance $d_{\text{crit}}=0.057\sqrt{V/T_{60}}$; SNR 30 dB |
| STFT | 16 kHz, 256 ms frame, half-overlap, Hamming analysis + optimal synthesis window |
| Iterations | $10M$ (both algorithms) |
| Scale restoration | Projection back to first microphone |
| Metrics | ΔSDR, ΔSIR (BSSEval v4) |
| Runtime test | C++/XTensor multicore implementation, i9-7900X (10 cores), open-sourced |

## Results

![[raw/papers/scheibler-2020-fast-stable-bss-rank-1-updates/figures/b9b3f2b697eda184d69a1c1fdfdf0c701b263b2fba5dd5c0a3c0468dd2675fa8.jpg|Histogram of reverberation times]]

*Fig. 1: Histogram of the reverberation time of the simulated rooms.*

![[raw/papers/scheibler-2020-fast-stable-bss-rank-1-updates/figures/1ce5ee4e4434e936e60d20af590a4bcbb8b61b42424e45c559b081a054f2a48e.jpg|Box-plots of SDR and SIR improvement]]

*Fig. 2: Box-plots of the SDR and SIR improvement after 10M iterations — IP and ISS are statistically indistinguishable.*

![[raw/papers/scheibler-2020-fast-stable-bss-rank-1-updates/figures/b21e78845325335f9836ae427f6f99cee611c436b13cd03944c117d2335d8413.jpg|Runtime comparison]]

*Fig. 3: Runtime of high-performance C++ implementations of AuxIVA-IP and AuxIVA-ISS for varying number of microphones.*

- **Separation quality**: identical to AuxIVA-IP up to statistical fluctuation, for all source counts.
- **Runtime**: ISS faster everywhere; advantage modest for few microphones but grows dramatically with $M$. All runtimes < 6 ms per iteration even at 17 microphones. The IP/ISS gap is smaller than the complexity analysis predicts (larger hidden constant and memory-access differences in ISS).

## Key Contributions

1. **ISS update rule**: rank-1 updates of the demixing matrix that minimize the AuxIVA auxiliary function in closed form — **no matrix inversions**, no step sizes, monotonic convergence inherited.
2. **Complexity reduction**: $O(FM^2N)$ vs $O(FM^3\max(M,N))$; order-optimal among algorithms that need covariance information; quadratic in $M$ online.
3. **Steering-vector interpretation**: the rank-1 updates equal alternate updates of the sources' steering vectors, with $v_{mk}$ interpretable as the projection of source $m$'s residual noise onto source $k$'s subspace — giving ISS its name and an intuitive noise-cancellation reading.
4. **In-place, $O(1)$-memory implementation** plus an open-source high-performance C++/XTensor multicore implementation with Python wrapper.

## Related Concepts

- [[concepts/iterative-source-steering|Iterative Source Steering]] — the method this paper introduces
- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/iterative-projection|Iterative Projection (IP)]] — the predecessor being replaced
- [[concepts/iterative-projection-with-adjustment|Iterative Projection with Adjustment]] — the later IP+ISS hybrid (Scheibler 2021)
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/independent-low-rank-matrix-analysis|ILRMA]] — source-model family that directly benefits from cheaper updates
- [[concepts/natural-gradient|Natural Gradient]] — the earlier step-size-based route both IP and ISS supersede

## Related Sources

- [[sources/ono-2011-stable-fast-update-rules-iva|Ono 2011: Stable and Fast Update Rules for IVA]] — the AuxIVA-IP baseline this paper replaces
- [[sources/scheibler-2020-fast-independent-vector-extraction|Scheibler & Ono 2020: FIVE]] — companion ICASSP 2020 paper on globally optimal single-source extraction
- [[sources/scheibler-2021-log-quadratically-penalized-iva|Scheibler 2021: IVA via LQPQM]] — IPA, which combines IP's replacement with ISS's adjustment of all other filters
- [[sources/dong-2026-spatially-regularized-switching-iva|Dong et al. 2026: Spatially-Regularized Switching IVA]] — downstream switching-IVA descendant using ISS updates
- [[sources/nakatani-2022-switching-iva|Nakatani et al. 2022: Switching IVA]] — AuxVA descendant framework
- [[sources/guo-2023-iva-survey|Guo, Luo & Li 2023: IVA Survey]] — surveys the IP/ISS families

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] — ISS updates feed the real-time end of this pipeline family
