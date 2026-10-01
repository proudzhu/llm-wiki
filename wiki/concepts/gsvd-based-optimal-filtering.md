---
type: concept
created: 2026-10-01
updated: 2026-10-01
sources:
  - raw/papers/doclo-2002-gsvd-optimal-filtering/full-text.md
tags:
  - speech-enhancement
  - multi-channel
  - signal-subspace
  - gsvd
  - wiener-filter
  - time-domain
  - robustness
---

# GSVD-Based Optimal Filtering

**GSVD-based optimal filtering** is a multimicrophone speech enhancement technique, introduced by [[sources/doclo-2002-gsvd-optimal-filtering|Doclo & Moonen 2002]], that extends single-microphone [[concepts/signal-subspace-speech-enhancement|signal subspace speech enhancement]] to the spatio-temporal domain: the optimal filter for estimating the received speech component is computed from the **generalized singular value decomposition (GSVD)** of a speech data matrix and a noise data matrix, jointly exploiting frequency *and* spatial characteristics of speech and noise. It is the time-domain instantiation of the [[concepts/multi-channel-wiener-filter|multi-channel Wiener filter]] on stacked data vectors.

## Derivation

### Step 1: Signal model and stacked vectors

Each of the $N$ microphone signals consists of a filtered version of the clean speech plus additive (possibly colored) noise, uncorrelated with the speech:

$$y_n[k] = h_n[k] \otimes s[k] + v_n[k] = x_n[k] + v_n[k], \quad n = 0, \ldots, N-1$$

With per-channel filters of length $L$, define the $L$-dimensional data vector, the $M = LN$-dimensional stacked filter and stacked data vector

$$\mathbf{y}_n[k] = [y_n[k] \;\; y_n[k-1] \;\; \ldots \;\; y_n[k-L+1]]^T, \qquad \mathbf{y}[k] = [\mathbf{y}_0^T[k] \;\; \ldots \;\; \mathbf{y}_{N-1}^T[k]]^T$$

so that the output is $z[k] = \mathbf{w}^T[k]\,\mathbf{y}[k]$. The estimation target is **one of the received speech components** $x_n[k]$ — not $s[k]$ itself — so, unlike a [[concepts/gsc-beamformer|GSC]], no unity-gain constraint toward the source direction is imposed.

### Step 2: Multidimensional Wiener filter

Filter the whole stacked vector with an $M \times M$ matrix: $\mathbf{z} = \mathbf{W}^T\mathbf{y}$, desired response $\mathbf{d}$, error $\mathbf{e} = \mathbf{d} - \mathbf{z}$. Minimizing the MSE cost

$$\mathbf{J}_{\mathrm{MSE}}(\mathbf{W}) = E\{\|\mathbf{e}\|_2^2\} = E\{\mathbf{d}^T\mathbf{d}\} - 2E\{\mathbf{y}^T\mathbf{W}\mathbf{d}\} + E\{\mathbf{y}^T\mathbf{W}\mathbf{W}^T\mathbf{y}\}$$

over $\mathbf{W}$ (setting $\partial \mathbf{J}_{\mathrm{MSE}}/\partial\mathbf{W} = 0$) yields the multidimensional Wiener filter

$$\mathbf{W}_{WF} = \mathbf{R}_{yy}^{-1}\,\mathbf{R}_{yd}$$

where $\mathbf{R}_{yy} = E\{\mathbf{y}\mathbf{y}^T\}$ and $\mathbf{R}_{yd} = E\{\mathbf{y}\mathbf{d}^T\}$ are $M \times M$ spatio-temporal (cross-)correlation matrices.

### Step 3: Eliminating the unobservable desired response

Here $\mathbf{d}[k] = \mathbf{x}[k]$ — the desired response is **unobservable**, so $\mathbf{R}_{yd}$ cannot be estimated directly. Two assumptions make the filter computable:

