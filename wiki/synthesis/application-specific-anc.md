---
type: synthesis
created: 2026-04-12
updated: 2026-10-24
sources:
  - zotero://select/items/0_M2F5PSAU
  - zotero://select/items/0_TVS87FW6
  - zotero://select/items/0_BQ3P7LZJ
  - zotero://select/items/0_WBAA4H6N
  - raw/papers/serizel-2010-integrated-anc-nr-hearing-aids/full-text.md
  - raw/papers/watanabe-2026-low-frequency-harmonic-control/full-text.md
  - raw/papers/yuan-2026-open-ear-anc-smart-glasses/full-text.md
  - raw/papers/chiba-2027-wideband-anc-coaxial-loudspeaker/full-text.txt
  - wiki/sources/liebich-2022-occlusion-effect-cancellation.md
tags:
  - application-specific-anc
  - drone-anc
  - hearing-aids
  - multi-channel-anc
  - open-ear-anc
  - selective-attenuation
  - occlusion-effect-cancellation
---

# Application-Specific ANC: Form Factor Drives Architecture

> Cross-source synthesis connecting: Steiner & Hilgemann (2026) drone ANC, Yuan et al. (2026) smart glasses, Yang & Wang (2026) vehicle interior, Huang et al. (2026) selective attenuation (Sona), and Serizel et al. (2010) hearing aids.

---

## The Core Insight: "ANC" Is Many Different Problems

The physical form factor and acoustic environment of an ANC system determine its architecture far more than algorithmic preference. Comparing four recent applications reveals fundamentally different control strategies:

| Application | Primary Noise Source | Acoustic Environment | Control Objective | Key Constraint |
|-------------|---------------------|---------------------|-------------------|----------------|
| **Drone** (Steiner 2026) | Propeller(s), co-located | Open field, outdoor | Broadband cancellation | Power, weight, nonstationary RPM |
| **Smart glasses** (Yuan 2026) | Ambient, diffuse | Open-ear (unsealed) | Partial attenuation + awareness | Situational awareness, compute |
| **Open-ear headphones** (Chiba 2027) | Ambient, broadband | Open-ear (unsealed) | Wideband noise reduction | Secondary-path delay budget; causality |
| **Vehicle interior** (Yang 2026) | Engine, road, wind | Sealed 3D cavity, multi-passenger | Multi-zone cancellation | Multi-channel cross-coupling |
| **Selective attenuation** (Huang 2026) | User-selected sources | Variable | Frequency-selective | User preference profile |
| **Hearing aid** (Serizel 2010) | Leakage through open fitting | Open ear canal (tympanic membrane target) | SNR improvement (NR + leakage cancel) | Causality margin of a few samples; ear-canal error mic |

Each requires a different architecture. A single "ANC algorithm" cannot serve all of them.

---

## 1. Drone-Mounted ANC (Steiner & Hilgemann 2026)

### Problem Characteristics

- **Noise source**: Propeller(s) — tonal + broadband, highly nonstationary (RPM changes during flight)
- **Acoustic environment**: Open field — no cavity resonance to exploit
- **Form factor**: Microphones and speakers mounted on the drone body — co-located with the noise source
- **Constraints**: Weight (< 200g for ANC payload), power (< 5W), real-time (< 2ms latency)

### Architecture

```
Propeller noise ──→ Onboard mic ──→ FxLMS controller ──→ Anti-noise speaker
                           ↓
                     RPM estimate (feedforward reference)
```

**Key design choice**: Use propeller RPM as an additional reference signal. This provides:
- A **predictable periodic component** (blade pass frequency and harmonics)
- **Advance warning** of frequency changes before they reach the microphone
- Improved convergence speed for the tonal component

**Algorithm**: Narrow-band FxLMS for tonal harmonics + broadband FxLMS for residual noise.

**Performance**: 8-15 dB reduction at blade pass frequency harmonics. Limited effectiveness at broadband component due to open-field radiation.

---

## 2. Open-Ear Smart Glasses ANC (Yuan et al. 2026)

### Problem Characteristics

- **Noise source**: Ambient environmental noise, diffuse
- **Acoustic environment**: **Open-ear** — the ear canal is not sealed; sound reaches the ear both through air and through the earbud
- **Form factor**: Smart glasses with open-ear speakers, 8-microphone array (4 per side), no in-ear error microphone
- **Constraints**: Must preserve situational awareness, limited compute (CPU + DSP on glasses frame, 5–7 W)

### Architecture: Virtual In-Ear Sensing

[[sources/yuan-2026-open-ear-anc-smart-glasses|Yuan, Liu & Xiao 2026]]'s key innovation: since the ear is **open**, no physical error microphone exists to close an adaptation loop. Their [[concepts/virtual-in-ear-sensing|virtual in-ear sensing]] network instead learns the mapping from frame microphones directly to the ANC **control filters** (not merely the in-ear signal):

