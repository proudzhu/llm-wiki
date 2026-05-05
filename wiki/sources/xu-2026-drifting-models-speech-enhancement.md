---
type: source
created: 2026-05-03
updated: 2026-05-03
sources:
  - raw/papers/xu-2026-drifting-models-speech-enhancement/full-text.md
  - https://doi.org/10.48550/arXiv.2604.24199
  - zotero://select/items/0_DP6PSJ6C
tags:
  - speech-enhancement
  - generative-models
  - diffusion-models
  - drifting-models
  - one-step-inference
  - self-supervised-learning
---

# Xu, Caviedes-Nozal, Kleijn, Yan & Olsson 2026: Speech Enhancement Based on Drifting Models

**Authors**: [[../entities/liang-xu|Liang Xu]]¹, [[../entities/diego-caviedes-nozal|Diego Caviedes-Nozal]]², [[../entities/bastiaan-kleijn|Bastiaan Kleijn]]¹, [[../entities/longfei-yan|Longfei Felix Yan]]¹, [[../entities/rasmus-kongsgaard-olsson|Rasmus Kongsgaard Olsson]]²

**Affiliations**: ¹ Victoria University of Wellington, New Zealand · ² GN Audio A/S, Denmark

**Published**: arXiv preprint, 2026 (arXiv:2604.24199) — Submitted to Interspeech 2026

**Type**: Preprint (Conference submission)