1. **Short-term noise stationarity**: $\mathbf{R}_{vv}[k] = \mathbf{R}_{vv}[k']$, where $k'$ lies in noise-only periods detected by [[concepts/voice-activity-detection|VAD]] — the noise correlation matrix is estimated during speech pauses;
2. **Speech–noise independence**: $\mathbf{R}_{xv}[k] = \mathbf{0}$, implying $\mathbf{R}_{yy} = \mathbf{R}_{xx} + \mathbf{R}_{vv}$ and $\mathbf{R}_{yx} = \mathbf{R}_{xx}$.

Substituting $\mathbf{R}_{yd} = \mathbf{R}_{xx} = \mathbf{R}_{yy} - \mathbf{R}_{vv}$ gives the filter in terms of estimable quantities only:

$$\mathbf{W}_{WF} = \mathbf{R}_{yy}^{-1}[k]\left(\mathbf{R}_{yy}[k] - \mathbf{R}_{vv}[k]\right)$$

### Step 4: Joint diagonalization

Assume $\mathbf{R}_{yy}$ and $\mathbf{R}_{vv}$ are full-rank and jointly diagonalizable (both symmetric block-Toeplitz):

$$\mathbf{R}_{yy} = \bar{\mathbf{Q}}\,\mathrm{diag}\{\bar{\sigma}_i^2\}\,\bar{\mathbf{Q}}^T, \qquad \mathbf{R}_{vv} = \bar{\mathbf{Q}}\,\mathrm{diag}\{\bar{\eta}_i^2\}\,\bar{\mathbf{Q}}^T$$

where $\bar{\mathbf{Q}}$ is invertible but not necessarily orthogonal. Using $(\bar{\mathbf{Q}}D\bar{\mathbf{Q}}^T)^{-1} = \bar{\mathbf{Q}}^{-T}D^{-1}\bar{\mathbf{Q}}^{-1}$, the filter becomes a **gain applied in the generalized-eigenvector transform domain**:

$$\mathbf{W}_{WF} = \bar{\mathbf{Q}}^{-T}\,\mathrm{diag}\left\{1 - \frac{\bar{\eta}_i^2}{\bar{\sigma}_i^2}\right\}\bar{\mathbf{Q}}^{T}$$

Special case — spatio-temporal white noise ($\mathbf{R}_{vv} = \bar{\eta}^2 I_M$): $\bar{\mathbf{Q}}$ reduces to an orthogonal matrix (a KLT), and $\mathbf{W}_{WF}$ is symmetric.

### Step 5: Low-rank speech model — why the gain is well-behaved

Model each acoustic impulse response as an FIR filter of length $K$; then $\mathbf{x}[k] = \mathcal{H}[k]\,\mathbf{s}[k]$ with $\mathcal{H}[k]$ an $M \times (K+L-1)$ block convolution matrix. If the clean speech admits a rank-$R$ model ($R \le K+L-1$, typically $K \gg M$), then

$$\mathbf{R}_{xx} = \mathcal{H}\,\mathbf{R}_{ss}\,\mathcal{H}^T$$

is rank-$R$, and the GEVD of $(\mathbf{R}_{xx}, \mathbf{R}_{vv})$ partitions into a rank-$R$ signal block and its complement, from which

$$\bar{\sigma}_i^2 > \bar{\eta}_i^2 \;\; (i = 1, \ldots, R), \qquad \bar{\sigma}_i^2 = \bar{\eta}_i^2 \;\; (i = R+1, \ldots, M)$$

Hence the Wiener gain $1 - \bar{\eta}_i^2/\bar{\sigma}_i^2$ has **exactly $R$ positive nonzero elements** (the speech subspace) and zeros elsewhere — it can never be negative, a property the practical algorithm relies on. In white noise, $\bar{\eta}^2$ can be read off the smallest eigenvalues of $\mathbf{R}_{yy}$ itself, so **no VAD is required** in that case.

### Step 6: Error covariance and column selection

The estimation error $\mathbf{e}[k] = \mathbf{W}_{WF}^T\mathbf{y}[k] - \mathbf{x}[k]$ has covariance (using Step 3–4 identities)

$$\mathbf{R}_{ee} = (\mathbf{R}_{yy} - \mathbf{R}_{vv})(I_M - \mathbf{W}_{WF}) = \mathbf{R}_{vv}\,\mathbf{W}_{WF}$$

Diagonal element $\{\mathbf{R}_{ee}\}_{ii}$ measures how well the $i$-th component of $\mathbf{x}[k]$ (a delayed speech sample in a particular microphone) is estimated; the smallest diagonal element identifies the **best column** $\mathbf{w}_{WF}^i$ of $\mathbf{W}_{WF}$. Recomputing $\mathbf{R}_{ee}$ at every time step is expensive; the fixed middle column $i = L/2$ (the linear-phase filter, see Properties) performs near-optimally at a fraction of the cost.

### Step 7: General estimator class and the μ trade-off

The Wiener filter belongs to a broader class

$$\mathbf{W} = \bar{\mathbf{Q}}^{-T}\,\mathrm{diag}\left\{f(\bar{\sigma}_i^2, \bar{\eta}_i^2)\right\}\bar{\mathbf{Q}}^{T}$$

interpretable as an **analysis filterbank** $\bar{\mathbf{Q}}^{-T}$ (signal-dependent transform), a **gain function** $f$, and a **synthesis filterbank** $\bar{\mathbf{Q}}^T$. Decompose the error into signal distortion and residual noise:

$$\mathbf{e}[k] = \underbrace{(\mathbf{W}^T - I_M)\,\mathbf{x}[k]}_{\mathbf{e}_y[k]\ \text{(distortion)}} + \underbrace{\mathbf{W}^T\,\mathbf{v}[k]}_{\mathbf{e}_v[k]\ \text{(residual noise)}}$$

Minimizing the distortion energy $\epsilon_y^2$ subject to a residual-noise bound $\epsilon_v^2 \le T$ (Lagrange multiplier $\mu > 0$, with $T$ an increasing function of $\mu$) yields the **μ-parameterized family**

$$\mathbf{W} = (\mathbf{R}_{xx} + \mu\mathbf{R}_{vv})^{-1}\mathbf{R}_{xx} = (\mathbf{R}_{yy} + (\mu-1)\mathbf{R}_{vv})^{-1}(\mathbf{R}_{yy} - \mathbf{R}_{vv}) = \bar{\mathbf{Q}}^{-T}\,\mathrm{diag}\left\{\frac{\bar{\sigma}_i^2 - \bar{\eta}_i^2}{\bar{\sigma}_i^2 + (\mu-1)\bar{\eta}_i^2}\right\}\bar{\mathbf{Q}}^T$$

- $\mu = 1$: MSE/Wiener estimate (used throughout the paper's experiments)
- $\mu > 1$: more noise reduction, more distortion
- $\mu < 1$: less distortion, less noise reduction; $\mu = 0$ gives $\mathbf{W} = I_M$ (no filtering)

This is the time-domain ancestor of the [[concepts/speech-distortion-constrained-noise-reduction|speech-distortion-constrained]] parameterization later formalized in the STFT domain.

### Step 8: Practical computation via GSVD of data matrices

In practice $\bar{\mathbf{Q}}$, $\bar{\sigma}_i^2$, $\bar{\eta}_i^2$ are estimated from **data matrices** rather than correlation matrices: a $p \times M$ speech data matrix $\mathbf{Y}[k]$ (rows = stacked vectors from speech-and-noise periods) and a $q \times M$ noise data matrix $\mathbf{V}[k']$ (noise-only periods; time indices need not be consecutive). Their GSVD is

$$\mathbf{Y}[k] = \mathbf{U}_Y\,\boldsymbol{\Sigma}_Y\,\mathbf{Q}^T, \qquad \mathbf{V}[k'] = \mathbf{U}_V\,\boldsymbol{\Sigma}_V\,\mathbf{Q}^T$$

with $\boldsymbol{\Sigma}_Y = \mathrm{diag}\{\sigma_i\}$, $\boldsymbol{\Sigma}_V = \mathrm{diag}\{\eta_i\}$, and the shared (invertible, non-orthogonal) generalized singular-vector matrix $\mathbf{Q}$; $\sigma_i/\eta_i$ are the generalized singular values. Since the empirical correlations approximate $\mathbf{R}_{yy} \simeq \mathbf{Y}^T\mathbf{Y}/p$ and $\mathbf{R}_{vv} \simeq \mathbf{V}^T\mathbf{V}/q$, substituting into Step 3 gives

$$\mathbf{W}_{WF} \simeq \mathbf{Q}^{-T}\,\mathrm{diag}\left\{1 - \frac{p}{q}\frac{\eta_i^2}{\sigma_i^2}\right\}\mathbf{Q}^{T}$$

The $p/q$ factor compensates for the unequal numbers of speech and noise snapshots. Finite-sample estimation can violate the Step 5 ordering ($\sigma_i^2 \le \eta_i^2$ by noise), producing negative gains — these are zero-estimates and are **clamped to zero**.

### Step 9: Output and estimate selection

The enhanced $p \times M$ speech data matrix is $\hat{\mathbf{X}}[k] = \mathbf{Y}[k]\,\mathbf{W}_{WF}$, which contains multiple estimates of each speech sample (all columns of $\mathbf{W}_{WF}$ applied at all time lags). The output is taken as one column filtered through the data matrix,

$$[\hat{x}_j[k-\Delta-p+1] \;\cdots\; \hat{x}_j[k-\Delta]]^T = \mathbf{Y}[k]\,\mathbf{w}_{WF}^i, \qquad j = \mathrm{div}(i-1, L), \;\; \Delta = \mathrm{rem}(i-1, L)$$

with the column index $i$ chosen per Step 6 (or fixed at $i = L/2$). Single-microphone procedures differ only in this last step: some average over all available estimates (shown in Section IV of the paper to be suboptimal), block-based procedures use overlap-add on the last row, and adaptive procedures retain only the first element (implicitly $i = 1$).

## Properties

- **Symmetry / linear phase**: the single-channel correlation matrices are symmetric Toeplitz (centrosymmetric), so $\mathbf{W} = J\mathbf{W}J$ ($J$ = reverse identity) for white and colored noise and any gain function; the middle column ($i = L/2$) is a linear-phase filter and is the recommended practical choice (near-optimal error variance without recomputing the error covariance matrix per time step). In the multichannel case, block symmetry $\mathbf{W} = S\mathbf{W}S$ holds under symmetric array conditions.
- **Averaging is suboptimal**: the diagonal-averaging step of some single-microphone subspace algorithms is unnecessary and even suboptimal — an individual $L$-dimensional column filter always attains lower error variance than the $(2L-1)$-dimensional averaged filter.
- **Beamforming behavior without steering**: for localized sources without multipath, the filter autonomously forms a directivity pattern with maximum gain toward the speech direction and nulls toward noise directions — no source-position estimate or array calibration required. Unlike a GSC, the speech-direction gain is not constrained to unity.
- **Robustness**: no a priori assumptions about source position or array geometry; provably insensitive to microphone amplification/phase variations, and more robust than the [[concepts/gsc-beamformer|GSC]] to microphone displacement and source-position errors.
- **Reverberation**: performance degrades gracefully with reverberation time (unlike the GSC, which relies on correlated noise across microphones); noise reduction mainly exploits the *spatial* characteristics of the noise, so it is insensitive to temporal nonstationarity of the noise source.
- **VAD sensitivity**: misclassifying speech as noise causes signal cancellation (analogous to GSC signal leakage); the reverse misclassification only reduces noise reduction.

## Computational Cost

A full GSVD costs $17M^3 + 3pM^2$ operations; recursive Jacobi-type GSVD updating reduces the per-update cost to $27.5M^2$ including the $4M^2$ filter-column computation ($21.5M^2$ square-root-free), and subsampling (updating every $r$ samples) divides the cost by $r$ — 684 Gflops down to 55 Mflops for $N = 4$, $L = 20$, $p = 4000$, $f_s = 8$ kHz, enabling real-time operation on a Pentium-III 450 MHz. A multi-channel subband variant (Spriet, Moonen & Wouters 2002) improves performance at further reduced complexity.

## Descendants

The joint-diagonalization idea survives in the STFT domain as [[concepts/gevd-spatial-filtering|GEVD-based spatial filtering]], where the generalized eigendecomposition of speech/noise spatial covariance matrices yields rank-constrained SDW-MWF filters (e.g., in the [[concepts/tango-framework|Tango]] family of distributed binaural enhancement frameworks). The GSVD-of-data-matrices and GEVD-of-SCMs formulations are the time-domain and frequency-domain expressions of the same principle.

## Related Concepts

- [[concepts/signal-subspace-speech-enhancement|Signal Subspace Speech Enhancement]] — the single-microphone family this technique extends
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]] — the underlying optimal-filter structure
- [[concepts/gevd-spatial-filtering|GEVD-Based Spatial Filtering]] — the frequency-domain/SCM descendant
- [[concepts/gsc-beamformer|Generalized Sidelobe Canceller (GSC)]] — the adaptive-beamforming alternative it outperforms
- [[concepts/singular-value-decomposition|Singular Value Decomposition]] — GSVD generalizes SVD to a matrix pair
- [[concepts/voice-activity-detection|Voice Activity Detection]] — separates speech and noise data matrices
- [[concepts/beamforming|Beamforming]] — the spatial interpretation

## Related Sources

- [[sources/doclo-2002-gsvd-optimal-filtering|Doclo & Moonen 2002: GSVD-Based Optimal Filtering for Single and Multimicrophone Speech Enhancement]] — origin paper: formulation, symmetry properties, averaging suboptimality, GSC comparison, robustness, complexity
