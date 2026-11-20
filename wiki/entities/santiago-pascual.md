---
type: entity
created: 2026-11-20
updated: 2026-11-20
tags:
  - researcher
  - speech-enhancement
  - speech-synthesis
  - generative-models
  - deep-learning
---

# Santiago Pascual

**Affiliation**: Universitat Politècnica de Catalunya (UPC), Barcelona, Spain (TALP Research Center), at the time of SEGAN
**Role**: Researcher
**Research Focus**: Generative deep learning for audio — speech enhancement and speech synthesis with adversarial and diffusion models; waveform-level (raw-audio) neural processing.

## Key Contributions

- Lead author of **SEGAN** — the first generative adversarial network applied to speech enhancement, and the first end-to-end waveform-level enhancement system (28 speakers and 40 noise conditions in one shared parametrization; MOS 3.18 vs. Wiener 2.70 with 16 listeners; PESQ 2.16 / CSIG 3.48 / CBAK 2.94 / COVL 2.80 / SSNR 7.73 on VoiceBank+DEMAND) — [[sources/pascual-2017-segan|Pascual, Bonafonte & Serrà 2017]]
- Public TensorFlow implementation of SEGAN (`santi-pdp/segan`), which made adversarial speech enhancement a widely reproduced baseline

## Related Concepts

- [[concepts/segan|SEGAN]]
- [[concepts/least-squares-gan|Least-Squares GAN (LSGAN)]]
- [[concepts/time-domain-speech-enhancement|Time-Domain Speech Enhancement]]
