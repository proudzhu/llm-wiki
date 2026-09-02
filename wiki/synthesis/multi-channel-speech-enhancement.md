---
type: synthesis
created: 2026-08-16
updated: 2026-09-02
sources:
  - raw/papers/lorenz-2005-robust-minimum-variance-beamforming/full-text.md
  - raw/papers/schwarz-2015-coherent-to-diffuse-power-ratio/full-text.md
  - raw/papers/tashev-2008-sound-capture-spatial-filter/full-text.md
  - raw/papers/jin-2017-multichannel-noise-reduction-mobile/full-text.md
  - raw/papers/lollmann-2020-generalized-coherence-based-signal-enhancement/full-text.md
  - raw/papers/mittal-2026-adaptive-diagonal-loading-beamforming/full-text.md
  - raw/papers/deng-2026-joint-covariance-wng-mvdr/full-text.md
  - raw/papers/oviste-2026-neural-vslf-speech-enhancement/full-text.txt
  - raw/papers/liu-2026-scm-reconstruction-speech-enhancement/paper.pdf
  - raw/papers/farmani-2026-virtual-mic-beamforming-hearing-aid/full-text.txt
  - raw/papers/zaidel-2026-linearly-constrained-deep-beamformer/full-text.md
  - raw/papers/huang-2026-ndf-joint-neural-directional-filtering/full-text.md
  - raw/papers/apostolidis-2026-listen-first-output-based-multi-microphone/full-text.md
  - raw/papers/liu-2026-array-invariant-speech-enhancement/full-text.md
  - raw/papers/lin-2024-agadir-array-geometry-agnostic-speech-recognition/full-text.md
  - raw/papers/taseska-2018-informed-spatial-filters/full-text.md
  - raw/papers/li-2026-geometry-conditioned-ssanc/full-text.md
  - raw/papers/frank-2026-low-latency-roi-beamforming/full-text.txt
  - raw/papers/yang-2025-mc-differential-asr-smart-glasses/full-text.md
  - raw/papers/ruan-2024-speech-extraction-low-snr/full-text.md
  - raw/papers/scheibler-2020-fast-independent-vector-extraction/full-text.md
  - raw/papers/kang-2019-low-complexity-permutation-alignment/full-text.md
  - raw/papers/yan-2014-dual-mic-bt-noise-reduction/full-text.md
  - raw/papers/braun-2015-residual-noise-control/full-text.md
tags:
  - multi-channel-speech-enhancement
  - beamforming
  - mvdr
  - cdr-estimation
  - spatial-coherence
  - coherence
  - gsc
  - speech-distortion
  - bluetooth-headset
  - robustness
  - array-invariant
  - neural-beamforming
  - evolution
  - differential-asr
---

# Multi-Channel Speech Enhancement: From Coherence Models to Geometry-Conditioned Neural Filters

> Cross-source synthesis tracing how multi-channel speech enhancement (MCSE) evolved along five largely independent axes — **what to estimate** (DOA → coherence → CDR → SCM → filter weights), **how to guarantee robustness** (ellipsoidal → Kantorovich → data-driven WNG), **where the decision lives** (input-based → output-based → multi-frontend fusion), **how to handle array geometry** (fixed → agnostic → conditioned), and **how to fuse data-driven estimation with classical structure** (purely classical → hybrid DNN-guided → end-to-end neural). The thesis: classical statistical-model MCSE is not obsolete in 2026 — it survives as the interpretability backbone of hybrid systems and the deployment-ready choice for resource-constrained hearables.

## Scope and Relationship to Other Syntheses

This page covers MCSE specifically — algorithms that exploit **spatial information across multiple microphones**. It deliberately defers to:

- [[synthesis/deep-speech-enhancement|Deep Speech Enhancement]] for the broader deep-learning SE backbone evolution (CRN → DPCRN → Conformer → Mamba); Insight 6 there sketches the multi-channel arc in 3 phases. This page goes deeper on the multi-channel-specific axes and adds the classical coherence/CDR lineage that the DL-focused synthesis omits.
- [[synthesis/multi-modal-speech-enhancement|Multi-Modal Speech Enhancement]] for BC/AC/IMU fusion.
- [[synthesis/joint-multitask-ultra-low-latency-se|Joint Multi-Task SE & Ultra-Low-Latency Paradigm]] for the AEC+NS+DR+OVC task-dissolution frontier and sub-10 ms latency tiers.

The distinction: this synthesis is about **spatial filtering** (beamforming, coherence, directional selection), not about single-channel SE backbones or multi-modal fusion.

## Sources Synthesized

