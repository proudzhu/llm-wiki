---
type: concept
created: 2026-05-16
updated: 2026-09-06
sources:
  - raw/papers/wang-2021-magnitude-phase-compensation/full-text.md
tags:
  - speech-enhancement
  - deep-learning
  - complex-domain
---

# Complex Spectral Mapping

Complex spectral mapping (CSM) is a speech enhancement paradigm that predicts the **real and imaginary (RI)** components of the clean speech STFT directly, rather than operating on magnitude alone. By jointly estimating both RI components, CSM preserves phase information — a critical advantage over magnitude-only methods that rely on noisy phase for reconstruction.

## Formulation

Given the noisy complex spectrogram $Y[t,f] = Y_r[t,f] + jY_i[t,f]$:

$$\hat{S}_r[t,f], \hat{S}_i[t,f] = f_\theta(Y_r[t,f], Y_i[t,f])$$

The model $f_\theta$ maps the 2-channel RI input to 2-channel RI output. A common training objective is the RI-Magnitude loss:

$$L = \|S_r - \hat{S}_r\|_1 + \|S_i - \hat{S}_i\|_1 + \||S| - |\hat{S}|\|_1$$

## Magnitude Loss and the Compensation Effect

[[sources/wang-2021-magnitude-phase-compensation|Wang, Wichern & Le Roux 2021]] analyze CSM's RI loss through the [[concepts/magnitude-phase-compensation-effect|magnitude-phase compensation effect]]: with the RI loss alone, the estimated magnitude compensates for the inaccurate estimated phase (the projection of $S$ onto the $\angle\hat{S}$ direction), so the magnitude is systematically compressed wherever the phase error is large. Adding a magnitude loss ($\mathcal{L}_{\text{RI+Mag}}$) balances complex- and magnitude-domain approximation — on WHAMR! it improves PESQ (2.49 → 2.92), eSTOI (80.3 → 81.9%), and WER at a small SI-SDR cost (9.1 → 8.6 dB). Conversely, when only a good magnitude is needed (e.g. robust ASR), direct magnitude spectrogram approximation avoids modelling phase altogether and yields better magnitudes (see [[concepts/magnitude-phase-compensation-effect|the effect's formulation]]).

## Advantages Over Magnitude Masking

| Aspect | Magnitude Masking | Complex Spectral Mapping |
|--------|:-:|:-:|
| Phase handling | Uses noisy phase | Predicts clean phase implicitly |
| Mask range | [0, 1] or unbounded | Unconstrained RI |
| Performance ceiling | Limited by phase error | Higher (phase-aware) |
| Typical architectures | CRN, U-Net | DC-CRN, DCCRN, FullSubNet |

## Key Architectures

- **DC-CRN (Wang 2022)**: Densely-connected CRN with complex RI inputs/outputs + pointwise skip connections
- **DCCRN (Hu 2020)**: Deep complex CRN with complex LSTM in bottleneck
- **FullSubNet (Hao 2021)**: Full-band + sub-band CSM with attention

## Related Concepts

- [[concepts/bone-conduction|Bone Conduction]]
- [[concepts/bcs-guided-speech-enhancement|BCS-Guided Speech Enhancement]]
- [[concepts/magnitude-phase-compensation-effect|Magnitude-Phase Compensation Effect]] — why the magnitude term in the RI+Mag loss is needed

## Related Sources

- [[sources/wang-2022-fusing-bc-ac-complex-domain-se|Wang, Zhang & Wang 2022: Fusing BC and AC for Complex-Domain SE]]
- [[sources/wang-2021-magnitude-phase-compensation|Wang, Wichern & Le Roux 2021: On the Compensation Between Magnitude and Phase in Speech Separation]] — analyzes the RI loss's implicit magnitude-phase compensation
