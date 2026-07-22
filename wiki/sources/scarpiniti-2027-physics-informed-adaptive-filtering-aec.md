---
type: source
created: 2026-07-22
updated: 2026-07-22
sources:
  - raw/papers/scarpiniti-2027-physics-informed-adaptive-filtering-aec/full-text.md
  - https://doi.org/10.1016/j.sigpro.2026.110819
  - zotero://select/items/0_6PXZWENL
tags:
  - acoustic-echo-cancellation
  - adaptive-filtering
  - physics-informed
  - room-impulse-response
  - nllms
---

# Scarpiniti, Comminiello & Uncini 2027: Physics-informed adaptive filtering for acoustic echo cancellation

**Authors**: [[entities/michele-scarpiniti|Michele Scarpiniti]], [[entities/danilo-comminiello|Danilo Comminiello]], [[entities/aurelio-uncini|Aurelio Uncini]]
**Affiliation**: Department of Information Engineering, Electronics and Telecommunications (DIET), Sapienza University of Rome, Italy
**Venue**: Signal Processing, 2027
**Type**: Journal article
**DOI**: [10.1016/j.sigpro.2026.110819](https://doi.org/10.1016/j.sigpro.2026.110819)

## Summary

This paper introduces a Physics-Informed Adaptive Filtering (PIAF) framework for [[concepts/acoustic-echo-cancellation|acoustic echo cancellation (AEC)]]. Unlike conventional adaptive algorithms that rely solely on data-driven error minimization, the proposed Physics-Informed NLMS (PI-NLMS) algorithm incorporates physically motivated priors derived from acoustic wave propagation and room impulse response (RIR) structure. The echo path estimation problem is formulated as a composite stochastic optimization task where the instantaneous squared error is regularized by constraints encoding causality, exponential energy decay, time-weighted sparsity of early reflections, spectral smoothness, and slow temporal variation. Theoretical convergence analysis establishes mean convergence conditions and characterizes the bias-variance trade-off introduced by structured regularization. Simulation results demonstrate faster convergence, improved steady-state misalignment, and enhanced ERLE compared to conventional NLMS and proportionate NLMS baselines.

## Problem Formulation

The acoustic echo cancellation problem is modeled as an adaptive system identification task. The microphone signal is given by:

$$
d(n) = \sum_{k=0}^{L-1} h_k x(n-k) + s(n) + v(n) \equiv \mathbf{h}_0^\top \mathbf{x}_n + s(n) + v(n),
$$

where $\mathbf{h}_0$ is the true RIR vector, $\mathbf{x}_n$ is the far-end signal vector, $s(n)$ is near-end speech, and $v(n)$ is background noise.

![[raw/papers/scarpiniti-2027-physics-informed-adaptive-filtering-aec/figures/dcb90ee88649a68d8a4a4102c55ef839fa9be0e870880e57a55dfdbad16004e8.jpg|Basic AEC framework]]
*Figure 1: Basic framework of the acoustic echo cancellation (AEC) problem.*

Conventional NLMS minimizes only the instantaneous squared error $J_\text{NLMS}(n) = \frac{1}{2} e^2(n)$, with the update:

$$
\mathbf{w}_{n+1} = \mathbf{w}_n + \frac{\mu}{\|\mathbf{x}_n\|^2 + \epsilon} e(n) \mathbf{x}_n.
$$

## Methodology

### Physics-Informed Composite Cost

The proposed PI-NLMS algorithm minimizes a composite cost integrating data-driven error minimization with physically motivated priors:

$$
J(n) = \frac{1}{2} e^2(n) + \sum_{i=1}^{M} \Phi_i(\mathbf{w}_n),
$$

where $\Phi_i(\mathbf{w}_n)$ are regularization terms encoding physical knowledge about RIR structure.

### Physical Priors

The framework incorporates five physically motivated priors:

1. **Causality** (hard constraint): The RIR is strictly causal due to finite sound propagation speed. Coefficients before the minimum delay $\tau_\text{min}$ are projected to zero:

   $$
   \mathcal{C} = \{\mathbf{w}: w_k = 0 \text{ for } k < \tau_\text{min}\}.
   $$

2. **Exponential energy decay** (soft prior): Following Sabine's reverberation theory, acoustic energy decays exponentially. The penalty weights coefficients by $e^{\alpha k}$ where $\alpha$ is derived from reverberation time $T_{60}$:

   $$
   \mathcal{P}_\text{decay}(\mathbf{w}) = \frac{1}{2} \sum_{k=0}^{L-1} e^{\alpha k} w_k^2, \quad \alpha \approx \frac{6.91}{T_{60}} T_s.
   $$

3. **Time-weighted sparsity** (soft prior): Early reflections are sparse while late reverberation is diffuse. An $\ell_1$-like penalty with exponential weighting $\beta_k = e^{-\eta k}$ promotes early sparsity:

   $$
   \mathcal{P}_{\ell_1}(\mathbf{w}) = \|\boldsymbol{\beta} \odot \mathbf{w}\|_1.
   $$

4. **Temporal smoothness** (soft prior): The RIR varies smoothly at the sampling scale, penalized via a discrete Laplacian operator:

   $$
   \mathcal{P}_\text{ts}(\mathbf{w}) = \frac{1}{2} \sum_{k=1}^{L-1} (w_k - w_{k-1})^2.
   $$

5. **Spectral smoothness** (soft prior): The acoustic transfer function is inherently band-limited. Penalty applied in the frequency domain via the Fourier matrix $\mathbf{F}$:

   $$
   \mathcal{P}_\text{ss}(\mathbf{w}) = \frac{1}{2} \sum_{k=1}^{L-1} (W_k - W_{k-1})^2, \quad \mathbf{W} = \mathbf{F}\mathbf{w}.
   $$

6. **Slow temporal variation** (soft prior): The acoustic path changes slowly relative to the sampling rate:

   $$
   \mathcal{P}_\text{slow}(\mathbf{w}_n) = \frac{1}{2} \|\mathbf{w}_n - \mathbf{w}_{n-1}\|^2.
   $$

![[raw/papers/scarpiniti-2027-physics-informed-adaptive-filtering-aec/figures/8d1514b1441694127d716e7c6899b5baa72232c10711da220c41ce981e25512e.jpg|Typical RIR structure]]
*Figure 2: Magnitude of a typical room impulse response (RIR), showing direct path, sparse early reflections, and decaying late reverberation tail.*

### PI-NLMS Update

The gradient of the composite cost combines the NLMS gradient with physics-informed regularization:

$$
\mathbf{g}_\text{phys}(n) = \boldsymbol{\Lambda} \mathbf{w}_n - \mathbf{b},
$$

where $\boldsymbol{\Lambda} = \boldsymbol{\Lambda}_\text{decay} + \boldsymbol{\Lambda}_{\ell_1} + \boldsymbol{\Lambda}_\text{ts} + \boldsymbol{\Lambda}_\text{ss} + \boldsymbol{\Lambda}_t$ aggregates all prior matrices.

The PI-NLMS update is:

$$
\mathbf{w}_{n+1} = \mathbf{w}_n + \mu_n e(n) \mathbf{x}_n - \mu_n \mathbf{g}_\text{phys}(n),
$$

followed by the causality projection: $w_k(n+1) = 0,\ \forall k < \tau_\text{min}$.

### Computational Complexity

| Term | Multiplications | Additions |
|------|----------------|-----------|
| NLMS | $3L$ | $3L$ |
| All priors (w/o spectral smoothness) | $4L$ | $3L$ |
| Total w/o spectral smoothness | $7L$ | $6L$ |
| Total w/ spectral smoothness | $7L + \frac{L}{2}\log_2 L$ | $6L + L\log_2 L$ |

The algorithm maintains $\mathcal{O}(L)$ complexity without the spectral smoothness prior, preserving real-time feasibility.

## Theoretical Analysis

### Mean Convergence

The weight error vector $\widetilde{\mathbf{w}}_n = \mathbf{h}_0 - \mathbf{w}_n$ evolves as:

$$
\mathbb{E}[\widetilde{\mathbf{w}}_{n+1}] = (\mathbf{I} - \mu_n \mathbf{R}_x - \mu_n \boldsymbol{\Lambda}) \mathbb{E}[\widetilde{\mathbf{w}}_n] + \mu_n \mathbf{c},
$$

with stability condition $0 < \mu_n < \frac{2}{\lambda_\max[\mathbf{R}_x + \boldsymbol{\Lambda}]}$. The regularization increases eigenvalues of the effective correlation matrix, improving conditioning.

### Steady-State MSD

Under white input and diagonal $\boldsymbol{\Lambda}$:

$$
\text{MSD} = \frac{\mu_n L \sigma_v^2 \sigma_x^2}{2(\sigma_x^2 + \lambda)},
$$

showing MSD reduction by factor $\sigma_x^2/(\sigma_x^2 + \lambda)$ compared to NLMS. The bias-variance trade-off is characterized as:

$$
\text{MSD} = \underbrace{\text{Tr}(\mathbf{Z}_\infty)}_{\text{variance}} + \underbrace{\|\widetilde{\mathbf{w}}_\infty\|^2}_{\text{bias}^2}.
$$

### Steady-State ERLE

$$
\text{ERLE} = \frac{\mathbf{h}_0^\top \mathbf{R}_x \mathbf{h}_0}{\text{EMSE} + \sigma_v^2}.
$$

PI-NLMS mainly improves low-energy modes (improving MSD), while ERLE improvements are more modest — particularly under white excitation. Under speech excitation, the conditioning improvement yields substantial ERLE gains.

## Experimental Setup

**Datasets**:
- Open AIR dataset: St. George's Episcopal Church RIR (96 kHz → resampled to 8 kHz, truncated to $L=1024$)
- Synthetic RIR generated via MATLAB's `acousticRoomResponse` (8 kHz, $L=1024$)
- Both RIRs normalized to $\|\mathbf{h}_0\|^2 = 1$

**Input signals**:
- White Gaussian noise (zero mean, unit variance, 20,000 samples)
- Female speech signal (resampled to 8 kHz, 22,400 samples)

**Noise**: Additive white Gaussian noise, SNR range [-10, 30] dB in 5 dB steps

**Hyperparameters**: $\mu = 0.5$, $\epsilon = 10^{-6}$, $\alpha = 0.01$ (synthetic) / 0.005 (Church), $\tau_\text{min} = 10$ (synthetic) / 140 (Church)

**Baselines**: NLMS ($\mu=0.5$), PNLMS ($\mu=0.4$), APA ($K=4$, $\mu=0.2$), RLS ($\lambda=0.999$)

## Results

### White Noise Excitation

PI-NLMS consistently outperforms NLMS and PNLMS across all SNR levels, with MSD gains of approximately 2–3 dB for synthetic RIR and ~1.6 dB for Church RIR at 20 dB SNR. ERLE gains remain modest under white excitation, as PI-NLMS primarily improves weakly-excited modes.

| SNR | PI-NLMS MSD (Synth) | NLMS MSD (Synth) | PNLMS MSD (Synth) |
|-----|--------------------|-----------------|------------------|
| 20 dB | -27.43 dB | -24.80 dB | -25.45 dB |
| 30 dB | -36.30 dB | -34.70 dB | -32.37 dB |

Excellent agreement between simulated and theoretical MSD/EMSE values validates the analysis.

### Speech Excitation

Under speech (colored) excitation, PI-NLMS shows substantially larger gains. At 20 dB SNR for synthetic RIR:
- MSD: -13.94 dB (vs. -11.89 NLMS, -12.82 PNLMS)
- ERLE: 15.36 dB (vs. 12.33 NLMS, 11.46 PNLMS)

The regularization reduces the effective condition number $\kappa' = \gamma_\max/\gamma_\min$, improving both MSD and ERLE — unlike the white input case. Saturation (bias-limited regime) is observed at high SNR under speech excitation.

### Comparison with APA and RLS

Despite being a first-order stochastic gradient algorithm, PI-NLMS achieves the lowest steady-state MSD, outperforming APA and RLS by ~1.7 dB at 20 dB SNR (synthetic RIR), while maintaining substantially lower computational complexity.

### Double-Talk and Tracking Performance

- **Double-talk**: With a correlation-based DTD, PI-NLMS maintains stable operation with only 2–3 dB ERLE degradation. Faster recovery after double-talk periods than NLMS.
- **Tracking**: After abrupt RIR change, PI-NLMS achieves MSD below -20 dB within ~5,000 samples vs. ~7,000 for NLMS and PNLMS, with 2–3 dB lower steady-state MSD.

## Key Contributions

1. **PIAF framework**: Formulates acoustic echo path identification as a physics-informed stochastic optimization problem integrating multiple physically motivated structural constraints within a unified adaptive filtering framework.

2. **PI-NLMS algorithm**: Derives the Physics-Informed NLMS algorithm combining gradient-based regularization with projection-based constraints, preserving NLMS-level computational complexity.

3. **Convergence analysis**: Provides mean and mean-square convergence analysis characterizing the bias-variance trade-off induced by structured physical priors, with closed-form MSD and EMSE expressions.

4. **Empirical validation**: Demonstrates through extensive simulations that PI-NLMS achieves faster convergence, 2–3 dB better steady-state MSD, and enhanced ERLE compared to NLMS, PNLMS, APA, and RLS — particularly under challenging colored (speech) excitation.

## Related Concepts

- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation (AEC)]]
- [[concepts/pi-nlms|Physics-Informed NLMS (PI-NLMS)]]
- [[concepts/physics-informed-neural-network|Physics-Informed Neural Network]]
- [[concepts/kalman-filter|Kalman Filter]]
- [[concepts/frequency-domain-kalman-filter|Frequency-Domain Kalman Filter]]
- [[concepts/spline-adaptive-filter|Spline Adaptive Filter]]

## Related Synthesis

- [[synthesis/kalman-filter-theory-and-application|Kalman Filter Theory and Application]]
