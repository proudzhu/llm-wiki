---
type: concept
created: 2026-11-21
updated: 2026-11-22
sources:
  - raw/papers/braun-2021-loss-functions-speech-enhancement/full-text.md
  - raw/papers/zhao-2026-spectrally-adaptive-loss/full-text.md
  - raw/papers/westhausen-2022-tplcnet/full-text.md
  - raw/papers/abdulatif-2024-cmgan/full-text.md
tags:
  - loss-function
  - speech-enhancement
  - phase-aware-loss
  - training-objective
---

# Mixed Magnitude-Complex Loss

A **mixed magnitude-complex loss** combines a magnitude-only criterion $\mathcal{L}_{\mathrm{mag}}$ with a phase-aware complex criterion $\mathcal{L}_{\mathrm{complex}}$ through a single mixing weight:

$$
\mathcal{L}_{\mathrm{mix}} = (1-\beta)\,\mathcal{L}_{\mathrm{mag}} + \beta\,\mathcal{L}_{\mathrm{complex}}, \qquad 0 \le \beta \le 1 .
$$

The form was systematized by [[sources/braun-2021-loss-functions-speech-enhancement|Braun & Tashev 2021]] (eq. 21), who tabulated it for every metric family in their loss taxonomy and measured $\beta$ sweeps for each — making it the "consolidated time-frequency loss" that later low-complexity systems cite by name.

## The Key Empirical Claim

Braun & Tashev's result is stronger than "a mixture can help": sweeping $\beta$ for **every** metric pair that has both a magnitude and a complex form produced a PESQ curve that rises from the magnitude-only endpoint, peaks in the interior, and falls toward the complex-only endpoint. All five mixture rows beat both endpoints.

The setting makes this non-obvious: their network predicts a **real-valued gain** $G(k,\ell)\in[0,1]$, so $\widehat{S}=GX$ always carries the noisy phase. The complex term therefore cannot reward phase estimation — there is none. What it changes is the magnitude the gain converges to, which is exactly the [[concepts/magnitude-phase-compensation-effect|magnitude–phase compensation effect]] in reverse: a phase-aware complex loss pulls $G$ toward the phase-dependent compromise magnitude, and the magnitude term re-anchors it at the perceptually correct value.

## Reported Optima and Outcomes (CHiME-2, PESQ / SI-SDR)

| Magnitude term | Complex term | Best mixed result | Magnitude-only | Complex-only |
|:---|:---|:---|:---|:---|
| magMSE | cMSE | 3.17 / 9.58 | 3.16 / 9.57 | 3.10 / 9.58 |
| magMAE | cMAE (RI loss) | 3.25 / **9.75** | 3.25 / 9.73 | 3.08 / 9.68 |
| magComp | cComp | **3.31** / 9.42 | 3.25 / 9.45 | 2.88 / 9.21 |
| SNR | SDR | 3.19 / 9.66 | 3.15 / 9.54 | 3.11 / 9.62 |
| magCorr | cCorr | 3.16 / 9.58 | 3.16 / 9.56 | 3.11 / 9.60 |

Two structural observations follow from the table:

- **The mixture gain is largest exactly where one endpoint is broken.** cComp alone is the worst complex loss in the study (2.88) yet the compressed mixture is the best row overall (3.31) — mixing is a repair mechanism, not a uniform refinement.
- **The optimal $\beta$ is metric-pair specific** (compressed pair peaks near $\beta=0.3$), and "out-of-metric" crossings — pairing the best magnitude loss with the best complex loss — did not improve on the in-row mixture.

## Later Instances

- [[sources/westhausen-2022-tplcnet|tPLCnet (Westhausen & Meyer 2022)]] uses $\alpha=0.1$ on a 32 ms STFT for the same $(1-\alpha)|\hat{X}|-\alpha|\hat{X}-X|$ structure in packet-loss concealment, and finds the magnitude-only variant matches the combined one in that regime.
- [[sources/zhao-2026-spectrally-adaptive-loss|Zhao & Madhu 2026]] keep the scalar $\beta$ as their baseline ($\lambda=0.3$, the value Braun & Tashev report as optimal) and replace it with a frequency-wise or signal-dependent weight — see [[concepts/spectrally-adaptive-loss|Spectrally Adaptive Loss]].
- [[concepts/complex-compressed-mse|CCMSE]] is the compressed-magnitude instantiation carried into AEC postfilters (Bark-AEC, DiffVQE).

## Related Concepts

- [[concepts/magnitude-phase-compensation-effect|Magnitude-Phase Compensation Effect]]
- [[concepts/spectrally-adaptive-loss|Spectrally Adaptive Loss]] — replaces the scalar $\beta$ with a spectral weight
- [[concepts/power-law-compression|Power-Law Compression]]
- [[concepts/complex-compressed-mse|Complex Compressed MSE (CCMSE)]]
- [[concepts/frequency-domain-loss|Frequency Domain Loss]]
- [[concepts/log-spectral-distance|Log-Spectral Distance (LSD)]]
- [[concepts/pesq|PESQ]] / [[concepts/si-sdr|SI-SDR]] — the two metrics the mixture trades between

## Related Sources

- [[sources/braun-2021-loss-functions-speech-enhancement|Braun & Tashev 2021: A Consolidated View of Loss Functions for Supervised Deep Learning-Based Speech Enhancement]] — defines eq. (21), sweeps $\beta$ per metric pair, and establishes the always-improves result
- [[sources/zhao-2026-spectrally-adaptive-loss|Zhao & Madhu 2026: Spectrally Adaptive Loss for Streaming Speech Enhancement]] — adopts $\lambda=0.3$ as the baseline scalar mixture and diagnoses its spectral non-uniformity
- [[sources/westhausen-2022-tplcnet|Westhausen & Meyer 2022: tPLCnet]] — $\alpha=0.1$ mixed magnitude+complex MAE for PLC; magnitude-only matches it
- [[sources/abdulatif-2024-cmgan|Abdulatif, Cao & Yang 2024: CMGAN]] — [[concepts/cmgan|CMGAN]] instantiates the mixture on $c=0.3$ power-compressed spectra as $\mathcal L_{TF}=0.7\mathcal L_{Mag}+0.3\mathcal L_{RI}$, selected by grid search. The total generator objective adds waveform $L_1$ and a 0.01-weighted PESQ-surrogate term. Removing waveform loss raises PESQ slightly (3.41 → 3.45) but costs 1.39 dB SSNR, demonstrating that the spectral mixture alone does not control waveform-domain quality.
