---
type: entity
created: 2026-08-01
updated: 2026-08-01
tags:
  - researcher
  - speech-enhancement
  - cepstral-analysis
  - acoustic-echo-cancellation
---

# Jinjiang Liu

**Affiliation**: College of Computer Science, Inner Mongolia University, China
**Role**: Researcher (PhD student / lab member at Xueliang Zhang's group)
**Research Focus**: Monaural and multi-channel speech enhancement, acoustic echo cancellation, cepstral-domain neural speech processing, inplace convolutional recurrent networks.

## Key Contributions

- Proposed **ICCRN** (Inplace Cepstral Convolutional Recurrent Neural Network), extending the IGCRN architecture with a Cepstral Frequency Block that processes speech in a cepstral space reached via real-valued FFT; achieved state-of-the-art low-SNR STOI on WSJ0 SI-84 with Auditec babble/cafeteria noise while being the most compact model in the comparison (ICASSP 2023) — [[sources/liu-2023-iccrn|Liu & Zhang 2023: ICCRN]]
- Co-developed the **IGCRN** (Inplace Gated Convolutional Recurrent Neural Network) for dual-channel speech enhancement, replacing CRN frequency downsampling with channel-wise LSTM to preserve per-bin spatial cues (Interspeech 2021). IGCRN was subsequently applied to mono and stereo acoustic echo cancellation.

## Related Sources

- [[sources/liu-2023-iccrn|Liu & Zhang 2023: ICCRN]]
