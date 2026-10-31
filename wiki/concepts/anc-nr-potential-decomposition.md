---
type: concept
created: 2026-10-31
updated: 2026-10-31
sources:
  - raw/papers/zhang-2020-coherence-mcanc-noise-reduction/full-text.txt
tags:
  - active-noise-control
  - multichannel-anc
  - coherence
  - performance-bounds
---

# ANC NR-Potential Decomposition

**ANC NR-potential decomposition** is the algorithm-independent performance-analysis framework of [[entities/jihui-aimee-zhang|Jihui Aimee Zhang]] et al. ([[sources/zhang-2020-coherence-mcanc-noise-reduction|JASA 2020]]): the residual-error energy of an arbitrary multichannel feedforward ANC system is decomposed into three physically interpretable terms, revealing the fundamental limit of noise reduction for a given transducer configuration and noise field — *before* any adaptive algorithm is chosen or run.

## The Three Terms

For a system with $P$ references, $L$ secondary sources, and $Q$ error microphones, the total residual energy at each frequency decomposes as $E_T = E_{T1} + E_{T2} + E_{T3}$:

| Term | Name | Physical meaning | When zero / minimized |
|------|------|------------------|------------------------|
| $E_{T1}$ | **Signal coherence** | Primary energy on each secondary-path eigen channel not linearly explainable by the reference eigen components — the generalized coherence limit | Only if references are fully coherent with the primary field on every reachable eigen channel |
| $E_{T2}$ | **Filter** | Weighted distance of the control filters from the optimum | Exactly zero for the closed-form optimal filter $\hat{w}_{rz}^{o} = -S_{\hat{\mu}_r c_z}/(\sigma_r k_z)$ |
| $E_{T3}$ | **System null space** | Primary energy projected onto the $\mathbf{G}$ null space ($r > R = \mathrm{rank}(\mathbf{G})$) — uncontrollable by *any* filter | Only if $\mathrm{rank}(\mathbf{G}) = Q$ (enough independent secondary paths) |

## Derivation Mechanism

Two matrix decompositions convert the MIMO system into **parallel eigen channels**, one per nonzero singular value $\sigma_r$ of the secondary path $\mathbf{G} = \mathbf{A}\mathbf{R}\mathbf{B}^H$:

1. **SVD of $\mathbf{G}$** — projects the error space onto left singular vectors $\mathbf{a}_r$; only $R \le \min(Q, L)$ directions are reachable.
2. **Eigendecomposition of $\mathbf{S}_{xx} = \mathbf{U}\mathbf{K}\mathbf{U}^H$** — transforms the $P$ correlated references into $Z \le P$ *uncorrelated* eigen references $\mathbf{c}$ with PSDs $k_z$ (the reference PSD matrix is typically ill-conditioned, so $Z$ meaningful eigen channels exist).

Each channel then behaves like a single-channel ANC problem between the projected primary signal $\hat{\mu}_r = \mathbf{a}_r^H\boldsymbol{\mu}$ and the eigen references, and the classical single-channel coherence bound applies *per channel*: $E_{T1} = \sum_r (1 - \sum_z C_{\hat{\mu}_r c_z}) S_{\hat{\mu}_r \hat{\mu}_r}$, where $\sum_z C_{\hat{\mu}_r c_z}$ is the multiple coherence of $\hat{\mu}_r$ w.r.t. the eigen references.

## Relation to Other Bounds

- **Single-channel coherence limit** (Kuo & Morgan 1996): $\mathrm{NR}_{\max}(f) = -10\log_{10}[1 - \gamma^2_{\mu x}(f)]$ — recovered exactly as the $Q = P = L = 1$ scalar special case; the decomposition is its multichannel generalization.
- **[[concepts/multiple-coherence-function|Multiple Coherence Function (MCF)]]** bounds multi-reference feedforward attenuation at $-10\log_{10}(1 - \eta_{ud}^2)$ for a *single* error point; this framework additionally handles $Q > 1$ error microphones and exposes the null-space term $E_{T3}$ that the MCF formulation does not isolate. Both are frequency-domain bounds blind to causality ([[sources/forster-2022-optimal-microphone-positioning|Forster et al. 2022]] show the MCF overestimates gains from acausal filters).
- **[[concepts/anc-attenuation-bounds|ANC attenuation bounds]]** (Liebich et al.): amplitude/phase-matching bounds on the anti-noise at a point — the *signal-level* counterpart to this *statistical/system-level* bound.

## Practical Use

Because $E_{T1}/E_{T2}/E_{T3}$ are computable from pre-measurable quantities ($\mathbf{S}_{mx}$, $\mathbf{S}_{mm}$, $\mathbf{S}_{xx}$, $\mathbf{G}$), the framework serves as an offline **configuration-design tool**: predict the maximum NR and its limiting factor for candidate transducer counts/placements before deployment. The JASA experiments show:

- **Reference starvation dominates**: with $P = 1$ reference and 4 error mics / 4 sources (case 3), NR collapses via the $E_{T1}$ coherence term.
- **Error-mic surplus over sources surfaces the null space**: with $Q = 9$ error mics and $L = 4$ sources (case 2), $E_{T3}$ becomes comparable to $E_{T1}$ — more sensing than actuation creates uncontrollable directions.
- For the follow-up multichannel feedback-mitigation line from the same ANU group, see [[sources/zhang-2026-feedback-path-mitigation-mcanc|Zhang et al. 2026]] — acoustic feedback from secondary sources to references was the explicitly deferred limitation of this framework.

## Related Concepts

- [[concepts/multi-channel-anc|Multi-Channel ANC]]
- [[concepts/broad-band-feedforward-anc|Broad-Band Feedforward ANC]]
- [[concepts/multiple-coherence-function|Multiple Coherence Function (MCF)]]
- [[concepts/anc-attenuation-bounds|ANC Attenuation Bounds]]
- [[concepts/singular-value-decomposition|Singular Value Decomposition]]
- [[concepts/spatial-coherence|Spatial Coherence]]

## Related Sources

- [[sources/zhang-2020-coherence-mcanc-noise-reduction|Zhang, Murata, Maeno, Samarasinghe, Abhayapala & Mitsufuji 2020: Coherence-Based Performance Analysis on Noise Reduction in Multichannel ANC]] — the originating paper
