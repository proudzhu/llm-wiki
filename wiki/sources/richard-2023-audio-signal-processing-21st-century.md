---
type: source
created: 2026-08-08
updated: 2026-08-08
sources:
  - raw/papers/richard-2023-audio-signal-processing-21st-century/full-text.md
  - https://doi.org/10.1109/MSP.2023.3276171
  - https://telecom-paris.hal.science/hal-04112575
  - zotero://select/items/0_6DW9CX6C
tags:
  - audio-signal-processing
  - survey
  - retrospective
  - deep-learning
  - speech-enhancement
  - source-separation
  - dereverberation
  - beamforming
  - acoustic-echo-cancellation
  - acoustic-feedback
  - active-noise-control
  - music-information-retrieval
  - dcase
  - audio-coding
---

# Richard, Smaragdis, Gannot, Naylor, Makino, Kellermann & Sugiyama 2023: Audio Signal Processing in the 21st Century

**Authors**: [[entities/gael-richard|Gaël Richard]], [[entities/paris-smaragdis|Paris Smaragdis]], [[entities/sharon-gannot|Sharon Gannot]], [[entities/patrick-a-naylor|Patrick A. Naylor]], [[entities/shoji-makino|Shoji Makino]], [[entities/walter-kellermann|Walter Kellermann]], [[entities/akihiko-sugiyama|Akihiko Sugiyama]]
**Venue**: IEEE Signal Processing Magazine (2023) — TC-AASP 25-years retrospective
**Type**: Survey / retrospective
**DOI**: [10.1109/MSP.2023.3276171](https://doi.org/10.1109/MSP.2023.3276171)
**HAL**: [hal-04112575](https://telecom-paris.hal.science/hal-04112575)
**Zotero**: [6DW9CX6C](zotero://select/items/0_6DW9CX6C)

## Summary

A 25-year retrospective of the IEEE Technical Committee on Audio and Acoustic Signal Processing (TC-AASP), written by seven committee members on the occasion of the committee's anniversary. Building on the landmark 1997 SPS 50th-anniversary survey by Kahrs et al. [1], the paper traces the field's evolution from model-based signal representations to the current paradigm shift toward data-driven and deep-learning methods, covering coding, acoustic-environment modeling, scene analysis and synthesis, signal enhancement, source separation, objective evaluation, Music Information Retrieval (MIR), and Detection and Classification of Acoustic Scenes and Events (DCASE). It closes with perspectives on hybrid model-based deep architectures, federated learning, and multimodal processing.

## Taxonomy

The paper organizes 25 years of AASP progress along two complementary axes.

**Axis 1 — Advances and highlights (Section II)**, grouped by problem domain:

1. **Modeling and representation** — (a) audio coding and signal modeling; (b) acoustic-environment modeling, analysis, and synthesis (RIR modeling, room simulators, room-characteristic inference, artificial reverberation).
2. **Analysis of acoustic scenes** — (a) acoustic sensor networks (WASNs); (b) localization and tracking; (c) data-independent spatial filtering.
3. **Synthesis of acoustic scenes** — (a) listener-centric binaural rendering (HRTF); (b) soundfield rendering (Ambisonics, wave field synthesis, room equalization).
4. **Acoustic signal enhancement** — (a) echo cancellation; (b) acoustic feedback and active noise control; (c) dereverberation; (d) noise suppression; (e) data-dependent beamforming; (f) audio-visual enhancement.
5. **Signal separation** — (a) determined case (BSS/ICA); (b) monophonic separation (NMF, deep clustering, discriminative masking).

**Axis 2 — Emerging topics (Section III)**, fields nearly absent in the 1990s and now mainstream:

6. **Objective evaluation** — perceptual quality/intelligibility metrics and trained evaluators.
7. **Music Information Retrieval (MIR)** — early adopter of deep neural networks; deep generative models and differentiable DSP.
8. **DCASE** — acoustic scene classification and event detection; weakly-supervised learning.
9. **Consumer devices and fast internet** — VoIP, teleconferencing, music streaming/identification.

A cross-cutting theme throughout is the **paradigm shift toward data-driven methods**, with deep learning moving from isolated early adoption (MIR) to mainstream dominance across nearly all subfields.

## Methodology

As a retrospective survey, this paper does not propose a new algorithm. The "methodology" surveyed is the body of AASP work since 1997; the subsections below follow the paper's own structure.

### Audio Coding and Signal Modeling

The paper traces the MPEG audio coding family: MPEG-1 Audio (1993) → MPEG-2 Audio (1995, backward-compatible multichannel) → MPEG-2 AAC (1997, foundation of modern codecs) → MPEG-4 AAC / HE-AAC (mobile applications, 64 / 32 kbit/s) → MPEG Surround (2007, binaural-cue-based spatial coding) → MPEG SAOC (2010, object-level-difference spatial coding) → MPEG USAC (2012, first unified speech/audio switching codec) → MPEG-H (2019, 3D/HOA audio). A key bitrate-reduction tool is **bandwidth extension (BWE/SBR)**, which encodes only a low-frequency subband plus a high-frequency power envelope and lets the decoder copy the low band upward (Fig. 1).

![[raw/papers/richard-2023-audio-signal-processing-21st-century/figures/8c99c7f39bfd0ea75f1aa3d0abaff1ddf707c6011f5e74c1b60d7120e668096a.jpg|Bandwidth extension principle]]
*Figure 1: Bandwidth extension (BWE) principle. Only the low-frequency subband is encoded; the decoder reconstructs the high band by copying and envelope adjustment.*

### Acoustic Environments: Modeling, Analysis, and Synthesis

Sound propagation in enclosures is characterized by the acoustic/room impulse response (AIR/RIR), whose decaying tail is summarized by the reverberation time $T_{60}$ and whose direct-to-reverberant balance is captured by the direct-to-reverberant ratio (DRR) and the [[concepts/coherent-to-diffuse-power-ratio|coherent-to-diffuse power ratio (CDR)]]. The paper surveys: RIR generators descending from Schroeder (frequency domain), Polack (time domain), and Allen–Berkley's [[concepts/image-source-method|image method]] — including the RIR generator, PyRoomAcoustics, and gpuRIR, plus recent GAN-based RIR generation; real-world RIR databases; the ACE challenge for blind room-acoustic-parameter estimation; the annotated `dEchorate` database; and artificial-reverberation methods, notably **feedback delay networks (FDN)** and the geometry-based **Radiance Transfer Method (RTM)**, later linked to FDN for efficient geometry-based reverberators.

### Analysis of Acoustic Scenes

- **Wireless acoustic sensor networks (WASNs)** — battery-powered multi-microphone nodes with wireless links, enabling distributed/edge processing and posing node-selection, synchronization, and bandwidth-constrained fusion challenges.
- **Localization and tracking** — from cross-correlation / GCC and SRP-PHAT, through subspace methods (MUSIC, ESPRIT) adapted to cylindrical/spherical harmonics, to Bayesian trackers (nonlinear Kalman, particle, PHD filters) and recursive EM; CDR-based range estimation in WASNs; [[concepts/direction-of-arrival-estimation|DoA]] and Acoustic SLAM for moving robots.
- **Data-independent spatial filtering** — [[concepts/spherical-harmonic-transform|spherical harmonics domain]], [[concepts/differential-microphone-array|differential microphone arrays]], polynomial beamforming, robustness-constrained non-iterative designs, and HRTF-incorporated designs; also used for loudspeaker-array reproduction.

### Synthesis of Acoustic Scenes

- **Binaural rendering** via head-related transfer functions (HRTFs), with challenges in acquiring/genericizing/individualizing HRTFs and VR-based HRTF selection.
- **Soundfield rendering** — channel-based formats (5.1/7.1/10.2/22.2) with a limited sweet spot vs. soundfield-reproduction approaches (Ambisonics, wave field synthesis, spatial-frequency-domain methods) with wider sweet spots and object-based coding; room equalization when the acoustic environment must be accounted for.

### Acoustic Signal Enhancement

A typical multichannel sound system interleaves analysis-side processing (noise reduction, separation, dereverberation, echo removal, localization) with synthesis-side rendering and active noise cancellation (Fig. 2).

![[raw/papers/richard-2023-audio-signal-processing-21st-century/figures/08c9a7a7a2016035dbdc7ec9145ae3a91e777d138cc1d28bfeadd72fc3feda64.jpg|Typical multichannel sound system]]
*Figure 2: A typical multichannel sound system. The analysis side applies spatially/spectrally selective acquisition (noise reduction, speaker separation via beamforming or ICA, dereverberation, echo removal, source localization); the synthesis side applies spatially selective rendering and active noise cancellation.*

- **[[concepts/acoustic-echo-cancellation|Echo cancellation (AEC)]]** — from RLS / affine projection / subband / frequency-domain adaptive filters and double-talk detectors, to nonlinear AEC (including DNN-based), combined AEC+dereverberation+noise-reduction postfiltering, Kalman-filter-based and DNN-based step-size control, and MIMO/wave-domain AEC. The IWAENC workshop series (1989→) tracks the field.
- **[[concepts/acoustic-feedback|Acoustic feedback]] and [[concepts/active-noise-control|active noise control (ANC)]]** — adaptive feedback cancellation (usable-gain improvements up to ~10 dB for hearing aids); ANC for headphones, automotive, and aircraft; multizone bright/dark-zone rendering, reducible to spatial filtering when reference signals are modeled rather than measured.
- **[[concepts/dereverberation|Dereverberation]]** — a blind estimation problem (no anechoic reference); statistical spectral methods for the single-channel case (late-reverberant spectral variance estimation); multichannel subspace and least-squares RIR equalization; joint anechoic-signal/RIR estimation via EM + Kalman; and the **weighted prediction error (WPE)** method, which realized blind dereverberation of nonstationary colored sources via multichannel linear prediction (MCLP) with two key extensions — a nonstationary Gaussian source model and delayed prediction that protects inherent source correlations from being whitened. The REVERB Challenge benchmarked the field. Recent work is data-driven (DNN-based spectral mapping), with the authors expecting continued model-based + data-driven hybridization.
- **Noise suppression** — from Boll/Berouti spectral subtraction and the Ephraim–Malah statistically-optimal spectral-amplitude / log-spectral-amplitude (LSA) estimators (with signal-presence-uncertainty and decision-directed a-priori-SNR estimation), through phase-aware enhancement, all-pole/EM+Kalman model-based enhancement, to DNN-based mask estimation: [[concepts/ideal-binary-mask|ideal binary mask (IBM)]], [[concepts/ideal-ratio-mask|ideal ratio mask (IRM)]], and the phase-sensitive [[concepts/complex-ratio-mask|complex ideal ratio mask (cIRM)]]. Open challenges: training-data scale and model size (driving interest in "thin" edge-deployable models), mandatory low latency for telecommunications, and hard environments (babble, extreme industrial noise, transient keyboard/wind noise).
- **Data-dependent beamforming** — from free-field models to AIR-aware matched filtering; the [[concepts/relative-transfer-function|relative transfer function (RTF)]] as a substitute for the acoustic transfer function in [[concepts/mvdr-beamformer|MVDR]] design; criteria including MVDR, [[concepts/multi-channel-wiener-filter|multichannel Wiener filter (MWF)]] and its speech-distortion-weighted (SDW-MWF) variant, maximum-SNR, and [[concepts/lcmv-beamformer|LCMV]]; binaural-cue-preserving algorithms; and distributed WASN versions. Three DNN trends: (1) DNN estimates building blocks of statistically-optimal beamformers; (2) DNN directly estimates multichannel beamformer weights (enables perceptual/WER losses but less robust); (3) DNN applied directly to multichannel data, abandoning the beamformer structure.
- **Audio-visual enhancement** — lip/face cues to extract a desired speaker from noise and competing speakers.

### Signal Separation

- **Determined case** — [[concepts/blind-source-separation|blind source separation]] began as an application of Independent Component Analysis (ICA); convolutive room mixtures are handled via frequency-domain ICA (STFT → instantaneous per-bin ICA), with permutation/scaling ambiguities resolved using spatial and spectral source information. Notable frameworks: **TRINICON** (information-theoretic cost using nonwhiteness, nongaussianity, nonstationarity); [[concepts/independent-vector-analysis|independent vector analysis (IVA)]]-family methods; **NMF** source separation via common spectral patterns; **ILRMA** (combining ICA spatial info with NMF spectral info); and the **multichannel VAE (MVAE)**, combining ICA spatial info with DNN spectral priors.
- **Monophonic separation** — NMF with trained target-specific spectral dictionaries; **W-disjoint orthogonality** (sparsity-based binary masking of spectrograms) as a cornerstone; **[[concepts/deep-clustering-speech-separation|deep clustering]]** (projecting T-F bins into a latent space for source-attributed clustering); and discriminative mask-prediction networks (dominant today, from on-device voice-communication enhancers to offline models used in award-winning Beatles restorations), exploring U-net/transformer architectures, soft masks, latent-space models, [[concepts/permutation-invariant-training|permutation-invariant training (PIT)]], user-guided conditional separation, and perceptual-loss optimization. Open questions: universal separators, limited-data learning, out-of-distribution generalization (Fig. 3).

![[raw/papers/richard-2023-audio-signal-processing-21st-century/figures/a6c1db96b52bf6e4080076a282e734c528ea4bad53c3e08392564271db5ebe80.jpg|Approaches for monophonic separation]]
*Figure 3: Examples of approaches for monophonic separation. NMF models (top) decompose inputs via trained dictionaries; deep clustering (bottom left) projects T-F points to a latent space where sources cluster separately; discriminative separation (bottom right) predicts masking functions directly from the input.*

## Applications Survey

The paper does not perform a head-to-head benchmark; instead it surveys, per subfield, the dominant line of evolution and the point at which deep learning became mainstream. The table below condenses the per-domain narrative.

| Subfield | Pre-2000 baseline | Key 21st-century advance | Deep-learning status (as of 2023) |
|---|---|---|---|
| Audio coding | MPEG-1/2 | AAC, HE-AAC, BWE/SBR, MPEG Surround/SAOC/USAC/H | (less affected; signal-model-driven) |
| RIR modeling | Image method, Polack | PyRoomAcoustics, gpuRIR, `dEchorate`, GAN-RIR | GAN-based RIR generation emerging |
| Localization | GCC, SRP-PHAT | MUSIC/ESPRIT in SH domain, Bayesian trackers, Acoustic SLAM | DNN-based DOA growing |
| Binaural/soundfield rendering | HRTF, Ambisonics (1973), WFS (1980s) | Parametric SH reproduction, room equalization | Limited |
| AEC | RLS, affine projection, double-talk | Nonlinear AEC, MIMO/wave-domain, combined postfilters | DNN step-size and residual-echo models |
| Feedback / ANC | Adaptive feedback cancellation, FxLMS | Multizone bright/dark rendering, ~10 dB hearing-aid gain | Emerging |
| Dereverberation | Few algorithms | WPE (MCLP), REVERB Challenge, subspace/LS | DNN spectral mapping; hybrid expected |
| Noise suppression | Spectral subtraction, Ephraim–Malah | Phase-aware enhancement, cIRM | Dominant (mask estimation) |
| Beamforming | Free-field MVDR | RTF-based MVDR/MWF/LCMV, binaural, distributed WASN | Three DNN trends (block-estim / weight-estim / end-to-end) |
| Determined separation | ICA | Freq-domain ICA, TRINICON, IVA, ILRMA, MVAE | MVAE and DNN-augmented IVA |
| Monophonic separation | NMF | W-disjoint orthogonality, deep clustering, PIT | Dominant (discriminative masking) |
| Objective evaluation | PESQ, PEAQ | POLQA, VISQoL, STOI/MBSTOI, SI-SDR/SAR/SIR | Trained perceptual scorers; crowdsourcing |
| MIR | Spectral features | Self-supervised pitch, DDSP, hybrid generative models | Early and continued adopter (Fig. 4) |
| DCASE | CASA (Bregman) | Weakly-supervised, mean-teacher, prototypical nets, Specaugment | Mainstream since 2018 (Fig. 5) |

![[raw/papers/richard-2023-audio-signal-processing-21st-century/figures/cd05f3c9a2ea36d70339a60eec098edd4cc6b23b9d61c5826aab9d3193fffb20.jpg|MIR as an early adopter of deep neural networks]]
*Figure 4: Music Information Retrieval — a rather early adoption of deep neural networks.*

![[raw/papers/richard-2023-audio-signal-processing-21st-century/figures/3470689c548fd20c51b5a32f477c8c64d638b0214fcb5535c68525f7d3e766d4.jpg|DCASE evolution from perceptual auditory analysis to large-scale deep learning]]
*Figure 5: DCASE — from perceptual auditory sound analysis to large-scale deep-learning algorithms.*

## Key Contributions

1. **A consolidated 25-year retrospective** of TC-AASP, explicitly extending the 1997 Kahrs et al. SPS-50th-anniversary survey [1] and framing the field's evolution around a paradigm shift to data-driven methods.
2. **A two-axis taxonomy** (advances-and-highlights by problem domain; emerging topics) that maps the AASP landscape from coding and room modeling through enhancement, separation, evaluation, MIR, and DCASE.
3. **A community-challenge catalog** (ACE, REVERB, LOCATA, SiSEC, AEC Challenge, DNS, DCASE) and benchmark/workshop history (IWAENC since 1989; DCASE workshop 2016→, submissions 84→470 in 2016→2020; DCASE = 23.5% of ICASSP audio submissions in 2022).
4. **Future-direction agenda**: hybrid model-based deep architectures (differentiable signal models / DDSP for frugal, interpretable, sustainable systems); federated/collaborative on-edge learning under privacy, heterogeneity, and communication constraints; and multimodal processing (audio-visual speaker localization/separation; EEG-informed speech separation).

## Limitations and Caveats

- **No quantitative benchmarking.** The paper is a narrative retrospective; per-domain "best variant" recommendations are qualitative, not backed by unified comparative experiments. Where performance claims appear (e.g., "usable gains risen by as much as 10 dB", "MPEG Surround ≈ AAC quality at 1/3 bitrate"), they are cited from individual prior works, not re-measured.
- **Coverage bounded by TC-AASP scope and a 2023 cutoff.** Pre-1997 history is delegated to [1]; very recent efficient variants published after the cutoff are out of scope.
- **Uneven depth across subfields.** Some areas (coding, enhancement, separation) get detailed methodological treatment; others (consumer devices, fast internet) are brief contextual sketches.
- **Survey-only concept mentions.** Many named algorithms (WPE, FDN, TRINICON, ILRMA, MVAE, BWE/SBR, Ambisonics, W-disjoint orthogonality, DDSP) are surveyed rather than contributed; per the wiki's review-paper concept threshold they are linked as plain text or to existing pages rather than spawning new stub pages.
- **Author-perspective bias.** Authored by seven TC-AASP members, the retrospective naturally reflects the committee's framing and the authors' own subfields (each author is a leading figure in one or more surveyed areas).

## Related Concepts

- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]]
- [[concepts/acoustic-feedback|Acoustic Feedback]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/dereverberation|Dereverberation]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/lcmv-beamformer|LCMV Beamformer]]
- [[concepts/multi-channel-wiener-filter|Multichannel Wiener Filter]]
- [[concepts/relative-transfer-function|Relative Transfer Function]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/deep-clustering-speech-separation|Deep Clustering Speech Separation]]
- [[concepts/permutation-invariant-training|Permutation Invariant Training]]
- [[concepts/ideal-binary-mask|Ideal Binary Mask]]
- [[concepts/ideal-ratio-mask|Ideal Ratio Mask]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask]]
- [[concepts/coherent-to-diffuse-power-ratio|Coherent-to-Diffuse Power Ratio]]
- [[concepts/spatial-coherence|Spatial Coherence]]
- [[concepts/image-source-method|Image Source Method]]
- [[concepts/room-impulse-response|Room Impulse Response]]
- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/spherical-harmonic-transform|Spherical Harmonic Transform]]
- [[concepts/direction-of-arrival-estimation|Direction of Arrival Estimation]]
- [[concepts/acoustic-scene-classification|Acoustic Scene Classification]]
- [[concepts/mclp|Multichannel Linear Prediction (MCLP)]]
- [[concepts/pesq|PESQ]]
- [[concepts/kalman-filter|Kalman Filter]]
- [[concepts/gaussian-mixture-model|Gaussian Mixture Model]]
- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]

## Related Sources

- [[sources/vanwaterschoot-2011-fifty-years-afc|van Waterschoot & Moonen 2011: Fifty Years of Acoustic Feedback Control]] — cited as [28]; canonical AFC survey that this retrospective references for the feedback-control subfield.
- [[sources/wang-2018-supervised-speech-separation-deep-learning-overview|Wang & Chen 2018: Supervised Speech Separation Based on Deep Learning: An Overview]] — cited as [38]; the survey's reference for DNN-based separation and masking (IBM/IRM/cIRM).
- [[sources/guo-2023-iva-survey|Guo, Luo & Li 2023: IVA Survey]] — complementary IVA-focused survey aligning with the determined-separation subsection.
- [[sources/zheng-2023-survey-frequency-domain-speech-enhancement|Zheng et al. 2023: Sixty Years of Frequency-Domain Monaural Speech Enhancement]] — complementary monaural-enhancement survey extending the noise-suppression subsection.
