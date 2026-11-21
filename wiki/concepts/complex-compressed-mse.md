---
type: concept
created: 2026-07-17
updated: 2026-11-21
sources:
  - raw/papers/braun-2021-loss-functions-speech-enhancement/full-text.md
  - raw/papers/seidel-2024-bark-scale-nn-residual-suppression/full-text.md
  - raw/papers/lugo-2026-diffvqe/full-text.md
tags:
  - speech-enhancement
  - deep-learning
  - loss-function
  - training-objective
---

# Complex Compressed MSE (CCMSE)

The **spectral complex compressed mean-squared error (CCMSE)** is a training loss for speech-enhancement / acoustic-echo-control neural networks that combines a magnitude-only term with a phase-aware (complex) term, both evaluated on **compressed** spectral magnitudes. It was popularized for audio-visual speech separation by Ephrat et al. (ACM TOG 2018) and is a common choice for hybrid AEC postfilter training.

## Definition

Given an estimated spectrum $\tilde{S}_\ell(k) = |\tilde{S}_\ell(k)| e^{j\varphi_{\tilde{S}}(\ell,k)}$ and a target spectrum $S_\ell(k) = |S_\ell(k)| e^{j\varphi_S(\ell,k)}$, the CCMSE loss is

$$
\begin{aligned}
J^{\mathrm{CCMSE}} = \sum_{k,\ell} &\,(1-\alpha)\bigl||\tilde{S}_\ell(k)|^c - |S_\ell(k)|^c\bigr|^2 \\
&+ \alpha\bigl||\tilde{S}_\ell(k)|^c e^{j\varphi_{\tilde{S}}(\ell,k)} - |S_\ell(k)|^c e^{j\varphi_S(\ell,k)}\bigr|^2,
\end{aligned}
$$

where:

- $0 < \alpha < 1$ is a weighting factor balancing magnitude-only and phase-aware terms.
- $c \in (0, 1]$ is the **compression exponent** — typically $c = 0.3$ in AEC work (Seidel et al. 2024) — that compresses the dynamic range of spectral magnitudes so that the loss is not dominated by high-energy bins.
- The first term is a magnitude-only compressed MSE.
- The second term is a complex compressed MSE that takes phase into account.

## Role in Hybrid AEC Training

CCMSE is used as the training loss for several hybrid AEC neural postfilters, including:

- [[sources/seidel-2024-bark-scale-nn-residual-suppression\|Seidel et al. 2024]] — used with $c = 0.3$ and an STFT-consistency enforcement on the estimated signal $\tilde{S}$.
- [[sources/lugo-2026-diffvqe\|Lugo et al. 2026 (DiffVQE)]] — the same $J^{CC}$ is applied twice in the hybrid diffusion AEC loss: once to the discriminative Cond DNN estimate $\hat{\mathbf{S}}^{\mathrm{cond}}$ and once to the post-diffusion output $\hat{\mathbf{S}}$, combined with a denoising score-matching term weighted by $\alpha = 0.005$.

## Relation to the Braun & Tashev Compressed Losses

[[sources/braun-2021-loss-functions-speech-enhancement|Braun & Tashev 2021]] tabulate the compressed losses as two separate rows of their taxonomy — magnitude-only $\langle|\widehat{A}^c-A^c|^2\rangle$ (magComp) and compressed complex (cComp) — and only then mix them, which is exactly the CCMSE form with $\alpha=\beta$:

$$
\mathcal{L}_{\mathrm{mix}} = (1-\beta)\left\langle|\widehat{A}^c-A^c|^2\right\rangle + \beta\left\langle|\widehat{S}^c-S^c|^2\right\rangle .
$$

Their measurements on reverberant CHiME-2 (real-valued gain predictor) give the exponents' operating point that later AEC work inherits: $c=0.3$, $\beta=0.3$, mixed PESQ 3.31 vs. 3.25 magnitude-only and 2.88 complex-only. The two-part structure is therefore not cosmetic — the complex compressed term alone is the weakest complex loss in their study.

## Why Compression?

The compression exponent $c$ applies a power-law nonlinearity $|S|^c$ to spectral magnitudes. With $c < 1$ (e.g., $c = 0.3$):

- High-energy bins (e.g., voiced speech harmonics) are attenuated relative to low-energy bins.
- The loss is less dominated by loud spectral peaks and pays more attention to perceptually relevant low-energy content.
- Mimics the loudness compression of human hearing, similar to the motivation for [[concepts/bark-scale-spectral-features\|Bark-scale]] or log-power features.

## Why Phase-Awareness?

The complex term $(\alpha)$ penalizes phase errors in addition to magnitude errors. This is especially important in hybrid AEC, where the residual echo $\Delta D$ has its own phase structure that the neural mask must suppress without distorting nearend speech phase.

## Related Concepts

- [[concepts/bark-scale-spectral-features\|Bark-Scale Spectral Features]]
- [[concepts/stft-consistency\|STFT Consistency]]
- [[concepts/nsnet2\|NSNet2]]
- [[concepts/mixed-magnitude-complex-loss|Mixed Magnitude-Complex Loss]] — the general $(1-\beta)$/$\,\beta$ rule of which CCMSE ($\alpha$) is the compressed instance
- [[concepts/speech-enhancement\|Speech Enhancement]]

## Related Sources

- [[sources/braun-2021-loss-functions-speech-enhancement|Braun & Tashev 2021: A Consolidated View of Loss Functions]] — measures the two compressed terms separately and then mixes them at $\beta=0.3$: mixed 3.31 PESQ vs. 3.25 magnitude-only and 2.88 complex-only, i.e. the $\alpha$-weighted structure is what makes the loss work
- [[sources/seidel-2024-bark-scale-nn-residual-suppression|Seidel, Mowlaee & Fingscheidt 2024]] — uses CCMSE with $c = 0.3$ for training the Bark-scale postfilter
- [[sources/lugo-2026-diffvqe\|Lugo et al. 2026: DiffVQE]] — double CCMSE term in a single-step hybrid diffusion AEC objective
