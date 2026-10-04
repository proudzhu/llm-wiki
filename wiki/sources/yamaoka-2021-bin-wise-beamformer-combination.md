---
type: source
created: 2026-10-04
updated: 2026-10-04
sources:
  - raw/papers/yamaoka-2021-bin-wise-beamformer-combination/full-text.md
  - https://doi.org/10.1109/TASLP.2021.3126950
  - zotero://select/items/0_8WPT8DAW
tags:
  - beamforming
  - speech-enhancement
  - underdetermined
  - time-frequency-masking
  - array-processing
  - distortionless
---

# Yamaoka, Ono & Makino 2021: TF-Bin-Wise Linear Combination of Beamformers

**Authors**: [[entities/kouei-yamaoka|Kouei Yamaoka]], [[entities/nobutaka-ono|Nobutaka Ono]], [[entities/shoji-makino|Shoji Makino]]
**Venue**: IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 29, pp. 3461–3475
**Year**: 2021
**Type**: Journal article
**DOI**: [10.1109/TASLP.2021.3126950](https://doi.org/10.1109/TASLP.2021.3126950)
**Zotero**: [8WPT8DAW](zotero://select/items/0_8WPT8DAW)
**Award**: TAF Telecom System Technology Student Award (Telecommunications Advancement Foundation)

## Summary

This paper proposes the **time-frequency-bin-wise linear combination (TFLC) beamformer**, which achieves distortionless signal enhancement in underdetermined situations ($M < N$) by combining $K$ MVDR-type beamformers per TF bin — each suppressing a different set of $M-1$ interferers — with weights $c_k(f,t)$ optimized jointly with the filters under a unified minimum variance criterion. It generalizes the authors' earlier TF-bin-wise switching (TFS) beamformer (binary selection) to continuous weights, derives a geometric convex-hull solution for the weight update, and introduces the restricted variant RTFLC that avoids target cancellation. Verified with the newly defined SRDR metric, the RTFLC beamformer attains high noise reduction in underdetermined cases while keeping the distortionless property of MVDR.

## Problem Formulation

**Signal model.** In the STFT domain, $M$ microphone signals observe one target and $N-1$ interferers:

$$
\boldsymbol{x}(f,t) = \boldsymbol{a}(f)\,s(f,t) + \sum_{n=1}^{N-1} \boldsymbol{h}_n(f)\,u_n(f,t),
$$

where $\boldsymbol{a}(f)$ is the [[concepts/relative-transfer-function|relative transfer function (RTF)]] of the target (normalized so the reference microphone has unit gain) and $s(f,t)$ is the target source image at the reference microphone — the estimation goal. The RTF is assumed **known** (exact RTF from DFT of impulse responses; eigenvector-based estimate for live recordings), so this is informed spatial filtering, not blind separation.

**Distortionless property.** An enhancement operator $G$ is *distortionless* if, applied to a noise-free observation with parameters $\theta$ estimated from noisy data, it returns the target unmodified: $s = G[\boldsymbol{a}s; \theta, \boldsymbol{a}]$. MVDR (and LCMV) possess it; TF masking, MWF-type filters, and MNMF do not.

**The tradeoff.** A conventional time-invariant MVDR beamformer with $M$ microphones suppresses at most $M-1$ interferers, so its noise reduction collapses in underdetermined situations, while TF masking works well there but distorts. Table I of the paper positions the TFLC beamformer as the first method in this comparison holding **both** properties (distortionless ○ and underdetermined noise reduction ○), at the cost of requiring the target RTF.

**Key idea.** Build $K$ beamformers, each with a spatial null toward a different combination of $M-1$ interferers. At each TF bin, only $M-1$ interferers are (approximately) dominant by sparsity, so *some* beamformer in this set can suppress whatever is active. The enhancement picks or mixes the best beamformer per TF bin — TF masking logic applied to *beamformer outputs* instead of scalar gains.

![[raw/papers/yamaoka-2021-bin-wise-beamformer-combination/figures/5c18be2b4d5e44bb087d72a8dfec8f61e4e1621beb6a93f74c3c525e72ad951b.jpg|Fig. 1]]
*Figure 1: Combining two beamformers, each with a spatial null for one interferer, in the underdetermined case $M=2$, $N=3$.*

## Methodology

### Joint optimization problem

Signal enhancement with $K$ beamformers and weights $c_k(f,t) \in [0,1]$ (the **beamformer selection mask**):

$$
y(f,t) = \sum_{k=1}^{K} c_k(f,t)\, y_k(f,t), \qquad y_k(f,t) = \boldsymbol{w}_k^{\mathsf{H}}(f)\,\boldsymbol{x}(f,t),
$$

$$
\min_{\boldsymbol{w}_k,\, c_k} \sum_{f} \frac{1}{T}\sum_t \left| \sum_{k=1}^{K} c_k(f,t)\,\boldsymbol{w}_k^{\mathsf{H}}(f)\,\boldsymbol{x}(f,t) \right|^2
\quad \text{s.t.} \quad
\boldsymbol{w}_k^{\mathsf{H}}(f)\boldsymbol{a}(f) = 1,\;
\sum_{k=1}^{K} c_k(f,t) = 1.
$$

**Proposition 1 (distortionlessness is preserved)**: a convex combination of distortionless filters is distortionless, because $\sum_k c_k\, \boldsymbol{w}_k^{\mathsf{H}}\boldsymbol{a} = \sum_k c_k = 1$. Both constraints exist precisely to keep the target undistorted. All formulas reduce to the conventional MVDR beamformer when $K=1$.

### TFS beamformer (binary special case)

$c_k^{\mathrm{b}}(f,t) \in \{0,1\}$ selects exactly one beamformer per TF bin. Alternating updates:

1. **Filters** — with the mask fixed, each $\boldsymbol{w}_k$ is an MVDR solution on the masked covariance $\Phi_{kk}(f) = \frac{1}{T}\sum_t \boldsymbol{x}_k(f,t)\boldsymbol{x}_k^{\mathsf{H}}(f,t)$, where $\boldsymbol{x}_k(f,t) = c_k(f,t)\boldsymbol{x}(f,t)$. The masking turns the underdetermined problem into a (over)determined one per cluster.
2. **Mask** — with filters fixed, select the beamformer with minimum output power $|\boldsymbol{w}_k^{\mathsf{H}}(f)\boldsymbol{x}(f,t)|^2$ at each TF bin. This acts as a **clustering of the dominant interferers**: each cluster's TF bins define the covariance for its beamformer.

### TFLC beamformer (continuous generalization)

1. **Filters** — Lagrangian stationary point with all cross-terms $\Phi_{ij}(f)$ ($i \neq j$):

$$
\boldsymbol{w}_i^{\text{(TFLC)}}(f) = \left(1 + \boldsymbol{a}^{\mathsf{H}}(f)\boldsymbol{u}_i(f)\right) \boldsymbol{w}_i^{\text{(TFS)}}(f) - \boldsymbol{u}_i(f), \qquad
\boldsymbol{u}_i(f) = \Phi_{ii}^{-1}(f) \sum_{j \neq i} \Phi_{ij}(f)\,\boldsymbol{w}_j(f).
$$

   Each filter is optimized knowing the others, so residual interferer outputs can be placed **in antiphase** and cancel in the sum — extra noise reduction beyond null steering. The risk: the same mechanism can cancel the *target* (the "antiphase problem").

2. **Mask** — geometric solution on the complex plane: $y = \sum_k c_k y_k$ with $\sum_k c_k = 1$ means $y$ lies in the convex hull of the beamformer outputs $\{y_k\}$.
   - $K = 2$: the optimal $y$ is the point on the segment $[y_1, y_2]$ closest to the origin (internal division).
   - $K \geq 3$: if the origin is outside the hull, the problem reduces to the closest edge; if inside, choose a triangle of vertices containing the origin (e.g., minimum area) and solve $y = 0$ with its positive weights.

![[raw/papers/yamaoka-2021-bin-wise-beamformer-combination/figures/6647e6bfc71f4a872b8010f3f02d9561420405d9b8c51cb0a01741b36e858bcb.jpg|Fig. 2 left]]
![[raw/papers/yamaoka-2021-bin-wise-beamformer-combination/figures/703e726956ddf13f1ca3c30bd49cd8f6911454054f830b7b1f6b06253cee42b5.jpg|Fig. 2 right]]
*Figure 2: Mask update geometry. Left: origin outside the convex hull — optimum on the closest edge ($c_5 = 0.6$, $c_6 = 0.4$). Right: origin inside — choose a containing triangle ($c_4 = 0.47$, $c_5 = 0.31$, $c_6 = 0.22$).*

### RTFLC beamformer (restricted variant)

Update the mask continuously (as in TFLC) but the filters by the TFS rule (25) on the weighted covariance — i.e., force $\boldsymbol{u}_i(f) = 0$. This forgoes antiphase cancellation but eliminates the target-cancellation risk and the instability of coupled updates; experimentally it is the best-performing variant.

### Initialization and sparsity

- **Initialization** (`-R`/`-N`/`-P` suffixes): random filters; fixed **null beamformers** from DOAs (anechoic model, DOAs may even be random); or **predesigned MVDR** filters from per-interferer covariance matrices. Null-beamformer initialization also fixes the permutation consistently across frequency (each filter keeps "its" interferer combination).
- **P-DO sparsity**: generalizes [[concepts/w-disjoint-orthogonality|W-disjoint orthogonality]] from "at most 1 source per TF bin" to "at most $P-1$ of $P$ sources per TF bin" ($\prod_{p=1}^{P} z_p(f,t) = 0$). The methods assume every $M$-combination of the $N-1$ interferers satisfies M-DO, i.e., at most $M-1$ interferers per TF bin — under which $K = C(N-1, M-1)$ beamformers are sufficient.

## Experimental Setup

Two experiment blocks. **Empirical analysis** (Section V): SiSEC UND dev1 female speech, simulated RIRs ($T_{60} = 120$ ms), $M=2$ (4 cm), $N=3$, DOAs 90°/50°/150°, 8 kHz, 1024/512 samples frame/shift, $K=2$, 5 s prior + 35 s enhancement. **Performance evaluation** (Section VI): dev1 (live-recorded, $M=2$, 5 cm, $N \in \{3,4\}$), dev3 (simulated from real RIRs, $M=3$, $N=4$), 16 kHz, frame lengths $2^i$ ($i = 8 \ldots 14$), half-overlap, 5 s prior + 5 s enhancement, $K = C(N-1, M-1)$, RTF from impulse-response DFT (dev1/dev3) or eigenvector of target covariance (live). Additional controlled studies via RIR generator: distortionless-property experiment (1000 trials, vs. TV-MWF and ideal binary mask), $K$/$M$/$N$ sweep ($T_{60}=200$ ms, 2048-sample frames, random init), and RTF-mismatch robustness (RTF contaminated by additive white Gaussian noise at controlled SNR).

**Metrics**: SDR, SIR, SAR (Vincent et al. 2006), plus the newly defined **SRDR** ([[concepts/signal-to-reconstruction-distortion-ratio|signal-to-reconstruction distortion ratio]]) that isolates algorithmic distortion by measuring against the interference-free reverberant target.

## Results

**Empirical analysis.** The binary selection mask switches frequently across the TF plane; each masked intermediate signal $y_k(f,t)$ contains a "perforated" target plus one suppressed-and-residual interferer, and their sum restores the target completely (Fig. 4). Iterating the clustering-like updates straightens the spatial nulls toward the true interferer DOAs within a few iterations (Fig. 5). The soft (RTFLC) mask agrees with the binary mask where one beamformer clearly dominates but differs by more than 0.5 in bins where binary switching was picking a wrongly-steered filter — the linear combination fixes wrong selection at high frequencies (Fig. 6). Cost-function convergence: both TFS and RTFLC converge in a few iterations, but TFS with bad initialization converges to worse local minima, while RTFLC is robust to initialization (small variance over 100 trials).

![[raw/papers/yamaoka-2021-bin-wise-beamformer-combination/figures/ed905f01f607d7ba3ebd71f4b6e4806f7b950403754e008dfca05fd09bab6986.jpg|Fig. 4a]]
![[raw/papers/yamaoka-2021-bin-wise-beamformer-combination/figures/de7179d2e8b49c8d8a67e6f91e967e163f3b079b9bb1774c42855e2cf8cfbbf9.jpg|Fig. 4b]]
![[raw/papers/yamaoka-2021-bin-wise-beamformer-combination/figures/244baac6f583c6db1a39e49f812def8de3c81ff5b015773566d3b09dc69587d0.jpg|Fig. 4c]]
![[raw/papers/yamaoka-2021-bin-wise-beamformer-combination/figures/d0ffcae02370c7fdca46c8da4fe66616f576bf153693a432d7a834bc5a691473.jpg|Fig. 4d]]
*Figure 4: TFS-P enhancement example. (a) Binary beamformer selection mask $c_k(f,t)$ (green $k=1$, blue $k=2$); (b) reconstructed enhanced signal; (c), (d) intermediate signals $y_1$, $y_2$ masked by $c_1$, $c_2$.*

**SiSEC performance** (Fig. 8, best frame length per method). MVDR alone: good SAR only (suppresses one interferer). TFS-P: notable SDR/SIR gains while keeping high SAR. TFS-N (no per-interferer covariance prior) is weaker than TFS-P; **TFLC-N recovers TFS-P-level performance without per-interferer priors** — the antiphase cancellation of residual interferers compensates for the missing prior. Full TFLC achieves the best SIR but risks target counteraction; **RTFLC achieves the best overall balance** — SDR improvements with SAR comparable to or better than MVDR. Random initialization already yields most of the gain.

**Optimal frame length.** The methods sit between TF masking (needs short frames for sparsity) and beamforming (needs frames longer than the ATF), so an interior optimum exists: 2048 samples at $T_{60}=120$ ms and 8192 at 380 ms — i.e., the smallest frame length exceeding the impulse-response length.

**Distortionless property** (Fig. 10, 1000 trials). IBM: high SDR, low SRDR. TV-MWF: highest SDR (MMSE-optimal) but limited SRDR — no distortionless constraint. MVDR: high SRDR, low SDR in the underdetermined case. **RTFLC-N (frame $2^{11}$): +5.9 dB SDR over MVDR at only −2.2 dB SRDR, and +17.4 dB SRDR over TV-MWF at only −0.6 dB SDR** — high noise reduction *and* near-distortionless output.

![[raw/papers/yamaoka-2021-bin-wise-beamformer-combination/figures/b77689fa6bdf78f336ccfab5611181b6cef8061f5bb74becaeab5a9c133a1abb.jpg|Fig. 10]]
*Figure 10: Average SRDR vs. average SDR over frame lengths ($i = 1\ldots7$ corresponds to $2^{i+7}$ samples). Proposed methods achieve MVDR-level SRDR with much higher SDR.*

**Scaling with $K$, $M$, $N$** (Fig. 11). Performance is insensitive around $K = C(N-1,M-1)$; in underdetermined cases all variants beat MVDR, and **RTFLC improves monotonically as $K$ grows**. In (over)determined cases TFS/RTFLC still beat MVDR (they suppress reverberant interferer components), but full TFLC **degrades** for large $K$ — its excess degrees of freedom let filters cancel the target through the residual-noise antiphase mechanism.

![[raw/papers/yamaoka-2021-bin-wise-beamformer-combination/figures/3eb0a094cd736cfd866d54b36ad284f8b48811f24382199d81aea55e96db65a7.jpg|Fig. 11]]
*Figure 11: SDR as a function of $K$ for $M \in \{2,3\}$, $N \in \{2,\ldots,6\}$ ($T_{60}=200$ ms). RTFLC improves monotonically with $K$; TFLC has an interior optimum and collapses at large $K$.*

**RTF-mismatch robustness** (Fig. 12). Performance follows MVDR's while the RTF estimate is accurate, but degrades rapidly when the RTF SNR falls below **40 dB** — the methods require a precise RTF, making RTF estimation a coupled essential problem.

![[raw/papers/yamaoka-2021-bin-wise-beamformer-combination/figures/7b6ef8d896d0823cc566e80e32756202a74a53c8d1fc0dae73f2033b5a1028a6.jpg|Fig. 12]]
*Figure 12: SDR as a function of RTF accuracy (SNR of contaminated impulse response). Performance drops sharply below 40 dB RTF SNR.*

## Key Contributions

1. **TFLC beamforming framework**: a general formulation of signal enhancement as a TF-bin-wise linear combination of multiple distortionless beamformers, with a joint optimization problem (filters + weights) under a unified minimum variance criterion — reducing exactly to MVDR at $K=1$ and generalizing the authors' earlier TFS beamformer (EUSIPCO 2018, ICASSP 2019).
2. **Distortionlessness proof for combinations**: Proposition 1 — convex combinations of distortionless filters remain distortionless — so nonlinear (per-bin) behavior is obtained without sacrificing the distortionless response that ASR front-ends need.
3. **Geometric mask-update algorithm**: a convex-hull solution (edge projection / origin-containing triangle) for the per-bin weight optimization, replacing generic constrained programming.
4. **RTFLC variant**: identifying and fixing the target-cancellation ("antiphase") failure mode of full TFLC by restricting filter updates to weighted-covariance MVDR — empirically the best variant.
5. **P-DO sparsity generalization**: relaxes W-disjoint orthogonality to "at most $P-1$ of $P$ sources active per TF bin", matching the $M-1$-interferers-per-bin assumption behind $K = C(N-1,M-1)$ beamformers.
6. **SRDR metric**: an objective criterion isolating algorithmic signal distortion from interference, used to verify the distortionless property empirically.
7. **Empirical characterization**: optimal frame length ≈ smallest frame longer than the impulse response; robustness to initialization; monotone RTFLC gains with $K$; the 40 dB RTF-accuracy requirement.

## Related Concepts

- [[concepts/tflc-beamformer|TFLC Beamforming]] — the paper's core contribution (TFS/TFLC/RTFLC variants and the beamformer selection mask)
- [[concepts/mvdr-beamformer|MVDR Beamformer]] — the $K=1$ base case and per-cluster filter design
- [[concepts/relative-transfer-function|Relative Transfer Function (RTF)]] — assumed-known steering information; robustness analysis quantifies the required precision
- [[concepts/w-disjoint-orthogonality|W-Disjoint Orthogonality]] — sparsity assumption generalized to P-DO
- [[concepts/signal-to-reconstruction-distortion-ratio|Signal-to-Reconstruction Distortion Ratio (SRDR)]] — metric defined to evaluate the distortionless property
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]] — SDW-MWF/TV-MWF as the distortion-vs-noise-reduction tradeoff contrast
- [[concepts/ideal-binary-mask|Ideal Binary Mask]] — masking baseline in the SRDR experiment
- [[concepts/beamforming|Beamforming]] — parent field

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