```
4 mics per side ──→ STFT + IPD/ILD features (11 ch) ──→ U-Net + LSTM + FiLM ──→ 4 × 2048-tap FIR filters (200 ms refresh)
                                        ↑ secondary-path embedding (FiLM)                    ↓ UDP
                                                              DSP: hybrid partitioned convolution → open-ear speaker (113 μs)
```

**Dual pipeline**:
1. **Neural network** (Raspberry Pi 5 CPU): estimates 2048-tap FIR control filters every 200 ms (4.2M params, 5.3G MACs), trained with an L1 loss on the *in-ear residual*
2. **DSP pipeline** (Bela): applies the filters via [[concepts/hybrid-partitioned-convolution|hybrid partitioned convolution]], 113 μs end-to-end latency

**Performance**: 9.6 dB mean reduction over 100–1000 Hz (no calibration), 11.2 dB (with a ~512-byte ESS secondary-path calibration, +1.6 dB and inter-user std 1.5→0.4 dB) — within 4.3 dB of the 14.7 dB Wiener oracle that needs an actual in-ear microphone. Tested across 8 unseen environments × 11 unseen users; ANC + music playback shows no intelligibility penalty.

**Key challenge**: The open-ear design means anti-noise leaks away and ambient sound enters freely. The neural network must model this complex acoustic coupling in real-time.

**A signal-side alternative (Watanabe et al. 2026)**: instead of controlling the noise, adapt the *playback signal* to the same open-ear constraints — weak low-frequency speaker output and freely-entering low-frequency environmental noise. [[sources/watanabe-2026-low-frequency-harmonic-control|Watanabe et al. 2026]]'s [[concepts/low-frequency-harmonic-control|LFHC]] post-filter suppresses the speech fundamental and emphasizes the 2nd/3rd harmonics, moving energy out of the masked, output-limited band. Where Yuan et al.'s virtual in-ear sensing needs a neural network updating every 200 ms plus a 4-channel 2048-tap DSP pipeline, LFHC needs one comb-filter tap plus a short moving-average low-pass. The form factor again drives the architecture — but toward DSP-minimal *signal adaptation* rather than noise control, trading what ANC cannot achieve in an open field (noise reduction) for what it can (intelligibility gain at −5 dB(A) SNR without volume increase).

**A hardware-side alternative (Chiba et al. 2027)**: attack the causality budget in the *acoustic domain* rather than the sensing or signal domain. [[sources/chiba-2027-wideband-anc-coaxial-loudspeaker|Chiba et al. 2027]]'s [[concepts/coaxial-two-way-secondary-source|coaxial 2-way secondary source]] (35 mm woofer + forward-offset 12 mm tweeter, nwm ONE headphone) applies [[concepts/delay-oriented-driver-allocation|delay-oriented driver allocation]] under an electronic/acoustic/mechanical delay budget: the woofer controls low frequencies (fundamental resonance ≈150 Hz → low mechanical group delay), the tweeter higher frequencies (≈6 µs vs ≈44 µs acoustic path). With a real error microphone at the ear-canal entrance and 3 housing reference microphones per ear, the measured-path offline evaluation reaches 8.01 dB over 100–2000 Hz (dual-filter background) / 7.58 dB (single-filter, at half the convolution and coefficient storage) versus 5.94 dB for the best single driver. The form factor drives the architecture a third way — into *loudspeaker design*: where Yuan et al. remove the error microphone and Watanabe et al. avoid ANC entirely, Chiba et al. keep conventional FxNLMS but reshape the secondary path itself.

---

## 3. Vehicle Interior Multi-Channel ANC (Yang & Wang 2026)

### Problem Characteristics

- **Noise source**: Engine, road, wind — multiple sources, low-frequency dominant
- **Acoustic environment**: **Sealed 3D cavity** (vehicle interior) — complex standing wave patterns, multiple passengers
- **Form factor**: Multiple speakers (phased secondary array) and microphones distributed throughout the cabin
- **Constraints**: Multi-passenger zones must be controlled independently

### Architecture: Phased Secondary Speaker Array

```
Engine/road noise ──→ Reference mics ──→ Multi-channel FxLMS ──→ Phased speaker array
                           ↓                                      ↓
                    Error mics (× zones)                    Zone 1    Zone 2    Zone 3
```

**Key design choice**: Use a **phased secondary speaker array** rather than independent speakers per zone. The phased array:
- Creates **directional anti-noise beams** targeted at specific passenger zones
- Reduces cross-coupling between zones (interference between anti-noise signals)
- Requires fewer speakers than a one-speaker-per-zone approach

