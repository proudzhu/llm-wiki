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
  - end-to-end
---

# Direct Separation (DS)

**Direct Separation (DS)** denotes the family of end-to-end regression-based multi-channel speech separation systems that estimate all speech sources directly from the mixture signal in a single forward pass, without an explicit spatial-filtering stage. The network is presented with the multi-channel input (and optionally directional features) and outputs as many source estimates as there are speakers in the mixture. The permutation ambiguity arising from the regression outputs is resolved by training with utterance-wise permutation invariant training (PIT) [39]. Throughout Tesch & Gerkmann 2024, DS serves as the contrastive baseline to the [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Filter (SSF)]] to isolate the effect of implicit vs. explicit spatial filtering.

## Signal & Training Formulation

Given the multi-channel STFT $Y^\ell(k, i)$, a DS network with parameters $\theta$ outputs $P$ masks $\{\mathcal{M}_p(k, i)\}_{p=1}^{P}$, applied to the reference channel to obtain per-speaker estimates:

$$\hat{S}_p(k, i) = Y^0(k, i) \cdot \mathcal{M}_p(k, i).$$

Training minimises an utterance-wise PIT loss:

$$L^{\text{PIT}} = \min_{\pi \in \Pi_P} \sum_{p=1}^{P} L\big(s_p, \hat{s}_{\pi(p)}\big),$$

where $\pi$ ranges over speaker permutations and $L$ is typically an $\ell_1$ loss in time and frequency domain (Tesch & Gerkmann 2024 use $L(s, \hat{s}) = \alpha \|s - \hat{s}\|_1 + \big\| |S| - |\hat{S}| \big\|_1$ with $\alpha = 10$).

## Properties and Trade-offs

- **Implicit spatial filtering**: spatial processing is learned from data rather than steered by an external cue. The degree to which the network learns powerful spatial processing can only be assessed indirectly.
- **Variable speaker count requires retraining**: a DS network's output dimension is fixed at training time, so a network trained for $P$ speakers cannot directly handle $P' \neq P$ without architectural changes.
- **Lower per-speaker parameter count than steered SSF**: for the same total parameter budget, DS spreads its parameters across all $P$ outputs, whereas an SSF evaluated $P$ times spends the full budget on each speaker.
- **Coupled failure modes**: per-speaker outputs are correlated through the shared encoder; the SSF decouples them.

## Empirical Comparison with SSF (Tesch & Gerkmann 2024)

Under matched architecture (JNF and [[concepts/mcnet|McNet]]) and matched parameters (Table III of the source), DS underperforms SSF increasingly with speaker count:

| Speakers | JNF-DS ΔPOLQA | JNF-SSF ΔPOLQA | McNet-DS ΔPOLQA | McNet-SSF ΔPOLQA |
|:---------|:--------------|:---------------|:----------------|:------------------|
| 2 | 1.20 | 1.41 | 1.82 | 1.85 |
| 3 | 0.87 | 1.30 | 1.40 | 1.76 |
| 5 | 0.53 | 0.96 | 0.87 | 1.43 |

Robustness and generalization experiments further show that:

- DS is largely insensitive to microphone-array perturbations, but Tesch & Gerkmann interpret this as **under-exploitation of spatial information** rather than genuine robustness — DS performs below the perturbed SSF peak for 3+ speakers.
- DS trained on 2-speaker mixtures collapses when an unseen music-noise source is added (ΔPOLQA 0.65, DNSMOS 2.28); DS trained on 3-speaker mixtures recovers much of the loss but still trails SSF (ΔPOLQA 1.51 vs. 1.66) while requiring DoA estimates for the noise source.
- In a "sources with similar DoA" scenario, DS produces low-quality outputs for all speakers when two are collocated, whereas the SSF decouples failure across speakers (third speaker still extracted cleanly).

The paper also introduces [[concepts/doa-informed-direct-separation|DoA-informed DS (iDS)]] to test whether simply providing DoA information to a PIT-trained DS network closes the SSF–DS gap; it does not.

## Related Concepts

- [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Non-Linear Filter (SSF)]]
- [[concepts/doa-informed-direct-separation|DoA-Informed Direct Separation (iDS)]]
- [[concepts/joint-nonlinear-filtering|Joint Nonlinear Filtering (JNF)]]
- [[concepts/mcnet|McNet]]
- [[concepts/target-speaker-extraction|Target Speaker Extraction]]
- [[concepts/beamforming|Beamforming]]

## Related Sources

- [[sources/tesch-2024-spatially-selective-nonlinear-filters|Tesch & Gerkmann 2024: Multi-channel Speech Separation Using Spatially Selective Deep Non-linear Filters]]
