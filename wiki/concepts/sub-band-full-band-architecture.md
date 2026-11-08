---
type: concept
created: 2026-11-08
updated: 2026-11-08
sources:
  - raw/papers/kuang-2025-low-complexity-bc-speech-enhancement/full-text.md
  - raw/papers/wang-2025-multi-modal-deep-filtering-bc/full-text.md
tags:
  - speech-enhancement
  - bone-conduction
  - lightweight-network
  - deep-filtering
  - erb-scale
  - architecture
---

# Sub-Band and Full-Band Architecture

A **sub-band and full-band architecture** is a two-step speech enhancement design that separates spectral processing by granularity: a cheap **coarse stage** operates on sub-band (band-compressed) features to estimate sub-band gains correcting the spectral envelope, and a **fine stage** operates on full-band features to estimate [[concepts/deep-filtering|deep-filtering]] (or masking) coefficients that suppress residual noise at full spectral resolution. It was proposed by Kuang, Yang, Wang & Yang (Applied Acoustics 2025) for low-complexity bone-conduction-aided speech enhancement.

## Motivation

Band-compression methods ([[concepts/erb-scale|ERB]] band gains in PercepNet/DeepFilterNet, band merging in [[concepts/gtcrn|GTCRN]]) are computationally cheap but merge multiple high-frequency bins into a single sub-band — a sub-band gain cannot suppress narrowband noise *within* a band, leaving residual noise concentrated at high frequencies. Full-resolution neural masks avoid this but are expensive. The two-step design assigns each granularity the task it is good at:

1. **Coarse**: $B = 32$ ERB sub-band gains $\mathbf{g}(t)$, interpolated to $F$ bins via matrix $\mathbf{W}$, enhance the spectral envelope — $\hat{\mathbf{y}}(t) = \mathbf{W}\mathbf{g}(t) \otimes \mathbf{y}_{AC}(t)$ (~2.5 MMACs/s).
2. **Fine**: $N$-order complex deep-filtering coefficients per TF bin suppress residual noise — $\hat{S}(t,f) = \sum_{i=1}^{N} C(t,f,i) \hat{Y}(t-i+1,f)$.

## Architecture

The backbone uses **two separate encoder-decoder sets**, one per granularity, sharing a grouped-sConformer bottleneck (one shared block + two parallel blocks):

- **Small ERB set**: three-conv-block encoders $\mathcal{E}_{erb1}$ (fused AC+BC ERB energies) and $\mathcal{E}_{erb2}$ (BC-only ERB energies), fused in the embedding space by [[concepts/iterative-attentional-feature-fusion|iAFF]], decoded by $\mathcal{D}_{erb}$ to the 32 gains, with [[concepts/attention-gate|AG]] skip-connections.
- **Large spectral set**: five-conv-block encoder $\mathcal{E}_{spec}$ (fused full-band AC+BC complex spectra) and decoder $\mathcal{D}_{spec}$ (depthwise separable convolutions, PWConv skips) producing $2N$ output channels (real/imaginary of the deep-filtering coefficients).

This is the architectural inversion of GTCRN-family band merging: rather than one encoder over a compressed spectrum, two encoders over *differently-compressed* views of the same spectrum, each with its own output granularity.

## Empirical Findings (A4BS, 109 speakers, SNR ∈ [−15, 5] dB)

| Variant | MACs (M) | wb-PESQ (low/mid/high SNR) | eSTOI (%) |
|---------|---------:|---|---|
| Full model | 40.3 | 2.102 / 2.396 / 2.747 | 74.82 / 79.84 / 84.61 |
| w/o deep filtering | 24.9 | 1.126 / 1.219 / 1.420 | 57.13 / 67.16 / 76.91 |
| w/o ERB gain | 37.8 | 1.809 / 2.061 / 2.359 | 73.10 / 78.45 / 83.48 |
| GTCRN-style band merging | 44.3 | 1.969 / 2.251 / 2.588 | 72.80 / 78.20 / 83.29 |

- Deep filtering is the dominant contributor; the ERB-gain stage adds ~2.5 MMACs for a significant additional gain — the cascade is what balances quality and complexity (best wb-PESQ/eSTOI among GTCRN, DeepFilterNet, DC-CRN, DenGCAN at the lowest MACs).
- Replacing the two-set design with GTCRN's high-frequency-only band merge at *comparable complexity* loses 0.146 average wb-PESQ and 1.64% eSTOI — the granularity separation, not capacity, drives the advantage.
- ERB gains alone suppress broadband noise but under-suppress harmonic noise (siren, ringing) due to band resolution; deep filtering removes the residual.
- Deep filtering beats a full-band cRM (N=1) on all metrics at slightly higher complexity.

