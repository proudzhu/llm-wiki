---
type: concept
created: 2026-08-01
updated: 2026-08-01
sources:
  - raw/papers/zhao-2024-sicrn/full-text.md
tags:
  - neural-network
  - speech-enhancement
  - state-space-model
  - inplace-convolution
  - causal
  - lightweight
  - single-channel
---

# SICRN

**SICRN** (State-space-model + Inplace-Convolution Recurrent Network) is a single-channel speech enhancement network proposed by Zhao, He & Zhang (arXiv 2024) that combines a multidimensional state space model ([[concepts/s4nd|S4ND]]) with 2D [[concepts/inplace-convolution|inplace convolution]] inside a [[concepts/convolutional-recurrent-network|CRN]]-style U-shape. It is the **first model to combine state space models with the inplace-convolution design** introduced by [[concepts/igcrn|IGCRN]] and refined by [[concepts/iccrn|ICCRN]], and the first application of S4ND to monaural speech enhancement. The model is notable for achieving near-FullSubNet quality on the [[concepts/dns-challenge|DNS Challenge]] at 0.38× the parameters and 0.14× the MACs, with **0 ms look-ahead** (strictly causal).

## Motivation

Two limitations of the conventional [[concepts/convolutional-recurrent-network|CRN]] family motivate SICRN:

1. **Frequency downsampling destroys spectral structure.** Standard CRN uses stride-2 convolutions on the frequency dimension, encoding spectral patterns into the channel dimension. The [[concepts/igcrn|IGCRN]] line established that this aliasing is harmful (especially in the multi-channel setting), and that [[concepts/inplace-convolution|inplace convolutions]] (stride 1 on frequency) preserve the original feature structure.
2. **Pure inplace convolutions cannot model full-band correlations.** Because each frequency bin is processed independently, no cross-frequency interaction is learned. [[concepts/iccrn|ICCRN]] addressed this with a cepstral-space FFT branch; SICRN addresses it with S4ND, a multidimensional state space model with an effectively infinite receptive field along every axis.

SICRN's central design choice is to **fuse the two solutions in a single block**: S4ND provides the global/full-band view, 2D inplace convolution provides the local/per-bin view, and an attention map derived from their sum gates the local branch with the global context.

## Architecture

SICRN follows the overall CRN shape:

1. **Input projection** — an inplace convolution adapts the input channel dimension.
2. **Encoder** — a stack of [[concepts/sic-block|SIC blocks]] processes the real and imaginary components, integrating global (S4ND) and local (inplace conv) features.
3. **Temporal bottleneck** — a 2-layer LSTM (a plain LSTM, not the [[concepts/channel-wise-lstm|channel-wise LSTM]] of IGCRN — S4ND already provides per-frequency global context).
4. **Decoder** — symmetric SIC-block decoder reconstructs real/imaginary spectra and estimates a complex mask, which is multiplied with the original input spectrum to produce the enhanced output.

Configuration (from the paper): 2 SIC-block encoder layers with channel sizes 16 and 32; 2 LSTM layers in the middle; 3 inplace-convolution layers and 4 S4ND blocks per SIC block.

![[raw/papers/zhao-2024-sicrn/figures/fig1.png|SICRN architecture overview]]

*Figure 1: SICRN system overview. (a) Overall network. (b) SIC block — channel-bifurcated design combining 2D inplace conv (local) with S4ND (global) via an attention map. (c) S4ND block — S4ND → ELU → linear → residual → batch norm.*

### STFT Configuration

- 16 kHz sampling rate
- 510-point DFT, Hanning window
- win-length 510, hop-length 160 (10 ms frame shift)
- 256-dimensional complex spectrum as model input

### Loss Function

Time-domain SI-SNR:

$$\mathcal{L}_{\text{si-snr}} = 10 \log_{10} \frac{\|\mathbf{s}_{\text{target}}\|^{2}}{\|\mathbf{e}_{\text{noise}}\|^{2}}, \qquad \mathbf{s}_{\text{target}} = \frac{\langle\hat{\mathbf{s}}, \mathbf{s}\rangle \mathbf{s}}{\|\mathbf{s}\|^{2}}, \quad \mathbf{e}_{\text{noise}} = \hat{\mathbf{s}} - \mathbf{s}_{\text{target}}$$

where $\hat{\mathbf{s}}$ is the estimated and $\mathbf{s}$ the clean time-domain signal.

## Key Results

On the INTERSPEECH 2020 [[concepts/dns-challenge|DNS Challenge]] test set:

| Method | #Para (M) | MACs (G/s) | Look Ahead (ms) | WB-PESQ (reverb / no-reverb) |
|---|---|---|---|---|
| FullSubNet | 5.64 | 30.84 | 32 | 2.969 / 2.777 |
| **SICRN** | **2.16** | **4.24** | **0** | 2.891 / 2.624 |

SICRN trails FullSubNet by only ~0.05 WB-PESQ on both test conditions, while using **0.38× the parameters, 0.14× the MACs, and 0 ms look-ahead**.

### Ablation: S4ND contribution

Replacing S4ND with a same-shape inplace convolution (the resulting model is called **IICRN**, "Inplace-Inplace CRN") degrades all metrics, with the largest gap on the reverberant test set:

| Method | With-Reverb WB-PESQ | Without-Reverb WB-PESQ |
|---|---|---|
| IICRN | 2.797 | 2.596 |
| **SICRN** | **2.891** | **2.624** |

The authors interpret the larger reverb gap as evidence that S4ND's global temporal-spectral context is most valuable when the test distribution shifts (reverberant test, predominantly non-reverberant training).

## Position in the Inplace-CRN Lineage

SICRN extends the inplace-CRN line from [[entities/xueliang-zhang|Xueliang Zhang]]'s group at Inner Mongolia University:

- **[[concepts/igcrn|IGCRN]]** (Liu & Zhang 2021, Interspeech) — introduces [[concepts/inplace-convolution|inplace convolution]] for dual-channel SE; channel-wise LSTM bottleneck preserves per-bin spatial cues.
- **[[concepts/iccrn|ICCRN]]** (Liu & Zhang 2023, ICASSP) — replaces GLU with the [[concepts/cepstral-frequency-block|Cepstral Frequency Block]] to recover full-band modeling capacity via cepstral-space processing.
- **SICRN** (Zhao, He & Zhang 2024) — replaces standard convolution with the [[concepts/sic-block|SIC block]] (S4ND + 2D inplace conv) to recover full-band modeling capacity via a state-space global branch; first non-Liu first-author paper in the line; first to apply S4ND to monaural SE.

Where IGCRN/ICCRN address the full-band-modeling gap by changing *where* the inplace convolution operates (cepstral space), SICRN addresses it by *augmenting* the inplace convolution with a parallel global branch whose receptive field is theoretically infinite.

## Related Concepts

- [[concepts/sic-block|SIC Block]] — the novel S4ND + inplace-conv module
- [[concepts/s4nd|S4ND]] — multidimensional state space model used for global feature modeling
- [[concepts/inplace-convolution|Inplace Convolution]] — the local-feature branch
- [[concepts/igcrn|IGCRN]] — predecessor in the inplace-CRN lineage
- [[concepts/iccrn|ICCRN]] — sibling predecessor (alternative solution to the same full-band gap)
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — the CRN family SICRN extends
- [[concepts/state-space-model|State-Space Model]] — broader family
- [[concepts/dns-challenge|DNS Challenge]] — evaluation dataset

## Related Sources

- [[sources/zhao-2024-sicrn|Zhao, He & Zhang 2024: SICRN — State Space Model + Inplace Convolution for Speech Enhancement]]
