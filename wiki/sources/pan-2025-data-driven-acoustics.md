---
type: source
created: 2026-09-19
updated: 2026-09-19
sources:
  - raw/papers/pan-2025-data-driven-acoustics/full-text.md
  - https://doi.org/10.48550/arXiv.2508.21470
  - zotero://select/items/0_WP9DAVN6
tags:
  - deep-learning
  - signal-processing
  - speech-enhancement
  - source-separation
  - speaker-recognition
  - sound-event-detection
  - survey
---

# Pan 2025: Fundamentals of Data-Driven Approaches to Acoustic Signal Detection, Filtering, and Transformation

**Author**: [[entities/chao-pan|Chao Pan]]
**Venue**: arXiv preprint 2508.21470 (submitted 2025-08-29)
**Type**: Tutorial / survey (single-author, text-only, no figures)
**DOI**: [10.48550/arXiv.2508.21470](https://doi.org/10.48550/arXiv.2508.21470)

## Summary

This tutorial systematically summarizes the principles and methods of data-driven (deep-learning-based) acoustic signal processing under a single unifying taxonomy: every technique is cast as **signal detection**, **signal estimation/filtering**, or **signal transformation**. It builds from neural-network fundamentals (notation, objective functions, backpropagation, optimizers) through network modules explained from a digital-signal-processing perspective, then develops a task-dependent loss-function construction methodology, and finally applies the framework to five fundamental acoustic problems — sound source localization, sound event detection, voiceprint extraction and recognition, noise reduction, and source separation — before closing with the author's reflections on generative adversarial learning, optimal transport, AUC optimization, diffusion models, and data visualization.

## Taxonomy

The paper's central claim is that the diversity of acoustic signal processing techniques reduces to three task types, and that the **construction of the objective function** — not the network architecture — is what distinguishes them:

| Task type | Goal | Typical losses | Acoustic applications |
|:----------|:-----|:---------------|:----------------------|
| **Detection** | Identify the existence of target information and its time/location | BCE, Dice loss (class imbalance), softmax CE, AUC optimization | Sound source localization (DOA), [[concepts/sound-event-detection\|sound event detection]], speaker verification/identification |
| **Estimation/Filtering** | Extract or separate source signals from observations | MSE, robust losses, [[concepts/si-sdr\|SI-SDR]], spectral-distance losses | Noise reduction / [[concepts/speech-enhancement\|speech enhancement]], source separation |
| **Transformation** | Convert signals to a more suitable domain for analysis | Contrastive/metric losses, density-alignment losses (optimal transport, adversarial) | Voiceprint extraction, feature learning, generative modeling, data visualization |

Within detection, the network output layer takes four canonical forms: sigmoid (single-target probability), softmax (multi-class), multiple sigmoid (multi-target probabilities), and linear-map-plus-sign (max-margin hyperplane, SVM-style).

## Methodology (Surveyed Frameworks)

### Composite-Function Notation

The tutorial's distinctive notational device is to express every architecture as a composition of module functions: $\mathcal{C}(\cdot)$ for CNNs, $\mathcal{G}(\cdot)$ for gated recurrent networks, $\mathcal{R}(\cdot)$ for residual networks, $\mathcal{U}(\cdot)$ for U-Net, $\mathcal{E}(\cdot)$/$\mathcal{D}(\cdot)$ for encoder/decoder, $\mathcal{A}(\cdot)$ for feature fusion, $\mathcal{F}(\cdot)$ for fully connected, $\mathcal{T}(\cdot)$ for transformers, and $\mathcal{S}(\cdot)$ for the output layer (sigmoid/softmax/linear). A full network is written e.g. $f(\bm{x}) = \mathcal{S} \circ \mathcal{F}_{3} \circ \mathcal{F}_{2} \circ \mathcal{F}_{1} \circ \mathcal{A} \circ \mathcal{C}_{3} \circ \mathcal{C}_{2} \circ \mathcal{C}_{1}(\bm{x})$, with $f_{\not{\mathcal{S}}}(\bm{x})$ denoting the network with the output layer removed (used when discussing training targets separately from embeddings).

### Network Modules from a DSP Perspective

- **Neuron as template matcher**: a neuron $\sigma[\bm{w} \bullet \bm{x}(t) + b]$ computes the inner product (similarity) between the input slice and a learned template $\bm{w}$; training finds suitable templates.
- **CNN**: convolution recast as filter inner products $\bm{w}(i) \bullet \bm{x}(t-i)$ — the fundamental linear-system filtering operation.
- **RNN / LSTM / GRU**: temporal-context models with gated state updates.
- **Residual, encoder-decoder, U-Net, feature fusion, self-attention**: each presented as a composable module with its input/output roles; the **Conformer** block is decomposed into four residual sub-modules (feed-forward half, multi-head attention, convolution, feed-forward half) plus layer normalization.
- **Signal slicing**: all acoustic inputs are reduced to "slices" — stacked time samples $\bm{x}(t) = [x(tK), \ldots, x(tK-L+1)]^{T}$, STFT frames, or extracted features (MFCC, Mel spectrogram).

### Loss Construction by Task

- **Detection**: BCE and its batch decomposition into positive/negative subsets; the **class imbalance problem** (rare positives) motivates Dice loss; multi-instance aggregation for frame-level labels.
- **Estimation**: MSE (whose optimum implies Gaussian error density); robust losses (Huber, truncated-hinge SVM family) for heavy-tailed errors; scale-invariant waveform losses — the tutorial derives [[concepts/si-sdr|SI-SDR]] as $-\rho_{\bm{s}\hat{\bm{s}}}^{2}/(1-\rho_{\bm{s}\hat{\bm{s}}}^{2})$ per frame, where $\rho$ is the Pearson correlation coefficient between target and estimate, showing that minimizing SI-SDR loss is *equivalent to maximizing the correlation coefficient* with an optimal scale factor $\alpha_t = \hat{\bm{s}}^{T}\bm{s}/\|\bm{s}\|^{2}$.
- **Transformation**: clustering properties (minimize intra-class, maximize inter-class distance — LDA as the classical linear case, contrastive losses with hinge $\max(0, \zeta_0 - \|\bm{z}_n - \bm{z}_i\|^{2})$ as the nonlinear case) and density properties (align the density of $\{f(\bm{x}_n)\}$ with a target dataset $\{\ddot{\bm{y}}_n\}$ without one-to-one correspondence — GANs and optimal transport).

## Applications Survey

| Application | Task type | Input features | Output form | Key challenges |
|:------------|:----------|:---------------|:------------|:---------------|
| Source localization (Section 4) | Detection | Spatial spectra / multichannel spectra | Angle-grid probabilities or Cartesian vector | Angle encoding, multi-source, joint detection+localization |
| Sound event detection (Section 5) | Detection | Mel spectrogram | $L \times T$ frame-event probability matrix | Class imbalance, aggregation from weak labels |
| Voiceprint extraction/recognition (Section 6) | Transformation (with detection-flavored applications) | MFCC | Fixed-dim embedding | Domain mismatch, open-set enrollment |
| Noise reduction (Section 7) | Estimation | Log-magnitude spectra / waveforms | Wiener gain, mask, or waveform | Loss level choice (gain/spectrum/waveform), phase |
| Source separation (Section 8) | Estimation | TF spectra (+ priors) | Per-source masks or waveforms | Permutation ambiguity |

### Source Localization

Signal model: direct-path propagation $p_m(t) = h_0 s(t - \tau_m) + \text{reflections}$, with the source angle encoded in inter-channel time differences $\tau_m - \tau_1 = \delta_{m,1}\cos\theta/c$; in the STFT domain these become phase shifts $e^{-\jmath\omega(\tau_m - \tau_1)}$. Localization is framed as **detection over directions**: the label indicates whether a source is active in a given direction. Loss options surveyed: softmax + CE over an angle grid (classification); multi-head sigmoid + BCE (multi-direction presence); regression to a unit Cartesian vector $\bm{\varphi}_n(t)$ with MSE; and the joint detection+localization cost [[concepts/activity-coupled-cartesian-doa|ACCDOA]], where the label is a $3 \times L$ matrix whose column norm is the activity probability and whose normalized column is the direction. Typical networks: CNN + FC on spatial spectra (frequency downsampled per layer); a multi-objective network (source count via softmax + angle via multi-sigmoid, sharing a 10-layer convolutional $g(\bm{x})$); and a U-Net mapping $T \times K \times 2M$ inputs to per-time-frequency-angle probabilities whose angle-summed output also yields a TF mask for direction-based extraction.

### Sound Event Detection

Input is the Mel spectrogram (e.g., 40 ms / 20 ms framing, 64 Mel bands); the network outputs an $L \times T$ frame-level probability matrix $\hat{\bm{Y}}$ plus clip-level $\hat{\bm{y}}$ after an aggregation layer $\mathcal{A}(\cdot)$ (multiple-instance-learning pooling). Class imbalance (dozens–hundreds of event types, sparse occurrence) is handled with Dice-type losses. Typical networks: a fully convolutional network (4 conv blocks, channels 32→64→128→128, $3\times3$ kernels, BN+ReLU, $1\times1$ conv to 41 event channels + sigmoid, frequency-averaged then aggregated) and a CRNN (conv layers + gated recurrent layer + multi-sigmoid output).

### Voiceprint Extraction and Recognition

Three application points: speaker **verification** (single-target detection against enrolled voiceprints), speaker **identification** (multi-target detection), and **diarization** (clustering over time slices). Because users will not upload their data, the train-time and usage-time speakers differ — a **domain mismatch** that forces voiceprint *extraction* to be a signal *transformation* task even though recognition is a detection task. Learning strategies: (i) classification — train $g(\cdot)$ with a softmax head + CE over $L$ training speakers, then discard the head; (ii) contrastive/clustering — minimize same-speaker distance $\|\bm{z}_n - \bm{z}_i\|^{2}$, hinge-truncate different-speaker distance at $\zeta_0$. Typical network: the **TDNN x-vector** extractor — five 1-D conv layers over 24-dim MFCC slices (kernels 5/5/7/1/1, dilated time context, channels 512/512/512/512/1500), statistics pooling (mean + std → 3000-dim), FC to a 512-dim embedding; enrollment compares cosine similarity against a voiceprint library.

### Noise Reduction

Framed as analysis–filter–reconstruction in the STFT domain: framing must satisfy the perfect-reconstruction window constraint $\sum_i \psi(t - iL_s) = 1$ (equivalently $\bm{A}\bm{\psi} = \bm{1}$, which constrains the window family given the overlap factor). Filtering multiplies the spectrum by a gain — classically the optimal Wiener gain, a real number in $[0,1]$ per frequency band. The tutorial organizes the loss design in three levels:

1. **Distance between filters** — BCE between the network output $\hat{\bm{h}}(t)$ and the optimal Wiener gain $\bm{h}(t)$ (see [[concepts/wiener-filter|Wiener filter]]);
2. **Distance between spectra** — $\|\hat{\bm{h}}(t) \odot |\bm{y}(t)| - |\bm{s}(t)|\|^{2}$, approximating the ideal mask first and refining against spectral amplitudes;
3. **Distance between waveforms** — the scale-invariant loss, i.e., [[concepts/si-sdr|SI-SDR]], equivalent to maximizing the frame-wise correlation coefficient.

Worked example (Han et al. 2015): concatenate $2Q{+}1$ log-magnitude spectra (16 kHz, 20 ms window, 161 frequency points, $Q=5$ → 1771-dim input) → three FC layers with 1600 units and ReLU → 161-dim sigmoid output estimating the Wiener gain; introduces $Q$-frame algorithmic delay. The section also contrasts time-domain end-to-end networks with frequency-domain analysis–filter–reconstruction frameworks.

### Source Separation

The **permutation ambiguity problem**: forcing fixed output-to-source label assignment creates a one-to-many mapping that prevents convergence. [[concepts/permutation-invariant-training|Permutation-invariant training]] replaces forced matching with optimal matching, $\mathcal{J} = \min_{\bm{p} \in \mathcal{P}} \sum_{j} d[\hat{\bm{s}}^{(j)}, \bm{s}^{(p_j)}]$ over $J!$ permutations. Within the transform-domain framework, [[concepts/tf-mask-estimation|mask estimation]] uses ideal masks $\bm{h}_i(t) = |\bm{s}^{(j)}(t)|^{2}/(\epsilon_0 + \sum_i |\bm{s}^{(i)}(t)|^{2})$ trained with PIT plus magnitude-spectral losses. **Prior-based methods** condition the network on voiceprint or spatial features (RTF phases, steering-vector inner products, beamformed pre-processing) by feature concatenation $\hat{\bm{h}}_j(t) = f_j[\tilde{\bm{x}}(t) \ddagger \bm{c}]$. **Clustering-assisted methods** add the [[concepts/deep-clustering-speech-separation|deep clustering]] loss $\|\bm{V}^{T}\bm{V} - \bm{U}^{T}\bm{U}\|^{2}$ over per-TF-bin embeddings, weighted by $\beta$ against the PIT mask loss; the clustering center of a source can serve as its voiceprint for conditioned extraction (Wavesplit).

## Advanced Topics (Section 9)

- **Generative adversarial learning** (GAN/CGAN/CycleGAN): characterizing the target *with data* — a discriminator $d(\bm{x})$ defines the training signal for the generator $g(\bm{z})$; consistency constraints and data-boundary constraints for style transfer; adversarial strategies for small-sample feature learning.
- **Optimal transport**: the Kantorovich program — minimize $\int\int \hbar(\bm{x}, \breve{\bm{x}}) c(\bm{x}, \breve{\bm{x}})$ over joint distributions with fixed marginals — defines a distance between data densities that can be backpropagated, aligning distributions without labels (WGAN connection).
- **AUC optimization**: recall and false-positive rate trade off along the ROC curve; the area under the curve is the *optimal optimization target* for detection, expressible as a pairwise ranking objective over positive/negative score pairs.
- **Diffusion models**: a forward Gaussian degradation process $q(\bm{x}^{(t)}|\bm{x}^{(t-1)}) = \mathcal{N}[\bm{x}^{(t)}; \sqrt{\alpha_t}\bm{x}^{(t-1)}, (1-\alpha_t)\bm{I}]$ with closed-form marginals $q(\bm{x}^{(t)}|\bm{x}^{(0)}) = \mathcal{N}[\bm{x}^{(t)}; \sqrt{\breve{\alpha}_t}\bm{x}^{(0)}, (1-\breve{\alpha}_t)\bm{I}]$, $\breve{\alpha}_t = \prod_i \alpha_i$; the generative direction follows from Bayes' theorem (see [[concepts/diffusion-models-for-speech|diffusion models for speech]]).
- **Data visualization**: MDS (match low-dim pairwise distances $\bm{Y}^{T}\bm{Y} = \bm{Q}\bm{D}\bm{Q}^{T}$), SNE/t-SNE, and LLE — a special case of signal transformation.

## Key Contributions

1. **Task triad taxonomy**: unifies acoustic signal processing — from localization to separation to generative modeling — under detection / estimation-filtering / transformation, with each task type dictating its own loss-construction methodology.
2. **Composite-function notation**: a compact module-algebra ($\mathcal{C}, \mathcal{G}, \mathcal{R}, \mathcal{U}, \mathcal{E}, \mathcal{D}, \mathcal{A}, \mathcal{F}, \mathcal{T}, \mathcal{S}$) for expressing arbitrary architectures, including output-layer removal $f_{\not{\mathcal{S}}}$.
3. **DSP-grounded module explanations**: neurons as template matchers, CNNs as filtering, framing as a constrained window design ($\bm{A}\bm{\psi} = \bm{1}$) — bridging classical signal processing and deep learning.
4. **Worked network examples per application**: concrete architectures with dimensions (multi-frame FC Wiener-gain estimator, SED FCN/CRNN, TDNN x-vector, U-Net localization) rather than abstract architecture name-dropping.
5. **Distinctive reformulations**: SI-SDR as a monotone function of the correlation coefficient; the deep-clustering affinity-matching loss; PIT as optimal matching; AUC as a pairwise ranking objective.

## Limitations and Caveats

- The author explicitly states the paper "does not claim to be exhaustive" and invites corrections — it is a personal-perspective tutorial (arXiv v1, 2025-08-29), not a systematic literature survey; the reference list (~80 entries) is modest for the breadth covered.
- No quantitative experiments, benchmarks, or comparisons — all "typical network" examples are reproduced qualitatively from cited literature.
- No figures; all concepts are conveyed through equations and prose.
- Coverage is weighted toward the author's own research lineage (microphone arrays, Wiener filtering, source separation with Benesty/Chen collaborations); e.g., large-scale pre-trained models, self-supervised learning, and real-time deployment constraints receive little attention.

## Related Concepts

- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]
- [[concepts/neural-networks|Neural Networks]]
- [[concepts/sound-source-localization|Sound Source Localization]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/activity-coupled-cartesian-doa|ACCDOA]]
- [[concepts/sound-event-detection|Sound Event Detection]]
- [[concepts/sel-d|SELD]]
- [[concepts/speaker-verification|Speaker Verification]]
- [[concepts/speaker-embedding|Speaker Embedding]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/wiener-filter|Wiener Filter]]
- [[concepts/si-sdr|SI-SDR]]
- [[concepts/tf-mask-estimation|TF Mask Estimation]]
- [[concepts/permutation-invariant-training|Permutation Invariant Training]]
- [[concepts/deep-clustering-speech-separation|Deep Clustering for Speech Separation]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/diffusion-models-for-speech|Diffusion Models for Speech Enhancement]]
- [[concepts/target-speaker-extraction|Target Speaker Extraction]]
- [[concepts/spectrogram-analysis|Spectrogram Analysis]]

