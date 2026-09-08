---
type: source
created: 2026-09-08
updated: 2026-09-08
sources:
  - raw/papers/xiao-2023-spatially-selective-anc/full-text.md
  - https://doi.org/10.1121/10.0019336
  - zotero://select/items/0_5AJNTV5T
tags:
  - active-noise-control
  - spatially-selective-anc
  - hybrid-anc
  - beamforming
  - relative-transfer-function
  - hearables
  - ar-glasses
  - robust-control
  - speech-preserving-anc
---

# Xiao, Xu & Zhao 2023: Spatially Selective Active Noise Control Systems

**Authors**: [[entities/tong-xiao|Tong Xiao]], [[entities/buye-xu|Buye Xu]], [[entities/chuming-zhao|Chuming Zhao]]
**Institutions**: Centre for Audio, Acoustics and Vibration, University of Technology Sydney, Australia; Meta Reality Labs Research, Redmond, WA, USA (work conducted during the first author's internship)
**Type**: Journal article
**Published**: Journal of the Acoustical Society of America 153(5), May 2023, pp. 2733–2744
**DOI**: [10.1121/10.0019336](https://doi.org/10.1121/10.0019336)
**Zotero**: [5AJNTV5T](zotero://select/items/0_5AJNTV5T)

---

## Summary

This is the foundational paper on **spatially selective active noise control (SSANC)**. Instead of the state-of-the-art approach of canceling all sound and then reconstructing the desired sound, the proposed multi-channel hybrid ANC system imposes a Frost-type **linear spatial constraint** (built from relative impulse responses, ReIRs) on the hybrid ANC cost function, so that sound from a desired direction is **physically preserved** ($e_s(n) = s(n)$) while noise from undesired directions is minimized. On a six-microphone AR-glasses array on KEMAR, the system improved SNR from −13.9 to 15.2 dB (NR 29.1 dB) with speech distortion at −25.1 dB, used only ~2% of the secondary-source energy of reconstruct-based systems, and preserved natural binaural localization cues without any reconstruction.

## Problem Formulation

Conventional ANC maximizes sound reduction regardless of incident direction. When desired sound is present, existing systems (Serizel et al. 2010; Dalga & Doclo 2011; Patel et al. 2020) cancel noise **and** desired sound, then reconstruct and reproduce the desired sound. This causes three problems:

1. **Control effort** — the secondary source must cancel both noise and desired sound, then re-reproduce the desired sound.
2. **ANC performance** — non-stationary desired sounds (speech, music) drive the adaptive controller to sub-optimal states, degrading noise attenuation.
3. **Distortion** — reconstruction introduces latency, undesired frequency shaping, and binaural-cue distortion for ear-level devices.

The paper asks: *can the system control only the noise but not the desired sound?* Building on prior work (Xu & Miller 2019), the answer is a spatially constrained hybrid ANC system.

### Signal Model

A hybrid ANC system with $K$ microphones (one error microphone, the binaural microphone #6 of an AR-glasses array) and one secondary source. The disturbance at the error microphone with ANC disabled is $d(n) = s(n) + v(n)$ (desired + noise). The error signal in matrix form:

$$e(n) = d(n) + \mathbf{w}^T \mathbf{G}^T \mathbf{x}(n) = \mathbf{u}^T \mathbf{x}(n), \qquad \mathbf{u} = \tilde{\mathbf{d}} + \mathbf{Gw},$$

where $\mathbf{w} \in \mathbb{R}^{KL}$ stacks the $K$ control filters of length $L$, $\mathbf{G}$ is the block-Toeplitz secondary-path matrix of the estimate $\hat{\mathbf{g}} = \mathbf{g}$, $\mathbf{x}(n)$ stacks the $K-1$ reference signals and the estimated disturbance $\hat{d}(n)$ (recovered as $\hat{d}(n+1) = e(n) - \hat{\mathbf{g}}^T\mathbf{y}(n)$ — the feedback part of the hybrid architecture), and $\tilde{\mathbf{d}} = [\mathbf{0}^T \dots \mathbf{0}^T\ \mathbf{d}^T]^T$ selects the disturbance channel.

### Spatial Constraint

From the Frost algorithm (linearly constrained adaptive array processing), the spatial constraint for a single desired source is

$$\mathbf{H}^T \mathbf{u} = \mathbf{f},$$

where $\mathbf{H} = [\mathbf{H}_1\ \mathbf{H}_2 \dots \mathbf{H}_K]^T$ contains the Toeplitz matrices of the **relative impulse responses (ReIRs)** $\mathbf{h}_k$ between the $k$th microphone and a chosen reference microphone (the one closest to the desired source), and the constraint vector

$$\mathbf{f} = \mathbf{h}_K$$

describes the frequency response of the signal from the desired direction at the error microphone. With ANC enabled the error signal decomposes as $e(n) = e_s(n) + v_{\mathrm{ANC}}(n)$; the constraint makes $e_s(n) = s(n)$ — the desired physical sound is left **unaltered**, not reconstructed.

### Cost Function

$$\min_{\mathbf{w}} \; \mathbb{E}\{e^2(n)\} \quad \text{such that} \quad \mathbf{H}^T(\tilde{\mathbf{d}} + \mathbf{Gw}) = \mathbf{f}.$$

![[raw/papers/xiao-2023-spatially-selective-anc/figures/fig01.png|Concept diagram of a spatially selective ANC system]]

*Figure 1: Concept diagram — the secondary source controls noise from undesired directions while the desired sound from one direction is preserved at the error microphone.*

## Methodology

### Optimal Solution

Solving via Lagrange multipliers (Appendix A) and re-writing with $\mathbf{r}(n) = \mathbf{G}^T\mathbf{x}(n)$, $\mathbf{U}_{rr} = \mathbb{E}\{\mathbf{r}(n)\mathbf{r}^T(n)\} + \beta\mathbf{I}$, $\boldsymbol{\phi}_{rd} = \mathbb{E}\{\mathbf{r}(n)d(n)\}$:

$$\mathbf{w}_{\mathrm{opt}} = -\mathbf{U}_{rr}^{-1}\boldsymbol{\phi}_{rd} + \mathbf{U}_{rr}^{-1}\mathbf{G}^T\mathbf{H}\big(\mathbf{H}^T\mathbf{G}\mathbf{U}_{rr}^{-1}\mathbf{G}^T\mathbf{H} + \theta\mathbf{I}\big)^{-1}\Big(\mathbf{f} - \big(\mathbf{H}^T\tilde{\mathbf{d}} - \mathbf{H}^T\mathbf{G}\mathbf{U}_{rr}^{-1}\boldsymbol{\phi}_{rd}\big)\Big)$$

Three interpretable terms:

1. **Wiener solution** of a hybrid ANC system controlling all observable sounds;
2. **Frost beamformer-like term** due to the spatial constraint, with the secondary-path matrix $\mathbf{G}$ added because of the physical constraint of the ANC system;
3. **Coupling term** between the two subsystems.

Because $\mathbf{G}$ is rank-deficient (secondary-path delays), a Tikhonov regularization $\theta$ is applied to $\mathbf{H}^T\mathbf{G}\mathbf{U}_{rr}^{-1}\mathbf{G}^T\mathbf{H}$; the factor $\beta$ on $\mathbf{U}_{rr}$ acts as a leaky-algorithm / white-noise-gain-style penalty $\|\mathbf{w}\|^2$ for robustness.

### Adaptive Solution

An LMS-type adaptive algorithm (Appendix B) with the constraint folded into a projection $\mathbf{P}$ and offset $\mathbf{q}$:

$$\mathbf{w}(n+1) = \mathbf{P}\big(\mathbf{w}(n) - \lambda \mathbf{G}^T\mathbf{x}(n)e(n)\big) + \mathbf{q}, \qquad \mathbf{w}(0) = \mathbf{q},$$

$$\mathbf{P} = \mathbf{I} - \mathbf{G}^T\mathbf{H}\big(\mathbf{H}^T\mathbf{G}\mathbf{G}^T\mathbf{H} + \epsilon\mathbf{I}\big)^{-1}\mathbf{H}^T\mathbf{G}, \qquad \mathbf{q} = \mathbf{G}^T\mathbf{H}\big(\mathbf{H}^T\mathbf{G}\mathbf{G}^T\mathbf{H} + \epsilon\mathbf{I}\big)^{-1}\big(\mathbf{f} - \mathbf{H}^T\tilde{\mathbf{d}}\big).$$

Without the constraint ($\mathbf{P} = \mathbf{I}$, $\mathbf{q} = \mathbf{0}$) this reduces to the traditional adaptive hybrid ANC solution. The solution couples the adaptive ANC subsystem with the adaptive Frost algorithm.

![[raw/papers/xiao-2023-spatially-selective-anc/figures/fig02.png|Block diagram of the proposed adaptive spatially selective ANC system]]

*Figure 2: Block diagram — the adaptive hybrid ANC algorithm is spatially constrained.*

### Spectral Weighting

When spatial filtering alone is insufficient (limited channels / filter lengths), a minimum-phase spectral weighting filter replaces the constraint: $\mathbf{F} = \mathbf{S}\mathbf{h}_K$ (Toeplitz $\mathbf{S}$), attenuating frequencies outside the range of interest. Non-minimum-phase filters are avoided since they delay the error signal. The attenuated band must barely overlap the desired signal; otherwise an NR-vs-distortion trade-off arises.

### Robustness: Eigenvalue-Based Regularization

Four robustness aspects: (1) ANC subsystem (leaky algorithm), (2) beamforming subsystem (diagonal loading / white-noise-gain constraint), (3) ANC on beamforming (secondary-path delays → rank deficiency, solved by $\theta$ and $\epsilon$), (4) beamforming on ANC (signal mismatches / sensor noise). Instead of the classical beamforming rule $\beta = \theta = 10\sigma_n^2$ (sensor-noise power), which over-regulates at high noise and under-regulates at low noise, the paper chooses

$$\beta = \lambda^1_{\max}/10\,000, \qquad \theta = \lambda^2_{\max}/10\,000,$$

where $\lambda^1_{\max}$, $\lambda^2_{\max}$ are the largest eigenvalues of $\mathbb{E}\{\mathbf{r}(n)\mathbf{r}^T(n)\}$ and $\mathbf{H}^T\mathbf{G}\mathbf{U}_{rr}^{-1}\mathbf{G}^T\mathbf{H}$; ratios between 5 000 and 50 000 worked well.

## Experimental Setup

| Parameter | Value |
|:----------|:------|
| Device | Open-fitting AR glasses on KEMAR manikin (EasyCom dataset geometry) |
| Microphones | 6 total: #1–#4 frame (reference), #5/#6 binaural (error); right ear #6 evaluated |
| Desired signal | 20-s male speech at $\theta = 0°$ |
| Noise | Speech babble (NOISEX-92) at $\theta = 60°$ |
| A priori SNR | −13.2 dB (clean speech unintelligible when mixed) |
| Secondary path | COMSOL Multiphysics simulation, point source ~0.05 m above error mic |
| Sampling rate | 48 kHz |
| Filter length $L$ | 768 |
| Secondary-path delay | 10 samples (208.3 µs) |
| Step-size $\lambda$ | Variable step-size (VSS) LMS: $\lambda_{\max}=10^{-4}$, $\lambda_{\min}=8\times10^{-8}$, $\alpha=0.99998$, $\gamma=10^{-5}$, $\beta_{\mathrm{VSS}}=0.99999$ |
| Regularization $\epsilon$ | 0.0001 |
| Spectral weighting | Minimum-phase high-pass, 140 Hz cut-off |

**Metrics**: noise reduction $\mathrm{NR} = 10\log_{10}\big(\mathbb{E}\{v^2(n)\}/\mathbb{E}\{v^2_{\mathrm{ANC}}(n)\}\big)$ (higher better); speech distortion index $\mathrm{SDI} = 10\log_{10}\big(\mathbb{E}\{[s(n)-e_s(n)]^2\}/\mathbb{E}\{s^2(n)\}\big)$ (lower better). Speech/noise components in the error signal are decoupled by re-filtering with the recorded control-filter history.

![[raw/papers/xiao-2023-spatially-selective-anc/figures/fig03.png|KEMAR manikin with AR glasses and six-microphone array]]

*Figure 3: (a) Isometric and (b) top view of the KEMAR manikin with AR glasses (six-microphone array); (c) microphone setup.*

## Results

### Control Performance

Noise is attenuated within the first 2 s, leaving the desired speech in good agreement with the clean signal. Over the last 10 s:

- **SNR improved from −13.9 dB to 15.2 dB**;
- **NR = 29.1 dB**; **SDI = −25.1 dB** (above 100 Hz) — low enough to be inaudible;
- minor residual noise below 100 Hz; the system is mainly bound by the ANC subsystem.

![[raw/papers/xiao-2023-spatially-selective-anc/figures/fig05.png|Error signal with ANC enabled: waveform, spectrogram, spectra, decoupled components]]

*Figure 5: (a) Waveform and spectrogram of the error signal with ANC enabled; (b) spectra of noisy speech, clean speech, and total error signal; (c) decoupled speech and noise components (last 10 s).*

Without the spectral weighting filter, the error signal cannot be controlled below 100 Hz — the spatial constraint is band-limited by filter length, while the ANC subsystem alone reduces noise across the spectrum (Fig. 6 of the paper).

### Robustness to Sensor Noise

Gaussian white sensor noise added to microphones #1, #3, #4, #5, parameterized by the signal-to-sensor-noise ratio (SsNR) at microphone #5, using the optimal solution:

| SsNR | Rule $\beta=\theta=10\sigma_n^2$ | Rule $\beta=\lambda^1_{\max}/10^4$, $\theta=\lambda^2_{\max}/10^4$ |
|:-----|:--------------------------------|:------------------------------------------------|
| 30 dB | NR 41.1 dB, SDI −14.0 dB (under-regularized, speech distorted) | maintained |
| −30 dB | NR 6.1 dB, SDI −3.1 dB (over-regulated) | **NR 24.3 dB, SDI −22.5 dB** |

With eigenvalue-based regularization, performance is maintained even under disastrous perturbation (sensor noise 30 dB above the desired signal).

![[raw/papers/xiao-2023-spatially-selective-anc/figures/fig07.png|NR and SDI vs SsNR for two regularization rules]]

*Figure 7: (a) NR level and (b) SDI value vs SsNR. Blue squares: $\beta=\theta=10\sigma_n^2$. Red diamonds: $\beta=\lambda^1_{\max}/10^4$, $\theta=\lambda^2_{\max}/10^4$. Shaded areas: ratios 5 000–50 000.*

### Directivity

With the desired source fixed at 0° and pink noise placed around the horizontal plane:

- $\theta \in (30°, 150°)$: best NR, ≥20 dB; below 500 Hz >30 dB reduction;
- $\theta = 0°$: all signals maintained, including noise (by design);
- $\theta \in (150°, 300°)$: unsatisfactory — noise reaches the error microphone **before** the reference microphones, violating causality; only the feedback subsystem operates (~10 dB below 500 Hz); high frequencies slightly increased by the [[concepts/waterbed-effect|waterbed effect]].

An idealized circular eight-reference-microphone array with a center error microphone (Fig. 8b) can cancel noise from every direction except the desired one when causality is maintained — directivity is bound by ANC causality, which depends mainly on the array configuration.

![[raw/papers/xiao-2023-spatially-selective-anc/figures/fig08.png|Directivity plots of residual noise for two array configurations]]

*Figure 8: Directivity of residual noise at error microphone #6 for (a) the AR-glasses configuration and (b) an eight-microphone circular array with center error microphone.*

## Comparison with Existing Methods

All methods evaluated on the same six-microphone AR glasses, with hybrid ANC control and the Frost algorithm for consistency:

| Configuration | Description | Desired-signal path |
|:--------------|:------------|:--------------------|
| Partially coupled (Dalga & Doclo 2011; [[sources/serizel-2010-integrated-anc-nr-hearing-aids|Serizel et al. 2010]]) | MWF beamformer on mics #2/#4, output added to error signal | Reconstructed, 1 ms delay |
| Decoupled (Patel et al. 2020) | ANC on #1/#3 (with #5/#6), superdirective beamformer on #2/#4, output injected into secondary source | Reconstructed, 5 ms delay |
| **Proposed** | All six microphones shared by ANC and spatial constraint | **Physically preserved** |

### Control Effort

The secondary-source signals of the reconstruct-based configurations contain the desired speech; the proposed method's contains only the anti-noise. Relative secondary-source energy $\bar{E}_y$ (Eq. 17, referenced to the partially coupled configuration):

- At a priori SNR = 10 dB, the proposed method needs **only ~2% energy** while achieving a better NR than the partially coupled configuration;
- The decoupled configuration uses ~50% more energy than the partially coupled one (better NR, but the desired speech is directly injected into the secondary source).

![[raw/papers/xiao-2023-spatially-selective-anc/figures/fig09.png|Secondary source signals, energy consumption and NR for the three configurations]]

*Figure 9: (a) Secondary source signals at a priori SNR = 0 dB; (b) relative secondary-source energy consumption; (c) NR levels for different a priori SNRs.*

### Multiple Noise Sources

Five uncorrelated pink-noise sources at 60°, 90°, 120°, 300°, 330°:

- The proposed configuration achieves the **best NR** — it never needs to cancel the speech;
- The partially coupled configuration is limited by eigenvalue spread of the input correlation matrix (desired speech in the input limits the step-size): maximum stable step-size 0.00004 vs 0.00008 (decoupled);
- Reconstructed desired speech in the other two systems differs from the clean speech by roughly 6–10 dB across the spectrum, while the proposed system's difference above 140 Hz is essentially zero (below 140 Hz the difference stems from the spectral weighting filter).

![[raw/papers/xiao-2023-spatially-selective-anc/figures/fig10.png|Spectra comparison of the three configurations for multiple noise sources]]

*Figure 10: Spectra of noisy speech, clean speech, (a) overall error signals, (b) noise components, (c) speech-component differences for the three configurations (last 10 s).*

### Binaural Localization Cues and Latency

With the desired speech at 60° and noise at 0°: the reconstruct-based systems produce a **monaural** reconstruction at microphone #4 for both ears — binaural cues are lost unless a binaural beamformer is used (spectral agreement with the true ear signals only between 100 Hz and 2 kHz on the right side). The proposed system's speech components at both ears agree with the original clean speech in time and frequency — natural binaural localization cues are preserved because the physical sound wave is never altered.

## Key Contributions

1. **Spatially selective ANC formulation**: a Frost-type linear spatial constraint $\mathbf{H}^T\mathbf{u} = \mathbf{f}$ built from ReIRs imposed on the hybrid ANC cost function, so that only noise from undesired directions is minimized while the desired physical sound is preserved rather than reconstructed.
2. **Optimal and adaptive solutions**: closed-form solution decomposable into Wiener-ANC + Frost-beamformer + coupling terms, and a coupled adaptive algorithm with projection $\mathbf{P}$ and offset $\mathbf{q}$; regularization factors ($\beta$, $\theta$, $\epsilon$) handle the rank deficiency induced by secondary-path delays.
3. **Spectral weighting extension**: a minimum-phase filter on the constraint vector relaxes the spatial constraint outside the frequency range of interest when the array/filter length is limiting.
4. **Eigenvalue-based robust regularization**: choosing $\beta$, $\theta$ by the largest eigenvalue of the matrices to invert (ratio 5 000–50 000) instead of the sensor-noise-power rule $10\sigma_n^2$ maintains NR 24.3 dB / SDI −22.5 dB even at SsNR = −30 dB.
5. **Preserve-vs-reconstruct quantification**: on identical hardware, the proposed system uses ~2% of the secondary-source energy of reconstruct-based systems at SNR 10 dB, achieves the best NR under multi-source noise, and preserves binaural cues and zero latency without reconstruction.

## Remarks and Future Directions

- **Multiple desired sources**: multiple spatial constraints $\mathbf{H}^T_{s_1}\mathbf{u} = \mathbf{f}_{s_1}, \dots$ can be added (LCMV-style) or combined into one.
- **Same-direction desired sound and noise** (co-located sources or reverberation): requires further investigation, possibly blind source separation.
- **Open- vs closed-fitting devices**: open-fitting AR glasses allow full coupling (all microphones for both ANC and constraint); closed-fitting headphones may need partially coupled configurations to save computation (error microphones see highly attenuated disturbances).
- **Transducer limits**: miniaturized speakers benefit from the relaxed excursion limit (only noise is canceled); the simulation used an ideal point source to exclude this factor.
- **Acoustic feedback** from secondary sources to reference microphones is left for future work, as are non-ideal (reverberant) environments.

## Related Concepts

- [[concepts/spatially-selective-anc|Spatially Selective ANC]]
- [[concepts/hybrid-anc|Hybrid ANC]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/relative-transfer-function|Relative Transfer Function (RTF/ReIR)]]
- [[concepts/lcmv-beamformer|LCMV Beamformer]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/soft-constrained-anc|Soft-Constrained ANC]]
- [[concepts/speech-preserving-anc|Speech-Preserving ANC]]
- [[concepts/selective-anc|Selective ANC (filter selection)]]
- [[concepts/filtered-x-mwf|Filtered-x MWF (FxMWF)]]
- [[concepts/waterbed-effect|Waterbed Effect]]
- [[concepts/causality|Causality in ANC]]
- [[concepts/variable-step-size-lms|Variable Step-Size LMS]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/diagonal-loading|Diagonal Loading]]

## Related Sources

- [[sources/xiao-2026-robust-spatially-selective-anc|Xiao 2026: Robust Soft-Constrained SSANC for Hearables]] — successor paper (robust soft-constrained extension under secondary-path variations)
- [[sources/serizel-2010-integrated-anc-nr-hearing-aids|Serizel 2010: Integrated Active Noise Control and Noise Reduction in Hearing Aids]] — compared partially coupled method (FxMWF)
- [[sources/liebich-2018-doa-dependency-anc-headphones|Liebich 2018: DOA Dependency of ANC Headphones]] — spatial aspect of personal ANC performance
- [[sources/zhang-2014-causality-feedforward-anc-headset|Zhang 2014: Causality Study on a Feedforward ANC Headset]] — DOA-dependent causality in feedforward ANC

## Related Synthesis

- [[synthesis/anc-architecture-evolution|ANC Architecture Evolution]]
- [[synthesis/modern-headphone-anc-systems|Modern Headphone ANC Systems]]
