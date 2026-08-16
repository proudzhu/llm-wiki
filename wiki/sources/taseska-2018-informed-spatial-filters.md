---
type: source
created: 2026-08-16
updated: 2026-08-16
sources:
  - raw/papers/taseska-2018-informed-spatial-filters/full-text.md
  - https://open.fau.de/handle/openfau/9332
  - zotero://select/items/0_VQZTHIS3
tags:
  - thesis
  - speech-enhancement
  - informed-spatial-filtering
  - beamforming
  - mvdr
  - mwf
  - gsc
  - noise-psd-estimation
  - cdr
  - doa-estimation
  - blind-source-separation
  - source-tracking
  - spotforming
  - multi-array
  - sparsity-based
  - mcra
  - rtf-estimation
---

# Taseska 2018: Informed Spatial Filters for Speech Enhancement

**Author**: [[entities/maja-taseska|Maja Taseska]]
**Supervisor**: [[entities/emanuele-habets|Emanuël A. P. Habets]]
**Second Reviewer**: Reinhold Häb-Umbach
**Institution**: Friedrich-Alexander-Universität Erlangen-Nürnberg (FAU), International Audio Laboratories Erlangen
**Type**: PhD Dissertation
**Defended**: 27 November 2017
**Published**: 5 February 2018
**URL**: [FAU Open Access](https://open.fau.de/handle/openfau/9332)
**Zotero**: [VQZTHIS3](zotero://select/items/0_VQZTHIS3)

## Summary

This thesis develops the **Informed Spatial Filter (ISF)** paradigm as a unified framework for multi-microphone speech enhancement in dynamic, reverberant environments. The central idea: at each Short-Time Fourier Transform (STFT) time-frequency (TF) bin, a *narrowband signal detector* decides which source (desired speech, interferer, or noise) is dominant; that decision drives online estimation of the second-order statistics (PSD matrices) and propagation vectors, which are substituted into closed-form optimal filters (MVDR/MWF) or adaptive GSC structures that are re-computed per TF bin. The framework is instantiated across five applications — blind noise-PSD estimation, DOA-informed source extraction, informed GSC, acoustic spotforming, and sparsity-based BSS of static and moving sources — spanning both single-array and distributed-multi-array setups.

## Problem Formulation

$M$ microphones capture a mixture of a desired speaker, interfering speakers, and background noise in a reverberant enclosure. Under the Multiplicative Transfer Function (MTF) approximation, the STFT-domain signal vector is

$$
\mathbf{y}(t,k) = \sum_{j=1}^{J_t} \mathbf{s}_j(t,k) + \mathbf{v}(t,k) = \sum_{j=1}^{J_t} \mathbf{g}_{jm_{jt}}(t,k)\, S_{jm_{jt}}(t,k) + \mathbf{v}(t,k),
$$

where $\mathbf{g}_{jm}$ is the Relative Transfer Function (RTF) vector of source $j$ w.r.t. reference microphone $m$, and $\mathbf{v}$ is the noise vector. The desired-signal PSD matrix is rank-one, $\boldsymbol{\Phi}_{\mathbf{s}} = \mathbf{g}\,\Phi_S\,\mathbf{g}^{\mathrm{H}}$. The objective is to estimate the desired signal $S_m(t,k)$ at a reference microphone via a linear filter $\mathbf{w}(t,k)$.

**Key assumption — speech sparsity in the STFT domain**: with a suitably chosen time/frequency resolution (32–64 ms frames), each TF bin is dominated by *one* source. This permits per-bin detection and per-bin statistics updates.

The three competing hypotheses at each TF bin (Chapter 4 scenario) are:

$$
\mathcal{H}_s: \mathbf{y} \approx \mathbf{s} + \mathbf{v}, \quad \mathcal{H}_i: \mathbf{y} \approx \mathbf{i} + \mathbf{v}, \quad \mathcal{H}_v: \mathbf{y} \approx \mathbf{v}.
$$

![[raw/papers/taseska-2018-informed-spatial-filters/figures/b826ff60c2b418acccac13656b3f993356bc949fc465799640cb2847ce393348.jpg|General block diagram of an informed spatial filtering framework]]
*Figure 2.2: A general block diagram of an informed spatial filtering framework. A narrowband detector classifies each TF bin, the decision updates the desired/undesired PSD matrices and RTF vectors, and the optimal filter is re-computed per bin.*

## Methodology

All frameworks share a five-step structure: (i) extract a TF-dependent spatial feature, (ii) design a statistical model-based detector, (iii) associate each TF bin to the dominant signal, (iv) update PSD matrices and propagation vectors, (v) compute ISFs. Chapters 3–5 use a single microphone array; Chapters 6–8 require $\geq 2$ spatially separated arrays.

### Chapter 1 — Introduction

Surveys the scope of modern multi-microphone speech enhancement, organised by application: (1.1) single- and multichannel speech enhancement, tracing single-channel methods from spectral subtraction through Wiener/MMSE/subspace approaches; (1.2) multichannel noise reduction, emphasising that estimating the array propagation vector and the SOS of desired/undesired signals are the two sub-problems, with challenges in non-stationarity and online estimation; (1.3) speech enhancement with undesired speakers — DOA-based extraction and acoustic spotforming; (1.4) BSS, categorised into ICA-based, spatial-filtering-based, sparsity-based, and combined approaches; (1.5) source tracking for BSS. Section 1.6 states the thesis structure and lists 16 publications.

![[raw/papers/taseska-2018-informed-spatial-filters/figures/fa7a9c4603775d7d7c3a92625e85ffc3b0f59288e4c8d83fa438dbcab824ce3a.jpg|Illustration beamforming versus spotforming]]
*Figure 1.1: Illustration of beamforming versus spotforming. Beamforming extracts sources from a desired direction; spotforming extracts sources from a desired spatial region (spot).*

### Chapter 2 — Optimal Spatial Filters in Theory and Practice

Provides the theoretical foundation. §2.1 defines the STFT-domain signal model under the Multiplicative Transfer Function (MTF) approximation, where $\mathbf{s}_j(t,k) = \mathbf{h}_j(k)\,\tilde{S}_j(t,k)$. §2.2 defines the statistical model: speech PSD matrices are rank-one ($\boldsymbol{\Phi}_{\mathbf{s}} = \phi_S\,\mathbf{g}\mathbf{g}^{\mathrm{H}}$), and the Gaussian signal model yields the multichannel SPP. §2.3 covers fixed beamformers (DSB). §2.4 summarises optimal data-dependent filters — [[concepts/mvdr-beamformer|MVDR]] ($\mathbf{w} = \boldsymbol{\Phi}_{\mathbf{u}}^{-1}\mathbf{g} / (\mathbf{g}^{\mathrm{H}}\boldsymbol{\Phi}_{\mathbf{u}}^{-1}\mathbf{g})$), [[concepts/multi-channel-wiener-filter|MWF]], [[concepts/mpdr-beamformer|MPDR]] (uses $\boldsymbol{\Phi}_{\mathbf{y}}$ instead of $\boldsymbol{\Phi}_{\mathbf{u}}$), PMWF (with trade-off parameter $\mu$), and [[concepts/lcmv-beamformer|LCMV]]. §2.5 elaborates the ISF concept: the distinguishing feature is *continuous* estimation of PSD matrices and RTF vectors using narrowband detector outputs, yielding near-instantaneous adaptation.

### Chapter 3 — CDR-Controlled Noise PSD Matrix Estimation (single array)

Addresses blind speech extraction in non-stationary noise. The noise PSD matrix $\boldsymbol{\Phi}_{\mathbf{v}}(t,k)$ is the critical quantity — its accuracy directly determines extracted-signal quality.

**ML formulation (§3.3)**: The thesis formulates noise-PSD/SPP estimation as a Maximum Likelihood problem and shows the solution has the *same structure* as multichannel MCRA, with a specific a priori SAP $q_v$ and a specific recursive averaging parameter $\alpha_v$. However, the pure-ML solution is **not robust in non-stationary environments**: without additional control, noise-property changes are falsely detected as speech onsets, corrupting $\boldsymbol{\Phi}_{\mathbf{v}}$.

**CDR-based a priori SAP (§3.4)**: The [[concepts/coherent-to-diffuse-power-ratio|Coherent-to-Diffuse Ratio (CDR)]] — exploiting that desired speech is *coherent* across the array while background noise is approximately *diffuse* — is mapped via a sigmoid to an a priori SAP. This is compared against three state-of-the-art SAP estimators: SC-Cohen (single-channel SNR-based), MC-Souden (multichannel SNR-based), and ML. Additional control mechanisms increase robustness. The CDR-based SAP is far more robust to non-stationary noise-property changes, because spatial coherence is a more reliable presence cue than energy ratios when the noise floor shifts.

**ISF design (§3.5)**: The estimated $\boldsymbol{\Phi}_{\mathbf{v}}$ and a posteriori SPP drive informed MVDR and MWF filters. The SPP also serves as the PMWF trade-off parameter $\mu$, and a conditional MMSE (c-MMSE) filter is discussed.

![[raw/papers/taseska-2018-informed-spatial-filters/figures/331c9e25b8eab9b9d067a16f38ad5817bae18445f2a9ff7050db18ec155d1eb3.jpg|Informed spatial filtering with CDR-based noise PSD matrix estimation]]
*Figure 3.2: Informed spatial filtering with CDR-based noise PSD matrix estimation.*

### Chapter 4 — DOA Model-Based Source Extraction (single array)

When interferers are *other speakers* (non-stationary, similarly coherent to the desired source), the CDR-based detector from Chapter 3 is inapplicable — the spatial-coherence distinction between desired and undesired speech vanishes. This chapter assumes the desired source DOA is approximately known (semi-blind scenario), while interferer number/locations are unknown and time-varying.

**Signal model (§4.1)**: $\mathbf{y} = \mathbf{s} + \mathbf{i} + \mathbf{v}$, with three per-bin hypotheses $\mathcal{H}_s$ (desired dominant), $\mathcal{H}_i$ (interferer dominant), $\mathcal{H}_v$ (noise dominant). The undesired PSD matrix is $\boldsymbol{\Phi}_{\mathbf{u}} = \boldsymbol{\Phi}_{\mathbf{i}} + \boldsymbol{\Phi}_{\mathbf{v}}$.

**DOA estimators (§4.2)**: Two narrowband DOA estimators — based on instantaneous phase differences and cross-PSD phase differences — each computed per TF bin from inter-microphone phase.

**DOA model-based detector (§4.4)**: The likelihoods under each hypothesis are:
- $\mathcal{H}_s$: **von Mises distribution** centred at the known desired DOA $\theta_s$, concentration $\kappa$ (estimation uncertainty).
- $\mathcal{H}_i$: **notched distribution** suppressing the region around $\theta_s$ (an interferer is unlikely to share the desired DOA).
- $\mathcal{H}_v$: the Gaussian signal model from Chapter 3 detects noise-dominated bins; the [[concepts/coherent-to-diffuse-power-ratio|CDR]] controls model parameters.

Spectral information (signal energy) and CDR control the detector parameters. The desired RTF vector $\mathbf{g}$ is estimated via the principal eigenvector of $\boldsymbol{\Phi}_{\mathbf{s}}$ (updated during $\mathcal{H}_s$ bins), and $\boldsymbol{\Phi}_{\mathbf{u}}$ is updated during $\mathcal{H}_i \cup \mathcal{H}_v$ bins, for an informed MVDR filter.

![[raw/papers/taseska-2018-informed-spatial-filters/figures/466d1bdf8b2b8e351826f7ebfd2cdb598907a70dba0cdbdbba0a8cc7973d6737.jpg|Main processing blocks of the DOA-informed spatial filtering framework]]
*Figure 4.4: Main processing blocks of the DOA-informed spatial filtering framework.*

### Chapter 5 — Informed GSC (single array)

Reformulates the Chapter 4 framework as a [[concepts/gsc-beamformer|General Sidelobe Canceller (GSC)]] with bin-wise adaptation control. The DOA model-based detector controls *when* each component updates:

- **Fixed Beamformer (FBF)**: $\mathbf{w}_{\mathrm{fbf}} = \mathbf{g}_1 / \|\mathbf{g}_1\|^2$, updated using the RTF estimate during $\mathcal{H}_s$ bins.
- **Blocking Matrix (BM)**: RTF-based construction (Gannot et al.), $\mathbf{g}_1^{\mathrm{H}}\mathbf{B} = \mathbf{0}$, updated during $\mathcal{H}_s$ bins.
- **Noise Canceller (NC)**: updated **only during desired-absent bins** ($\mathcal{H}_i \cup \mathcal{H}_v$), using $\boldsymbol{\Phi}_{\mathbf{u}}$ rather than $\boldsymbol{\Phi}_{\mathbf{y}}$ — the key to avoiding signal cancellation from RTF mismatch.

Three GSC implementations are evaluated: **GSC-RLS** (recursive least squares NC, quadratic complexity), **GSC-NLMS** (normalised LMS NC, linear complexity), and **R-GSC** (robust GSC with anechoic-RTF FBF and adaptive BM/NC). The R-GSC offers comparable performance to GSC-RLS at lower complexity. Conclusion: GSC-NLMS and R-GSC, with the DOA-based detector, offer an efficient practical solution; the marginal MVDR advantage does not justify its quadratic complexity.

### Chapter 6 — Acoustic Spotforming (multiple arrays)

Introduces fully data-dependent acoustic spotforming — extracting signals from a user-defined Spot of Interest (SOI), a 2D spatial region, rather than a direction. Requires $\geq 2$ spatially separated arrays (known geometry/location/orientation, synchronised, central processor).

**Narrowband position estimation (§6.4.1)**: Per-array narrowband DOAs are triangulated to obtain a 2D position estimate $\hat{\mathbf{r}}_{tk}$ at each TF bin. Two DOA vectors intersect to provide a position only if their inner product is positive — inherently discarding many outliers.

**Spot signal detector (§6.4)**: A Gaussian model for $\hat{\mathbf{r}}_{tk}$ (mean at cluster centre, covariance from estimation noise) yields the likelihood under "spot signal dominant" vs. "undesired dominant"; the Gaussian signal model provides the SPP for noise detection. A minimum Bayes risk decision rule (with costs $C_{su}, C_{us}$ for false positives/negatives) classifies each bin.

**Rank-one MVDR spotformer (§6.3)**: Due to speech sparsity, small spot size, and recursive temporal averaging, the spot-signal PSD matrix is approximately **rank-one** — even with multiple sources in the SOI. This enables an MVDR spotformer with a *single* time-varying constraint, unlike fixed LCMV-based spotformers that need multiple eigenvector constraints across the SOI (sacrificing degrees of freedom). A **projection-based RTF estimator** handles multi-source SOIs by reducing distortion vs. the rank-one-model RTF estimator. Multi-array spotforming improves spatial selectivity vs. single-array, at the cost of slightly larger spot-signal distortion.

### Chapter 7 — EM-Based BSS of Static Sources (multiple arrays)

Addresses BSS of an *unknown* number of static sources using the multi-array setup from Chapter 6.

**Feature choice (§7.3)**: Narrowband position estimates (triangulated DOAs) serve as clustering features. When a source is active, its narrowband positions form a cluster around its location — an intuitive, low-dimensional feature enabling fast clustering and meaningful number-of-source estimation.

**EM with joint number-of-source detection (§7.3)**: An EM variant models the position-feature density as a Gaussian mixture (one component per source). The number of sources is estimated *from the data* by a model-order selection mechanism within EM iterations, rather than assumed known. Only a few EM iterations and a few seconds of unlabelled training data suffice.

**Speech presence uncertainty (§7.2–7.3)**: The Gaussian model-based SPP (from Chapter 3) models speech presence uncertainty — noisy TF bins are detected and excluded from clustering and from updating separation-filter look directions. This is a distinct approach vs. adding a noise likelihood component or using energy-based VADs.

**ISF design for BSS (§7.4)**: TF masks (posterior source-index probabilities $p(Z_{tk}=j)$) update each source's PSD matrix. For each source $j$, the desired PSD matrix is $\boldsymbol{\Phi}_{\mathbf{s}_j}$ (rank-one via RTF), and the undesired PSD matrix is the sum of all *other* sources' PSD matrices plus the noise PSD matrix. Informed MVDR or MWF filters extract each source. Incorporating the SDR-based SPP provides simultaneous noise PSD matrix estimation and noise reduction.

### Chapter 8 — Sparsity-Based Source Tracking & BSS of Moving Sources (multiple arrays)

Extends Chapter 7 to time-varying numbers of moving sources (1–2 m/s). Online clustering (sliding-window EM) is sub-optimal for moving sources; instead, an **approximate Bayesian multi-source tracker** is proposed.

**Signal model (§8.1)**: Same as Ch 7 but $J_t$ (number of sources) is time-varying, and the reference microphone $m_{jt}$ per source is time-varying (nearest array). The RTF vector $\mathbf{g}_{jm_{jt}}$ is slowly time-varying across neighbouring frames (a source moves only 3.2–6.4 cm per 64 ms frame at 1–2 m/s), justifying the rank-one PSD matrix assumption.

**Augmented measurement model (§8.2)**: Each TF bin provides $\mathbf{o}_{tk} = \{\hat{\mathbf{r}}_{tk}, \mathbf{y}(t,k)\}$ — the narrowband position estimate *and* the signal vector. The position follows a Gaussian (clutter model: uniform over the room for noise-dominated bins), and the signal vector follows the Gaussian signal model for SPP. Position and signal are assumed independent, so the likelihood factorises. This **multiple-measurements-per-source-per-frame** model is required because the same source can be dominant at different frequency bins — invalidating JPDA's single-measurement-per-source assumption.

**Tracker (§8.3)**: Tracking is formulated as a **missing-data problem** — the dominant-source labels $Z_{tk}$ are hidden. An EM-style scheme estimates the source states (positions $\mathbf{x}_t^j$) and the measurement-noise covariances (source-dependent, time-varying). The data-association probabilities $p(Z_{tk} \mid \mathcal{V}_{1:t})$ *are* the TF masks. The tracker relates to JPDA (shares Gaussian-plus-clutter model, but handles multiple measurements per source) and PMHT (shares soft associations, but is consistent with the narrowband model).

**Track management (§8.4)**: Source detection initializes new tracks when measurement clusters persistently fail to associate; source removal deletes tracks whose association probabilities decay below a threshold. The Markovian motion model ensures consistent source association across time frames, and the approach avoids the frequency-permutation problem of convolutive BSS.

## Experimental Setup

| Aspect | Configuration |
|--------|---------------|
| **STFT** | Frame length 64 ms (typical); analysis window with zero-padding; $K/2+1$ bins processed |
| **Arrays** | Ch 3–5: single array; Ch 6–8: $\geq 2$ spatially separated arrays (known locations/orientations, synchronised, central processor) |
| **Reverberation** | $T_{60} \in \{0.2, 0.4\}$ s (simulated); also real measurements (Ch 8) |
| **Noise** | White/stationary and modulated/babble; SNR $\in \{3, 6, 7, 10\}$ dB |
| **Interferers** | Up to 4 concurrent speakers (Ch 7); moving sources 1–2 m/s (Ch 8) |
| **Baselines** | DSB, fixed MVDR, MPDR, multichannel MCRA (SC-Cohen, MC-Souden, ML), NOSET (DOA-based BSS), IVA-based BSS |
| **Filters** | Informed MVDR, MWF, PMWF, c-MMSE; informed GSC (RLS NC) |
| **Metrics** | iSNR/iSIR, oSNR/oSIR, $\Delta$SNR/$\Delta$SIR, Speech Distortion index $\nu_{\mathrm{sd}}$, PESQ, STOI, FSD (noise-PSD estimation error), FPR/FNR (detector ROC) |
| **Segmentation** | 30 ms non-overlapping segments; iSNR/iSIR averaged over segments in $[-40, 40]$ dB |

## Results

- **Noise PSD estimation (Ch 3)**: CDR-based a priori SAP yields more accurate $\boldsymbol{\Phi}_{\mathbf{v}}$ estimates and better noise tracking in non-stationary conditions than single-channel and multichannel SNR-based SAPs (SC-Cohen, MC-Souden, ML). Consistent improvements in $\nu_{\mathrm{sd}}$, segmental noise reduction, PESQ, and STOI at the ISF outputs.
- **DOA-informed extraction (Ch 4)**: The DOA model-based detector is robust to non-stationary interferers where the Gaussian-model detector fails; ROC curves and objective quality confirm superiority over DSB and MPDR (which suffers severe distortion from anechoic-RTF mismatch).
- **Informed GSC (Ch 5)**: RLS-based informed GSCs match closed-form informed MVDR performance without notable loss — validating the GSC as an efficient practical alternative.
- **Spotforming (Ch 6)**: Position-based detector operates at very low false-positive rates while detecting sufficient spot-signal TF bins; the spotformer adapts near-instantaneously to moving sources and outperforms fixed spotformers when interferer count/locations change.
- **BSS of static sources (Ch 7)**: Robust number-of-source detection and clustering with few EM iterations and few seconds of unlabelled data, in scenarios up to 4 concurrent sources; good separation quality even in adverse multi-talk. Incorporating SDR-based SPP provides simultaneous noise reduction.
- **BSS of moving sources (Ch 8)**: The Bayesian tracker's data-association probabilities provide accurate TF masks; competitive with state-of-the-art sparsity-based and IVA-based BSS on both simulated and real measurements, with efficient track management for appearing/disappearing sources.
- **Gap identified**: A "large gap" remains between ISFs using *oracle* TF masks and those using *estimated* masks — motivating integration of spectral features and DNN-based mask estimation (future work).

## Key Contributions

1. **ML formulation of multichannel noise-PSD/SPP estimation** (Ch 3) — shows equivalence to multichannel MCRA, and that the pure-ML solution needs additional control; proposes a CDR-based a priori SAP for robust non-stationary noise tracking.
2. **DOA model-based detector** (Ch 4) — a narrowband DOA-likelihood detector (von Mises / notched) for semi-blind source extraction in the presence of competing talkers, robust where Gaussian-model detectors fail.
3. **Informed GSC with bin-wise adaptation control** (Ch 5) — recursive (RLS) GSC implementations controlled by the DOA model-based detector, matching informed-MVDR quality at lower complexity.
4. **Data-dependent acoustic spotforming** (Ch 6) — position-based spot-signal detection and rank-one MVDR spotforming using distributed arrays, adapting instantaneously to changing conditions.
5. **EM-based joint number-of-source detection and clustering for BSS** (Ch 7) — narrowband position features with Gaussian-model SPP for speech presence uncertainty; few iterations, robust up to 4 sources.
6. **Bayesian multi-source tracker for BSS of moving sources** (Ch 8) — narrowband augmented measurement model (position + signal vector) where data-association probabilities yield TF masks; relates to JPDA/PMHT with multi-measurement-per-source model; includes track management.

## Related Concepts

- [[concepts/informed-spatial-filter|Informed Spatial Filter (ISF)]] — the unifying paradigm of this thesis
- [[concepts/acoustic-spotforming|Acoustic Spotforming]] — introduced in Ch 6
- [[concepts/doa-informed-source-extraction|DOA-Informed Source Extraction]] — Ch 4 framework
- [[concepts/multichannel-mcra|Multichannel MCRA]] — Ch 3 ML formulation
- [[concepts/informed-gsc|Informed GSC]] — Ch 5 adaptive implementation
- [[concepts/tf-mask-estimation|TF Mask Estimation]] — central to Ch 7–8 BSS
- [[concepts/sparsity-based-source-tracking|Sparsity-Based Source Tracking]] — Ch 8
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/multi-channel-wiener-filter|Multichannel Wiener Filter (MWF)]]
- [[concepts/gsc-beamformer|General Sidelobe Canceller (GSC)]]
- [[concepts/coherent-to-diffuse-power-ratio|Coherent-to-Diffuse Power Ratio (CDR)]]
- [[concepts/relative-transfer-function|Relative Transfer Function (RTF)]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/voice-activity-detection|Voice Activity Detection]]

## Related Synthesis

- This thesis contributes the ISF paradigm as a unifying thread across noise reduction, interference reduction, and BSS; see [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] for the broader landscape.