**Algorithm**: Multi-channel FxLMS with $O(M \cdot L \cdot N)$ complexity, where $M$ = reference channels, $L$ = filter length, $N$ = secondary speakers.

**Performance**: 6-12 dB reduction at 20-200 Hz (low-frequency vehicle noise). Performance degrades at higher frequencies due to spatial aliasing in the cavity.

---

## 4. Selective Sound Attenuation (Huang et al. 2026, "Sona")

### Problem Characteristics

- **Noise source**: User-selected — the system attenuates sounds the user finds annoying while passing others through
- **Acoustic environment**: Variable — headphones, earbuds, speakers
- **Form factor**: Real-time audio processing system (not limited to headphones)
- **Constraints**: Must preserve user-specified frequency bands (e.g., speech, alarms)

### Architecture: Frequency-Selective Attenuation

```
Input audio ──→ Source separation ──→ Identify target sounds ──→ Selective attenuation
                       ↓
                User preference profile
                (what to attenuate, what to pass)
```

**Key design choice**: Instead of broadband cancellation (traditional ANC), the system performs **source-aware selective attenuation**:
- Identifies individual sound sources (speech, traffic, HVAC, etc.)
- Applies user-specific attenuation profiles per source
- Preserves critical sounds (alarms, speech) while attenuating annoyances

**This is fundamentally different from ANC**: it's not about destructive interference — it's about **semantic sound classification + selective filtering**.

**Performance**: Targeted attenuation of 5-15 dB for specific sources while maintaining transparency for others. Designed for users with noise sensitivity (misophonia, autism, PTSD).

---

## 5. Hearing-Aid ANC + Noise Reduction (Serizel et al. 2010)

### Problem Characteristics

- **Noise source**: The [[concepts/open-fitting-noise-leakage|leakage]] — ambient noise entering the ear canal directly through the open fitting, unprocessed and with lower SNR than the hearing-aid output
- **Acoustic environment**: Open ear canal; the zone of quiet is the **tympanic membrane**, and the secondary path (loudspeaker → eardrum) attenuates the processed signal (dc gain < 1)
- **Form factor**: Two-microphone BTE hearing aid; assumes an ear-canal error microphone (technically feasible on the eartip, absent from commercial devices)
- **Constraints**: The microphone–loudspeaker distance is a few centimeters, leaving a causality margin of only **a few samples** (ν = 2 measured for a 270° noise DOA) — the tightest latency budget of any application in this comparison

### Architecture: Integrated ANC + NR (FxMWF)

Uniquely among these applications, the hearing aid must run ANC *jointly* with noise reduction. Serizel et al. show the topology decides everything: cascading NR and ANC fails twice (the ANC input is the noise-suppressed NR output, and the NR delay of 32 samples consumes the two-sample causality margin), while the integrated [[concepts/filtered-x-mwf|Filtered-x MWF]] merges both functions into one filter set on secondary-path-filtered references. The filter provably decomposes into an NR part and an ANC part that is *independent of the NR delay*, so no NR/ANC performance trade-off exists.

**Performance**: ~12 dB intelligibility-weighted SNR improvement (vs. ~4 dB cascaded at a relaxed ν = 48; >10 dB vs. ~1 dB cascaded at the realistic ν = 2). In the non-causal regime the ANC benefit vanishes, but secondary-path-aware NR still outperforms standard MWF-NR.

**Key challenge**: The open fitting trades the occlusion effect for leakage — the exact inversion of the sealed-earbud assumption. Combined with the few-sample causality margin, this makes the hearing aid the most constraint-bound ANC application in this comparison.

**The sealed-fitting alternative**: [[sources/liebich-2022-occlusion-effect-cancellation|Liebich & Vary 2022]] show the trade-off can be taken in the other direction — keep the sealed fitting and remove the occlusion effect *actively*. Their [[concepts/occlusion-effect-cancellation|OEC]] uses the same inner+outer microphone pair as the FxMWF hearing aid, but with $\mathcal{H}_\infty$ feedback control attenuating the amplified body-conducted low frequencies (50–700 Hz) and a hear-through feedforward filter restoring the attenuated air-conducted high frequencies, decoupled via a correction filter $\hat{G}(z) = G(z)$. A 23-participant listening test confirms restored own-voice naturalness (Δη = 1.67), and the same hardware switches between ANC and OEC modes by exchanging filter coefficients — an operation-mode dimension none of the other applications in this comparison needs.

---

## 6. Cross-Application Comparison

### 6.1 Architecture Drivers

