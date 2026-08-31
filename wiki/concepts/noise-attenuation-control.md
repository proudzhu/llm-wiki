---
type: concept
created: 2026-08-31
updated: 2026-08-31
sources:
  - raw/papers/shetu-2026-munet/full-text.md
tags:
  - speech-enhancement
  - noise-suppression
  - post-processing
  - tunable-inference
---

# Noise Attenuation Control

**Noise attenuation control (NAL control)** is a post-processing mechanism for DNN-based speech enhancement that allows a configurable trade-off between noise suppression and speech quality at inference time, without retraining the model. Given an enhanced estimate $\hat{\mathbf{s}}$ and estimated residual noise $\hat{\mathbf{n}}=\mathbf{x}-\hat{\mathbf{s}}$, the adjusted output is:

$$\hat{\mathbf{s}}_{-\text{dB}}=\hat{\mathbf{s}}+\beta\,\hat{\mathbf{n}}, \qquad \beta=\sqrt{\frac{P_{\hat{s}}}{P_{\hat{n}}\cdot 10^{(\text{NAL}_{\text{dB}}/10)}}}$$

where $P_{\hat{s}}$ and $P_{\hat{n}}$ are the mean powers of the enhanced speech and residual noise, and $\text{NAL}_{\text{dB}}$ is the user-defined noise attenuation level in dB. A more negative NAL mixes *more* noise back into the output — paradoxically improving PESQ, because aggressive neural suppressors tend to distort non-harmonic speech components along with the noise.

## Origin

The formulation is inspired by the parametric multichannel Wiener filter of Braun et al. (2015), applied by [[sources/shetu-2026-munet|Shetu et al. 2026]] as a user-facing control on their μNet model. This mirrors how classical hearing-aid noise reduction exposes a suppression-depth parameter to the fitter/user.

## Relationship to Power-Law Compression

Shetu et al. empirically show that the power-law compression factor (PF, α) and NAL act as **near-equivalent knobs** on the same speech-quality vs. suppression trade-off: increasing α improves speech quality at the cost of less noise suppression, functionally like setting a higher (less aggressive) NAL. The difference:

- **PF** requires retraining for each operating point
- **NAL** is configurable at inference time, making it suitable as a user preference setting (e.g., a "noise control" slider on a hearable)

They recommend the NAL mechanism because most listeners prefer strong noise suppression but are highly sensitive to speech distortion: for $\text{NAL}_{\text{dB}}$ up to −35 dB, speech quality improves while noise remains effectively suppressed.

## Results with μNet

On the DNS non-reverb test set (μNet trained with MSE loss, PF 0.3):

| NAL | PESQ | SI-SDR | BAK |
|-----|-----:|-------:|----:|
| default | 1.90 | 13.24 | 4.03 |
| −25 dB | 2.24 | 13.61 | 3.55 |
| −30 dB | 2.27 | 13.53 | 3.71 |

NAL −30 dB achieves the best PESQ of all models in the comparison (including GTCRN at 2.26), at some cost in BAK.

## Related Concepts

- [[concepts/munet|μNet]]
- [[concepts/power-law-compression|Power-Law Compression]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask (cRM)]]

## Related Sources

- [[sources/shetu-2026-munet|Shetu et al. 2026: μNet]]
