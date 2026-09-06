---
type: concept
created: 2026-09-06
updated: 2026-09-06
sources:
  - raw/papers/wang-2021-magnitude-phase-compensation/full-text.md
tags:
  - evaluation-metric
  - speech-separation
  - speech-enhancement
  - phase-estimation
---

# Magnitude SNR and Phase SNR (mSNR / pSNR)

**mSNR** (magnitude SNR) and **pSNR** (phase SNR) are diagnostic evaluation metrics that decompose speech separation/enhancement quality into separate magnitude- and phase-accuracy measurements. mSNR follows earlier separation work (Isik et al. 2016); the paired use with pSNR for diagnosing the [[concepts/magnitude-phase-compensation-effect|magnitude-phase compensation effect]] is due to [[sources/wang-2021-magnitude-phase-compensation|Wang, Wichern & Le Roux 2021]].

## Definitions

$$\text{mSNR}=10\,\text{log}_{10}\frac{\sum_{t,f}|S(t,f)|^{2}}{\sum_{t,f}\big||S(t,f)|-|\hat{S}(t,f)|\big|^{2}}$$

$$\text{pSNR}=10\,\text{log}_{10}\frac{\sum_{t,f}|S(t,f)|^{2}}{\sum_{t,f}\big|S(t,f)-|S(t,f)|e^{j\angle\hat{S}(t,f)}\big|^{2}}$$

pSNR is computed with **oracle magnitude supplied**, so it isolates the quality of the estimated phase $\angle\hat{S}(t,f)$ alone; mSNR isolates the quality of the estimated magnitude $|\hat{S}(t,f)|$.

## Diagnostic Use

On WHAMR! enhancement (Wang 2021, Table I), the decomposition separates effects that broadband metrics conflate:

| Model | mSNR (dB) | pSNR (dB) | Reading |
|-------|-----------|-----------|---------|
| MSA, no re-synthesis | **13.05** | – | best learned magnitude — direct magnitude estimation avoids compensation |
| Phase model | – | **12.4** | best phase — oracle-magnitude phase loss |
| RI | 12.66 | 10.8 | good magnitude *and* phase, but magnitude partly compensated |
| RI+Mag | 12.84 | 10.35 | magnitude loss improves mSNR but *degrades* pSNR |
| Wav×0+Mag | 11.36 | −3.64 | good magnitude with near-random phase — PESQ/eSTOI stay good (2.67/80.6) |

The RI vs. RI+Mag contrast is the core evidence for the compensation effect: adding a magnitude loss trades a little phase accuracy (pSNR −0.4 dB) for better magnitude (mSNR +0.2 dB) — and the perceptual metrics follow the magnitude, not the phase.

## Related Concepts

- [[concepts/magnitude-phase-compensation-effect|Magnitude-Phase Compensation Effect]]
- [[concepts/pesq|PESQ]] — magnitude-dominant perceptual metric
- SI-SDR-style time-domain metrics — phase-sensitive, compensation-favoring (no dedicated page; see [[concepts/frequency-domain-loss|Frequency Domain Loss]] for the metric trade-offs)
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/wang-2021-magnitude-phase-compensation|Wang, Wichern & Le Roux 2021: On the Compensation Between Magnitude and Phase in Speech Separation]] — introduces the mSNR/pSNR decomposition for the analysis
