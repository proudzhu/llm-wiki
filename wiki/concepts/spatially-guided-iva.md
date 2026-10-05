---
type: concept
created: 2026-10-05
updated: 2026-10-05
sources:
  - raw/papers/brendel-2020-spatially-guided-iva/full-text.md
tags:
  - blind-source-separation
  - independent-vector-analysis
  - direction-of-arrival
  - spatial-processing
  - bayesian-inference
  - optimization-algorithms
---

# Spatially Guided IVA

**Spatially guided IVA** is the Maximum A Posteriori (MAP) formulation of [[concepts/independent-vector-analysis|Independent Vector Analysis]] introduced by [[entities/andreas-brendel|Brendel]], [[entities/thomas-haubner|Haubner]] & [[entities/walter-kellermann|Kellermann]] (ICASSP 2020), in which a **prior probability density over the demixing matrices** injects spatial (direction-of-arrival) knowledge into the otherwise blind separation objective. It steers IVA toward a desired solution and precludes the **outer permutation problem** — the ambiguity of which broadband output channel carries which source — without any post-hoc association of outputs to directions. With an uninformative prior, the MAP problem reduces exactly to the standard IVA cost function, making it a strict probabilistic generalization of IVA (extending Knuth's Bayesian view of ICA to the convolutive, multivariate case).

## Key Formulations

### MAP Objective

Marginalizing the demixed signals out of the joint posterior (with a Dirac-delta likelihood for the deterministic mixing relation) gives

$$
p(\mathcal{W} \mid \mathcal{X}) \propto p(\mathcal{W}) \prod_{f=1}^{F} |\det \mathbf{W}_f|^{2N} \prod_{n,k} p\left(\underline{\mathbf{y}}_{k,n}\right),
$$

so the MAP cost function is $J(\mathcal{W}) = J_{\mathrm{IVA}}(\mathcal{W}) + J_{\mathrm{prior}}(\mathcal{W})$: the original IVA cost plus a nonnegative term from the prior's negative log-likelihood.

### DOA-Uncertainty-Aware Gaussian Prior

The prior on each demixing vector $\mathbf{w}_f^k$ is a complex Gaussian that favors a **spatial null** toward the source DOA $\vartheta_k$:

$$
p(\mathbf{w}_f^k) \propto \exp\left(-\frac{1}{\tilde{\sigma}_f^2}(\mathbf{w}_f^k)^{\mathrm{H}}\left(\lambda_E\mathbf{I} + \mathbf{h}_f^k(\mathbf{h}_f^k)^{\mathrm{H}}\right)\mathbf{w}_f^k\right),
$$

where $\mathbf{h}_f^k$ is the free-field [[concepts/relative-transfer-function|relative transfer function]] at DOA $\vartheta_k$. Two design parameters carry physical meaning:

- $\tilde{\sigma}_f^2$ — the **uncertainty of the DOA estimate**; user-defined in the paper, but directly obtainable from a localization or tracking algorithm, enabling principled fusion of localization confidence into separation.
- $\lambda_E\mathbf{I}$ — a **Tikhonov regularization** of the filter energy that keeps the prior proper and the demixing filters well-behaved.

Only channels in a constrained set $\mathcal{I}$ receive the informative prior; $|\mathcal{I}| = K-1$ priors suffice to disambiguate $K$ sources.

### MM (AuxIVA-Style) Updates

Because the prior is quadratic, its contribution $\mathbf{P}_f = (\lambda_E\mathbf{I} + \mathbf{h}_f^k(\mathbf{h}_f^k)^{\mathrm{H}})/\sigma_f^2$ (with $\sigma_f^2 = N\tilde{\sigma}_f^2$) simply **adds to the AuxIVA weighted covariance** in the majorize-minimize upper bound: constrained rows update with $\mathbf{V}_f^k + \mathbf{P}_f$ via the standard sequential (IP-style) rule, unconstrained rows with $\mathbf{V}_f^k$ alone. This inherits AuxIVA's guaranteed monotonic convergence and stepsize-free operation — the spatial prior does **not** impair convergence speed relative to plain auxIVA.

## Evidence

On measured RIRs (2 mics, 0.21 m spacing; $T_{60}$ = 50–400 ms; DRR 3.3–6.8 dB; SNR 10–30 dB), the resulting algorithm (called **GC auxIVA** in the paper) achieved:

- Higher SIR than the gradient-based geometrically constrained IVA of Khan et al. 2015 (**GC gradIVA**) in all scenarios, comparable with oracle-permutation auxIVA;
- SDR slightly below auxIVA (a price of the free-field prior) but comparable with GC gradIVA;
- Convergence nearly identical to auxIVA and dramatically faster than GC gradIVA — slightly costlier per iteration (~0.24 s vs. 0.15 s on an i7-5600U) but far fewer iterations, hence cheaper overall.

## Position within the Spatially Informed BSS Family

Spatial information can enter BSS at three points; spatially guided IVA occupies the *prior/penalty* slot:

| Injection point | Mechanism | Representative |
|:----------------|:----------|:---------------|
| **Prior/penalty on the objective** | Probabilistic MAP prior (quadratic penalty) on demixing vectors | Spatially guided IVA (this page; Brendel et al. 2020); [[concepts/spatial-regularization\|spatial regularization]] (steering-proximity penalty, SR-ILRMA/SR-SwIVA) |
| **Hard linear constraints** | LCMV-style response constraints (null or distortionless) added to the AuxIVA bound | [[concepts/geometrically-constrained-iva\|Geometrically Constrained IVA]] (GCAV-IVA, GC-AuxIVA-ISS) |
| **Initialization** | Spatially guided filter initialization only | Spatially-guided MPDR initialization of [[concepts/switching-independent-vector-analysis\|swIVA]]/[[concepts/switching-civa\|swCIVA]] (Nakatani et al. 2022) |

Its distinguishing features: the guidance is **soft and probabilistic** (graded by $\tilde{\sigma}_f^2$, unlike hard response constraints), it offers a principled interface to **DOA-tracker uncertainty**, and it composes transparently with the AuxIVA machinery. The gradient-based GC-IVA of Khan et al. 2015 is the closest predecessor but requires step-size tuning and converges much more slowly.

## Related Concepts

- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/geometrically-constrained-iva|Geometrically Constrained IVA]]
- [[concepts/spatial-regularization|Spatial Regularization]]
- [[concepts/permutation-alignment|Permutation Alignment]]
- [[concepts/relative-transfer-function|Relative Transfer Function]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/iterative-projection|Iterative Projection]]

## Related Sources

- [[sources/brendel-2020-spatially-guided-iva|Brendel, Haubner & Kellermann 2020: Spatially Guided Independent Vector Analysis]] — the founding paper: MAP derivation, DOA-uncertainty prior, MM updates, measured-RIR evaluation vs. auxIVA and GC gradIVA
- [[sources/li-2020-geometrically-constrained-iva|Li & Koishida 2020: Geometrically Constrained IVA]] — the hard-constraint counterpart (concurrent work)
- [[sources/nakatani-2022-switching-iva|Nakatani et al. 2022: Switching IVA]] — the initialization-based counterpart
