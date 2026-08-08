---
type: concept
created: 2026-08-08
updated: 2026-08-08
sources:
  - raw/papers/wung-2011-residual-echo-suppression-system/full-text.md
tags:
  - acoustic-echo-cancellation
  - robust-aec
  - error-recovery-nonlinearity
  - double-talk
---

# Error Recovery Nonlinearity (ERN)

Error recovery nonlinearity (ERN) is the nonlinear stage of the robust AEC of Wada & Juang (Proc. IEEE WASPAA 2009) that reduces the disturbance remaining in the AEC estimation error so the linear adaptive filter can keep tracking the room impulse response during double talk **without** a double-talk detector (DTD) or voice activity detector. It is the component that makes the system-level residual echo estimate of [[sources/wung-2011-residual-echo-suppression-system|Wung et al. 2011]] tractable, because it guarantees $\lambda_B \ll \lambda_V$ after convergence.

## Key Formulations

The single-channel AEC error is $e[n] = v[n] + b[n]$, where $v$ is the near-end signal and $b$ the true (noise-free) residual echo. In a conventional AEC, strong $v$ during double talk corrupts $e$ and can drive the adaptive filter to diverge; a DTD would normally freeze adaptation to prevent this, at the cost of losing tracking. The ERN instead applies a nonlinearity to $e$ to attenuate the near-end disturbance *before* it reaches the update, so the filter can continue adapting. Combined with **batch adaptation** (data reuse), this recovers the convergence speed lost to the aggressive step-size control that the nonlinearity imposes.

The practical consequence for downstream [[concepts/residual-echo-suppression|residual echo suppression]] is that after convergence the residual echo power $\lambda_B$ is small relative to $\lambda_V$ (double talk) or $\lambda_D$ (single talk), which is the assumption underpinning the LSA-based residual echo estimate $\hat{b} = \tilde{d} - \hat{d}$.

## Related Concepts

- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]] — ERN is the nonlinear component of the robust AEC variant.
- [[concepts/residual-echo-suppression|Residual Echo Suppression]] — the small $\lambda_B$ guaranteed by ERN is what makes the system-approach residual echo estimate valid.

## Related Sources

- [[sources/wung-2011-residual-echo-suppression-system|Wung et al. 2011]] — uses the robust AEC with ERN and batch adaptation as the front-end for the proposed RES.
