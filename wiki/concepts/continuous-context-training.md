---
type: concept
created: 2026-09-15
updated: 2026-09-15
tags:
  - streaming-inference
  - training-methodology
  - real-time-processing
---

# Continuous-Context Training

Continuous-context training is a training methodology for streaming (frame-by-frame) causal models: the network is trained on single continuous segments in one forward pass, with no internal zero padding, so that the convolution context the network sees during training matches the running cache of real past frames it sees at deployment. It was identified as *essential* — not an accuracy optimization — by [[sources/li-2026-realtime-music-separation-dsp|Li et al. 2026]].

## The Failure Mode: Chunk-Padded Training Is Out-of-Distribution for Streaming

Causal convolutions are normally trained on independent chunks, each zero-padded on the left. At inference the same layers see a running cache of *real* past frames. Stacked layers compound the mismatch: a $3\times3$ kernel depends on two past frames, so an $L$-layer stack makes the first $2L$ frames of every chunk padding-dependent. With $L \approx 8$ layers, ~16 of the 65 frames in a 0.755 s chunk — a quarter — sit in a regime that never occurs in deployment.

The consequence is easy to miss with standard evaluation: a chunk-trained model scoring 3.93 dB under the block-wise protocol (which resets state at every block, reproducing the padding regime) collapses to *silent output* within ~2 s when run frame-by-frame with the convolution cache carried, as a DSP runs it. A silent estimate scores exactly 0 dB by construction, which is the signature of the collapse. An ablation by Li et al. attributes the failure to the convolution context, not recurrent state: threading recurrent state across blocks while keeping per-block zero padding costs only ~0.2 dB.

## The Recipe

Training on single continuous 5.8 s segments (one forward pass, no internal padding, cut at a random position, sources re-mixed across tracks as usual) restores frame-by-frame performance to within 0.1 dB of block-wise. The rest of the recipe is unremarkable by design — AdamW at $10^{-4}$, gradient-norm clip 3.0, mixed precision, batch 6. A truncated-BPTT variant must overlap consecutive chunks by $n_{\mathrm{fft}} - H$ samples, or the frame grid skips a position at every boundary.

The general lesson for any streaming neural audio system evaluated block-wise: block-wise scores can hide a total streaming failure, because block-wise evaluation resets state at every block and thus re-creates the zero-padding regime the model was trained in.

## Related Concepts

- [[concepts/music-source-separation|Music Source Separation]]
- [[concepts/tfc-tdf-unet|TFC-TDF U-Net]]
- [[concepts/gated-recurrent-unit|Gated Recurrent Unit]]

## Related Sources

- [[sources/li-2026-realtime-music-separation-dsp|Li, Liu, Malsky & Yi 2026: Real-Time Music Source Separation on a Low-Power Audio DSP]]