| Factor | Drone | Smart Glasses | Vehicle | Selective | Hearing Aid |
|--------|-------|--------------|---------|-----------|-------------|
| **Sealed vs Open** | Open | Open | Sealed | Variable | Open (fitting) |
| **Noise predictability** | High (RPM-based) | Low (diffuse) | Medium (engine periodic) | Variable | Low (babble) |
| **Channel count** | 1-2 | 8 mic + 4 speaker | Multi-channel (M×N) | 2 (stereo) | 2 mic + 1 error |
| **Primary algorithm** | Narrow-band FxLMS | Neural + DSP hybrid | Multi-channel FxLMS | Source separation + filter | FxMWF (integrated NR + ANC) |
| **Latency budget** | < 2ms | 113μs (DSP) + 200ms (NN) | < 5ms | < 20ms | ~2 samples (~125μs) |
| **Power budget** | < 5W | < 1W (glasses frame) | < 50W (vehicle) | < 10W (device) | mW-scale (hearing aid) |

### 6.2 What "Performance" Means

| Application | Metric | Target | Achieved |
|-------------|--------|--------|----------|
| Drone | NR at blade pass freq. | > 10 dB | 8-15 dB |
| Smart glasses | Overall NR | > 10 dB | 9.6-11.2 dB |
| Vehicle | NR at 20-200 Hz | > 8 dB | 6-12 dB |
| Selective | Target source attenuation | > 10 dB | 5-15 dB |
| Hearing aid | Intelligibility-weighted SNR improvement | > 10 dB | ~12 dB (integrated); ~4 dB (cascaded) |

### 6.3 The Open vs. Sealed Divide

The most fundamental architectural split is **open-ear vs. sealed-ear**:

| Aspect | Sealed (Vehicle, Headphones) | Open (Glasses, Drone) |
|--------|----------------------------|----------------------|
| Anti-noise containment | High (sealed cavity) | Low (leaks freely) |
| Reference signal quality | Good (error mic inside) | Poor (estimated/virtual) |
| Algorithm complexity | Lower (well-defined plant) | Higher (complex coupling) |
| Maximum achievable NR | 15-30 dB | 8-15 dB |

### 5.4 The Algorithm Convergence

Despite their differences, all four applications converge on a common pattern:

1. **Characterize the noise** (RPM, ambient, engine, source-specific)
2. **Generate anti-noise** (FxLMS, neural, multi-channel, source separation)
3. **Adapt to changing conditions** (nonstationary RPM, user movement, road surface, user preference)

The specific implementation of each step differs, but the **sense-act-adapt loop** is universal.

---

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/broad-band-feedforward-anc|Broad-Band Feedforward ANC]]
- [[concepts/narrow-band-feedforward-anc|Narrow-Band Feedforward ANC]]
- [[concepts/multi-channel-anc|Multi-Channel ANC]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/feedback-anc|Feedback ANC]]
- [[concepts/hybrid-anc|Hybrid ANC]]
- [[concepts/occlusion-effect-cancellation|Occlusion Effect Cancellation]]
- [[concepts/virtual-in-ear-sensing|Virtual In-Ear Sensing]] — the error-microphone-free enabler of the smart-glasses application
- [[concepts/hybrid-partitioned-convolution|Hybrid Partitioned Convolution]] — real-time long-filter replay on wearables
- [[concepts/open-ear-headphones|Open-Ear Headphones]] — the form-factor class driving the glasses constraint set
- [[concepts/coaxial-two-way-secondary-source|Coaxial Two-Way Secondary Source]] — loudspeaker-side answer to the open-ear delay dilemma
- [[concepts/delay-oriented-driver-allocation|Delay-Oriented Driver Allocation]] — driver-band assignment by delay characteristics under a causality budget

## Related Sources

- [[sources/watanabe-2026-low-frequency-harmonic-control|Watanabe et al. 2026: Low-Frequency Harmonic Control for Speech Intelligibility in Open-Ear Headphones]] — signal-side alternative to open-ear ANC: reallocate harmonic energy instead of canceling noise
- [[sources/yuan-2026-open-ear-anc-smart-glasses|Yuan, Liu & Xiao 2026: Active Noise Cancellation on Open-Ear Smart Glasses]] — first working open-ear ANC: virtual in-ear sensing + FiLM secondary-path conditioning, 11.2 dB with per-user calibration
- [[sources/chiba-2027-wideband-anc-coaxial-loudspeaker|Chiba, Kamado, Kako & Noguchi 2027: Wideband ANC for Open-Ear Headphones with a Coaxial Loudspeaker]] — hardware-side open-ear ANC: delay-budgeted woofer/tweeter band allocation, 8.01 dB over 100–2000 Hz in measured-path evaluation
- [[sources/liebich-2022-occlusion-effect-cancellation|Liebich & Vary 2022: Occlusion Effect Cancellation in Headphones and Hearing Devices]] — sealed-fitting alternative to the open-fitting trade-off: active OEC restores own-voice naturalness on closed hardware
