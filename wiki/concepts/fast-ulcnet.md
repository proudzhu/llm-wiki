---
type: concept
created: 2026-07-19
updated: 2026-07-19
tags:
  - deep-learning
  - speech-enhancement
  - low-complexity
  - low-latency
  - recurrent-neural-network
---

# Fast-ULCNet

**Fast-ULCNet** is a fast and ultra-low-complexity single-channel speech enhancement architecture proposed by [[entities/nicolas-arrieta-larraza|Larraza]] & [[entities/niels-de-koeijer|de Koeijer]] (Bang & Olufsen, ICASSP 2026). It extends the [[concepts/ulcnet|ULCNet]] architecture of Shetu et al. (ICASSP 2024) by replacing the GRU recurrent layers with [[concepts/fastgrnn|FastGRNN]]-based layers — optionally with the [[concepts/comfi-fastgrnn|Comfi-FastGRNN]] drift-correction variant — to reduce both parameter count and inference latency on embedded targets while matching ULCNet's noise-suppression quality.

## Architecture

Fast-ULCNet preserves ULCNet's two-stage structure (magnitude-mask estimation + phase-refinement CNN with [[concepts/complex-ratio-mask|complex ratio masking]]). The only modification is the substitution of GRU layers with FastGRNN-based layers (with or without the complementary filter):

- **Stage 1**: Modified [[concepts/power-law-compression|power-law compression]] on real/imag STFT components → [[concepts/channel-wise-feature-reorientation|channel-wise feature reorientation]] (1.5 kHz resolution, 0.33 overlap) → 4 depthwise-separable conv layers (32 / 64 / 96 / 128 filters, max-pool ×2 on layers 2–4) → bidirectional Freq-FastGRNN (64 units + pointwise conv 64) → 2 subband temporal Fast-GRNN blocks (each 2 × 128-unit layers) → 2 FC layers (257 neurons each) → real-valued magnitude mask
- **Stage 2**: CNN on magnitude mask + noisy phase (two 2D conv layers, 32 filters, 1×3 kernel + pointwise conv with 2 output channels) → complex ratio mask → enhanced complex spectrogram

## Computational Profile

| Model | Params (M) | MACs (M) | RTF<sub>Pi3</sub> | RTF<sub>ARM</sub> |
|-------|-----------:|---------:|------------------:|------------------:|
| ULCNet | 0.685 | 2.057 | 0.976 | 0.927 |
| Fast-ULCNet | 0.338 | 1.691 | 0.657 | 0.604 |

- ~51% parameter reduction, ~18% MACs reduction
- ~33% RTF improvement on Raspberry Pi 3 B+, ~35% on Arm Cortex-A53

## Long-Sequence Behavior

Fast-ULCNet (plain FastGRNN) suffers from [[concepts/fastgrnn|FastGRNN]] state drift on long (>60 s) inference sequences, causing measurable quality decay (e.g., BAKMOS 3.95 → 3.62 on 90 s DNS test set). The [[concepts/comfi-fastgrnn|Comfi-FastGRNN]] variant fully recovers long-sequence performance — see the concept page for details.

## Related Concepts

- [[concepts/fastgrnn|FastGRNN]]
- [[concepts/comfi-fastgrnn|Comfi-FastGRNN]]
- [[concepts/ulcnet|ULCNet]]
- [[concepts/channel-wise-feature-reorientation|Channel-Wise Feature Reorientation]]
- [[concepts/power-law-compression|Power-Law Compression]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask]]
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/larraza-2026-fast-ulcnet-speech-enhancement|Larraza & de Koeijer 2026: Fast-ULCNet]]