## Frequency-Range Split vs. Granularity Split (Wang et al. 2025)

A coarser cousin of this architecture appears in [[sources/wang-2025-multi-modal-deep-filtering-bc|Wang, Kuang, Li, Yang, Bai & Liu 2025]]'s **MDFNet**, from the same research group. Instead of splitting by *granularity* (32 ERB bands vs. full band, both covering the whole spectrum), MDFNet splits by *frequency range*:

- **High band** — ERB-band gains applied to the **noisy AC spectrum only**, since BC has essentially no high-frequency content to contribute.
- **Low band** — [[concepts/multi-modal-deep-filtering|multi-modal deep filtering]] at full resolution over both AC and BC complex spectra, where the BC structure is intact.

So the coarse stage covers the range where BC is useless and the fine stage covers the range where BC is informative — the two design axes are orthogonal but motivated by the same physical asymmetry of bone conduction. MDFNet is a single shared encoder with two offline decoders (ERB-gain and deep-filtering) rather than the two encoder-decoder sets above, and uses frequency-only depthwise convolutions ($1\times3$ depthwise + $1\times1$ pointwise, 64 channels).

Two caveats on comparability: MDFNet reports no parameter count, MACs, or RTF even though it is likewise motivated by embedded deployment; and its numeric band split and DF order are unstated. Its results are on ABCS (PESQ 3.21 / STOI 0.79 / CER 24.8%) rather than A4BS, so they cannot be placed directly against the table above.

## Relation to Other Dual-Granularity Designs

| Design | Granularity split | Mechanism |
|--------|-------------------|-----------|
| **Sub-band + full-band (this)** | Full-range ERB bands vs. full-band DF | Two encoder-decoder sets, sequential gain→DF application |
| [[concepts/cofi-lite\|CoFi-Lite]] (Yang et al. 2026) | Full-band envelope (×16) vs. low-freq detail (<2 kHz, ×2) | Two parallel paths, both predict IRMs, coarse mask full-band then fine mask low-freq |
| GTCRN band merging | Low (uncompressed) vs. high (ERB-compressed) | Single path over merged spectrum |
| DeepFilterNet (Schröter et al. 2022) | ERB gains + full-band DF, one shared encoder | Sequential ERB gain then DF, single backbone |

| **Frequency-range split (MDFNet, Wang 2025)** | Low band (full-resolution DF over AC+BC) vs. high band (ERB gains on AC only) | Single encoder + two offline decoders; split frequency unstated |

CoFi-Lite and this architecture both split coarse/fine duties for lightweight monaural/bone-air SE, but CoFi-Lite splits by *frequency range* (envelope vs. low-freq detail), while Kuang et al. split by *spectral granularity* (32-band envelope vs. full-band deep filtering). DeepFilterNet is the closest prior — ERB gains followed by deep filtering from a single shared encoder — with Kuang et al. showing the two-set separation plus iAFF BC/AC fusion beats GTCRN-style merging at lower MACs in the bone-air setting.

## Related Concepts

- [[concepts/deep-filtering|Deep Filtering]]
- [[concepts/erb-scale|ERB Scale]]
- [[concepts/iterative-attentional-feature-fusion|Iterative Attentional Feature Fusion (iAFF)]]
- [[concepts/attention-gate|Attention Gate (AG)]]
- [[concepts/gtcrn|GTCRN]]
- [[concepts/cofi-lite|CoFi-Lite]]
- [[concepts/bcs-guided-speech-enhancement|BCS-Guided Speech Enhancement]]
- [[concepts/multi-modal-deep-filtering|Multi-Modal Deep Filtering]]

## Related Sources

- [[sources/kuang-2025-low-complexity-bc-speech-enhancement|Kuang, Yang, Wang & Yang 2025: Low-Complexity BC-Aided Speech Enhancement Leveraging Sub-Band and Full-Band Architecture]] — introduces the architecture
- [[sources/schroter-2022-deepfilternet|Schröter et al. 2022: DeepFilterNet]] — prior ERB-gain + deep-filtering cascade with a shared encoder
- [[sources/yang-2026-cofi-lite-ultra-lightweight-speech-enhancement|Yang et al. 2026: CoFi-Lite]] — parallel dual-granularity (frequency-range) design in monaural SE
- [[sources/wang-2025-multi-modal-deep-filtering-bc|Wang, Kuang, Li, Yang, Bai & Liu 2025: Multi-Modal Deep-Filtering-Based Speech Enhancement via BC Speech]] — frequency-range variant from the same group; no complexity figures reported
