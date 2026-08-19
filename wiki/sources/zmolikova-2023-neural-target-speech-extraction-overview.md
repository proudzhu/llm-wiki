---
type: source
created: 2026-08-19
updated: 2026-08-19
sources:
  - raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/full-text.md
  - https://doi.org/10.1109/MSP.2023.3240008
  - zotero://select/items/X5JSCD25
tags:
  - survey
  - target-speaker-extraction
  - speech-processing
  - deep-learning
  - multi-modal
  - beamforming
  - speaker-recognition
---

# Zmolikova, Delcroix & Ochiai 2023: Neural Target Speech Extraction: An Overview

**Authors**: [[entities/katerina-zmolikova|Katerina Zmolikova]], [[entities/marc-delcroix|Marc Delcroix]], [[entities/tsubasa-ochiai|Tsubasa Ochiai]], [[entities/keisuke-kinoshita|Keisuke Kinoshita]], [[entities/jan-cernocky|Jan Černocký]], [[entities/dong-yu|Dong Yu]]
**Venue**: IEEE Signal Processing Magazine, Vol. 40, 2023, pp. 8–29
**Type**: Review / Overview Article
**DOI**: [10.1109/MSP.2023.3240008](https://doi.org/10.1109/MSP.2023.3240008)
**Zotero**: [X5JSCD25](zotero://select/items/X5JSCD25)

## Summary

This paper presents an in-depth overview of recent neural-based approaches to **target speech/speaker extraction (TSE)**, the task of isolating a target speaker's speech from a mixture of multiple speakers (with or without noise and reverberation) using auxiliary "clues" that identify the speaker in the mixture. The review unifies the field by introducing a single general neural TSE framework — clue encoder + mixture encoder + fusion layer + target extractor — and showing how audio, visual, and spatial clue variants instantiate it. It further covers extensions to ASR and diarization, identifies open challenges, and catalogs datasets and toolkits.

## Problem Formulation

### Speech Mixture Model

Recording a target speaker with a distant microphone in a multi-source acoustic scene yields a mixture:

$$
\mathbf{y}^{m} = \mathbf{x}_{s}^{m} + \underbrace{\sum_{k \neq s} \mathbf{x}_{k}^{m} + \mathbf{v}^{m}}_{\triangleq \mathbf{i}^{m}}, \tag{1}
$$

where $\mathbf{y}^{m}$ is the mixture, $\mathbf{x}_{s}^{m}$ is the target speech of speaker $s$, $\mathbf{x}_{k}^{m}$ are interfering speakers, $\mathbf{v}^{m}$ is noise, and $m$ indexes the microphone. The interference $\mathbf{i}^{m}$ aggregates everything to be suppressed; no explicit hypothesis is made about the number of interfering speakers.

### TSE Problem and Contrast with BSS / Noise Reduction

The TSE problem is to estimate the target speech given a clue $\mathbf{C}_{s}$:

$$
\hat{\mathbf{x}}_{s} = \mathrm{TSE}(\mathbf{y}, \mathbf{C}_{s}; \theta^{\mathrm{TSE}}). \tag{2}
$$

The clue $\mathbf{C}_{s}$ can take three principal forms:

- **Audio clue** $\mathbf{C}_{s}^{(a)}$ — pre-recorded enrollment utterance of the target speaker.
- **Visual clue** $\mathbf{C}_{s}^{(v)}$ — video of the speaker's face/lips.
- **Spatial clue** $\mathbf{C}_{s}^{(d)}$ — direction of arrival (DOA) or multi-channel enrollment.

![[raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/figures/dd602cf6eb93100406c3aafcb5bd8c55e1ea2a0c8d22b9333b66cbaa0096854a.jpg|Fig. 1: TSE problem and examples of clues]]
*Figure 1: TSE problem and examples of clues (audio, visual, spatial).*

The contrast with **blind source separation (BSS)** and **noise reduction** is fundamental:

| Task | Uses clue? | Output | Source count known? | Permutation ambiguity? |
|:-----|:-----------|:-------|:--------------------|:-----------------------|
| **TSE** | Yes | Target speech only | No | No |
| **BSS** | No | All $K$ sources | Yes (must be estimated) | Yes (global) |
| **Noise reduction** | No | Target speech (noise-only interference) | N/A | No |

![[raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/figures/1cccd7d4fcc7ebcb70bdd812c4cde4989d133a1fe37401b61108efaa3e9992c7.jpg|Fig. 2: Comparison of TSE with BSS and noise reduction]]
*Figure 2: Comparison of TSE with BSS and noise reduction.*

TSE shares with BSS the ability to handle interfering speakers; it shares with noise reduction the property of producing only the target speaker (no permutation ambiguity). However, TSE internally requires solving **two sub-tasks simultaneously**: (1) identify the target speaker in the mixture and (2) estimate that speaker's speech.

### Historical Context

The TSE lineage spans four eras:

1. **1980s — Fixed beamformers** (Flanagan et al. 1985): early spatial-clue TSE using a microphone array to enhance a fixed known direction.
2. **Mid-1990s to 2000s — BSS heritage**: independent component analysis (ICA), independent vector analysis (IVA), and independent vector extraction (IVE) [12]. Single-channel BSS via factorial HMM (F-HMM) and non-negative matrix factorization (NMF). F-HMM was the first to achieve super-human single-channel performance [17]; it also pioneered visual clue use [4].
3. **Mid-2010s — Deep neural networks**: deep clustering and [[concepts/permutation-invariant-training|permutation invariant training (PIT)]] enabled speaker-open single-channel BSS [20], [21]. Du et al. [22] proposed the first speaker-close neural TSE using audio clues.
4. **Late 2010s to present — Enrollment-conditioned neural TSE**: SpeakerBeam [10], VoiceFilter [11], and SpEx/SpEx+ [31] enable speaker-open TSE from a short enrollment utterance. Visual clue-based TSE [7], [8] and neural spatial-clue TSE [3], [24] follow the same template.

## Taxonomy

The review organizes TSE approaches along four dimensions (Table I):

1. **Type of clue**: audio, visual, spatial, or other (semantic, EEG, language, concept).
2. **Number of channels**: single-channel vs. multi-channel.
3. **Speaker-close vs. speaker-open**: requires training data of the target speaker vs. generalizes to unseen speakers given an enrollment.
4. **Generative vs. discriminative**: models the source distribution vs. directly estimates the mask/filter.

The scope of this overview is **neural, speaker-open, discriminative** approaches with audio, visual, and spatial clues (single- or multi-channel).

## Methodology

### General Neural TSE Framework

A neural TSE system consists of two main modules (Fig. 3):

**1. Clue encoder** — converts the raw clue $\mathbf{C}_{s}$ into embeddings $\mathbf{E}_{s}$:

$$
\mathbf{E}_{s} = \mathrm{ClueEncoder}(\mathbf{C}_{s}; \theta^{\mathrm{Clue}}). \tag{5}
$$

For audio clues, $\mathbf{E}_{s}^{(a)} \in \mathbb{R}^{D^{\mathrm{Emb}}}$ is a single speaker embedding; for visual clues, $\mathbf{E}_{s}^{(v)} \in \mathbb{R}^{D^{\mathrm{Emb}} \times N}$ is a per-frame sequence (e.g., lip embeddings).

**2. Speech extraction module** — three sub-components:

$$
\mathbf{Z}_{y} = \mathrm{MixEncoder}(\mathbf{y}; \theta^{\mathrm{Mix}}), \tag{6}
$$
$$
\mathbf{Z}_{s} = \mathrm{Fusion}(\mathbf{Z}_{y}, \mathbf{E}_{s}; \theta^{\mathrm{Fusion}}), \tag{7}
$$
$$
\hat{\mathbf{x}}_{s} = \mathrm{TgtExtractor}(\mathbf{Z}_{s}, \mathbf{y}; \theta^{\mathrm{TgtExtractor}}). \tag{8}
$$

The mixture encoder is itself decomposed into a feature extractor $\mathrm{FE}$ (STFT magnitude or a learnable 1-D conv operating on the raw waveform [23], [39]) and a context network $\mathrm{MixNet}$ (RNN/CNN/attention):

$$
\mathbf{Y} = \mathrm{FE}(\mathbf{y}; \theta^{\mathrm{FE}}), \quad \mathbf{Z}_{y} = \mathrm{MixNet}(\mathbf{Y}; \theta^{\mathrm{MixNet}}). \tag{9, 10}
$$

![[raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/figures/23b3e6e7d3b5ce036553e89975af29dad96279bef8aae4333299674aef219841.jpg|Fig. 3: General framework for neural TSE]]
*Figure 3: General framework for neural TSE.*

### Fusion Layers

The fusion layer (a.k.a. adaptation layer) is the key component that conditions the extraction on the clue. Table II of the paper surveys five widely used options:

| Fusion type | Equation | Extra parameters |
|:-----------|:---------|:-----------------|
| Concatenation | $\mathbf{Z}_{s} = [\mathbf{Z}_{y}, \mathbf{E}_{s}]$ | — |
| Addition | $\mathbf{Z}_{s} = \mathbf{Z}_{y} + \mathbf{L}\mathbf{E}_{s}$ | $\mathbf{L} \in \mathbb{R}^{D^{Z} \times D^{\mathrm{Emb}}}$ |
| Multiplication | $\mathbf{Z}_{s} = \mathbf{Z}_{y} \odot (\mathbf{L}\mathbf{E}_{s})$ | $\mathbf{L} \in \mathbb{R}^{D^{Z} \times D^{\mathrm{Emb}}}$ |
| **FiLM** | $\mathbf{Z}_{s} = \mathbf{Z}_{y} \odot (\mathbf{L}_{1}\mathbf{E}_{s}) + \mathbf{L}_{2}\mathbf{E}_{s}$ | $\mathbf{L}_{1}, \mathbf{L}_{2} \in \mathbb{R}^{D^{Z} \times D^{\mathrm{Emb}}}$ |
| Factorized layer | $\mathbf{Z}_{s} = \sum_{i=1}^{D^{\mathrm{Emb}}} \mathbf{L}_{i}\mathbf{Z}_{y} \mathrm{diag}(\mathbf{e}_{i})$ | $\mathbf{L}_{i} \in \mathbb{R}^{D^{Z} \times D^{Z}}$ |

Attention-based fusion [40] is another alternative; multi-clue fusion is discussed in Section VI.B. The review's own experiments report that the choice of fusion layer has "rather insignificant" impact on performance, with multiplication and [[concepts/film-layer|FiLM]] generally performing well. Best results come from a shallow mixture encoder with a deep extractor and a fusion layer placed low in the network.

### Target Extractor: Mask-Based Processing

The dominant target extractor estimates a time-frequency mask:

$$
\mathbf{M}_{s} = \mathrm{MaskNet}(\mathbf{Z}_{s}; \theta^{\mathrm{Mask}}), \tag{11}
$$
$$
\hat{\mathbf{X}}_{s} = \mathbf{M}_{s} \odot \mathbf{Y}, \tag{12}
$$
$$
\hat{\mathbf{x}}_{s} = \mathrm{Reconstruct}(\hat{\mathbf{X}}_{s}; \theta^{\mathrm{Reconst}}). \tag{13}
$$

The mask is inspired by the sparseness assumption of speech: different speakers rarely overlap in a single time-frequency bin, so a mask indicating the bins where the target is dominant can isolate it. [[concepts/ideal-binary-mask|Ideal binary masks]] assume each bin belongs to one speaker; modern real- and complex-valued masks relax this. Recent approaches perform the same masking in a learned feature domain (ConvTasNet-style [23], [39]).

![[raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/figures/bf93255d0746bb5e05973816fe708d3e73daf635923d7390f02f838b61451505.jpg|Fig. 4: Example of time-frequency mask for speech extraction]]
*Figure 4: Time-frequency mask for speech extraction — applying the mask to the mixture yields the extracted target speech.*

### Integration with Microphone Array Processing

When a microphone array is available, TSE can replace the masking of Eq. (12) with [[concepts/beamforming|beamforming]] (e.g., [[concepts/mvdr-beamformer|MVDR]]):

$$
\hat{X}_{s}[n, f] = \mathbf{W}^{\mathsf{H}}[f] \mathbf{Y}[n, f], \tag{14}
$$

where beamformer coefficients $\mathbf{W}[f]$ are derived from spatial correlation matrices computed from the TSE-estimated mask [30], [42], [43]. This yields **distortionless** extraction, often preferable as an ASR front-end [10].

### Training

TSE models are trained on simulated mixtures — clean speech samples from a target speaker, an interferer, and noise are mixed following Eq. (1). The clue comes from another utterance by the target speaker (audio) or the video associated with the target speech (visual).

![[raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/figures/2e7dbab4c4748f57d2085869974bf276c298ecfe2d9c4bf6cc4c3ce04e64627d.jpg|Fig. 5: Example of generating simulation data for training or testing]]
*Figure 5: Simulation data generation assumes video availability; audio-only TSE does not require video, and visual-only TSE may use a single video per speaker.*

The training loss is minimized over $(\mathbf{x}_{s}, \hat{\mathbf{x}}_{s})$ triplets:

$$
\theta^{\mathrm{TSE}} = \arg\min_{\theta} \mathcal{L}(\mathbf{x}_{s}, \hat{\mathbf{x}}_{s}). \tag{15}
$$

Common losses: cross-entropy between oracle and estimated masks, magnitude-spectrum MSE, and (recently dominant) **negative scale-invariant SNR** in the time domain [6], [23], [39]:

$$
\mathcal{L}^{\mathrm{SNR}}(\mathbf{x}_{s}, \hat{\mathbf{x}}_{s}) = -10 \log_{10}\left(\frac{\|\mathbf{x}_{s}\|^{2}}{\|\mathbf{x}_{s} - \hat{\mathbf{x}}_{s}\|^{2}}\right). \tag{16}
$$

Variants include SI-SNR and signal-to-distortion ratio (SDR) [44], or an end-to-end ASR loss for TS-ASR applications [45]. The clue encoder can be **pre-trained** (speaker identification, lip-reading) or **jointly trained** with the extraction module; multi-task schemes that add a speaker-discriminative loss on the embeddings [46] are a common middle ground.

## Applications Survey

### Audio-Clue-Based TSE

**Audio clue encoder variants** (Fig. 6):

1. **i-vectors** [50] — the pre-2010 speaker-verification paradigm; adapts a [[concepts/gaussian-mixture-model|GMM]]-UBM mean supervector via $\boldsymbol{\mu} = \mathbf{m} + \mathbf{T}\mathbf{w}$. Captures both speaker and channel variability, which can help when enrollment and mixture share channel conditions.
2. **NN-based embeddings** — d-vectors and [[concepts/speaker-embedding|x-vectors]] [51] trained for speaker classification with a pooling layer (mean + optional std). Highly speaker-discriminative, robust to channel/content variability, and readily available from public models.
3. **Jointly-learned embeddings** [10], [31] — the embedding NN is co-trained with the extraction module, directly optimizing for TSE.

![[raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/figures/264cd4c37e42c8b2963a8ea4817c4d9ee06471aed3bb803cd70bbcb242e6e2c0.jpg|Fig. 6: Illustration of i-vector, NN-based, and jointly-trained embeddings]]
*Figure 6: i-vector, NN-based, and jointly-trained embedding schemes; orange parts are training-only.*

**Existing approaches** — SpeakerBeam [10] (single- and multi-channel, with mask or beamformer extractor), VoiceFilter [11] (ASR-focused, streaming variants), speaker-inventory systems [40] (multiple enrolled speakers, meeting scenario), and SpEx/SpEx+ [31] (time-domain).

**Experimental results** (Fig. 7) — Time-domain [[concepts/td-speakerbeam|SpeakerBeam]] on WSJ0-2mix, WHAM!, WHAMR!. The direct TSE scheme outperforms the cascade BSS-then-speaker-ID system, especially in difficult conditions (WHAMR!), because (i) the TSE model does not waste capacity on extracting other speakers and (ii) the TSE model is given additional speaker information.

![[raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/figures/dc311945264454cf1c69e03e99efa148c90c61a37a0c7023e32bc1d1aeee7bce.jpg|Fig. 7: Comparison of TSE and cascade BSS systems in SI-SNR improvement]]
*Figure 7: Comparison of TSE and cascade BSS systems using an audio clue (SI-SNR improvement, higher is better) [52].*

![[raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/figures/174da47b5e0300f4db4e26d1e667250048ab7745d1d52f953106bee447ebd247.jpg|Fig. 8: Example of spectrograms of mixed, reference, and extracted speech]]
*Figure 8: Spectrograms of mixed, reference, and extracted speech from the WHAMR! database.*

**Limitations** — Audio-clue TSE is practical (no extra hardware), but vulnerable to intra-speaker variability (emotion, channel, Lombard effect) and inter-speaker similarity. Future directions include adopting advances from speaker verification (realistic large-scale datasets, self-supervised pre-trained features).

### Visual / Multi-Modal Clue-Based TSE

Visual clues derive from the lip movements of the target speaker captured by a camera. They are time-synchronized with the target speech and not corrupted by interferers, so visual TSE handles same-gender mixtures better than audio TSE. The visual clue encoder processes the video signal:

$$
\mathbf{E}_{s}^{(v)} = \mathrm{Upsample}(\mathrm{NN}(\mathrm{VFE}(\mathbf{C}_{s}^{(v)}), \theta^{\mathrm{v\text{-}clue}})), \tag{18}
$$

where $\mathrm{VFE}$ is a visual feature extractor and $\mathrm{Upsample}$ matches the audio frame rate.

![[raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/figures/04a2115dbf5b60d0b18ee2cba763edc75dfad33cc7f15ffb8401799792a35487.jpg|Fig. 9: Visual clue-based TSE system]]
*Figure 9: Visual clue-based TSE system.*

**Visual feature extractor options**:

| Source | Training task | Captures | Training data |
|:-------|:--------------|:---------|:--------------|
| Face landmarks [32] | Off-the-shelf keypoint detector | Mouth/eye/nose positions | None (rule-based) |
| FaceNet embeddings [8] | Face recognition | Speaker identity (not lip dynamics) | Still images with identity labels |
| Lip-reading embeddings [7] | Visual speech recognition | Phoneme/word content | Video with phoneme/word transcripts |
| Audio-visual sync embeddings [9] | Audio-video synchronization | Lip-motion/sound timing | Self-supervised (audio-shifted video) |

**Audio-visual fusion** (Fig. 10) — combines the strengths of both clues via concatenation [35], summation, or attention-based weighted summation [33], [34] (dynamic per-clue reliability).

![[raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/figures/eb03376903ee3c14d07d1ec794474f0067030b0c246d4c3c55700d95bcdeebb6.jpg|Fig. 10: Audio-visual clue-based TSE system]]
*Figure 10: Audio-visual clue-based TSE system.*

**Experimental results** (Fig. 11) — Audio, visual, and audio-visual SpeakerBeam on LRS3-TED, comparing same/different-gender mixtures and clue corruptions (audio enrollment with 0 dB SNR white noise; video with mouth-masked frames). Visual TSE has a smaller gap between same- and different-gender mixtures than audio TSE; the audio-visual combination achieves the best performance and is the most robust to clue corruption.

![[raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/figures/37c0f6b7d337848ba384dc5535b6d9fd24bc99e4787b7e81a767bfafc30946c1.jpg|Fig. 11: SDR improvement of audio, visual, and audio-visual TSE]]
*Figure 11: SDR improvement of TSE with audio, visual, and audio-visual clues for mixtures of same/different gender and for corruptions of audio and visual clues.*

**Open issues** — Most approaches assume face tracking and audio-video synchronization are solved; video processing is computationally heavy, motivating research into efficient online systems.

### Spatial Clue-Based TSE

When a microphone array is available, the target speaker can be identified by location. Spatial clues take two forms: a known DOA (e.g., driver's position in a car) or a multi-channel enrollment utterance recorded at the target location.

![[raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/figures/e47dfdeeb43ed4e9aa059d0157da647c8aafbc5c6cbb2ea6e631a02816d271dc.jpg|Fig. 12: Illustration of spatial clue encoder and directional features]]
*Figure 12: Spatial clue encoder structure and directional feature visualization.*

**Directional features** — the dominant form is the **angle feature**, the cosine of the difference between the target phase difference (TPD) and the interaural phase difference (IPD):

$$
\mathrm{AF}[n, f] = \sum_{m_{1}, m_{2} \in \mathcal{M}} \cos\left(\mathrm{TPD}(m_{1}, m_{2}, \phi_{s}, f) - \mathrm{IPD}(m_{1}, m_{2}, n, f)\right), \tag{19}
$$
$$
\mathrm{TPD}(m_{1}, m_{2}, \phi_{s}, f) = \frac{2\pi f F_{s}}{F} \frac{\cos\phi_{s}\,\Delta_{m_{1}, m_{2}}}{c}, \tag{20}
$$
$$
\mathrm{IPD}(m_{1}, m_{2}, n, f) = \angle Y^{m_{2}}[n, f] - \angle Y^{m_{1}}[n, f], \tag{21}
$$

where $\phi_{s}$ is the target direction, $c$ the speed of sound, and $\Delta_{m_{1}, m_{2}}$ the inter-microphone distance. Angle features approach $\pm 1$ for time-frequency bins dominated by a source from $\phi_{s}$. Other directional features include fixed-grid beamformer power ratios and directional SNRs.

**Experimental results** (Fig. 13, Gu et al. [36]) — Mandarin audio-visual dataset, two- and three-speaker mixtures, conditions split by inter-speaker angle separation. Spatial clues are very effective but performance drops sharply when speakers are < 15° apart; combining spatial with audio/visual clues outperforms any single-clue system in all conditions.

![[raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/figures/fe6a74bb88cf8ed69fa14c4f508223d6a1fcc13014d76a4355f42446141b26bd.jpg|Fig. 13: SI-SNR improvement of TSE with audio, visual, and spatial clues]]
*Figure 13: SI-SNR improvement of TSE with audio, visual, and spatial clues under four conditions based on angle separation between speakers [36].*

**Limitations** — Requires a microphone array and a way to localize the target; fails when DOA estimation is wrong or speakers are not angularly separable. Most work assumes a fixed source location, with few exceptions [24].

### Extensions to Other Tasks

#### Target-Speaker ASR (TS-ASR)

[[concepts/target-speaker-asr|TS-ASR]] aims to transcribe the target speaker while ignoring interferers. Three architectures:

1. **Cascade**: TSE front-end + ASR back-end (modular, interpretable, but TSE artifacts limit gains).
2. **Joint training**: TSE front-end and ASR back-end interconnected by differentiable operations (beamforming, feature extraction) and jointly trained [10].
3. **Integrated**: clue conditioning is inserted directly into the ASR network [26], [45] — lower cost, less interpretable.

Audio clues come from pre-recorded enrollment [10], [26], [45] or a keyword ("anchor") for smart devices [54]; visual clues can also be used [55].

#### Target-Speaker VAD and Diarization

[[concepts/target-speaker-vad|Target-speaker VAD]] exploits a speaker embedding from an enrollment to predict the target speaker's activity (a binary classifier in place of the mask estimator in the TSE framework) [27]. Multi-target extension [[concepts/target-speaker-vad|TS-VAD]] [28] simultaneously predicts the activity of multiple target speakers and achieved the top diarization performance in the CHiME-6 campaign. Audio-visual VAD [56] uses video clues analogously.

## Key Contributions

1. **Unified framework**: introduces the general neural TSE framework (clue encoder + mixture encoder + fusion layer + target extractor) that subsumes audio, visual, and spatial clue variants under a single description, enabling straightforward multi-clue combinations.
2. **Taxonomy**: organizes TSE approaches along four orthogonal axes (clue type, channel count, speaker-close/open, generative/discriminative) and traces the historical lineage from 1980s beamforming through ICA/IVA/IVE, F-HMM/NMF, deep clustering/PIT, to enrollment-conditioned neural TSE.
3. **Fusion layer survey**: tabulates five widely used fusion layers (concatenation, addition, multiplication, FiLM, factorized) with equations and parameter counts, and reports empirically that the choice has "rather insignificant" impact.
4. **Comparative experiments**: uses a single time-domain SpeakerBeam backbone to compare (a) direct TSE vs. cascade BSS+speaker-ID, (b) audio/visual/audio-visual clues under same-gender and corrupted-clue conditions, and (c) audio/visual/spatial clues under varying angular separations.
5. **Open-challenge agenda**: identifies inactive-target-speaker handling, training/evaluation criteria separating extraction vs. identification errors, robustness to real recording conditions, lightweight/low-latency deployment, and spatial rendering for hearables as the principal open problems.
6. **Resources catalog**: Table III lists datasets (WSJ0-mix, WHAM(R)!, LibriMix, LibriCSS, MC-WSJ0-mix, SMS-WSJ, LRS, AVSpeech) and open implementations (SpeakerBeam, SpEx+, VoiceFilter, Multisensory, AV-speech-enh, FaceNet).

## Limitations and Caveats

- The paper focuses on **neural, discriminative, speaker-open** approaches; classical ICA/IVA/IVE and NMF/F-HMM methods are covered only as historical context, and generative Bayesian approaches (e.g., spatial-clue CVAE [29]) are mentioned but not surveyed in depth.
- Most reported experiments are the authors' own (time-domain SpeakerBeam variants on WSJ0-2mix, WHAM!, WHAMR!, LRS3-TED, and a Mandarin AV corpus); a comprehensive cross-method benchmark is not provided.
- **Coverage cutoff**: literature reviewed is up to early 2023; post-2023 developments in self-supervised speaker encoders (e.g., ECAPA-TDNN successors), diffusion-based TSE, large-scale pre-training for multi-modal TSE, and efficient architectures (e.g., Mamba/MinGRU for OVC) are not covered.
- Visual TSE coverage assumes face tracking and audio-video synchronization are solved pre-processing problems; computational cost of online visual TSE is identified as an open issue but not quantitatively addressed.
- The "best variant" recommendations are mostly qualitative (e.g., "multiplication or FiLM usually perform well", "audio-visual combination is most robust"); per-architecture quantitative comparisons are deferred to cited primary works.

## Related Concepts

- [[concepts/target-speaker-extraction|Target Speaker Extraction (TSE)]]
- [[concepts/td-speakerbeam|TD-SpeakerBeam]]
- [[concepts/cocktail-party-problem|Cocktail-Party Problem]]
- [[concepts/target-speaker-vad|Target-Speaker VAD (TS-VAD)]]
- [[concepts/target-speaker-asr|Target-Speaker ASR (TS-ASR)]]
- [[concepts/angle-feature|Angle Feature]]
- [[concepts/speaker-embedding|Speaker Embedding]]
- [[concepts/ecapa-tdnn|ECAPA-TDNN]]
- [[concepts/film-layer|FiLM Layer]]
- [[concepts/ideal-binary-mask|Ideal Binary Mask]]
- [[concepts/gaussian-mixture-model|Gaussian Mixture Model]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/permutation-invariant-training|Permutation Invariant Training (PIT)]]
- [[concepts/deep-clustering-speech-separation|Deep Clustering Speech Separation]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/dereverberation|Dereverberation]]
- [[concepts/independent-vector-analysis|Independent Vector Analysis (IVA)]]
- [[concepts/voice-activity-detection|Voice Activity Detection]]
- [[concepts/deep-filtering|Deep Filtering]]
- [[concepts/time-domain-speech-enhancement|Time-Domain Speech Enhancement]]
- [[concepts/personalized-speech-enhancement|Personalized Speech Enhancement]]

## Related Synthesis

- [[synthesis/deep-speech-enhancement|Deep Speech Enhancement]]
- [[synthesis/multi-modal-speech-enhancement|Multi-Modal Speech Enhancement]]
- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
