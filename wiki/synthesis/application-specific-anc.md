---
type: synthesis
created: 2026-04-12
updated: 2026-04-12
sources:
- zotero://select/items/0_M2F5PSAU
- zotero://select/items/0_TVS87FW6
- zotero://select/items/0_BQ3P7LZJ
- zotero://select/items/0_WBAA4H6N
tags:
- application-specific-anc
- drone-anc
- multi-channel-anc
- open-ear-anc
- selective-attenuation
---

# Application-Specific ANC: Form Factor Drives Architecture

> Cross-source synthesis connecting: Steiner & Hilgemann (2026) drone ANC, Yuan et al. (2026) smart glasses, Yang & Wang (2026) vehicle interior, and Huang et al. (2026) selective attenuation (Sona).

---

## The Core Insight: "ANC" Is Many Different Problems

The physical form factor and acoustic environment of an ANC system determine its architecture far more than algorithmic preference. Comparing four recent applications reveals fundamentally different control strategies:

| Application | Primary Noise Source | Acoustic Environment | Control Objective | Key Constraint |
|-------------|---------------------|---------------------|-------------------|----------------|
| **Drone** (Steiner 2026) | Propeller(s), co-located | Open field, outdoor | Broadband cancellation | Power, weight, nonstationary RPM |
| **Smart glasses** (Yuan 2026) | Ambient, diffuse | Open-ear (unsealed) | Partial attenuation + awareness | Situational awareness, compute |
| **Vehicle interior** (Yang 2026) | Engine, road, wind | Sealed 3D cavity, multi-passenger | Multi-zone cancellation | Multi-channel cross-coupling |
| **Selective attenuation** (Huang 2026) | User-selected sources | Variable | Frequency-selective | User preference profile |

Each requires a different architecture. A single "ANC algorithm" cannot serve all four.

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
- **Form factor**: Smart glasses with earbud speakers, 8-microphone array
- **Constraints**: Must preserve situational awareness, limited compute (DSP on glasses frame)

### Architecture: Virtual In-Ear Perception

Yuan et al.'s key innovation: since the ear is **open**, you cannot measure the in-ear acoustic field directly. Instead, they train a **neural network** to estimate the in-ear sound pressure from the 8-microphone array on the glasses frame:

```
8-mic array on glasses ──→ U-Net + LSTM + FiLM ──→ Estimate in-ear pressure
                                                        ↓
                                                 DSP anti-noise generation
                                                        ↓
                                                 4-channel FIR filter (2048-tap)
```

**Dual pipeline**:
1. **Neural network** (CPU): Estimates virtual in-ear pressure, updates every 200ms
2. **DSP pipeline** (dedicated): Generates anti-noise via hybrid convolution, 113μs end-to-end latency

**Performance**: 9.6 dB noise reduction (no calibration), 11.2 dB (with user-specific calibration). Tested across 8 environments × 11 users.

**Key challenge**: The open-ear design means anti-noise leaks away and ambient sound enters freely. The neural network must model this complex acoustic coupling in real-time.

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

## 5. Cross-Application Comparison

### 5.1 Architecture Drivers

| Factor | Drone | Smart Glasses | Vehicle | Selective |
|--------|-------|--------------|---------|-----------|
| **Sealed vs Open** | Open | Open | Sealed | Variable |
| **Noise predictability** | High (RPM-based) | Low (diffuse) | Medium (engine periodic) | Variable |
| **Channel count** | 1-2 | 8 mic + 4 speaker | Multi-channel (M×N) | 2 (stereo) |
| **Primary algorithm** | Narrow-band FxLMS | Neural + DSP hybrid | Multi-channel FxLMS | Source separation + filter |
| **Latency budget** | < 2ms | 113μs (DSP) + 200ms (NN) | < 5ms | < 20ms |
| **Power budget** | < 5W | < 1W (glasses frame) | < 50W (vehicle) | < 10W (device) |

### 5.2 What "Performance" Means

| Application | Metric | Target | Achieved |
|-------------|--------|--------|----------|
| Drone | NR at blade pass freq. | > 10 dB | 8-15 dB |
| Smart glasses | Overall NR | > 10 dB | 9.6-11.2 dB |
| Vehicle | NR at 20-200 Hz | > 8 dB | 6-12 dB |
| Selective | Target source attenuation | > 10 dB | 5-15 dB |

### 5.3 The Open vs. Sealed Divide

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

- [[../concepts/active-noise-control|Active Noise Control]]
- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[../concepts/broad-band-feedforward-anc|Broad-Band Feedforward ANC]]
- [[../concepts/narrow-band-feedforward-anc|Narrow-Band Feedforward ANC]]
- [[../concepts/multi-channel-anc|Multi-Channel ANC]]
- [[../concepts/beamforming|Beamforming]]
- [[../concepts/feedback-anc|Feedback ANC]]
- [[../concepts/hybrid-anc|Hybrid ANC]]

## Related Sources
