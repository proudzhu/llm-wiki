---
type: source
created: 2026-10-24
updated: 2026-10-24
sources:
  - raw/papers/chiba-2027-wideband-anc-coaxial-loudspeaker/full-text.txt
  - https://doi.org/10.1016/j.apacoust.2026.111618
  - zotero://select/items/0_5FCJ3LBZ
tags:
  - active-noise-control
  - open-ear-headphones
  - feedforward-anc
  - causality
  - secondary-path-delay
  - group-delay
  - coaxial-loudspeaker
  - wearable-audio
---

# Chiba, Kamado, Kako & Noguchi 2027: Wideband Active Noise Control for Open-Ear Headphones via Low-Delay Acoustic Design with a Coaxial Loudspeaker

**Authors**: [[entities/hironobu-chiba|Hironobu Chiba]], [[entities/noriyoshi-kamado|Noriyoshi Kamado]], [[entities/tatsuya-kako|Tatsuya Kako]], [[entities/kenichi-noguchi|Kenichi Noguchi]]
**Affiliation**: NTT Inc., Tokyo, Japan
**Venue**: Applied Acoustics 257 (2027), article 111618
**Year**: 2027
**Type**: Journal article
**DOI**: [10.1016/j.apacoust.2026.111618](https://doi.org/10.1016/j.apacoust.2026.111618)
**Zotero**: [5FCJ3LBZ](zotero://select/items/0_5FCJ3LBZ)

## Summary

This paper proposes a **design-oriented secondary-path delay budget** for broadband feedforward ANC on [[concepts/open-ear-headphones|open-ear headphones]], decomposing the secondary-path delay into electronic, acoustic, and mechanical terms and allocating control bands to drivers according to their delay characteristics. A **coaxial offset 2-way secondary source** (35 mm woofer, 12 mm tweeter mounted in front of it) exploits the complementary delays: the woofer handles low frequencies where its larger diaphragm yields a lower fundamental resonance (≈150 Hz) and thus smaller mechanical group delay, while the tweeter handles higher frequencies where its forward placement gives a shorter acoustic propagation delay (≈6 µs vs ≈44 µs). In a controlled measured-path offline evaluation (one nwm ONE device, one dummy-head configuration, 3 reference microphones per ear, FxNLMS at 48 kHz with 104 µs virtual electronic delay), the dual-filter background condition Du-BpHp-Bg achieved **8.01 dB** band-limited pink-noise reduction over 100–2000 Hz and the single-filter condition Xo-BpHp achieved **7.58 dB**, versus 5.94 dB (woofer-only) and 5.02 dB (tweeter-only) baselines.

## Problem Formulation

Open-ear headphones provide environmental awareness but almost no passive attenuation, so broadband feedforward ANC is required — yet the causality budget is extremely tight:

$$\tau_S(f) \leq \tau_P(f) - \tau_R(f)$$

where $\tau_S$ is the secondary-path group delay, $\tau_P$ the noise-source-to-error-microphone delay, and $\tau_R$ the noise-source-to-reference-microphone delay. Unlike closed headphones (whose passive attenuation above ~1 kHz relaxes the ANC requirement), open-ear devices need control over a wider band, tightening the budget at every frequency.

### Relaxed causality model

Since the strict condition is generally violated in open-ear devices at low frequencies (where the loudspeaker's mechanical group delay is large), the paper derives a **relaxed boundary** via single-frequency analysis. With phase error $\Delta\theta(f) = 2\pi f \Delta\tau(f)$ from excess delay $\Delta\tau(f) = \tau_S(f) - [\tau_P(f) - \tau_R(f)]$, the residual level under optimal amplitude is:

$$\beta_{\min}(f) = 20\log_{10}|\sin(2\pi f \Delta\tau(f))|$$

valid for $0 \leq \Delta\theta < \pi/2$. Positive noise reduction survives until the quarter-period margin $\Delta\tau_q(f) = 1/(4f)$ is exhausted — so delay reduction becomes increasingly critical at higher frequencies, and pushing the achievable-attenuation boundary upward is the design objective.

### The open-ear delay dilemma

The secondary-path delay decomposes as $\tau_S(f) = \tau_S^E(f) + \tau_S^A(f) + \tau_S^M(f)$ (electronic + acoustic + mechanical):

- **Electronic delay** can now be reduced to tens of µs (oversampling, low-delay ADC/DAC).
- **Acoustic delay** $\approx l/c$ grows with the diaphragm-to-ear distance needed for openness.
- **Mechanical delay** rises sharply near and below the driver's fundamental resonance $f_0$ — and compact open-ear drivers have $f_0$ of several hundred Hz, exactly where environmental noise energy concentrates.

A single compact driver cannot achieve low acoustic *and* low mechanical delay across the full band. The paper's answer: a **2-way driver** whose woofer (low $f_0$ = 150 Hz → low mechanical delay at low frequencies) and tweeter (forward placement → low acoustic delay at high frequencies) offer *complementary* delay advantages.

## Methodology

### Coaxial offset 2-way secondary source

The tweeter sits in front of the woofer on a common axis (13 mm offset). From the geometry: tweeter-to-error-mic ≈ 2 mm (≈6 µs), woofer-to-error-mic ≈ 15 mm (≈44 µs). JIS-enclosure isolated-driver measurements confirm the mechanical complementarity: woofer $f_0 \approx 150$ Hz, tweeter $f_0 \approx 300$ Hz; woofer group delay decreases rapidly above 150 Hz while the tweeter's remains elevated to ~500 Hz.

### Three band-splitting architectures

The control band is split by a first-order Butterworth high-pass ($f_c = 500$ Hz, chosen above the tweeter's resonant region) between woofer and tweeter, realized in three configurations:

1. **Dual-filter, background placement (Bg)**: independent adaptive-filter branches per driver; the band-limiting filters $h_W, h_T$ act *only* on the gradient (error and filtered-reference) signals — **delayless** in the output path. Ideal delay envelope $\tau_{\text{env}}^{\text{Bg}}(f) = \min(\tau_{S,W}, \tau_{S,T})$.
2. **Dual-filter, foreground placement (Fg)**: band-limiting filters in the output branches — direct out-of-band suppression at the cost of adding crossover-filter group delay ($\approx$160 µs at 500 Hz, 64 µs at 1 kHz). Envelope $\tau_{\text{env}}^{\text{Fg}}(f) = \min(\tau_{S,W} + \tau_{H_W}, \tau_{S,T} + \tau_{H_T})$.
3. **Single-filter configuration**: one adaptive-filter branch feeding a fixed crossover network ($g_W = 1$, $g_T = g_m g_{adj}$) — the composite secondary path $s_C = g_W h_W * s_W + g_T h_T * s_T$ is controlled as one path. Halves the control-output convolution, coefficient-commitment rate, and coefficient storage (~2x), but the crossover is necessarily in the foreground path.

Gain matching: $g_m$ is the woofer/tweeter RMS magnitude ratio over a flat common band (500–2000 Hz): $g_m = 1.655$ (L), $1.409$ (R).

**Not a conventional audio crossover**: the motivation is delay minimization under a causality constraint, not spectral response quality; in most ANC applications the control objective concentrates at low frequencies where a single woofer suffices, but the open-ear target band extends into the mid range where passive attenuation does not relax the requirement.

### Nine comparison conditions

| ID | Config | Placement | $h_W$ | $h_T$ |
|----|--------|-----------|-------|-------|
| Wf-Bp | Woofer only | equiv. | Bypass | Off |
| Tw-Bp | Tweeter only | equiv. | Off | Bypass |
| Tw-Hp-Fg / Tw-Hp-Bg | Tweeter only | Fg / Bg | Off | HP 500 |
| Du-BpBp | Dual | equiv. | Bypass | Bypass |
| Du-BpHp-Fg / Du-BpHp-Bg | Dual | Fg / Bg | Bypass | HP 500 |
| Xo-BpBp / Xo-BpHp | Single | Fg only | Bypass | Bypass / HP 500 |

Bypass = $h = \delta$ (no band limitation); Off = driver disabled. Bypass conditions are delay *references*, not practical recommendations (driving the tweeter below its efficient range raises distortion/instability risk in a physical implementation).

## Experimental Setup

| Item | Detail |
|------|--------|
| Device | nwm ONE open-ear headphone (coaxial offset 2-way: woofer 35 mm, tweeter 12 mm, 13 mm coaxial offset), opposite-phase-radiation leakage mitigation |
| Reference microphones | 3 omni electret (Hosiden KUB0623, 4 mm) per ear on the housing |
| Error microphone | 1 per ear, on the loudspeaker axis at the ear-canal entrance |
| Measurement room | 6.0 × 4.0 × 2.6 m, RT ≈ 0.1 s |
| Primary sources | 4 Genelec 8030C at ~2.0 m around a SAMREC 2600RS dummy head |
| Path measurement | TSP (exponential swept sine, $2^{18}$ samples, 48 kHz), 8-ch interface with analog loopback latency compensation |
| Algorithm | Time-domain multi-reference FxNLMS, R = 3 refs/ear, reference-specific normalization |
| Control filter / secondary path | $N = 1024$ taps / $L = 256$ taps |
| Coefficient commitment | every $B = 10$ samples (block implementation) |
| Step size | $\mu = 0.04$ (all active branches) |
| Virtual electronic delay | 5 samples = 104 µs prepended to secondary paths and models (controlled parameter, not measured latency) |
| Noise source | 4-channel uncorrelated pink noise, 10 s per run |
| Evaluation | $L_{NR}(f)$ (STFT, Hann 4096, hop 1024), 1/1-octave bands (125 Hz–4 kHz, IEC 61260), band-limited power ratio $L_{BL}(B)$; final 25% (≈2.5 s) steady-state window |
| Isolated-driver measurement | JIS C 5532 enclosure, pressure mic at 30 mm, 1-s log sweep 20 Hz–24 kHz at 192 kHz |
| Platform evidence | ADSP-21569 + AK5736 ADC + AK4454 DAC, 192 kHz / 8-sample frames with 24 kHz internal rate; pass-through peak 83.3 µs; foreground 27.7 µs < 41.7 µs deadline, background ≤ 79.7% of block deadline |

The evaluation is an **idealized linear measured-path offline study** — it deliberately excludes loudspeaker nonlinearities, secondary-path modeling error, microphone noise, coupled secondary-to-reference feedback (post-hoc estimate: worst contamination ratio −19.88 dB), processing precision, controller timing for the exact evaluated configurations, and wearing-position variation.

## Results

### Driver delay basis (Table 5 of the paper)

Representative delay budgets at 500 Hz / 1 kHz (woofer branch ≈ 44 µs acoustic + mechanical, tweeter branch ≈ 6 µs acoustic + mechanical):

| Frequency | Condition | Acoustic | Mechanical | Filter delay | Subtotal | Total (+104 µs) |
|-----------|-----------|----------|------------|--------------|----------|-----------------|
| 500 Hz | Wf-Bp | ≈44 | ≈162 | 0 | ≈206 | ≈310 |
| 500 Hz | Tw-Bp / Tw-Hp-Bg | ≈6 | ≈412 | 0 | ≈418 | ≈522 |
| 500 Hz | Tw-Hp-Fg | ≈6 | ≈412 | ≈160 | ≈578 | ≈682 |
| 1 kHz | Wf-Bp | ≈44 | ≈62 | 0 | ≈106 | ≈210 |
| 1 kHz | Tw-Bp / Tw-Hp-Bg | ≈6 | ≈62 | 0 | ≈68 | ≈172 |
| 1 kHz | Tw-Hp-Fg | ≈6 | ≈62 | ≈64 | ≈132 | ≈236 |

At 500 Hz the woofer wins (tweeter still near resonance); at 1 kHz the tweeter wins (mechanical terms equalize, acoustic offset dominates). The measured worn-device impulse responses show the tweeter path starting ~2 samples (42 µs) earlier than the woofer path — consistent with the geometry.

### Band-limited noise-power reduction $L_{BL}$ at 104 µs virtual delay (L/R averaged)

| Condition | 100–1000 Hz | 100–2000 Hz | 100–4000 Hz |
|-----------|-------------|-------------|-------------|
| Wf-Bp (woofer only) | 7.23 | 5.94 | 4.60 |
| Tw-Bp (tweeter only) | 4.92 | 5.02 | 4.31 |
| Tw-Hp-Fg | 1.04 | 1.92 | 2.25 |
| Tw-Hp-Bg | 2.61 | 3.25 | 3.22 |
| Du-BpBp (reference) | 10.42 | 8.88 | 6.23 |
| Du-BpHp-Fg | 8.77 | 7.92 | 5.88 |
| **Du-BpHp-Bg** | **8.84** | **8.01** | **5.91** |
| Xo-BpBp (reference) | 9.22 | 8.04 | 5.96 |
| **Xo-BpHp** | **8.41** | **7.58** | **5.78** |

Key findings:

- **Two-driver allocation works**: Du-BpHp-Bg exceeds Wf-Bp in *every* octave band from 125 Hz to 4 kHz (by 0.7–3.2 dB) and exceeds Tw-Bp from 125 Hz to 2 kHz.
- **Foreground filter-delay penalty is real**: Tw-Hp-Bg beats Tw-Hp-Fg by 3.9/4.5/1.9 dB at 250/500/1000 Hz — placing the same high-pass filter in the output path consumes causality margin directly. In the full dual-filter architecture the penalty is smaller and path-dependent (joint MSE allocation across branches masks it).
- **Single-filter ≈ dual-filter at half cost**: Xo-BpHp trails Du-BpHp-Bg by only ~1.0 dB at 125 Hz and ~0.7 dB at 1 kHz, other bands close — while halving control-output convolution (294.9 → 147.5 MMAC/s per ear at 48 kHz), coefficient-commitment rate, and coefficient storage (6656 → 3328 coefficients).
- **Delay sweep** ($d = 0–13$ samples, 0–271 µs): degradation is strongest around 500 Hz–1 kHz — not only the top band — because the compact drivers' resonance-related mechanical delay already consumes margin there. Woofer better preserves absolute low-frequency attenuation (6.0 dB at 125 Hz even at $d=13$); tweeter relatively less delay-sensitive in the upper band. At $d \geq 9$ the mid-band advantage of two-driver allocation largely collapses: **two-way allocation cannot compensate for excessive electronic delay**; low-delay electronics and low-delay secondary-path design are *both* required.
- **Sensitivity** (Appendix D): Xo-BpHp is insensitive to cutoff frequency (0.051 dB variation over 100–1500 Hz) and gain-matching bands ending ≤2 kHz; the dual-filter Bg/Fg ranking is cutoff-dependent. Dual-filter conditions become non-attenuating at $\mu \geq 0.08$.

## Key Contributions

1. **Design-oriented secondary-path delay budget**: separates acoustic propagation, mechanical group delay, and crossover-filter group delay as a *design* decomposition (not an exact physical separation of non-minimum-phase worn paths), enabling principled driver-band allocation — no prior work used such a budget to allocate different frequency bands to distinct drivers for broadband ANC.
2. **Coaxial offset 2-way secondary source**: a woofer + forward-mounted tweeter whose complementary delay characteristics (woofer: low mechanical delay below ~500 Hz; tweeter: short acoustic delay above ~1 kHz) reduce the effective secondary-path delay across the target bandwidth, demonstrated on the nwm ONE open-ear headphone.
3. **Three band-splitting architectures with quantified trade-offs**: background dual-filter (delayless output path, structurally favorable), foreground dual-filter, and single-filter composite-path (≈half the foreground convolution/commitment/storage cost) — with MAC-rate, storage, and measured DSP execution-time evidence (ADSP-21569: 66.5% foreground / 79.7% background deadline utilization).
4. **Measured-path validation of driver-band allocation**: 8.01 dB (Du-BpHp-Bg) / 7.58 dB (Xo-BpHp) band-limited pink-noise reduction over 100–2000 Hz versus 5.94/5.02 dB single-driver baselines at 104 µs virtual delay, plus a delay sweep showing where the allocation benefit collapses.

## Related Concepts

- [[concepts/open-ear-headphones|Open-Ear Headphones]]
- [[concepts/feedforward-anc|Feedforward ANC]]
- [[concepts/causality|Causality in ANC]]
- [[concepts/delay-oriented-driver-allocation|Delay-Oriented Driver Allocation]]
- [[concepts/coaxial-two-way-secondary-source|Coaxial Two-Way Secondary Source]]
- [[concepts/anc-attenuation-bounds|ANC Attenuation Bounds]]
- [[concepts/broad-band-feedforward-anc|Broad-Band Feedforward ANC]]
- [[concepts/multi-reference-anc|Multi-Reference ANC]]
- [[concepts/audio-latency|Audio Latency]]
- [[concepts/hearables|Hearables]]

## Related Synthesis

- [[synthesis/application-specific-anc|Application-Specific ANC]]
- [[synthesis/modern-headphone-anc-systems|Modern Headphone ANC Systems]]