**DOI**: [10.48550/arXiv.2604.24199](https://doi.org/10.48550/arXiv.2604.24199)

**Zotero**: [DP6PSJ6C](zotero://select/items/0_DP6PSJ6C)

## Summary

Proposes DriftSE, a generative speech enhancement framework that reformulates denoising as a distributional equilibrium problem. By evolving the pushforward distribution of a mapping function to match the clean speech distribution via a learned Drifting Field, DriftSE achieves native one-step inference (1 NFE). The direct mapping variant achieves PESQ 3.15 and SI-SDR 16.1 dB on VoiceBank-DEMAND, while the conditional variant achieves SCOREQ 4.33. On the DNS Challenge 2020 blind test set, DriftSE achieves state-of-the-art WV-MOS 2.65 and SCOREQ 2.97, demonstrating strong real-world generalization.

## Problem Formulation

Current diffusion-based speech enhancement methods require iterative sampling (10–100 NFE), creating a latency bottleneck for real-time applications. Existing acceleration strategies fall into two categories:

1. **Trajectory compression**: Reduce steps via distillation (consistency models) or hybrid approaches (predictive + diffusion refinement)
2. **Trajectory linearization**: Flow matching / rectified flow to straighten ODE paths, but still require discretization

Both approaches remain fundamentally trajectory-based. DriftSE instead reformulates enhancement as finding a **distributional equilibrium** — no trajectory, no iterative sampling.

## Methodology

### Drifting Models Background

Given source distribution $p_\epsilon$ (e.g., Gaussian noise) and mapping function $f_\theta$, the pushforward distribution is $q_\theta = (f_\theta)_\# p_\epsilon$. The **Drifting Field** $\mathbf{V}_{p,q}$ is a correction vector at each generated sample that points toward the data distribution:

$$\mathbf{x}_{\text{target}} \leftarrow \mathbf{x} + \mathbf{V}_{p,q}(\mathbf{x})$$

At equilibrium: $q_\theta = p_{\text{data}} \Rightarrow \mathbf{V}_{p,q}(\mathbf{x}) = \mathbf{0}, \forall \mathbf{x}$.

The drifting field decomposes into attraction and repulsion forces (inspired by mean-shift theory):

$$\mathbf{V}_{p,q}(\mathbf{x}) = \mathbf{V}_p^+(\mathbf{x}) - \mathbf{V}_q^-(\mathbf{x})$$

which unifies into:

$$\mathbf{V}_{p,q}(\mathbf{x}) = \frac{1}{Z_p Z_q} \mathbb{E}_{p,q}\left[k(\mathbf{x}, \mathbf{y}^+) k(\mathbf{x}, \mathbf{y}^-)(\mathbf{y}^+ - \mathbf{y}^-)\right]$$

with exponential similarity kernel $k_\tau(\mathbf{x}, \mathbf{y}) = \exp\left(-\|\mathbf{x} - \mathbf{y}\|_2 / \tau\right)$.

### DriftSE: Two Enhancement Paradigms

**Direct Mapping**: $\hat{\mathbf{x}} = f_\theta(\mathbf{y} + \sigma\bm{\epsilon})$ — maps noisy speech directly to clean speech. At inference, $\sigma = 0$ for deterministic denoising.

**Conditional Generator**: $\hat{\mathbf{x}} = f_\theta(\bm{\epsilon}, \mathbf{y})$ — generates clean speech from Gaussian noise conditioned on noisy observation. Enables diverse outputs and better perceptual quality.

### Speech Latent Encoder

The drifting field is computed in a semantic latent space using a frozen SSL encoder (HuBERT-Large, WavLM-Large, or DistilHuBERT). Multi-layer supervision captures hierarchical speech structures:
- DistilHuBERT: layers $\mathcal{S} = \{0, 1, 2\}$ (768-d)
- WavLM-Large / HuBERT-Large: layers $\mathcal{S} = \{6, 12, 24\}$ (1024-d)

### Training Objective

$$\mathcal{L}_{\text{drift}} = \mathbb{E}_\epsilon\left[\left\|\phi(\mathbf{x}) - \text{sg}\left(\phi(\mathbf{x}) + \mathbf{V}(\phi(\mathbf{x}))\right)\right\|_2^2\right]$$

where $\text{sg}(\cdot)$ is stop-gradient. Multi-temperature kernel with $\tau \in \{0.1, 0.5, 1.0\}$.

![DriftSE framework overview](raw/papers/xu-2026-drifting-models-speech-enhancement/figures/fig1-driftse-overview.png)
*Figure 1: Overview of the DriftSE framework (Direct Mapping formulation). The mapping function processes noisy speech + noise injection to produce a denoised spectrogram. Both enhanced and clean waveforms are projected into a frame-wise latent space via a frozen SSL encoder. The Drifting Field combines attraction toward clean distribution and repulsion from current model distribution.*

## Experimental Setup

| Aspect | Detail |
|--------|--------|
| **Training data** | VoiceBank (10,802 clean utterances) + DEMAND (18 noise types), dynamic mixing |
| **SNR range** | {0, 5, 10, 15} dB (randomly sampled) |
| **Evaluation (in-domain)** | VoiceBank-DEMAND test set (824 utterances) |
| **Evaluation (real-world)** | DNS Challenge 2020 blind test set (300 recordings) |
| **Architecture** | NCSN++V2 (without time embedding) |
| **Sampling rate** | 16 kHz |
| **STFT** | Window 510, hop 128, Hann window |
| **Noise injection** | $\log\sigma \sim \mathcal{N}(-3.0, 1.2)$, truncated to $\sigma \in [0.01, 0.3]$ |
| **SSL encoder** | DistilHuBERT (default), HuBERT-Large, WavLM-Large |
| **Kernel temperatures** | $\tau \in \{0.1, 0.5, 1.0\}$ |
| **Optimizer** | AdamW, lr $5 \times 10^{-4}$, weight decay 0.01 |
| **Batch size** | 16 |
| **Epochs** | 100 |
| **GPU** | Single NVIDIA RTX A6000 (48GB) |

## Results

### In-Domain (VoiceBank-DEMAND)

| Method | NFE | PESQ | SI-SDR | ESTOI | DNSMOS | SCOREQ |
|--------|-----|------|--------|-------|--------|--------|
| MetricGAN+ | 1 | 3.13 | 8.50 | 0.83 | 3.22 | 3.82 |
| SGMSE+ (30 steps) | 30 | 2.90 | 16.90 | 0.85 | 3.48 | 3.98 |
| ROSE-CD (1-step) | 1 | 3.49 | 17.80 | 0.87 | 3.49 | 4.23 |
| SBCTM (1-step) | 1 | 3.56 | 12.70 | 0.87 | 3.55 | 4.35 |
| MeanFlowSE (1-step) | 1 | 2.81 | 19.97 | 0.88 | 3.58 | 4.25 |
| **DriftSE (DistilHuBERT, σ=0)** | **1** | **3.15** | **16.10** | **0.86** | **3.47** | **4.08** |
| DriftSE∗ (conditional) | 1 | 2.99 | 17.98 | 0.86 | 3.64 | 4.33 |
| DriftSE† (aux losses) | 1 | 3.45 | 20.60 | 0.87 | 3.49 | 4.11 |
| DriftSE (Unpaired, DNS) | 1 | 2.00 | 6.60 | 0.74 | 3.61 | 3.92 |

Key findings:
- DriftSE (σ=0) outperforms 30-step SGMSE+ and 1-step MeanFlowSE in PESQ
- Conditional variant achieves best reference-free perceptual quality (SCOREQ 4.33, DNSMOS 3.64)
- With auxiliary losses (†), DriftSE reaches PESQ 3.45 and SI-SDR 20.60 — competitive with distillation methods
- Unpaired training still achieves strong non-intrusive scores (DNSMOS 3.61, SCOREQ 3.92)

### Real-World Generalization (DNS Challenge 2020)

| Method | NFE | WV-MOS | SCOREQ | SIG | BAK | OVRL |
|--------|-----|--------|--------|-----|-----|------|
| SGMSE+ | 30 | 2.34 | 2.95 | 4.12 | 3.94 | 3.62 |
| ROSE-CD | 1 | 2.37 | 2.81 | 4.01 | 3.80 | 3.42 |
| **DriftSE (DistilHuBERT)** | **1** | **2.65** | **2.97** | **3.78** | **3.84** | **3.31** |

DriftSE achieves **state-of-the-art WV-MOS 2.65 and SCOREQ 2.97** on real-world recordings, outperforming all baselines.

### Key Ablation Findings

1. **Latent encoder**: DistilHuBERT (768-d) is competitive with HuBERT/WavLM (1024-d); single deep layer (WavLM L24) degrades performance — multi-layer supervision is essential
2. **Noise injection**: σ=0 gives higher fidelity (PESQ 3.15, SI-SDR 16.10); σ>0 improves perceptual quality (SCOREQ 4.08 → 4.15) via distributional smoothing
3. **Unpaired training**: Matching distributions rather than paired samples enables training without noisy-clean pairs, with strong non-intrusive quality scores

## Key Contributions

1. Introduces DriftSE, the first application of Drifting Models to speech enhancement, reformulating denoising as a distributional equilibrium problem that achieves native one-step inference without iterative sampling or predefined trajectories.

2. Proposes two enhancement paradigms within the drifting framework: a direct mapping from noisy observation and a stochastic conditional generative model, demonstrating that both achieve high-fidelity enhancement in a single step.

3. Demonstrates that computing the drifting field in a multi-scale semantic latent space (using frozen SSL encoders) provides a robust training signal, and validates the framework's ability to train on unpaired data by matching distributions rather than paired samples.

## Related Concepts

- [[../concepts/drifting-models|Drifting Models]]
- [[../concepts/diffusion-models-for-speech|Diffusion Models for Speech Enhancement]]
- [[../concepts/self-supervised-speech-representation|Self-Supervised Speech Representation]]
- [[../concepts/one-step-generative-models|One-Step Generative Models]]

## Related Sources

- [[../sources/mohapatra-2026-localizing-conversation-partners-head-motion|Mohapatra et al. 2026: Localizing Conversation Partners Using Head Motion]]
