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
  - lightweight-network
  - temporal-redundancy
---

# Post-Processing Network (PostNet)

The **Post-Processing Network (PostNet)** is a lightweight full-sequence refinement module introduced by [[sources/chen-2023-ultra-dual-path-compression\|Chen et al. 2023]] to recover quality lost from [[concepts/frame-skip-prediction\|frame-skip prediction]] in time-axis compression. PostNet has only **67K parameters and 15M MACs/s**, yet recovers >0.2 WB-PESQ across 4×–32× compression ratios.

## Motivation

Frame-skip prediction copies a mask predicted on one frame to the next $r-1$ skipped frames. Because speech spectra can change substantially over $r \times \text{hop}$ milliseconds, the copied masks are unmatched to the actual spectral content, producing significant quality degradation. PostNet addresses this by performing **full-sequence modeling** on the copied masks at low computational cost.

## Architecture

PostNet consists of four components:

1. **Feature compression module** — reduces input dimensionality (uses frequency compression with ratio 2 to save compute)
2. **1-layer Gated Recurrent Unit (GRU)** — performs full-sequence temporal modeling
3. **Feature decompression module** — restores dimensionality
4. **Output layer** — stacked $1 \times 1$ convolutions + linear transforms + sigmoid activation, predicting real-valued masks

The input feature has dimension $2 \times T \times F$, combining:
- The log power spectrum of the linear-AEC error signal $\hat{e}$
- The log power spectrum of the previous-stage output

PostNet uses log-power spectra (not complex features) and predicts real-valued masks (not complex masks), keeping the parameter and MAC count low.

## Hyperparameters

- Band count $B = 80$ (frequency compression target)
- Change of $B$ has limited effect on parameter size and computational cost because compression, decompression, and output layer occupy a non-negligible ratio of the module.

## Empirical Recovery

| Compression Ratio | SkipPred alone (DT WB-PESQ) | +PostNet (DT WB-PESQ) | Recovery |
|-------------------|----------------------------:|----------------------:|---------:|
| 4× | 2.39 | 2.61 | +0.22 |
| 8× | 2.14 | 2.47 | +0.33 |
| 16× | 2.03 | 2.42 | +0.39 |
| 32× | 2.02 | 2.40 | +0.38 |

PostNet is the single most cost-effective addition in the time-compression family — at 15M MACs/s, it adds <2% to the uncompressed model's 1822M MACs/s budget while recovering substantial quality.

## Known Limitations

- **ERLE degradation** — PostNet causes lower ST-FE ERLE compared to frequency-only compression. This propagates into [[concepts/dual-path-compression\|dual-path compression]] when the time path uses PostNet. The authors flag this as future work.
- **Single-layer GRU** — the limited modeling capacity of a 1-layer GRU constrains the recovery ceiling; deeper variants were not explored.

## Relationship to Other Refinement Approaches

| Refinement | Where | Cost | Mechanism |
|-----------|-------|------|-----------|
| PostNet (Chen 2023) | After frame-skip prediction | 67K / 15M MACs/s | 1-layer GRU + convs |
| HALO restoration (Zhao 2026) | Within backbone, after rate reduction | Larger | Dynamic-conv adaptive gating |
| Closed-loop FT (L3C-DeepMFC) | Training-time only | 0 inference cost | Simulated feedback mixing |

## Related Concepts

- [[concepts/frame-skip-prediction\|Frame-Skip Prediction]]
- [[concepts/dual-path-compression\|Dual-Path Compression]]
- [[concepts/dpt-fsnet\|DPT-FSNet]]

## Related Sources

- [[sources/chen-2023-ultra-dual-path-compression\|Chen et al. 2023: Ultra Dual-Path Compression]] — introduces PostNet as the time-compression refinement module
