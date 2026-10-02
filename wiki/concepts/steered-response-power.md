---
type: concept
created: 2026-10-02
updated: 2026-10-02
sources:
  - raw/articles/wikipedia-steered-response-power.md
  - raw/papers/grinstein-2024-srp-tutorial-review/full-text.md
tags:
  - sound-source-localization
  - doa-estimation
  - beamforming
  - microphone-array
  - gcc
  - audio-processing
---

# Steered-Response Power (SRP)

**Steered-response power** (SRP) is a family of [[concepts/sound-source-localization|sound source localization]] algorithms interpretable as a [[concepts/beamforming|beamforming]]-based approach: it searches for the candidate position or direction that maximizes the output power of a steered delay-and-sum beamformer. Its most widely used variant, **SRP-PHAT**, applies a **phase transform** (PHAT) weighting to make the estimate robust in reverberant and noisy acoustic environments (DiBiase 2000; Silverman et al. 2005). The definitive tutorial treatment is the review by [[sources/grinstein-2024-srp-tutorial-review|Grinstein et al. 2024]], which classifies over 200 SRP papers into a taxonomy of complexity-reduction, robustness, multi-source, and practical-variant strategies, and reformulates the algorithm as the modular [[concepts/x-srp|X-SRP]] framework.

## Definition

For a system of $M$ microphones with discrete-time signals $s_m(n)$, the (unweighted) SRP at a candidate source position $\mathbf{x} = [x, y, z]^{\mathsf{T}}$ is the output energy of the delay-and-sum beamformer steered to $\mathbf{x}$:

$$P_{0}(\mathbf{x}) \triangleq \sum_{n\in\mathbb{Z}} \left|\sum_{m=1}^{M} s_m\big(n-\tau_{m}(\mathbf{x})\big)\right|^{2},$$

where $\tau_{m}(\mathbf{x})$ is the propagation time-lag from a source at $\mathbf{x}$ to the $m$-th microphone. The **weighted** SRP generalizes this in the frequency domain:

$$P(\mathbf{x}) = \frac{1}{2\pi} \sum_{m_{1}=1}^{M}\sum_{m_{2}=1}^{M} \int_{-\pi}^{\pi} \Phi_{m_{1},m_{2}}(e^{j\omega})\, S_{m_{1}}(e^{j\omega}) S_{m_{2}}^{*}(e^{j\omega})\, e^{j\omega \tau_{m_{1},m_{2}}(\mathbf{x})} \,d\omega,$$

with $\Phi_{m_{1},m_{2}}$ a frequency-domain weighting function, $S_m$ the discrete-time Fourier transform of $s_m$, and $\tau_{m_{1},m_{2}}(\mathbf{x})$ the integer **time-difference of arrival** (TDOA) between microphones $m_1$ and $m_2$ for a source at $\mathbf{x}$:

$$\tau_{m_{1},m_{2}}(\mathbf{x}) \triangleq \left\lfloor f_s \frac{\|\mathbf{x}-\mathbf{x}_{m_{1}}\|-\|\mathbf{x}-\mathbf{x}_{m_{2}}\|}{c} \right\rceil,$$

where $f_s$ is the sampling frequency, $c$ the speed of sound, and $\lfloor\cdot\rceil$ the rounding operator.

## Relation to Generalized Cross-Correlation (GCC)

The SRP objective decomposes into a sum of **generalized cross-correlations** (GCCs) evaluated at each microphone pair's TDOA — the [[concepts/gcc-phat|GCC-PHAT]] correlation is the standard choice (see its concept page for the formulation and partial-whitening variants):

$$P(\mathbf{x}) = \sum_{m_{1}=1}^{M}\sum_{m_{2}=1}^{M} R_{m_{1},m_{2}}\big(\tau_{m_{1},m_{2}}(\mathbf{x})\big),$$

where

$$R_{m_{1},m_{2}}(\tau) \triangleq \frac{1}{2\pi} \int_{-\pi}^{\pi} \Phi_{m_{1},m_{2}}(e^{j\omega})\, S_{m_{1}}(e^{j\omega}) S_{m_{2}}^{*}(e^{j\omega})\, e^{j\omega\tau} \,d\omega.$$

The **phase transform** (PHAT) weighting forces the GCC to use only phase information by whitening the cross-spectrum:

$$\Phi_{m_{1},m_{2}}(e^{j\omega}) \triangleq \frac{1}{|S_{m_{1}}(e^{j\omega}) S_{m_{2}}^{*}(e^{j\omega})|},$$

which discards magnitude cues dominated by the source spectrum and room acoustics, making the delay estimate robust in reverberant environments.

## Localization by Grid Search

SRP-PHAT localization is a grid search: evaluate $P(\mathbf{x})$ on a grid of candidate locations $\mathcal{G}$ and pick the maximizer

$$\hat{\mathbf{x}}_{s} = \arg\max_{\mathbf{x} \in \mathcal{G}} P(\mathbf{x}).$$

The SRP map $P(\mathbf{x})$ over the grid is often visualized as an acoustic "power map" whose peak marks the estimated source position.

## Complexity and its Reduction

