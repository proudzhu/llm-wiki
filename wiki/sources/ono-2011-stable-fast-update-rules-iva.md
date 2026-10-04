---
type: source
created: 2026-10-04
updated: 2026-10-04
sources:
  - raw/papers/ono-2011-stable-fast-update-rules-iva/full-text.md
  - https://doi.org/10.1109/ASPAA.2011.6082320
  - zotero://select/items/0_4354E22N
tags:
  - blind-source-separation
  - independent-vector-analysis
  - optimization-algorithms
  - audio-source-separation
---

# Ono 2011: Stable and Fast Update Rules for Independent Vector Analysis Based on Auxiliary Function Technique

**Author**: [[entities/nobutaka-ono|Nobutaka Ono]]
**Affiliation**: National Institute of Informatics, Tokyo, Japan (at the time)
**Venue**: IEEE Workshop on Applications of Signal Processing to Audio and Acoustics (WASPAA), New Paltz, NY, 2011, pp. 189–192
**Year**: 2011
**Type**: Conference paper
**DOI**: [10.1109/ASPAA.2011.6082320](https://doi.org/10.1109/ASPAA.2011.6082320)
**Zotero**: [4354E22N](zotero://select/items/0_4354E22N)

## Summary

This is the founding paper of **AuxIVA**: it derives stable and fast update rules for [[concepts/independent-vector-analysis|IVA]] based on the auxiliary function technique (a majorization-minimization scheme extending EM), replacing the step-size-dependent [[concepts/natural-gradient|natural gradient]] updates that dominated IVA until then. The algorithm alternates between (1) updates of weighted covariance matrices and (2) **iterative projection (IP)** updates of the demixing matrix rows, with **no tuning parameters** and guaranteed monotonic decrease of the objective. On convolutive speech mixtures, AuxIVA converges much faster than natural gradient updates and never diverges, while natural gradient with a large step size diverges within tens of iterations.

## Problem Formulation

Determined BSS of $K$ sources by $K$ microphones in the STFT domain: $\boldsymbol{x}(\omega)=\boldsymbol{A}(\omega)\boldsymbol{s}(\omega)$, separated by $\boldsymbol{y}(\omega)=\boldsymbol{W}(\omega)\boldsymbol{x}(\omega)$. IVA minimizes

$$
J(\mathcal{W})=\sum_{k=1}^{K}E\left[G(\boldsymbol{y}_k)\right]-\sum_{\omega=1}^{N_\omega}\log|\det W(\omega)|
$$

where the **spherical contrast function** $G(\boldsymbol{y}_k)=G_R(r_k)$, $r_k=\|\boldsymbol{y}_k\|_2$ couples all frequency bins of source $k$ and thereby avoids the permutation problem of frequency-domain ICA.

The standard solver was the natural gradient update, which requires a step size $\mu$ trading off convergence speed against stability — too large causes divergence.

## Methodology

### Auxiliary function of the contrast function

Define the class $S_G=\{G\mid G(\boldsymbol{z})=G_R(\|\boldsymbol{z}\|_2)\}$ with $G_R(r)$ continuous, differentiable, and $G_R'(r)/r$ monotonically decreasing (super-Gaussian sources). Common members: $G_1(\boldsymbol{z})=Cr$ and $G_2(\boldsymbol{z})=m\log\cosh(Cr)$.

- **Theorem 1** (quadratic majorizer): for any $G\in S_G$,
$$
G(\boldsymbol{z})\le\frac{G_R'(r_0)}{2r_0}\|\boldsymbol{z}\|_2^2+\left(G_R(r_0)-\frac{r_0G_R'(r_0)}{2}\right)
$$
with equality iff $r_0=\|\boldsymbol{z}\|_2$.
- **Theorem 2**: summing the majorizer over frames yields the auxiliary function
$$
Q(\mathcal{W},\mathcal{V})=\sum_\omega\left[\frac{1}{2}\sum_k\boldsymbol{w}_k^h(\omega)\boldsymbol{V}_k(\omega)\boldsymbol{w}_k(\omega)-\log|\det W(\omega)|\right]+R,
\qquad
\boldsymbol{V}_k(\omega)=E\left[\frac{G_R'(r_k)}{r_k}\boldsymbol{x}(\omega)\boldsymbol{x}^h(\omega)\right]
$$
with $J(\mathcal{W})\le Q(\mathcal{W},\mathcal{V})$, equality iff $r_k=\|\boldsymbol{y}_k\|_2$.

### From HEAD problem to iterative projection

Minimizing $Q$ over **all** rows of $W(\omega)$ simultaneously is exactly the Hybrid Exact-Approximate joint Diagonalization (HEAD) problem (Yeredor 2009) — closed-form solution still open. The paper instead updates **one demixing vector at a time**, keeping the others fixed. The stationary conditions reduce to a linear system whose solution is

$$
\boldsymbol{w}_k(\omega)\leftarrow(W(\omega)V_k(\omega))^{-1}\boldsymbol{e}_k,
\qquad
\boldsymbol{w}_k(\omega)\leftarrow\frac{\boldsymbol{w}_k(\omega)}{\sqrt{\boldsymbol{w}_k^h(\omega)V_k(\omega)\boldsymbol{w}_k(\omega)}}
$$

applied sequentially for all $k$ and all $\omega$, alternating with the auxiliary-variable update of $V_k(\omega)$ (with $r_k$ shared across frequencies). The complete scheme is named **AuxIVA**, and its demixing-matrix step is the first **iterative projection (IP)** rule.

## Experimental Setup

| Item | Value |
|------|-------|
| Task | Convolutive BSS of speech mixtures |
| Sources | ATR Japanese speech database (Set B) |
| Impulse responses | RWCP Sound Scene Database, variable-reverberation room E2A |
| Mixtures | 20 per condition, $K\in\{2,3\}$, source directions $10^\circ$–$170^\circ$ by $20^\circ$ |
| Reverberation | 300 ms; mic spacing 2.83 cm; source-mic distance 2 m |
| STFT | 16 kHz, 2048-point frame, 1024 shift, Hamming window |
| Contrast | $G(\boldsymbol{y}_k)=r_k$ |
| Baseline | Natural gradient, $\mu\in\{0.1,0.2,0.3\}$ |
| Initialization | Identity demixing matrix |
| Scale restoration | Projection back (Murata et al. 2001) |
| Metric | Average SIR improvement (BSS toolbox), every 10 iterations |

## Results

![[raw/papers/ono-2011-stable-fast-update-rules-iva/figures/8f71dd3764bd343e369fbbb4df74cfa68acedcfbac5b1b0d2ca3836534aff1bc.jpg|SIR improvement, K=2]]

![[raw/papers/ono-2011-stable-fast-update-rules-iva/figures/95aa8a02678674458ad6086a4fc75cad2cc25659ffeebe3de611f23d02d6cbac.jpg|SIR improvement, K=3]]

*Figure 1: Averaged SIR improvements at every ten iterations by AuxIVA updates and the natural gradient updates with different step sizes, for K = 2 (top) and K = 3 (bottom).*

- AuxIVA converges **much faster** and reaches **better final SIR** than natural gradient at any step size.
- Natural gradient at $\mu=0.2$ beats $\mu=0.1$ but $\mu=0.3$ **diverges** — in 70–80 iterations for some $K=2$ trials, within the first 10 iterations for $K=3$ — illustrating exactly the stability/speed tradeoff AuxIVA eliminates.
- Per-iteration cost (Matlab R2011a, 2.66 GHz): AuxIVA 0.15 s ($K{=}2$) / 0.34 s ($K{=}3$) vs natural gradient 0.10 s / 0.16 s — AuxIVA is ~1.5–2× more expensive per iteration due to the matrix inversion, but its iteration count is drastically lower, so it wins overall.

## Key Contributions

1. **AuxIVA**: the first tuning-parameter-free IVA algorithm — auxiliary-function (MM) optimization of the IVA negative log-likelihood with guaranteed monotonic decrease.
2. **IP update rule**: the closed-form single-row demixing update $(W(\omega)V_k(\omega))^{-1}\boldsymbol{e}_k$ + normalization, the seed of the entire IP/ISS/IPA family.
3. **Identification of the HEAD connection**: the joint minimization of the auxiliary function is a Hybrid Exact-Approximate joint Diagonalization problem, motivating the sequential (block-coordinate) approach.
4. **Empirical demonstration** that monotonic no-step-size updates outperform and out-stabilize natural gradient on reverberant speech.

## Related Concepts

- [[concepts/independent-vector-analysis|Independent Vector Analysis]] — parent framework
- [[concepts/iterative-projection|Iterative Projection (IP)]] — the demixing-matrix update introduced here
- [[concepts/iterative-source-steering|Iterative Source Steering]] — the later inverse-free rank-1 alternative (Scheibler & Ono 2020)
- [[concepts/iterative-projection-with-adjustment|Iterative Projection with Adjustment]] — the later joint-update extension (Scheibler 2021)
- [[concepts/natural-gradient|Natural Gradient]] — the step-size-based predecessor displaced by AuxIVA
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/independent-low-rank-matrix-analysis|ILRMA]] — the most influential downstream framework reusing the IP machinery

## Related Sources

- [[sources/scheibler-2020-fast-stable-bss-rank-1-updates|Scheibler & Ono 2020: Fast and Stable BSS with Rank-1 Updates]] — ISS, the inverse-free alternative to IP
- [[sources/scheibler-2021-log-quadratically-penalized-iva|Scheibler 2021: IVA via LQPQM]] — IPA, which removes IP's frozen-others limitation
- [[sources/scheibler-2020-fast-independent-vector-extraction|Scheibler & Ono 2020: FIVE]] — the special case where the auxiliary function can be minimized globally in closed form
- [[sources/guo-2023-iva-survey|Guo, Luo & Li 2023: IVA Survey]] — surveys the family this paper founded
- [[sources/nakatani-2022-switching-iva|Nakatani et al. 2022: Switching IVA]] — downstream AuxVA descendant

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] — AuxIVA-IP is the baseline optimization core of this pipeline family
