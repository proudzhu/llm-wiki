---
type: concept
created: 2026-11-22
updated: 2026-11-22
sources:
  - raw/papers/abdulatif-2024-cmgan/full-text.md
tags:
  - speech-enhancement
  - conformer
  - metric-optimization
  - complex-domain
  - generative-adversarial-network
---

# CMGAN

**CMGAN (Conformer-Based Metric-GAN)** is a monaural speech-enhancement architecture that combines a shared magnitude/complex TF generator with a MetricGAN-style PESQ surrogate. Cao, Abdulatif & Yang introduced the denoising model at Interspeech 2022; [[sources/abdulatif-2024-cmgan|Abdulatif, Cao & Yang's 2024 TASLP article]] extends it to dereverberation and speech super-resolution and supplies the full architecture, ablation, and generalization study.

The generator has **1.83 M parameters** and is non-causal: its temporal attention can use the complete utterance.

## Architecture

1. **Power-compressed input.** A 400-point STFT at 16 kHz is compressed by $|Y_o|^{0.3}e^{jY_p}$; compressed magnitude, real, and imaginary channels are concatenated.
2. **Shared encoder.** Two convolution blocks surround a four-block dilated DenseNet with dilations $\{1,2,4,8\}$. The encoder produces 64 channels and halves frequency resolution.
3. **Four [[concepts/two-stage-conformer|two-stage Conformer blocks]].** Each runs a time Conformer followed by a frequency Conformer, avoiding joint attention over every TF position.
4. **Two decoders.** A mask decoder estimates a per-frequency-PReLU magnitude mask, while a complex decoder predicts unconstrained real/imaginary residuals. Both use dilated dense blocks and sub-pixel frequency upsampling.
5. **Metric discriminator.** Four stride-2 convolution blocks (16/32/64/128 channels), global average pooling, and $128\rightarrow64\rightarrow1$ fully connected layers estimate normalized PESQ from clean/enhanced magnitude pairs.

![[raw/papers/abdulatif-2024-cmgan/figures/3573763c33ddbff77f1ff18483c25edf98dd7f1ecf53c68428f9a18937b0498c.jpg|CMGAN generator, two-stage Conformer, and metric discriminator]]

*The CMGAN generator, factorized Conformer block, and metric discriminator (TASLP Fig. 2).*

## Decoupled Complex Reconstruction

For denoising and dereverberation, the masked magnitude $\hat X'_m=M\odot Y_m$ is combined with noisy phase and the complex residual:

$$\hat X_r=\hat X'_m\cos(Y_p)+\hat X'_r,\qquad
\hat X_i=\hat X'_m\sin(Y_p)+\hat X'_i.$$

The final magnitude $\sqrt{\hat X_r^2+\hat X_i^2}$ is computed after this summation, so the magnitude loss supervises both decoder branches. This distinguishes CMGAN from pure [[concepts/complex-spectral-mapping|complex spectral mapping]] and from magnitude-only masking.

## Training Objective

The generator minimizes

$$\mathcal L_G=\mathcal L_{TF}+0.01\mathcal L_{GAN}+\mathcal L_{Time},$$

where

$$\mathcal L_{TF}=0.7\mathcal L_{Mag}+0.3\mathcal L_{RI}$$

is a [[concepts/mixed-magnitude-complex-loss|mixed magnitude-complex loss]], $\mathcal L_{Time}$ is waveform $L_1$, and $\mathcal L_{GAN}$ pushes the PESQ surrogate toward 1. The discriminator learns normalized PESQ on current enhanced outputs, making adversarial co-adaptation essential; a frozen discriminator pretrained without enhanced tracks performs worse.

The default discriminator target is [[concepts/pesq|PESQ]]. **CMGAN-LLR** replaces it with normalized log-likelihood ratio and changes the desired score from 1 to 0 for dereverberation.

## Task-Specific Mask Operator

| Task | Mask operation | Purpose |
|:-----|:---------------|:--------|
| Denoising | $M\odot Y_m$ | Suppress noise while retaining speech |
| Dereverberation | $M\odot Y_m$ | Suppress late-reverberation energy |
| [[concepts/speech-super-resolution|Super-resolution]] | $M'+Y_m$ | Add missing high-frequency content rather than suppressing input energy |

## Empirical Findings

- **VoiceBank+DEMAND:** PESQ 3.41, CSIG 4.63, CBAK 3.94, COVL 4.12, SSNR 11.10 dB, STOI 0.96. This exceeds the paper's MetricGAN+ row by 0.26 PESQ and 0.48 COVL.
- **Decoder ablations:** Single-Mask reaches PESQ 3.23 and Single-Complex 3.35; neither Dual-Mask nor Dual-Complex reproduces the mixed design. A single three-channel decoder loses 0.91 dB SSNR relative to full CMGAN.
- **Discriminator ablations:** removing the discriminator drops PESQ to 3.24 and COVL to 3.93. MetricGAN+ and PESQ+STOI variants improve selected scores but reduce SSNR.
- **Conformer ablations:** sequential time-then-frequency blocks outperform parallel and frequency-then-time variants. One block adds about 0.4 PESQ over zero blocks; gains saturate after four.
- **Dereverberation:** PESQ-guided CMGAN gives the best average CD and FWSegSNR among the paper's compared systems; CMGAN-LLR instead improves SRMR, especially on real recordings.
- **Super-resolution:** the additive complex-TF variant reports strong VCTK results, while removing complex refinement improves magnitude-only LSD but substantially reduces waveform SNR.
- **Subjective evaluation:** CMGAN ranks first in DNSMOS on four test domains and finishes 0.81 MOS ahead of second-place PHASEN in a 25-participant, 10-sample listening test.

## Limitations

CMGAN is an offline architecture with no reported causal/streaming variant, FLOP count, or ASR evaluation. Its denoising, dereverberation, and super-resolution models are trained separately rather than as one multi-distortion system. The journal also reports 200 STFT bins in Section IV-B but 201 in Appendix Table VI; the latter is consistent with a 400-point real STFT.

## Related Concepts

- [[concepts/two-stage-conformer|Two-Stage Conformer]]
- [[concepts/metricgan|MetricGAN]]
- [[concepts/black-box-metric-optimization|Black-Box Metric Score Optimization]]
- [[concepts/complex-spectral-mapping|Complex Spectral Mapping]]
- [[concepts/power-law-compression|Power-Law Compression]]
- [[concepts/mixed-magnitude-complex-loss|Mixed Magnitude-Complex Loss]]
- [[concepts/speech-super-resolution|Speech Super-Resolution]]
- [[concepts/dereverberation|Dereverberation]]
- [[concepts/voicebank-demand|VoiceBank+DEMAND]]
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/abdulatif-2024-cmgan|Abdulatif, Cao & Yang 2024: CMGAN]] — the TASLP journal extension and primary architecture reference
- [[sources/fu-2019-metricgan|Fu, Liao, Tsao & Lin 2019: MetricGAN]] — origin of the metric-surrogate discriminator
- [[sources/braun-2021-loss-functions-speech-enhancement|Braun & Tashev 2021: A Consolidated View of Loss Functions]] — origin of the power-compressed mixed-loss lineage
