---
type: concept
created: 2026-05-13
updated: 2026-10-07
sources:
  - wiki/sources/liebich-2022-occlusion-effect-cancellation.md
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
- **OEC design target**: In [[concepts/occlusion-effect-cancellation|occlusion effect cancellation]], $S(z)$ should approximate the *inverse occlusion function*, attenuating 50–700 Hz where the occlusion effect amplifies body-conducted sound, while accepting the waterbed amplification at 1.5–4 kHz (compensated in the hear-through filter design). An adaptive factor $\alpha$ scales the effective loop gain: $S_\alpha = \frac{1}{1 + G\alpha K}$ (Liebich & Vary 2022).

## Related Concepts

- [[concepts/feedback-anc|Feedback ANC]]
- [[concepts/waterbed-effect|Waterbed Effect]]
- [[concepts/robust-control|Robust Control]]
- [[concepts/occlusion-effect-cancellation|Occlusion Effect Cancellation]]

## Related Sources

- [[sources/seo-2016-feedback-anc-constrained-optimization|Seo et al. 2016: Feedback ANC via Constrained Optimization]]
- [[sources/liebich-2022-occlusion-effect-cancellation|Liebich & Vary 2022: Occlusion Effect Cancellation in Headphones and Hearing Devices]]
