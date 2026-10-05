---
type: concept
created: 2026-10-05
updated: 2026-10-05
sources:
  - raw/papers/ueda-2024-online-joint-optimization/full-text.md
tags:
  - blind-source-separation
  - independent-vector-extraction
  - dereverberation
  - online-processing
  - low-latency
  - optimization-algorithms
---

# Online Joint Optimization (online-WPE×IVE)

**Online joint optimization** (denoted **online-WPE×IVE**) is the frame-wise, real-time algorithm introduced by [[entities/tetsuya-ueda|Tetsuya Ueda]] et al. (TASLP 2024) that jointly optimizes [[concepts/weighted-prediction-error|WPE]] dereverberation and [[concepts/independent-vector-extraction|IVE]] separation under a **single maximum-likelihood criterion** — the first blind algorithm to perform source separation, dereverberation, and noise reduction *online* by joint optimization. The "×" notation distinguishes it from cascaded ("+") configurations, where WPE and IVE are each optimized by their own cost function; joint optimization lets a short STFT frame (8 ms) achieve accuracy that would otherwise require frames longer than the reverberation time.

## Key Formulations

### Negative log-likelihood with forgetting factor

The offline joint WPE×IVE likelihood is turned into an online objective by exponentially weighting past frames with forgetting factor $\beta$ ($0 < \beta < 1$):

$$
\mathcal{L}_\beta(\mathcal{X}_t; \Theta_t) \stackrel{c}{=} \sum_f \big(\log\det\boldsymbol{\Omega} - 2\log|\det\boldsymbol{W}|\big) + \frac{1}{\sum_{t'\leq t}\beta^{t-t'}} \sum_{f,t'\leq t} \beta^{t-t'} \Big\{ \sum_{n=1}^{N} \Big(\log v_n + \frac{|\hat{s}_n|^2}{v_n}\Big) + \hat{\boldsymbol{z}}^{\mathsf{H}}\boldsymbol{\Omega}^{-1}\hat{\boldsymbol{z}} \Big\},
$$

minimized at each frame by alternately updating time-varying source variances $\mathcal{V}_t$, separation matrices $\mathcal{W}_t$, and dereverberation filters $\mathcal{G}_t$ (each initialized from the previous frame). The IVE source model (frequency-coherent variance $v_n(t)$, stationary Gaussian noise) is unchanged from offline.

### Update rules

| Variable | Update | Device |
|---|---|---|
| $v_n(t)$ | $\frac{1}{F}\sum_f \|\hat{s}_n(f,t)\|^2$ | IVE source grouping (same as offline) |
| $\boldsymbol{\Sigma}_n(t)$ | $\beta\boldsymbol{\Sigma}_n(t{-}1) + (1-\beta)\,\boldsymbol{y}(t)\boldsymbol{y}^{\mathsf{H}}(t)/v_n(t)$ | recursive covariance; inverted via matrix inversion lemma |
| $\boldsymbol{w}_n(t)$ | $\boldsymbol{\Sigma}_n^{-1}\boldsymbol{W}^{-\mathsf{H}}\boldsymbol{e}_n$, then $\boldsymbol{\Sigma}_n$-normalized | [[concepts/iterative-projection|IP]] rule |
| $\boldsymbol{W}_{\mathrm{Z}}(t)$, $\boldsymbol{\Omega}(t)$ | closed-form joint update of all noise rows | IVE trick: no per-column iteration |
| $\boldsymbol{G}_n(t)$ | Kalman-gain recursion on $\boldsymbol{R}_n^{-1}$, $\boldsymbol{G}_n = \boldsymbol{R}_n^{-1}\boldsymbol{P}_n$ | source-wise factorization + matrix inversion lemma |

