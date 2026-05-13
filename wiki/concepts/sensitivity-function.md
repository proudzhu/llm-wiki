---
type: concept
created: 2026-05-13
updated: 2026-05-13
tags:
  - control-theory
  - feedback
  - active-noise-control
---

# Sensitivity Function

The **sensitivity function** $S$ characterizes how disturbances propagate through a feedback control system to the output. In feedback ANC, it represents the closed-loop transfer function from primary noise to residual error:

$$S = \frac{1}{1 + CP}$$

where $C$ is the controller and $P$ is the plant (secondary path).

## Key Properties

- **Noise attenuation**: $|S(j\omega)| < 1$ indicates noise reduction at frequency $\omega$
- **Waterbed effect**: Due to Bode's integral theorem, reducing sensitivity in one frequency band necessarily increases it in another — the area under $\log|S|$ is conserved
- **Robust stability**: The complementary sensitivity $T = 1 - S = \frac{CP}{1+CP}$ must satisfy $|T\Delta| < 1$ for robustness against plant uncertainty $\Delta$

## Applications in ANC

- **Design objective**: Minimize $|S|$ in the control band (typically < 1kHz for ANC)
- **Constraint**: Limit maximum $|S|$ (e.g., 3dB) to control noise boosting outside the control band

## Related Concepts

- [[../concepts/feedback-anc|Feedback ANC]]
- [[../concepts/waterbed-effect|Waterbed Effect]]
- [[../concepts/robust-control|Robust Control]]

## Related Sources

- [[../sources/seo-2016-feedback-anc-constrained-optimization|Seo et al. 2016: Feedback ANC via Constrained Optimization]]
