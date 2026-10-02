---
type: source
created: 2026-10-02
updated: 2026-10-02
sources:
  - raw/papers/grinstein-2024-srp-tutorial-review/full-text.md
  - https://doi.org/10.1186/s13636-024-00377-z
  - zotero://select/items/0_7FFQJGSP
tags:
  - sound-source-localization
  - doa-estimation
  - steered-response-power
  - beamforming
  - microphone-array
  - tutorial-review
  - audio-processing
---

# Grinstein, Tengan, Çakmak et al. 2024: Steered Response Power for Sound Source Localization — a Tutorial Review

**Authors**: [[entities/eric-grinstein|Eric Grinstein]], [[entities/elisa-tengan|Elisa Tengan]], [[entities/bilgesu-cakmak|Bilgesu Çakmak]], [[entities/thomas-dietzen|Thomas Dietzen]], [[entities/leonardo-nunes|Leonardo Nunes]], [[entities/toon-van-waterschoot|Toon van Waterschoot]], [[entities/mike-brookes|Mike Brookes]], [[entities/patrick-a-naylor|Patrick A. Naylor]]
**Venue**: EURASIP Journal on Audio, Speech, and Music Processing 2024(1):59
**Year**: 2024
**Type**: Tutorial review
**DOI**: [10.1186/s13636-024-00377-z](https://doi.org/10.1186/s13636-024-00377-z)
**arXiv**: [2405.02991](https://arxiv.org/abs/2405.02991)
**Zotero**: [7FFQJGSP](zotero://select/items/0_7FFQJGSP)
**Code**: [github.com/egrinstein/xsrp](https://github.com/egrinstein/xsrp) — X-SRP Python library

## Summary

This tutorial review surveys over 200 papers on the Steered Response Power (SRP) method and its variants, with emphasis on SRP-PHAT, and provides the field's first centralized resource for SRP research. It formulates the conventional method in both the time and frequency domains, derives its computational complexity, and organizes the variant literature into a task-oriented taxonomy (complexity reduction, robustness, multi-source, practical considerations). Beyond the survey, the authors contribute **eXtensible-SRP (X-SRP)** — a generalized, modularized formulation of the algorithm (with a released Python library) that unifies the reviewed extensions within one functional-block framework.

## Taxonomy

The review classifies SRP variants by the task they address, then re-groups them by implementation module in Sec. 7:

| Category | Core idea | Representative approaches |
|----------|-----------|---------------------------|
| **Complexity reduction** (Sec. 3) | Shrink the grid $G$, the pair set $P$, or the frequency set | Volumetric SRP (V-SRP, M-SRP), iterative refinement (quadtree, [[concepts/steered-response-power\|SRP]] region contraction, branch-and-bound), prior-based grids, GPU parallelization, SVD low-rank approximation |
| **Robustness** (Sec. 4) | Remove noise/reverberation artifacts from SRP maps | GCC-PHAT$_\beta$ partial whitening, weighted combination (W-SRP), alternative correlation functions, pre/post-processing (VAD, Wiener), neural blocks (Deep-GCC, Neural-SRP) |
| **Multi-source** (Sec. 5) | Localize $N$ (usually unknown) simultaneous sources | Source cancellation/de-emphasis, grid refinement, clustering, sparsity-based modeling |
| **Practical** (Sec. 6) | Real-world deployment aspects | Applications, tracking of moving sources, directional sources/microphones, comparisons to other SSL methods, analytical models |

## Methodology (Surveyed Methods)

### The conventional SRP model (Sec. 2)

The free-field signal model for microphone $m$ (reverberation folded into the noise term):

$$x_{m}(t)=a_{m}(\mathbf{u})s(t-\tau_{m}(\mathbf{u}))+\epsilon_{m}(t),$$

with time-difference of arrival (TDOA) $\tau_{lm}(\mathbf{u})=\big(\lVert\mathbf{u}-\mathbf{v}_{l}\rVert-\lVert\mathbf{u}-\mathbf{v}_{m}\rVert\big)/c$. Positions sharing one TDOA lie on a hyperbola branch; two-step (triangulation) methods intersect these but are non-robust because they commit early to a single TDOA estimate per pair. SRP instead follows the **principle of least commitment**: every cross-correlation value is projected onto the spatial locus it is consistent with, and commitment happens only at the final grid maximization.

The **GCC-PHAT** correlation (see [[concepts/gcc-phat|GCC-PHAT]]) whitens the cross-spectrum so that only phase information survives, sharpening the correlation peak:

$$\text{GCC-PHAT}(f;\bar{\mathbf{x}}_{l},\bar{\mathbf{x}}_{m})=\frac{\bar{x}_{l}(t,f)\bar{x}^{*}_{m}(t,f)}{|\bar{x}_{l}(t,f)|\,|\bar{x}_{m}(t,f)|}.$$

The **time-domain SRP** for a candidate position $\mathbf{u}$ and microphone pair $(l,m)$ is the cross-correlation evaluated at the rounded pair TDOA,

$$\text{SRP}_{lm}(\mathbf{u};\mathbf{x}_{l},\mathbf{x}_{m})=\text{CC}(\lfloor\tau_{lm}(\mathbf{u})\rceil;\mathbf{x}_{l},\mathbf{x}_{m}),$$

and the global SRP is the sum over all $P=M(M-1)/2$ pairs: $\text{SRP}(\mathbf{u};\mathcal{X})=\sum_{l}\sum_{m>l}\text{SRP}_{lm}(\mathbf{u})$. The **frequency-domain SRP** instead steers each frequency bin by a complex exponential, $\text{SRP}_{lm}(\mathbf{u},f)=\text{GCC-PHAT}(f)\,e^{jf\tau_{lm}(\mathbf{u})}$, summed over pairs and frequencies; the two formulations are not exactly equivalent (rounding vs. low-pass effects).

Near-field (distributed) arrays estimate full positions — **position SSL (PSSL)**; far-field (compact) arrays estimate only azimuth/elevation — **DOA estimation**, on Cartesian or polar/spherical grids respectively.

![[raw/papers/grinstein-2024-srp-tutorial-review/figures/fig1.png|SRP map example]]
*Figure 3: Example SRP map for 3D DOA estimation of a speech source with a spherical 8-microphone array (reverberation time 400 ms, source at (100°, 60°), uncorrelated noise at 20 dB SNR). The peak of the map is the estimated DOA.*

### Complexity analysis (Sec. 3.1)

Frequency-domain SRP costs $\text{O}(ML\log L+GPL)$ (FFT + GCC per pair + per-grid-point/per-frequency steering); the time-domain version drops the frequency loop, $\text{O}(ML\log L+PL+GP)$. All complexity-reduction strategies follow from shrinking $G$, $P$, $L$, or the frequency range — at some localization-performance cost.

### Complexity-reduction variants (Sec. 3)

- **Volumetric SRP (V-SRP)**: coarse grids pool correlation values over the *volume* around each candidate instead of a single point, via a pooling function (sum, average, or max). The **Modified SRP (M-SRP)** (Cobos et al., the gradient-based TDOA-bound approximation described on [[concepts/steered-response-power|the SRP concept page]]) is the popular instance; exact anechoic bounds need only the volume's 26 boundary points, or approximately its 8 vertices.
- **Iterative grid refinement**: quadtree subdivision of azimuth-elevation cells; **low-pass SRP** (only frequencies below ~200 Hz produce a smoother map whose broad peak survives coarse grids — see Figure 5); **Stochastic Region Contraction (SRC)** and its coarse-fine variant CFRC; branch-and-bound searches with guarantees of not discarding the global maximum; Artificial Bee Colony, Majorization-Minimization, and Lagrange-Galerkin searches.
- **Prior-based grids**: initialize from GCC-PHAT peak triangulations (e.g. 4 peaks per pair) instead of the full room grid; **prior scene information** merges grid points with indistinguishable TDOA sets, uses non-uniform geometric grids, or filters TDOA hash tables by correlation value.
- **Parallelization**: SRP is embarrassingly parallel over grid points — CUDA GPU implementations report 70–275× speedups over optimized CPU counterparts; OpenCL/FPGA/Jetson and vectorized IPP implementations also surveyed.

![[raw/papers/grinstein-2024-srp-tutorial-review/figures/fig2.png|Low-pass SRP map]]
*Figure 5: Low-pass version of the frequency-domain SRP, using only frequencies up to 200 Hz — a smoother map that keeps the source's neighbourhood salient under coarse initial grids.*

### Robustness variants (Sec. 4)

- **GCC-PHAT$_\beta$** — partial whitening, $\text{GCC-PHAT}_{\beta} \propto \bar{x}_{l}\bar{x}^{*}_{m}/|\bar{x}_{l}\bar{x}^{*}_{m}|^{\beta}$, interpolates between plain CC ($\beta=0$) and full PHAT ($\beta=1$); the review reports acceptable $\beta$ between 0.65 and 0.7 for general signals, and $\beta=0.8$ for narrowband sources under directional noise.
- **Alternative correlations**: kurtosis-based (Gaussian noise suppressed in theory), sum-of-Gaussians-smoothed GCCs, MCCC (multi-channel cross-correlation), eigenvector-domain correlations, envelope of the analytic GCC (against sinc ripples for narrowband sources), wavelet-based GCCs for outdoor propagation-model errors.
- **W-SRP** — generalized pairwise/frequency combination with weights $k_{lm}$, $k_f$; replacing pairwise summation by a *product* reduced localization RMS error by 45% in the cited simulations (all pairs must then agree).
- **Neural blocks** (Sec. 4.4): Deep-GCC networks regress an idealized single-peak GCC (Gaussian target at the true TDOA); CNNs estimate frequency weights $k_f$ (Wiener-filter or SNR targets); SRP maps feed CNNs/CRNNs as input features (MLP, 3D, spherical, and icosahedral convolutions); **Neural-SRP** replaces the pairwise-processing core with a Relation-Network-style architecture (Figure 7).

![[raw/papers/grinstein-2024-srp-tutorial-review/figures/fig3.png|Neural-SRP+ vs conventional SRP map]]
*Figure 7: Neural-SRP+ vs. conventional SRP map in a highly reverberant room — the learned pairwise processing suppresses reverberation-induced spurious peaks around the true source position (cross).*

### Multi-source SRP (Sec. 5)

With $N$ sources the pairwise correlations show one peak per source plus ghost peaks from reflections, and cross-source interference lowers correlation amplitudes — simple thresholding fails. Four strategy families: **modified computation** (geometric/harmonic mean combination removes sidelobes), **source cancellation** (de-emphasis of an already-located dominant source via a TDOA-domain notch filter — Brutti et al.; orthogonal-subspace projection of GCCs; spatial-gradient subtraction; GMM-based probabilistic maps), **grid refinement** (TDOA-interval zones, spatially-averaged probability maps), and **clustering** (agglomerative or GMM clustering of per-frame/per-subband estimates; Multi-Stage Rejection Sampling). **Sparsity-based** approaches model the broadband SRP map as a group-sparse function of per-location PSDs, exploit W-disjoint orthogonality of speech in the TF domain (histograms of narrowband DOA estimates), or decompose TF signals with NMF (SRP-NMF).

## Practical Considerations Survey

### Applications (Sec. 6.1)

Surveillance and defence (UAV detection and UAV-embedded arrays, intrusion detection, gunshot localization); environmental noise-pollution monitoring and seismic-event detection; underwater localization of sound-emitting fish; faulty-equipment detection in power stations; vehicle horns and in-cabin talkers; medical (footstep analysis for early dementia detection, fall detection); human-robot interaction; camera steering for meetings and smart rooms; helmet-mounted arrays for industrial acoustic awareness.

### Tracking moving sources (Sec. 6.2)

Frame-wise independent SRP estimates can be chained with state-space models: Kalman filters, particle filters (dominant; source motion commonly modeled by Langevin dynamics with damping/excitation parameters), or deep trackers.

### Directional sources and microphones (Sec. 6.3)

Directivity enters the attenuation term as $a_{m}=d^{(1)}_{m}(\theta_{1}-\theta_{2})\,d^{(2)}(\theta_{3}-\theta_{4})\,k_{d}/\lVert\mathbf{u}-\mathbf{v}_{m}\rVert$; source orientation can be added as an extra search dimension, or estimated a posteriori from the kurtosis (sharpness) of per-array SRP maps.

### Comparison to other localization approaches (Sec. 6.4)

- **SRP ≡ ML-SSL in the high-SNR limit**: under high microphone SNR and inter-microphone-independent reverberation, the maximum-likelihood SSL estimator reduces to the SRP formulation — the review's main theoretical justification for SRP's robustness in moderately reverberant, low-noise environments.
- vs. **two-step TDOA/triangulation**: SRP is more robust in noise/reverberation (least commitment) at higher computational cost.
- vs. **ROOT-MUSIC**: SRP-PHAT superior in reverberation and low SNR despite higher cost.
- **MCCC**-based estimators yield higher resolution than SRP in some regimes; intensity-vector (AIV) methods on spherical arrays outperform SRP for well-separated sources, while SRP degrades for ≥3 sources separated by less than ~45°.
- SRP-PHAT assembles **without** the noise statistics that ML methods require; in the SLF/SOF integration framework it is the special case that integrates array likelihood maps while ignoring their uncertainty.

### Analytical models (Sec. 6.5)

Closed-form models predict SRP maps from array topology, room geometry, and signal bandwidth (not spectral content); sensor calibration errors at array endpoints dominate localization error above a threshold related to propagation distance and sampling rate.

## X-SRP (Sec. 7)

The survey's own methodological contribution: SRP re-expressed as an algorithm with replaceable **modules** — `create_initial_candidate_grid`, `compute_signal_features` (CC / GCC-PHAT / neural), `create_srp_map`, `grid_search`, `update_signal_features` (e.g. source de-emphasis), `update_grid` (e.g. region contraction) — so that the reviewed extensions become instantiations of a common loop (see [[concepts/x-srp|X-SRP]]). This yields a second, implementation-oriented grouping of the literature that complements the task-oriented taxonomy, and is released as a Python library.

![[raw/papers/grinstein-2024-srp-tutorial-review/figures/fig4.png|X-SRP flowchart]]
*Figure 9: Flowchart of the generalized X-SRP algorithm — parallelograms are input data, rectangles functions, diamonds decisions, ellipses terminal states.*

## Key Contributions

1. **First comprehensive SRP survey**: 200+ papers classified, described, and compared — previously no centralized SRP resource existed.
2. **Task-oriented taxonomy**: complexity reduction / robustness / multi-source / practical considerations, with an implementation-oriented module-based re-grouping (Sec. 7).
3. **Dual tutorial formulation**: time- and frequency-domain SRP derivations with a unified complexity analysis, positioned for newcomers.
4. **Theoretical positioning**: the SRP ≡ ML-SSL reduction in the high-SNR/uncorrelated-reverberation limit, and the least-commitment framing versus two-step TDOA methods.
5. **X-SRP framework and library**: a modular algorithm formulation (Algorithm 1) plus an open-source Python implementation enabling reproduction and combination of the surveyed variants.

## Limitations and Caveats

- **SRP means SRP-PHAT** throughout — other correlation weightings are only treated as modifications of the PHAT baseline.
- **No unified benchmark**: quantitative claims (e.g. the 45% RMS reduction from product combination, the β ranges) are inherited from the cited original papers' simulations, not re-evaluated under a common protocol.
- **Literature cutoff ~2024**: the neural-SSL field moves quickly; post-2024 extensions are uncovered.
- **Extraction note** (this wiki copy, arXiv HTML): only 4 of the paper's 9 figures are raster images (Figures 3, 5, 7, 9 above); Figures 1, 2, 4, 6, 8 are vector graphics that the arXiv HTML renders inline and the extractor could not export. The published version also appends an extensive acronym glossary (~600 entries).

## Related Concepts

- [[concepts/steered-response-power|Steered-Response Power (SRP)]]
- [[concepts/x-srp|X-SRP]]
- [[concepts/gcc-phat|GCC-PHAT]]
- [[concepts/sound-source-localization|Sound Source Localization]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/search-based-doa-estimation|Search-based DoA Estimation]]
- [[concepts/intensity-vector-doa-estimation|Intensity-Vector DOA Estimation]]

## Related Sources

- [[sources/wikipedia-steered-response-power|Wikipedia: Steered-response power]] — the original reference for the SRP formula set on the concept page; this tutorial review is the authoritative peer-reviewed formulation.
- [[sources/grumiaux-2022-ssl-deep-learning-survey|Grumiaux et al. 2022: A Survey of SSL with Deep Learning Methods]] — the complementary view: where the DL survey treats SRP-PHAT as the conventional baseline that neural methods improve upon, this review shows the converse direction (SRP maps as neural input features, neural SRP blocks).
- [[sources/kim-2014-doa-based-snr-estimation|Kim & Kim 2014: DOA-based SNR Estimation]] — an application of the GCC/SRP-PHAT reliability window.
