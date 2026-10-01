---
type: concept
created: 2026-04-10
updated: 2026-10-01
sources:
  - raw/papers/serizel-2010-integrated-anc-nr-hearing-aids/full-text.md
  - raw/papers/zhang-2024-active-noise-control-soundfield-interpolation-pinn/full-text.md
  - raw/papers/guo-2024-anc-saturation-survey/full-text.md
  - raw/papers/bai-2026-feedback-guided-anc/full-text.md
  - raw/papers/zhang-2026-feedback-path-mitigation-mcanc/full-text.md
  - raw/papers/veluri-2023-semantic-hearing/full-text.md
  - raw/papers/yang-2026-direction-preserving-anc/full-text.txt
  - raw/papers/cheng-2026-anc-gain-constraint/full-text.txt
  - raw/papers/rao-2026-keep-speech-anc/full-text.txt
aliases:
- Active Noise Control
tags:
- acoustics
- control-systems
- signal-processing
- acoustic-feedback
---

# Active Noise Control

## Overview

**Active Noise Control (ANC)** is a technique that cancels unwanted sound by generating an "anti-noise" signal — a secondary sound of equal amplitude but opposite phase — which combines with the primary noise to achieve destructive interference, based on the principle of superposition.

## How It Works

1. A **reference sensor** (microphone) picks up the primary noise
2. A **controller** processes this signal and generates an anti-noise signal
3. A **secondary source** (loudspeaker) emits the anti-noise
4. The anti-noise and primary noise cancel each other at the **error sensor** location

## Two System Architectures

### Feedforward ANC

- Uses a reference sensor placed **upstream** of the noise source to get a time-advanced reference signal
- Requires the noise to be measurable before it reaches the cancellation zone
- Generally better performance for predictable noise

### Feedback ANC

- No reference sensor; uses only an **error sensor** to drive the controller
- Used when the primary noise cannot be directly observed or there are too many primary noise sources
- Typical applications: headsets, headrests, headphones, double-glazed windows, ducts
- Two subtypes:
  - **Non-adaptive**: Fixed controller with high gain at frequencies of interest. Requires solving optimization problems; vulnerable to changing conditions.
  - **Adaptive**: Controller adapts automatically. Includes [[internal-model-control|Internal Model Control]] (IMC) based systems and [[adaptive-feedback-control|Adaptive Feedback Control]] systems.

## Deep Learning Approaches

Traditional ANC algorithms are limited by linear assumptions and cannot handle nonlinear acoustic paths or selectively preserve speech. Deep learning approaches address these limitations:

- **[[convolutional-recurrent-network|CRN]]-based Deep ANC**: End-to-end anti-noise generation using encoder-LSTM-decoder architecture with [[complex-spectrum-mapping|Complex Spectrum Mapping]] for precise phase control
- **[[speech-preserving-anc|Speech-Preserving ANC]]**: Uses a modified loss function that algebraically cancels speech components, training the network to cancel only noise while leaving speech transparent
- **[[concepts/reference-signal-enhancement|Reference Signal Enhancement]] (Rao et al. 2026)**: keep-speech ANC without touching the controller — a causal time-domain WaveNet (zero algorithmic delay) suppresses the speech contaminating the reference microphone signal, and a conventional RLS-adapted FIR control filter cancels only the noise; improves STOI/DNSMOS over Unprocessed, Conventional ANC, and DeepANC on measured headphone IRs, where DeepANC's frame-level CRN latency violates causality
- SFANC/GFANC: Selective/Generative Fixed-Filter ANC uses CNNs for filter selection or generation, enabling instant response to changing noise types
- **[[feedback-guided-controller-fusion|Feedback-guided Controller Fusion]]** (Bai 2026): Hybrid WaveNet + mixture-of-experts of FIR experts, where the MoE gating network consumes reference + control + **delayed residual-error** signals — closing the loop on the actual acoustic condition (unlike SFANC/GFANC, which use reference-side features only). 19.00 dB avg NR (50 Hz–5 kHz) on CCF-AATC headphone ANC with negligible 1–8 kHz amplification; 32.69k params / 672.93 MMac/s for the 10-expert streaming model.
- **[[concepts/physics-informed-neural-network|PINN]]-assisted ANC** (Zhang 2024): A PINN interpolates the soundfield at virtual microphone positions from monitoring microphones placed outside the ROI, using the acoustic wave equation as a PDE residual loss. The interpolated signals drive a multi-channel FxLMS controller, achieving better noise reduction at the ear than a conventional multiple-point ANC system.
- **E2E-CFG**: End-to-End Control-Filter Generation directly generates control filters via Transformer co-processor in a differentiable ANC system, trained unsupervised on residual error
- **[[concepts/semantic-hearing|Semantic hearing]]** (Veluri et al. 2023): inverts the ANC paradigm — modern noise-canceling headsets (e.g., Sony WH-1000XM4) provide an "acoustic clean slate" by attenuating *all* external sounds, and a real-time binaural target-sound-extraction network reintroduces only user-chosen sound classes while preserving their spatial cues. An end-to-end experiment showed the semantic-hearing playback coexisting with adaptive feedforward ANC; residual-noise-aware playback adaptation remains open.
- **[[direction-preserving-anc|DP-ANC]]** (Yang 2026): Direction-conditioned network estimates the full multichannel FIR control-filter bank in one forward pass (FiLM-conditioned, differentiable secondary-path-aware training), cancelling noise from non-desired directions while preserving desired-direction sound naturally — 22.8 dB NR at −11.4 dB desired-response distortion over 3300 cases, ≈3000× cheaper per filter bank than the analytical SSANC solve

