---
type: concept
created: 2026-10-04
updated: 2026-10-04
sources:
  - raw/papers/zhao-2025-robust-fusion-differential-beamformers/full-text.md
tags:
  - differential-microphone-array
  - beamforming
  - speech-enhancement
  - interference-suppression
  - online-adaptive-fusion
  - distortionless
---

# AF-DMA (Adaptive Fusion of Differential Beamformers)

**AF-DMA** makes [[concepts/differential-microphone-array|differential microphone arrays]] adaptive in dynamic interference conditions by fusing a **pre-designed bank** of beamformers online instead of adapting any filter coefficients. Introduced by [[entities/kunlong-zhao|Zhao]], [[entities/xueqin-luo|Luo]], [[entities/jilu-jin|Jin]], [[entities/danqi-jin|Jin]] & [[entities/gongping-huang|Huang]] in [[sources/zhao-2025-robust-fusion-differential-beamformers|Zhao et al. 2025]], the bank contains $K$ null-constrained differential beamformers (each with a null at a different candidate interference direction, all distortionless toward the endfire target) plus a maximum-[[concepts/white-noise-gain|WNG]] (MWNG) beamformer as the robustness anchor.

## Key Formulations

The combined filter lives on the simplex spanned by the bank columns:

$$
\mathbf{h}_{\mathrm{opt}} = \mathbf{H}\mathbf{w}, \qquad \sum_{k=1}^{K+1} w_k = 1, \quad 0 \le w_k \le 1,
$$

which preserves distortionlessness by construction ($\mathbf{h}_{\mathrm{opt}}^{H}\mathbf{d}_{\theta_{\mathrm{s}}} = \sum_k w_k = 1$). Because noise/interference covariance matrices are unreliable in dynamic scenes, the fusion criterion is the **instantaneous output variance**:

$$
\min_{\mathbf{w}} |\mathbf{w}^{T}\mathbf{z}|^{2} \quad \text{s.t.} \quad \mathbf{w} \in \text{simplex},
$$

with $\mathbf{z}$ the stacked bank outputs. Jensen's inequality relaxes this quadratic program into a **linear program** over the instantaneous output energies $\mathcal{E}_k = |Z_k|^{2}$, whose optimum is combinatorial:

- **Unique minimum** $\mathcal{E}_l$: hard selection, $w_l = 1$, all others $0$.
- **$Q$-way tie**: any convex combination of the tied outputs is optimal; take the uniform $1/Q$ split.

The intuition: under the distortionless constraint, the bank member with the lowest absolute output energy delivers the greatest interference + noise attenuation *at that time-frequency bin*. The method therefore resembles a hard-selection **beamformer selection mask** — the same principle as the TFS variant of [[concepts/tflc-beamformer|TFLC beamforming]] — but obtained per frame from instantaneous energies alone, with no covariance estimation, no iterative mask optimization, and no gradient adaptation.

## Findings

- 8-mic, 1 cm ULA, $T_{60} \approx 300$ ms, one moving ($90^\circ \to 180^\circ$ at $10^\circ$/s) + one fixed ($210^\circ$) interferer: AF-DMA reaches 0.07 dB SNR / 7.66 dB SIR / 1.95 [[concepts/pesq|PESQ]] / 0.69 STOI, beating adaptive convex combination (ACC-DMA: −1.84 dB / 4.49 dB / 1.81 / 0.69) and NLMS-based Adaptive-DMA (−4.30 dB / 0.76 dB / 1.56 / 0.60).
- Robustness advantage over gradient-based ACC-DMA stems from its statistics-free per-frame criterion: exponential-gradient weight updates lag or misestimate in rapidly changing interference, while AF-DMA re-selects instantly.
- Distortionless output leaves headroom for further SNR gains via post-processing (not explored in the paper).
- Design limitation (shared with the ACC approach): the null grid pre-defines the candidate interference directions, so suppression quality depends on how well actual interferer directions are covered by the bank.

## Related Concepts

- [[concepts/differential-microphone-array|Differential Microphone Array]] — the fixed bank being fused
- [[concepts/tflc-beamformer|TFLC Beamforming]] — per-TF-bin convex combination of distortionless beamformers with covariance-based mask optimization; AF-DMA is its statistics-free, fixed-DMA counterpart
- [[concepts/fixed-beamformer|Fixed Beamformer]] — AF-DMA renders a fixed bank adaptive at the output level
- [[concepts/white-noise-gain|White Noise Gain]] — the MWNG bank member guards against white-noise amplification
- [[concepts/mvdr-beamformer|MVDR Beamformer]] — the covariance-based alternative whose statistics AF-DMA avoids
- [[concepts/beamforming|Beamforming]]

## Related Sources

- [[sources/zhao-2025-robust-fusion-differential-beamformers|Zhao, Luo, Jin, Jin & Huang 2025: Robust Fusion of Differential Beamformers]] — origin paper (IEEE SPL 2025)