| Source | Year | Axis advanced | Key contribution |
|--------|------|---------------|------------------|
| [[sources/lorenz-2005-robust-minimum-variance-beamforming\|Lorenz & Boyd 2005]] | 2005 | Robustness | Robust MVB: ellipsoidal array-manifold uncertainty → SOCP, guaranteed unity-gain over uncertainty set |
| [[sources/yan-2014-dual-mic-bt-noise-reduction\|Yan, Qiu & Lu 2014]] | 2014 | Application | Two-mic Bluetooth headset: coherence-based (CPSD) vs spatial pre-separation (ATF-GSC) framed as an SD-constrained optimal filter $\boldsymbol{h} = [\Phi_{xx} + \beta\Phi_{vv}]^{-1}\Phi_{xx}\boldsymbol{u}$; pre-modeled RTF blocking matrix robust to wearing-angle mismatch |
| [[sources/braun-2015-residual-noise-control\|Braun, Kowalczyk & Habets 2015]] | 2015 | Trade-off control | Extends the SD-constrained framework with a noise-containing target ($Z = \mathbf{e}_1^T\mathbf{x} + c\,\mathbf{e}_1^T\mathbf{v}$), yielding $\mathbf{h}_Z = (1-c)\mathbf{h}_X + c\,\mathbf{e}_1$ — direct control of maximum noise reduction without the rank-one assumption; classical origin of the DNN-era NAL knob |
| [[sources/tashev-2008-sound-capture-spatial-filter\|Tashev et al. 2008]] | 2008 | Estimate what | Back-to-back unidirectional array + probability-based spatial filter; level-difference-dominated post-filter for 9.6 mm baseline |
| [[sources/jin-2017-multichannel-noise-reduction-mobile\|Jin et al. 2017]] | 2017 | Estimate what | MVDR + adaptive coherence NE with adaptive split-frequency; globally MMSE-optimal multi-channel variance decomposition |
| [[sources/taseska-2018-informed-spatial-filters\|Taseska 2018]] | 2018 | Estimate what | ISF paradigm: CDR as a priori SAP *control* (not post-filter gain) for multichannel MCRA; DOA-model & position-based detectors drive per-bin MVDR/GSC across noise reduction, spotforming, and BSS |
| [[sources/schwarz-2015-coherent-to-diffuse-power-ratio\|Schwarz & Kellermann 2015]] | 2015 | Estimate what | Unified CDR framework; first DOA-independent unbiased CDR estimator (requires only $\Gamma_n$) |
| [[sources/schwarz-2019-dereverberation-spatial-coherence\|Schwarz 2019]] | 2019 | Estimate what | Doctoral thesis: spatial coherence models for dereverb + spatial features as DNN-ASR input |
| [[sources/kang-2019-low-complexity-permutation-alignment\|Kang, Yang & Yang 2019]] | 2019 | Estimate what | Low-complexity permutation alignment for per-bin-ICA BSS: confidence-thresholded bin-wise + local-centroid stages cut alignment runtime 4–5× at equal SIR/PESQ |
| [[sources/lollmann-2020-generalized-coherence-based-signal-enhancement\|Löllmann et al. 2020]] | 2020 | Estimate what | GMC-based CDR via eigenvalue decomposition of $N$-channel coherence matrix; implicit microphone selection via principal eigenvector |
| [[sources/scheibler-2020-fast-independent-vector-extraction\|Scheibler & Ono 2020]] | 2020 | Estimate what | Blind extraction via iterative max-SINR beamforming (FIVE): auxiliary function globally minimized per iteration; peak SDR in 1–3 iterations, an order of magnitude faster than full AuxIVA |
| [[sources/lin-2024-agadir-array-geometry-agnostic-speech-recognition\|Lin et al. 2024 (AGADIR)]] | 2024 | Geometry | Multi-geometry training + NLCMV beamformer with WNG control for smart-glasses ASR |
| [[sources/ruan-2024-speech-extraction-low-snr\|Ruan et al. 2024]] | 2024 | Estimate what | Blind extraction at −20 dB SNR: OGIVE with mixing-vector optimization + natural gradient; parameterization choice beats modeling sophistication |
| [[sources/mittal-2026-adaptive-diagonal-loading-beamforming\|Mittal et al. 2026]] | 2026 | Robustness | Kantorovich-bounded adaptive diagonal loading; deterministic WNG guarantee via condition-number bound |
| [[sources/deng-2026-joint-covariance-wng-mvdr\|Deng et al. 2026]] | 2026 | Robustness | Data-driven frequency-dependent WNG thresholds via dual-branch network + differentiable robust MVDR layer |
| [[sources/oviste-2026-neural-vslf-speech-enhancement\|Oviste et al. 2026]] | 2026 | Hybrid | HVSF: DNN predicts SCM + tradeoff → classical VSLF weights (MWF/MVDR/GEV as special cases) |
| [[sources/liu-2026-scm-reconstruction-speech-enhancement\|Liu et al. 2026 (R-MWF)]] | 2026 | Hybrid | Analytical SCM reconstruction from variance ratios + predefined coherence matrices; online $\mathcal{O}(M^2(I+2))$ |
| [[sources/farmani-2026-virtual-mic-beamforming-hearing-aid\|Farmani et al. 2026]] | 2026 | Hybrid | Virtual microphone synthesis via power-function RTF model; +3–4 dB ISNR from 2 mics + 2 VMs on HA |
| [[sources/zaidel-2026-linearly-constrained-deep-beamformer\|Zaidel et al. 2026]] | 2026 | Hybrid | Linearly-constrained deep beamformer: DNN predicts weights, augmented-Lagrangian loss enforces distortionless + null constraints |
| [[sources/huang-2026-ndf-joint-neural-directional-filtering\|Huang et al. 2026 (NDF+)]] | 2026 | Hybrid | Dual-mask neural directional filtering: jointly estimate coherent + diffuse components → controllable VDM directivity |
| [[sources/apostolidis-2026-listen-first-output-based-multi-microphone\|Apostolidis et al. 2026]] | 2026 | Where | Output-based MPDR: select candidate output by Glimpse Proportion, not input features; rehabilitates MPDR |
| [[sources/li-2026-geometry-conditioned-ssanc\|Li et al. 2026 (GC-SSF)]] | 2026 | Geometry | FiLM + DOA-MPE conditioning for target-speaker extraction across array geometries |
| [[sources/liu-2026-array-invariant-speech-enhancement\|Liu et al. 2026 (Geo-DConv)]] | 2026 | Geometry | TACT + dynamic convolution converts fixed-array backbones to array-invariant; ~10× fewer MACs than USES2-comp |
| [[sources/frank-2026-low-latency-roi-beamforming\|Frank & Cohen 2026]] | 2026 | Application | Time-domain vs STFT-domain ROI beamforming for smart glasses: 2× lower latency, higher DF, at higher compute |

