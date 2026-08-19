---
type: concept
created: 2026-05-23
updated: 2026-08-19
sources:
  - raw/papers/ostergaard-2026-own-voice-cancellation/full-text.md
  - raw/papers/huang-2026-lightweight-speech-enhancement-guided-target-speech-extraction/full-text.md
  - raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/full-text.md
tags:
  - speech-processing
  - source-separation
  - deep-learning
  - spatial-filtering
---

# Target Speaker Extraction

**Target Speaker Extraction (TSE)** is the task of isolating a specific speaker's speech from a mixture containing multiple speakers and background noise. Unlike blind source separation, TSE uses auxiliary information (cues) to identify and extract the target speaker.

## Cues for Target Identification

| Cue type | Description | Examples |
|:---------|:------------|:---------|
| **Spatial** | Direction or location of target | DOA, beamforming, [[concepts/spatially-selective-nonlinear-filter\|SSF]] |
| **Enrolment** | Reference utterance from target | Speaker beam, speaker embeddings |
| **Visual** | Lip movements, face video | Audio-visual separation |
| **Textual** | Transcript or keywords | Speech recognition guided |

## Approaches

### Spatial Methods

- **[[concepts/beamforming|Beamforming]]**: Classical spatial filtering using array geometry
- **[[concepts/spatially-selective-nonlinear-filter|Spatially Selective Non-Linear Filter (SSF)]]**: Deep learning-based mask estimation conditioned on target DOA
- **[[concepts/geometry-conditioned-ssf|Geometry-Conditioned SSF (GC-SSF)]]**: SSF extended with explicit geometry conditioning for robustness across array configurations
- **[[concepts/spatially-selective-anc|Spatially Selective ANC]]**: Control-theoretic approach for hearables combining ANC with spatial discrimination

### Enrolment-Based Methods

Enrollment-based TSE uses a reference utterance from the target speaker to condition extraction. Three sub-families exist:

- **Speaker embedding / encoder-based** — obtain target speaker representations via pretrained embedding models (e.g., [[concepts/speaker-embedding|ECAPA-TDNN]]) or jointly-trained speaker encoders (e.g., SpEx, SpEx+). High accuracy but large model size and slow inference.
- **Embedding/encoder-free** — avoid explicit embeddings by directly modeling enrollment–mixture interactions, e.g., via iterative attention (SEF-Net), STFT-domain attention ([[concepts/cie-mdptnet|CIE-mDPTNet]]), or local/global context aggregation ([[concepts/sef-pnet|SEF-PNet]]). Increasingly SOTA-competitive at lower deployment cost.
- **Hybrid** — combine explicit embeddings with direct interaction for richer guidance.

A key failure mode in noisy multi-speaker scenarios is **noise contamination of the enrollment guidance**: when the context interaction is computed against the noisy mixture, noise leaks into the target-speaker representation and misleads the backbone. [[concepts/noise-agnostic-enrollment-guidance|Noise-agnostic enrollment guidance]] (LGTSE, Huang et al. 2026) addresses this by denoising the mixture before context interaction; [[concepts/distortion-aware-training|distortion-aware training]] (D-LGTSE) further exploits the denoiser's residual distortion as a training signal.

- **Speaker beam**: Uses enrolment utterances to extract speaker embeddings that condition the extraction network
- **Time-domain audio-visual separation**: Combines speaker embeddings with visual cues

### Audio-Visual Methods

- **AV-SepFormer**: Cross-attention between audio and visual features
- **Visual voice activity detection**: Lip-reading to identify active speaker segments

## Evaluation Metrics

| Metric | Description |
|:-------|:------------|
| **PESQ** | Perceptual Evaluation of Speech Quality (ITU-T P.862) |
| **SI-SDR** | Scale-Invariant Signal-to-Distortion Ratio |
| **SDR** | Signal-to-Distortion Ratio (BSS Eval) |
| **STOI** | Short-Time Objective Intelligibility |

## Unified Neural TSE Framework

Zmolikova et al. 2023 [[sources/zmolikova-2023-neural-target-speech-extraction-overview|(Zmolikova 2023)]] survey the field and propose a single general framework that subsumes audio-, visual-, and spatial-clue TSE under one description. The framework factors a TSE system into two modules:

