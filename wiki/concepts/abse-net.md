---
type: concept
created: 2026-09-06
updated: 2026-09-06
sources:
  - raw/papers/hu-2026-abse-net/full-text.md
tags:
  - binaural-speech-enhancement
  - active-noise-control
  - hearing-aids
  - lightweight-neural-network
---

# ABSE-NET

**ABSE-NET** is a lightweight neural framework for [[concepts/active-binaural-speech-enhancement|active binaural speech enhancement]] in open-fit hearing aids, proposed by Hu et al. (INTERSPEECH 2026). It cascades a binaural MVDR (BMVDR) beamformer with a 0.112M-parameter lightweight neural network (LNN) that simultaneously cancels acoustic leakage through the hearing-aid vent and compensates BMVDR-induced speech distortion — without requiring an in-ear error microphone at inference.

## Key Formulations

The LNN implements a data-driven post-filter after the BMVDR beamformer:

$$\mathcal{F}(\bm{\hat{w}}_{L}^{H}\bm{y},\,y_{L})\mapsto -d_{L}/g_{L}+a_{L}s$$

where $d_L$ is the acoustic leakage signal, $g_L$ the secondary path, and $a_L s$ the undistorted target as received at the reference microphone. The first term is the anti-leakage signal played by the loudspeaker (destructive interference); the second compensates beamformer distortion.

The LNN is an encoder–decoder with a feature augmentation (FA) module repeated $L=4$ times, each consisting of:

- **F-TDL block** — frequency dependency learning (FDL) sub-block (per-frame processing, linear bottleneck $C\to C_1\to C$ with SiLU + RMB-Conv1D along frequency) and time dependency learning (TDL) sub-block (per-bin processing with *causal* C-RMB-Conv1D along time in an expanded $C_2$-dim space).
- **ConvAtt block** — factorized channel attention ($\bm{M}_C\in\mathbb{R}^{C\times 1\times 1}$) and frequency–time attention ($\bm{M}_{FT}=[1-\alpha\cdot\rho\cdot\bm{G}]$, $\alpha=0.3$), avoiding full 3D attention tensors.

**RMB-Conv1D** (reparameterized multi-branch 1D convolution, after RepVGG) trains multi-scale depth-wise convolutions ($\mathcal{K}=\{1,3,5\}$) that are fused into a single kernel at inference, giving multi-scale capacity at single-convolution cost.

Training loss: $\mathcal{L}=-\text{SI-SDR}(\hat{\bm{u}},\bm{u})-\lambda\cdot\text{STOI}(\hat{\bm{u}},\bm{u})$ with $\lambda=10$.

![[raw/papers/hu-2026-abse-net/figures/fig2.png|ABSE-NET architecture]]

*Figure 2: ABSE-NET overview (a), F-TDL block (b), ConvAtt block (c).*

## Key Results

On a LibriSpeech + NOISEX-92 + Hearpiece-HRIR benchmark (−5 to 0 dB SNR, open-fit condition), ABSE-NET achieves PESQ 3.626 / STOI 0.955 / SI-SDR 9.869 dB with 0.112M parameters and 0.184G FLOPs — 29× fewer parameters and 78× fewer FLOPs than ASE-TM, with best-in-class spatial-cue preservation ($\Delta$ILD 3.047, $\Delta$IPD 0.251). It remains robust to 15° DOA error (SI-SDR 6.434 dB) where plain BMVDR degrades below the unprocessed signal.

## Related Concepts

- [[concepts/active-binaural-speech-enhancement|Active Binaural Speech Enhancement]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/spatially-selective-anc|Spatially Selective ANC]]
- [[concepts/speech-preserving-anc|Speech-Preserving ANC]]
- [[concepts/ear-canal-occlusion-effect|Ear Canal Occlusion Effect]]

## Related Sources

- [[sources/hu-2026-abse-net|Hu et al. 2026: ABSE-NET]]
