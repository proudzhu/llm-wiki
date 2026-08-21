---
type: source
created: 2026-08-21
updated: 2026-08-21
sources:
  - raw/papers/bai-2026-feedback-guided-anc/full-text.md
  - https://doi.org/10.48550/arXiv.2608.14061
  - zotero://select/items/0_MPHR6YAJ
tags:
  - active-noise-control
  - fixed-parameter-anc
  - deep-learning
  - mixture-of-experts
  - wavenet
  - streaming-inference
  - headphones
---

# Bai, He, Nan, Chen & Lu 2026: Feedback-guided DNN-based Controller Fusion for Robust Fixed-Parameter ANC

**Authors**: [[entities/lu-bai|Lu Bai]], [[entities/yiming-he|Yiming He]], [[entities/xiaofeng-nan|Xiaofeng Nan]], [[entities/kai-chen|Kai Chen]], [[entities/jing-lu|Jing Lu]]\*
**Institution**: Key Lab of Modern Acoustics, Institute of Acoustics, Nanjing University; NJU-Horizon Intelligent Audio Laboratory, Nanjing Institute of Advanced Artificial Intelligence
**Venue**: arXiv preprint (eess.SY)
**Year**: 2026 (submitted 14 Aug 2026)
**Type**: Preprint
**DOI**: [10.48550/arXiv.2608.14061](https://doi.org/10.48550/arXiv.2608.14061)
**arXiv**: 2608.14061
**Zotero**: [MPHR6YAJ](zotero://select/items/0_MPHR6YAJ)

## Summary

This paper proposes a [[concepts/feedback-guided-controller-fusion|feedback-guided DNN-based controller fusion]] framework for robust fixed-parameter active noise control (ANC). A causal WaveNet controller provides a stable baseline, while a feedback-guided mixture-of-experts (MoE) module dynamically fuses multiple pre-trained FIR experts using a gating network that consumes reference, control, and delayed-error signals. Unlike prior [[concepts/selective-fixed-filter-anc|SFANC]] / [[concepts/generative-fixed-filter-anc|GFANC]] methods that select controllers from reference-side features alone, the framework exploits the residual-error signal to characterize the actual control outcome under the current acoustic path, improving robustness to acoustic-path mismatch without online parameter updates. A fully causal sample-wise streaming implementation distributes the computational cost across sampling points to reduce peak computational load.

## Problem Formulation

The proposed method replaces the conventional control filter with a DNN-based controller in a feedforward ANC topology. Let $\mathbf{p}(n)$ and $\mathbf{s}(n)$ denote the primary and secondary paths; the reference signal $\mathbf{x}(n)$ is processed to produce control signal $\mathbf{y}(n)$. The primary noise and residual error are

$$
\mathbf{d}(n) = \mathbf{p}(n) * \mathbf{x}(n), \qquad \mathbf{e}(n) = \mathbf{d}(n) + \mathbf{s}(n) * \mathbf{y}(n),
$$

where $*$ denotes linear convolution. The controller has two parallel branches whose outputs are fused:

$$
\mathbf{y}(n) = \alpha\, \mathbf{y}_{\mathrm{W}}(n) + (1-\alpha)\, \mathbf{y}_{\mathrm{M}}(n),
$$

where $\mathbf{y}_{\mathrm{W}}(n)$ is the feedforward WaveNet output, $\mathbf{y}_{\mathrm{M}}(n)$ is the feedback-guided MoE output, and $\alpha$ is the fusion coefficient.

The motivation is twofold: (i) adaptive ANC may diverge under secondary-path modeling errors or rapidly varying conditions, prompting the use of fixed-parameter controllers; (ii) offline-trained DNN-based controllers and SFANC/GFANC frameworks select/generate filters from reference-side features that do not reflect the actual control outcome under the current acoustic system, leaving them limited against acoustic-path mismatch.

## Methodology

![[raw/papers/bai-2026-feedback-guided-anc/figures/fig1.png|Figure 1: Overall architecture of the proposed feedforward–feedback hybrid ANC system, including the feedforward WaveNet controller branch, the gating network, and the filter experts.]]

*Figure 1: Overall architecture of the proposed feedforward–feedback hybrid ANC system, including the feedforward WaveNet controller branch, the gating network, and the filter experts.*

### Feedforward WaveNet Controller Branch

A WaveNet provides a stable baseline controller. Two Conv1d layers at input/output adjust channel count; the backbone is a stack of residual blocks each consisting of a dilated Conv1d, a gated activation unit, and a Conv1d. The gated activation unit is

$$
\mathbf{z} = \tanh(W_{f,k} * \mathbf{a}) \odot \sigma(W_{g,k} * \mathbf{a}),
$$

with $*$ convolution, $\odot$ element-wise product, $\sigma$ the sigmoid, $k$ the layer index, and $f/g$ the filter and gate. Trained on all conditions, this branch yields an averaged optimal solution shared across paths — stable but limited on path outliers (e.g., path 7 in the experiments). The VNN module of WaveNet-VNN (Bai 2025, predecessor work) is intentionally omitted: the nonlinear effects in this task are limited, and avoiding higher-order nonlinear modeling reduces cost. For stronger nonlinear distortions the branch can be swapped for WaveNet-VNN.

### Feedback-Guided MoE Branch

The MoE module consists of a gating network and $N$ pre-trained 2048-tap FIR filter experts, one per acoustic path. The fused controller and its output are

$$
\mathbf{w}_{\mathrm{M}}(n) = \sum_{i=1}^{N} \beta_i(n-1)\, \mathbf{w}_i, \qquad \mathbf{y}_{\mathrm{M}}(n) = \mathbf{w}_{\mathrm{M}}(n) * \mathbf{x}(n).
$$

The weights $\beta(n-1)$ estimated at the previous sampling point are used to generate the current control signal — this guarantees causality: no current output depends on gating weights computed from that same output.

**Gating network inputs**: $\mathbf{x}(n)$, $\mathbf{y}(n)$, and $\mathbf{e}(n-1)$. The error signal is delayed by one sample because $\mathbf{e}(n)$ is only available after $\mathbf{y}(n)$ has propagated through the secondary path. The 1-sample misalignment has negligible impact on performance (verified experimentally). Two parallel feature-extraction branches process the concatenated inputs:

- **Temporal branch**: three cascaded Conv1d blocks (Conv1d → Layer Norm → SiLU), followed by a temporal mean for global temporal representation.
- **Statistical branch**: log-RMS features capturing amplitude statistics.

Features from both branches are concatenated and passed through an MLP (two linear layers + SiLU) followed by Softmax to produce the fusion weights $\beta$.

**Filter experts**: each expert is implemented as a Conv1d layer with kernel size 2048 — equivalent to a 2048-tap FIR filter without coefficient flipping. Coefficients are dynamically weighted by $\beta$ to form the MoE controller.

### Frequency-Aware Loss and Staged Training

The training objective is a [[concepts/frequency-aware-anc-loss|frequency-aware ANC loss]] based on one-third-octave-band analysis:

$$
\mathcal{L}_{\mathrm{ANC}} = \mathcal{L}_{\mathrm{NR}} + \lambda\, \mathcal{L}_{\mathrm{RB}} + \mathcal{L}_{\mathrm{NMSE}},
$$

with $\mathcal{L}_{\mathrm{NR}}$ the negative mean noise reduction over 50 Hz–5 kHz (equally weighted), $\mathcal{L}_{\mathrm{RB}}$ the largest noise amplification over 1 kHz–8 kHz (extended to 16 kHz for a more conservative constraint, set to zero when no band is amplified), and $\mathcal{L}_{\mathrm{NMSE}} = 10 \log_{10}\!\left( \sum_n e^2(n) / \sum_n d^2(n) \right)$. $\lambda$ balances noise reduction and rebound suppression. All spectral terms use an 8192-point STFT with a Hann window and 2048-hop.

Training proceeds in three stages:

1. **WaveNet pre-training** (180 epochs) on all training conditions.
2. **FIR expert pre-training** (180 epochs per expert), one expert per acoustic path. Stages 1 and 2 can run in parallel.
3. **Gating network training** (100 epochs) with WaveNet and FIR experts frozen. A cross-entropy auxiliary loss $\mathcal{L}_{\mathrm{cls}}$ supervised by acoustic-path labels (label-smoothing 0.05) is added:

$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{ANC}} + \gamma\, \mathcal{L}_{\mathrm{cls}},
$$

where $\gamma$ balances the two terms. $\mathcal{L}_{\mathrm{cls}}$ establishes the correspondence between acoustic paths and their associated FIR experts, while $\mathcal{L}_{\mathrm{ANC}}$ refines the soft fusion weights according to the resulting ANC performance.

### Streaming and Peak-MAC Optimization

The model is fully causal and supports sample-wise streaming inference, with computational cost evenly distributed across sampling points to reduce peak computational load. For the 10-expert model, peak-MAC optimization reduces the peak MAC from 34.62k to 14.15k while leaving the overall complexity essentially unchanged.

## Experimental Setup

| Item | Value |
|------|-------|
| Dataset | CCF Audio and Acoustic Technology Challenge (CCF-AATC), Track 2 (headphone ANC) |
| Noise scenarios | 8 (6 train, 2 unseen) |
| Primary noise recordings | 80 × 30 min |
| Secondary paths | 10 (8 train, 2 unseen) |
| Sample rate | 48 kHz |
| Train split | 8 paths + 6 noise scenarios; 1 FIR expert per path |
| Test split (robustness) | 2 unseen paths + 2 unseen noise scenarios |
| Streaming eval (10-expert) | 3 paths × 2 noise conditions × 5 s = 30 s |
| FIR expert length | 2048 taps |
| STFT for loss | 8192-pt Hann, hop 2048 |
| Loss frequency bands | NR: 50 Hz–5 kHz; rebound: 1–8 kHz (conservative: 1–16 kHz) |
| Baselines | CCF 2026 official baseline (NMSE loss); standalone WaveNet (this work's loss + training) |
| Training stages | 180 ep WaveNet ∥ 180 ep FIR experts → 100 ep gating network |

## Results

### Model Complexity

| Model | Params | Compute | Peak MAC (per sample) |
|-------|-------:|---------:|-----------------------:|
| CCF 2026 official baseline | 42.76k | 2.04 GMac/s | — |
| WaveNet-only (this work) | 10.08k | 483.84 MMac/s | — |
| Proposed hybrid (8-expert) | 28.57k | 672.83 MMac/s | — |
| Proposed hybrid (10-expert) | 32.69k | 672.93 MMac/s | 14.15k (peak-optimized) / 34.62k (standard streaming) |

The proposed hybrid is lighter than the official baseline (28.57k vs. 42.76k params; 672.83 MMac/s vs. 2.04 GMac/s) while adding the MoE branch.

### Spectral Behavior (Figs. 2–3)

![[raw/papers/bai-2026-feedback-guided-anc/figures/fig2.png|Figure 2: Noise reduction spectra of different ANC methods under seen acoustic paths with unseen noise.]]

*Figure 2: Noise reduction spectra of different ANC methods under seen acoustic paths with unseen noise.*

![[raw/papers/bai-2026-feedback-guided-anc/figures/fig3.png|Figure 3: Noise reduction spectra of different ANC methods under unseen acoustic paths with unseen noise.]]

*Figure 3: Noise reduction spectra of different ANC methods under unseen acoustic paths with unseen noise.*

- The standalone WaveNet, although fewer parameters and lower cost than the official baseline, outperforms it thanks to the optimized loss and training strategy.
- The standalone WaveNet fails on path 7 — a path whose acoustic response differs significantly from the other training paths — because the shared parameters can only approximate an average optimal solution.
- The MoE-only branch substantially improves low-frequency reduction on path 7 but introduces larger high-frequency amplification on some paths (e.g., path 6).
- The hybrid architecture combines the two branches' complementary advantages: improved low-frequency reduction while alleviating high-frequency amplification.
- On unseen acoustic paths (Fig. 3), the proposed method achieves superior reduction on both paths, demonstrating robustness to acoustic-path variations.

### Time-Domain and Third-Octave Performance (Figs. 4–5)

![[raw/papers/bai-2026-feedback-guided-anc/figures/fig4.png|Figure 4: Time-domain noise reduction performance of the proposed ANC model under different acoustic paths and noise conditions.]]

*Figure 4: Time-domain noise reduction performance of the proposed ANC model under different acoustic paths and noise conditions.*

![[raw/papers/bai-2026-feedback-guided-anc/figures/fig5.png|Figure 5: Third-octave band noise reduction performance of the proposed ANC model.]]

*Figure 5: Third-octave band noise reduction performance of the proposed ANC model.*

For the 10-expert model evaluated on six 5-s cases spanning three paths and two noise conditions per path:

- **Stable noise reduction across condition switches without convergence time** — a key advantage over adaptive ANC (Fig. 4).
- **Average 19.00 dB noise reduction from 50 Hz to 5 kHz**, with **negligible noise amplification over 1–8 kHz** (Fig. 5).

## Key Contributions

1. **Feedback-guided controller fusion framework**: introduces the use of control and residual-error signals (not just reference-side features) to dynamically fuse multiple pre-trained FIR experts with a WaveNet baseline, distinct from [[concepts/selective-fixed-filter-anc|SFANC]] and [[concepts/generative-fixed-filter-anc|GFANC]] which determine the controller primarily from reference-side noise features.
2. **Acoustic-path robustness without online adaptation**: improves robustness to acoustic-path mismatch by incorporating the effects of acoustic transfer paths into controller fusion, without online parameter updating.
3. **[[concepts/frequency-aware-anc-loss|Frequency-aware ANC loss]]**: jointly optimizes one-third-octave-band noise reduction (50 Hz–5 kHz), high-frequency rebound suppression (1–16 kHz conservative), and broadband NMSE — explicitly trading off low-frequency attenuation against high-frequency amplification.
4. **Staged training strategy**: progressively optimizes the WaveNet (180 ep, all conditions), path-specific FIR experts (180 ep each, parallelizable), and gating network (100 ep with cross-entropy path-label auxiliary + label smoothing 0.05).
5. **Fully causal sample-wise streaming implementation with peak-MAC optimization**: distributes computational cost evenly across sampling points, reducing peak MAC from 34.62k to 14.15k for the 10-expert model while keeping total complexity essentially unchanged.
6. **Efficiency**: hybrid model (28.57k params, 672.83 MMac/s) is lighter and cheaper than the CCF 2026 official baseline (42.76k params, 2.04 GMac/s) while delivering 19 dB average NR (50 Hz–5 kHz) with negligible 1–8 kHz amplification.

## Related Concepts

- [[concepts/feedback-guided-controller-fusion|Feedback-guided Controller Fusion]] — the proposed framework
- [[concepts/frequency-aware-anc-loss|Frequency-aware ANC Loss]] — the proposed loss
- [[concepts/active-noise-control|Active Noise Control]] — parent domain
- [[concepts/selective-fixed-filter-anc|Selective Fixed-Filter ANC]] (SFANC) — baseline family, reference-side feature selection
- [[concepts/generative-fixed-filter-anc|Generative Fixed-Filter ANC]] (GFANC) — baseline family, reference-side feature generation
- [[concepts/hybrid-anc|Hybrid ANC]] — architectural pattern (feedforward WaveNet + feedback-guided MoE)
- [[concepts/feedforward-anc|Feedforward ANC]] — branch topology
- [[concepts/feedback-anc|Feedback ANC]] — error-signal feedback for gating (delayed by 1 sample for causality)
- WaveNet-VNN (Bai 2025, predecessor) — the present work uses WaveNet only, dropping the VNN module to save cost

## Related Synthesis

(No existing synthesis pages currently address fixed-filter / DNN-based ANC robustness across acoustic-path variations; this paper contributes the first feedback-guided fusion data point for that axis.)

## Related Sources

- [[sources/luo-2026-hybrid-gfanc-fxnlms|Luo 2026: Hybrid GFANC-FxNLMS]] — hybrid generative-filter + adaptive stabilization, a related fixed-filter + adaptive combination
- [[sources/yang-2026-transformer-e2e-cfg-anc|Yang 2026: Transformer-based E2E-CFG for ANC]] — direct filter generation via Transformer co-processor; another fixed-filter generation baseline
- [[sources/yin-2023-selective-fixed-filter-anc-headphones|Yin 2023: Selective Fixed-Filter ANC Based on Frequency Response Matching in Headphones]] — non-neural SFANC; reference-side selection baseline
