---
type: concept
created: 2026-07-20
updated: 2026-07-20
sources:
  - raw/papers/chen-2023-ultra-dual-path-compression/full-text.md
tags:
  - speech-enhancement
  - model-compression
  - real-time
  - streaming
  - temporal-redundancy
---

# Frame-Skip Prediction

**Frame-Skip Prediction** (SkipPred) is a time-axis compression technique in which the heavy mask-estimation network is invoked only once every $r$ frames and the predicted mask is **copied** to the $r-1$ skipped frames in between. It exploits temporal redundancy in STFT features (50% overlap means adjacent frames share half their samples) to reduce the computational cost of streaming speech enhancement.

## Mechanism

At each $r$-frame interval, the compression module accepts the stacked current and history frames and uses a linear transformation to generate features with dimension $E \times T' \times F$, where $T' = T/r$. After the backbone processes this compressed feature, decompression copies the predicted mask for the current frame to the next $r-1$ frames.

## Performance Degradation

SkipPred alone produces significant quality degradation because the copied masks are **unmatched** to the actual spectral content of the skipped frames — speech can change substantially over $r \times \text{hop}$ milliseconds. At 8× compression (i.e., $r=8$), DT WB-PESQ drops from 2.78 (uncompressed) to 2.14, and ST-FE ERLE drops from 46.82 to 39.42.

## Recovery via Post-Processing Network

[[sources/chen-2023-ultra-dual-path-compression\|Chen et al. 2023]] show that a lightweight [[concepts/post-processing-network\|Post-Processing Network (PostNet)]] can recover most of the lost quality. With PostNet, 8× SkipPred recovers DT WB-PESQ from 2.14 to 2.47 — a gain of +0.33 at only 67K parameters and 15M MACs/s.

| Compression | SkipPred alone (DT WB-PESQ) | +PostNet (DT WB-PESQ) | Recovery |
|-------------|----------------------------:|----------------------:|---------:|
| 2× (r=2) | 2.68 | 2.75 | +0.07 |
| 4× (r=4) | 2.39 | 2.61 | +0.22 |
| 8× (r=8) | 2.14 | 2.47 | +0.33 |
| 16× (r=16) | 2.03 | 2.42 | +0.39 |
| 32× (r=32) | 2.02 | 2.40 | +0.38 |

The recovery grows with compression ratio because there is more lost quality to recover. At ratios ≥16×, PostNet recovery plateaus near +0.4 WB-PESQ.

## Comparison with Fixed-Rate Skipping

[[concepts/fixed-rate-skipping\|Fixed-Rate Skipping (FRS)]] in RT-Tango is conceptually similar but operates at the **mask-estimator invocation** level (skip the whole backbone) rather than at the **T-F feature** level. Key differences:

| Property | Frame-Skip Prediction (Chen 2023) | Fixed-Rate Skipping (RT-Tango 2026) |
|----------|-----------------------------------|-------------------------------------|
| What is skipped | T-F feature frames inside backbone | Entire backbone invocation |
| What is reused | Predicted mask copied to skipped frames | Last predicted mask reused |
| Refinement | [[concepts/post-processing-network\|PostNet]] (67K params, GRU + convs) | None — FRS commits to fixed schedule |
| Compressed feature | Used for both fullband and subband parts | N/A (backbone skipped entirely) |
| Application | Joint AEC + NS | Distributed binaural SE |

The two techniques are complementary in principle: FRS skips backbone invocation, while Frame-Skip Prediction compresses within the backbone.

## Relationship to HALO

[[sources/zhao-2026-halo-half-frame-rate-adaptive-operator\|HALO]] also halves the internal frame rate, but uses **dynamic convolution** (adaptive gating) instead of fixed copy-and-reuse. HALO's adaptive rate-reduction/restoration operators are more expressive than fixed copy, at the cost of more parameters. Ablations in HALO show that simple decimation + duplication is the worst HALO variant — adaptive gating is essential. This is consistent with Chen et al.'s finding that PostNet is needed to recover SkipPred degradation.

## Related Concepts

- [[concepts/post-processing-network\|Post-Processing Network]]
- [[concepts/dual-path-compression\|Dual-Path Compression]]
- [[concepts/dpt-fsnet\|DPT-FSNet]]
- [[concepts/fixed-rate-skipping\|Fixed-Rate Skipping]]

## Related Sources

- [[sources/chen-2023-ultra-dual-path-compression\|Chen et al. 2023: Ultra Dual-Path Compression]] — introduces SkipPred + PostNet as the time-compression axis
- [[sources/zhao-2026-halo-half-frame-rate-adaptive-operator\|Zhao et al. 2026: HALO]] — alternative adaptive frame-rate reduction
- [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement\|Benslimane et al. 2026: RT-Tango]] — Fixed-Rate Skipping (whole-backbone skip)
