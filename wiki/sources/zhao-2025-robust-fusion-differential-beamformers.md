---
type: source
created: 2026-10-04
updated: 2026-10-04
sources:
  - raw/papers/zhao-2025-robust-fusion-differential-beamformers/full-text.md
  - https://doi.org/10.1109/LSP.2025.3612336
  - zotero://select/items/0_ZKPSATXE
tags:
  - differential-microphone-array
  - beamforming
  - speech-enhancement
  - interference-suppression
  - online-adaptive-fusion
  - distortionless
---

# Zhao, Luo, Jin, Jin & Huang 2025: Robust Fusion of Differential Beamformers

**Authors**: [[entities/kunlong-zhao|Kunlong Zhao]], [[entities/xueqin-luo|Xueqin Luo]], [[entities/jilu-jin|Jilu Jin]], [[entities/danqi-jin|Danqi Jin]], [[entities/gongping-huang|Gongping Huang]]
**Venue**: IEEE Signal Processing Letters (2025)
**Type**: journalArticle (letter)
**DOI**: [10.1109/LSP.2025.3612336](https://doi.org/10.1109/LSP.2025.3612336)
**Zotero**: [ZKPSATXE](zotero://select/items/0_ZKPSATXE)

## Summary

This letter proposes **AF-DMA** (adaptive fusion of differential microphone arrays): a bank of $K$ null-constrained [[concepts/differential-microphone-array|differential beamformers]] (each placing a null at a different candidate interference direction) plus a maximum-white-noise-gain (MWNG) beamformer are pre-designed, and their outputs are fused online per time-frequency bin by minimizing the instantaneous output variance over the simplex. Via Jensen's inequality the problem collapses to selecting the beamformer(s) with the minimum instantaneous output energy — no covariance estimation, no gradient adaptation, no statistical priors — giving a distortionless, real-time-capable response that outperforms adaptive DMA (Teutsch & Elko) and adaptive convex combination (ACC-DMA) baselines in moving- and multi-interferer scenarios.

## Problem Formulation

A ULA of $M$ microphones (spacing $\delta$) receives a desired source at azimuth $\theta_{\mathrm{s}}$ (endfire, $\theta_{\mathrm{s}} = 0^\circ$), $P$ interferers at $\theta_{\mathrm{i},p}$, plus noise:

$$
\mathbf{y}(\omega,t) = X_{\mathrm{s}}(\omega,t)\,\mathbf{d}_{\theta_{\mathrm{s}}}(\omega) + \sum_{p=1}^{P} X_{\mathrm{i},p}(\omega,t)\,\mathbf{d}_{\theta_{\mathrm{i},p}}(\omega) + \mathbf{v}(\omega,t).
$$

The beamformer output $Z = \mathbf{h}^{H}\mathbf{y}$ must satisfy the **distortionless constraint** $\mathbf{h}^{H}\mathbf{d}_{\theta_{\mathrm{s}}} = 1$. Performance is measured by the SNR gain and the SIR gain, both of which take the form

$$
\mathcal{G}[\mathbf{h}] = \frac{|\mathbf{h}^{H}\mathbf{d}_{\theta_{\mathrm{s}}}|^{2}}{\mathbf{h}^{H}\boldsymbol{\Gamma}_{\mathbf{v}}\mathbf{h}},
\qquad
\mathcal{I}[\mathbf{h}] = \frac{|\mathbf{h}^{H}\mathbf{d}_{\theta_{\mathrm{s}}}|^{2}}{\mathbf{h}^{H}\boldsymbol{\Gamma}_{\mathrm{i}}\mathbf{h}},
$$

where $\boldsymbol{\Gamma}_{\mathbf{v}}$ is the noise pseudo-coherence matrix and $\boldsymbol{\Gamma}_{\mathrm{i}} = \boldsymbol{\Lambda}_{\mathrm{i}}\boldsymbol{\Lambda}_{\mathrm{i}}^{H}$ stacks the interferer steering vectors. Under distortionlessness, maximizing both gains amounts to minimizing residual noise/interference power — but $\boldsymbol{\Gamma}_{\mathbf{v}}$ and $\boldsymbol{\Gamma}_{\mathrm{i}}$ are unavailable or unreliable in dynamic environments, motivating an instantaneous, statistics-free criterion.

## Methodology

### Beamformer bank

Design $K$ null-constrained differential beamformers $\mathbf{h}_{\mathrm{DMA},k}$ (nulls at various potential interference directions, distortionless at $\theta_{\mathrm{s}}$) plus the MWNG beamformer $\mathbf{h}_{\mathrm{MWNG}}$, assembled as $\mathbf{H} = [\mathbf{h}_{\mathrm{DMA},1} \dots \mathbf{h}_{\mathrm{DMA},K}\ \mathbf{h}_{\mathrm{MWNG}}]$. The combined filter is

$$
\mathbf{h}_{\mathrm{opt}} = \mathbf{H}\mathbf{w}, \qquad \sum_{k=1}^{K+1} w_k = 1, \quad 0 \le w_k \le 1,
$$

so the simplex constraint on $\mathbf{w}$ **automatically preserves distortionlessness**: $\mathbf{h}_{\mathrm{opt}}^{H}\mathbf{d}_{\theta_{\mathrm{s}}} = \sum_k w_k = 1$. The final output is $Z_{\mathrm{opt}} = \mathbf{w}^{T}\mathbf{z}$ with $\mathbf{z} = [Z_{\mathrm{DMA},1}, \dots, Z_{\mathrm{DMA},K}, Z_{\mathrm{MWNG}}]^{T}$ the bank outputs.

### Online minimum-variance fusion

Substituting $\mathbf{h} = \mathbf{H}\mathbf{w}$ into the gain formulas gives $\mathcal{G}[\mathbf{w}] = 1/(\mathbf{w}^{T}\mathbf{H}^{H}\boldsymbol{\Gamma}_{\mathbf{v}}\mathbf{H}\mathbf{w})$ (similarly for $\mathcal{I}$). Since the covariance matrices are unavailable, the criterion is replaced by the instantaneous variance:

$$
\min_{\mathbf{w}} |\mathbf{w}^{T}\mathbf{z}|^{2} \quad \text{s.t.} \quad \sum_k w_k = 1,\ 0 \le w_k \le 1.
$$

By **Jensen's inequality** (convexity of $|\cdot|^{2}$),

$$
|\mathbf{w}^{T}\mathbf{z}|^{2} \le \sum_{k=1}^{K} w_k |Z_{\mathrm{DMA},k}|^{2} + w_{K+1}|Z_{\mathrm{MWNG}}|^{2} = \sum_k w_k \mathcal{E}_k,
$$

which relaxes the problem into a linear program over the simplex. Its solution is fully combinatorial:

- **Case 1 (unique minimum)**: if $\mathcal{E}_l < \mathcal{E}_k\ \forall k \ne l$, then $w_l = 1$ and all other weights are 0 — i.e., *select the single beamformer whose output has the lowest instantaneous energy*.
- **Case 2 ($Q$ tied minima)**: any convex combination of the tied beamformers is optimal; choose uniform $w_k = 1/Q$ over the tied set, $0$ elsewhere.

Intuition: under the distortionless constraint, the beamformer output with the smallest absolute energy applies the greatest attenuation to interference + noise. The fusion needs **no statistical information** and no iterative adaptation, making it suitable for real-time processing; the distortionless response guarantees high-fidelity output amenable to further post-processing.

## Experimental Setup

| Item | Value |
|---|---|
| Array | ULA, $M = 8$ microphones, $\delta = 1.0$ cm |
| Room | $8 \times 6 \times 3$ m, image-method RIRs |
| Target | 2 m from array center, $\theta_{\mathrm{s}} = 0^\circ$ (endfire) |
| Scenario 1 | moving interferer rotating $90^\circ \to 180^\circ$ at $10^\circ$/s, 10 s |
| Scenario 2 | moving interferer + fixed interferer at $210^\circ$; $T_{60} \approx 300$ ms; overlapping (2–8 s) and non-overlapping speech segments |
| Source signals | TIMIT, 10 s utterances |
| Noise | white Gaussian, direct-path-to-noise input power ratio 20 dB |
| STFT | 256 samples, 75% overlap, Kaiser window |
| Averaging | 100 Monte Carlo runs per condition |
| Metrics | SNR, SIR (time domain, direct path = desired), [[concepts/pesq\|PESQ]], STOI |
| Baselines | DMA-I/II/III (null-constrained first-order DMAs, nulls at 90°/120°/180°); MWNG; Adaptive-DMA (Teutsch & Elko 2001, NLMS learning rate 0.005); ACC-DMA (Jin et al. 2024, adaptive convex combination) |

## Results

Under increasing reverberation (Scenario 1), all methods degrade but AF-DMA consistently achieves the highest SNR and SIR among the adaptive methods across all reverberation conditions.

![[raw/papers/zhao-2025-robust-fusion-differential-beamformers/figures/cbb2646b0a72f7f1dc95fe73b68dbea35aacbae04779f2273baa16eb8b560c4d.jpg|Figure 1]]
*Figure 1: Performance of the Adaptive-DMA, ACC-DMA, and proposed AF-DMA methods under different reverberation conditions: (a) SNR and (b) SIR.*

Multi-interferer scenario ($T_{60} \approx 300$ ms, Scenario 2), from Table I:

| Method | SNR (dB) | SIR (dB) | PESQ | STOI |
|---|---|---|---|---|
| Unprocessed | −9.19 | −6.96 | 1.31 | 0.52 |
| DMA-I (null 90°) | −4.75 | −3.23 | 1.41 | 0.58 |
| DMA-II (null 120°) | −2.52 | 2.88 | 1.82 | 0.68 |
| DMA-III (null 180°) | −3.93 | 1.33 | 1.74 | 0.66 |
| MWNG | −8.64 | −6.08 | 1.40 | 0.57 |
| Adaptive-DMA | −4.30 | 0.76 | 1.56 | 0.60 |
| ACC-DMA | −1.84 | 4.49 | 1.81 | 0.69 |
| **AF-DMA (proposed)** | **0.07** | **7.66** | **1.95** | **0.69** |

Single DMAs and MWNG alone cannot sufficiently suppress interference; combining multiple DMAs yields large gains. AF-DMA beats ACC-DMA by ~1.9 dB SNR and ~3.2 dB SIR, and improves PESQ (1.95 vs 1.81) at equal STOI. Spectrograms confirm visibly better interference suppression than ACC-DMA.

![[raw/papers/zhao-2025-robust-fusion-differential-beamformers/figures/ce853d671dbe9d45908481077bd48b4b3ca1163df61f3f43c0cb492abad9d0c5.jpg|Figure 2]]
*Figure 2: Spectrograms of the (a) clean signal, (b) noisy signal at the first microphone, (c) ACC-DMA output, and (d) proposed AF-DMA output.*

## Key Contributions

1. **Statistics-free online fusion criterion**: replaces covariance-based SNR/SIR maximization with per-frame minimization of the instantaneous output variance over the beamformer-bank simplex — no noise/interference statistics, no gradient adaptation (unlike ACC-DMA's exponential-gradient updates, which lag in rapidly changing conditions).
2. **Jensen-relaxed closed-form solution**: the non-trivial quadratic program relaxes via Jensen's inequality to a linear program whose optimum is "pick the minimum-energy output(s)" — Case 1 hard selection, Case 2 uniform split over ties — computationally trivial and real-time suitable.
3. **Distortionlessness by construction**: the simplex constraint on the fusion weights preserves the distortionless response of every bank member, guaranteeing high-fidelity output open to further post-filtering.
4. **Empirical validation in dynamic conditions**: superior SNR/SIR/PESQ/STOI against adaptive-DMA and ACC-DMA baselines with a moving interferer ($90^\circ \to 180^\circ$ at $10^\circ$/s) and a moving + fixed two-interferer configuration.

## Related Concepts

- [[concepts/differential-microphone-array|Differential Microphone Array]] — the fixed beamformers being fused
- [[concepts/af-dma-beamformer|AF-DMA (Adaptive Fusion of Differential Beamformers)]] — the method introduced by this paper
- [[concepts/tflc-beamformer|TFLC Beamforming]] — kindred per-TF-bin convex combination of distortionless beamformers (Yamaoka et al. 2021), with covariance-based mask optimization
- [[concepts/fixed-beamformer|Fixed Beamformer]] — fixed designs rendered adaptive through output-level fusion
- [[concepts/white-noise-gain|White Noise Gain]] — the MWNG bank member provides the robustness anchor
- [[concepts/beamforming|Beamforming]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/pesq|PESQ]] — quality metric

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] — adaptive vs. fixed beamforming axis
