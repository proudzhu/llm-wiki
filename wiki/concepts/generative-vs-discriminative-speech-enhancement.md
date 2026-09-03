---
type: concept
created: 2026-09-03
updated: 2026-09-03
sources:
  - raw/papers/shetu-2026-generative-discriminative-comparison/full-text.md
tags:
  - speech-enhancement
  - generative-models
  - discriminative-models
  - gan
  - diffusion-models
  - model-complexity
---

# Generative vs. Discriminative Speech Enhancement

The two training paradigms for deep-learning speech enhancement (SE), formulated over the conditional distribution $p(\mathbf{x}_{0}\mid\mathbf{y})$ of clean speech given the noisy signal: **discriminative** methods learn a deterministic regression $\mathbf{x}_{0}\approx\mathcal{F}_{\theta}(\mathbf{y})$ via a signal- or mask-level loss; **generative** methods learn a transformation whose samples follow the clean-speech distribution conditioned on $\mathbf{y}$ — via GAN min–max training, denoising score matching (diffusion), conditional flow matching, or consistency objectives.

## Key Formulations

| Paradigm | Objective | Inference |
|----------|-----------|-----------|
| Discriminative | $\mathcal{L}_{\mathrm{disc}}=\mathbb{E}\left[\ell(\mathbf{x}_{0},\mathcal{F}_{\theta}(\mathbf{y}))\right]$ | single step |
| GAN | $\min_{\theta}\max_{\phi}\;\mathbb{E}\big[\mathcal{L}_{D}\big]+\mathbb{E}\big[\mathcal{L}_{G}\big]$ | single step |
| Diffusion (score matching) | $\mathcal{L}_{\mathrm{diff}}=\mathbb{E}\left[\|\bm{\epsilon}-\mathbf{S}_{\theta}(\mathbf{x}_{t},\mathbf{y},t)\|^{2}_{2}\right]$ | iterative (10–50 steps) |
| Flow matching (OT) | $\mathcal{L}_{\mathrm{CFM}}=\mathbb{E}\left[\|\mathbf{v}_{\theta}(\mathbf{x}_{t},\mathbf{y},t)-\mathbf{u}_{t}\|^{2}_{2}\right]$, $\mathbf{u}_{t}=\mathbf{x}_{0}-\mathbf{y}$ | few-step ODE |
| Consistency | $\mathcal{L}_{\mathrm{cons}}=\mathbb{E}\left[\|f_{\theta}(\mathbf{x}_{t_{n}},\mathbf{y},t_{n})-f_{\theta^{-}}(\mathbf{x}_{t_{n-1}},\mathbf{y},t_{n-1})\|^{2}_{2}\right]$ | single step |

## Empirical Trade-offs (Shetu, Habets & Brendel 2026)

The first controlled 14-model comparison (same NCSN++ backbone trained with diffusion, GAN, and discriminative objectives; ~1000-h DNS-derived datasets at high and low SNR) finds:

| Dimension | Discriminative | GAN | Diffusion/flow/consistency |
|-----------|----------------|-----|----------------------------|
| PESQ / SI-SDR / FwSegSNR (matched high- and low-SNR, mismatched) | competitive to good | **best** (NCSN++ (GAN), DisCoGAN) | SI-SDR comparable, PESQ/FwSegSNR poor at very low SNR |
| DNSMOS (non-intrusive, generative-quality proxy) | moderate | moderate | **slightly best** |
| Convergence | fastest (~200k steps) | fast (~250k steps, oscillating to 400k) | slow (BBED ~300–400k steps, PESQ never catches up) |
| Data efficiency | — | **best** (peak at 50 h) | worst (BBED needs ≥200 h) |
| Complexity (GMACs) | low | low | 60–100× higher for iterative methods |
| Hallucination (WER/CER/LPS) | — | less | slightly more |

Key insight: **the training objective, not the architecture, drives the gains** — the NCSN++ score-network backbone trained with a GAN objective (NCSN++ (GAN)) beats the same backbone trained as a diffusion model on nearly every metric at a fraction of the inference cost. Because SE benefits from strong conditioning on $\mathbf{y}$, the iterative generative machinery of diffusion offers no measurable complexity–performance advantage; generative methods are hypothesized to be more valuable for tasks that are inherently generative (speech synthesis, bandwidth extension) where such conditioning is absent.

## Related Concepts

- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/diffusion-models-for-speech|Diffusion Models for Speech Enhancement]]
- [[concepts/one-step-generative-models|One-Step Generative Models]]
- [[concepts/speech-enhancement-hallucination|Speech Enhancement Hallucination]]

## Related Sources

- [[sources/shetu-2026-generative-discriminative-comparison|Shetu, Habets & Brendel 2026: Generative vs. Discriminative SE]]
- [[sources/lugo-2026-diffvqe|Lugo et al. 2026: DiffVQE]] — single-step hybrid discriminative+generative design, a middle route
- [[sources/xu-2026-drifting-models-speech-enhancement|Xu et al. 2026: Drifting Models]] — one-step generative SE without trajectories
