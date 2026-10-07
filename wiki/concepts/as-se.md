---
type: concept
created: 2026-10-07
updated: 2026-10-07
sources:
  - raw/papers/ohlenbusch-2026-pas-se/full-text.md
tags:
  - speech-enhancement
  - hearables
  - in-ear-microphone
  - bone-conduction
  - auxiliary-sensor
  - neural-network
---

# Auxiliary-Sensor Speech Enhancement (AS-SE)

Auxiliary-sensor speech enhancement (AS-SE) refers to speech enhancement systems that use both an outer microphone and an auxiliary body-conduction sensor — typically an in-ear microphone, or alternatively an accelerometer — as input. The term was broadly formulated by Ohlenbusch et al. (2026), who systematized the approach in the context of own-voice pickup for hearables.

## Rationale

Modern hearables include microphones inside or near the occluded ear canal (typically for active noise reduction). These in-ear microphones are acoustically shielded from environmental noise and interfering talkers by the device, while the user's own voice is picked up predominantly through [[concepts/bone-conduction|body conduction]] — yielding a substantial own-voice SNR advantage. However, the in-ear signal suffers time- and user-varying band-limitation, nonlinearities, and additive body-produced noises, so it cannot be used directly; it serves as an auxiliary *input* to a network that estimates the clean signal at the outer microphone.

## Signal Model

In the STFT domain, outer and in-ear microphone signals decompose as

$$
Y_{\{o,i\}} = S_{\{o,i\}} + N_{\{o,i\}} + V_{\{o,i\}},
$$

with own voice $S$, noise $N$, and interfering talkers $V$. The key design question is how $N_i$ and $V_i$ (noise/interferer leakage into the in-ear microphone) are modeled during training, since datasets with recorded in-ear interferer signals are scarce.

## Training-Time Augmentation Configurations

Ohlenbusch et al. (2026) ablate four configurations (evaluated with an FT-JNF network, see [[concepts/joint-nonlinear-filtering|Joint Nonlinear Filtering]]):

| Config | OM noise | OM interf. | IM noise | IM interf. |
|--------|----------|-----------|----------|-----------|
| A | ✓ | ✓ | ✗ | ✗ |
| B | ✓ | ✗ | ✓ | ✗ |
| C | ✓ | ✓ | ✓ | ✗ |
| D | ✓ | ✓ | ✓ | $a \cdot V_o$, $a \sim U[0.001, 1]$ |

Findings:

- **Configuration A collapses** (SI-SDR −0.92 dB even for noise-only in-domain) — in-ear noise leakage must be modeled during training.
- **Cross-dataset generalization requires interferer modeling** (C or D): trained on Vibravox (close-talk OM) and evaluated on Oldenburg (device outer-face OM), configuration D's attenuated in-ear interferer approximation achieves the best interferer suppression (SI-SDR 7.20 dB vs. 2.62 dB for B), nearing in-domain-trained baselines without any recorded in-ear interferer data.

## Trade-offs vs. PSE

AS-SE can be used by any user without a setup procedure, but the resulting system may not generalize across devices due to unique array properties or acoustic design of the hearable — mitigated by the augmentation configurations above. [[concepts/personalized-speech-enhancement|PSE]] has the complementary trade-off (enrollment required, device-agnostic). Their combination is [[concepts/pas-se|PAS-SE]].

## Related Concepts

- [[concepts/pas-se|PAS-SE]] — enrollment-based personalization of AS-SE
- [[concepts/personalized-speech-enhancement|Personalized Speech Enhancement (PSE)]]
- [[concepts/bone-conduction|Bone Conduction]] — how own voice reaches the in-ear sensor
- [[concepts/hearables|Hearables]] — the application platform
- [[concepts/joint-nonlinear-filtering|Joint Nonlinear Filtering]] — FT-JNF backbone used in the systematic study

## Related Sources

- [[sources/ohlenbusch-2026-pas-se|Ohlenbusch, Kegler & Stamenovic 2026: PAS-SE]] — systematizes the AS-SE term, benchmark, and training configurations
