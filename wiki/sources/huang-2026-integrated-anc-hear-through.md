---
type: source
created: 2026-11-08
updated: 2026-11-08
sources:
  - raw/papers/huang-2026-integrated-anc-hear-through/full-text.md
  - https://doi.org/10.1109/TCE.2026.3749926
  - zotero://select/items/0_RG5W628U
tags:
  - active-noise-control
  - hear-through
  - transparency-mode
  - feedforward-anc
  - speech-clarity
  - audio-processing
  - model-order-reduction
  - in-ear-headphones
  - fxlms
  - fixed-filter-anc
---

# Huang, Chang & Kuo 2026: Integrated Active Noise Control and Hear-Through for Speech Clarity Under Low-Frequency Ambient Noise

**Authors**: [[entities/chong-rui-huang|Chong-Rui Huang]], [[entities/cheng-yuan-chang|Cheng-Yuan Chang]], [[entities/sen-m-kuo|Sen M. Kuo]]
**Institutions**: Department of Electrical Engineering, Chung Yuan Christian University, Taoyuan, Taiwan
**Venue**: IEEE Transactions on Consumer Electronics, 2026
**Type**: Journal article
**DOI**: [10.1109/TCE.2026.3749926](https://doi.org/10.1109/TCE.2026.3749926)
**Zotero**: [RG5W628U](zotero://select/items/0_RG5W628U)
**Audio demo**: [doi.org/10.21227/nf6k-nv50](https://doi.org/10.21227/nf6k-nv50)

## Summary

This paper proposes an acoustic equalization system (AES) for in-ear headphones that integrates feedforward ANC and hear-through (HT) within a single control framework via frequency-band allocation, instead of treating them as mutually exclusive operating modes. A feedforward ANC filter (offline-trained with FxLMS, then reduced from a 3000-tap FIR to a 50th-order IIR via balanced truncation) suppresses low-frequency noise below an adjustable crossover, while an HT filter compensates passive isolation above it; two user gains ($g_a$, $g_h$) and the crossover frequency $f_L$ tune the noise-reduction vs. awareness trade-off. On a real-time TMS320C6713 DSP platform validated on a KEMAR, the ANC+HT mode achieves the highest SRMR_norm score (0.974, exceeding even open-ear speech-in-noise at 0.878) and the highest subjective speech-clarity rating (0.88 vs. 0.60 for HT alone, Friedman $\chi^2(3)=69.66$, $p<0.001$) among headphone conditions.

## Problem Formulation

Commercial headphones offer ANC and hear-through as distinct, mutually exclusive modes. In low-frequency-noise environments (e.g., aircraft cabins), the HT mode "restores ambient sound perception but leaves low-frequency noise largely unattenuated", degrading speech clarity — while the ANC mode attenuates low-frequency noise but suppresses speech-relevant external components as well. The goal is a unified ANC/HT controller for compact in-ear headphones that jointly: (1) suppresses low-frequency noise, (2) preserves speech-relevant ambient sound, and (3) provides user-adjustable control — under the stringent causality constraints of the short reference-mic-to-loudspeaker path.

The signal model (Fig. 1): ambient sound $x(t) = s(t) + n(t)$ (desired sound + low-frequency noise) reaches the eardrum under the open-ear condition as $\hat{d}(t) = \hat{s}(t) + \hat{n}(t)$, while passive isolation of the in-ear headphone yields residual $d(t) = s'(t) + n'(t)$ with $n'(t) \approx n(t)$ (low frequencies barely attenuated passively). The eardrum receives

$$e(t) = d(t) + y'(t), \tag{2}$$

and the three modes correspond to three target responses:

$$e(t) = d(t) + y'_{\mathrm{HT}}(t) \approx \hat{d}(t) \quad \text{(HT: open-ear replica)} \tag{3}$$
$$e(t) = d(t) + y'_{\mathrm{ANC}}(t) \ll \hat{d}(t) \quad \text{(ANC: strong attenuation)} \tag{4}$$
$$e(t) = d(t) + y'_{\mathrm{ANC+HT}}(t) \approx \hat{s}(t) \quad \text{(ANC+HT: desired sound restored, noise removed)} \tag{5}$$

![[raw/papers/huang-2026-integrated-anc-hear-through/figures/a3821c35b33e9023cd9af07933cc179112083fa4c4b43df3f9aa78f9fcffe6ed.jpg|Setup of an in-ear headphone integrating with AES]]
*Figure 1: Setup of an in-ear headphone integrating with AES.*

Relevant transfer functions (Fig. 2): primary path $P(z)$ (external mic → KEMAR ear, in-ear condition), target path $T(z)$ (relative transfer function under the open-ear condition — the desired HT reproduction characteristic), and secondary path $S(z)$ (loudspeaker → KEMAR ear). Offline estimates $\hat{S}(z)$ and $\hat{T}(z)$ feed the filter adaptation. Acoustic feedback is neglected thanks to strong passive isolation.

![[raw/papers/huang-2026-integrated-anc-hear-through/figures/33f13d4c613f2c611a7896a9c32111bc99f2987f6425db841cc625d2a033f174.jpg|Relevant transfer functions under open-ear and in-ear headphone conditions measured using a KEMAR]]
*Figure 2: Relevant transfer functions under open-ear and in-ear headphone conditions measured using a KEMAR.*

## Methodology

### Frequency-Band Allocation (design foundation)

Measured passive isolation (open-ear condition as 0 dB reference, right ear of a KEMAR, pink-noise excitation from a loudspeaker 50 cm away, DOA $0^\circ$–$315^\circ$ in $45^\circ$ steps; Figs. 3–4) is relatively ineffective below 500 Hz, so the nominal ANC operating band is defined as **100–500 Hz**; the HT band is **500 Hz–4 kHz**, where isolation is significant and DOA variation limited. Above 4 kHz the response becomes DOA-sensitive, so HT compensation is deliberately limited to avoid excessive amplification at unmodeled incidence directions. The authors stress this allocation is an engineering approximation, not a strict speech/noise spectral separation — voiced-speech harmonics overlap the ANC band and consonant cues extend beyond 4 kHz — so the crossover $f_L$ is a tunable trade-off parameter, adjustable 300–700 Hz in the implementation.

![[raw/papers/huang-2026-integrated-anc-hear-through/figures/a9e20d8db9724f333ca46710d6990f2246540a577dc4d0d83f5d55c1c60ed510.jpg|DOA measurements using a KEMAR]]
*Figure 3: DOA measurements using a KEMAR.*

![[raw/papers/huang-2026-integrated-anc-hear-through/figures/292fe6d2f693eeb0d95405fc9ead0cb7c3794e02caf620478c40af5a95a6905c.jpg|Passive isolation of the in-ear headphone at the right ear of the KEMAR for different DOAs]]
*Figure 4: Passive isolation of the in-ear headphone at the right ear of the KEMAR for different DOAs.*

### ANC Filter Design (offline FxLMS + balanced truncation)

The steady-state optimal feedforward controller for complete disturbance cancellation is

$$W^\circ(z) = \frac{P(z)}{S(z)}, \tag{6}$$

but the practical $W(z)$ is trained **offline** with the FxLMS algorithm on synchronized recordings of $x(n)$ and $d(n)$ with secondary-path estimate $\hat{S}(z)$ (Fig. 5):

$$\mathbf{w}(n+1) = \mathbf{w}(n) - \mu [\hat{\mathbf{s}}(n) * \mathbf{x}(n)] e_b(n). \tag{9}$$

Because a high-order FIR is too expensive for real-time in-ear DSP, the trained filter is reduced by **balanced truncation** to an IIR implemented as $K$ cascaded second-order sections:

$$\tilde{W}(z) = g \prod_{i=1}^{K} \frac{b_{0,i} + b_{1,i} z^{-1} + b_{2,i} z^{-2}}{a_{0,i} + a_{1,i} z^{-1} + a_{2,i} z^{-2}}. \tag{10}$$

![[raw/papers/huang-2026-integrated-anc-hear-through/figures/68917a9f265a041c06c6713b042690e4f6e6ac445a9edc4f92ac2242facbce5c.jpg|Block diagram for offline training of the ANC filter using the FxLMS algorithm]]
*Figure 5: Block diagram for offline training of the ANC filter using the FxLMS algorithm.*

### HT Filter Design

The HT filter compensates passive isolation to reproduce the open-ear response $\hat{d}(n)$. Assuming $d(n) \approx 0$ (it contains only components below 500 Hz, outside the HT band), the optimal compensation filter and its causal, realizable version are

$$H^\circ(z) = \frac{T(z)}{S(z)}, \qquad H(z) = \frac{\hat{T}(z) z^{-\Delta}}{\hat{S}(z)}, \tag{11–12}$$

where the delay $z^{-\Delta}$ satisfies the causality constraint of broadband feedforward control. $H(z)$ is then approximated offline by FxLMS training (Fig. 6), but unlike the ANC filter it starts from an analytically derived low-order FIR (adopted from the authors' previous time-shift-modeling HT system, Huang et al. 2022) — already suitable for real-time implementation, no order reduction needed.

![[raw/papers/huang-2026-integrated-anc-hear-through/figures/7fb74c9bedea9499e3dd3ed88a42c6590ddf15a0c94e63ca1062658bb087b093.jpg|Block diagram for offline training of the HT filter using the FxLMS algorithm]]
*Figure 6: Block diagram for offline training of the HT filter using the FxLMS algorithm.*

### AES Integration (the ANC+HT mode)

The two filters coexist in one signal flow (Fig. 7) with band separation enforced by filters rather than by operating-mode switching:

- a low-pass filter $L(z)$ (cutoff $f_c$) confines the ANC branch to the designated band;
- a bandpass **shaping filter** $C(z)$ (cutoffs $f_L$, $f_H$) confines the HT branch;
- gains $g_a$ (ANC strength, larger in low-frequency-dominated environments like aircraft cabins) and $g_h$ (ambient-sound compensation level, larger outdoors) let the user tune the trade-off.

The composite eardrum response is

$$E(z) = D(z) + S(z) [g_h H(z) C(z) + g_a \tilde{W}(z) L(z)] X(z). \tag{16}$$

![[raw/papers/huang-2026-integrated-anc-hear-through/figures/97e5a0b3bc2f8a044a055f6dec9962581407135ff6e3dd1bc712fbe0d8bd4641.jpg|Signal flow diagram of the proposed AES]]
*Figure 7: Signal flow diagram of the proposed AES.*

Three operating modes are supported by setting the gains (Table I): ANC ($g_a$ free, $g_h = 0$), HT ($g_a = 0$, $g_h$ free), and ANC+HT (both free).

## Experimental Setup

| Item | Configuration |
|:-----|:--------------|
| **Platform** | TMS320C6713 DSP Starter Kit + DSK6713IF-B ADC/DAC daughterboard, 48 kHz sampling |
| **Analog chain** | Mic preamp → ADC → DSP → DAC → power amp → in-ear headphone; anti-aliasing/reconstruction filters at 20 kHz |
| **Reference mic** | MEMS microphone mounted on the headphone shell |
| **Manikin** | G.R.A.S. KEMAR (right ear), rotatable platform for DOA experiments; measurements in an anechoic chamber |
| **ANC filter** | 3000-tap FIR (offline FxLMS) → 50th-order IIR via balanced truncation, 25 cascaded SOSs; ~125 multiplications/sample (vs. ~3000, i.e. 6 vs. 144 M multiplications/s at 48 kHz) |
| **LPF $L(z)$** | 1st-order IIR, cutoff 3 kHz (short latency) |
| **Shaping filter $C(z)$** | 6th-order IIR bandpass 500 Hz–4 kHz ($f_L$ adjustable 300–700 Hz) |
| **Filter lengths** | $H(z)$: 350 taps; $\hat{S}(z)$: 400 taps; $\hat{T}(z)$: 350 taps |
| **Stimuli** | Pink noise 80 dBA (training); recorded aircraft-cabin noise 77 dBA; clean TIMIT speech 71 dBA (10 utterances, 5 female/5 male, for the commercial comparison) |
| **Default DOA** | 270° (lateral incidence reference condition); DOA sweep separately |
| **Hardware latency** | 37 μs ADC→DSP→DAC group delay at 1 kHz; open-ear vs. in-ear acoustic response difference ~292 μs |
| **Power** | DSK platform: 2.42 W idle, 3.01 W AES running (not representative of battery products) |
| **Objective metric** | SRMR_norm (non-intrusive speech quality/intelligibility), signals resampled 48→16 kHz |
| **Subjective test** | 25 participants (14 M / 11 F), 5 s samples, four fixed-order conditions, 5-point clarity scale from −1 to +1; Friedman test + Wilcoxon signed-rank with Holm correction |
| **Baselines** | Two commercial in-ear headphones in HT mode |

![[raw/papers/huang-2026-integrated-anc-hear-through/figures/d97304e5546aae4c4691fe061a49a79f75f5b3d2c135e67fa3646f73ba3fc2e3.jpg|Experimental setup: system configuration]]
![[raw/papers/huang-2026-integrated-anc-hear-through/figures/9d5ae5dfc7e9f110c927365c66fbf6459c50acccd47dfafaa5f3ca9903050130.jpg|An in-ear headphone with AES and two commercial headphones]]
*Figure 8: Experimental setup: (a) system configuration; (b) an in-ear headphone with AES and two commercial headphones.*

## Results

### Mode spectra and DOA robustness

- Mode spectra (Fig. 10): passive isolation kicks in above 500 Hz; ANC mode attenuates below 500 Hz only; HT mode restores an open-ear-like spectrum to 4 kHz; ANC+HT mode with $f_L = 300$ Hz attenuates below 300 Hz and compensates 300 Hz–4 kHz — noise removed, speech-relevant band restored.
- DOA sweep (Fig. 11, $f_L = 700$ Hz): attenuation below 700 Hz varies with DOA but remains noticeable for all DOAs; the HT band stays close to the open-ear condition from 700 Hz–4 kHz across DOAs; above 4 kHz, compensation is intentionally limited.
- Tuning (Fig. 12): $g_a$ controls overall attenuation level, $g_h$ the transparency level, $f_L$ the effective noise-reduction bandwidth — demonstrating user-controllable trade-off tuning.

![[raw/papers/huang-2026-integrated-anc-hear-through/figures/610c7f4eeb562fe5942411a9fa6cfc80d6a4a53b6d4d08dabbda68dd67813b14.jpg|Measured spectra at the right ear of the KEMAR for different modes of AES]]
*Figure 10: Measured spectra at the right ear of the KEMAR for different modes of AES.*

![[raw/papers/huang-2026-integrated-anc-hear-through/figures/5f99061202856881f1467cddba82434ae85b16450db45fd4e680c677b142dd42.jpg|Measured results of the ANC+HT mode with different DOAs]]
*Figure 11: Measured results of the ANC+HT mode with different DOAs.*

![[raw/papers/huang-2026-integrated-anc-hear-through/figures/5449735623d31c2921cb999a76580d68dea6fdfabd164fecb8dd97d7c5aca662.jpg|Effects of gain and filter configuration: ga]]
![[raw/papers/huang-2026-integrated-anc-hear-through/figures/5707999bf156648017bd1e89d30cae45515b4ee807daa28b3cb35db19a2cadc0.jpg|Effects of gain and filter configuration: gh]]
![[raw/papers/huang-2026-integrated-anc-hear-through/figures/7b223cdd5af944bb758feab0db2575b5db29584ed54d327cd8c30fb75b8f9104.jpg|Effects of gain and filter configuration: lower cutoff frequency fL of the shaping filter C(z)]]
*Figure 12: Effects of gain and filter configuration: (a) $g_a$; (b) $g_h$; (c) lower cutoff frequency $f_L$ of the shaping filter $C(z)$.*

### Speech clarity under aircraft-cabin noise

Spectrogram analysis (Fig. 13, TIMIT sentence + recorded aircraft noise): passive isolation and ANC both suppress low-frequency speech components (poor clarity); HT restores mid/high-frequency components but reintroduces aircraft noise; ANC+HT attenuates noise below 300 Hz while compensating 300 Hz–4 kHz — preserving speech clarity in low-frequency noise.

![[raw/papers/huang-2026-integrated-anc-hear-through/figures/c7a5c89e2213678b713e80474f7a2e613e844ef41728f1c7d62b2a40238a9a6f.jpg|Spectrogram of the signal with different operating modes]]
*Figure 13: Spectrogram of the signal with different operating modes.*

**SRMR_norm scores** (higher = better intelligibility):

| Condition | SRMR_norm |
|:----------|:----------|
| Open ear (speech + aircraft noise) | 0.878 |
| Passive isolation | 0.723 |
| ANC mode | 0.717 |
| HT mode | 0.833 |
| **ANC+HT mode** | **0.974** |

The HT mode is comparable to the open-ear condition; ANC+HT is the best of all four headphone conditions and surpasses even open-ear listening in noise.

### Commercial comparison

Against two commercial in-ear headphones in HT mode (Fig. 14): commercial A matches the open-ear response up to ~4 kHz, commercial B only to ~2 kHz — but neither suppresses low-frequency noise. The proposed AES in ANC+HT mode suppresses low-frequency noise while preserving the 300 Hz–4 kHz spectrum close to open-ear — the best balance of noise reduction and voice preservation.

![[raw/papers/huang-2026-integrated-anc-hear-through/figures/a1189f11f9f1d272e94aeff232cc06c8da739954007896785f065dc94667c924.jpg|Comparison of measured spectra for the proposed AES and two commercial in-ear headphones under mixed speech and recorded low frequency noise]]
*Figure 14: Comparison of measured spectra for the proposed AES and two commercial in-ear headphones under mixed speech and recorded low-frequency noise.*

### Subjective listening test

25 participants rated speech clarity on a 5-point scale (−1 to +1) for KEMAR-recorded stimuli played back over a loudspeaker in a conference room (group-based, fixed condition order; Fig. 15):

| Condition | Mean | Median | SD |
|:---------|:-----|:-------|:---|
| Passive isolation | −0.26 | 0 | 0.293 |
| ANC mode | −0.72 | −0.5 | 0.292 |
| HT mode | 0.60 | 0.5 | 0.289 |
| **ANC+HT mode** | **0.88** | **1.0** | 0.261 |

Friedman test: $\chi^2(3) = 69.66$, $p < 0.001$, Kendall's $W = 0.929$ (large effect). All six pairwise Wilcoxon signed-rank comparisons significant at $p_{\mathrm{Holm}} < 0.001$; ANC+HT vs. HT: $W = 19$, $r_{rb} = 0.778$. Subjective results are consistent with the objective SRMR_norm ranking.

![[raw/papers/huang-2026-integrated-anc-hear-through/figures/9719f3e0375f3a300c520c68ee3685768cef300ebada2724ad71bfeabaa01dab.jpg|Group-based subjective listening evaluation setup in a conference room using recorded signals]]
*Figure 15: Group-based subjective listening evaluation setup in a conference room using recorded signals.*

![[raw/papers/huang-2026-integrated-anc-hear-through/figures/78559f754d3edc10e1087644db3d467850b68d462386c7e0eb2a7a4eca35710e.jpg|Boxplots of subjective speech clarity ratings under the four listening conditions]]
*Figure 16: Boxplots of subjective speech clarity ratings under the four listening conditions.*

## Key Contributions

1. **Integrated ANC+HT framework**: a single acoustic equalization system coordinating feedforward ANC and HT via frequency-band allocation (LPF-confined ANC branch + bandpass-shaped HT branch + two user gains $g_a, g_h$ + adjustable crossover $f_L$), replacing the mutually-exclusive-mode paradigm of commercial headphones — explicitly positioned as *not* claiming novelty for the general concept of simultaneous ANC/HT, but for a practical, tunable in-ear implementation for speech clarity in low-frequency noise.
2. **Causality- and compute-aware realization**: offline FxLMS training followed by balanced-truncation model-order reduction (3000-tap FIR → 50th-order IIR, 25 SOSs, ~125 multiplications/sample) on a 37 μs-delay DSP platform, plus an analytically derived low-order HT filter — a fixed-filter architecture compatible with the tight causality margin of in-ear feedforward control.
3. **Speech-clarity evidence**: the first (to the authors' knowledge) combined objective + subjective validation of integrated ANC/HT for speech clarity: SRMR_norm 0.974 (best, exceeding open-ear-in-noise 0.878) and subjective clarity 0.88 vs. 0.60 for HT alone (25 listeners, Friedman $p < 0.001$), plus superiority over two commercial in-ear headphones in HT mode on spectral grounds.

## Limitations and Caveats

- Single fixed SNR scenario (pink 80 / aircraft 77 / speech 71 dBA); no systematic SNR sweep.
- Listening test is proof-of-concept: group playback in a conference room (uncharacterized reverberation), fixed condition order, single 5 s sample per condition, no randomization/counterbalancing/repeated trials — order, learning, and short-duration effects cannot be excluded.
- Stimuli were KEMAR-recorded signals, not direct on-ear listening; listener-dependent ear anatomy, insertion depth, and fit variations are not covered.
- Fixed 270° incidence for main results (a controlled reference, not a representative average); DOA robustness was assessed separately.
- HT band capped at 4 kHz — perceptually relevant speech components above 4 kHz are not compensated (a deliberate robustness trade-off, but a speech-quality limit nonetheless).
- DSK platform power (3.01 W) is far from battery-powered earbud budgets; fixed-point and SoC implementation left to future work.

## Related Concepts

- [[concepts/acoustic-equalization-system|Acoustic Equalization System (AES)]]
- [[concepts/hear-through-frequency-band-allocation|Hear-Through Frequency-Band Allocation]]
- [[concepts/transparency-mode|Transparency Mode]]
- [[concepts/feedforward-anc|Feedforward ANC]]
- [[concepts/speech-preserving-anc|Speech-Preserving ANC]]
- [[concepts/selective-anc|Selective ANC]]
- [[concepts/causality|Causality in ANC]]
- [[concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/balanced-truncation-model-reduction|Balanced Truncation Model Reduction]]

## Related Synthesis

- [[synthesis/modern-headphone-anc-systems|Modern Headphone ANC Systems]]

## Related Sources

- [[sources/serizel-2010-integrated-anc-nr-hearing-aids|Serizel, Moonen, Wouters & Jensen 2010: Integrated ANC and NR in Hearing Aids]] — earlier integrated ANC + noise-reduction framework for open-fitting hearing aids, FxMWF-based rather than band-allocated fixed filters
- [[sources/rao-2026-keep-speech-anc|Rao et al. 2026: Causal Reference-Enhanced Keep-Speech Active Noise Control]] — concurrent speech-preserving headphone ANC via neural reference enhancement
- [[sources/kuo-2006-anc-headphones|Kuo, Mitra & Gan 2006: Active Noise Control System for Headphone Applications]] — same group's earlier adaptive feedback ANC headphone
