---
type: concept
created: 2026-06-19
updated: 2026-10-24
sources:
  - raw/papers/ostergaard-2026-own-voice-cancellation/full-text.md
  - raw/papers/zhu-2026-g-map-se-guided-speech-enhancement/full-text.md
  - raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/full-text.md
  - raw/papers/pan-2025-data-driven-acoustics/full-text.md
  - raw/papers/ohlenbusch-2026-pas-se/full-text.md
  - raw/papers/zhang-2025-mbenet/full-text.md
tags:
  - speaker-recognition
  - representation-learning
---

# Speaker Embedding

A speaker embedding is a fixed-dimensional vector representation extracted from a speech utterance that captures speaker-specific characteristics. Speaker embeddings are used for speaker verification, diarization, and as conditioning features in personalized speech enhancement. Common extractors include x-vectors and ECAPA-TDNN.

## Key Formulations

- $Typically 128-512 dimensional vectors$
- $Often $\ell_2$-normalized to project onto the unit hypersphere$
- $Extracted from a frozen pretrained speaker recognition model$

## Auxiliary Encoder Architectures

In enrollment-conditioned tasks ([[concepts/target-speaker-extraction|TSE]], [[concepts/own-voice-cancellation|OVC]]), the speaker embedding is produced by an **auxiliary network** (auxiliary encoder). Two families are commonly used:

| Auxiliary type | Architecture | Compute | Notes |
|----------------|--------------|---------|-------|
| ConvTasNet-based | Temporal convolutional network | ~1.67 GMAC/s | Standard in [[concepts/td-speakerbeam|TD-SpeakerBeam]] |
| Linear RNN-based | Bidirectional [[concepts/mingru|MinGRU]] / Mamba blocks | ~0.26 GMAC/s | Better SDR on full-mixture condition at ~6× lower compute |

Østergaard et al. (2026) showed that linear RNN auxiliary encoders provide better speaker representations than ConvTasNet-based ones for speaker conditioning in OVC, while substantially reducing compute.

Ohlenbusch et al. 2026 [[sources/ohlenbusch-2026-pas-se|(Ohlenbusch 2026)]] use a jointly-trained SpeakerBeam-style encoder (learnable filterbank → 1-D conv block → temporal averaging, 1.810M params) producing a 128-dim embedding applied by multiplicative conditioning on the enhancement network's F-LSTM output — and show that the enrollment *sensor* matters as much as the encoder: in-ear-microphone enrollments (acoustically shielded) preserve conditioning benefits down to −10 dB enrollment SNR, while outer-microphone enrollments break down below 0 dB.

Embedding-based cues also face competition from **sensor-derived cues**: on the ABCS-2Mix benchmark, the AC-only MBENet variant using a [[concepts/speaker-embedding|speaker-embedding]] clue reaches 11.19 dB SI-SDR / 2.68 PESQ, while the same backbone using the bone-conduction signal as clue reaches 16.67 dB / 3.17 (Zhang et al. 2025, [[sources/zhang-2025-mbenet|MBENet]]) — under strong noise (SNR −5…10 dB, SIR 0–2 dB), a concurrent noise-immune observation of the target is far more informative than a pre-recorded embedding. See [[concepts/bone-conduction|bone conduction]] as a TSE clue.

## Audio Clue Encoder Families in TSE

Zmolikova et al. 2023 [[sources/zmolikova-2023-neural-target-speech-extraction-overview|(Zmolikova 2023)]] survey three families of audio clue encoders used in [[concepts/target-speaker-extraction|target speech extraction]]:

