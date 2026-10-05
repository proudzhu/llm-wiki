---
type: source
created: 2026-10-05
updated: 2026-10-05
sources:
  - raw/papers/brendel-2020-spatially-guided-iva/full-text.md
  - https://doi.org/10.1109/ICASSP40776.2020.9052905
  - zotero://select/items/0_Q355DBZI
tags:
  - blind-source-separation
  - independent-vector-analysis
  - direction-of-arrival
  - spatial-processing
  - optimization-algorithms
---

# Brendel, Haubner & Kellermann 2020: Spatially Guided Independent Vector Analysis

**Authors**: [[entities/andreas-brendel|Andreas Brendel]], [[entities/thomas-haubner|Thomas Haubner]], [[entities/walter-kellermann|Walter Kellermann]]
**Institution**: Multimedia Communications and Signal Processing, Friedrich-Alexander-Universität Erlangen-Nürnberg (FAU), Germany
**Venue**: IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2020
**Type**: Conference paper
**DOI**: [10.1109/ICASSP40776.2020.9052905](https://doi.org/10.1109/ICASSP40776.2020.9052905)
**Zotero**: [Q355DBZI](zotero://select/items/0_Q355DBZI)

## Summary

This paper presents a Maximum A Posteriori (MAP) derivation of [[concepts/independent-vector-analysis|IVA]] that augments the blind separation objective with a **spatial prior over the demixing matrices**, resolving the outer permutation ambiguity and guiding the algorithm toward a desired solution in adverse acoustic conditions. The DOA-uncertainty-aware Gaussian prior favors spatial nulls toward specified directions, and the resulting optimization problem is solved with majorize-minimize (AuxIVA-style) update rules, so the constraint does not impair convergence speed. On measured room impulse responses, the proposed "GC auxIVA" beats the gradient-based geometrically constrained IVA of Khan et al. (2015) in interference suppression at lower total computational cost.

## Problem Formulation

In a determined scenario ($K$ sources, $K$ microphones), the STFT-domain mixture is $\mathbf{x}_{f,n} = \mathbf{A}_f \mathbf{s}_{f,n}$, and separation seeks demixing matrices $\mathbf{W}_f$ with $\mathbf{y}_{f,n} = \mathbf{W}_f \mathbf{x}_{f,n}$.

While IVA's multivariate source model resolves the **inner** (per-frequency-bin) permutation problem, the **outer** permutation ambiguity — which broadband output channel carries which source — remains undetermined. Associating outputs with known target DOAs post hoc fails in reverberant or underdetermined conditions, so prior knowledge must instead steer the adaptation itself.

Applying Bayes' theorem and marginalizing the demixed signals (via the Dirac-delta likelihood of the deterministic mixing relation), the posterior over the demixing matrices is

$$
p(\mathcal{W} \mid \mathcal{X}) \propto p(\mathcal{W}) \prod_{f=1}^{F} |\det \mathbf{W}_f|^{2N} \prod_{n=1}^{N}\prod_{k=1}^{K} p\left(\underline{\mathbf{y}}_{k,n}\right),
$$

which yields the MAP problem

$$
\mathbf{W}_f = \arg\max_{\mathbf{W}_f} \frac{\log p(\mathcal{W})}{N} + 2\sum_{f=1}^{F}\log|\det \mathbf{W}_f| - \sum_{k=1}^{K}\hat{\mathbb{E}}\left\{G\left(\underline{\mathbf{y}}_{k,n}\right)\right\},
$$

with source model $G(\underline{\mathbf{y}}_{k,n}) = -\log p(\underline{\mathbf{y}}_{k,n})$. Choosing an uninformative prior $p(\mathcal{W}) = \mathrm{const.}$ recovers the standard IVA cost function exactly — MAP IVA is a strict generalization of IVA (extending Knuth's Bayesian ICA view to the convolutive/multivariate case).

## Methodology

### Spatial Prior on the Demixing Matrices

Assuming free-field propagation, the relative transfer function (RTF) of a source at DOA $\vartheta_k$ w.r.t. the first microphone is

$$
[\mathbf{h}_f^k]_m = \exp\left(j\frac{2\pi\nu_f}{c_s}\|\mathbf{r}_m - \mathbf{r}_1\|_2 \cos\vartheta_k\right).
$$

The prior is i.i.d. over frequency bins and channels, and each demixing vector follows a **complex Gaussian that favors a spatial null into DOA $\vartheta_k$**:

$$
p(\mathbf{w}_f^k) \propto \exp\left(-\frac{1}{\tilde{\sigma}_f^2}(\mathbf{w}_f^k)^{\mathrm{H}}\left(\lambda_E \mathbf{I} + \mathbf{h}_f^k(\mathbf{h}_f^k)^{\mathrm{H}}\right)\mathbf{w}_f^k\right).
$$

Key design points:

- $\tilde{\sigma}_f^2$ expresses the **uncertainty of the DOA estimate** — a user-defined parameter here, but directly obtainable from a localization or tracking algorithm, enabling fusion with DOA estimators' confidence.
- The $\lambda_E \mathbf{I}$ term is a **Tikhonov regularizer** penalizing filter energy, ensuring the prior stays proper for all DOAs.
- Only channels in a constrained set $\mathcal{I}$ receive the informative prior; the others keep a non-informative prior. $|\mathcal{I}| = K-1$ priors of this form suffice to disambiguate $K$ sources.

The resulting cost function is $J(\mathcal{W}) = J_{\mathrm{IVA}}(\mathcal{W}) + J_{\mathrm{prior}}(\mathcal{W})$ with the nonnegative quadratic prior term

$$
J_{\mathrm{prior}}(\mathcal{W}) = \frac{1}{\sigma_f^2}\sum_{f=1}^{F}\sum_{k=1}^{K}(\mathbf{w}_f^k)^{\mathrm{H}}\left(\lambda_E\mathbf{I} + \mathbf{h}_f^k(\mathbf{h}_f^k)^{\mathrm{H}}\right)\mathbf{w}_f^k, \quad \sigma_f^2 = N\tilde{\sigma}_f^2.
$$

### MM (AuxIVA-Style) Update Rules

Following the auxiliary-function/majorize-minimize construction of AuxIVA, the super-Gaussian source-model term is upper-bounded using the weighted covariance matrix

$$
\mathbf{V}_f^k(\mathcal{W}_k^{(l)}) = \hat{\mathbb{E}}\left\{\frac{G'(r_n^k)}{r_n^k}\mathbf{x}_{f,n}\mathbf{x}_{f,n}^{\mathrm{H}}\right\}, \qquad r_n^k = \|\underline{\mathbf{y}}_{k,n}\|_2,
$$

which yields an upper bound $Q(\mathcal{W}|\mathcal{W}^{(l)})$ identical to the AuxIVA bound except that the quadratic form uses $\mathbf{V}_f^k + \mathbf{P}_f$ for constrained channels, where

$$
\mathbf{P}_f = \frac{\lambda_E\mathbf{I} + \mathbf{h}_f^k(\mathbf{h}_f^k)^{\mathrm{H}}}{\sigma_f^2}.
$$

Minimizing the bound with the sequential (IP-style) update strategy gives, for constrained channels $k \in \mathcal{I}$:

$$
\tilde{\mathbf{w}}_f^{k,(l+1)} = \left(\mathbf{W}_f^{(l)}\left[\mathbf{V}_f^{k,(l)} + \mathbf{P}_f\right]\right)^{-1}\mathbf{e}_k, \qquad
\mathbf{w}_f^{k,(l+1)} = \frac{\tilde{\mathbf{w}}_f^{k,(l+1)}}{\sqrt{(\tilde{\mathbf{w}}_f^{k,(l+1)})^{\mathrm{H}}\left[\mathbf{V}_f^{k,(l)} + \mathbf{P}_f\right]\tilde{\mathbf{w}}_f^{k,(l+1)}}},
$$

and the standard AuxIVA updates for unconstrained channels. The full procedure ("Informed IVA", Algorithm 1) is summarized as:

1. Initialize $\mathbf{W}_f^{(0)} = \mathbf{I}$.
2. For each iteration $l$ and each source $k$: estimate demixed-signal energies $r_n^k$ (22), per-frequency weighted covariances $\mathbf{V}_f^k$ (21).
3. Update constrained rows via $\mathbf{V}+\mathbf{P}$, unconstrained rows via $\mathbf{V}$ alone; demix with $\mathbf{y} = \mathbf{W}\mathbf{x}$.

Because the prior is quadratic, it simply **adds to the AuxIVA weighted covariance** — no step-size parameter appears and monotonic convergence is inherited from the MM construction.

## Experimental Setup

| Item | Value |
|------|-------|
| Scenario | $K = 2$ (female + male speech), determined, 2 mics, 0.21 m spacing |
| RIRs | Measured, 3 rooms: Room 1 ($T_{60} = 50$ ms, low-reverberant chamber), Room 2 ($T_{60} = 200$ ms), Room 3 ($T_{60} = 400$ ms, meeting rooms) |
| Source distance / DOA pairs | 1 m; Room 1: 45°/135°, 45°/90°, 20°/160°; Rooms 2–3: 50°/130°, 50°/90°, 10°/170° |
| Average DRRs | 6.8 dB (Room 1), 4.5 dB (Room 2), 3.3 dB (Room 3) |
| Noise | Additive white Gaussian at SNR ∈ {10, 20, 30} dB |
| STFT | Hamming window, length 2048, 50% overlap, 16 kHz |
| Source model | $G(r_n^k) = r_n^k$ for all methods |
| Prior parameters | $\sigma_f^2 = \tilde{\sigma}^2 = 40$ (constant over frequency), $\lambda_E = 10^{-3}$ |
| Baselines | auxIVA (Ono 2011, L = 100); GC gradIVA (Khan et al. 2015, L = 350, stepsize 0.05, constraint weight 0.5) |
| Metrics | SIR, SDR (Vincent et al. 2006 toolbox), averaged over all source configurations and directional constraints |
| Oracle note | Outer permutation of plain auxIVA resolved by oracle knowledge (GC variants resolve it algorithmically) |

## Results

![[raw/papers/brendel-2020-spatially-guided-iva/figures/11d3d1c33cbad15e9e23fe7ed7938b9790c48658bdb0ae7bee7d9113036eee26.jpg|SIR (first row) and SDR (second row), Room 1]]

![[raw/papers/brendel-2020-spatially-guided-iva/figures/71177537946c173da977361c5fa9de86729d98585ee71fbdaa19f0262ce73556.jpg|SIR (first row) and SDR (second row), Room 2]]

![[raw/papers/brendel-2020-spatially-guided-iva/figures/a9e221e49dd34fdd6c6aebdebd8d2de1cb7639cb88278fb044b5ea182b161b45.jpg|SIR (first row) and SDR (second row), Room 3]]

*Figure 1: SIR (first row) and SDR (second row) of the proposed GC auxIVA and the two benchmark algorithms auxIVA and GC gradIVA, averaged over different directional priors and source DOAs for the three rooms.*

- **SIR**: GC auxIVA achieves higher SIR than GC gradIVA in **all** scenarios and is comparable with (oracle-permutation) auxIVA.
- **SDR**: GC auxIVA is slightly below auxIVA — attributed to the free-field prior — but comparable with GC gradIVA. SDR decreases with $T_{60}$ for all algorithms due to decreasing DRR. SAR showed the same trends (omitted for space; comprehensive evaluation in the journal version, arXiv:2001.05958).
- **Convergence**: auxIVA and GC auxIVA converge almost identically — the spatial prior does **not** impair the AuxIVA convergence speed — and both are dramatically faster than GC gradIVA (Fig. 2).

![[raw/papers/brendel-2020-spatially-guided-iva/figures/bd9e79f200cad8243bbc7d6cd1498a6ae764499f0c5a1fd0f9c1ac6e88d2422f.jpg|Normalized IVA cost function values over iterations]]

*Figure 2: Exemplary behavior of the logarithmic normalized IVA cost function values (without the prior term) for the three investigated algorithms.*

- **Computational cost**: one iteration takes ~0.24 s (auxIVA / GC auxIVA) vs. ~0.15 s (GC gradIVA) on an Intel Core i7-5600U — GC auxIVA is slightly more expensive per iteration but needs far fewer iterations to converge, so it is **computationally cheaper overall**.
- Spatial aliasing did not visibly affect the prior in these experiments.

## Key Contributions

1. **MAP generalization of IVA**: first spatially informed formulation of IVA as a MAP estimation problem with a prior PDF over the demixing matrices (extending the Bayesian ICA view of Knuth 1999), reducing exactly to standard IVA under an uninformative prior.
2. **DOA-uncertainty-aware soft prior**: a Gaussian prior favoring spatial nulls toward given DOAs, whose variance $\tilde{\sigma}_f^2$ encodes localization confidence — enabling principled fusion with DOA localization/tracking algorithms — and whose $\lambda_E$ term Tikhonov-regularizes filter energy.
3. **MM update rules with unimpaired convergence**: the quadratic prior simply adds to the AuxIVA weighted covariance ($\mathbf{V} + \mathbf{P}$), preserving stepsize-free, monotonic AuxIVA convergence — unlike the earlier gradient-based GC-IVA of Khan et al. 2015.
4. **Empirical validation on measured RIRs**: higher SIR than GC gradIVA in all tested rooms/SNRs, comparable to oracle-permutation auxIVA, at lower total computational cost despite slightly costlier iterations.

## Related Concepts

- [[concepts/spatially-guided-iva|Spatially Guided IVA]] — the MAP-prior framework introduced by this paper
- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/geometrically-constrained-iva|Geometrically Constrained IVA]] — the hard-linear-constraint counterpart family
- [[concepts/spatial-regularization|Spatial Regularization]]
- [[concepts/permutation-alignment|Permutation Alignment]] — the outer permutation problem context
- [[concepts/relative-transfer-function|Relative Transfer Function]] — free-field RTF defines the prior's steering vector
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]] — DOA estimates (with uncertainty) parameterize the prior
- [[concepts/iterative-projection|Iterative Projection]] — the AuxIVA update family the MM derivation builds on
- [[concepts/natural-gradient|Natural Gradient]] — the alternative (slower) optimization family used by GC gradIVA

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] — spatially guided BSS within the multichannel enhancement toolbox

## Related Sources

- [[sources/ono-2011-stable-fast-update-rules-iva|Ono 2011: Stable and Fast Update Rules for IVA]] — the AuxIVA framework whose update rules this paper extends with the spatial prior
- [[sources/li-2020-geometrically-constrained-iva|Li & Koishida 2020: Geometrically Constrained IVA]] — concurrent hard-constraint alternative (GCAV-IVA)
- [[sources/nakatani-2022-switching-iva|Nakatani et al. 2022: Switching IVA]] — spatially guided initialization as an alternative injection point for spatial information
