---
type: concept
created: 2026-11-17
updated: 2026-11-17
sources:
  - raw/papers/li-2024-dbccrn/full-text.md
tags:
  - loss-function
  - speech-enhancement
  - scale-preservation
---

# Scale-Aware SNR (SA-SNR)

SA-SNR (Li et al. 2024) is a waveform-level training loss that repairs the **scale blindness** of [[concepts/si-sdr|SI-SNR]] and OSI-SNR: it keeps the angular separation objective but multiplies it by a norm-matching regularization factor, so the network is trained to output speech at the *same amplitude* as the target — a prerequisite for streaming enhancement where per-segment normalization is destructive.

## Why SI-SNR/OSI-SNR fail at scale

For an arbitrary gain $\alpha$ on the estimate, SI-SNR loss reduces to $-10\log_{10}(1/\tan^2\theta)$ and OSI-SNR to $10\log_{10}(1/\sin^2\theta)$, with $\theta$ the angle between estimate and target: **the loss is independent of $\alpha$**. Consequences:

- Amplified inputs produce over-scale outputs that clip in $[-1,1]$ playback, smearing the spectrum and degrading PESQ/COVL.
- Global normalization only works offline; normalizing each streaming segment separately breaks loudness continuity (SI-SNR + per-segment normalization: SSNR −7.96 dB vs SA-SNR's 6.77 dB, Table 5 of the paper).
- Plain SNR loss is scale-aware but its optimum is the projection of $s$ onto $\hat{s}$ — always $\|\hat{s}_{SNR}\| \le \|s\|$ (shrinkage) — and its lower bound $-\|s\|^2$ fluctuates with target energy.

## Formulation

$$
\text{SA-SNRLoss}(\hat{s}, s) = -10\log_{10}\left( \frac{\|s_{target}\|^2}{\|e_{noise}\|^2} \cdot \frac{\min\!\left(\frac{\|\hat{s}\|}{\|s\|}, 1\right)}{\max\!\left(\frac{\|\hat{s}\|}{\|s\|}, 1\right)} \right)
$$

The SNR ratio uses the OSI-SNR construction ($s_{target} = \frac{\|\hat{s}\|^2}{\langle\hat{s},s\rangle}s$, $e_{noise} = \hat{s} - s_{target}$; per the paper's §4.2.2 comparison "OSI-SNR versus SI-SNR in the SNR part"). The regularization factor is $e^{-|\log(\|\hat{s}\|/\|s\|)|} \in (0,1]$: symmetric in log-scale, it penalizes over-scaling ($\|s\|/\|\hat{s}\|$) and under-scaling ($\|\hat{s}\|/\|s\|$) alike, pulling the estimate's norm to the target's without SNR's projection shrinkage.

In [[concepts/dbccrn|DBCCRN]] the total objective applies it to both branches: $\mathcal{L} = \text{SA-SNRLoss}(\hat{s},s) + \text{SA-SNRLoss}(\hat{n},n)$ — no coefficients.

## Versus additive regularizers

The paper compares SI-SNR + $\eta\|\hat{s}-s\|$ (L1) and SI-SNR + $\eta(\|\hat{s}\|/\|s\|-1)^2$ (energy constraint), both needing $\eta=100$ ($\eta=1,10$ failed). SA-SNR beats both on all metrics; the difference is twofold — OSI-SNR vs SI-SNR in the SNR part, and a *log-domain norm ratio* vs a *waveform-distance* penalty. Additive waveform penalties reintroduce the regression artifacts SI-SNR was designed to avoid; the multiplicative factor does not.

## Evidence

On VoiceBank+DEMAND with DBCCRN: ScaleError 0.014% (SI-SNR: 18.653%, OSI-SNR: 19.791%); under peak-normalized inputs PESQ drops only 3.16 → 3.15 while SI-SNR drops 2.89 → 2.50. SA-SNR also lifts the base quality itself (PESQ 3.16 vs 2.89 SI-SNR on the same architecture), i.e., scale awareness is not a quality trade-off here.

## Related Concepts

- [[concepts/si-sdr|SI-SDR / SI-SNR]] — the scale-invariant family SA-SNR extends
- [[concepts/scale-error|ScaleError]] — companion metric + scaled-test-set recipe
- [[concepts/dbccrn|DBCCRN]] — architecture trained with SA-SNR
- [[concepts/frequency-domain-loss|Frequency-Domain Loss]] — the spectral-domain alternative

## Related Sources

- [[sources/li-2024-dbccrn|Li, Sun, Zhang & Van hamme 2024: DBCCRN]] — proposing paper