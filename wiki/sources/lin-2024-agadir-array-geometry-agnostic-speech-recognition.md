---
type: source
created: 2026-05-24
updated: 2026-05-24
sources:
  - raw/papers/lin-2024-agadir-array-geometry-agnostic-speech-recognition/full-text.md
  - https://doi.org/10.48550/arXiv.2401.10411
  - zotero://select/items/0_8K2YN6P5
tags:
  - speech-recognition
  - beamforming
  - smart-glasses
  - array-geometry
  - icassp-2024
---

# Lin, Moritz, Huang, Xie, Sun, Fuegen & Seide 2024: AGADIR — Towards Array-Geometry Agnostic Directional Speech Recognition

**Authors**: [[entities/ju-lin|Ju Lin]], [[entities/niko-moritz|Niko Moritz]], [[entities/yiteng-huang|Yiteng Huang]], [[entities/ruiming-xie|Ruiming Xie]], [[entities/ming-sun|Ming Sun]], [[entities/christian-fuegen|Christian Fuegen]], [[entities/frank-seide|Frank Seide]]
**Affiliation**: Meta (Reality Labs?)
**Venue**: ICASSP 2024 (arXiv: 2401.10411)
**Type**: Conference Paper (preprint)
**DOI**: [10.48550/arXiv.2401.10411](https://doi.org/10.48550/arXiv.2401.10411)
**Zotero**: [8K2YN6P5](zotero://select/items/0_8K2YN6P5)

---

## Summary

AGADIR (Array-Geometry Agnostic Directional Speech Recognition) extends the authors' previous directional ASR system for smart glasses to be insensitive to limited variations in microphone-array geometry. By training a multi-channel RNN-T model with serialized output training (SOT) on data simulated from multiple similar array geometries, the model becomes largely agnostic to the specific geometry — it generalizes well to unseen geometries (deviations of a few mm to cm) and concurrently improves accuracy for seen geometries by 15–28% relative. The paper also introduces a novel Non-Linearly Constrained Minimum Variance (NLCMV) beamformer that incorporates white noise gain and null direction control.

## Problem Formulation

Directional ASR on smart glasses aims to transcribe a conversation partner at a distance of several feet while disambiguating between the wearer ("self"), the conversation partner ("other"), and unrelated bystanders. Multi-channel ASR processes $K+1$ beamformed signals (one per steering direction plus the mouth direction) to exploit spatial information. A practical challenge: during system development, microphone placements change across prototypes, requiring costly retraining.

The goal is to make the multi-channel ASR model insensitive to limited geometry variations (changes of mm to cm in microphone positions) without sacrificing accuracy.

## Methodology

### System Architecture

![[raw/papers/lin-2024-agadir-array-geometry-agnostic-speech-recognition/figures/x1.png|AGADIR system architecture]]

*Figure 1: Proposed array-geometry agnostic directional ASR architecture. Multi-channel audio is processed by $K+1$ fixed beamformers, then a convolutional front-end, followed by a streaming RNN-T with serialized output training.*

The system comprises:
1. **Beamforming stage**: $K+1$ fixed beamformers with predetermined coefficients — $K$ horizontal steering directions plus one towards the mouth
2. **Convolutional front-end**: Two Conv2D blocks with GLU activation, batch normalization, and stride-2 downsampling — keeps beam channels separate for a few layers before projection
3. **Streaming RNN-T**: Encoder (20 Emformer layers, 4 attention heads, 2048-dim FF), prediction network (1-layer 256-dim LSTM), and joiner; uses Serialized Output Training (SOT) for multi-talker disambiguation

### NLCMV Beamforming

The key beamforming contribution is Non-Linearly Constrained Minimum Variance (NLCMV), which extends MVDR by adding white noise gain control and null direction constraints:

$$\mathbf{h}^{H}(j\omega)\left[\mathbf{\Phi}_{dd}(j\omega) + \phi_{pp}(w)\sum_{n=1}^{N}\alpha_{p,n}\cdot\mathbf{g}_{n}(j\omega)\mathbf{g}_{n}^{H}(j\omega)\right]\mathbf{h}(j\omega)$$

subject to:
$$\mathbf{h}^{H}{(j\omega)}\mathbf{g}{(j\omega)} = 1 \quad \text{(linear equality)}$$
$$c(w) \triangleq \mathbf{h}^{H}({j\omega})\mathbf{\Psi}(j\omega)\mathbf{h}(j\omega) \leq 0 \quad \text{(nonlinear inequality: WNG constraint)}$$

where $\mathbf{\Psi}(j\omega) \triangleq \textbf{I} - \mathbf{g}(j\omega)\mathbf{g}^{H}(j\omega) \cdot M / [\sum_{m=1}^{M}|G_{m}(j\omega)|^2]$.

Compared to super-directive beamforming, NLCMV achieves a superior 10 dB gain at the designated look direction (e.g., backwards), and early ASR tests on real data showed ~0.7% absolute WER gain.

### Multi-Geometry Training

For geometry agnosticism, the model is trained on data simulated from **multiple** microphone-array configurations simultaneously. Two variants are compared:
- **Multi-geometry**: Uses a one-hot array-id embedding concatenated with the convolutional front-end output — supports switching beamformer parameters between known devices
- **Geometry-agnostic**: No array-id — trained on multiple geometries but remains adaptable to unseen devices

The training data is entirely simulated: 1M multi-channel RIRs generated via image-source method (ISM) using pyroomacoustics, with room sizes 5–10 m. Audio data is 14.6k hours of de-identified single-channel video data publicly shared by Facebook users.

## Experimental Setup

| Dataset | Size | Details |
|---------|------|---------|
| Training (simulated) | 14.6k hours | De-identified video data, 1M RIRs via ISM, SNR -5 to 30 dB |
| Simulated test | 3.7 hours | In-house video, different RIRs |
| Real test | Conversations | Project Aria glasses, partner at 4–6 ft, bilingual (EN/ES) |

**Devices**: Project Aria glasses (7 mics → 5-channel subsets Aria_A, Aria_B) and a composite prototype (5 configurations Comp_A–E). Configurations differ by moving microphones by several cm, including substituting the nose mic.

**Model config**: 80-dim log-Mel features, conv front-end (2× Conv2D, 5 channels, filter 2×5, stride 1×2), 20 Emformer layers, RNN-T with 256-dim LSTM prediction network, trained 8 epochs with Adam_sam, tri-stage LR scheduler (base LR 0.0005, 10k warmup).

**Metrics**: Speaker-unattributed WER (u/a) and speaker-attributed WER (self, other).

## Results

### Training on Multiple Geometries (Simulated Test)

| Model Type | Test Device | u/a WER | self WER | other WER |
|------------|-------------|---------|----------|-----------|
| Matching geometry (single) | Aria_A | 22.9 | 13.3 | 26.1 |
| Geometry-agnostic (multi) | Aria_A | — | ~28% relative improvement | — |
| Matching geometry (single) | Comp_B (clean) | 8.3 | — | — |
| Geometry-agnostic (multi) | Comp_B (clean) | 6.0 | — | — |

Training on multiple geometries outperforms single-geometry matching by up to 28% relative (8.3% → 6.0% WER for Comp_B clean). Excluding array-id information ("Geometry-agnostic") causes only 0.5% absolute WER increase.

### Unseen Geometries (Real Test)

| Test Device | Seen/Unseen | u/a WER | self WER | other WER |
|-------------|-------------|---------|----------|-----------|
| Aria_A | seen | 20.4 | 10.1 | 22.2 |
| Aria_B | unseen | 20.7 | 10.1 | 22.8 |

The geometry-agnostic model exhibits <0.6% absolute WER deviation between seen and unseen geometries. However, extreme changes (dropping a microphone, e.g., Comp_A 4-mic) cause WERs >25% — agnosticity fails.

## Key Contributions

1. **NLCMV beamforming**: Novel Non-Linearly Constrained Minimum Variance criterion incorporating white noise gain constraint and null direction control, achieving superior look-direction gain (~10 dB over super-directive)
2. **Geometry-agnostic training**: Demonstrating that multi-geometry training makes the ASR model largely agnostic to limited geometry variations (mm-to-cm changes), eliminating the need for per-prototype retraining
3. **Accuracy improvement**: Multi-geometry training improves WER by 15–28% relative over single-geometry matching baselines — likely due to increased robustness discouraging over-indexing to fine beam-pattern structure
4. **Convolutional front-end**: Two Conv2D+GLU blocks keeping beam channels separate for additional layers, improving speaker-attributed WER by 1.3% absolute over the previous linear projection approach

## Related Concepts

- [[concepts/beamforming|Beamforming]]
- [[concepts/nlcmv-beamforming|NLCMV Beamforming]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/roi-beamforming|Region-of-Interest Beamforming]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/target-speaker-extraction|Target Speaker Extraction]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]

## Related Synthesis

- [[synthesis/application-specific-anc|Application-Specific ANC]]
- [[synthesis/adaptive-algorithm-tradeoffs|Adaptive Algorithm Trade-offs]]
