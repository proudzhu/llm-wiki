---
type: concept
created: 2026-05-23
updated: 2026-07-25
sources:
  - raw/papers/ostergaard-2026-own-voice-cancellation/full-text.md
  - raw/papers/huang-2026-lightweight-speech-enhancement-guided-target-speech-extraction/full-text.md
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

## Challenges

- **Permutation problem**: In blind separation, assigning outputs to sources is ambiguous
- **Geometry mismatch**: Spatial methods trained on fixed geometries degrade on unseen configurations
- **DOA errors**: Spatial selectivity trades off with robustness to target direction errors
- **Reverberation**: Room reflections complicate spatial cues and target identification
- **Real-time processing**: Low-latency requirements for hearing aids and hearables

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

- [[sources/li-2026-geometry-conditioned-ssanc|Li 2026: Geometry-Conditioned Spatially Selective Non-Linear Filter]]
- [[sources/zaidel-2026-linearly-constrained-deep-beamformer|Zaidel et al. 2026: Linearly Constrained Deep Beamformer]]
- [[sources/huang-2026-lightweight-speech-enhancement-guided-target-speech-extraction|Huang et al. 2026: Lightweight Speech Enhancement Guided TSE in Noisy Multi-Speaker Scenarios]]