1. **Clue encoder** — $\mathbf{E}_{s} = \mathrm{ClueEncoder}(\mathbf{C}_{s}; \theta^{\mathrm{Clue}})$. Maps a raw clue (enrollment utterance, face video, DOA, or multi-channel enrollment) to embeddings $\mathbf{E}_{s}$.
2. **Speech extraction module** — three sub-components:
   - **Mixture encoder**: $\mathbf{Z}_{y} = \mathrm{MixNet}(\mathrm{FE}(\mathbf{y}))$. A feature extractor (STFT magnitude or learnable 1-D conv) followed by a context network (RNN/CNN/attention).
   - **[[concepts/film-layer|Fusion layer]]**: $\mathbf{Z}_{s} = \mathrm{Fusion}(\mathbf{Z}_{y}, \mathbf{E}_{s})$. Conditions $\mathbf{Z}_{y}$ on the clue. Five widely used variants are surveyed (concatenation, addition, multiplication, FiLM, factorized).
   - **Target extractor**: $\hat{\mathbf{x}}_{s} = \mathrm{TgtExtractor}(\mathbf{Z}_{s}, \mathbf{y})$. Often a mask estimator (mask-based) or a [[concepts/beamforming|beamformer]] (multi-channel, distortionless).

The framework highlights that TSE internally solves **two sub-tasks**: (1) identifying the target speaker and (2) estimating that speaker's speech. Direct TSE consistently outperforms the cascade alternative (BSS then speaker-ID), especially in adverse conditions (WHAMR!), because the TSE model is directly optimized for the target and is given the speaker information upfront. Three principal clue types instantiate the same backbone:

- **Audio clue** $\mathbf{C}_{s}^{(a)}$ — pre-recorded enrollment; clue encoder is an i-vector, NN-based embedding (d-/x-vector), or jointly-trained encoder (see [[concepts/speaker-embedding|speaker embedding]]).
- **Visual clue** $\mathbf{C}_{s}^{(v)}$ — face/lip video; clue encoder uses face landmarks, FaceNet, lip-reading, or audio-visual sync embeddings. Best for same-gender mixtures.
- **Spatial clue** $\mathbf{C}_{s}^{(d)}$ — DOA or multi-channel enrollment; clue encoder produces [[concepts/angle-feature|angle features]] (TPD-vs-IPD cosine). Best when speakers are angularly separated.

Multi-clue combinations (audio-visual, audio-spatial, audio-visual-spatial) are implemented by concatenating, summing, or attention-weighting per-clue embeddings, and consistently outperform any single-clue system under adverse conditions (same-gender mixtures, corrupted clues, small angular separation).

## Extensions Beyond Waveform Extraction

The TSE framework naturally extends to:

- **[[concepts/target-speaker-asr|Target-Speaker ASR (TS-ASR)]]** — replaces the mask estimator with an ASR back-end (cascade, joint, or integrated variants).
- **[[concepts/target-speaker-vad|Target-Speaker VAD (TS-VAD)]]** — replaces the mask estimator with a binary activity classifier; the multi-target extension achieves state-of-the-art diarization (top of CHiME-6).
- **Other modalities** — semantic, EEG, language, or concept clues [59]–[61] for emerging applications.

## Challenges

- **Permutation problem**: In blind separation, assigning outputs to sources is ambiguous
- **Geometry mismatch**: Spatial methods trained on fixed geometries degrade on unseen configurations
- **DOA errors**: Spatial selectivity trades off with robustness to target direction errors
- **Reverberation**: Room reflections complicate spatial cues and target identification
- **Real-time processing**: Low-latency requirements for hearing aids and hearables
- **Inactive target speaker**: TSE systems are typically trained assuming the target is speaking; abstaining when the target is silent requires dedicated training [57].
- **Identification vs. extraction failure modes**: signal-level metrics (SI-SNR, SDR) do not separate identification failures from extraction failures; dedicated metrics are an open problem.

## Related Concepts

- [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Non-Linear Filter (SSF)]]
- [[concepts/geometry-conditioned-ssf|Geometry-Conditioned SSF (GC-SSF)]]
- [[concepts/doa-microphone-positional-encoding|DOA-Microphone Positional Encoding (DOA-MPE)]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/spatially-selective-anc|Spatially Selective ANC]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/noise-agnostic-enrollment-guidance|Noise-agnostic Enrollment Guidance]]
- [[concepts/distortion-aware-training|Distortion-aware Training]]
- [[concepts/sef-pnet|SEF-PNet]]
- [[concepts/cie-mdptnet|CIE-mDPTNet]]
- [[concepts/personalized-speech-enhancement|Personalized Speech Enhancement]]
- [[concepts/speaker-embedding|Speaker Embedding]]

## Related Sources

- [[sources/zmolikova-2023-neural-target-speech-extraction-overview|Zmolikova et al. 2023: Neural Target Speech Extraction: An Overview]]
- [[sources/li-2026-geometry-conditioned-ssanc|Li 2026: Geometry-Conditioned Spatially Selective Non-Linear Filter]]
- [[sources/zaidel-2026-linearly-constrained-deep-beamformer|Zaidel et al. 2026: Linearly Constrained Deep Beamformer]]
- [[sources/huang-2026-lightweight-speech-enhancement-guided-target-speech-extraction|Huang et al. 2026: Lightweight Speech Enhancement Guided TSE in Noisy Multi-Speaker Scenarios]]
