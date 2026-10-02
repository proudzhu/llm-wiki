---
type: source
created: 2026-10-02
updated: 2026-10-02
sources:
  - raw/articles/wikipedia-steered-response-power.md
  - https://en.wikipedia.org/wiki/Steered-response_power
tags:
  - sound-source-localization
  - doa-estimation
  - beamforming
  - gcc
  - microphone-array
  - encyclopedia
---

# Wikipedia: Steered-Response Power

**Type**: Encyclopedia article (Wikipedia)
**Retrieved**: 2026-10-02
**URL**: [en.wikipedia.org/wiki/Steered-response_power](https://en.wikipedia.org/wiki/Steered-response_power)
**License**: CC BY-SA 4.0

---

## Summary

An encyclopedia reference for **steered-response power** (SRP) — a family of acoustic source localization methods that find the candidate position maximizing the output of a steered delay-and-sum beamformer — and its reverberation-robust variant **SRP-PHAT**, which applies a phase transform weighting to the generalized cross-correlations (GCCs) whose sum constitutes the SRP objective. The article derives the SRP objective in time and frequency domains, its decomposition into pairwise GCCs, the PHAT weighting, the grid-search localization procedure, and the modified SRP-PHAT of Cobos et al. (2011) with its TDOA-gradient-based GCC accumulation limits.

---

## Key Content

### SRP objective

- **Unweighted SRP** — output energy of a delay-and-sum beamformer steered to candidate position $\mathbf{x}$: $P_0(\mathbf{x}) = \sum_n |\sum_m s_m(n - \tau_m(\mathbf{x}))|^2$.
- **Weighted SRP** — pairwise frequency-domain form with weighting function $\Phi_{m_1,m_2}(e^{j\omega})$ and integer TDOAs $\tau_{m_1,m_2}(\mathbf{x})$ computed from microphone geometry, sampling frequency $f_s$, and speed of sound $c$ (rounded to integer samples).

### GCC decomposition and PHAT

- The objective equals the sum of pairwise **generalized cross-correlations** evaluated at each pair's TDOA: $P(\mathbf{x}) = \sum_{m_1}\sum_{m_2} R_{m_1,m_2}(\tau_{m_1,m_2}(\mathbf{x}))$.
- The **phase transform** sets $\Phi = 1/|S_{m_1} S_{m_2}^*|$, whitening the cross-spectrum so only phase information is used — effective for time-delay estimation in reverberant environments.

### Grid-search localization

- SRP-PHAT estimates the source position as the grid point maximizing $P(\mathbf{x})$ over candidate locations $\mathcal{G}$.
- **Classical-grid inconsistency**: assigning each grid point one integer TDOA per pair does not guarantee all TDOAs map to grid points (hyperboloid intersections); coarse grids lose TDOA information.

### Modified SRP-PHAT (Cobos, Marti & Lopez 2011)

- Accumulates GCC values over delay ranges $[L^l, L^u]$ tied to the volume surrounding each grid point, with limits derived exactly from grid-cell boundaries or approximately from the **spatial TDOA gradient** $\nabla_{\tau_{m_1,m_2}}(\mathbf{x})$ and direction angles $(\theta, \phi)$ for rectangular grids — reducing computational cost and improving robustness under scalable spatial sampling.

## References Cited in the Article

1. Johnson & Dudgeon (1993), *Array Signal Processing: Concepts and Techniques* — beamforming interpretation of SRP.
2. DiBiase (2000), PhD thesis, Brown Univ. — origin of SRP-PHAT for talker localization in reverberant environments.
3. Silverman et al. (2005), *IEEE Trans. Speech Audio Process.* — real-time performance of source-location estimators on a large-aperture microphone array.
4. Cobos, Marti & Lopez (2011), *IEEE Signal Process. Lett.* — the modified SRP-PHAT functional.

## Relevance to This Wiki

SRP-PHAT is the canonical **conventional baseline** in the SSL literature of this wiki: the Grumiaux et al. 2022 survey lists SRP-PHAT power maps among standard classical methods and reports DL systems roughly doubling DoA classification accuracy over SRP-PHAT at low SNR; Kim & Kim (2014) rely on GCC/SRP-PHAT reliability within their target-DOA error window. The concept page [[concepts/steered-response-power|Steered-Response Power]] holds the full formulation. The article also connects to [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]] and [[concepts/sound-source-localization|Sound Source Localization]].

---

## Related Concepts

- [[concepts/steered-response-power|Steered-Response Power]] — the concept page distilled from this article
- [[concepts/sound-source-localization|Sound Source Localization]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/interaural-time-difference|Interaural Time Difference]]

## Related Sources

- [[sources/grumiaux-2022-ssl-deep-learning-survey|Grumiaux et al. 2022: A Survey of SSL with Deep Learning Methods]]
- [[sources/kim-2014-doa-based-snr-estimation|Kim & Kim 2014: DOA-based SNR Estimation]]
- [[sources/tervo-2009-sound-intensity-direction|Tervo 2009: Direction Estimation Based on Sound Intensity Vectors]]
