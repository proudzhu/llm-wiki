---
type: concept
created: 2026-05-16
updated: 2026-05-16
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

## Related Sources

- [[sources/wang-2022-fusing-bc-ac-complex-domain-se|Wang, Zhang & Wang 2022: Fusing BC and AC for Complex-Domain SE]]