### Performance Comparison (Dai 2026, RT60=0.3s)

| Noise Type | FxLMS (dB) | Deep ANC (dB) | Improvement |
|:-----------|:-----------|:--------------|:------------|
| Engine (Periodic) | 12.22 | 22.92 | +10.70 |
| Babble (Non-stationary) | 5.28 | 18.17 | +12.89 |
| Volvo (Stationary) | 4.91 | 19.08 | +14.17 |

## Key Challenges

- **Secondary path estimation**: The path from loudspeaker to error sensor (including DAC, amplifier, speaker, acoustic path, ADC) must be estimated accurately
- **Stability**: Phase shifts in the secondary path can cause negative feedback to become positive feedback
- **Predictability**: Performance depends on how predictable the primary noise is; narrow-band noise works better than broadband noise
- **Nonlinear distortion**: Low-cost speakers and high-SPL scenarios introduce nonlinearities that linear algorithms cannot model
- **[[output-saturation-effect|Output saturation]]**: When the secondary-path amplifier is driven beyond its rated output, the control signal is clipped and unconstrained adaptive filters (linear and nonlinear) diverge. Mitigated by [[output-constraint-anc-algorithms|output constraint algorithms]] or [[nonlinear-active-noise-control|nonlinear adaptive algorithms]] depending on the saturation regime (Guo 2024)
- **Micro-loudspeaker mechanical over-excursion**: The rolled-off low-frequency response of micro-loudspeakers in compact devices, combined with the high low-frequency gain of unconstrained (Wiener) control filters, drives the diaphragm beyond its mechanical limits — a transducer-side limit distinct from amplifier saturation. Mitigated at design time by [[concepts/frequency-response-constrained-anc|frequency-response gain constraints]] on the fixed control filter (Cheng 2026), which avoid the group-delay penalty of runtime high-pass cascades
- **Speech cancellation**: Traditional "cancel everything" approach damages useful speech signals in mixed sound fields
- **DOA dependency**: The primary path $P(z)$ varies with sound direction, degrading feedforward ANC at non-nominal DOAs (Liebich 2018)
- **Acoustic feedback in multichannel arrays**: loudspeaker-to-reference coupling grows with channel count, so the closed loop sets the usable step size. In a $(J_{\mathrm{R}}, J_{\mathrm{F}}, L, R) = (8, 8, 2, 2)$ array, plain multichannel FxLMS diverges once the secondary sources are spread beyond ~0.3 m, and the primary noise cannot be switched off to measure the feedback paths offline (Zhang 2026)

## Related Sources

- [[sources/lu-2021-survey-active-noise-control-linear|Lu et al. 2021: Survey on ANC — Part I: Linear Systems]]

## Related Concepts
- [[adaptive-algorithm-tradeoffs]]
- [[cha-2023-dnoisenet-feedback-anc]]
- [[how-to-estimate-secondary-path]]
- [[impulsive-noise-control]]
- [[jiang-2025-ai-driven-avnc-review]]
- [[luo-2026-hybrid-gfanc-fxnlms]]
- [[multichannel-anc-efficiency-and-robustness]]
- [[personal-sound-zones-evolution-and-optimization]]
- [[what-is-simplified-adaptive-feedback-anc]]

