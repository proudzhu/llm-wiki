---
type: concept
created: 2026-10-11
updated: 2026-10-11
sources:
  - raw/papers/warsitz-2007-blind-gev-beamforming/full-text.md
  - raw/papers/heymann-2016-neural-spectral-mask-beamforming/full-text.md
  - raw/papers/boeddeker-2018-neural-mask-beamforming/full-text.md
tags:
  - beamforming
  - speech-enhancement
  - array-processing
---

# Blind Analytical Normalization (BAN)

**Blind Analytical Normalization (BAN)** is a closed-form single-channel post-filter that fixes the arbitrary magnitude response of the [[concepts/gev-beamformer|GEV beamformer]] without any knowledge of the acoustic transfer functions, the DoA, or the array geometry. It was introduced by [[sources/warsitz-2007-blind-gev-beamforming|Warsitz & Haeb-Umbach 2007]] and later adopted verbatim by the neural [[concepts/mask-based-beamforming|mask-based beamforming]] front-ends of [[sources/heymann-2016-neural-spectral-mask-beamforming|Heymann et al. 2016]] and [[sources/boeddeker-2018-neural-mask-beamforming|Boeddeker et al. 2018]], where it complements a group-delay (phase) normalization.

## Key Formulations

The GEV beamformer $\mathbf{F}_{\mathrm{SNR}}(k)$ (principal generalized eigenvector of the speech-plus-noise / noise SCM pair) is defined only up to an arbitrary complex scalar per frequency bin. The distortionless response condition toward the target is $|w^*(k)\,\mathbf{F}_{\mathrm{SNR}}^{\mathrm{H}}(k)\,\mathbf{H}(\ell_t, k)| = 1$; computing $w(k)$ directly would require the unknown transfer function vector $\mathbf{H}$. BAN eliminates the unknowns via the approximation $\|\mathbf{H}(\ell_t, k)\|^2 \approx \|\mathbf{d}(\theta_t, k)\|^2 = M$ (transfer-function norm approximated by the anechoic steering-vector norm, i.e. $M$ microphones), yielding

$$
w_{\mathrm{BAN}}(k) = \frac{\sqrt{\mathbf{F}_{\mathrm{SNR}}^{\mathrm{H}}(k)\,\boldsymbol{\Phi}_{\mathbf{NN}}(k)\,\boldsymbol{\Phi}_{\mathbf{NN}}(k)\,\mathbf{F}_{\mathrm{SNR}}(k) / M}}{\mathbf{F}_{\mathrm{SNR}}^{\mathrm{H}}(k)\,\boldsymbol{\Phi}_{\mathbf{NN}}(k)\,\mathbf{F}_{\mathrm{SNR}}(k)},
$$

a closed-form expression requiring only the GEV filter vector and the noise SCM. With perfect distortion removal the GEV+BAN coincides with the (generalized) MVDR beamformer.

## Properties and Caveats

- **Accuracy vs. reverberation**: the $\|\mathbf{H}\|^2 \approx M$ assumption holds well for short filters capturing predominantly the direct path; at longer reverberation times ($T_{60} \gtrsim 0.3$ s in the 2007 experiments) BAN's response at the target degrades, and the [[concepts/blind-statistical-normalization|statistical normalization (BSN)]] variant stays closer to unity gain.
- **Adaptation transients**: BAN presumes the eigenvector tracker has converged; during initial adaptation its response can fluctuate strongly.
- **Magnitude only**: BAN normalizes magnitude; phase/group-delay distortion requires a separate normalization (Heymann et al. 2016 apply a group-delay normalization for ASR).

## Related Concepts

- [[concepts/gev-beamformer|GEV Beamformer]] — the beamformer whose arbitrary scale BAN fixes
- [[concepts/blind-statistical-normalization|Blind Statistical Normalization (BSN)]] — the statistical alternative
- [[concepts/mvdr-beamformer|MVDR Beamformer]] — GEV+BAN coincides with it under perfect distortion removal
- [[concepts/mask-based-beamforming|Mask-Based Beamforming]] — later family that adopts BAN with mask-estimated SCMs

## Related Sources

- [[sources/warsitz-2007-blind-gev-beamforming|Warsitz & Haeb-Umbach 2007: Blind Acoustic Beamforming Based on Generalized Eigenvalue Decomposition]] — introduces BAN
- [[sources/heymann-2016-neural-spectral-mask-beamforming|Heymann, Drude & Haeb-Umbach 2016: Neural Network Based Spectral Mask Estimation for Acoustic Beamforming]] — adopts GEV+BAN with DNN-mask SCMs; BAN used for PESQ evaluation
- [[sources/boeddeker-2018-neural-mask-beamforming|Boeddeker, Erdogan, Yoshioka & Haeb-Umbach 2018: Exploring Practical Aspects of Neural Mask-Based Beamforming for Far-Field Speech Recognition]] — GEV+BAN+group-delay variant at commercial scale