Three efficiency devices distinguish the journal version from its conference predecessors: (i) recursive $\boldsymbol{\Sigma}_n^{-1}$ via the matrix inversion lemma; (ii) rank-1 updates of $\boldsymbol{W}^{-\mathsf{H}}$ after each single-column $\boldsymbol{w}_n$ update; (iii) a **block-matrix-inversion** formula for $\boldsymbol{W}^{-\mathsf{H}}$ after the multi-column $\boldsymbol{W}_{\mathrm{Z}}$ update, which the rank-1 lemma cannot handle. The shared dereverberation filter $\boldsymbol{G} = \bar{\boldsymbol{G}}\boldsymbol{W}^{-1}$ never needs to be formed: per-source dereverberated signals $\boldsymbol{y}_n(t) = \boldsymbol{x}(t) - \boldsymbol{G}_n^{\mathsf{H}}(t)\bar{\boldsymbol{x}}(t)$ suffice to compute the outputs (**source-wise factorization**).

### Processing flow and forgetting factors

Per frame, all parameters iterate $N_{\mathrm{Iter}}$ times *except* the WPE filters $\boldsymbol{G}_n$, updated only at the first iteration — WPE converges much faster than IVE and costs more per iteration. The two blocks use **different forgetting factors**: $\alpha$ for IVE (small $M \times M$ statistics; $\alpha = 0.99$) and $\beta$ for WPE (large $ML \times ML$ statistics; $\beta = 0.9999$). Experiments in both a car (RT60 ≈ 60 ms) and an office (RT60 ≈ 780 ms) confirm this split is important: shrinking $\beta$ to the IVE-scale value destabilized the optimization, and the $(\alpha, \beta) = (0.99, 0.9999)$ pair gave the best SegSDRs — a refinement of the single-factor trade-off on the [[concepts/online-iva|online IVA]] page.

## Complexity and Special Cases

| Algorithm | Complexity per frame |
|---|---|
| online-IVA | $O(FM^3)$ |
| online-IVE | $O(FNM^2)$ |
| online-WPE×IVA | $O(FM^3L^2)$ |
| online-WPE×IVE / online-WPE×SRIVE | $O(F(N{+}1)M^2L^2)$ |

Dropping the WPE part ($\boldsymbol{G} = \boldsymbol{0}$) yields **online-IVE** — itself newly proposed by the same paper as the first online IVE for *multi-source* extraction — and, with spatial regularization, **online-SRIVE**. Adding the [[concepts/spatial-regularization|spatial regularization]] terms (unit/null/scale) leaves complexity unchanged because the regularized IP/VCD updates cost the same as (23)–(24).

## Low-Latency Results

With an 8 ms STFT frame (4 ms shift) the joint algorithm runs in 2.01 ms/frame (single-core Xeon), for a **10.01 ms total delay** — inside the 12 ms in-car communication budget — while beating cascaded online-WPE+IVE by ~1.3 dB SDRi and ~0.9 dB SIRi at 0 dB SNR in the car, and leading all online baselines in the office environment as well. The same framework instantiated with IVA instead of IVE gives **online-WPE×IVA** (the ICASSP 2021 conference predecessor).

## Related Concepts

- [[concepts/independent-vector-extraction|Independent Vector Extraction]]
- [[concepts/weighted-prediction-error|Weighted Prediction Error (WPE)]]
- [[concepts/convolutional-beamformer|Convolutional Beamformer]]
- [[concepts/online-iva|Online IVA]]
- [[concepts/spatial-regularization|Spatial Regularization]]
- [[concepts/iterative-projection|Iterative Projection]]
- [[concepts/dereverberation|Dereverberation]]

## Related Sources

- [[sources/ueda-2024-online-joint-optimization|Ueda et al. 2024: Blind and Spatially-Regularized Online Joint Optimization of Source Separation, Dereverberation, and Noise Reduction]] — the journal paper introducing online-WPE×IVE, online-IVE, online-SRIVE, and online-WPE×SRIVE
- [[sources/nakatani-2022-switching-iva|Nakatani et al. 2022: Switching IVA and Its Extension to Blind and Spatially Guided Convolutional Beamforming]] — the offline joint-optimization ([[concepts/switching-civa|swCIVA]]) relative: same CBF machinery, switching states instead of online recursion
