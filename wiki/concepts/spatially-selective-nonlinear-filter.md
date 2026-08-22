---
type: concept
created: 2026-05-23
updated: 2026-08-22
sources:
  - raw/papers/tesch-2024-spatially-selective-nonlinear-filters/full-text.md
tags:
  - deep-learning
  - spatial-filtering
  - target-speaker-extraction
  - microphone-arrays
  - speech-separation
---

# Spatially Selective Non-Linear Filter

**Spatially Selective Non-Linear Filter (SSF)** is a deep-learning-based spatial filter for [[concepts/target-speaker-extraction|target speaker extraction]] and multi-channel speech separation that uses the target direction-of-arrival (DOA) as a steering cue. Proposed by Tesch & Gerkmann (ICASSP 2023 [26]; journal extension in IEEE/ACM TASLP 2024), the SSF employs a recurrent neural network (the [[concepts/joint-nonlinear-filtering|JNF]] or [[concepts/mcnet|McNet]] architecture) to estimate a complex-valued mask applied to a reference microphone signal, extracting the target speaker from a multi-channel mixture. Per-speaker recovery in a separation task is achieved by steering and running the SSF once per target direction.

## Signal Model

In the STFT domain, the multi-channel observed signal is:

$$\mathbf{Y}(f,t) = \mathbf{X}(f,t) + \mathbf{V}(f,t),$$

where $\mathbf{Y}(f,t) \in \mathbb{C}^M$ stacks signals from $M$ microphones, $\mathbf{X}(f,t)$ is the target speech, and $\mathbf{V}(f,t)$ is interference.

The SSF estimates a complex mask $\mathcal{M}(f,t)$ applied to the reference microphone:

$$\hat{X}_1(f,t) = \mathcal{M}(f,t) \, Y_1(f,t).$$

## Architecture

The SSF comprises two LSTM layers:

1. **Frequency-domain LSTM (F-LSTM)**: Encodes spatial and spectral information from $\mathbf{Y}(f,t)$ into high-dimensional features
2. **Time-domain LSTM (T-LSTM)**: Models temporal dependencies across time frames
3. **Linear output layer**: Produces the complex mask $\mathcal{M}(f,t)$

**DOA conditioning**: The target DOA $\theta$ is mapped to a 180-dimensional one-hot vector (2° resolution, 360° total) and projected via a linear layer to an embedding matching the F-LSTM cell-state size (256 units for JNF). This embedding **initialises the forward and backward cell states of the bidirectional F-LSTM**. Only the first F-LSTM is conditioned (preliminary experiments showed that conditioning the second T-LSTM as well does not help and slightly increases computational demand — consistent with the observation that spatial selectivity is mainly controlled by the F-LSTM [22]). This mechanism avoids a far-field steering-vector assumption (unlike Jenrungrot et al. [30], who time-align channels based on geometry), and was shown in [26] to outperform that competing method.

## Limitations

- **Geometry dependency**: Learned features are tied to the training array geometry
- **Mismatched geometry degradation**: Performance drops significantly when evaluated on different array configurations
- **No explicit geometry representation**: The network cannot adapt to unseen geometries without retraining

## Extensions

### Geometry-Conditioned SSF (GC-SSF)

The [[concepts/geometry-conditioned-ssf|GC-SSF]] addresses the geometry dependency by adding a [[concepts/film-layer|FiLM]]-based conditioning branch driven by [[concepts/doa-microphone-positional-encoding|DOA-MPE]] features. This enables a single model trained on random arrays to generalise across circular, ULA, and random geometries.

## Multi-Speaker Separation (Tesch & Gerkmann 2024)

The 2024 IEEE/ACM TASLP journal extension of [26] systematically compares the SSF against a [[concepts/direct-separation|Direct Separation (DS)]] baseline trained with utterance-wise permutation invariant training (PIT), using the same backbone architectures ([[concepts/joint-nonlinear-filtering|JNF]] and [[concepts/mcnet|McNet]]) to isolate the effect of explicit (SSF) vs. implicit (DS) spatial filtering. The SSF is run once per speaker to recover individual sources from a reverberant mixture.

**Key finding**: the SSF advantage over DS grows with the number of speakers.

| Speakers | JNF-DS ΔPOLQA | JNF-SSF ΔPOLQA | McNet-DS ΔPOLQA | McNet-SSF ΔPOLQA |
|:---------|:--------------|:---------------|:-----------------|:------------------|
| 2 | 1.20 | 1.41 | 1.82 | 1.85 |
| 3 | 0.87 | 1.30 | 1.40 | 1.76 |
| 5 | 0.53 | 0.96 | 0.87 | 1.43 |