## Related Sources

- [[sources/xiang-2025-wiener-gain-reverberant|Xiang et al. 2025: Design of the Wiener Gain in Noisy and Reverberant Environments]] — the author's own work on the Wiener gain that Section 7 uses as the classical filtering reference
- [[sources/grumiaux-2022-ssl-deep-learning-survey|Grumiaux et al. 2022: A Survey of SSL with Deep Learning Methods]] — deeper DL-based localization survey complementing Section 4
- [[sources/wang-2018-supervised-speech-separation-deep-learning-overview|Wang & Chen 2018: Supervised Speech Separation Based on Deep Learning: An Overview]] — the canonical separation overview complementing Section 8
- [[sources/ansari-2023-ai-bss-survey|Ansari et al. 2023: AI Approaches in BSS Survey]] — DNN-based mask prediction survey complementing Section 8.4
- [[sources/zmolikova-2023-neural-target-speech-extraction-overview|Zmolikova et al. 2023: Neural Target Speech Extraction: An Overview]] — prior-conditioned extraction, related to Section 8.5 prior-based methods
- [[sources/zheng-2023-survey-frequency-domain-speech-enhancement|Zheng et al. 2023: Sixty Years of Frequency-Domain Monaural Speech Enhancement]] — historical depth for Section 7's frequency-domain framework
