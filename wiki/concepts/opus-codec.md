---
type: concept
created: 2026-08-14
updated: 2026-08-14
sources:
  - raw/papers/valin-2022-real-time-plc/full-text.md
tags:
  - opus
  - speech-codec
  - audio-coding
  - real-time
  - low-latency
  - open-source
---

# Opus Audio Codec

**Opus** is a low-latency, open-source audio codec standardized by the IETF as RFC 6716 (2012). Designed for real-time voice and music communication over the Internet, it combines two coding modes — a SILK-based speech mode (linear-prediction-based) and a CELT music mode — and switches between them based on signal characteristics and bitrate.

## Authors and History

Opus was designed by [[entities/jean-marc-valin|Jean-Marc Valin]], Koen Vos, [[entities/timothy-b-terriberry|Timothy B. Terriberry]], and [[entities/christopher-montgomery|Christopher Montgomery]] through the IETF CODEC working group. It builds on Skype's SILK speech codec (for speech at low-to-medium bitrates) and Xiph.Org's CELT transform codec (for music and high bitrates). The Opus 1.0 specification was published as RFC 6716 in September 2012.

## Properties

- **Bitrate range**: 6 kb/s to 510 kb/s
- **Frame sizes**: 2.5, 5, 10, 20, 40, 60 ms
- **Algorithmic delay**: as low as 5 ms (frame size + look-ahead), suitable for real-time communication
- **Sample rates**: 8, 12, 16, 24, 48 kHz
- **Open-source** royalty-free implementation under BSD license, maintained by Xiph.Org and the IETF

## Speech Mode (SILK)

Opus's speech mode is a linear-prediction-based codec derived from Skype's SILK codec. It uses **linear prediction** to encode the spectral envelope and a long-term predictor (pitch predictor) to capture voiced periodicity. This linear-prediction structure is what enables the codec to *inherently avoid discontinuities* at packet-loss boundaries when seeded with appropriate decoder state — a property exploited by [[sources/valin-2022-real-time-plc|Valin et al. 2022]] to skip the cross-fade step otherwise required in causal PLC.

## SILK PLC and Neural PLC Replacement

Opus ships with a classical **SILK PLC** algorithm that extrapolates the speech signal during packet loss using the codec's prediction state. [[sources/valin-2022-real-time-plc|Valin et al. 2022]] demonstrate the first neural PLC operating *inside* the Opus voice coding mode:

- The proposed hybrid LPCNet + predictive RNN PLC **completely replaces the existing SILK PLC**.
- The concealed audio is also used to seed the decoder's long- and short-term prediction state when a new packet arrives after a loss, so the first post-loss packet reconstructs cleanly.
- Because Opus is a stateful codec, the non-causal resynchronization mode (using 5 ms look-ahead to cross-fade backward and forward synthesis) is impossible: the concealed audio is needed to reconstruct the first post-loss packet's decoder state, so the system cannot wait for the next packet before deciding what to play.

## Evaluation

In the Opus codec integration experiment of Valin 2022, utterances were encoded at 24 kb/s using the speech mode with 20-ms frames, with encoder robustness settings tuned for 20% loss. On the dev set (15 listeners × 966 utterances, ACR MOS), the proposed neural PLC significantly outperformed the existing Opus (SILK) PLC.

## Related Concepts

- [[concepts/packet-loss-concealment|Packet Loss Concealment]] — the application that integrates neural PLC into Opus
- [[concepts/lpcnet|LPCNet]] — the neural vocoder used by the integrated PLC
- Speech coding, real-time audio communication (related fields)

## Related Sources

- [[sources/valin-2022-real-time-plc|Valin et al. 2022: Real-Time Packet Loss Concealment With Mixed Generative and Predictive Model]] — replaces Opus's SILK PLC with a neural LPCNet-based PLC
