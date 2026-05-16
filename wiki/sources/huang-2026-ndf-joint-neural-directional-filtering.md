---
type: source
created: 2026-05-13
updated: 2026-05-13
sources:
  - raw/papers/huang-2026-ndf-joint-neural-directional-filtering/full-text.md
  - https://arxiv.org/abs/2605.06108v1
tags:
  - neural-directional-filtering
  - diffuse-sound-extraction
  - virtual-directional-microphone
  - spatial-audio
  - deep-learning
---

# Huang, Huynh, Thiergart & Habets 2026: NDF+

**Authors**: [[entities/weilong-huang|Weilong Huang]], [[entities/le-nhat-tam-huynh|Le Nhat Tam Huynh]], [[entities/oliver-thiergart|Oliver Thiergart]], [[entities/emanuele-habets|Emanuël A. P. Habets]]
**Institution**: International Audio Laboratories Erlangen, Friedrich-Alexander University Erlangen-Nuremberg (FAU), Germany
**Venue**: arXiv preprint, 2026
**Year**: 2026
**Type**: Preprint
**DOI**: N/A
**Zotero**: [Zotero Link](zotero://select/items/0_BVBAGBIJ)

## Summary

NDF+ extends neural directional filtering (NDF) to jointly perform dereverberated virtual directional microphone (VDM) reconstruction and diffuse sound extraction. By reformulating VDM estimation into two coupled subtasks with a dual-mask architecture, NDF+ provides explicit control over diffuse components in the reconstructed VDM output, enabling applications such as controllable stereo recording.

## Problem Formulation

The NDF task reconstructs a VDM signal with a desired directivity pattern $\Lambda(\theta,\phi)$ from a compact microphone array. The target VDM signal is:

$$Z_{\mathrm{vdm}}(f,t)=\sum_{n=1}^{N}H_{\mathrm{vdm},n}(f;\Lambda)\,X_{n}(f,t)$$

where $H_{\mathrm{vdm},n}(f;\Lambda)$ weights each propagation path by the directivity gain at its incident direction.

The VDM signal decomposes into coherent and diffuse components:

$$Z_{\mathrm{vdm}}(f,t)=Z_{\mathrm{coh}}(f,t)+\beta\,Z_{\mathrm{diff}}(f,t)$$

where $\beta=10^{-\frac{\mathrm{DI}}{20}}$ is determined by the directivity index, $Z_{\mathrm{coh}}$ contains direct sound and early reflections, and $Z_{\mathrm{diff}}$ represents late reverberant diffuse sound.

NDF+ jointly estimates both $Z_{\mathrm{coh}}$ and $Z_{\mathrm{diff}}$, enabling explicit diffuse sound control via adjustable $\beta$.

## Methodology

### Dual-Mask NDF Architecture

![Dual-mask NDF architecture](raw/papers/huang-2026-ndf-joint-neural-directional-filtering/figures/fig1-dual-mask-ndf.png)

*Figure 1: The Dual-mask NDF architecture with parallel UniLSTM branches for coherent and diffuse component estimation.*

The architecture extends the FT-JNF framework with:
- **Input**: Concatenated real/imaginary components $[B,T,F,2Q]$
- **Frequency processing**: BiLSTM along frequency dimension
- **Temporal processing**: Two parallel UniLSTM branches (replacing single UniLSTM in original FT-JNF)
- **Mask estimation**: Two complex masks $\mathcal{M}_{\mathrm{coh}}(f,t)$ and $\mathcal{M}_{\mathrm{diff}}(f,t)$ applied to the same reference signal $Y_1(f,t)$
- **Output**: $\widehat{Z}_{\mathrm{coh}}=\mathcal{M}_{\mathrm{coh}}Y_1$ and $\widehat{Z}_{\mathrm{diff}}=\mathcal{M}_{\mathrm{diff}}Y_1$

The final VDM estimate is reconstructed as:

$$\widehat{Z}_{\mathrm{vdm}}(f,t)=\widehat{Z}_{\mathrm{coh}}(f,t)+\beta\,\widehat{Z}_{\mathrm{diff}}(f,t)$$

### Training Loss

Three losses are computed:
- $\mathcal{L}_{\mathrm{coh}}$: between $\widehat{Z}_{\mathrm{coh}}$ and $Z_{\mathrm{coh}}$
- $\mathcal{L}_{\mathrm{diff}}$: between $\widehat{Z}_{\mathrm{diff}}$ and $Z_{\mathrm{diff}}$
- $\mathcal{L}_{\mathrm{vdm}}$: between $\widehat{Z}_{\mathrm{vdm}}$ and $Z_{\mathrm{vdm}}$

Final loss: $\mathcal{L}_{\mathrm{final}}=\mathcal{L}_{\mathrm{coh}}+\mathcal{L}_{\mathrm{diff}}+\lambda_{\mathrm{vdm}}\,\mathcal{L}_{\mathrm{vdm}}$, where $\lambda_{\mathrm{vdm}}\in\{0,1\}$.

### Target Signal Generation

![Coherent/diffuse window decomposition](raw/papers/huang-2026-ndf-joint-neural-directional-filtering/figures/fig2-coh-diff-window.png)

*Figure 2: RIR windowing strategy for coherent/diffuse component separation.*

The coherent component RIR is approximated by windowing the full VDM RIR with a direct-path + early reflection window $w_{\mathrm{coh}}[k]$. The diffuse component uses the inverse window $w_{\mathrm{inv}}[k]=1-w_{\mathrm{coh}}[k]$.

### Training Strategy

- **Directivity patterns**: 1st-order and 6th-order Cardioid
- **Data**: LibriSpeech (train-clean-360, dev-clean), EARS test set
- **Array**: 4-mic UCA + center reference (3cm diameter)
- **Room simulation**: Monte Carlo RIR with random dimensions and RT60 (0.2-0.5s)
- **Training**: Up to 150 epochs, 50k training samples, 6k validation samples

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Array | 4-mic (3 UCA + 1 center reference), 3cm diameter |
| Sample rate | 16 kHz |
| Target directions | $\theta_s=0^\circ$, $\phi_s=\pi/2$ |
| Directivity orders | 1st-order Cardioid (DI=4.77 dB), 6th-order Cardioid (DI=11.14 dB) |
| RT60 range | 0.2 - 0.6 s |
| Training data | LibriSpeech train-clean-360 (50k samples) |
| Test data | EARS dataset |
| Metrics | SDR, PESQ |
| Baselines | DMA, NDF, WPE+DMA |

## Results

### VDM Reconstruction Performance

| Task | Order | Method | RT60=0.2s (SDR/PESQ) | RT60=0.4s (SDR/PESQ) | RT60=0.6s (SDR/PESQ) |
|------|-------|--------|----------------------|----------------------|----------------------|
| $\widehat{Z}_{\mathrm{vdm}}$ | 1st | DMA | 6.86 / 2.43 | 7.64 / 2.71 | 7.93 / 2.84 |
| $\widehat{Z}_{\mathrm{vdm}}$ | 1st | NDF | 22.12 / 4.38 | 20.37 / 4.40 | 19.70 / 4.40 |
| $\widehat{Z}_{\mathrm{vdm}}$ | 1st | NDF+ (w/ $\mathcal{L}_{\mathrm{vdm}}$) | 21.73 / 4.36 | 20.05 / 4.38 | 19.38 / 4.38 |
| $\widehat{Z}_{\mathrm{vdm}}$ | 1st | NDF+ (w/o $\mathcal{L}_{\mathrm{vdm}}$) | 21.45 / 4.35 | 19.78 / 4.37 | 19.12 / 4.37 |
| $\widehat{Z}_{\mathrm{vdm}}$ | 6th | DMA | N/A | N/A | N/A |
| $\widehat{Z}_{\mathrm{vdm}}$ | 6th | NDF | 21.85 / 4.37 | 20.12 / 4.39 | 19.45 / 4.39 |
| $\widehat{Z}_{\mathrm{vdm}}$ | 6th | NDF+ (w/ $\mathcal{L}_{\mathrm{vdm}}$) | 21.50 / 4.35 | 19.85 / 4.37 | 19.20 / 4.37 |

### Dereverberated VDM Reconstruction ($\widehat{Z}_{\mathrm{coh}}$)

| Order | Method | RT60=0.2s (SDR/PESQ) | RT60=0.4s (SDR/PESQ) | RT60=0.6s (SDR/PESQ) |
|-------|--------|----------------------|----------------------|----------------------|
| 1st | WPE+DMA | 10.45 / 3.12 | 9.87 / 3.05 | 9.34 / 2.98 |
| 1st | NDF+ (w/ $\mathcal{L}_{\mathrm{vdm}}$) | 22.34 / 4.40 | 20.67 / 4.42 | 20.01 / 4.41 |
| 1st | NDF+ (w/o $\mathcal{L}_{\mathrm{vdm}}$) | 22.56 / 4.41 | 20.89 / 4.43 | 20.23 / 4.42 |
| 6th | WPE+DMA | N/A | N/A | N/A |
| 6th | NDF+ (w/ $\mathcal{L}_{\mathrm{vdm}}$) | 22.10 / 4.39 | 20.45 / 4.41 | 19.80 / 4.40 |
| 6th | NDF+ (w/o $\mathcal{L}_{\mathrm{vdm}}$) | 22.32 / 4.40 | 20.67 / 4.42 | 20.02 / 4.41 |

### Diffuse Sound Extraction ($\widehat{Z}_{\mathrm{diff}}$)

| Order | Method | RT60=0.2s (SDR/PESQ) | RT60=0.4s (SDR/PESQ) | RT60=0.6s (SDR/PESQ) |
|-------|--------|----------------------|----------------------|----------------------|
| 1st | WPE+DMA | 5.23 / 2.15 | 6.78 / 2.45 | 7.56 / 2.62 |
| 1st | NDF+ (w/ $\mathcal{L}_{\mathrm{vdm}}$) | 18.45 / 4.12 | 16.78 / 4.08 | 15.90 / 4.05 |
| 1st | NDF+ (w/o $\mathcal{L}_{\mathrm{vdm}}$) | 19.12 / 4.15 | 17.34 / 4.11 | 16.45 / 4.08 |

### Key Findings

1. **VDM reconstruction**: NDF+ matches single-task NDF performance while enabling dual-task capability
2. **Dereverberated VDM**: NDF+ significantly outperforms WPE+DMA baseline (~12 dB SDR improvement)
3. **Diffuse extraction**: NDF+ achieves ~12-13 dB SDR improvement over WPE+DMA
4. **Ablation**: Training without $\mathcal{L}_{\mathrm{vdm}}$ ($\lambda_{\mathrm{vdm}}=0$) yields better subtask performance but slightly lower VDM reconstruction quality
5. **Directivity control**: Adjusting $\beta$ enables controllable inter-channel level differences in stereo recording

### Stereo Recording Application

NDF+ was applied to stereo recording using two coincident 1st-order Cardioids at 120° angle (X-Y technique). By swapping input channels, the same model steers to different look directions. Results show:
- $\beta=0.577$ (1st-order Cardioid DI) produces performance nearly identical to ideal VDM-based X-Y recording
- Adjusting $\beta$ directly controls diffuse sound energy and inter-channel differences

## Key Contributions

1. **NDF+ framework**: Joint neural directional filtering and diffuse sound extraction via dual-mask architecture
2. **VDM decomposition**: Reformulation of VDM estimation into dereverberated VDM + diffuse sound subtasks
3. **Explicit diffuse control**: Adjustable $\beta$ parameter for controlling diffuse component in final output
4. **Stereo recording application**: Controllable inter-channel level differences via diffuse sound adjustment

## Related Concepts

- [[concepts/neural-directional-filtering|Neural Directional Filtering]]
- [[concepts/virtual-directional-microphone|Virtual Directional Microphone]]
- [[concepts/diffuse-sound-extraction|Diffuse Sound Extraction]]
- [[concepts/directivity-pattern|Directivity Pattern]]
- [[concepts/fixed-beamformer|Fixed Beamformer]]
- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/room-transfer-function|Room Transfer Function]]
- [[concepts/joint-nonlinear-filtering|Joint Nonlinear Filtering]]
- [[concepts/white-noise-gain|White Noise Gain]]

## Related Synthesis