## Insight 1: The Classical Coherence/CDR Lineage — DOA-Independence as the Key Relaxation

The longest-running MCSE sub-lineage is **coherence-based dereverberation**, in which the coherent-to-diffuse power ratio (CDR) is estimated from spatial coherence and applied as a spectral post-filter. The lineage's organizing principle is a **monotonic relaxation of prior-information requirements**:

| Year | Source | Prior info required | Key relaxation |
|------|--------|--------------------|-----------------|
| 2008 | [[sources/tashev-2008-sound-capture-spatial-filter\|Tashev]] | VAD + per-frame/per-bin level & delay features | Direction resolved statistically via posterior probability, not explicit DOA |
| 2015 | [[sources/schwarz-2015-coherent-to-diffuse-power-ratio\|Schwarz (DOA-dep.)]] | DOA + $\Gamma_n$ | Unified framework; unbiased estimators |
| 2015 | [[sources/schwarz-2015-coherent-to-diffuse-power-ratio\|Schwarz (DOA-indep.)]] | $\Gamma_n$ only | **First unbiased CDR estimator without DOA** — Proposal 3, MSE 0.071 vs 0.070 for best DOA-dependent |
| 2017 | [[sources/jin-2017-multichannel-noise-reduction-mobile\|Jin]] | SPP + coherence (adaptive split-freq) | Globally MMSE-optimal multi-channel variance decomposition (not pairwise averaging) |
| 2020 | [[sources/lollmann-2020-generalized-coherence-based-signal-enhancement\|Löllmann (GMC)]] | $\Gamma_n$ only (binaural model) | **Generalizes pairwise coherence to $N$ channels via eigenvalue decomposition**; implicit mic selection via principal eigenvector |

The trajectory is clear: each step removes an assumption. Schwarz 2015's **DOA-independent estimator** (Proposal 3) is the inflection point — it achieves MSE within 1% of the best DOA-dependent estimator while requiring no source localization, enabling fully blind dereverberation. Löllmann 2020's GMC then removes the pairwise-averaging suboptimality by exploiting all $N$ microphones simultaneously through the largest eigenvalue of the coherence matrix, and recovers microphone selection as a free byproduct of the principal eigenvector.

**A parallel track — CDR as detector control, not post-filter gain**: while the lineage above uses the CDR *estimate* directly as a spectral gain, [[sources/taseska-2018-informed-spatial-filters|Taseska & Habets 2018]] (Ch 3) redirect the CDR to control the *a priori Speech Absence Probability* in a [[concepts/multichannel-mcra|multichannel MCRA]] noise-PSD-matrix estimator. A sigmoid-mapped CDR → SAP is more robust to non-stationary noise-property changes than SNR-based SAPs (SC-Cohen, MC-Souden), because spatial coherence (coherent speech vs. diffuse noise) is a more reliable presence cue than energy ratios when the noise floor shifts. This is the same physical quantity (CDR) serving a *different* role in the pipeline — gating statistics updates rather than attenuating bins — and it underpins the broader [[concepts/informed-spatial-filter|ISF]] paradigm where per-bin detectors (CDR-based, DOA-model-based, or position-based) drive online PSD-matrix and RTF estimation for MVDR/MWF/GSC filters across noise reduction, spotforming, and BSS.

**Why this lineage persists in 2026**: classical coherence/CDR methods are **deterministic, low-compute, and require no training data** — properties that matter for hearing aids and mobile phones. The 2026 hybrid systems below ([[sources/oviste-2026-neural-vslf-speech-enhancement|HVSF]], [[sources/liu-2026-scm-reconstruction-speech-enhancement|R-MWF]]) deliberately keep classical filter structures and add data-driven estimation only for the SCM/noise-statistics stage, preserving these deployment advantages.

## Insight 2: MVDR Robustness — Three Eras of WNG / Condition-Number Control

MVDR beamforming's Achilles' heel is **sensitivity to array-manifold mismatch and snapshot deficiency**. The robustness frontier has advanced through three eras, each replacing an ad-hoc parameter with a principled guarantee:

### Era 1 — Ellipsoidal Uncertainty (2005)