- [[adaptive-feedback-control|Adaptive Feedback Control]]
- [[internal-model-control|Internal Model Control]]
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[leaky-fxlms-algorithm|Leaky FxLMS Algorithm]]
- [[simplified-adaptive-feedback-anc|Simplified Adaptive Feedback ANC]]
- [[online-secondary-path-modeling|Online Secondary-Path Modeling]]
- [[convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[speech-preserving-anc|Speech-Preserving ANC]]
- [[image-source-method|Image Source Method]]
- [[uncertainty-modeling-for-anc|Uncertainty Modeling for ANC]]
- [[robust-stability-constraint|Robust Stability Constraint]]
- [[convex-hull-uncertainty-model|Convex Hull Uncertainty Model]]
- [[elliptic-uncertainty-model|Elliptic Uncertainty Model]]
- [[concepts/output-saturation-effect|Output Saturation Effect]]
- [[concepts/output-constraint-anc-algorithms|Output Constraint ANC Algorithms]]
- [[concepts/nonlinear-active-noise-control|Nonlinear Active Noise Control]]
- [[concepts/acoustic-feedback|Acoustic Feedback]] — the secondary-to-reference leakage that limits feedforward ANC stability
- [[concepts/relative-transfer-matrix|Relative Transfer Matrix (ReTM)]] — spatial-mapping approach to multichannel feedback neutralization
- [[concepts/covariance-subtraction|Covariance Subtraction]] — identifies the mapping without a noise-free training window

## Related Sources

- [[sources/wu-2014-simplified-adaptive-feedback-anc|Wu 2014: Simplified Adaptive Feedback ANC]] — Proposes a simplified adaptive feedback system using error signal directly as reference
- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] — Comprehensive ANC tutorial covering all major algorithms
- [[sources/dai-2026-speech-preserving-deep-anc|Dai 2026: Speech-Preserving Deep ANC]] — CRN-based Deep ANC with speech preservation in reverberant environments
- [[sources/hilgemann-2024-data-driven-uncertainty-anc|Hilgemann 2024: Data-Driven Uncertainty Modeling for Robust Feedback ANC]] — Elliptic and convex hull uncertainty models for robust feedback ANC
- [[sources/wang-2026-predictive-dsfanc-crnn|Wang 2026: Predictive Directional SFANC via CRNN]] — CRNN predicts next-frame DoA for proactive filter selection in moving source ANC
- [[sources/holzmuller-2026-dtw-secondary-path-anc|Holzmüller & Sontacchi 2026: DTW for Secondary Path Interpolation in ANC]] — DTW-based interpolation extends stable frequency range for moving listeners
- [[sources/zhang-2024-active-noise-control-soundfield-interpolation-pinn|Zhang et al. 2024: ANC with PINN-based Soundfield Interpolation]] — PINN interpolates soundfield from outside-ROI monitoring microphones for improved ANC
- [[sources/fujii-2006-simultaneous-equations-anc|Fujii et al. 2006: Verification of Simultaneous Equations Method]] — Experimental validation of secondary-path-model-free ANC
- [[sources/ma-2027-robust-ffanc-online-path-modeling|Ma 2027: Robust FFANC with Simultaneous OSPM and OFBPM]] — feedforward ANC with simultaneous online SP and FBP modeling; introduces a second supporting filter and SF-driven global AWGN scaling for robustness under time-varying paths
- [[sources/guo-2024-anc-saturation-survey|Guo et al. 2024: ANC Algorithms Overcoming Output Saturation]] — survey of adaptive ANC algorithms mitigating the output saturation effect, organising the field into output-constraint and nonlinear-adaptive families
- [[sources/bai-2026-feedback-guided-anc|Bai 2026: Feedback-guided DNN-based Controller Fusion for Robust Fixed-Parameter ANC]] — hybrid WaveNet + feedback-guided MoE of FIR experts; 19 dB avg NR (50 Hz–5 kHz) on CCF-AATC headphone ANC with negligible 1–8 kHz amplification
- [[sources/serizel-2010-integrated-anc-nr-hearing-aids|Serizel, Moonen, Wouters & Jensen 2010: Integrated ANC and NR in Hearing Aids]] — ANC integrated with noise reduction for open-fitting hearing aids; see also [[concepts/filtered-x-mwf|Filtered-x MWF]] and [[concepts/open-fitting-noise-leakage|Open-Fitting Noise Leakage]]
- [[sources/zhang-2026-feedback-path-mitigation-mcanc|Zhang, Abhayapala, Samarasinghe & Bastine 2026: Acoustic Feedback Path Mitigation for Multichannel ANC]] — multichannel feedforward ANC with ReTM-based feedback subtraction ahead of a normalized frequency-domain FxLMS controller
- [[sources/veluri-2023-semantic-hearing|Veluri et al. 2023: Semantic Hearing]] — uses ANC as an acoustic clean slate and reintroduces user-selected sound classes in real time; demonstrates coexistence with adaptive feedforward ANC on commercial headphones
- [[sources/yang-2026-direction-preserving-anc|Yang et al. 2026: Direction-Preserving ANC with a Conditional Control-Filter Estimation Network]] — FiLM-conditioned network estimates the full control-filter bank; cancels non-desired directions while preserving desired-direction sound
- [[sources/cheng-2026-anc-gain-constraint|Cheng et al. 2026: Active Noise Control With a Gain Constraint for Micro-Loudspeakers]] — design-time frequency-response gain constraint on fixed control filters to prevent micro-loudspeaker mechanical over-excursion
- [[sources/rao-2026-keep-speech-anc|Rao, Rong, Sun, He, Chen, Zou & Lu 2026: Causal Reference-Enhanced Keep-Speech Active Noise Control]] — keep-speech ANC with a causal WaveNet on the reference path and a conventional RLS FIR controller; zero added delay, improves STOI/DNSMOS over all baselines on measured headphone IRs

## Related Entities

- [[entities/sen-m-kuo|Sen M. Kuo]] — ANC authority, author of the definitive tutorial review
- [[entities/dennis-r-morgan|Dennis R. Morgan]] — Co-author of the tutorial review, foundational FXLMS analysis
- [[entities/lifu-wu|Lifu Wu]] — Proposed the simplified adaptive feedback architecture
- [[entities/xiaojun-qiu|Xiaojun Qiu]] — Corresponding author on the SimpAFB paper
- [[entities/shuning-dai|Shuning Dai]] — Speech-preserving Deep ANC in reverberant environments
- [[entities/stefan-liebich|Stefan Liebich]] — DOA dependency of ANC headphones
