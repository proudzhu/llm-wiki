---
type: concept
created: 2026-09-09
updated: 2026-09-09
sources:
  - raw/papers/tervo-2009-sound-intensity-direction/full-text.md
tags:
  - sound-intensity
  - array-processing
  - sound-source-localization
  - signal-processing
---

# Sound Intensity Vector

The **sound intensity vector** is the time- and frequency-dependent vector quantity whose direction points (approximately) toward a sound source and whose length carries acoustic power information. On a Cartesian axis $a$, the intensity in the frequency domain is the real part of the cross-spectrum between sound pressure and particle velocity:

$$I_a(\omega) = \operatorname{Re}\{P^*(\omega)\, U_a(\omega)\}$$

where $P(\omega)$ is the sound pressure, $U_a(\omega)$ the particle velocity, and $*$ the complex conjugate. Each intensity vector decomposes into a **radial component** $r$ (magnitude) and an **angular component** $\theta$ (azimuth, in 2-D probe geometries), which downstream estimators may weight differently — a design choice with large performance consequences (see [[concepts/intensity-vector-doa-estimation|Intensity-Vector DOA Estimation]]).

## Estimation

Two practical routes:

1. **Microphone-pair (p–p probe) measurement** — particle velocity is approximated by the finite-difference pressure gradient between closely spaced pressure microphones. For a four-microphone square grid with spacing $d$ (Tervo 2009, after Kallinger et al.):

   $$P(\omega) \approx \frac{1}{4}\sum_{n=1}^{4} P_n(\omega), \qquad U_x(\omega) \approx \frac{-j}{\omega \rho_0 d}\big[P_1(\omega) - P_2(\omega)\big]$$

   with $\rho_0 = 1.2~\mathrm{kg/m^3}$ the median air density; the $y$-axis velocity uses the orthogonal microphone pair.
2. **B-format ([[concepts/ambisonics|Ambisonics]]) signals** — pressure and velocity components are directly available from a Soundfield-type microphone.

## Systematic Bias and Compensation

Both routes bias the intensity direction:

- **p–p probes**: the pressure gradient is not constant within the sensor array, so the finite-difference velocity estimate warps the azimuth in a frequency-dependent way. For the square grid the bias is

  $$\theta_{\text{biased}} = \arctan\!\left( \frac{\sin\!\big(\tfrac{\omega d}{2c} \sin\theta\big)}{\sin\!\big(\tfrac{\omega d}{2c} \cos\theta\big)} \right)$$

  ($c = 343~\mathrm{m/s}$). The mapping has no closed-form inverse; it is inverted by **linear interpolation** and is valid only below $f_{\max} = c/(d\sqrt{2})$. Broadband operation therefore requires multiple grid sizes — e.g., $d = 100~\mathrm{mm}$ for 100 Hz–1 kHz and $d = 10~\mathrm{mm}$ for 1–5 kHz (Tervo 2009).
- **Soundfield microphones**: non-idealities in the capsule directivity patterns bias the velocity channels.

## Uses

- **Direction estimation**: per-frame azimuth histograms of intensity vectors feed DOA estimators — averaged directly or fitted with wrapped mixture distributions ([[concepts/intensity-vector-doa-estimation|Intensity-Vector DOA Estimation]]).
- **Room acoustics analysis**: locating from where and when direct sound and early reflections arrive in concert-hall [[concepts/room-impulse-response|impulse responses]].
- **Directional Audio Coding (DirAC)** and teleconferencing: reproducing or capturing the direction of sound arriving at a receiver.
- **SELD/ACCDOA input features**: first-order Ambisonics intensity vectors (active/real and reactive/imaginary parts) are a standard feature family for DNN-based [[concepts/sound-source-localization|localization]] and [[concepts/sel-d|sound event localization and detection]]; the Grumiaux et al. 2022 survey lists intensity-based features among the main conventional input types and notes that classical intensity methods degrade quickly under reflections — Tervo 2009 quantifies that degradation in a hall with RT ≈ 2.1 s.

## Related Concepts

- [[concepts/intensity-vector-doa-estimation|Intensity-Vector DOA Estimation]] — estimators operating on intensity-vector azimuths
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]] — the general problem
- [[concepts/ambisonics|Ambisonics]] — B-format route to intensity vectors; FOA intensity features in SELD
- [[concepts/sound-source-localization|Sound Source Localization]] — umbrella field
- [[concepts/room-impulse-response|Room Impulse Response]] — measurement context

## Related Sources

- [[sources/tervo-2009-sound-intensity-direction|Tervo 2009: Direction Estimation Based on Sound Intensity Vectors]] — p–p probe formulation, bias compensation, and five-estimator comparison on concert-hall data
- [[sources/grumiaux-2022-ssl-deep-learning-survey|Grumiaux et al. 2022: A Survey of SSL with Deep Learning Methods]] — intensity-based features and methods in the conventional/DL SSL landscape