[[sources/lorenz-2005-robust-minimum-variance-beamforming|Lorenz & Boyd 2005]] cast robust MVDR as a semi-infinite SOCP: minimize output power subject to $\mathbf{Re}\, w^* a \geq 1$ for **all** array responses $a$ in an uncertainty ellipsoid $\mathcal{E}$. The Cauchy–Schwarz reformulation yields a second-order cone constraint solvable by Newton's method on a scalar secular equation (~7–10 iterations, quadratic convergence). The RMVB guarantees unity gain over the entire ellipsoid — but the ellipsoid must be **specified** (designed from measured/simulated manifold variation). Isotropic uncertainty reduces to diagonal loading with a specific $\mu$; anisotropic uncertainty is the real gain.

### Era 2 — Kantorovich-Bounded Adaptive Loading (2026)

[[sources/mittal-2026-adaptive-diagonal-loading-beamforming|Mittal et al. 2026]] replace the fixed ellipsoid with a **deterministic WNG → condition-number bound** via the Kantorovich inequality:

$$\frac{W}{M} \geq \frac{4\kappa}{(\kappa+1)^2}, \quad \kappa_{\max} = (2A_G - 1) + 2\sqrt{A_G(A_G - 1)}$$

The required diagonal loading $\mu[i] = \max(0, (\lambda_{\max} - \kappa_{\max}\lambda_{\min})/(\kappa_{\max} - 1))$ is computed per-frame from the sample SCM, with three scalable modes (Trace $\mathcal{O}(M)$, Gershgorin $\mathcal{O}(M^2)$, Exact EVD $\mathcal{O}(M^3)$). The guarantee is **deterministic and frame-by-frame** — no design-time ellipsoid specification, no tuning of $\mu$. The Gershgorin mode is the practical sweet spot: near-EVD SINR at $\mathcal{O}(M^2)$.

### Era 3 — Data-Driven Frequency-Dependent WNG (2026)

[[sources/deng-2026-joint-covariance-wng-mvdr|Deng et al. 2026]] make the WNG threshold itself **learnable and frequency-dependent**: a dual-branch network jointly predicts T-F noise masks (for SCM estimation) and per-frequency-bin WNG thresholds $\mathcal{W}_0(k)$, integrated via a differentiable robust MVDR layer. No explicit WNG supervision is needed — the reconstruction loss naturally balances directivity vs. robustness. Results: +1.4–1.8 dB SNR gain and +1.9–2.2 dB SDR over optimally-tuned fixed-WNG baselines, with the advantage **growing under array mismatch** (unseen 1 cm / 3 cm spacings).

