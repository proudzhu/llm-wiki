---
type: concept
created: 2026-08-22
updated: 2026-08-22
sources:
  - raw/papers/tesch-2024-spatially-selective-nonlinear-filters/full-text.md
tags:
  - speech-separation
  - multi-channel
  - deep-learning
  - permutation-invariant-training
  - direction-of-arrival
---

# DoA-Informed Direct Separation (iDS)

**DoA-Informed Direct Separation (iDS)** is a variant of [[concepts/direct-separation|Direct Separation (DS)]] introduced by Tesch & Gerkmann (2024) to investigate whether the performance gap between [[concepts/spatially-selective-nonlinear-filter|SSF]] and DS can be explained by the explicit provisioning of speaker DoA information to the SSF rather than by the algorithmic distinction between explicit and implicit spatial filtering. iDS augments a PIT-trained DS network with the same one-hot DoA-conditioning mechanism used by the SSF, but presents the DoAs of all speakers simultaneously via a **multi-hot** encoding (rather than one-hot for a single target).

## Mechanism

- Network backbone: same as DS and SSF — JNF or [[concepts/mcnet|McNet]].
- Conditioning target: the first F-LSTM, identical to SSF (initial cell-state injection from a linear-projected DoA encoding).
- DoA encoding: **multi-hot** vector indicating the angular bins occupied by every speaker in the mixture (vs. SSF's one-hot for a single target).
- Output dimension: $P$ masks, like DS.
- Training: PIT loss (as in DS) on the multi-channel STFT input + multi-hot DoA conditioning.

## Purpose and Findings

iDS is designed to answer a confounding question for the SSF-vs-DS comparison: is the SSF advantage due to (i) the algorithmic distinction of explicit spatial filtering (one SSF evaluation per speaker) or (ii) the simple fact that the SSF receives helpful DoA supervision that DS does not? iDS controls for (ii) by giving DS the DoA information too.

Tesch & Gerkmann 2024 (Table II) report McNet-iDS (oracle DoA) vs. McNet-SSF (oracle DoA):

| Speakers | McNet-iDS ΔPOLQA | McNet-SSF ΔPOLQA | Gap |
|:---------|:-----------------|:------------------|:----|
| 2 | 1.82 | 1.85 | 0.03 |
| 3 | 1.61 | 1.76 | 0.15 |
| 5 | 0.96 | 1.43 | **0.47** |

- For 2 speakers, providing DoA information to DS closes the gap entirely (1.82 vs. 1.85).
- For 3 and especially 5 speakers, iDS still substantially trails SSF — the explicit spatial-filtering strategy of running the SSF once per speaker clearly exploits spatial information better than simply feeding DoA features to a PIT-trained DS network.
- In the "sources with similar DoA" generalization experiment (Sec. VII-B), iDS does **not** achieve the per-speaker output decoupling that the SSF exhibits — DS-style PIT training couples the outputs regardless of the DoA conditioning.
- In the unseen-noise experiment (Table V), iDS improves with oracle DoAs but still trails SSF by 0.82 ΔPOLQA on a 2-speaker + music-noise mixture.

## Implication

iDS confirms that the SSF's advantage over DS — especially as speaker count grows — is **not** a side effect of DoA supervision leaking into the SSF; it is an algorithmic consequence of the explicit, per-speaker spatial-filtering formulation. The decoupling of per-speaker outputs is the structural property that distinguishes SSF from iDS.

## Related Concepts

- [[concepts/direct-separation|Direct Separation (DS)]]
- [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Non-Linear Filter (SSF)]]
- [[concepts/mcnet|McNet]]
- [[concepts/joint-nonlinear-filtering|Joint Nonlinear Filtering (JNF)]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]

## Related Sources

- [[sources/tesch-2024-spatially-selective-nonlinear-filters|Tesch & Gerkmann 2024: Multi-channel Speech Separation Using Spatially Selective Deep Non-linear Filters]]
