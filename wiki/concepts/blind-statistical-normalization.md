---
type: concept
created: 2026-10-11
updated: 2026-10-11
sources:
  - raw/papers/warsitz-2007-blind-gev-beamforming/full-text.md
tags:
  - beamforming
  - speech-enhancement
  - array-processing
---

# Blind Statistical Normalization (BSN)

**Blind Statistical Normalization (BSN)** is a single-channel post-filter for the [[concepts/gev-beamformer|GEV beamformer]] that controls speech distortion by treating the unknown direction of arrival as a random variable and integrating the beamformer's spatial response against a probability density over directions. It was introduced by [[sources/warsitz-2007-blind-gev-beamforming|Warsitz & Haeb-Umbach 2007]] as the statistically motivated counterpart of the closed-form [[concepts/blind-analytical-normalization|BAN]].

## Key Formulations

Given partial (or no) knowledge of the DoA expressed as a pdf $p(\theta)$, the normalization extends the known-DoA form $w(k) = 1/|\mathbf{F}_{\mathrm{SNR}}^{\mathrm{H}}(k)\,\mathbf{d}(\theta_t, k)|$ to

$$
w_{\mathrm{BSN}}(k) = \frac{1}{\int_{-\pi/2}^{\pi/2} p(\theta)\,\left|\mathbf{F}_{\mathrm{SNR}}^{\mathrm{H}}(k)\,\mathbf{d}(\theta, k)\right|\,\mathrm{d}\theta}.
$$

The key idea: the beamformer's **own spatial response serves as the pdf** — a correctly operating beamformer responds strongly toward the desired signal and weakly toward the noise, so

$$
p(\theta) = \frac{\left|\mathbf{F}_{\mathrm{SNR}}^{\mathrm{H}}(k)\,\mathbf{d}(\theta, k)\right|}{\int_{-\pi/2}^{\pi/2} \left|\mathbf{F}_{\mathrm{SNR}}^{\mathrm{H}}(k)\,\mathbf{d}(\theta, k)\right|\,\mathrm{d}\theta},
$$

which makes BSN completely self-contained:

$$
w_{\mathrm{BSN}}(k) = \frac{\int_{-\pi/2}^{\pi/2} \left|\mathbf{F}_{\mathrm{SNR}}^{\mathrm{H}}(k)\,\mathbf{d}(\theta, k)\right|\,\mathrm{d}\theta}{\int_{-\pi/2}^{\pi/2} \left|\mathbf{F}_{\mathrm{SNR}}^{\mathrm{H}}(k)\,\mathbf{d}(\theta, k)\right|^{2}\,\mathrm{d}\theta}.
$$

It reduces to the known-DoA normalization when $p(\theta) = \delta(\theta - \theta_t)$, and requires only the anechoic steering vector $\mathbf{d}(\theta, k)$ — a pure function of the candidate angle, not of the unknown true propagation. A **DoA point estimate is available as a byproduct** (mean or maximum of the response-derived pdf).

## Properties

- **Robustness during adaptation**: unlike BAN, BSN shows no peaks in the spatial response at the target during the acquisition phase (target switched on at $t = 0.7$ s in the 2007 experiments), because the response-derived pdf re-normalizes continuously.
- **Reverberation robustness**: in the 2007 evaluation BSN's target response stays close to unity for all frequencies and reverberation times, whereas BAN degrades for $T_{60} \gtrsim 0.3$ s.
- **Numerical cost**: the angular integral (90 discrete angles in the 2007 implementation) makes BSN more expensive than the closed-form BAN — one reason later neural mask-based systems adopted BAN instead.

## Related Concepts

- [[concepts/gev-beamformer|GEV Beamformer]] — the beamformer BSN normalizes
- [[concepts/blind-analytical-normalization|Blind Analytical Normalization (BAN)]] — closed-form counterpart, better at low reverberation, worse during adaptation
- [[concepts/mvdr-beamformer|MVDR Beamformer]] — the distortionless ideal both normalizations approximate blindly

## Related Sources

- [[sources/warsitz-2007-blind-gev-beamforming|Warsitz & Haeb-Umbach 2007: Blind Acoustic Beamforming Based on Generalized Eigenvalue Decomposition]] — introduces BSN
