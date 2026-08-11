---
type: concept
created: 2026-08-11
updated: 2026-08-11
sources:
  - raw/papers/fang-2020-robust-residual-echo-suppression/full-text.md
tags:
  - residual-echo-suppression
  - power-spectral-density
  - statistical-correlation
  - signal-processing
---

# Statistical Normalized Correlation (for Residual Echo PSD)

Statistical normalized correlation, as introduced by [[entities/bingxiao-fang|Fang (2020)]], is a residual echo power spectral density (PSD) estimator that uses the *normalized cross-correlation* between the AEC error signal and the echo replica — both mean-removed — to track the residual echo power without requiring a voice activity detector (VAD), double-talk detector (DTD), or [[concepts/minimum-statistics|minimum statistics]].

## Key Formulations

Let $\hat{D}(i,k)$ be the echo replica (output of the linear AEC filter) and $E(i,k)$ the AEC error signal in the STFT domain. After mean removal,

$$\tilde{D}(i,k) = \hat{D}(i,k) - \mathcal{E}\{\hat{D}(i,k)\}, \qquad \tilde{E}(i,k) = E(i,k) - \mathcal{E}\{E(i,k)\},$$

the smoothed cross- and auto-PSDs are computed recursively with smoothing factor $\alpha$:

$$r^{de}(i,k) = \alpha\, r^{de}(i{-}1,k) + (1{-}\alpha)\,|\tilde{D}^{*}(i,k)\,\tilde{E}(i,k)|,$$

$$r^{dd}(i,k) = \alpha\, r^{dd}(i{-}1,k) + (1{-}\alpha)\,|\tilde{D}^{*}(i,k)\,\tilde{D}(i,k)|.$$

The residual echo PSD estimate is the normalized cross-spectrum:

$$\hat{\lambda}_R(i,k) = \frac{r^{de}(i,k)\cdot r^{de}(i,k)}{r^{dd}(i,k)}.$$

### Justification

The estimator exploits the fact that the residual echo $R = (H-W)X$ and the echo replica $\hat{D} = WX$ share the same excitation $X$:

- **Single talk** ($s=0$, so $e=r$): the estimate reduces to $|R(i,k)|^2 \cos\theta$, where $\cos\theta$ is the coherence between $\tilde{D}$ and $R$. Since $R$ and $\hat{D}$ share the same excitation, $\cos\theta \approx 1$, giving $\hat{\lambda}_R \approx |R|^2$.
- **Double talk** ($s\neq 0$): near-end speech $S$ is assumed statistically uncorrelated with $\hat{D}$ over the smoothing window, so the cross-term $\tilde{D}^{*}S$ averages out and the estimator continues to track $|R|^2\cos\theta$ rather than $|S+R|^2$.

The **mean removal** (subtracting $\mathcal{E}\{\cdot\}$) is critical: it removes the DC / long-term average component so that only the fluctuating, excitation-driven part of $\hat{D}$ and $E$ contributes to the cross-correlation, sharpening the coherence with the residual echo.

### Role in the RES Pipeline

The PSD estimate drives an Ephraim-Malah-style spectral gain via priori/posteriori signal-to-echo ratios (SER) and a decision-directed recursion, producing a Wiener-type gain $G(i,k) = \max\!\big(\xi^{\mathrm{priori}}/(\xi^{\mathrm{priori}}+1),\, G_{\min}\big)$ applied to $E(i,k)$.

## Distinction from Baselines

| Method | Needs VAD/DTD? | Needs min-statistics? | Tracking speed |
|--------|----------------|----------------------|----------------|
| Slow-attach-fast-decay [Hoshuyama 2006] | No | Effectively yes | Slow attach, fast decay |
| [[concepts/psychoacoustic-postfilter\|Psychoacoustic postfilter]] (Wung 2011) | Yes (NT/ST/DTD) | No | Depends on VAD |
| Minimum statistics (Martin 1994) | No | Yes | Limited by min-tracking |
| **Statistical normalized correlation** (Fang 2020) | **No** | **No** | Set by smoothing $\alpha$ |

## Related Concepts

- [[concepts/residual-echo-suppression|Residual Echo Suppression]] — the problem this estimator solves.
- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]] — the front-end producing $\hat{D}$ and $E$.
- [[concepts/minimum-statistics|Minimum Statistics]] — a baseline PSD estimator this method replaces.

## Related Sources

- [[sources/fang-2020-robust-residual-echo-suppression|Fang 2020]] — introduces the estimator and validates it on real recordings.
