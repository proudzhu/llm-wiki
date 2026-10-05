---
type: source
created: 2026-10-05
updated: 2026-10-05
sources:
  - raw/papers/ueda-2024-online-joint-optimization/full-text.md
  - https://doi.org/10.1109/TASLP.2024.3351353
  - zotero://select/items/0_UMZX2Y4H
tags:
  - blind-source-separation
  - independent-vector-extraction
  - dereverberation
  - spatial-regularization
  - online-processing
  - low-latency
  - speech-enhancement
  - microphone-array
---

# Ueda, Nakatani, Ikeshita, Kinoshita, Araki & Makino 2024: Blind and Spatially-Regularized Online Joint Optimization of Source Separation, Dereverberation, and Noise Reduction

**Authors**: [[entities/tetsuya-ueda|Tetsuya Ueda]], [[entities/tomohiro-nakatani|Tomohiro Nakatani]], [[entities/rintaro-ikeshita|Rintaro Ikeshita]], [[entities/keisuke-kinoshita|Keisuke Kinoshita]], [[entities/shoko-araki|Shoko Araki]], [[entities/shoji-makino|Shoji Makino]] (Waseda University; NTT Communication Science Laboratories)
**Venue**: IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 32, 2024
**Type**: Journal article
**DOI**: [10.1109/TASLP.2024.3351353](https://doi.org/10.1109/TASLP.2024.3351353)
**Zotero**: [UMZX2Y4H](zotero://select/items/0_UMZX2Y4H)

## Summary

This paper proposes **online-WPE×IVE**, the first blind *online joint* optimization algorithm that performs source separation, dereverberation, and noise reduction under a **single maximum-likelihood criterion**, by introducing a forgetting factor into the joint log-likelihood of [[concepts/weighted-prediction-error|WPE]] dereverberation and [[concepts/independent-vector-extraction|IVE]] separation and deriving computationally efficient updates for it. Joint optimization (denoted ×) lets the method work with STFT frames far shorter than the reverberation time — achieving an 8 ms algorithmic delay (10.01 ms total processing delay, within the 12 ms in-car communication budget) while significantly outperforming cascaded online-WPE+IVE. The paper then extends the algorithm with DOA-based spatial regularization (online-WPE×SRIVE) and reveals that **scale regularization is indispensable** for making unit/null spatial regularization robust against IVE's scale ambiguity, reducing the source permutation error rate to 0%.

## Problem Formulation

$M$ microphones capture a reverberant mixture of $N$ source signals and $M-N$ noise signals, modeled in the STFT domain by a convolutive transfer function of length $L_A$:

$$
\boldsymbol{x}(f,t) = \sum_{\tau=0}^{L_A-1} \boldsymbol{A}(f,\tau) \begin{bmatrix} \boldsymbol{s}(f,t-\tau) \\ \boldsymbol{z}(f,t-\tau) \end{bmatrix}.
$$

Two goals: (1) obtain source estimates $\{\hat{s}_n(f,t)\}$ with high separation accuracy by **low-latency online processing**; (2) align the estimates to a specified source permutation ($\hat{s}_n \simeq s_n$ for $1 \leq n \leq N$), which the paper calls **source permutation alignment**.

**Problem 1 — low latency vs. accuracy**: in frequency-domain BSS the algorithmic delay equals the STFT frame length, but frames must be *longer than the reverberation time* for accurate separation — a direct conflict with e.g. the 12 ms delay required for in-car communication (ICC) systems. Dereverberation by WPE can remove reverberation longer than the frame, but cascaded (individually optimized) online-WPE+IVE is suboptimal because each block is optimized by its own cost function rather than a single criterion over the whole output.

![[raw/papers/ueda-2024-online-joint-optimization/figures/3c8076061c19f76acfafaccf7c07207b49f0204ab50aaa62a511224ff7930f43.jpg|Figure 1: Separation and update flow of WPE+IVE and WPE×IVE]]
*Figure 1: Individual optimization (a) WPE+IVE optimizes each block by its own cost function; joint optimization (b) WPE×IVE optimizes all cascaded blocks by a single cost function defined on the output of the whole processing.*

**Problem 2 — permutation alignment under scale ambiguity**: online-IVE separates sources in an arbitrary permutation. DOA-based [[concepts/spatial-regularization|spatial regularization]] can align the permutation, but the steering vectors derived from DOAs under the plane-wave assumption are inaccurate in real reverberant environments, and IVE's **scale ambiguity** (the likelihood is invariant to the filter power $\|\boldsymbol{w}_n\|_2^2$) can make the regularization behave inappropriately — a previously unaddressed failure mode that this paper identifies and solves.

## Methodology

### Convolutional beamformer

Offline WPE×IVE obtains estimates with a [[concepts/convolutional-beamformer|convolutional beamformer]] (CBF) applied to the augmented observation $[\boldsymbol{x}; \bar{\boldsymbol{x}}]$ (with $\bar{\boldsymbol{x}}$ the past $L$ frames delayed by $D$):

$$
\begin{bmatrix} \hat{\boldsymbol{s}}(f,t) \\ \hat{\boldsymbol{z}}(f,t) \end{bmatrix} = \begin{bmatrix} \boldsymbol{W}(f) \\ \bar{\boldsymbol{W}}(f) \end{bmatrix}^{\mathsf{H}} \begin{bmatrix} \boldsymbol{x}(f,t) \\ \bar{\boldsymbol{x}}(f,t) \end{bmatrix},
$$

which decomposes into a WPE stage and a separation stage:

$$
\boldsymbol{y}(f,t) = \boldsymbol{x}(f,t) - \boldsymbol{G}^{\mathsf{H}}(f)\,\bar{\boldsymbol{x}}(f,t), \qquad
\begin{bmatrix} \hat{\boldsymbol{s}}(f,t) \\ \hat{\boldsymbol{z}}(f,t) \end{bmatrix} = \boldsymbol{W}^{\mathsf{H}}(f)\,\boldsymbol{y}(f,t),
$$

with dereverberation filter $\boldsymbol{G} = -\bar{\boldsymbol{W}}\boldsymbol{W}^{-1}$. Sources are modeled as $\hat{\boldsymbol{s}}_n(t) \sim \mathcal{N}_\mathbb{C}(\boldsymbol{0}_F, v_n(t)\boldsymbol{I}_F)$ (time-varying variance, mutually independent over frequency — the IVE source model) and the noise as stationary $\hat{\boldsymbol{z}} \sim \mathcal{N}_\mathbb{C}(\boldsymbol{0}, \boldsymbol{\Omega})$.

### Online joint optimization (online-WPE×IVE)

For online processing, the offline negative log-likelihood is turned into a **time-weighted** version with forgetting factor $\beta$ ($0 < \beta < 1$):

$$
\mathcal{L}_\beta(\mathcal{X}_t; \Theta_t) \stackrel{c}{=} \sum_f \big(\log\det\boldsymbol{\Omega} - 2\log|\det\boldsymbol{W}|\big) + \frac{1}{\sum_{t'\leq t}\beta^{t-t'}} \sum_{f,t'\leq t} \beta^{t-t'} \Big\{ \sum_{n=1}^{N} \Big(\log v_n + \frac{|\hat{s}_n|^2}{v_n}\Big) + \hat{\boldsymbol{z}}^{\mathsf{H}}\boldsymbol{\Omega}^{-1}\hat{\boldsymbol{z}} \Big\},
$$

minimized at each frame by alternately updating the variances $\mathcal{V}_t$, separation matrices $\mathcal{W}_t$, and dereverberation filters $\mathcal{G}_t$ (each initialized from the previous frame):

1. **Variance update**: $v_n(t) \leftarrow \frac{1}{F}\sum_f |\hat{s}_n(f,t)|^2$ — the same frequency-coherent averaging that gives IVE its source grouping.
2. **Separation matrix update**: with spatial covariance matrices propagated recursively,

$$
\boldsymbol{\Sigma}_n(t) \leftarrow \beta\,\boldsymbol{\Sigma}_n(t-1) + (1-\beta)\,\frac{\boldsymbol{y}(t)\boldsymbol{y}^{\mathsf{H}}(t)}{v_n(t)},
$$

the source rows $\boldsymbol{w}_n$ update by the [[concepts/iterative-projection|iterative projection]] rule $\boldsymbol{w}_n \leftarrow \boldsymbol{\Sigma}_n^{-1}\boldsymbol{W}^{-\mathsf{H}}\boldsymbol{e}_n$ followed by $\boldsymbol{\Sigma}_n$-normalization, and the noise rows $\boldsymbol{W}_{\mathrm{Z}}$ update in closed form together with $\boldsymbol{\Omega}$ (no per-column iterations) — the IVE trick that skips most noise-related computation.
3. **Dereverberation filter update**: with recursively updated spatio-temporal covariances $\boldsymbol{R}_n, \boldsymbol{P}_n$, the source-wise dereverberation filters $\boldsymbol{G}_n = \boldsymbol{R}_n^{-1}\boldsymbol{P}_n$ update via a Kalman-gain (matrix-inversion-lemma) recursion, and the shared filter is recovered as $\boldsymbol{G} = \bar{\boldsymbol{G}}\boldsymbol{W}^{-1}$ — or, more efficiently, $\boldsymbol{G}$ is never formed and the outputs are computed per-source as $\boldsymbol{y}_n(t) = \boldsymbol{x}(t) - \boldsymbol{G}_n^{\mathsf{H}}(t)\,\bar{\boldsymbol{x}}(t)$ (**source-wise factorization**).

**Computational efficiency**: the paper derives three efficient-update devices beyond its conference predecessors — (i) $\boldsymbol{\Sigma}_n^{-1}$ via the matrix inversion lemma; (ii) $\boldsymbol{W}^{-\mathsf{H}}$ via a rank-1 update after each $\boldsymbol{w}_n$ update; (iii) a **block-matrix-inversion** formula for $\boldsymbol{W}^{-\mathsf{H}}$ after the multi-column $\boldsymbol{W}_{\mathrm{Z}}$ update (which the rank-1 lemma cannot handle). In the processing flow (Algorithm 1), $\boldsymbol{G}_n$ is updated only at the first of $N_{\mathrm{Iter}}$ iterations because WPE converges much faster than IVE, and the two blocks use **different forgetting factors** — $\alpha$ for IVE (small $M \times M$ statistics, quicker adaptation) and $\beta$ for WPE (large $ML \times ML$ statistics, slower adaptation). Complexity is $O(F(N{+}1)M^2L^2)$ per frame; **online-IVE** (drop the WPE part, $\boldsymbol{G}=\boldsymbol{0}$) costs $O(FNM^2)$ and is itself a newly proposed multi-source online extraction algorithm.

### Robust spatial regularization (online-WPE×SRIVE)

To align the source permutation, the cost gains a regularization term $\mathcal{L} = \mathcal{L}_\beta + \mathcal{J}_{\mathrm{SR}}$ built from DOA-based steering vectors $\boldsymbol{a}_n(f)$ (plane-wave model with TDOAs from the given DOAs) and three sub-terms:

$$
\mathcal{J}_{\mathrm{SR}} = \sum_{f}\sum_{n=1}^{N} \big( \lambda^{\text{unit}}\,|\boldsymbol{w}_n^{\mathsf{H}}\boldsymbol{a}_n - 1|^2 + \lambda^{\text{null}} \sum_{i \neq n} |\boldsymbol{w}_n^{\mathsf{H}}\boldsymbol{a}_i|^2 + \lambda^{\text{scale}}\,\boldsymbol{w}_n^{\mathsf{H}}\boldsymbol{w}_n \big),
$$

- **unit** — respond with 1 to the target direction (distortionless response);
- **null** — place spatial nulls on the interferers' directions;
- **scale** — penalize the filter power $\|\boldsymbol{w}_n\|_2^2$.

The update rules modify IP by replacing $\boldsymbol{\Sigma}_n$ with $\boldsymbol{\Pi}_n = \boldsymbol{\Sigma}_n + \lambda^{\text{scale}}\boldsymbol{I} + \sum_i \lambda_{ni}\boldsymbol{a}_i\boldsymbol{a}_i^{\mathsf{H}}$; for $\lambda^{\text{unit}} \neq 0$ the closed form becomes a vectorwise coordinate descent (VCD) update. Noise rows $\boldsymbol{W}_{\mathrm{Z}}$ are unaffected. Introducing spatial regularization adds **zero** computational complexity.

**Key insight — scale regularization is indispensable**: because the IVE likelihood is invariant to filter scale, the estimated $\|\boldsymbol{w}_n\|_2^2$ can become arbitrarily large. Then (i) *unit* no longer enhances the target — a filter with $\|\boldsymbol{w}_n\|_2^2 \gg 1$ that responds 1 to $\boldsymbol{a}_n$ greatly enhances the space *orthogonal* to the target direction, suppressing the target relatively; (ii) *null* dominates the objective function — the alignment is decided solely by the (reverberation-corrupted, especially at low frequencies) DOA-based nulls, disabling IVE's source grouping. Penalizing filter power via *scale* restores the intended behavior of both terms.

![[raw/papers/ueda-2024-online-joint-optimization/figures/f329bb2b9006105ca5e8d42226e59eb619de879ea70b1ed95f162ee424e53aa9.jpg|Figure 2a: unit works when filter power converges close to 1]]
![[raw/papers/ueda-2024-online-joint-optimization/figures/205d2769901db81267b8276074e58b4d2a7e760c43ad6310c61a1fb4a7a8c241.jpg|Figure 2b: with filter power much greater than 1, unit enhances the space orthogonal to the target]]
*Figure 2: Example behaviors of the separation filter optimized using unit regularization.*

![[raw/papers/ueda-2024-online-joint-optimization/figures/055d03c1b872ff6287998f5c2834c7b9daef09677cbd71f2e29449a873ff9aae.jpg|Figure 3a: IVE w/o null groups sources correctly but permutation is arbitrary]]
![[raw/papers/ueda-2024-online-joint-optimization/figures/17d12cc9eb9eb72ea3d221eaa60f05e28bf535306daa67a165387d88bd28175f.jpg|Figure 3b: IVE w/ null achieves correct grouping and permutation alignment]]
![[raw/papers/ueda-2024-online-joint-optimization/figures/93d835874f527baf3d91b7da38758f37c4a9c695bb093279eccf7d7c09868363.jpg|Figure 3c: with scale ambiguity, null dominates and estimation fails in low frequencies]]
*Figure 3: Behavior of IVE with and without null regularization for source grouping and source permutation alignment.*

## Experimental Setup

| Item | Setting |
|---|---|
| Data | ATR digital speech database set B (10 speakers, 6M/4F); 100 mixtures of 2 speakers, each 20 s |
| RIRs / noise | Car environment (self-recorded, RT60 ≈ 60 ms); office = RWCP Sound Scene Database OFC (RT60 ≈ 780 ms) |
| Geometry | Speakers at 130° and 50°; linear arrays (car: $d = 0.021$ m; office: 5 mics #19–23, $d = 0.0281$ m) |
| Sampling / STFT | 16 kHz; 8 ms frame / 4 ms shift (→ 8 ms algorithmic delay), square-root Hanning window |
| Forgetting factors | $\alpha = 0.99$ (IVE), $\beta = 0.9999$ (WPE) |
| WPE parameters | Car: $L = 4$, $D = 1$, $N_{\mathrm{Iter}} = 2$; Office: $L = 21$, $D = 2$, $N_{\mathrm{Iter}} = 5$ (not real-time capable) |
| Methods compared | online-IVE, online-WPE+IVE (cascade), online-WPE×IVE (joint), and each with spatial regularization (online-SRIVE, online-WPE+SRIVE, online-WPE×SRIVE); offline-WPE×IVE as reference |
| Metrics | SegSDR (2 s segments), Total-SDRi/SIRi/SARi (bss_eval v3, 512 taps, dry-source reference), permutation error permE (fraction of 100 mixtures with incorrect permutation) |
| SNRs | 0, 10, 30 dB input SNR |
| Hardware | Python 3.7.7, Intel Xeon Gold 2.4 GHz single core |

![[raw/papers/ueda-2024-online-joint-optimization/figures/3ce93f50687b065e6d2fb3f5fa87ab59c67deadb09ab8024e2b39c531ffc5799.jpg|Figure 4: Sound source and microphone layout in the ICC scenario]]
*Figure 4: Sound source and microphone layout in the ICC (in-car communication) scenario.*

## Results

### Blind joint optimization (Problem 1)

In the car environment (Table V), online-WPE×IVE consistently beat both cascading and plain online-IVE:

| Method (0 dB SNR) | SDRi [dB] | SIRi [dB] | SARi [dB] | Time [s] |
|---|---|---|---|---|
| online-IVE | 8.13 | 13.44 | 3.92 | 4.63 |
| online-WPE+IVE | 9.50 | 14.73 | 4.86 | 6.30 |
| online-WPE×IVE | **10.82** | **15.60** | **6.04** | 10.6 |

The 10.6 s computing time for 20 s of audio (5000 frames) is **2.01 ms/frame**, giving a total delay of **10.01 ms < 12 ms** — real-time capable for ICC. The same ordering holds at 10 and 30 dB SNR and in the office environment (Table VI: SDRi 3.48 vs 3.28 vs 1.96 dB at 0 dB SNR), where the long WPE filter ($L = 21$) prevents real-time operation in the current implementation but the joint method clearly wins in SIRi at all SNRs.

![[raw/papers/ueda-2024-online-joint-optimization/figures/c35e45e84f6edf6b45ef33439f9781fdaafa6d94b07df47fd46d6ac2d045aec2.jpg|Figure 5: SegSDR in car environment with 0 dB input-SNR]]
*Figure 5: SegSDR over time in the car environment (0 dB input-SNR); error bars are 1.96× standard error. online-WPE×IVE significantly exceeds the other online methods after ~4 s; offline-WPE×IVE is best but has 20 s algorithmic delay.*

**Forgetting factors**: varying $\alpha$ (IVE) controls the SegSDR level and convergence speed; shrinking $\beta$ (WPE) from 0.9999 to 0.99 destabilized the optimization after 10 s and dropped SegSDRs drastically. Using *different* forgetting factors per block ($\alpha = 0.99$, $\beta = 0.9999$) was consistently best in both environments — matching the statistics sizes ($M \times M$ for IVE vs $ML \times ML$ for WPE).

### Spatial regularization (Problem 2)

Permutation error heatmaps over the regularization weights (Fig. 9) and the joint evaluation (Tables VIII–IX, car 0 dB / office 10 dB SNR):

| Method | Reg. config | SDRi [dB] | SIRi [dB] | permE [%] |
|---|---|---|---|---|
| online-WPE×SRIVE (car) | none | 10.82 | 15.60 | 32 |
| online-WPE×SRIVE (car) | null, $\lambda{=}10$ | **12.23** | 16.70 | 3 |
| online-WPE×SRIVE (car) | null + scale ($10^{-4}$) | 11.29 | **17.67** | **0** |
| online-WPE×SRIVE (car) | unit, $\lambda{=}10$ | 9.08 | 15.40 | 98 |
| online-WPE×SRIVE (car) | unit + scale ($\lambda{=}10$) | 9.26 | 16.47 | **0** |
| online-WPE×SRIVE (office) | none | 2.77 | 5.37 | 37 |
| online-WPE×SRIVE (office) | null, $\lambda{=}10$ | 3.14 | 5.77 | **0** |
| online-WPE×SRIVE (office) | null + scale ($10^{-4}$) | **3.25** | **6.00** | **0** |
| online-WPE×SRIVE (office) | unit, $\lambda{=}10$ | 2.49 | 5.48 | 100 |
| online-WPE×SRIVE (office) | unit + scale ($\lambda{=}1$) | 2.98 | 6.25 | **0** |

![[raw/papers/ueda-2024-online-joint-optimization/figures/a8296e332981a325efb17db9f143fa89d2bb5388ba7e3926a19432de49acbe5d.jpg|Figure 9a: permE with unit in car environment]]
![[raw/papers/ueda-2024-online-joint-optimization/figures/3380ae5ddf12cfb03875c5c7876df2d31bb1f36ec9a8f6efd59a620ead1d51c0.jpg|Figure 9b: permE with null in car environment]]
![[raw/papers/ueda-2024-online-joint-optimization/figures/4f984c7a821894c80753c17cb4f290152b851b390fd52e6e013543a0417fe6be.jpg|Figure 9c: permE with unit in office environment]]
![[raw/papers/ueda-2024-online-joint-optimization/figures/286bca837e0242f4da636e03e8ae1d9c585c3eeeeb7acb5456a7bef55a3b88cc.jpg|Figure 9d: permE with null in office environment]]
*Figure 9: Permutation error (permE) as a function of the regularization weights (white = 0%). Zero permE is achieved only with scale > 0 in the car environment for both unit and null; in the office, null alone suffices but unit requires scale.*

The mechanism is confirmed by the root-mean-square norm (RMSN) of the estimated filters: without scale, unit produced filters with RMSN 2773.35 (car) / 30.21 (office) that *suppressed* the target's oracle steering vector; with scale the RMSN fell to 0.93 / 0.89 and the filters enhanced the target while nulling the interferer. For null without scale (RMSN 3963.4 in the car), the DOA-based null dominated and misaligned the permutation exactly in the low-frequency region where the DOA-based steering vector deviates most from the oracle; with scale (RMSN 16.54) the full band aligned correctly. In the office, null alone (RMSN 73.27) already achieved 0% permE.

**Conclusions**: (1) scale is *necessary* for unit to work at all; (2) scale also rescues null whenever reverberation corrupts the low-frequency DOA cues; (3) null + scale never degraded — and usually improved — SDRi/SIRi over no regularization, while achieving 0% permE for online joint optimization.

## Key Contributions

1. **online-WPE×IVE** — the first blind *online joint* optimization of source separation, dereverberation, and noise reduction under a single maximum-likelihood criterion (with forgetting factor), with computationally efficient updates: matrix-inversion-lemma recursions for $\boldsymbol{\Sigma}_n^{-1}$ and $\boldsymbol{W}^{-\mathsf{H}}$, a new block-inversion update of $\boldsymbol{W}^{-\mathsf{H}}$ after the multi-column $\boldsymbol{W}_{\mathrm{Z}}$ update, and source-wise-factorized WPE updates skipping the shared $\boldsymbol{G}$.
2. **online-IVE and online-SRIVE** — the first online IVE algorithms for *multi-source* extraction (obtained by dropping the WPE part), extending online IVA's efficiency trick (closed-form noise-row updates) to the extraction scenario.
3. **Robust spatial regularization via scale regularization** — the discovery that penalizing filter power is *indispensable* to make DOA-based unit/null regularization behave as intended under IVE's scale ambiguity, with filter-RMSN and directional-response evidence, reducing the source permutation error of online joint optimization to 0%.
4. **Low-latency validation** — 8 ms algorithmic delay and 10.01 ms total delay (12 ms ICC budget) with significantly better separation than cascaded online-WPE+IVE in both a car (RT60 ≈ 60 ms) and a highly reverberant office (RT60 ≈ 780 ms); the value of *different* forgetting factors per block (α for IVE, β for WPE) is demonstrated experimentally.

This paper extends the authors' conference versions (online-WPE×IVA, ICASSP 2021; online-WPE×IVE, EUSIPCO 2021) with the complete derivations, the spatial regularization analysis, and long-reverberation evaluations.

## Related Concepts

- [[concepts/online-joint-optimization|Online Joint Optimization (online-WPE×IVE)]]
- [[concepts/convolutional-beamformer|Convolutional Beamformer]]
- [[concepts/independent-vector-extraction|Independent Vector Extraction]]
- [[concepts/weighted-prediction-error|Weighted Prediction Error (WPE)]]
- [[concepts/online-iva|Online IVA]]
- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/spatial-regularization|Spatial Regularization]]
- [[concepts/permutation-alignment|Permutation Alignment]]
- [[concepts/iterative-projection|Iterative Projection]]
- [[concepts/dereverberation|Dereverberation]]

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] — positions model-based joint optimization vs. neural approaches in the real-time speech enhancement landscape
