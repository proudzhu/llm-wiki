---
type: concept
created: 2026-08-26
updated: 2026-08-26
sources:
  - raw/papers/kang-2019-low-complexity-permutation-alignment/full-text.md
tags:
  - blind-source-separation
  - audio-source-separation
  - permutation-alignment
  - signal-processing
---

# Permutation Alignment

**Permutation alignment** is the post-processing step of frequency-domain [[concepts/blind-source-separation|blind source separation]] that resolves the **permutation problem**: when ICA is applied independently to each STFT frequency bin, the ordering of the separated sources is arbitrary per bin, so bin-wise outputs must be re-aligned to a consistent global source order before inverse STFT. A single misaligned bin mixes different sources in the reconstructed time-domain signal, and errors in one bin can propagate to neighbors in sequential alignment schemes.

## The Permutation Problem

Per-bin ICA yields $\mathbf{y}(l,f) = \mathbf{W}(f)\mathbf{x}(l,f)$, defined only up to scaling and permutation: the ideal $\mathbf{W}(f)\mathbf{H}(f) = \mathbf{I}$ is relaxed to $\mathbf{P}(f)\mathbf{W}(f)\mathbf{H}(f) = \mathbf{D}(f)$ with an unknown per-bin permutation matrix $\mathbf{P}(f)$ and diagonal $\mathbf{D}(f)$. Scaling is fixed by the minimal distortion principle, $\boldsymbol{\Lambda}(f) = \operatorname{diag}(\mathbf{W}^{-1}(f))$; recovering $\mathbf{P}(f)$ for all bins is the alignment task.

## Method Families

| Family | Key idea | Representative | Weakness |
|--------|----------|----------------|----------|
| **DOA / spatial clustering** | Cluster per-bin source directions estimated from the (inverse) separation matrix | Sawada et al. 2004; Nesta et al. 2008 | Sensitive to reverberation |
| **Filter smoothness** | Enforce smooth separation matrices / spectral continuity across frequency | Asano et al. 2001; Smaragdis 1998; Servière & Pham 2006 | Only mitigates, doesn't resolve |
| **Envelope correlation** | Align adjacent bins by correlation of signal envelopes | Murata et al. 2001 | Weak dependence measure |
| **Power-ratio correlation** | Correlate bin-wise power-ratio sequences $v_i(l,f)$ (Sawada's measure); combine local + global optimization | Sawada et al. 2007; MBMC (Wang 2014); RG (Wang et al. 2011) | High iteration counts in the global stage |
| **Low-complexity three-stage** | Confidence-thresholded bin-wise alignment → local centroid correction → few-iteration global clustering | [[sources/kang-2019-low-complexity-permutation-alignment\|Kang, Yang & Yang 2019]] | — |

## Sawada's Dependence Measure

With $\mathbf{A}(f) = \mathbf{W}^{-1}(f)$, the power ratio of the $i$th separated signal in the mixture is

$$v_i(l, f) = \frac{\|\mathbf{a}_i(f)\, Y_i(l, f)\|^2}{\sum_{k=1}^{N} \|\mathbf{a}_k(f)\, Y_k(l, f)\|^2} \in [0, 1]$$

The correlation coefficient $\rho(\mathbf{v}_i(f_1), \mathbf{v}_j(f_2))$ between power-ratio sequences is high when both sequences stem from the same source — especially for neighboring bins — making it a sharper dependence measure than envelope correlation.

## Kang's Three-Stage Low-Complexity Method

[[sources/kang-2019-low-complexity-permutation-alignment|Kang, Yang & Yang 2019]] reorder the local/global decomposition for efficiency:

1. **Bin-wise alignment with confidence threshold**: fix a bin's permutation only if its average adjacent-bin correlation $\rho_f \geq U_{th}$ (good range $0.5$–$0.7$); defer low-confidence bins instead of guessing.
2. **Local centroid correction**: resolve deferred bins by correlating against a centroid $\mathbf{m}_k$ of the high-confidence bins, preventing misalignment spread.
3. **Fine global optimization**: one-centroid clustering converges in <5 iterations because stages 1–2 provide an excellent initialization — versus ~15 iterations when the global stage runs first (Sawada 2007, MBMC).

Result: separation quality on par with Sawada/MBMC (SIR/PESQ within ~0.1 dB / 0.02) at 4–5× lower permutation-stage runtime (7.3 s vs. 39.3–51.2 s for 4 sources, 10 s signals), with the saving growing in the number of sources.

## Relation to Other Ambiguity-Resolution Approaches

- **Built-in resolution**: [[concepts/independent-vector-analysis|IVA]], [[concepts/independent-low-rank-matrix-analysis|ILRMA]], and [[concepts/fastmnmf|FastMNMF]] avoid post-hoc alignment entirely by modeling source vectors jointly across frequency.
- **Learned resolution**: [[concepts/permutation-invariant-training|permutation invariant training]] is the deep-learning analog — it makes the *training loss* invariant to output permutation rather than aligning frequency bins.
- **Alternative regularizer**: [[concepts/spatial-regularization|spatial regularization]] uses DOA priors inside BSS optimization to keep permutations consistent, sidestepping the alignment problem from within the cost function.

## Related Concepts

- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/independent-low-rank-matrix-analysis|Independent Low-Rank Matrix Analysis]]
- [[concepts/permutation-invariant-training|Permutation Invariant Training]]
- [[concepts/spatial-regularization|Spatial Regularization]]

## Related Sources

- [[sources/kang-2019-low-complexity-permutation-alignment|Kang, Yang & Yang 2019: A Low-Complexity Permutation Alignment Method for Frequency-Domain BSS]]
- [[sources/sawada-2019-bss-ilrma-review|Sawada et al. 2019: BSS/ILRMA Review]] — treats the permutation problem as a central motivation for the IVA/ILRMA route
- [[sources/ansari-2023-ai-bss-survey|Ansari et al. 2023: AI Approaches in BSS Survey]]
