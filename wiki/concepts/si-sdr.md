---
type: concept
created: 2026-09-19
updated: 2026-11-17
sources:
  - raw/papers/pan-2025-data-driven-acoustics/full-text.md
  - wiki/sources/wu-2026-dbmif-multimodal-fusion.md
  - raw/papers/li-2024-dbccrn/full-text.md
tags:
  - loss-function
  - speech-enhancement
  - source-separation
  - signal-estimation
---

# SI-SDR (Scale-Invariant Signal-to-Distortion Ratio)

SI-SDR is a waveform-level distance and training loss for signal estimation (speech enhancement, separation) that is invariant to the scale of the estimate: if $\hat{\bm{s}}(t) = c \cdot \bm{s}(t)$ for a non-zero constant $c$, the distance is zero. Proposed by Le Roux et al. 2019 ("SDR — Half-Baked or Well Done?") to fix the ill-posedness of plain SNR/SDR under scale mismatch.

## Formulation

The optimal scale factor is obtained in closed form by projecting the estimate onto the target:

$$
\alpha_t = \arg\min_{\alpha} \|\alpha \bm{s}(t) - \hat{\bm{s}}(t)\|^{2} = \frac{\hat{\bm{s}}^{T}(t)\bm{s}(t)}{\|\bm{s}(t)\|^{2}}
$$

The SI-SDR loss treats the residual as noise and takes the (negative, per frame) log ratio:

$$
\mathcal{J} = -\sum_{t} 10\log\left(\frac{\|\alpha_t \bm{s}(t)\|^{2}}{\|\alpha_t \bm{s}(t) - \hat{\bm{s}}(t)\|^{2}}\right)
$$

## Equivalence to Correlation Maximization (Pan 2025)

Pan 2025 shows the loss simplifies to a monotone function of the Pearson correlation coefficient $\rho_{\bm{s}\hat{\bm{s}}}(t) = \hat{\bm{s}}^{T}(t)\bm{s}(t) / (\|\bm{s}(t)\| \cdot \|\hat{\bm{s}}(t)\|)$:

$$
\mathcal{J} = -\sum_{t} \frac{\rho_{\bm{s}\hat{\bm{s}}}^{2}(t)}{1 - \rho_{\bm{s}\hat{\bm{s}}}^{2}(t)}
$$

Minimizing SI-SDR loss is therefore **equivalent to maximizing the correlation coefficient** between the target and the estimate — a classical signal-processing criterion. This connects the deep-learning loss to the Pearson-correlation view of noise reduction (Cohen, Huang, Chen & Benesty 2009).

## Usage

- Standard evaluation metric and training loss for [[concepts/speech-enhancement|speech enhancement]] and [[concepts/blind-source-separation|source separation]] (e.g., ConvTasNet and successors train directly on SI-SDR).
- Appears throughout the diffusion-for-SE literature as a reporting metric (see [[concepts/diffusion-models-for-speech|diffusion models for speech]] benchmark tables).
- Scale invariance removes the degree of freedom that plain MSE wastes on amplitude matching, letting the network focus on waveform shape; the trade-off is insensitivity to overall level errors.

## Scale Sensitivity in Practice and the SA-SNR Repair (Li et al. 2024)

[[sources/li-2024-dbccrn|Li et al. 2024]] turn the level-insensitivity trade-off above into a quantified failure mode: with an arbitrary gain $\alpha$ on the estimate, SI-SNR loss reduces to $-10\log_{10}(1/\tan^2\theta)$ (and OSI-SNR to $10\log_{10}(1/\sin^2\theta)$), depending **only on the angle** $\theta$ between estimate and target. Enhanced speech therefore emerges at an unpredictable scale — clipping in $[-1,1]$ playback, and per-segment normalization in streaming is worse than the disease (SSNR −7.96 dB vs 6.77 dB for their [[concepts/scale-aware-snr|SA-SNR]] loss, which multiplies the OSI-SNR ratio by a min/max norm-matching factor). Measured with [[concepts/scale-error|ScaleError]]: 16–21% for SI-SNR/OSI-SNR vs 0.014% for SA-SNR on VoiceBank+DEMAND. Plain SNR loss is scale-aware but biased toward shrinkage ($\|\hat{s}_{SNR}\| \le \|s\|$).

## Related Concepts

- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/permutation-invariant-training|Permutation Invariant Training]] — SI-SDR is the usual per-source distance $d[\cdot,\cdot]$ inside the PIT minimization
- [[concepts/frequency-domain-loss|Frequency-Domain Loss]] — the spectral-domain alternative
- [[concepts/wiener-filter|Wiener Filter]]
- [[concepts/scale-aware-snr|Scale-Aware SNR (SA-SNR)]] — OSI-SNR ratio × log-domain norm-matching factor; restores scale awareness
- [[concepts/scale-error|ScaleError]] — peak-amplitude metric exposing scale drift invisible to PESQ

## Related Sources

- [[sources/wu-2026-dbmif-multimodal-fusion|Wu et al. 2026: DBMIF]] — SI-SDR as the headline quality metric (12.42 dB for AC/BC fusion at −15…5 dB)
- [[sources/pan-2025-data-driven-acoustics|Pan 2025: Fundamentals of Data-Driven Approaches to Acoustic Signal Detection, Filtering, and Transformation]] — derives the SI-SDR–correlation-coefficient equivalence in Section 7.2.3
- [[sources/li-2024-dbccrn|Li, Sun, Zhang & Van hamme 2024: DBCCRN]] — angle-only derivation of SI-SNR/OSI-SNR scale blindness; proposes SA-SNR and ScaleError
