---
type: concept
created: 2026-09-15
updated: 2026-09-15
tags:
  - music-source-separation
  - source-separation
  - real-time-processing
---

# Music Source Separation

Music source separation (MSS) is the task of decomposing a mixed music recording into its constituent stems — conventionally vocals, drums, bass, and other — on MUSDB18(-HQ), the standard benchmark corpus. Unlike speech enhancement, MSS must produce four *correlated* outputs and a decoder that reconstructs every stem, making it harder at a given compute budget than speech-oriented separation.

## Real-Time and Embedded MSS

The strongest systems (Hybrid Demucs, band-split RNN/transformer models) are large and offline, consuming a whole track at once. The real-time regime is much sparser: HS-TasNet demixes at 23 ms latency, and RT-STT matches that latency with ~0.4 M parameters. Both separate *algorithmic latency* from *computational efficiency* and report per-frame processing time — but on i7-class CPUs and RTX-class GPUs, not the low-power audio DSPs that hearing aids, in-ear monitors, and live-sound processors actually run on.

[[sources/li-2026-realtime-music-separation-dsp|Li et al. 2026]] showed that no published real-time MSS system satisfies the two constraints of a commercial audio DSP (2 MB SRAM, 2.07 GMAC/s measured): weight memory rules out the 16–51 M parameter TasNet/X-UMX family by 8.0–25.5×, while per-frame compute rules out RT-STT, which needs 5.5× the available MAC rate. Parameter count predicts neither failure (see [[concepts/weight-reuse-factor|weight reuse factor]]). They then built the first MSS system demonstrated on such a device: a causal [[concepts/tfc-tdf-unet|TFC-TDF U-Net]] with a gated [[concepts/deep-filtering|deep-filter]] head, trained with [[concepts/continuous-context-training|continuous-context training]], reaching 4.70 dB cSDR on MUSDB18-HQ in 10.43 ms of an 11.6 ms frame deadline.

## Evaluation Caveats

MSS quality metrics are not uniform across papers: cSDR (median over 1 s windows, silent reference windows gated) is a plain energy ratio and differs from BSSEval-v4 by up to ±1.3 dB per stem with inconsistent sign, so cross-paper comparisons are indicative only. Weight memory comparisons should assume int8 (the most generous case for the baselines); the deployed model of Li et al. 2026 uses float32 weights.

## Related Concepts

- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/tfc-tdf-unet|TFC-TDF U-Net]]
- [[concepts/deep-filtering|Deep Filtering]]
- [[concepts/weight-reuse-factor|Weight Reuse Factor]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask]]

## Related Sources

- [[sources/li-2026-realtime-music-separation-dsp|Li, Liu, Malsky & Yi 2026: Real-Time Music Source Separation on a Low-Power Audio DSP]]
