---
type: concept
created: 2026-08-22
updated: 2026-08-22
sources:
  - raw/papers/tesch-2024-spatially-selective-nonlinear-filters/full-text.md
tags:
  - neural-network
  - multi-channel
  - speech-enhancement
  - speech-separation
  - spatial-filtering
  - deep-learning
---

# McNet (Multi-Cue Network)

**McNet** (Multi-Cue Network) is a multi-channel speech enhancement/separation architecture proposed by Yang, Quan & Li (ICASSP 2023) [34] that extends the [[concepts/joint-nonlinear-filtering|JNF (FT-JNF)]] architecture of Tesch et al. [22], [27] with two additional single-channel (SC) LSTM layers and skip connections, aiming to better exploit single-channel spectral correlations in time and frequency after the multi-channel spatial processing. It is one of the two backbone architectures used by [[concepts/spatially-selective-nonlinear-filter|Tesch & Gerkmann's SSF (2024)]] and by the corresponding [[concepts/direct-separation|DS]] baseline.

## Architecture

McNet retains the JNF's two-layer core (F-LSTM for frequency/spatial processing, T-LSTM for temporal processing) and adds on top:

- **Two additional single-channel LSTM layers** (SC-LSTM-1, SC-LSTM-2) that focus on single-channel spectral correlations along time and frequency.
- **Feed-forward layers** appended after every LSTM layer (not just at the output).
- **Three skip connections**:
  1. Concatenate the noisy multi-channel input to the input of the T-LSTM.
  2. Concatenate the noisy magnitude of the reference channel to the input of SC-LSTM-1.
  3. Concatenate the noisy reference-channel magnitude to the input of SC-LSTM-2.

The first skip connection ensures the temporal layer sees both the F-LSTM-encoded features and the raw multi-channel observation; the second and third inject the raw single-channel spectral cue into the SC-LSTM layers that would otherwise operate only on the upstream-computed features.

## Steering as an SSF

Because the [[concepts/spatially-selective-nonlinear-filter|SSF]] conditioning mechanism targets only the first F-LSTM (initializing its bidirectional cell state from a one-hot-encoded DOA), it is architecture-agnostic: the same steering mechanism applies to both JNF and McNet, since both share the same F-LSTM front-end. This enables direct SSF-vs-DS comparisons on McNet without altering the architecture.

## Empirical Findings (Tesch & Gerkmann 2024)

On a simulated reverberant separation task (WSJ0, 3-mic circular array, 5 interfering speakers during training), McNet-SSF vs. McNet-DS under matched architecture:

| Speakers | Method | ΔPOLQA | ΔSI-SDR | DNSMOS |
|:---------|:-------|:-------|:--------|:--------|
| 2 | McNet-DS | 1.82 | 15.0 | 3.03 |
| 2 | McNet-SSF (oracle) | 1.85 | 14.7 | 3.13 |
| 3 | McNet-DS | 1.40 | 15.4 | 2.79 |
| 3 | McNet-SSF (oracle) | 1.76 | 16.3 | 3.04 |
| 5 | McNet-DS | 0.87 | 14.2 | 2.39 |
| 5 | McNet-SSF (oracle) | 1.43 | 17.3 | 2.84 |

- The SSF advantage grows from negligible at 2 speakers to 0.56 ΔPOLQA at 5 speakers.
- McNet strictly improves over JNF for both DS and SSF configurations.
- McNet-SSF search-based localization has slightly higher mean angular error (2.07° vs. JNF-SSF's 1.57° for 2 speakers), interpreted as JNF's stronger spatial selectivity producing sharper energy peaks.

## Related Concepts

- [[concepts/joint-nonlinear-filtering|Joint Nonlinear Filtering (JNF / FT-JNF)]]
- [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Non-Linear Filter (SSF)]]
- [[concepts/direct-separation|Direct Separation (DS)]]
- [[concepts/doa-informed-direct-separation|DoA-Informed Direct Separation (iDS)]]
- [[concepts/target-speaker-extraction|Target Speaker Extraction]]

## Related Sources

- [[sources/tesch-2024-spatially-selective-nonlinear-filters|Tesch & Gerkmann 2024: Multi-channel Speech Separation Using Spatially Selective Deep Non-linear Filters]]
