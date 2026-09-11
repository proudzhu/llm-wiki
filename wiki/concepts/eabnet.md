---
type: concept
created: 2026-09-11
updated: 2026-09-11
sources:
  - raw/papers/li-2022-embedding-beamforming/full-text.md
tags:
  - neural-beamformer
  - beamforming
  - multi-channel
  - speech-enhancement
  - deep-learning
---

# EaBNet

**EaBNet** (Embedding and Beamforming Network) is a causal all-neural beamformer for [[concepts/multi-channel-speech-enhancement|multi-channel speech enhancement]], proposed by Li et al. (ICASSP 2022). It replaces both stages of the classic mask-then-MVDR pipeline with networks: an Embedding Module (EM) produces a 3-D spectral-spatial embedding tensor, and a Beamforming Module (BM) directly regresses framewise complex filter weights that are applied via filter-and-sum.

## Key Formulations

The pipeline is:

$$\widetilde{\mathbf{E}} = EMet(\mathrm{Cat}(\mathbf{X}^{0}, \dots, \mathbf{X}^{P-1})) \in \mathbb{C}^{F \times T \times C}$$

$$\widetilde{\mathbf{M}} = BFNet(\widetilde{\mathbf{E}}) \in \mathbb{C}^{F \times T \times \bar{P}}, \qquad \widetilde{\mathbf{S}}^{(1)} = \sum_{p=0}^{P-1} \left(\widetilde{\mathbf{M}}^{p}\right)^{\mathsf{H}} \widetilde{\mathbf{X}}^{p}$$

- **EM**: U²-Encoder/Decoder (recalibration layers with 2D-(De)GLU + instance norm + PReLU + nested UNet-block), 3 stacked S-TCNs at the bottleneck; input is the RI concatenation of all $P$ channels ($F \times T \times 2P$).
- **BM variants**: C-BF (pointwise $1\times1$ conv, $C \to 2P$) or R-BF (LayerNorm → 2 uni-directional LSTMs → FC-ReLU); R-BF performs better because the frame-by-frame state update yields better weights when spatial cues are unreliable. The LSTM is shared across frequency subbands, mirroring per-frequency classical beamformers.
- **PostNet**: a single-channel SE network (GaGNet) cascaded on the beamformed output + reference channel to suppress residual noise.
- Trained end-to-end on [[concepts/power-law-compression|power-compressed]] spectra ($|X|^{0.5} e^{j\theta}$ — magnitude compressed, phase untouched so inter-channel spatial information is preserved) with an MMSE + magnitude-constraint loss.

## Key Findings

- **2.84M parameters, RTF 0.59** (Intel i5-4300 CPU): real-time capable, causal (framewise weights).
- Outperforms FasNet+TAC, MC-ConvTasNet, MIMO-UNet, CTSNet, GaGNet by a large margin (avg. PESQ 3.52 vs. 2.67 for the best baseline) on a simulated 9-channel DNS-Challenge setup.
- **Surpasses an oracle-IRM MB-MVDR beamformer** (3.52 vs. 3.10 PESQ) — the tandem statistical stage is the bottleneck, not just mask estimation error.
- The **EaBNet\* ablation**: explicitly computing [[concepts/spatial-covariance-matrix|spatial covariance matrices]] from predicted speech/noise masks (as in GST-RNN) and feeding them to the BM performs *worse* (3.46 vs. 3.52 PESQ) than the purely implicit embedding — evidence that the SCM is sparse/redundant and that a learned embedding can capture higher-order spatial statistics.

## Related Concepts

- [[concepts/neural-beamforming|Neural Beamforming]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/power-law-compression|Power-Law Compression]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/causality|Causality]]

## Related Sources

- [[sources/li-2022-embedding-beamforming|Li, Liu, Zheng & Li 2022: Embedding and Beamforming]]