The frequency-domain SRP costs $\text{O}(ML\log L+GPL)$ and the time-domain version $\text{O}(ML\log L+PL+GP)$ — $M$ microphones, $P=M(M-1)/2$ pairs, $L$-sample frames, $G$ grid points (Grinstein et al. 2024). Every fast variant shrinks $G$, $P$, or the analyzed frequency set, at some localization cost: **volumetric SRP** (V-SRP, pooling correlation over the volume around each coarse grid point), **iterative refinement** (quadtree subdivision, Stochastic Region Contraction, branch-and-bound searches with guarantees), grids seeded from **cheaper prior estimators** (GCC-peak triangulations), and **parallelization** (SRP is embarrassingly parallel over grid points; CUDA implementations report 70–275× speedups).

## Relation to Maximum-Likelihood SSL

Grinstein et al. 2024 highlight that under high microphone SNR and reverberation modeled as independent across microphones, the maximum-likelihood SSL estimator reduces to the SRP objective — the theoretical justification for SRP's robustness in moderately reverberant, low-noise conditions. SRP is also a *least-commitment* alternative to two-step TDOA/triangulation localization: instead of committing early to a per-pair TDOA peak (which fails under reverberation-induced multiple peaks), every correlation value is projected onto its spatial locus, and commitment happens only at the final grid maximization.

## Volumetric SRP: V-SRP and M-SRP (Cobos et al. 2011)

Classical SRP-PHAT assigns each grid point a unique integer TDOA per microphone pair. This does not guarantee grid consistency — some TDOAs correspond to no grid point (they fail to lie on an intersection of hyperboloids), and with coarse grids part of the TDOA information is lost. The **modified SRP-PHAT** (M-SRP) is the popular instance of **volumetric SRP** (V-SRP), in which a pooling function (summation, average, or max) aggregates correlation values over the entire *volume* surrounding each coarse grid point. It accumulates GCC values over the range of delays associated with the volume surrounding each grid point:

$$P'(\mathbf{x}) = \sum_{m_{1}=1}^{M}\sum_{m_{2}=1}^{M} \sum_{\tau=L_{m_{1},m_{2}}^{l}(\mathbf{x})}^{L_{m_{1},m_{2}}^{u}(\mathbf{x})} R_{m_{1},m_{2}}(\tau),$$

with lower/upper accumulation limits $L^{l}, L^{u}$ computed either exactly from the grid-cell boundaries or approximately from the spatial gradient of the TDOA, $\nabla_{\tau_{m_{1},m_{2}}}(\mathbf{x})$ — each component $\gamma \in \{x,y,z\}$ being $\nabla_{\gamma\tau}(\mathbf{x}) = \frac{1}{c}\left(\frac{\gamma-\gamma_{m_1}}{\|\mathbf{x}-\mathbf{x}_{m_1}\|} - \frac{\gamma-\gamma_{m_2}}{\|\mathbf{x}-\mathbf{x}_{m_2}\|}\right)$, with limits offset by $\|\nabla_{\tau}\| \cdot d$ around the nominal TDOA. This modification reduces computational cost and increases robustness for scalable (coarser) spatial sampling. Grinstein et al. 2024 note that exact anechoic bounds for a cuboid volume require searching only 26 boundary points (its vertices, edges, and faces) — or approximately just the 8 vertices, which can be precomputed.

## Position in the SSL Landscape

- SRP-PHAT is the classic **conventional** baseline in the SSL literature: the Grumiaux et al. 2022 survey lists TDoA/GCC-PHAT and SRP-PHAT power maps among the standard non-learning methods, and reports DNN systems achieving large gains over them (e.g., ~2x DoA classification accuracy vs SRP-PHAT at low SNR). The Grinstein et al. 2024 review adds the counterpoint: SRP remains a standard method (simple, robust, array-geometry-agnostic at run time), and the two families converge — SRP maps as neural input features, neural replacements of SRP blocks (Deep-GCC, Neural-SRP).
- Compared to [[concepts/intensity-vector-doa-estimation|intensity-vector methods]], SRP estimates full 3-D positions (not only direction), but at the cost of an expensive grid search over candidate locations.
- Its computational burden motivated hierarchical/coarse-to-fine searches, stochastic region contraction, and — as in the search-based DoA estimation of Tesch & Gerkmann 2024 — the general pattern of trading one filter evaluation per candidate direction against learned classifiers.

## Related Concepts

- [[concepts/sound-source-localization|Sound Source Localization]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/beamforming|Beamforming]] — SRP is the power output of a steered delay-and-sum beamformer
- [[concepts/gcc-phat|GCC-PHAT]] — the correlation function underlying SRP-PHAT and its partial-whitening variants
- [[concepts/x-srp|X-SRP]] — the modular reformulation of the algorithm and its variant space
- [[concepts/interaural-time-difference|Interaural Time Difference]] — the two-microphone (binaural) special case of TDOA
- [[concepts/search-based-doa-estimation|Search-based DoA Estimation]] — a grid-search localizer built on a learned spatially selective filter

## Related Sources

- [[sources/grinstein-2024-srp-tutorial-review|Grinstein et al. 2024: SRP for Sound Source Localization — a Tutorial Review]] — the authoritative peer-reviewed reference for the formulations, taxonomy, and X-SRP on this page
- [[sources/wikipedia-steered-response-power|Wikipedia: Steered-response power]] — the reference for the formulas on this page
- [[sources/grumiaux-2022-ssl-deep-learning-survey|Grumiaux et al. 2022: A Survey of SSL with Deep Learning Methods]] — positions SRP-PHAT as the conventional baseline that DL methods improve upon
- [[sources/kim-2014-doa-based-snr-estimation|Kim & Kim 2014: DOA-based SNR Estimation]] — notes GCC/SRP-PHAT reliability within the target-DOA error window
