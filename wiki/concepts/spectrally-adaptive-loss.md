---
type: concept
created: 2026-09-06
updated: 2026-09-06
sources:
  - raw/papers/zhao-2026-spectrally-adaptive-loss/full-text.md
tags:
  - loss-function
  - speech-enhancement
  - deep-learning
  - spectral-analysis
---

# Spectrally Adaptive Loss

The **spectrally adaptive loss** (Zhao & Madhu 2026) is a family of STFT training objectives that modulate the phase-aware loss contribution with a **frequency-wise weight** instead of a scalar mixing coefficient, counteracting the [[concepts/magnitude-phase-compensation-effect|magnitude-phase compensation effect]]'s spectrally non-uniform over-attenuation in mid-to-high frequencies. Two variants exist: a fixed sigmoid-weighted loss and the signal-dependent spectrally adaptive loss proper.

## Key Formulations

Both variants replace the scalar $\lambda$ of the phase-aware compressed loss

$$
\mathcal{L}_{\mathrm{Mix}}=(1-\lambda)\lvert\widehat{S}^{c}-S^{c}\rvert^{2}+\lambda\lvert\widehat{S}^{c}e^{j\phi_{\widehat{S}}}-S^{c}e^{j\phi_{S}}\rvert^{2}
$$

($c=0.3$ power compression) with a frequency-wise weight $w(f)$ on the phase-aware term:

### Sigmoid-Weighted Loss $\mathcal{L}_{\mathrm{Sig}}$

$$
\mathcal{L}_{\mathrm{Sig}}=0.7\cdot\mathcal{L}_{\mathrm{Mag}}+\lambda_{\mathrm{sig}}\cdot\sigma(\beta\cdot(f_{\mathrm{n}}-r))\cdot\mathcal{L}_{\mathrm{Pha}}
$$

with normalised frequency $f_n \in [0,1]$, cut-off $r=0.4$, $\lambda_{\mathrm{sig}}=0.5$, steepness $\beta=-20$. The weight is **fixed** across utterances: high at low frequencies (preserving noise suppression), smoothly suppressed at mid-to-high frequencies (relieving over-attenuation), avoiding spectral banding artefacts.

### Spectrally Adaptive Loss $\mathcal{L}_{\mathrm{Adp}}$

Motivated by the empirical correlation between phase-estimation accuracy and spectral magnitude (high-magnitude regions yield accurate phase; weak regions are error-prone), the weight is derived from the **ground-truth log-magnitude spectrogram**:

$$
\mathcal{L}_{\mathrm{Adp}}=0.7\cdot\mathcal{L}_{\mathrm{Mag}}+\lambda_{\mathrm{adp}}\cdot\mathcal{F}_{s}(\mathcal{N}(\sigma(\mathbb{E}_{t}[\log\lvert S\rvert])))\cdot\mathcal{L}_{\mathrm{Pha}}
$$

where $\mathbb{E}_t$ averages along time, the sigmoid (steepness 15, cut-off 0.5) operates on log-magnitude, $\mathcal{N}$ is min-max normalisation, $\mathcal{F}_s$ is 1D spectral smoothing, and $\lambda_{\mathrm{adp}}=0.6$. The phase-aware term is up-weighted in time-averaged high-energy bands and suppressed where the signal is weak — **signal-dependent** rather than frequency-only.

Both losses are used in multi-resolution form (STFT sizes 320/512/768, 50% overlap), denoted $\mathcal{L}_{\mathrm{MR\_Sig}}$ / $\mathcal{L}_{\mathrm{MR\_Adp}}$.

## Empirical Findings (HyST-Net, DNS Challenge)

- Both variants hold broadband metrics (PESQ/ESTOI/DNSMOS) on par with the scalar-$\lambda$ baseline — these metrics are dominated by low frequencies.
- In the HF band (4–8 kHz): C-RMSE −9.5%, M-RMSE −15.2%, LSD −1.18 dB, SI-SDR +0.43 dB vs baseline.
- Only $\mathcal{L}_{\mathrm{Adp}}$ also improves the MF band (2–4 kHz) across all metrics — the fixed sigmoid is signal-agnostic and misses frequency-wise energy variation.

## Related Concepts

- [[concepts/magnitude-phase-compensation-effect|Magnitude-Phase Compensation Effect]] — the failure mode these losses target
- [[concepts/frequency-domain-loss|Frequency Domain Loss for Time-Domain Networks]] — the broader loss family
- [[concepts/power-law-compression|Power-Law Compression]] — the $c=0.3$ compression shared by both loss terms
- [[concepts/hyst-net|HyST-Net]] — the evaluation backbone
- [[concepts/generalized-loss-function|Generalized Loss Function]] — the exponent-parameterized magnitude-loss family

## Related Sources

- [[sources/zhao-2026-spectrally-adaptive-loss|Zhao & Madhu 2026: Spectrally Adaptive Loss for Streaming Speech Enhancement]]
- [[sources/zheng-2023-survey-frequency-domain-speech-enhancement|Zheng et al. 2023: Sixty Years of Frequency-Domain Monaural Speech Enhancement]] — surveys the magnitude-phase compensation effect in RI-MSE losses
