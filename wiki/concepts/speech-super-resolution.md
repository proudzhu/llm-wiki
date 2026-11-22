---
type: concept
created: 2026-11-22
updated: 2026-11-22
sources:
  - raw/papers/abdulatif-2024-cmgan/full-text.md
tags:
  - speech-enhancement
  - super-resolution
  - bandwidth-extension
  - complex-domain
  - deep-learning
---

# Speech Super-Resolution

**Speech super-resolution**, also called **bandwidth extension**, reconstructs a high-sampling-rate speech signal from a low-resolution observation. Unlike denoising or dereverberation, the input does not primarily contain an unwanted component to suppress: high-frequency content and intermediate waveform samples are missing and must be synthesized.

In the TASLP CMGAN experiments, 16 kHz references are subsampled by $s\in\{2,4,8\}$, producing 8, 4, or 2 kHz inputs that the model restores to 16 kHz.

## Time-Domain and TF-Domain Views

- **Time-domain interpolation:** map $K$ low-rate samples to $M>K$ high-rate samples. U-Net, TFiLM, and AFiLM are representative approaches discussed by Abdulatif et al.
- **TF-domain inpainting:** treat the missing high-frequency region as missing spectrogram content, analogous to image inpainting. Hybrid systems such as TFNet and neural-vocoder approaches such as NVSR combine spectral and waveform modeling.

A magnitude-only TF system can obtain a low log-spectral distance while still producing a poor waveform because phase is absent or inconsistent. This makes joint magnitude and complex modeling central to CMGAN's formulation.

## CMGAN's Additive Complex-TF Residual

[[concepts/cmgan|CMGAN]] reuses its denoising generator but changes the mask operator from multiplication to addition. If $Y_m$ and $Y_p$ are the power-compressed low-resolution magnitude and phase, the mask decoder predicts an additive residual $M'$:

$$\hat X_r=(M'+Y_m)\cos(Y_p)+\hat X'_r,$$

$$\hat X_i=(M'+Y_m)\sin(Y_p)+\hat X'_i.$$

Here $M'$ is not constrained to a suppression mask in $[0,1]$: it excites missing high-frequency bands while retaining the observed low-frequency input. The separate complex decoder supplies $(\hat X'_r,\hat X'_i)$, and the final waveform is obtained by decompression and ISTFT.

![[raw/papers/abdulatif-2024-cmgan/figures/f2be9896d13e46c2a3ac011da0abb8692673493bfaedc4b41710aee2e22cd8d0.jpg|Low-resolution input spectrogram]]
![[raw/papers/abdulatif-2024-cmgan/figures/b19bd0c6513f64bd07658952ade7d4087dad494366ebfa5cd161b85470ee1062.jpg|Predicted additive high-frequency residual]]
![[raw/papers/abdulatif-2024-cmgan/figures/b37e15758dc7cdc83e7a2b5f16462c638d1e4b1424d807e8dd939f965b600ae5.jpg|Predicted high-resolution spectrogram]]
![[raw/papers/abdulatif-2024-cmgan/figures/05d7b70123a7e13e44cf47e54ea0a634f0b23ddb4d452a570371b19f950c48ad.jpg|High-resolution reference spectrogram]]

*Scale-4 CMGAN super-resolution: low-resolution input, predicted additive residual, output, and reference (TASLP Fig. 7a–d).*

## Evaluation and Metric Trade-Off

The standard evaluation in this paper uses:

- **LSD$_e$ and LSD$_{10}$:** log-spectral distances under natural and base-10 logarithms, computed with 2048-sample Hanning windows and hop 512; lower is better.
- **Waveform SNR:** measures the reconstructed time-domain signal; higher is better.
- **VCTK-Single:** speaker p225, 223 training and 8 test utterances.
- **VCTK-Multi:** first 100 speakers for training and last 8 for testing.

| Scale | Single: LSD$_e$ / LSD$_{10}$ / SNR | Multi: LSD$_e$ / LSD$_{10}$ / SNR |
|------:|:----------------------------------|:---------------------------------|
| 2 | 1.7 / 0.7 / **24.7 dB** | 1.6 / 0.7 / **24.4 dB** |
| 4 | 2.3 / 1.0 / 18.6 dB | 2.2 / 1.0 / **19.1 dB** |
| 8 | 2.6 / 1.1 / 12.9 dB | 2.7 / 1.2 / **14.1 dB** |

CMGAN improves multi-speaker SNR over the best listed baseline by 2.3, 1.0, and 2.1 dB at scales 2, 4, and 8, respectively. The prose claims superiority on every multi-speaker metric, but Table V contradicts that blanket statement: NVSR has lower LSD$_{10}$ at scales 4 and 8 (0.9 versus 1.0 and 1.1 versus 1.2). Single-speaker results are also mixed: AE is slightly better at scale 4, and TFNet has higher scale-8 SNR. The authors attribute the weaker single-speaker results to overfitting on only 223 training utterances.

Removing the complex decoder and metric discriminator (**CMGAN-Mag.**) improves magnitude-only LSD but reduces SNR. At scale 2, for example, LSD$_e$ improves from 1.7 to 1.4 single-speaker while SNR falls from 24.7 to 22.2 dB. **LSD and waveform quality therefore measure different failure modes; optimizing magnitude alone can make the reconstructed signal worse.**

## Related Concepts

- [[concepts/cmgan|CMGAN]] — additive complex-TF residual implementation
- [[concepts/power-law-compression|Power-Law Compression]] — spectral representation used before residual prediction
- [[concepts/complex-spectral-mapping|Complex Spectral Mapping]] — real/imaginary refinement and phase-aware reconstruction
- [[concepts/mixed-magnitude-complex-loss|Mixed Magnitude-Complex Loss]] — the reconstruction objective retained for super-resolution
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/abdulatif-2024-cmgan|Abdulatif, Cao & Yang 2024: CMGAN]] — complex-TF additive-residual formulation and VCTK evaluation
