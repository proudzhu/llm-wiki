---
type: concept
created: 2026-09-06
updated: 2026-09-06
sources:
  - raw/papers/wang-2021-magnitude-phase-compensation/full-text.md
tags:
  - speech-separation
  - speech-enhancement
  - time-frequency-masking
  - training-target
  - phase-estimation
---

# Phase-Sensitive Mask (PSM)

The **phase-sensitive mask** is a real-valued T-F mask training target for magnitude-domain speech enhancement/separation, proposed by Erdogan et al. (ICASSP 2015). Unlike the ideal amplitude mask (IAM, $|S|/|Y|$), the PSM explicitly accounts for the phase difference between the target and the mixture when the mixture phase $\angle Y$ is used for signal re-synthesis:

$$\text{PSM}(t,f) = \frac{|S(t,f)|}{|Y(t,f)|}\cos(\angle S(t,f) - \angle Y(t,f))$$

The masked mixture spectrum $\text{PSM}\cdot Y$ is then the **closest approximation of the clean spectrum $S(t,f)$ along the direction of the mixture phase $\angle Y(t,f)$** — i.e., the *compensated* magnitude. When $|\angle S - \angle Y| > \pi/2$, the cosine is negative and the mask becomes negative, which is typically truncated to zero.

## Relation to the Magnitude-Phase Compensation Effect

[[sources/wang-2021-magnitude-phase-compensation|Wang, Wichern & Le Roux 2021]] use the PSM as the motivation for the [[concepts/magnitude-phase-compensation-effect|magnitude-phase compensation effect]]: the PSM *explicitly* computes the magnitude that compensates for the (known-inaccurate) mixture phase, maximizing SNR of the target estimate when re-synthesizing with $\angle Y$. Their key insight is that the same compensation **implicitly arises** in end-to-end complex-/time-domain losses — the network learns a compensated magnitude whenever its phase estimate is inaccurate — which explains why adding an explicit magnitude loss improves magnitude accuracy and perceptual metrics.

## Oracle-Mask Behavior (Wang 2021, WHAMR!/SMS-WSJ)

| Oracle mask | SI-SDR | mSNR / WER |
|-------------|--------|------------|
| PSM | Better (masked spectrum closer to clean) | Worse |
| IAM | Worse (aggressive step $|S|$ along $\angle Y$) | Better (oracle magnitude survives re-synthesis) |

The DNN-estimated analog is **phase-sensitive spectrogram approximation (PSA)**, which trains a network on input $|Y|$ to predict $|S|\,\text{clip}_{0}^{1}(\cos(\angle S-\angle Y))$; PSA yields better SI-SDR than plain magnitude spectrogram approximation (MSA) but worse scores on all magnitude-favoring metrics.

## Related Concepts

- [[concepts/magnitude-phase-compensation-effect|Magnitude-Phase Compensation Effect]]
- [[concepts/ideal-ratio-mask|Ideal Ratio Mask (IRM)]]
- [[concepts/ideal-binary-mask|Ideal Binary Mask (IBM)]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask (cRM)]]
- [[concepts/tf-mask-estimation|TF Mask Estimation]]

## Related Sources

- [[sources/wang-2021-magnitude-phase-compensation|Wang, Wichern & Le Roux 2021: On the Compensation Between Magnitude and Phase in Speech Separation]] — PSM as the explicit-encoding motivation for the compensation view; oracle PSM-vs-IAM analysis
- [[sources/wang-2018-supervised-speech-separation-deep-learning-overview|Wang & Chen 2018: Supervised Speech Separation Based on Deep Learning: An Overview]] — surveys PSM among masking-based training targets
