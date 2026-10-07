---
type: source
created: 2026-10-07
updated: 2026-10-07
sources:
  - raw/papers/liebich-2022-occlusion-effect-cancellation/full-text.md
  - https://doi.org/10.1109/TASLP.2021.3130966
  - zotero://select/items/0_U2BVZM66
tags:
  - active-noise-control
  - occlusion-effect
  - occlusion-effect-cancellation
  - hear-through
  - headphones
  - hearing-aids
  - feedback-control
  - robust-control
---

# Liebich & Vary 2022: Occlusion Effect Cancellation in Headphones and Hearing Devices

**Authors**: [[entities/stefan-liebich|Stefan Liebich]], [[entities/peter-vary|Peter Vary]]

**Institutions**: Institute of Communication Systems, RWTH Aachen University

**Venue**: IEEE/ACM Transactions on Audio, Speech, and Language Processing (TASLP), vol. 30, 2022

**Year**: 2022 | **Type**: Journal Article | **DOI**: [10.1109/TASLP.2021.3130966](https://doi.org/10.1109/TASLP.2021.3130966)

**Zotero**: [U2BVZM66](zotero://select/items/0_U2BVZM66)

**Note**: Journal extension of two conference papers — Liebich et al. 2018 (OEC with hear-through equalization, ICASSP) and [[sources/liebich-2018-doa-dependency-anc-headphones|Liebich et al. 2018 (DOA dependency of ANC headphones, INTERNOISE)]].

## Summary

This paper provides a comprehensive joint treatment of **occlusion effect cancellation (OEC)** and its "sister" [[concepts/active-noise-control|Active Noise Cancellation (ANC)]]. Occluding the ear canal amplifies body-conducted sound at low frequencies and attenuates air-conducted sound at high frequencies, making one's own voice sound boomy. The authors present a novel OEC filter structure — combined feedforward-feedback control with a correction filter $\hat{G}(z)$ that decouples the hear-through filter design from the feedback controller — plus an adaptive factor $\alpha$ for stability/performance tuning and manual gains for personal preference. Listening tests with 23 participants confirm significant improvement of own-voice naturalness, and objective measurements show the flattened occlusion function.

## Problem Formulation

The occlusion effect (OE) arises when headphones, headsets, or hearing aids fully or partially occlude the ear canal:

- **Body-conducted (BC) sounds** (own voice, chewing, swallowing, footsteps) are radiated into the ear canal via the vibrating ear-canal walls and are **amplified at low frequencies** (mainly below 700 Hz).
- **Air-conducted (AC) sounds** are **attenuated** by the earpiece, predominantly at high frequencies.

Own-voice dissatisfaction affects 27% of hearing-aid users (chewing/swallowing: 36%), and own-voice perception correlates with overall satisfaction (r = 0.6, MarkeTrak VIII). Passive remedies — vents/open fittings (risking acoustic feedback and leakage) or deep insertion (physical discomfort) — all have drawbacks.

**Measuring the OE.** The ideal occlusion function is the ratio of eardrum spectra between occluded and open ear:

$$OE = \frac{|D_{\mathrm{occl}}|}{|D_{\mathrm{open}}|} = \frac{|\mathrm{REOG} \cdot X_{\mathrm{AC}} + H_{\mathrm{BC,occl}} \cdot X_{\mathrm{BC}}|}{|\mathrm{REUG} \cdot X_{\mathrm{AC}} + H_{\mathrm{BC,open}} \cdot X_{\mathrm{BC}}|}$$

Since vocal excitation is not exactly repeatable, the measurable occlusion function uses simultaneous inner/outer microphone signals:

$$\widetilde{OE} = \frac{|E|}{|X|} = \frac{|P \cdot X_{\mathrm{AC}} + H_{\mathrm{BC,mic}} \cdot X_{\mathrm{BC}}|}{|X_{\mathrm{AC}}|}$$

with two assumptions: BC sound in the open ear is negligible (15–40 dB below AC, 300 Hz–6 kHz), and the inner-microphone-to-eardrum transfer is $H_{\mathrm{EC}} \approx 1$ (valid below the open-canal resonance of 2–3 kHz).

![[raw/papers/liebich-2022-occlusion-effect-cancellation/figures/0561d52c002178f8bed34ac90d28baa00c0f0314b3ec42d68d3252b9c98241d9.jpg|Occlusion effect measurements from various studies]]
*Figure 9: Occlusion effect measurements $\widetilde{OE}(f)$ from various studies (Wimmer, Thorup, May) with vocalized or bone-transducer excitation, overlayed with the authors' measurement of one subject vocalizing [i:] wearing a deactivated Bose QC20. All show the typical low-frequency amplification and high-frequency attenuation.*

## Methodology

### ANC Primer: Combined Feedforward-Feedback Control

The paper first reviews the shared ANC machinery: a feedforward filter $W(z)$ driven by the outer microphone and a feedback controller $K(z)$ driven by the inner microphone, with primary path $P(z)$ (outer→inner), secondary path $G(z)$ (loudspeaker→inner), and acoustic feedback $F(z)$. The error signal (neglecting $F$):

$$E = \left(\frac{P - GW}{1 + GK}\right)X$$

with the [[concepts/sensitivity-function|sensitivity function]] $S = \frac{1}{1+GK}$ and complementary sensitivity $T = \frac{GK}{1+GK}$, constrained by $S + T = 1$. The ideal feedforward filter $W(z) = P(z)/G(z)$ is unrealizable (latency, non-minimum phase); a causal FIR approximation follows the Wiener-Hopf equation $\hat{w} = R_{gg}^{-1} \varphi_{pg}$. The feedback controller is designed by mixed-sensitivity $\mathcal{H}_\infty$ synthesis with secondary-path uncertainty margins.

![[raw/papers/liebich-2022-occlusion-effect-cancellation/figures/2bdc54c4c49ae51db44d9e62c0dd7a05ecde04a4654b5a772ddaf7618b1ea834.jpg|Combined feedforward-feedback control structure]]
*Figure 3: Combined feedforward-feedback control structure with measurement noise. Digital filters (white) and discrete-time models of acoustic paths (gray).*

Accuracy demands are severe: for $Att > 20$ dB the compensation signal needs magnitude deviation $\Delta A_{\mathrm{rel}} < 1$ dB and phase deviation $|\Delta\phi| < 6°$ (cf. [[concepts/anc-attenuation-bounds|ANC Attenuation Bounds]]). Path variations compound this: the primary path varies with DOA (4608 measured directions), the secondary path with fitting/ear-canal geometry (46 measurements across 23 subjects).

### OEC Structure with Correction Filter

OEC exploits the ANC machinery for a different target: **natural own-voice perception** instead of silence. The BC amplification is attenuated by feedback control (inner microphone); the AC attenuation is compensated by a hear-through feedforward filter $W(z)$ (outer microphone). The key novelty is a **correction filter** $\hat{G}(z)$ fed with the hear-through signal $u_W(n)$ and added to the inner-microphone signal before the feedback controller. The overall transfer function becomes:

$$E = \underbrace{X\left(\frac{P}{1 + KG}\right)}_{\text{primary AC contr.}} - \underbrace{X\left(GW\frac{1 + K\hat{G}}{1 + KG}\right)}_{\text{equalized AC contr.}} + \underbrace{D_{\mathrm{BC}}\left(\frac{1}{1 + KG}\right)}_{\text{BC contr.}}$$

For $\hat{G}(z) = G(z)$ the designs of $W(z)$ and $K(z)$ are **decoupled** — the major advantage over Kuo's hybrid structure (where the correction filter input is $u(n)$, altering the feedback loop and requiring a different controller).

![[raw/papers/liebich-2022-occlusion-effect-cancellation/figures/c3bd1bf9b4ddff40406a77613d9dc7d3b34fdb0a2e146c5fd4d1fe7fee427e94.jpg|Basic OEC structure]]
*Figure 11: Basic structure for occlusion effect cancellation (OEC) with feedback controller input correction by $u_W(n) * \hat{g}(n)$.*

### Feedback Controller and Hear-Through Filter Design

The feedback controller $K(z)$ is designed by $\mathcal{H}_\infty$ synthesis such that the sensitivity $S(z)$ attenuates 50–700 Hz where the OE is most prominent — ideally $S(z)$ corresponds to the inverse occlusion function. Slight amplification in 1.5–4 kHz is an unavoidable [[concepts/waterbed-effect|waterbed effect]], accounted for in the hear-through design.

![[raw/papers/liebich-2022-occlusion-effect-cancellation/figures/22551911326fc39370984dba846bbe5c68f11471a5aa0341ea284793e9285c92.jpg|Feedback controller and sensitivity]]
*Figure 12: Feedback controller $K(z)$ and sensitivity $S(z)$ together with the underlying secondary path $G(z)$. Attenuation in 50–700 Hz; waterbed amplification in 1.5–4 kHz.*

The hear-through filter targets transparent transmission $\frac{E}{X} \stackrel{!}{=} z^{-\tau}$:

$$W(z) = \frac{P(z)S(z) - z^{-\tau}}{G(z)}$$

realized via the Wiener-Hopf equation with $R(z) = P(z)S(z) - z^{-\tau}$. Qualitatively $W(z)$ is inverse to $P(z)$: it re-amplifies the previously attenuated air-conducted components.

![[raw/papers/liebich-2022-occlusion-effect-cancellation/figures/a5e4d70d6efe26ab9606634231f84af14e737e00367bac0b8a0ab7fadf693f5c.jpg|Hear-through filter and overall transfer function]]
*Figure 13: Hear-through filter $W(z)$ (inverse to the primary path $P(z)$) and the resulting overall transfer function.*

### Adaptive Factor α

The robust controller is time-invariant, but individual paths vary. An adaptive factor $\alpha$ scales the feedback loop gain (sensitivity $S_\alpha = \frac{1}{1 + G\alpha K}$) based on the normalized cross-correlation between the corrected error signal $\tilde{e}(n)$ and an estimated compensation signal $\hat{y}(n)$, both smoothed by first-order IIR filters ($\beta = 0.999$ at 48 kHz):

$$\alpha = 1 - \frac{\hat{\varphi}_{e\hat{y}}(n)}{\sqrt{\hat{\varphi}_{ee}(n)\hat{\varphi}_{\hat{y}\hat{y}}(n)}} = 1 - \hat{\Psi}_{e\hat{y}}(n), \quad 0 \leq \alpha \leq 2$$

Values $0 \leq \alpha < 1$ improve **stability**; $1 < \alpha \leq 2$ increase **performance**.

### Adjustable System and ANC/OEC Switching

The full system exposes three manual gains for personal preference: $g_{\mathrm{FB}}$ (body-conducted attenuation), $g_{\mathrm{HT}}$ (air-conducted perception), $g_{\mathrm{A}}$ (desired audio level, e.g., music with equalizer $W_a = U/G$ for a target curve $U$ such as the Harman curve).

![[raw/papers/liebich-2022-occlusion-effect-cancellation/figures/32f9661295acd721ea7722629b909f5065d06bd63fda3c55bfd158ff74ca00d2.jpg|Adjustable OEC system]]
*Figure 14: Adjustable occlusion effect cancellation system with adaptive factor $\alpha$ and manual gains $g_{\mathrm{FB}}, g_{\mathrm{HT}}, g_{\mathrm{A}}$.*

The same structure switches between **ANC and OEC modes by exchanging filter coefficients**: $W(z) = P/G$ and $\hat{G} = 0$ for ANC; $W(z) = (PS - z^{-\tau})/G$, robust $K_{\mathrm{OEC}}$, and $\hat{G} = G$ for OEC. Both modes require ultra-low latency of 20–40 μs.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Participants | 23 normal-hearing (20 male, 3 female), ages 21–61 (avg. 31) |
| Headphone | Bose QC20 (in-ear) |
| Real-time platform | dSPACE DS1005 (DS2004/DS2102 boards); informal tests on Analog Devices ADAU 1777 |
| Sampling rate | 48 kHz |
| Adaptive factor | $\beta = 0.999$, $0 \leq \alpha \leq 2$ |
| Test environment | Acoustic booth (STUDIOBOX Premium, 44 dB attenuation) |
| Speech material | TIMIT sentences sa1, sx32, sx198 |
| Test design | Full-factorial paired comparison, 5-point Likert scale (−2…+2), 12 randomized blind comparisons per part, least-squares scoring, paired t-tests |
| Settings | A: passive (FB off, HT off); B: HT only; C: FB only; D: FB+HT; E: FB+HT individually tuned ($g_{\mathrm{FB}}, g_{\mathrm{HT}}$) |
| Objective measurement | $\widetilde{OE}(f)$ from inner/outer microphone recordings (part T3), 46 ears × 5 settings |

## Results

### Subjective (parts T1/T2)

| Comparison | Mean score distance $\overline{\Delta\eta}$ | p-value | Note |
|------------|------|---------|------|
| B (HT only) vs A | 1.02 | < 0.000005 | 20/23 subjects preferred B |
| C (FB only) vs A | 0.370 | < 0.0127 | marginal improvement only |
| D (FB+HT) vs B | 0.576 | < 0.008 | 18/23 preferred D over B |
| D vs A | 1.592 | < 0.000008 | |
| E (tuned) vs D | 0.377 | < 0.027 | 16/23 preferred E |
| E vs A | 1.667 | < 9·10⁻¹³ | 22/23 preferred E |

Key insight: solving only the BC amplification (setting C) does **not** achieve natural own-voice perception — hear-through (AC restoration) is essential, and combining both with individual tuning (E) works best. Outliers trace to hear-through noise (16-bit ADC dynamic range) and incipient instability for two subjects when $\alpha \to 2$.

![[raw/papers/liebich-2022-occlusion-effect-cancellation/figures/2f7e0c13c38a29adc69c3c5977bbc5e207ccdc9b0df78dc12689cb78fcd93c05.jpg|Listening test scores T1]]
(a) (T1) with default settings for all participants.

![[raw/papers/liebich-2022-occlusion-effect-cancellation/figures/49075220e946619e11f92c4b2a0f79543b6386e7f002983dd70b5e9fcd38b73c.jpg|Listening test scores T2]]
(b) (T2) including individually tuned setting E.

*Figure 16: Scores from parts (T1) and (T2) of the listening test. Settings A–D according to Table 2; ratings 0 = equal, 1 = better, 2 = much better.*

### Objective (part T3)

The occlusion functions $\widetilde{OE}(f)$ (median over left ears, 1/3-octave smoothed) show: setting A the typical passive earplug curve; B raises the high frequencies toward 0 dB; C significantly reduces 100–400 Hz; E (tuned FB+HT) yields a nearly spectrally flat $\widetilde{OE}(f)$ — both OE symptoms compensated to a large extent.

![[raw/papers/liebich-2022-occlusion-effect-cancellation/figures/6901dc9873e2ec2f33f7e71de6cbf3bd9bfcfa93041c3ff9aa3f731d850f7842.jpg|Occlusion function setting A]]
(a) Setting A — Passive Earplug

![[raw/papers/liebich-2022-occlusion-effect-cancellation/figures/937237cbc62971bcd6c53801cfc384b143336e9a9f59701c29c836ae1054a0dc.jpg|Occlusion function setting B]]
(b) Setting B — Only HT

![[raw/papers/liebich-2022-occlusion-effect-cancellation/figures/e2710b2787f3e250add0167024b86ca934bb3288386daa7c55e922264a77a0d2.jpg|Occlusion function setting C]]
(c) Setting C — Only FB

![[raw/papers/liebich-2022-occlusion-effect-cancellation/figures/e5c23b1e3e06b4667afcc4fcce7c9dee92e2049d8cb80929d62b724b130f7256.jpg|Occlusion function setting E]]
(d) Setting E — FB+HT tuned

*Figure 17: Occlusion functions $\widetilde{OE}(f)$ for left ears of test part (T3) with 1/3-octave band smoothing.*

### ANC Performance

Median overall gain over 72 horizontal-plane directions (dummy head): the combined FFFB mode outperforms FB-only (attenuates < 600 Hz) and FF-only (attenuates < 1.3 kHz), especially below 400 Hz. Compared to the manufacturer's (Bose) electronics: Bose is better below 330 Hz and above 700 Hz; FFFB is stronger in 330–700 Hz — attributable to different design targets.

![[raw/papers/liebich-2022-occlusion-effect-cancellation/figures/dbbcbed233acfda4ff5b4795c4f77f61e87949907a5cca148ac541582646540b.jpg|Overall ANC gain]]
*Figure 18: Overall ANC gain including active and passive attenuation (median of 72 directions, dummy head).*

## Key Contributions

1. **Joint OEC/ANC treatment**: first comprehensive joint formulation of occlusion effect cancellation and active noise cancellation, explicating shared principles (combined feedforward-feedback control, 20–40 μs ultra-low latency) and contrary objectives (silence vs. natural own-voice perception).
2. **Novel OEC structure with correction filter**: inserting $\hat{G}(z) = G(z)$ fed by the hear-through signal into the feedback controller input decouples the designs of $W(z)$ and $K(z)$ — unlike Kuo's hybrid structure where the correction alters the feedback loop.
3. **Adaptive factor α**: normalized cross-correlation-based loop-gain scaling ($0 \leq \alpha \leq 2$) that improves stability below 1 and performance above 1.
4. **Adjustable system with mode switching**: manual gains ($g_{\mathrm{FB}}, g_{\mathrm{HT}}, g_{\mathrm{A}}$) for personal preference; switching between ANC and OEC modes by exchanging filter coefficients.
5. **Combined subjective and objective validation**: 23-participant listening test (naturalness) plus objective occlusion-function measurements (46 ears), showing that hear-through and feedback control must be combined — feedback alone is insufficient.
6. **Measurement methodology for the occlusion function**: systematic comparison of OE measurement approaches and their assumptions (BC-open neglect, $H_{\mathrm{EC}} \approx 1$), with cross-study measurement comparison (Wimmer, Thorup, May).

## Related Concepts

- [[concepts/occlusion-effect-cancellation|Occlusion Effect Cancellation]] — the paper's central contribution
- [[concepts/ear-canal-occlusion-effect|Ear Canal Occlusion Effect]] — the phenomenon being cancelled
- [[concepts/transparency-mode|Transparency Mode]] — hear-through equalization as the feedforward component
- [[concepts/hybrid-anc|Hybrid ANC]] — shared feedforward-feedback architecture
- [[concepts/sensitivity-function|Sensitivity Function]] — feedback design objective (inverse occlusion function)
- [[concepts/waterbed-effect|Waterbed Effect]] — unavoidable 1.5–4 kHz amplification
- [[concepts/robust-control|Robust Control]] — $\mathcal{H}_\infty$ mixed-sensitivity controller synthesis
- [[concepts/anc-attenuation-bounds|ANC Attenuation Bounds]] — accuracy requirements (<1 dB, <6° for 20 dB)
- [[concepts/primary-path-variability|Primary Path Variability]] — DOA-dependent $P(z)$
- [[concepts/feedforward-anc|Feedforward ANC]] / [[concepts/feedback-anc|Feedback ANC]] — the two control components

## Related Synthesis

- [[synthesis/modern-headphone-anc-systems|Modern Headphone ANC Systems]] — occlusion effect as an ANC trade-off
- [[synthesis/application-specific-anc|Application-Specific ANC]] — hearing aids vs. headphones constraint comparison
