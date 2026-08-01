---
type: source
created: 2026-08-01
updated: 2026-08-01
sources:
  - raw/papers/zhao-2024-sicrn/full-text.md
  - https://doi.org/10.48550/arXiv.2402.14225
  - zotero://select/items/0_DRNH5RMU
tags:
  - speech-enhancement
  - state-space-model
  - inplace-convolution
  - neural-network
  - causal
  - lightweight
---

# Zhao, He & Zhang 2024: SICRN — State Space Model + Inplace Convolution for Speech Enhancement

- **Authors**: [[entities/changjiang-zhao|Changjiang Zhao]], [[entities/shulin-he|Shulin He]], [[entities/xueliang-zhang|Xueliang Zhang]]
- **Institution**: Inner Mongolia University, School of Computer Science
- **Venue**: arXiv preprint (Feb 2024)
- **Type**: Preprint
- **DOI**: [10.48550/arXiv.2402.14225](https://doi.org/10.48550/arXiv.2402.14225)
- **arXiv**: [2402.14225](http://arxiv.org/abs/2402.14225)
- **Zotero**: [DRNH5RMU](zotero://select/items/0_DRNH5RMU)
- **Funding**: China National Nature Science Foundation (No. 61876214)

## Summary

SICRN is a single-channel speech enhancement network that replaces the standard strided convolutions of a [[concepts/convolutional-recurrent-network|CRN]] with a novel **SIC block** combining a multidimensional state space model ([[concepts/s4nd|S4ND]]) for global feature modeling with a 2D [[concepts/inplace-convolution|inplace convolution]] for local feature modeling. By avoiding frequency downsampling throughout, SICRN preserves the original spectral structure; by adding S4ND it recovers the full-band correlations that pure inplace convolutions miss. On the INTERSPEECH 2020 [[concepts/dns-challenge|DNS Challenge]] test set, SICRN approaches FullSubNet's quality with **only 2.16 M parameters (0.38×) and 4.24 G/s MACs (0.14×)**, while being strictly causal (0 ms look-ahead).

## Problem Formulation

The standard CRN encoder downsamples the frequency dimension with stride-2 convolutions, encoding spectral patterns into the channel dimension. The authors identify two issues:

1. **Frequency downsampling destroys the inherent feature structure of speech** — amplitude-spectrum harmonics and "spatial position information" are aliased when the frequency axis is shrunk. (This argument echoes the multi-channel motivation in [[concepts/igcrn|IGCRN]], but applied here to single-channel SE.)
2. **Convolutional layers lack temporal modeling ability** — a separate recurrent layer is needed, and the convolutional encoder/decoder cannot by themselves capture long-range dependencies.

The authors further note that pure inplace convolution (no downsampling) preserves local structure but cannot easily obtain **full-band correlations**, because each frequency bin is processed independently — exactly the limitation that motivated the [[concepts/cepstral-frequency-block|Cepstral Frequency Block]] in [[concepts/iccrn|ICCRN]]. SICRN addresses this by adding S4ND, which acts as a convolution kernel with infinite receptive field along every axis.

The training objective is the [[concepts/time-domain-speech-enhancement|time-domain]] scale-invariant signal-to-noise ratio (SI-SNR) loss:

$$\mathbf{s}_{\text{target}} = \frac{\langle\hat{\mathbf{s}}, \mathbf{s}\rangle \mathbf{s}}{\|\mathbf{s}\|^{2}}, \qquad \mathbf{e}_{\text{noise}} = \hat{\mathbf{s}} - \mathbf{s}_{\text{target}}$$

$$\mathcal{L}_{\text{si-snr}} = 10 \log_{10} \frac{\|\mathbf{s}_{\text{target}}\|^{2}}{\|\mathbf{e}_{\text{noise}}\|^{2}}$$

where $\hat{\mathbf{s}}$ and $\mathbf{s}$ are the estimated and clean time-domain signals.

## Methodology

![[raw/papers/zhao-2024-sicrn/figures/fig1.png|SICRN architecture overview]]

*Figure 1: Overview of the proposed SICRN system. (a) Overall network — inplace conv → SIC blocks (encoder) → 2-layer LSTM → SIC blocks (decoder) → complex mask. (b) SIC block — channel-bifurcated design combining 2D inplace conv (local) with S4ND (global) via an attention map. (c) S4ND block — S4ND → ELU → linear → residual → batch norm.*

### Overall Architecture

SICRN follows the "overall-detailed" U-shape of CRN-style networks, taking the complex spectrum as input:

1. **Input projection** — an inplace convolution adapts the input channel dimension.
2. **Encoder** — a stack of [[concepts/sic-block|SIC blocks]] extracts and integrates global (S4ND) and local (inplace conv) features from the real and imaginary components.
3. **Temporal bottleneck** — a 2-layer LSTM performs temporal modeling. (Note: a plain LSTM, not a [[concepts/channel-wise-lstm|channel-wise LSTM]] as in [[concepts/igcrn|IGCRN]] — the S4ND branch already provides per-frequency global context.)
4. **Decoder** — symmetric SIC-block decoder reconstructs real/imaginary spectra; a complex mask is estimated and multiplied with the original input spectrum to produce the enhanced output.

The configuration is: 2 SIC-block encoder layers with channel sizes 16 and 32; 2 LSTM layers in the middle; 3 inplace-convolution layers per SIC block; 4 S4ND blocks per SIC block.

### SIC Block (the novel module)

The [[concepts/sic-block|SIC block]] is the paper's core contribution. The input channel of size $c$ is split into two halves:

- **First half** $X_{0 \sim c/2}$ goes through 2D inplace convolution $\operatorname{IC}(\cdot)$ followed by a 1D convolution $C_{1d}$, producing **local features** $X^{L}_{0 \sim c/2}$.
- **Second half** $X_{c/2 \sim c}$ goes through the S4ND layer $\operatorname{S}(\cdot)$, producing **global features** $X^{R}_{c/2 \sim c}$.
- An **attention map** is computed by summing the local-conv output and the S4ND output and applying a sigmoid:
$$ATmap = \sigma\!\left( C_{1d}\!\left( \operatorname{IC}(X_{0 \sim c/2}) \right) + X^{R}_{c/2 \sim c} \right)$$
- The fused output is the local feature modulated by the attention map:
$$\mathrm{X} = X^{L}_{0 \sim c/2} \cdot ATmap$$

This is the mechanism by which S4ND's global view "harmonizes" the inplace convolution's local view: the attention map acts as a global-context gate on the local feature.

### S4ND Block

The [[concepts/s4nd|S4ND block]] applies S4ND for global feature extraction, followed by ELU, a linear layer, a residual connection, and batch normalization. The authors justify choosing S4ND over LSTM or 2D convolutions as the global-modeling branch by noting that (i) S4ND's global capacity exceeds LSTM at smaller parameter and computational cost, and (ii) S4 (the 1D precursor) processes frequency bins independently and therefore cannot capture frequency-axis correlations, whereas S4ND's multidimensional PDE formulation captures correlations along every axis.

### Loss Function

SI-SNR (time domain) — see Problem Formulation above.

## Experimental Setup

| Item | Value |
|------|-------|
| **Dataset** | INTERSPEECH 2020 [[concepts/dns-challenge\|DNS Challenge]] — 500 h clean (2150 speakers) + 180 h noise (150 classes); dynamic mixing |
| **Reverberation** | 75 % of clean speech convolved with RIRs (Multichannel Impulse Response Database: T60 = 0.16/0.36/0.61 s; REVERB Challenge: T60 = 0.3/0.6/0.7 s) |
| **Training SNR** | Random in $[-5, 20]$ dB |
| **Test set** | DNS Challenge synthetic test set — 150 clips × {with reverb, without reverb}, SNR 0–20 dB |
| **Sampling rate** | 16 kHz |
| **STFT** | win-length 510, hop 160, Hanning window, 510-point DFT → 256-dim complex spectrum |
| **Optimizer** | Adam, initial lr $2 \times 10^{-4}$, halved after 4 epochs without validation-loss improvement |
| **Look-ahead** | 0 ms (strictly causal — uses only current + past frame) |
| **Model size** | 2.16 M params, 4.24 G/s MACs |

### Baselines

NSNet, DTLN, Conv-TasNet, DCCRN-E, PoCoNet, and **FullSubNet** (the primary comparison target — also causal-friendly but uses 32 ms look-ahead).

## Results

### Main comparison (DNS Challenge test set)

| Method | #Para (M) | Look Ahead (ms) | WB-PESQ | NB-PESQ | STOI (%) | SI-SDR (dB) |
|---|---|---|---|---|---|---|
| **With Reverb** | | | | | | |
| Noisy | — | — | 1.822 | 2.753 | 86.62 | 9.033 |
| NSNet | 5.1 | 0 | 2.365 | 3.076 | 90.43 | 14.721 |
| DTLN | 1.0 | — | — | 2.700 | 84.68 | 10.530 |
| Conv-TasNet | 5.08 | 33 | 2.750 | — | — | — |
| DCCRN-E | 3.7 | 37.5 | — | 3.077 | — | — |
| PoCoNet | 50 | — | 2.832 | — | — | — |
| FullSubNet | 5.64 | 32 | **2.969** | **3.473** | **92.62** | **15.750** |
| **SICRN** | **2.16** | **0** | 2.891 | 3.433 | 92.59 | 15.137 |
| **Without Reverb** | | | | | | |
| Noisy | — | — | 1.582 | 2.454 | 91.52 | 9.071 |
| NSNet | 5.1 | 0 | 2.145 | 2.873 | 94.47 | 15.613 |
| DTLN | 1.0 | — | — | 3.040 | 94.76 | 16.340 |
| Conv-TasNet | 5.08 | 33 | 2.730 | — | — | — |
| DCCRN-E | 3.7 | 37.5 | — | 3.266 | — | — |
| PoCoNet | 50 | — | 2.748 | — | — | — |
| FullSubNet | 5.64 | 32 | **2.777** | **3.305** | **96.11** | **17.290** |
| **SICRN** | **2.16** | **0** | 2.624 | 3.233 | 95.83 | 15.998 |

### Efficiency comparison vs FullSubNet

| Method | #Para (M) | MACs (G/s) | Look Ahead (ms) |
|---|---|---|---|
| FullSubNet | 5.64 | 30.84 | 32 |
| **SICRN** | **2.16** | **4.24** | **0** |

SICRN uses **0.38× the parameters, 0.14× the MACs, and 0 ms look-ahead** of FullSubNet, while scoring within ~0.05 WB-PESQ / ~0.04 NB-PESQ / ~0.25 STOI / ~0.5 dB SI-SDR of it on both test conditions.

### Ablation: S4ND vs Inplace-Conv-Only (IICRN)

To isolate S4ND's contribution, the 4-layer S4ND in each SIC block is replaced with a 4-layer inplace convolution, yielding **IICRN** (Inplace-Inplace CRN — purely local, no global branch).

| Method | WB-PESQ | NB-PESQ | STOI | SI-SDR |
|---|---|---|---|---|
| **With Reverb** | | | | |
| Mixture | 1.822 | 2.753 | 86.62 | 9.033 |
| IICRN | 2.797 | 3.378 | 91.71 | 14.929 |
| **SICRN** | **2.891** | **3.433** | **92.59** | **15.137** |
| **Without Reverb** | | | | |
| Noisy | 1.582 | 2.454 | 91.52 | 9.071 |
| IICRN | 2.596 | 3.218 | 95.56 | 15.795 |
| **SICRN** | **2.624** | **3.233** | **95.83** | **15.998** |

S4ND's gain is consistent across all metrics and conditions, and is **more pronounced in the reverberant test set** (~0.09 WB-PESQ, ~0.88 pt STOI, ~0.21 dB SI-SDR) than in the anechoic one (~0.03 WB-PESQ, ~0.27 pt STOI, ~0.20 dB SI-SDR). The authors interpret this as evidence that the global temporal-spectral context modeled by S4ND is most valuable when the test condition differs from the predominantly non-reverberant training distribution. Even IICRN alone is already competitive — confirming the inplace-convolution finding of [[concepts/igcrn|IGCRN]] / [[concepts/iccrn|ICCRN]] that avoiding frequency downsampling is itself a strong inductive bias for SE.

## Key Contributions

1. **A novel SIC (State space model + Inplace Convolution) block** that fuses S4ND and 2D inplace convolution via an attention map. The block combines a global branch (S4ND — infinite receptive field along every axis, captures full-band correlations) with a local branch (inplace conv — preserves per-bin structure, no downsampling) in a single drop-in replacement for standard convolution.
2. **SICRN architecture**: a CRN-style SE network built from SIC blocks (encoder + decoder) around a 2-layer LSTM bottleneck. It is the **first model to combine state-space models with the inplace-convolution design** (introduced by [[concepts/igcrn|IGCRN]] and refined by [[concepts/iccrn|ICCRN]]), and the first application of S4ND to monaural speech enhancement.
3. **Near-SOTA quality at fraction of cost**: 2.16 M params and 4.24 G/s MACs — 0.38× and 0.14× of FullSubNet respectively — while scoring within ~0.05 WB-PESQ of FullSubNet on the DNS Challenge test set, with **0 ms look-ahead** (strictly causal) vs. FullSubNet's 32 ms.
4. **Ablation isolating S4ND's contribution**: replacing S4ND with a same-shape inplace convolution (IICRN) degrades all metrics, with the largest gap in the reverberant condition — empirically supporting the claim that S4ND's global receptive field is what recovers the full-band correlations missing from pure inplace designs.

## Related Concepts

- [[concepts/sicrn|SICRN]] — main concept page for the architecture
- [[concepts/sic-block|SIC Block]] — the novel S4ND + inplace-conv module
- [[concepts/s4nd|S4ND]] — multidimensional state space model used for global feature modeling
- [[concepts/inplace-convolution|Inplace Convolution]] — the local-feature branch, introduced by IGCRN
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — the CRN family SICRN extends
- [[concepts/igcrn|IGCRN]] — first inplace-CRN model; SICRN shares the inplace design and the same lab lineage
- [[concepts/iccrn|ICCRN]] — successor to IGCRN; SICRN's S4ND branch addresses the same full-band-modeling gap that ICCRN's Cepstral Frequency Block addresses
- [[concepts/state-space-model|State-Space Model]] — broader family
- [[concepts/dns-challenge|DNS Challenge]] — evaluation dataset
- [[concepts/speech-enhancement|Speech Enhancement]] — the task

## Related Synthesis

(none — SICRN is a single-task SE paper; the existing synthesis pages focus on multi-task + ultra-low-latency or ANC efficiency, neither of which is materially advanced by SICRN's contribution.)
