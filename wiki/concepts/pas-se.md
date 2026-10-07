---
type: concept
created: 2026-10-07
updated: 2026-10-07
sources:
  - raw/papers/ohlenbusch-2026-pas-se/full-text.md
tags:
  - speech-enhancement
  - personalized-speech-enhancement
  - auxiliary-sensor
  - hearables
  - in-ear-microphone
  - neural-network
---

# PAS-SE

**PAS-SE** (personalized auxiliary-sensor speech enhancement) combines [[concepts/personalized-speech-enhancement|personalized speech enhancement (PSE)]] with [[concepts/as-se|auxiliary-sensor speech enhancement (AS-SE)]] for voice pickup in hearables: the enhancement network takes both an outer microphone and an in-ear microphone as input, and is additionally conditioned on an enrollment utterance of the device user. Introduced by Ohlenbusch, Kegler & Stamenovic (ICASSP 2026).

## Architecture

The instantiation in the founding paper modifies the FT-JNF architecture (see [[concepts/joint-nonlinear-filtering|Joint Nonlinear Filtering]]): the magnitude-STFT inputs (OM + IM) are processed by an F-LSTM (512 units, frequency) and causal T-LSTM (128 units, time), producing a magnitude mask applied to the outer-microphone signal. A SpeakerBeam-style speaker encoder (learnable filterbank → 1-D conv block → temporal averaging → 128-dim embedding, 1.810M params) processes the enrollment utterance and conditions the main network multiplicatively on the F-LSTM output.

## Key Findings

- **Complementarity**: PAS-SE systematically outperforms AS-SE, especially on interferer suppression — enrollment conditioning can even compensate for absent in-ear interferer modeling during training.
- **In-ear enrollment is best**: recording the enrollment utterance with the in-ear microphone (matching the auxiliary sensor) beats outer-microphone enrollment in cross-dataset evaluation; PAS-SE with in-ear enrollment outperforms even in-domain-trained AS-SE baselines across datasets.
- **Robustness to noisy enrollment**: in-ear enrollments retain the personalization benefit down to −10 dB enrollment SNR (the in-ear microphone is acoustically shielded), whereas outer-microphone enrollments provide no benefit below 0 dB.

## Related Concepts

- [[concepts/as-se|Auxiliary-Sensor Speech Enhancement (AS-SE)]]
- [[concepts/personalized-speech-enhancement|Personalized Speech Enhancement (PSE)]]
- [[concepts/target-speaker-extraction|Target Speaker Extraction (TSE)]] — PSE is the special case where the target is always the device user
- [[concepts/td-speakerbeam|TD-SpeakerBeam]] — source of the speaker-encoder branch
- [[concepts/hearables|Hearables]]

## Related Sources

- [[sources/ohlenbusch-2026-pas-se|Ohlenbusch, Kegler & Stamenovic 2026: PAS-SE]] — founding paper
