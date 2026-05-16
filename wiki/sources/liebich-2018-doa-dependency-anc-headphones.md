---
type: source
created: 2026-05-05
updated: 2026-05-05
sources:
  - raw/papers/liebich-2018-doa-dependency-anc-headphones/full-text.md
  - https://doi.org/10.1115/NCAD2018-6120
  - zotero://select/items/0_T9JAV2ND
tags:
  - active-noise-control
  - direction-of-arrival
  - headphones
  - hrtf
  - feedforward-anc
  - feedback-anc
  - hybrid-anc
---

# Liebich, Richter, Fabry, Durand, Fels & Jax 2018: Direction-of-Arrival Dependency of ANC Headphones

**Authors**: [[entities/stefan-liebich|Stefan Liebich]], [[entities/jan-gerrit-richter|Jan-Gerrit Richter]], [[entities/johannes-fabry|Johannes Fabry]], [[entities/christopher-durand|Christopher Durand]], [[entities/janina-fels|Janina Fels]], [[entities/peter-jax|Peter Jax]]

**Institutions**: Institute of Communication Systems & Institute of Technical Acoustics, RWTH Aachen University

**Venue**: ASME 2018 Noise Control and Acoustics Division Session at INTERNOISE 2018

**Year**: 2018 | **Type**: Conference Paper | **DOI**: [10.1115/NCAD2018-6120](https://doi.org/10.1115/NCAD2018-6120)

**Zotero**: [T9JAV2ND](zotero://select/items/0_T9JAV2ND)

## Summary

This paper investigates how the direction of arrival (DOA) of sound affects ANC performance in in-ear headphones. Using device-specific head-related transfer functions (DHRTF) measured on a dummyhead with Bose QC20 headphones across 4608 directions, the authors show that the primary path $P(z)$ varies significantly with DOA, especially above 1 kHz. Since feedforward ANC relies on $P(z)$, its attenuation is DOA-dependent, while feedback ANC (dependent only on $G(z)$) is not. A novel analytical bound on attenuation as a function of magnitude and phase deviation is derived, showing that 20 dB attenuation requires <0.83 dB amplitude error and <5.76° phase error.

## Problem Formulation

The core problem is that time-invariant ANC filters are optimized for a specific primary path $P(z)$, which describes the acoustic transfer from the outer to the inner microphone. When the sound source moves, $P(z)$ changes, degrading the match between the anti-noise and the actual disturbance.

The optimal feedforward filter is:

$$\hat{W}_{\text{opt}}(z) = \frac{P(z)}{G(z)}$$

Since $G(z)$ is DOA-independent (loudspeaker and inner microphone are fixed), DOA dependency enters solely through $P(z)$. The causal FIR approximation uses the Wiener-Hopf equation:

$$\hat{w} = \Psi_{g,g}^{-1} \cdot \varphi_{p,g}$$

For feedback ANC, the sensitivity function is:

$$S_{\text{FB}}(z) = \frac{1}{1 + G(z)K(z)}$$

which depends only on $G(z)$ and the controller $K(z)$, not on $P(z)$, making feedback ANC inherently DOA-independent.

## Methodology

### Attenuation Bound Derivation

The paper derives a closed-form expression for the attenuation achieved by anti-phase compensation given amplitude and phase deviations. For a disturber $A \cos(\omega t)$ and compensation $B \cos(\omega t + \Delta\phi)$:

$$\text{Gain} = 1 - 2\Delta A_{\text{rel}} \cos(\Delta\phi) + \Delta A_{\text{rel}}^2$$

where $\Delta A_{\text{rel}} = B/A$. The relative amplitude deviation for a target attenuation is:

$$\Delta A_{\text{rel}} = \cos(\Delta\phi) \pm \sqrt{\cos^2(\Delta\phi) - (1 - \text{Gain})}$$

![Attenuation boundary curves for different target attenuations](raw/papers/liebich-2018-doa-dependency-anc-headphones/figures/77a8dacef63f0503e4e34de42e2a4482a61a6bbe90daeae5c50677734ac77622.jpg)
*Figure 5: Attenuation boundary curves. Deviations below the curve achieve the indicated attenuation; deviations above result in amplification.*

### DHRTF Measurement Setup

Two measurement campaigns were conducted:

1. **Full-sphere DHRTF** (M = 4608 directions): 64 loudspeakers on a half-circle, rotating platform, frequency range 350 Hz–24 kHz
2. **Horizontal plane** (M = 72 directions): Single Neumann KH120A loudspeaker, frequency range 20 Hz–24 kHz (extended low-frequency coverage)

Both used a Head Acoustics HMS II.3 dummyhead with Bose QC20 in-ear headphones (without Bose electronics). Sampling rate: 48 kHz. Measurements every 5° in azimuth.

### Primary Path Deviation Metrics

Relative magnitude deviation:

$$\Delta P_{\text{rel}}(z) = \left|\frac{P_i(z) - P_n(z)}{P_n(z)}\right|$$

Phase deviation:

$$\Delta\angle P(z) = |\angle P_i(z) - \angle P_n(z)|$$

where $P_n(z)$ is the nominal primary path (lateral left, $\theta=90°$, $\varphi=-90°$).

### Active Measurement Setup

Five ANC settings measured on the horizontal plane:
- **Passive**: No active compensation
- **FB**: Feedback controller only
- **FF**: Feedforward controller only (Wiener-Hopf FIR)
- **FFFB**: Combined feedforward + feedback
- **BoseElec**: Original Bose QC20 electronics

Bose QC20 connected to dSPACE DS1005 real-time system (1-sample round-trip delay excluding acoustics).

## Experimental Setup

| Parameter | DHRTF Measurement | Single LS Measurement |
|-----------|-------------------|----------------------|
| Loudspeakers | 64 on half-circle | Neumann KH120A |
| Directions | M = 4608 | M = 72 |
| Frequency range | 350 Hz – 24 kHz | 20 Hz – 24 kHz |
| Azimuth resolution | 5° | 5° |
| Sampling rate | 48 kHz | 48 kHz |
| Dummyhead | Head Acoustics HMS II.3 | Same |
| Headphone | Bose QC20 (no electronics) | Same |
| Sweep method | Multiple exponential sweeps | Same |
| Window | Hann, 7.2–7.5 ms cutoff | Hann, 12.2–12.6 ms cutoff |

## Results

### Primary Path DOA Dependency

| Frequency Range | Magnitude Deviation (50% quantile) | Phase Deviation (50% quantile) | Magnitude Deviation (95% quantile) | Phase Deviation (95% quantile) |
|-----------------|-------------------------------------|-------------------------------|-------------------------------------|-------------------------------|
| < 200 Hz | Negligible | Negligible | Negligible | Negligible |
| 200 Hz – 1 kHz | 1–2 dB | 10–20° | Up to 5 dB | Up to 30° |
| > 1 kHz | Increasing | Increasing | Large (>5 dB) | Large (>30°) |

Key findings:
- **Below 200 Hz**: Primary path is approximately DOA-independent → ANC performance is robust
- **200 Hz – 1 kHz**: Moderate DOA dependency; 50% of directions within 1–2 dB magnitude and 10–20° phase
- **Above 1 kHz**: Severe DOA dependency with resonance effects from the headphone housing, especially at contralateral angles (φ = 50°–135°)

### Active Attenuation Results

| Setting | DOA Dependency | Low-Freq Performance | Notes |
|---------|---------------|---------------------|-------|
| Passive | Minimal | Slight amplification ~200 Hz; >26 dB at 2 kHz | DOA-independent |
| FB | **None** | Good low-freq attenuation | Only depends on $G(z)$ |
| FF | **Significant** | Good at nominal DOA; degrades at other angles | Depends on $P(z)$ |
| FFFB | Moderate | Best overall; FB compensates FF DOA weakness | FB part is DOA-independent |
| BoseElec | Moderate | Similar to FFFB | Commercial hybrid implementation |

### Attenuation Bound Results

| Target Attenuation | Max Amplitude Deviation | Max Phase Deviation |
|---------------------|------------------------|---------------------|
| 0 dB (no amplification) | 6.02 dB | 60° |
| 5 dB | 2.54 dB | 18.19° |
| 10 dB | 1.49 dB | 10.29° |
| 15 dB | 1.06 dB | 7.18° |
| 20 dB | 0.83 dB | 5.76° |

## Key Contributions

1. **Novel attenuation bound**: Closed-form expression relating magnitude/phase deviation to achievable attenuation for tonal signals — 20 dB requires <0.83 dB amplitude and <5.76° phase accuracy
2. **Comprehensive DHRTF dataset**: 4608-direction measurement of primary path DOA dependency for in-ear headphones, showing primary paths are approximately DOA-independent below 200 Hz
3. **DOA dependency of ANC architectures**: First systematic comparison showing feedforward ANC is DOA-dependent while feedback ANC is not, with experimental validation across five ANC settings
4. **Resonance effects identification**: Discovered angle- and frequency-localized resonance effects in the headphone housing above 1 kHz causing large primary path deviations
5. **In-ear vs. on-ear comparison**: In-ear headphones show less DOA dependency than on-ear (cf. Guldenschuh), as expected from closer microphone proximity and more compact housing

## Related Concepts

- [[concepts/feedforward-anc|Feedforward ANC]] — DOA-dependent through primary path
- [[concepts/feedback-anc|Feedback ANC]] — DOA-independent (only depends on secondary path)
- [[concepts/hybrid-anc|Hybrid ANC]] — FB component compensates FF DOA weakness
- [[concepts/device-specific-hrtf|Device-Specific HRTF (DHRTF)]] — HRTF measured with headphone microphones
- [[concepts/primary-path-variability|Primary Path Variability]] — DOA-induced changes in $P(z)$
- [[concepts/anc-attenuation-bounds|ANC Attenuation Bounds]] — Analytical limits on achievable attenuation
- [[concepts/active-noise-control|Active Noise Control]] — General ANC framework
- [[concepts/wiener-filter|Wiener Filter]] — Optimal FIR filter via Wiener-Hopf equation

## Related Synthesis

- [[synthesis/anc-architecture-evolution|ANC Architecture Evolution]]
- [[synthesis/modern-headphone-anc-systems|Modern Headphone ANC Systems]]