| Family | Training task | Strengths | Limitations |
|:-------|:--------------|:---------|:------------|
| **i-vectors** [50] | GMM-UBM mean supervector adaptation | Captures speaker + channel; useful when enrollment and mixture share channel | Outperformed by NN-based; pre-2010 paradigm |
| **NN-based (d-vectors, [[concepts/ecapa-tdnn|x-vectors]])** [51] | Speaker classification with a pooling layer | Highly speaker-discriminative; robust to channel/content; large public models available | Designed for verification, not optimal for TSE |
| **Jointly-learned** [10], [31] | Co-trained with TSE extraction module | Directly optimized for TSE; captures task-relevant features | Smaller training corpora; less robust than pre-trained |

A common middle ground is to **pre-train then fine-tune** a NN-based encoder jointly with the TSE task, or to use **multi-task training** that adds a speaker-discriminative auxiliary loss on the embeddings [46]. The review notes that, to its knowledge, pure fine-tuning of a pre-trained encoder for TSE has not been thoroughly explored at the time of writing.

## Voiceprint Extraction as Transformation (Pan 2025)

[[sources/pan-2025-data-driven-acoustics|Pan 2025]] frames voiceprint extraction as a **signal transformation** task (not detection): because usage-time speakers differ from training speakers (users won't upload their data), the extractor $g(\cdot)$ must generalize across distributions — the **domain mismatch** problem. Two learning strategies: (i) **classification** — train with a softmax head + cross-entropy over $L$ training speakers, then discard the head (larger, more diverse speaker sets reduce mismatch); (ii) **contrastive/clustering** — minimize same-speaker $\|\bm{z}_n - \bm{z}_i\|^{2}$, hinge-truncate different-speaker distances at $\zeta_0$. The canonical extractor is the **TDNN x-vector** network: five 1-D conv layers over 24-dim MFCC slices (kernels 5/5/7/1/1 with dilated time context, channels 512/512/512/512/1500) → statistics pooling (mean + std, 3000-dim) → FC to a 512-dim embedding. See [[concepts/speaker-verification|Speaker Verification]] for the detection-flavored applications built on these embeddings.

## Related Concepts

- [[concepts/ecapa-tdnn|ECAPA-TDNN]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/prior-matching|Prior Matching]]
- [[concepts/personalized-speech-enhancement|Personalized Speech Enhancement (PSE)]]
- [[concepts/own-voice-cancellation|Own-Voice Cancellation (OVC)]]
- [[concepts/td-speakerbeam|TD-SpeakerBeam]]
- [[concepts/mamba-mingru|Mamba-MinGRU]]
- [[concepts/target-speaker-extraction|Target Speaker Extraction (TSE)]]
- [[concepts/target-speaker-vad|Target-Speaker VAD (TS-VAD)]]
- [[concepts/speaker-verification|Speaker Verification]] — the detection-flavored application family built on embeddings
- [[concepts/pas-se|PAS-SE]]
- [[concepts/bone-conduction|Bone Conduction]] — sensor-derived cue competing with embeddings under noise

## Related Sources

- [[sources/ostergaard-2026-own-voice-cancellation|Østergaard et al. 2026: Don't Listen to Me — Own-Voice Cancellation]]
- [[sources/zhu-2026-g-map-se-guided-speech-enhancement|G-MaP-SE: Guided Speech Enhancement via GMM-Based Prior Matching (Interspeech 2026)]]
- [[sources/zmolikova-2023-neural-target-speech-extraction-overview|Zmolikova et al. 2023: Neural Target Speech Extraction: An Overview]]
- [[sources/pan-2025-data-driven-acoustics|Pan 2025: Fundamentals of Data-Driven Approaches to Acoustic Signal Detection, Filtering, and Transformation]] — voiceprint extraction as signal transformation; TDNN x-vector architecture details (Section 6)
- [[sources/ohlenbusch-2026-pas-se|Ohlenbusch, Kegler & Stamenovic 2026: PAS-SE]] — jointly-trained 128-dim embedding; enrollment-sensor robustness analysis
- [[sources/zhang-2025-mbenet|Zhang, Feng, Liu, Zhang & Li 2025: MBENet]] — embedding cue vs. bone-conduction cue ablation under noise