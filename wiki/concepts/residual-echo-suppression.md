---
type: concept
created: 2026-08-08
updated: 2026-08-08
sources:
  - raw/papers/wung-2011-residual-echo-suppression-system/full-text.md
tags:
  - acoustic-echo-cancellation
  - residual-echo-suppression
  - speech-enhancement
  - postfiltering
---

# Residual Echo Suppression (RES)

Residual echo suppression (RES) is the stage that follows [[concepts/acoustic-echo-cancellation|acoustic echo cancellation]] (AEC) to attenuate the residual echo left over by imperfect adaptive filtering. Because the adaptive filter $\mathbf{w}$ never matches the room impulse response $\mathbf{h}$ exactly, the AEC error signal $e = v + b$ still contains the *residual echo* $b = (\mathbf{h}^\mathrm{T} - \mathbf{w}^\mathrm{T})\mathbf{x}$, where $v$ is the near-end signal and $\mathbf{x}$ the far-end reference. RES applies a (typically spectral) gain to suppress $b$ while minimally distorting $v$.

## Key Formulations

RES is usually formulated as a Wiener-type or LSA spectral gain $G(k) \in [0,1]$ applied to the AEC error spectrum $E_k$, driven by an estimate of the residual echo variance $\hat{\lambda}_B(k) = \mathcal{E}\{|B_k|^2\}$. The LSA gain of Ephraim & Malah is a common choice:

$$G_{\mathrm{LSA}}(k) = \frac{\xi_k}{1+\xi_k}\exp\!\left(\frac{1}{2}\int_{\nu_k}^{\infty}\frac{e^{-t}}{t}\,\mathrm{d}t\right),\qquad \nu_k \equiv \frac{\xi_k}{1+\xi_k}\gamma_k,$$

with a priori SNR $\xi_k = \lambda_V(k)/\lambda_B(k)$ and a posteriori SNR $\gamma_k = |E_k|^2/\lambda_B(k)$. The a priori SNR is typically estimated by the decision-directed (DD) estimator. The central difficulty is obtaining $\hat{\lambda}_B(k)$: the residual echo is unobservable and corrupted by near-end speech/noise, especially during double talk.

### System Approach (Wung et al. 2011)

[[sources/wung-2011-residual-echo-suppression-system|Wung et al. 2011]] proposes estimating the residual echo as the difference between a *nonlinear* (LSA) echo estimate and the *linear* AEC echo estimate:

$$\hat{b}[n] = \tilde{d}[n] - \hat{d}[n] = f_{\mathrm{LSA}}\{Y, \lambda_V\} - \hat{d}[n].$$

The LSA filter is applied to the microphone signal $Y$ (treating the near-end $v$ as noise) to emphasize the echo $d$ and suppress $v$; because the robust AEC (with [[concepts/error-recovery-nonlinearity|ERN]]) keeps $\lambda_B \ll \lambda_V$ after convergence, the LSA output $\tilde{D}_k \approx D_k$ in all three operating cases (near-end talk, single talk, double talk), so $\hat{b}$ closely tracks the true noise-free residual echo. This exploits the robustness of the *whole* AEC system rather than treating RES as an isolated estimator.

### Traditional Baselines

Conventional RES estimates $\lambda_B$ from the equivalent transfer function (ETF) method and/or the coherence function (CF) method. Frequency-domain Wiener filtering based on these estimates is sensitive to SNR-estimation accuracy and may introduce near-end speech distortion or musical noise.

## Related Concepts

- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]] — the linear front-end whose residual error RES suppresses.
- [[concepts/psychoacoustic-postfilter|Psychoacoustic Postfilter]] — a masking-threshold-driven gain that suppresses residual echo without audible distortion.
- [[concepts/error-recovery-nonlinearity|Error Recovery Nonlinearity (ERN)]] — the nonlinear stage that makes the robust AEC's residual echo small enough for the system approach to hold.

## Related Sources

- [[sources/wung-2011-residual-echo-suppression-system|Wung et al. 2011]] — system approach combining robust AEC, LSA-based residual echo estimation, and a psychoacoustic postfilter.
