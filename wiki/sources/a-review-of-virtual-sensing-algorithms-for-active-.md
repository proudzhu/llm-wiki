---
type: source
created: 2026-04-18
updated: 2026-05-26
sources:
  - raw/papers/moreau-2008-virtual-sensing-review/full-text.md
  - raw/papers/moreau-2008-virtual-sensing-review/figures/
  - https://www.mdpi.com/1999-4893/1/2/69
  - zotero://select/items/0_LJDPCZ9G
tags:
  - active-noise-control
  - virtual-sensing
  - review
  - remote-microphone-technique
  - auxiliary-filter
  - virtual-microphone-arrangement
  - algorithms
---

# Moreau, Cazzolato, Zander & Petersen 2008: A Review of Virtual Sensing Algorithms for Active Noise Control

**Authors**: [[entities/danielle-moreau|Danielle Moreau]], [[entities/ben-cazzolato|Ben Cazzolato]], [[entities/anthony-zander|Anthony Zander]], [[entities/cornelis-petersen|Cornelis Petersen]]
**Institution**: School of Mechanical Engineering, The University of Adelaide, Australia
**Published**: Algorithms, Vol. 1, No. 2, pp. 69–99, 2008
**Type**: Review Article
**DOI**: [10.3390/a1020069](https://doi.org/10.3390/a1020069)
**Zotero**: [LJDPCZ9G](zotero://select/items/0_LJDPCZ9G)

---

## Summary

This is the **comprehensive review paper** on virtual sensing algorithms for active noise control. It systematically categorizes and compares all major virtual sensing approaches: Remote Microphone Technique (RMT), Virtual Microphone Arrangement (VMA), Auxiliary Filter Method, Forward Difference Prediction, Adaptive LMS Virtual Microphone, Kalman Filtering, and Stochastically Optimal Tonal Diffuse Field methods. The paper provides theoretical derivations, numerical simulations, and experimental comparisons for each approach.

---

## Problem Formulation

### Zone of Quiet Limitation

Traditional local ANC creates a zone of quiet at the physical error sensor location. The zone is defined by a sinc function, with 10 dB reduction over a sphere of diameter **λ/10** (one tenth of the excitation wavelength). This is too small to extend to the observer's ear in many applications (e.g., ANC headrests).

### Virtual Sensing Solution

Virtual sensing algorithms estimate the error signal at a remote "virtual" location using:
- Physical error signal $e_p(n)$
- Control signal $y(n)$
- Knowledge of the system (transfer functions)

Instead of minimizing the physical error signal, the estimated virtual error signal is minimized to generate a zone of quiet at the virtual location.

---

## Virtual Sensing Algorithm Categories

### Class I: Direct Estimation (No Training)

#### 1. Remote Microphone Technique (RMT)

Uses a preliminary training phase where a physical microphone is temporarily placed at the virtual location to identify the transfer function between the permanent physical error mic and the target.

**Key equations**:
- Observation filter $H(z)$ maps physical error to virtual error: $E_v(z) = H(z) E_p(z)$
- Trained offline, then used online during control

**Advantages**: Simple, well-understood
**Limitations**: Highly sensitive to changes in the acoustic path (e.g., user moving head)

#### 2. Virtual Microphone Arrangement (VMA)

Uses an array of physical microphones to interpolate the sound pressure at the virtual point.

**Advantages**: Does not strictly require a training phase
**Limitations**: Performance degrades as frequency increases due to spatial aliasing

### Class II: Training-Based Methods

#### 3. Auxiliary Filter Method

Uses an auxiliary filter to model the primary noise path difference between physical and virtual locations.

**Two-stage process**:
1. **Tuning stage**: Train auxiliary filters using known signals
2. **Control stage**: Use pre-trained auxiliary filters to estimate virtual error

**Advantages**: More robust than RMT, avoids causality constraints
**Limitations**: Requires training phase, additional computational cost

#### 4. Forward Difference Prediction

Fits a polynomial to signals from a physical microphone array and extrapolates to the virtual location.

**Advantages**: No training required, robust to sound field changes
**Limitations**: Only suitable for low frequencies and small virtual distances; sensitive to microphone position errors

#### 5. Adaptive LMS Virtual Microphone

Uses LMS to adaptively weight physical microphone array signals to minimize the difference between predicted and measured virtual pressure.

**Advantages**: Compensates for position errors and sensitivity mismatches
**Limitations**: Requires training, not robust to sound field changes

#### 6. Kalman Filtering Virtual Sensing

Models the ANC system as a state-space system and uses Kalman filtering for optimal virtual error estimation.

**Advantages**: Compact state-space model, handles measurement noise, optimal estimation
**Limitations**: Limited to low-order systems, requires training

#### 7. Stochastically Optimal Tonal Diffuse Field

Generates optimal virtual microphones using correlation functions in pure-tone diffuse sound fields.

**Advantages**: Fixed gain, no training, robust to sound field changes
**Limitations**: Only suitable for pure-tone diffuse fields; performance decreases with virtual distance

### Moving Virtual Sensing Algorithms

Three moving virtual sensing algorithms have been developed:
1. **Remote Moving Microphone [10]**: Interpolates RMT estimates at fixed virtual locations
2. **Adaptive LMS Moving Virtual Microphone [11]**: Interpolates adaptive LMS VM estimates
3. **Kalman Filtering Moving Virtual Sensing [12]**: Interpolates Kalman filter estimates

All three achieve greater attenuation at moving virtual locations than control at fixed physical or virtual sensors.

---

## Comparative Analysis

| Method | Training Required | Robustness | Complexity | Frequency Range |
|:-------|:------------------|:-----------|:-----------|:----------------|
| RMT | Yes | Low | $O(L)$ | Broadband |
| VMA | No | Moderate | $O(M \cdot L)$ | Low frequency |
| Forward Difference | No | High | $O(M)$ | Low frequency |
| Adaptive LMS VM | Yes | Moderate | $O(M \cdot L)$ | Broadband |
| Kalman Filtering | Yes | High | $O(N^3)$ | Broadband (low-order) |
| Stochastically Optimal | No | High | $O(1)$ | Pure-tone diffuse |

Where $L$ = filter length, $M$ = number of physical mics, $N$ = state dimension.

---

## Experimental Validation

The paper validates all methods on various setups:
- **RMT**: Achieves ~20 dB attenuation at virtual location, but degrades rapidly with head movement
- **VMA**: Good performance at low frequencies (< 500 Hz), degrades above due to spatial aliasing
- **Forward Difference**: Effective for small virtual distances, sensitive to microphone position errors
- **Adaptive LMS VM**: Compensates for position errors, maintains ~15 dB attenuation
- **Kalman Filtering**: Optimal estimation in low-order systems (e.g., acoustic duct)
- **Moving Virtual Sensing**: Achieves additional 14 dB attenuation at moving virtual location compared to fixed sensor control

---

## Key Contributions

1. **First comprehensive review** of virtual sensing algorithms for ANC, categorizing methods into spatially fixed and moving virtual sensing
2. **Systematic comparison** of 9 virtual sensing methods with theoretical analysis, simulations, and experiments
3. **Zone of quiet characterization**: Quantified the λ/10 diameter limit for pressure-based ANC
4. **Complete summary table** (Table 1) with characteristics, advantages, and disadvantages for all methods
5. **Practical guidelines**: Method selection depends on application requirements (training availability, robustness needs, frequency range, system order)

---

## Related Concepts

- [[concepts/virtual-sensing|Virtual Sensing]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/remote-microphone-technique|Remote Microphone Technique]]
- [[concepts/kalman-filter|Kalman Filter]]

## Related Synthesis

- [[synthesis/virtual-sensing-evolution|Evolution of Virtual Sensing in ANC]]
- [[synthesis/modern-headphone-anc-systems|Modern Headphone ANC Systems]]
- [[synthesis/kalman-filter-theory-and-application|Kalman Filter Theory and Application]]