**The pattern**: Era 1 specified the uncertainty set at design time. Era 2 derived the loading analytically from the data at run time. Era 3 learned the optimal robustness level end-to-end. Each era subsumes the previous as a special case (Era 3 with fixed thresholds → Era 2; Era 2 with isotropic uncertainty → Era 1's diagonal-loading equivalence), but the 2026 data-driven approach is the first to make robustness **frequency-adaptive** — a degree of freedom the analytical frameworks structurally cannot exploit.

## Insight 3: The "Estimate What" Spectrum — A Relaxation Chain

Across the whole corpus, MCSE methods can be placed on a single spectrum of **what the estimator produces**, each step relaxing an assumption of the previous:

| Step | Estimate | Filter computed from | Representative |
|------|----------|---------------------|----------------|
| 1 | DOA | Steering vector → MVDR/MVDR weights | Classical MVDR |
| 2 | Coherence $\Gamma_x$ | CDR → spectral post-filter | [[sources/schwarz-2015-coherent-to-diffuse-power-ratio\|Schwarz 2015]] |
| 3 | CDR $\Lambda$ | Directly the post-filter gain $G = 1 - \sqrt{\mu/(\Lambda+1)}$ | [[sources/schwarz-2015-coherent-to-diffuse-power-ratio\|Schwarz 2015]], [[sources/lollmann-2020-generalized-coherence-based-signal-enhancement\|Löllmann 2020]] |
| 4 | SCM $\Phi_x, \Phi_n$ | MVDR/MWF/VSLF weights | [[sources/oviste-2026-neural-vslf-speech-enhancement\|HVSF]], [[sources/liu-2026-scm-reconstruction-speech-enhancement\|R-MWF]] |
| 5 | RTF $\mathbf{a}$ | Steering vector for MPDR/MVDR | [[sources/farmani-2026-virtual-mic-beamforming-hearing-aid\|Farmani 2026]], [[sources/apostolidis-2026-listen-first-output-based-multi-microphone\|Apostolidis 2026]] |
| 6 | Filter weights $\mathbf{w}$ directly | (no intermediate) | [[sources/zaidel-2026-linearly-constrained-deep-beamformer\|Zaidel 2026]], [[sources/huang-2026-ndf-joint-neural-directional-filtering\|NDF+]] |

**The tradeoff**: moving down the spectrum relaxes assumptions (DOA → coherence → SCM → direct weights) but sacrifices interpretability and controllability. Schwarz 2015's CDR estimators expose a clean physical quantity (coherent-to-diffuse ratio) with a geometric interpretation in the complex plane; Zaidel 2026's deep beamformer produces weights that satisfy constraints only statistically via the loss function. The 2026 **hybrid** methods (Steps 4–5) deliberately stop short of Step 6 to preserve the ability to inspect and control the filter — HVSF exposes the VSLF tradeoff parameter $\mu$ and span dimension $Q$, R-MWF exposes variance ratios $\psi_i, \psi_R, \psi_V$, Farmani's virtual-mic MVDR exposes the RTF power $\lambda$.

**A Step-1 variant — DOA as an SNR cue rather than a weights cue**: [[sources/kim-2014-doa-based-snr-estimation|Kim & Kim 2014]] show that the DOA cue can enter the pipeline at a different stage altogether: instead of converting a steering vector into spatial-filter weights, the phase difference of the time-aligned dual microphones is converted into a [[concepts/target-to-non-target-directional-signal-ratio|TNR]] and then a [[concepts/doa-based-snr-estimation|DOA-based a priori SNR]] for a single-reference [[concepts/wiener-filter|Wiener gain]]. This is Step-1 prior information driving a Step-2/3-style post-filter, and it quantifies the small-array ceiling of the classical beamforming branch directly: a dual-microphone SDB (Step 1 applied literally) was consistently the *worst* method in their benchmark, while the same two microphones used as a phase-difference cue beat every conventional baseline — the number of microphones constrains the SDP of a beamformer but not the information content of the inter-channel phase.

**The relaxation is not monotonic in performance**: [[sources/apostolidis-2026-listen-first-output-based-multi-microphone|Apostolidis 2026]] shows that an output-based wrapper around Step 5 (MPDR with RTF dictionary) can outperform a Step 6 end-to-end approach at low SNR — the structural prior (candidate dictionary + GP selection) beats unconstrained learned weights when input statistics are unreliable.

**A parallel blind-extraction branch (Ruan 2024)**: [[sources/ruan-2024-speech-extraction-low-snr|Ruan et al. 2024]] sit outside the spatial-statistics chain entirely — [[concepts/ogive|OGIVE]] estimates the extraction filter from statistical *independence* (non-Gaussian SOI + Gaussian background), with no DOA/coherence/SCM estimation step. At −20 dB SNR — far below the −5 dB regime of Apostolidis 2026 — they show that the **parameterization of the estimator dominates its modeling sophistication**: optimizing the mixing vector $\mathbf{a}$ (whose cost landscape has a wide, flat convergence region at low SNR) instead of the conventional demixing vector $\mathbf{w}$ is the difference between extracting the weak speech source and locking onto the dominant noise, and replacing the ordinary gradient with the natural gradient removes the remaining convergence instability. The resulting OGIVEa_NG matches [[concepts/independent-low-rank-matrix-analysis|ILRMA]] separation despite modeling only the target — the same "structure beats capacity" lesson as R-MWF (Insight 4), now extended to the blind-statistical branch and the extreme-SNR regime.

**The blind-extraction branch's speed frontier (FIVE)**: the branch's convergence-speed limit is set by [[sources/scheibler-2020-fast-independent-vector-extraction|Scheibler & Ono 2020]]'s [[concepts/fast-independent-vector-extraction|FIVE]] — iterative max-SINR beamforming in which each iteration's auxiliary function is minimized *globally* via an eigendecomposition. Where gradient-based OGIVE needs thousands of step-size-sensitive iterations, FIVE reaches peak SDR improvement in 1–3 iterations (roughly 5× faster than OverIVA, 10× than full AuxIVA), making blind extraction a real-time prospect. The two blind-extraction data points bracket the branch's tradeoffs: FIVE establishes the speed frontier under a Gaussian-background assumption, while Ruan 2024 establishes the robustness frontier at extreme SNR — both degrade when the background deviates from Gaussianity, which identifies the background model as the branch's open problem.

**The same lesson on the separation side (Kang 2019)**: the *determined-separation* branch learned the initialization-before-iteration lesson a year earlier. [[sources/kang-2019-low-complexity-permutation-alignment|Kang, Yang & Yang 2019]] show that for per-bin ICA, reordering the pipeline — cheap confidence-thresholded [[concepts/permutation-alignment|permutation alignment]] first, global one-centroid clustering second — cuts the alignment stage from 39–51 s to 7.3 s (4 sources, 10 s signals) at SIR/PESQ parity with Sawada/MBMC, because the global stage converges in <5 iterations instead of ~15. As with FIVE, the gain comes not from a better optimizer but from exploiting problem structure (inter-frequency power-ratio correlation) to start the iterative part nearly converged.

## Insight 4: Hybrid DNN-Guided Linear Filters Preserve Interpretability

A distinct 2026 cluster keeps the classical filter structure and uses a DNN only to estimate its parameters. The motivation is explicit: **interpretability + controllability + deployment robustness**.

| Method | DNN estimates | Classical filter | Controllable knob |
|--------|--------------|-------------------|-------------------|
| [[sources/oviste-2026-neural-vslf-speech-enhancement\|HVSF (Oviste 2026)]] | $\hat\Phi_x, \hat\Phi_n, \hat\mu$ | VSLF (generalizes MWF/MVDR/GEV) | Tradeoff $\mu$, span $Q$ |
| [[sources/liu-2026-scm-reconstruction-speech-enhancement\|R-MWF (Liu 2026)]] | (no DNN — analytical) | MWF with reconstructed SCM | Variance ratios $\psi_i, \psi_R, \psi_V$ |
| [[sources/farmani-2026-virtual-mic-beamforming-hearing-aid\|Farmani 2026]] | (no DNN — power-function RTF) | MVDR with virtual mics | VM position $\lambda$, VM count |
| [[sources/deng-2026-joint-covariance-wng-mvdr\|Deng 2026]] | Noise mask + WNG threshold $\mathcal{W}_0(k)$ | Robust MVDR | Frequency-dependent WNG |

R-MWF is the extreme case: **no neural network at all**, just an online $\mathcal{O}(M^2(I+2))$ multiplicative update for variance ratios against predefined coherence matrices (rank-one RTF, diffuse sinc, white identity). Yet it outperforms DG-MVDR and MVJD-MWF baselines on real RealMAN recordings (LivingRoom6: SNRseg 4.66 vs 3.07 dB; STOI 0.76 vs 0.70). The lesson: for multi-source reverberant scenes, **the SCM model matters more than the estimator's neural capacity** — a well-structured analytical decomposition (source + diffuse + noise coherence) captures the field's physical structure that a black-box mask estimator must rediscover from data.

HVSF generalizes this by letting the DNN predict the SCM decomposition (via Cholesky factorization to guarantee PSD) and the tradeoff parameter, then computing VSLF weights in closed form. The span dimension $Q$ — automatically estimated by thresholding generalized eigenvalues — provides a data-driven rank for the speech SCM that classical MWF/MVDR assume is known.

**The classical ancestor of the controllable knob (Braun 2015)**: the controllability motivation is not a 2026 invention. [[sources/braun-2015-residual-noise-control|Braun, Kowalczyk & Habets 2015]] showed that a single interpretable parameter can control a *different* axis than the distortion-vs-suppression trade-off: redefining the MWF/PMWF target as speech plus a fraction $c$ of the noise yields $\mathbf{h}_Z = (1-c)\,\mathbf{h}_X + c\,\mathbf{e}_1$, capping the maximum noise reduction and bounding speech distortion at $(1-c)^2$ — *without* the rank-one assumption that spectral-gain flooring requires, so the control survives in reverberant scenes. This knob crossed the classical→neural boundary: it reappears as the inference-time [[concepts/noise-attenuation-control|noise attenuation level (NAL)]] post-processor on μNet (2026), where it trades suppression depth against speech quality without retraining — evidence for Takeaway 1 that classical control structures outlive their statistical estimation machinery.

## Insight 5: The Input → Output Inversion (Apostolidis 2026)

[[sources/apostolidis-2026-listen-first-output-based-multi-microphone|Apostolidis et al. 2026]] inverts a long-standing structural assumption of MCSE: instead of extracting features (VAD, masks, RTF) from the **noisy input** to parameterize a filter, evaluate the SI/SQ of **candidate outputs** and select the best.

The system constructs a dictionary of MPDR beamformers indexed by candidate steering directions $\theta_i$, runs a neural VAD on each output to compute a Glimpse Proportion (GP) score, and selects the argmax. The key insight: **MPDR uses the noisy covariance $\mathbf{C_X}$ — not noise-only $\mathbf{C_V}$ — so no VAD-based noise statistics are needed to construct a candidate**. This makes MPDR a natural fit for output-based selection, despite its notorious steering-error sensitivity in conventional usage.

Results at $\text{SNR}_i = -5$ dB: ΔSNR of 10.64 dB (MPDR$_F$) vs 6.69 dB (input-based MVDR), with the advantage **growing at low SNR** — exactly where input-based VAD fails. The gain persists under RTF mismatch (coarse 15° dictionary, non-individualized HATS), demonstrating practical deployability.

**Why this matters for the synthesis**: the input→output inversion is a **structural** contribution, not a parameter-tuning one. It generalizes beyond beamforming — any SE system with a discrete configuration space (filter order, tradeoff parameter, array subset) can in principle be wrapped in an output-based selector. The 2026 work is the first to demonstrate it concretely for hearing-aid MPDR, rehabilitating a filter that classical robustness analysis (Insight 2) had largely sidelined.

**A third "where" axis — multi-frontend fusion (Yang 2025)**: [[sources/yang-2025-mc-differential-asr-smart-glasses|Yang et al. 2025]] introduce a third option orthogonal to input-based vs. output-based: rather than parameterize one filter (input-based) or select one output (output-based), **feed the downstream model multiple complementary frontend outputs in parallel**. Their differential ASR system concatenates a beamformer output (ch-x), a fixed microphone-selection output (ch-0), and a 5-dim side-talk-detection embedding as parallel input channels to a streaming RNN-T, with all frontends frozen (<1M additional trainable parameters). The 18.0% relative WER reduction over the single-MVDR-frontend baseline shows that breaking the "single frontend" assumption is a substantive structural axis — and while framed for ASR, the pattern is directly portable to MCSE pipelines that currently feed only one beamformer output to downstream consumers (ASR, codecs, assistants). The "where the decision lives" axis therefore expands from {input, output} to {input, output, multi-frontend-fusion}.

## Insight 6: Array Geometry — From Fixed to Agnostic to Conditioned

Array-geometry handling has three phases, each relaxing an assumption of the previous:

### Phase 1 — Fixed-Array (geometry-specific)

Classical MVDR, MWF, and fixed-array neural backbones (SpatialNet, TF-GridNet) are trained and deployed on **one** array geometry. Highest in-domain performance, but no cross-device transfer.

### Phase 2 — Array-Agnostic (geometry-implicit)

TAC, USES2, FOA, UniArray handle variable microphone counts and permutations by **pooling across channels** — they never see explicit geometry. Robust to permutation and count, but leave a known spatial cue (geometry) on the table. [[sources/lin-2024-agadir-array-geometry-agnostic-speech-recognition|AGADIR (Lin 2024)]] takes a hybrid route: multi-geometry **training** (data augmentation across similar geometries) with a geometry-agnostic model, generalizing to mm–cm deviations for smart-glasses ASR.

### Phase 3 — Geometry-Conditioned (geometry-explicit)

The 2026 frontier **re-injects explicit geometry** into array-invariant models:

| Method | Geometry encoding | Conditioning mechanism | Generalizes to |
|--------|-------------------|------------------------|----------------|
| [[sources/liu-2026-array-invariant-speech-enhancement\|Geo-DConv (Liu 2026)]] | Fourier PE of $(r,\theta,\phi)$ | TACT → transformation matrix → dynamic convolution kernels | ≤4-mic training → 6-mic CHiME-4 zero-shot (DNSMOS OVRL 1.42 → 2.73) |
| [[sources/li-2026-geometry-conditioned-ssanc\|GC-SSF (Li 2026)]] | DOA-MPE: polar coords + target DOA | FiLM layer modulating SSF intermediate features | Circular, ULA, random arrays (target-speaker extraction) |
| [[sources/lin-2024-agadir-array-geometry-agnostic-speech-recognition\|AGADIR (Lin 2024)]] | (implicit via multi-geometry training) | One-hot array-id embedding (multi-geometry variant) | Similar geometries (mm–cm deviations) |

The conceptual move from Phase 2 to Phase 3: array-agnostic methods threw away geometry to gain invariance; Phase 3 methods **recover the geometry cue via conditioning** while keeping invariance. Geo-DConv's TACT consumes Fourier-encoded coordinates through a permutation-equivariant Transformer, producing a transformation matrix that linearly combines basis convolution kernels into geometry-specific weights. The permutation-equivariance guarantee (point-wise PE + MHSA) ensures stable outputs under arbitrary channel ordering — the property Phase 2 methods achieved only empirically.

**The efficiency payoff**: SpatialNet-Geo-DConv matches USES2-comp quality at ~10× fewer MACs (6.08 vs 70.26 G/s) on RealMAN — explicit geometry conditioning closes most of the gap to fixed-array upper bounds at a fraction of the compute. This makes geometry-conditioned approaches the practical choice for resource-constrained deployment where array-agnostic methods are too expensive.

## Insight 7: Application-Driven Constraints Drive Architecture

The corpus shows that **form factor and use case, not algorithmic novelty, are the primary architecture drivers** for deployed MCSE:

| Application | Constraint | Architectural response | Representative |
|-------------|-----------|------------------------|----------------|
| **Hearing aids** | Sub-mW compute, binaural cue preservation, no training data | Classical CDR/GMC + binaural coherence models; output-based MPDR with dictionary | [[sources/lollmann-2020-generalized-coherence-based-signal-enhancement\|Löllmann 2020]], [[sources/farmani-2026-virtual-mic-beamforming-hearing-aid\|Farmani 2026]], [[sources/apostolidis-2026-listen-first-output-based-multi-microphone\|Apostolidis 2026]] |
| **Mobile phones** | 2–3 mics, <10 mm baseline, hands-free at arm's length | Level-difference-dominated post-filters; back-to-back unidirectional capsules; adaptive coherence NE with split-frequency | [[sources/tashev-2008-sound-capture-spatial-filter\|Tashev 2008]], [[sources/jin-2017-multichannel-noise-reduction-mobile\|Jin 2017]] |
| **Bluetooth headsets** | 2 mics, 3–4 cm baseline, near-field mouth source, wearing-angle variability (0°/45°/90°) | Pre-modeled RTF blocking matrix calibrated in quiet environment (robust to wearing mismatch and user variation); SD-constrained trade-off over pure coherence filtering; post-filtering for incoherent noise | [[sources/yan-2014-dual-mic-bt-noise-reduction\|Yan 2014]] |
| **Smart glasses** | Sub-2 ms latency, 6-mic wearable array, head motion | Time-domain ROI beamforming (2× lower latency than STFT); NLCMV with WNG + null control; multi-geometry training; multi-frontend differential ASR (beamformer + close-mic + STD embedding) | [[sources/frank-2026-low-latency-roi-beamforming\|Frank 2026]], [[sources/lin-2024-agadir-array-geometry-agnostic-speech-recognition\|AGADIR 2024]], [[sources/yang-2025-mc-differential-asr-smart-glasses\|Yang 2025]] |
| **ASR front-end** | Recognition-rate optimization, robustness to reverberation | CDR post-filter + spatial features as DNN-ASR input (beyond signal enhancement) | [[sources/schwarz-2015-coherent-to-diffuse-power-ratio\|Schwarz 2015]], [[sources/schwarz-2019-dereverberation-spatial-coherence\|Schwarz 2019]] |

[[sources/frank-2026-low-latency-roi-beamforming|Frank & Cohen 2026]] crystallize the latency–complexity–performance tradeoff for smart glasses: time-domain ROI beamforming achieves 2× lower algorithmic latency (0.5 ms at $L_y=16$) than STFT-domain, with higher directivity factor and better own-voice suppression — at the cost of $\mathcal{O}(M L_y^2)$ vs $\mathcal{O}(M L_y \log L_y)$ complexity. The conclusion is deployment-guided: "when low latency is critical and modest additional on-device computing power is available, time-domain ROI beamforming is the preferred choice."

[[sources/schwarz-2019-dereverberation-spatial-coherence|Schwarz 2019]]'s doctoral thesis reveals a complementary application-driven insight: for **ASR**, feeding spatial coherence features directly to a DNN acoustic model can outperform applying signal enhancement as a preprocessing step — the downstream model extracts more from the raw spatial features than from the enhanced signal. This reframes MCSE for ASR as **feature extraction**, not enhancement.

[[sources/yan-2014-dual-mic-bt-noise-reduction|Yan et al. 2014]] adds the earliest corpus entry for **near-field wearable arrays** and a trade-off axis the later coherence lineage leaves implicit: the coherence-function filter family (Le 1992 → CPSD) buys large noise reduction at the cost of severe speech distortion, because it never models the target statistics. Framing the same two-mic problem as a speech-distortion-constrained optimal filter, $\boldsymbol{h} = [\Phi_{xx} + \beta\Phi_{vv}]^{-1}\Phi_{xx}\boldsymbol{u}$, subsumes both the coherence family and GSC/SDW-MWF as points on a single $\beta$ (distortion-vs-NR) trade-off curve — a precursor of the $\mu$-weighted trade-off that HVSF later lets a DNN predict.

## Cross-Cutting Takeaways

1. **Classical MCSE is not obsolete in 2026.** The coherence/CDR lineage (Schwarz → Löllmann) and the analytical SCM reconstruction (R-MWF) remain competitive in resource-constrained and data-scarce settings. The 2026 hybrid methods (HVSF, R-MWF, Farmani) deliberately keep classical filter structures and add data-driven estimation only where it adds value — preserving interpretability, controllability, and deployment robustness.

2. **Robustness evolved from design-time to run-time to learned.** Lorenz 2005 (ellipsoidal RMVB) → Mittal 2026 (Kantorovich adaptive loading) → Deng 2026 (data-driven WNG). Each era subsumes the previous; the 2026 frontier makes robustness **frequency-adaptive**, a degree of freedom analytical methods structurally cannot exploit.

3. **The "estimate what" spectrum is a relaxation chain, not a replacement story.** DOA → coherence → CDR → SCM → RTF → direct weights. Each step relaxes an assumption but sacrifices interpretability. The 2026 hybrid methods deliberately stop at Steps 4–5 (SCM/RTF) to preserve controllability.

4. **The input→output inversion (Apostolidis 2026) is structural, not parametric.** It generalizes beyond beamforming to any SE system with a discrete configuration space, and rehabilitates MPDR — a filter classical robustness analysis had sidelined.

5. **Array geometry went fixed → agnostic → conditioned.** Phase 3 (geometry-conditioned) recovers the geometry cue that Phase 2 (array-agnostic) threw away, via Fourier PE + Transformer conditioning. The payoff is both quality (closes gap to fixed-array) and efficiency (~10× fewer MACs than USES2-comp).

6. **Application constraints, not algorithmic novelty, drive deployed architecture.** Hearing aids → classical CDR/GMC; mobile phones → level-difference post-filters; smart glasses → time-domain ROI beamforming; ASR → spatial features as DNN input. The "best" method is the one that fits the form-factor constraint, not the one with the highest benchmark score.

7. **MVDR remains the connective tissue.** Every era engages MVDR: classical implementations (Lorenz, Schwarz, Tashev, Jin, Löllmann), robustness research (Mittal, Deng), hybrid systems (HVSF exposes MVDR as a VSLF special case, Farmani's virtual mics feed MVDR, Apostolidis wraps MPDR). The 2026 work refines MVDR's *parameterization* (SCM estimation, WNG control, output-based steering) rather than replacing it.

## Open Questions / Future Synthesis Candidates

- **Classical-vs-neural head-to-head on shared benchmarks**: the corpus lacks a direct comparison of, e.g., GMC-based CDR (Löllmann 2020) vs. NDF+ (Huang 2026) on the same binaural HA setup. A controlled benchmark would clarify where classical methods still win.
- **Geometry-conditioned robustness**: no source jointly addresses array-geometry generalization (Insight 6) and MVDR robustness (Insight 2). Geo-DConv assumes the geometry is known exactly; combining it with Mittal's Kantorovich loading or Deng's data-driven WNG is an open frontier.
- **Output-based selection beyond beamforming**: Apostolidis 2026 demonstrates the paradigm for MPDR; extending it to VSLF span dimension, NDF directivity order, or R-MWF variance-ratio constraints is unexplored.
- **Cross-source synthesis on virtual microphone methods**: Farmani 2026 (power-function RTF), UniArray (virtual mic estimation), and NDF+ (virtual directional microphone) share a "synthesize channels you don't have" theme but use very different mechanisms — a dedicated synthesis would clarify when each applies.
