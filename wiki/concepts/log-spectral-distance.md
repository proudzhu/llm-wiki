---
type: concept
created: 2026-11-21
updated: 2026-11-21
sources:
  - raw/papers/braun-2021-loss-functions-speech-enhancement/full-text.md
  - raw/papers/zhao-2026-spectrally-adaptive-loss/full-text.md
  - raw/papers/nguyen-2023-predictive-plc/full-text.md
tags:
  - loss-function
  - speech-enhancement
  - evaluation-metric
  - spectral-analysis
  - perceptual-weighting
---

# Log-Spectral Distance (LSD)

The **log-spectral distance (LSD)** compares two spectra in the log-magnitude domain:

$$
\mathrm{LSD} = \left\langle \left| \log_{10}\widehat{A} - \log_{10}A \right|^{2} \right\rangle,
$$

with $\langle\cdot\rangle$ the mean over time and frequency. It was a standard distortion measure of classical model-based speech enhancement (Ephraim & Malah's MMSE-LSA log-spectral amplitude estimator, 1985) and remains a common evaluation metric where full-band behaviour matters — e.g. packet-loss concealment, where PESQ/STOI are band-limited (see [[concepts/plcmos|PLCMOS]]).

## As a Training Loss: the Negative Result

[[sources/braun-2021-loss-functions-speech-enhancement|Braun & Tashev 2021]] trained a real-time FF+GRU gain predictor on reverberant CHiME-2 with LSD as the objective. They note that prior LSD losses had only been used in networks predicting the log-power spectrum directly, not in filter-prediction networks. The result was **worse than plain MSE**: PESQ 3.04 (LSD) vs. 3.16 (magMSE), SI-SDR 8.59 vs. 9.57 dB.

The diagnosis is in the logarithm's unboundedness: log compression produces large errors at **low-energy bins**, which carry little perceptual weight, so the loss spends capacity on perceptually irrelevant detail. The paper's remedy is not to limit the log (which it calls suboptimal) but to reweight it by target-signal power.

## Weighted LSD (wLSD)

$$
W_{\mathrm{lsd}}(k,\ell) = \left| \widehat{S}(k,\ell) + \gamma\, X(k,\ell) \right|^{0.3}, \qquad
\mathcal{L}_{\mathrm{wLSD}} = \left\langle W_{\mathrm{lsd}} \left| \log_{10}\widehat{A} - \log_{10}A \right|^{2} \right\rangle,
$$

with $\gamma = 0.1$ chosen so the noisy signal blends in and prevents zero weights where suppression is strong; the 0.3 exponent matches the power-law compression exponent used elsewhere in the same study. Effect: PESQ 3.19 (wLSD) vs. 3.04 (LSD), SI-SDR 9.12 vs. 8.59 dB — the weighting clears the plain-MSE bar (3.16) that the unweighted LSD misses.

## Phase-Aware LSD (PLSD)

$$
\mathrm{PLSD} = \left\langle \left| \log_{10}\left|\frac{\widehat{S}}{S}\right| \cdot \left(2 - \Re\left\{\frac{\widehat{S}}{S}\right\}\right) \right| \right\rangle,
$$

where $\Re\{\widehat{S}/S\} = \cos(\varphi_{\widehat{S}}-\varphi_S)$. The phase term is multiplied **bin-wise** by the magnitude term, so it vanishes where the magnitude error vanishes; the constant 2 keeps the factor in $[1,3]$ so a perfectly magnitude-matched bin cannot reach zero loss. The same target-power weight can be applied (wPLSD).

PLSD alone gave **no** advantage over LSD (3.03 vs. 3.04 PESQ, 8.31 vs. 8.59 dB SI-SDR); wPLSD did slightly better than magnitude-only wLSD (3.21 vs. 3.19). The paper's conclusion is that for log-domain criteria, suppressing the low-energy bins matters more than adding a phase term.

## Why It Still Appears

- **Evaluation**: LSD is unbounded and full-band, so it exposes errors above the 5 kHz horizon of [[concepts/stoi|STOI]] and the 8 kHz analysis limit of PESQ — used for 48 kHz evaluation ([[sources/kim-2026-faster-enhancer|Kim 2026]]) and for PLC ([[sources/nguyen-2023-predictive-plc|Nguyen et al. 2023]]).
- **Training**: multi-resolution spectral losses (auraloss-style) use a log-magnitude term alongside spectral convergence; the compression variant is preferred where perceptually weighted errors are wanted.

## Related Concepts

- [[concepts/frequency-domain-loss|Frequency Domain Loss]]
- [[concepts/power-law-compression|Power-Law Compression]] — the bounded, positive-semi-definite alternative to the log
- [[concepts/mixed-magnitude-complex-loss|Mixed Magnitude-Complex Loss]]
- [[concepts/magnitude-phase-compensation-effect|Magnitude-Phase Compensation Effect]]
- [[concepts/pesq|PESQ]] / [[concepts/stoi|STOI]]
- [[concepts/spectrally-adaptive-loss|Spectrally Adaptive Loss]] — also weights the phase-aware term by target magnitude structure

## Related Sources

- [[sources/braun-2021-loss-functions-speech-enhancement|Braun & Tashev 2021]] — LSD as a filter-prediction loss; introduces wLSD, PLSD, wPLSD; reports the LSD-below-MSE result
- [[sources/nguyen-2023-predictive-plc|Nguyen, Nguyen & Khong 2023: Full-Band Blind PLC]] — LSD as a full-band evaluation metric for 48 kHz PLC
- [[sources/kim-2026-faster-enhancer|Kim 2026: faster-enhancer.c]] — LSD among the fullband metrics used when PESQ/STOI's band limits bite
