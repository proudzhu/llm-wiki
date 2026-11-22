---
type: concept
created: 2026-09-03
updated: 2026-11-22
sources:
  - raw/papers/shetu-2026-generative-discriminative-comparison/full-text.md
  - raw/papers/pascual-2017-segan/full-text.md
  - raw/papers/fu-2019-metricgan/full-text.md
  - raw/papers/fu-2021-metricgan-plus/full-text.md
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

The generative branch of SE starts with [[sources/pascual-2017-segan|SEGAN (Pascual, Bonafonte & Serrà 2017)]] — the first GAN for enhancement: a waveform-level convolutional encoder–decoder trained with a [[concepts/least-squares-gan|least-squares adversarial loss]] plus an $L_1$ anchor ($\lambda = 100$) against a critic that scores (noisy, clean) against (noisy, enhanced) pairs. Two of its design choices recur throughout this page's later entries: the adversarial term is justified precisely by the failure of regression losses (MAE/MSE assume a unimodal output and bias the estimate to the conditional mean), and the $L_1$/adversarial balance is a hyperparameter with a wide inert region — at $\lambda = 1$ the anchor sat two orders of magnitude below the adversarial term and had no effect on learning. Its weaknesses are equally canonical: adversarial artifacts cost it PESQ against a plain Wiener filter (2.16 vs 2.22) even while it wins on subjective MOS (3.18 vs 2.70) and on CSIG/CBAK/COVL/SSNR.

## Key Formulations

A third position emerged between the two paradigms: [[sources/fu-2019-metricgan|**MetricGAN** (Fu et al., ICML 2019)]] trains a generator against a **learned surrogate of the evaluation metric** rather than against the clean signal or a real/fake boundary. Its discriminator regresses $Q'(G(\mathbf{x}),\mathbf{y}) \in [0,1]$ instead of classifying, and the generator minimizes $(D(G(\mathbf{x}),\mathbf{y}) - s)^2$ for an assigned score $s$. This is not a third generative model — it is a *conditional GAN whose adversarial objective has been re-pointed at a metric*, and the paper's own measurement shows why: the conventional adversarial term is inert for SE (IRM(CGAN) 2.002 PESQ vs IRM(L1) 2.033 at matched generator, no listener preference), whereas the metric surrogate moves PESQ to 2.133 and STOI to 0.768 at the same capacity. Since 2019 this has become the dominant way GAN machinery is used in SE: MetricGAN+ and CMGAN are benchmark fixtures, and later systems (LiSenNet, FastEnhancer) attach a MetricGAN-style discriminator as an *auxiliary* loss ($\lambda \approx 0.05$ or $10^{-3}$) rather than as the sole objective.

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

- [[sources/fu-2019-metricgan|Fu, Liao, Tsao & Lin 2019: MetricGAN]] — the metric-surrogate turn: the discriminator regresses PESQ/STOI instead of classifying, and the paper measures the conventional adversarial SE term as inert (IRM(CGAN) 2.002 vs IRM(L1) 2.033 PESQ at matched generator)
- [[sources/pascual-2017-segan|Pascual, Bonafonte & Serrà 2017: SEGAN]] — the first generative (GAN) SE system; establishes the canonical failure profile of adversarial training (sub-Wiener PESQ 2.16 vs 2.22, artifacts at high frequency) alongside its wins on CSIG/CBAK/COVL/SSNR and subjective MOS 3.18 vs 2.70
- [[sources/shetu-2026-generative-discriminative-comparison|Shetu, Habets & Brendel 2026: Generative vs. Discriminative SE]]
- [[sources/lugo-2026-diffvqe|Lugo et al. 2026: DiffVQE]] — single-step hybrid discriminative+generative design, a middle route
- [[sources/xu-2026-drifting-models-speech-enhancement|Xu et al. 2026: Drifting Models]] — one-step generative SE without trajectories
- [[sources/fu-2021-metricgan-plus|Fu et al. 2021: MetricGAN+]] — loss-over-architecture evidence at benchmark scale: the unchanged BLSTM magnitude-mask generator reaches PESQ 3.15 (vs 2.71 with MSE), beating attention-based (T-GSA 3.06) and phase-aware (DEMUCS 3.07, PHASEN 2.99) systems
