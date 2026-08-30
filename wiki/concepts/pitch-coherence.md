---
type: concept
created: 2026-07-17
updated: 2026-08-30
sources:
  - raw/papers/valin-2021-percepnet-joint-echo-control/full-text.md
  - raw/papers/valin-2018-lpcnet/full-text.md
tags:
  - speech-enhancement
  - acoustic-echo-cancellation
  - pitch
  - periodicity
  - perceptual
---

# Pitch Coherence

Pitch coherence is a perceptually-motivated feature used in the [[concepts/percepnet|PercepNet]] speech enhancement and acoustic echo cancellation system. It quantifies the degree of periodicity in a speech signal at a given pitch period, enabling a neural network to distinguish near-end voiced speech from noise and residual echo that may have similar spectral envelopes but different periodicity structure.

## Definition

In PercepNet, pitch coherence q_y,b(l) is computed per ERB band b for each frame l. The coherence estimation itself uses the full look-ahead, but the feature provided to the DNN is the no-look-ahead version q_y,b(l) (the DNN separately receives look-ahead via the band energy feature Y_b(l+M)).

Pitch coherence is paired with a **non-causal comb filter** controlled by a per-band strength parameter r_b(l) ∈ [0, 1]:

- r_b(l) = 0: no comb filtering (band unchanged)
- r_b(l) = 1: band fully replaced by comb-filtered version (maximum periodicity)

The comb filter removes noise between pitch harmonics, making the signal more periodic. This is important because tones have relatively little masking effect on noise — inter-harmonic noise is particularly perceptible and reduces the perceived voicing/periodicity of speech.

## Precursor: Pitch Correlation in LPCNet

The same periodicity feature appears earlier — and globally rather than per-band — in [[concepts/lpcnet|LPCNet]] (Valin & Skoglund 2018), where a scalar **pitch correlation** $g_p \in (0, 1)$ is one of the 20 conditioning inputs (alongside 18 Bark-scale cepstral coefficients and the pitch period). LPCNet also exploits it at *inference* time: the sampling temperature of the autoregressive excitation distribution is set to $c = 1 + \max(0,\, 1.5\,g_p - 0.5)$, so highly periodic (voiced) frames are sampled from a sharper distribution — a continuous generalization of the earlier practice of multiplying logits by a constant only for voiced sounds. PercepNet later generalized the idea to per-ERB-band coherence, for enhancement rather than synthesis.

## Why It Matters for AEC

In acoustic echo cancellation, residual echo can be hard to distinguish from near-end voiced speech because both are speech-like. Pitch coherence provides a complementary cue to spectral envelope: even when the spectral envelopes overlap, the near-end and far-end signals typically have different pitch periods, so their coherence patterns differ. This helps the PercepNet DNN preserve near-end speech during double-talk while suppressing residual echo.

## Related Concepts

- [[concepts/percepnet|PercepNet]]
- [[concepts/lpcnet|LPCNet]] — earlier global (scalar) pitch-correlation usage
- [[concepts/percepnet-style-neural-post-filter|PercepNet-Style Neural Post Filter]]
- [[concepts/erb-scale|ERB Scale]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]]

## Related Sources

- [[sources/valin-2021-percepnet-joint-echo-control|Valin et al. 2021: Joint Neural Echo Control and Speech Enhancement Based On PercepNet]]
- [[sources/valin-2018-lpcnet|Valin & Skoglund 2018: LPCNet]] — earlier global pitch-correlation feature and its use as the sampling temperature
