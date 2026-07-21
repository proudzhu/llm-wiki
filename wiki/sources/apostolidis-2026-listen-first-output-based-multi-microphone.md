---
type: source
created: 2026-07-21
updated: 2026-07-21
sources:
  - raw/papers/apostolidis-2026-listen-first-output-based-multi-microphone/full-text.md
  - https://arxiv.org/abs/2607.12529
  - zotero://select/items/0_HFEKLBV8
tags:
  - beamforming
  - multi-channel-speech-enhancement
  - hearing-aid
  - output-based-processing
  - voice-activity-detection
  - speech-intelligibility
---

# Apostolidis, Feldt, Tan, Østergaard & Jensen 2026: Listen first — output-based multi-microphone speech enhancement

**Authors**: [[entities/panos-apostolidis|Panos Apostolidis]], [[entities/svend-feldt|Svend Feldt]], [[entities/zheng-hua-tan|Zheng-Hua Tan]], [[entities/jan-ostergaard|Jan Østergaard]], [[entities/jesper-jensen|Jesper Jensen]]
**Type**: arXiv Preprint
**arXiv**: [2607.12529](https://arxiv.org/abs/2607.12529)
**DOI**: [10.48550/arXiv.2607.12529](https://doi.org/10.48550/arXiv.2607.12529)
**Date**: 2026-07-14
**Zotero**: [HFEKLBV8](zotero://select/items/0_HFEKLBV8)

## Summary

Proposes a novel [[concepts/output-based-speech-enhancement|output-based paradigm]] for hearing-aid multi-microphone speech enhancement in which the system is configured by evaluating the speech-intelligibility quality of its *output*, rather than by extracting acoustic features (e.g., VAD cues) from its noisy *input*. To demonstrate the paradigm, the authors build a system that selects among a discrete dictionary of candidate [[concepts/mpdr-beamformer|MPDR beamformers]] the one whose output maximizes a [[concepts/glimpse-proportion|Glimpse Proportion (GP)]] score computed from a neural-VAD-estimated audibility map. Despite MPDR's notorious sensitivity to steering errors, the output-based wrapper makes it robust, and the system consistently outperforms a conventional input-based [[concepts/mvdr-beamformer|MVDR]] baseline — especially at low input SNR and even under RTF mismatch (non-individualized or coarse dictionaries).

## Problem Formulation

Conventional hearing-aid SE pipelines are *input-based*: a VAD operating directly on noisy microphone signals produces masks used to estimate target/noise spatial covariance matrices and the [[concepts/relative-transfer-function|RTF]], which then parameterize a [[concepts/mvdr-beamformer|MVDR]] beamformer (Eq. 6). Because VAD decisions degrade precisely in challenging acoustic scenes (low SNR, reverberation, interferers), the downstream statistics become unreliable — exactly when HA users need the most support.

The noisy microphone signal is modeled in the STFT domain as:

$$\mathbf{X}(k,l) \approx S(k,l)\,\mathbf{H}(k) + \mathbf{V}(k,l)$$

where $\mathbf{H}(k)$ is the $M$-dimensional Head-Related Transfer Function (HRTF) vector and $\mathbf{V}(k,l)$ is the noise vector.

The paper instead asks: can we select the *configuration* of an SE system (here, the steering direction of an MPDR beamformer) by evaluating the SI quality of each candidate's *output*, rather than by estimating input statistics?

## Methodology

### Output-based MPDR Beamforming

An MPDR beamformer (Eq. 2) with weights

$$\mathbf{W}_{\text{MPDR}}(k,l) = \frac{\mathbf{C}_{\mathbf{X}}^{-1}(k,l)\,\mathbf{d}_{\theta_i}(k)}{\mathbf{d}_{\theta_i}^{H}(k)\,\mathbf{C}_{\mathbf{X}}^{-1}(k,l)\,\mathbf{d}_{\theta_i}(k)}$$

is constructed for each candidate direction $\theta_i$ from a pre-enrolled dictionary $\mathbf{d}_\theta(k) = \{\mathbf{d}_{\theta_1}(k), \ldots, \mathbf{d}_{\theta_N}(k)\}$ of time-invariant RTF vectors (Eq. 3). Crucially, MPDR uses the noisy covariance $\mathbf{C}_{\mathbf{X}}$ — not noise-only $\mathbf{C}_{\mathbf{V}}$ — so no VAD-based noise statistics are needed to *construct* a candidate. This makes MPDR a natural fit for output-based selection.

### Output-based Speech Intelligibility Prediction

A neural VAD (CRN, see §4.2) estimates a per-time-frequency **audibility** map $\widehat{\mathrm{AUD}}(k,l) \in [0,1]$ adopted from the Speech Intelligibility Index (SII): the T-F SNR at the reference microphone (Eq. 4) is clipped to $[-15, 15]$ dB and linearly mapped to $[0, 1]$.

For each candidate MPDR beamformer, the VAD is run on its *output* signal, producing $\widehat{\mathrm{AUD}}(k,l)$. The [[concepts/glimpse-proportion|Glimpse Proportion]] (Eq. 5, Cooke 2006) is then computed:

$$\mathrm{GP} = \frac{1}{KL}\sum_k \sum_l U\!\left(\widehat{\mathrm{AUD}}(k,l) - \gamma_{\mathrm{GP}}\right)$$

where $U(\cdot)$ is the unit step. The candidate with the highest GP is selected for the current segment. GP is preferred over SNR/SQ measures because it emphasizes speech-dominant T-F regions and is more sensitive to the correct target direction.

### Input-based MVDR Baseline

For fair comparison, the same neural VAD drives a conventional input-based MVDR (Eq. 6):

$$\mathbf{W}_{\text{MVDR}}(k,l) = \frac{\mathbf{C}_{\mathbf{V}}^{-1}(k,l)\,\mathbf{d}(k)}{\mathbf{d}^{H}(k)\,\mathbf{C}_{\mathbf{V}}^{-1}(k,l)\,\mathbf{d}(k)}$$

Ideal binary masks (Eq. 7) are formed from the audibility map with speech / noise thresholds $\gamma_S, \gamma_V$ and used to estimate $\mathbf{C}_{\mathbf{S}}$ (Eq. 8) and $\mathbf{C}_{\mathbf{V}}$ via the principal-eigenvector RTF method. This ensures the comparison isolates the input vs. output *structural* distinction rather than VAD architecture differences.

### Neural VAD (CRN) Architecture

A [[concepts/convolutional-recurrent-network|CRN]] with 2.9M parameters is tuned via Bayesian optimization. It takes stacked real/imaginary STFT parts as input and outputs $\widehat{\mathrm{AUD}}(k,l)$ via a sigmoid. Five causal convolutional encoder-decoder layers with kernel $(3,2)$, ELU activations, batchnorm, and frequency-stride 2 surround four stacked LSTM layers. Trained with MSE on 1 s segments (Eq. 9) for 300 epochs (Adam, lr 0.016, batch size 32).

![[raw/papers/apostolidis-2026-listen-first-output-based-multi-microphone/figures/9279ffbceb75d11f03cb7685f8f36fcd00b5a7883e7b8d964f2a045f10ac2994.jpg|Figure 1]]

*Figure 1: Block diagrams of (a) conventional input-based SE and (b) the proposed output-based paradigm. The output-based loop evaluates candidate outputs to select the system configuration.*

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Array | Bilateral HA, 2 mics per HA, 4 channels total; left-front = reference |
| Source signals | Librispeech (target), 10-class ESC-50 subset (point noise) |
| HRIRs | OTIMP dataset, 46 individuals, 48 azimuths (7.5°), 0° elevation, late reverb removed |
| Noise scene | 1–3 point sources on 1.9 m ring + isotropic speech-shaped noise (SSN) |
| SNR sampling | Input SNR uniform in $[-15, +15]$ dB |
| Sample rate / STFT | 16 kHz, 128-pt FFT, 8 ms Hann, 4 ms hop |
| VAD training | 1 hour, 90/10 split, 1 s segments, 2.9M params, MSE loss, 300 epochs |
| Beamformer eval | 2 hours, 50/50 validation/test split |
| Segment duration $D_T$ | $\{0.2, 0.4, 0.6, 0.8, 1.0\}$ s (weights fixed per segment; non-causal) |
| Hyperparameters $\gamma_S, \gamma_V, \gamma_{\mathrm{GP}}$ | Tuned on validation set to maximize output SNR |
| RTF dictionary conditions | MPDR$_F$ (matched, 7.5° resolution), MPDR$_U$ (15° spaced, target between entries), MPDR$_S$ (non-individualized HATS RTFs) |
| Baselines | Input-based MVDR (same VAD), Oracle MVDR (clean stats), Oracle MPDR (true RTF) |
| Metrics | $\Delta$SNR, $\Delta$ESTOI, $\Delta$PESQ vs. unprocessed; Wilcoxon signed-rank $p < 0.05$ |

## Results

### Output-based MPDR vs. input-based MVDR

At $\mathrm{SNR}_i = -5$ dB (Fig. 2), the output-based MPDR consistently and significantly outperforms the input-based MVDR across all metrics and all segment durations $D_T$. For $D_T > 0.5$ s, the proposed system approaches the *oracle* MPDR upper bound, indicating that GP-based selection reliably identifies the optimal candidate even in challenging conditions. The input-based MVDR struggles because VAD decisions on noisy inputs corrupt the noise covariance estimate.

Across input SNRs from $-10$ to $+5$ dB at $D_T = 0.6$ s (Fig. 3), the output-based system retains its advantage for SNR and ESTOI at all SNRs; differences are statistically significant except for PESQ at $\mathrm{SNR}_i \leq -8$ dB. The advantage *grows* at low SNR — exactly where input-based VAD fails.

### Robustness to RTF mismatch (Table 1, $\mathrm{SNR}_i = -5$ dB)

| $D_T$ | ΔSNR: Input MVDR | MPDR$_U$ | MPDR$_S$ | MPDR$_F$ | ΔESTOI: Input MVDR | MPDR$_U$ | MPDR$_S$ | MPDR$_F$ |
|-------|------------------|----------|----------|----------|---------------------|----------|----------|----------|
| 0.2   | 6.33  | 7.40  | 7.65  | **9.21**  | −0.09 | 0.02 | 0.02 | **0.14** |
| 0.4   | 6.42  | 7.69  | 7.73  | **10.19** | −0.04 | 0.11 | 0.10 | **0.23** |
| 0.6   | 6.69  | 7.88  | 7.87  | **10.64** | −0.02 | 0.15 | 0.14 | **0.26** |
| 0.8   | 6.78  | 7.95  | 7.89  | **10.88** | 0.00  | 0.17 | 0.15 | **0.28** |
| 1.0   | 6.78  | 7.97  | 7.90  | **11.00** | 0.00  | 0.17 | 0.16 | **0.28** |

Bold-faced MPDR$_F$ values indicate significant improvement over the MVDR baseline (Wilcoxon, $p = 0.05$). Even under the two mismatch conditions (MPDR$_U$ coarse dictionary, MPDR$_S$ non-individualized HATS), the output-based system still significantly outperforms input-based MVDR in SNR and ESTOI for all $D_T$.

## Key Contributions

1. **Output-based processing paradigm** — a general framework in which a sound-processing system is configured by evaluating SI/SQ of its *output* rather than extracting features from its noisy input. Applicable beyond beamforming.
2. **MPDR rehabilitation via output-based selection** — shows that MPDR, normally avoided for its steering-error sensitivity, becomes effective inside an output-based wrapper because GP-based selection searches over a candidate set rather than committing to a single (potentially mismatched) steering vector.
3. **GP-based output selection criterion** — adopts the Glimpse Proportion (Cooke 2006) as an SI-inspired measure computed from neural-VAD-estimated audibility maps of candidate outputs; emphasizes speech-dominant T-F regions and is more direction-selective than SNR/SQ measures.
4. **Robustness under RTF mismatch** — significant SNR/ESTOI gains persist when the RTF dictionary is coarse (15° spacing) or non-individualized (HATS), demonstrating practical deployability.
5. **Fair architectural comparison** — uses the same neural VAD in both the proposed and baseline systems, isolating the structural input-vs-output distinction rather than conflating it with VAD-architecture differences.

## Related Concepts

- [[concepts/output-based-speech-enhancement|Output-based Speech Enhancement]]
- [[concepts/glimpse-proportion|Glimpse Proportion]]
- [[concepts/mpdr-beamformer|MPDR Beamformer]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/voice-activity-detection|Voice Activity Detection]]
- [[concepts/relative-transfer-function|Relative Transfer Function]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[concepts/ideal-binary-mask|Ideal Binary Mask]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Related Synthesis

- [[synthesis/adaptive-algorithm-tradeoffs|Adaptive Algorithm Trade-offs]]