A [[concepts/doa-informed-direct-separation|DoA-informed DS variant (iDS)]] that augments DS with the same DoA-conditioning mechanism (multi-hot for all speakers) does not close the gap — for 5 speakers, iDS still trails SSF by 0.47 ΔPOLQA, demonstrating that the SSF's advantage is structural (per-speaker explicit filtering) rather than a side effect of DoA supervision.

**Robustness and generalization findings:**

- **DoA-error robustness** is trainable: training with up to 4° DoA noise flattens the sensitivity curve for ≤4° evaluation errors at the cost of slightly lower peak performance; there is a tunable sensitivity/robustness trade-off.
- **Microphone-array perturbations**: SSF tolerates 1 mm placement noise but degrades sharply beyond; DS is largely insensitive but performs far below the perturbed SSF peak for 3+ speakers, which the authors interpret as DS under-exploiting spatial information rather than being genuinely robust.
- **Far-field/near-field**: training with near-field examples (0.3–1.0 m) improves close-source performance at the cost of far-source performance — capacity is reallocated to modelling near-field spatial structure.
- **Sources with similar DoA**: when two speakers are collocated within ±20°, the SSF cleanly extracts the third (non-collocated) speaker (per-speaker output **decoupling**); the DS approach produces low-quality outputs for all speakers (coupled failure).
- **Unseen noise**: SSF generalises far better than DS to an unseen music-noise source — DS trained on 2-speaker mixtures collapses (ΔPOLQA 0.65), and DS trained on 3-speaker mixtures still trails SSF by 0.15 ΔPOLQA while requiring noise-source DoA estimates.

**Blind deployment strategies** (without oracle DoA):

- [[concepts/search-based-doa-estimation|Search-based]]: evaluate the SSF on a candidate-direction grid, peak-find on filtered-output energy. Computationally expensive (≈90 forward passes at 4° resolution) but exposes the SSF's spatial selectivity.
- [[concepts/dnn-based-doa-classifier|DNN-based classifier]]: a compact F-LSTM + 2 feed-forward layers trained for 100 epochs with binary cross-entropy on 2-speaker mixtures; both **more efficient** (one forward pass) and **more accurate** (mean angular error 1.06° vs. 1.57° for 2 speakers, 2.13° vs. 3.54° for 5 speakers). McNet-SSF steered with DNN-classifier DoAs matches oracle-DoA separation performance.

## Comparison with Related Methods

| Method | Spatial cue | Adaptation | Geometry handling |
|:-------|:------------|:-----------|:------------------|
| [[concepts/beamforming\|Beamforming]] | Array geometry | Often online | Explicit |
| SSF | Target DOA | None | Tied to training |
| [[concepts/geometry-conditioned-ssf\|GC-SSF]] | Target DOA + geometry | None | Explicit conditioning |
| [[concepts/spatially-selective-anc\|SSANC]] | Target direction (ReIRs) | Typically offline | Explicit (control-theoretic) |

## Related Concepts

- [[concepts/joint-nonlinear-filtering|Joint Nonlinear Filtering (JNF / FT-JNF)]]
- [[concepts/mcnet|McNet (Multi-Cue Network)]]
- [[concepts/direct-separation|Direct Separation (DS) with PIT]]
- [[concepts/doa-informed-direct-separation|DoA-Informed Direct Separation (iDS)]]
- [[concepts/search-based-doa-estimation|Search-based DoA Estimation]]
- [[concepts/dnn-based-doa-classifier|DNN-based DoA Classifier]]
- [[concepts/geometry-conditioned-ssf|Geometry-Conditioned SSF (GC-SSF)]]
- [[concepts/doa-microphone-positional-encoding|DOA-Microphone Positional Encoding (DOA-MPE)]]
- [[concepts/film-layer|FiLM Layer]]
- [[concepts/target-speaker-extraction|Target Speaker Extraction]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/spatially-selective-anc|Spatially Selective ANC]]

## Related Sources

- [[sources/tesch-2024-spatially-selective-nonlinear-filters|Tesch & Gerkmann 2024: Multi-channel Speech Separation Using Spatially Selective Deep Non-linear Filters]]
- [[sources/li-2026-geometry-conditioned-ssanc|Li 2026: Geometry-Conditioned Spatially Selective Non-Linear Filter]]
