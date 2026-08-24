---
type: concept
created: 2026-08-22
updated: 2026-08-24
sources:
  - raw/papers/ruan-2024-speech-extraction-low-snr/full-text.md
  - raw/papers/scheibler-2020-fast-independent-vector-extraction/full-text.md
tags:
  - blind-source-extraction
  - independent-vector-extraction
  - optimization-algorithms
  - convergence-analysis
---

# OGIVE

**OGIVE** (Independent Vector Extraction with the Orthogonal Constraint) is the gradient-ascent instantiation of [[concepts/independent-vector-extraction|IVE]]. The **orthogonal constraint (OG)** — $(1/J)\sum_j s_{ij}\mathbf{z}_{ij}^* = \mathbf{0}$, i.e., decorrelation of the source of interest (SOI) and background (BG) — links the mixing and demixing vectors through the mixture covariance:

$$\mathbf{w}_i = \frac{(\hat{\mathbf{C}}_{\mathbf{x}}^i)^{-1}\mathbf{a}_i}{\mathbf{a}_i^{\mathrm{H}}(\hat{\mathbf{C}}_{\mathbf{x}}^i)^{-1}\mathbf{a}_i}, \qquad \mathbf{a}_i = \frac{\hat{\mathbf{C}}_{\mathbf{x}}^i \mathbf{w}_i}{\mathbf{w}_i^{\mathrm{H}}\hat{\mathbf{C}}_{\mathbf{x}}^i \mathbf{w}_i}$$

so the IVE likelihood can be optimized over *either* $\{\mathbf{a}_i\}$ *or* $\{\mathbf{w}_i\}$.

## Variant Family

| Variant | Optimization term | Gradient | Notes |
|---|---|---|---|
| OGIVEw | demixing vector $\mathbf{w}_i$ | ordinary | Advantageous at high SNR |
| OGIVEa | mixing vector $\mathbf{a}_i$ | ordinary | Advantageous at extremely low SNR; needs $\lambda(\mathbf{a}_i)$ weighting |
| OGIVEs | switched $\mathbf{w} \leftrightarrow \mathbf{a}$ | ordinary | Switches by SNR level |
| OGIVEw_NG | $\mathbf{w}_i$ | natural | Proposed by Ruan et al. 2024 |
| OGIVEa_NG | $\mathbf{a}_i$ | natural | Proposed by Ruan et al. 2024; best performer at −20 dB |

The ordinary-gradient updates are $\Delta\mathbf{w}_i = \mathbf{a}_i - J^{-1}\sum_j \mathbf{x}_{ij}\varphi_i(\mathbf{s}_j)$ and $\Delta\mathbf{a}_i = \mathbf{w}_i - J^{-1}\lambda(\mathbf{a}_i)(\hat{\mathbf{C}}_{\mathbf{x}}^i)^{-1}\sum_j \mathbf{x}_{ij}\varphi_i(\mathbf{s}_j)$; the natural-gradient versions premultiply by $\mathbf{W}_i^{\mathrm{H}}\mathbf{W}_i$ / $\mathbf{A}_i\mathbf{A}_i^{\mathrm{H}}$ (see [[concepts/natural-gradient|Natural Gradient]]) and avoid matrix inversions.

## Convergence-Region (ROC) Analysis

Plotting the OGIVE cost on real speech against $\mathbf{w} = [1, w]^{\mathrm{T}}$ and $\mathbf{a} = [1, a]^{\mathrm{T}}$ at different SNR reveals **which parameterization to optimize**:

![[raw/papers/ruan-2024-speech-extraction-low-snr/figures/ca416ce4cd7ae04b99dfda7ad6449c5d5ec6e99e11d3513c7319a1d1e96032f6.jpg|Cost function vs demixing parameter w at SNR = −20/0/20 dB]]

*Figure 1 (Ruan et al. 2024): cost w.r.t. the demixing parameter $\mathbf{w}$ with Gaussian noise at SNR = (a) −20 dB, (b) 0 dB, (c) 20 dB.*

![[raw/papers/ruan-2024-speech-extraction-low-snr/figures/126bea871ef7365452b9b6cc8cd70e5ad1e7964df1099d662c32f03b3a2d6d5f.jpg|Cost function vs mixing parameter a at SNR = −20/0/20 dB]]

*Figure 2 (Ruan et al. 2024): cost w.r.t. the mixing parameter $\mathbf{a}$. At −20 dB the desired solution's region of convergence is wide and flat — solutions with offset barely degrade performance — while the demixing landscape (Fig. 1) is sharp and hard to hit. At +20 dB the roles reverse.*

- **Extremely low SNR**: optimize $\mathbf{a}$ (wide flat ROC around the SOI solution; OGIVEa converges robustly, and offset solutions cost little).
- **High SNR**: optimize $\mathbf{w}$.
- **Sparse interference** (e.g., competing speech): a local optimum appears at the BG solution $a = 1$, but its ROC stays narrow/sharp while the desired ROC remains wide/flat — $\mathbf{a}$-optimization stays robust.

The same analysis explains convergence behavior: demixing-vector methods drift to the *dominant* source (the noise at −20 dB), mixing-vector methods extract the *weak* source; the natural gradient removes OGIVEa's unstable convergence and OGIVEw's below-start degradation.

## Comparison with FIVE

The auxiliary-function-based [[concepts/fast-independent-vector-extraction|FIVE]] is the fast counterpart of OGIVE within the IVE family: in Scheibler & Ono's (2020) experiments, FIVE reaches peak SDR improvement in **one to three iterations**, while gradient-ascent OGIVE (4000 iterations, step size 0.1) converges much more slowly, eventually reaching similar SDR improvement only outside the plotted runtime range. Both share the Gaussian-background blind spot — under background-model mismatch (few interferers) FIVE and OGIVE degrade similarly, where model-free AuxIVA is markedly more robust.

## Related Concepts

- [[concepts/independent-vector-extraction|Independent Vector Extraction]]
- [[concepts/fast-independent-vector-extraction|Fast Independent Vector Extraction]]
- [[concepts/blind-source-extraction|Blind Source Extraction]]
- [[concepts/natural-gradient|Natural Gradient]]
- [[concepts/independent-vector-analysis|Independent Vector Analysis]]

## Related Sources

- [[sources/ruan-2024-speech-extraction-low-snr|Ruan, Liao, Chen & Lu 2024: Speech Extraction Under Extremely Low SNR Conditions]]
- [[sources/guo-2023-iva-survey|Guo, Luo & Li 2023: IVA Survey]]
- [[sources/scheibler-2020-fast-independent-vector-extraction|Scheibler & Ono 2020: Fast Independent Vector Extraction]]
