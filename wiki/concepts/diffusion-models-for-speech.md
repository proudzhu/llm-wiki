---
type: concept
created: 2026-05-03
updated: 2026-09-03
sources:
  - raw/papers/xu-2026-drifting-models-speech-enhancement/full-text.md
  - raw/papers/lugo-2026-diffvqe/full-text.md
  - raw/papers/shetu-2026-generative-discriminative-comparison/full-text.md
tags:
  - speech-enhancement
  - generative-models
  - diffusion-models
---

# Diffusion Models for Speech Enhancement

**Diffusion models for speech enhancement** apply score-based generative modeling to the denoising problem, defining a forward process that gradually corrupts clean speech into noise and a reverse process that recovers clean speech from noisy observations.

## Overview

Score-based diffusion models have established state-of-the-art performance in speech enhancement by modeling the gradient of the log-density of the clean speech distribution. The reverse dynamics can be formulated as either a Stochastic Differential Equation (SDE) or a deterministic Probability Flow ODE (PF-ODE) sharing the same marginal densities.

However, their inference is inherently iterative — numerically integrating the reverse-time trajectories requires 10–100 discretization steps, resulting in a high Number of Function Evaluations (NFE) that creates a latency bottleneck for real-time applications.

## Acceleration Strategies

### Trajectory Compression
- **Hybrid approaches**: Combine predictive models with a small number of diffusion refinement steps (e.g., Storm, Trachu et al.)
- **Diffusion-GAN hybrids**: Further reduce steps via adversarial training
- **Consistency Models**: Enforce self-consistency along the PF-ODE to distill a multi-step sampler into a single-step mapping (ROSE-CD, SBCTM)

### Trajectory Linearization
- **Flow Matching**: Learn a vector field that defines a probability path from noise to data
- **Rectified Flow**: Explicitly straightens the transport path to minimize ODE curvature
- **MeanFlow**: Learns a continuous mean velocity field to model probability paths

### Beyond Trajectories
- **[[drifting-models|Drifting Models]]**: Reformulate generation as a distributional equilibrium problem, achieving native one-step inference without any trajectory (DriftSE)

### Single-Step Hybrid Discriminative + Generative (EffDiffSE lineage)

A complementary route to 1-NFE diffusion is a **hybrid discriminative+generative** design: a discriminative Cond DNN predicts a first estimate $\hat{\mathbf{S}}^{\mathrm{cond}}$, which initializes the reverse process at $t = T$; a generative Score DNN then applies a **single** noise-consistent Langevin correction step. Matched-condition training at $\tilde{t} = T$, denoising score matching, and Karras preconditioning yield stable single-step inference. [[sources/lugo-2026-diffvqe|DiffVQE (Lugo et al. 2026)]] brings this EffDiffSE-style framework to joint [[concepts/acoustic-echo-cancellation|acoustic echo control]] + denoising: it outperforms the discriminative DeepVQE baseline on most quality/intelligibility metrics (PESQ, ESTOI, LPS, AECMOS Other) at ~10–13% of its FLOPS, with RTF 0.172–0.185 on CPU — evidence that generative SE can be single-step without a distillation teacher.

## Representative Methods on VoiceBank-DEMAND

| Method | NFE | PESQ | SI-SDR | Approach |
|--------|-----|------|--------|----------|
| SGMSE+ | 30 | 2.90 | 16.90 | Score-based diffusion |
| ROSE-CD | 1 | 3.49 | 17.80 | Consistency distillation |
| SBCTM | 1 | 3.56 | 12.70 | Schrödinger bridge + consistency |
| MeanFlowSE | 1 | 2.81 | 19.97 | Mean flow |
| DriftSE | 1 | 3.15 | 16.10 | Drifting models (equilibrium) |

## Head-to-Head with GAN and Discriminative Training (Shetu 2026)

[[sources/shetu-2026-generative-discriminative-comparison|Shetu, Habets & Brendel 2026]] train SGMSE+ (30 steps), BBED, SToRM (50 steps), GALDSE, FlowSE, and SEBridge (consistency, 1 step) alongside GAN and discriminative models on ~1000-h DNS-derived data. Findings:

- **Diffusion lags on PESQ/FwSegSNR at low SNR**: at matched low SNR, diffusion models match GAN ΔSI-SDR (FlowSE: 16.80/15.59/13.63 dB across [-11,-8]/[-7,-4]/[-3,0] dB) but lose clearly on ΔPESQ and ΔFwSegSNR — attributed to over-denoising or oscillations while converging in extremely low SNR.
- **DNSMOS is the one metric favoring diffusion** (GALDSE 4.15 vs clean 4.01), consistent with stronger generative capability.
- **Slow convergence and data hunger**: BBED needs ~300–400k training steps (vs ~250k for GAN) and ≥200 h of data to reach peak (GAN peaks at 50 h).
- **60–100× GMACs cost**: iterative SGMSE+/SToRM are 60–100× more expensive than single-step GAN/discriminative models; FlowSE/SEBridge cut NFEs to 1–5 but retain the expensive NCSN++ backbone. Under these conditions diffusion shows no complexity–performance advantage over the same backbone GAN-trained (NCSN++ (GAN)).

See [[concepts/generative-vs-discriminative-speech-enhancement|Generative vs. Discriminative Speech Enhancement]] for the full paradigm comparison.

## Related Concepts

- [[concepts/drifting-models|Drifting Models]]
- [[concepts/one-step-generative-models|One-Step Generative Models]]
- [[concepts/self-supervised-speech-representation|Self-Supervised Speech Representation]]
- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]]
- [[concepts/urgent-challenge|URGENT Challenge]]
- [[concepts/generative-vs-discriminative-speech-enhancement|Generative vs. Discriminative Speech Enhancement]]
- [[concepts/speech-enhancement-hallucination|Speech Enhancement Hallucination]]

## Related Sources

- [[sources/xu-2026-drifting-models-speech-enhancement|Xu et al. 2026: Speech Enhancement Based on Drifting Models]]
- [[sources/lugo-2026-diffvqe|Lugo et al. 2026: DiffVQE]] — first reproducible diffusion-based AEC; single-step hybrid Cond/Score framework (EffDiffSE lineage)
- [[sources/shetu-2026-generative-discriminative-comparison|Shetu, Habets & Brendel 2026: Generative vs. Discriminative SE]] — controlled comparison of six diffusion/flow/consistency models against GAN and discriminative training
