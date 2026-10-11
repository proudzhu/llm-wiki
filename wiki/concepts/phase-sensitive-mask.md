---
type: concept
created: 2026-09-06
updated: 2026-10-11
sources:
  - raw/papers/wang-2021-magnitude-phase-compensation/full-text.md
  - raw/papers/erdogan-2016-improved-mvdr-mask-prediction/full-text.md
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

## From MSA to PSM in the Mask-Prediction Line

The mask-prediction network of [[sources/erdogan-2016-improved-mvdr-mask-prediction|Erdogan et al. 2016]] (the founding mask-based beamforming paper, by the same group) is trained with the **magnitude spectrum approximation (MSA)** loss, $D_{\mathrm{msa}}(\hat{a}) = (\hat{a}|\hat{y}| - |s|)^2$ — the direct predecessor objective in the same single-channel enhancement line (Weninger et al. 2014 → Erdogan et al. 2015). The PSM/PSA objectives of Erdogan et al. 2015 extend MSA by accounting for the phase difference between target and mixture, yielding better SI-SDR at the cost of magnitude-favoring metrics (see the oracle-mask table above). In the 2016 beamforming paper, the MSA-trained mask is repurposed from reconstructing speech to *steering* an MVDR beamformer via noise SCM estimation — the training target choice (signal-domain MSA vs. mask-domain cross-entropy) is one of the explicit differences from the concurrent Heymann et al. 2016 system.

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
- [[concepts/mask-based-beamforming|Mask-Based Beamforming]] — the MSA/PSM mask-objective line repurposed for MVDR steering

## Related Sources

- [[sources/wang-2021-magnitude-phase-compensation|Wang, Wichern & Le Roux 2021: On the Compensation Between Magnitude and Phase in Speech Separation]] — PSM as the explicit-encoding motivation for the compensation view; oracle PSM-vs-IAM analysis
- [[sources/wang-2018-supervised-speech-separation-deep-learning-overview|Wang & Chen 2018: Supervised Speech Separation Based on Deep Learning: An Overview]] — surveys PSM among masking-based training targets
- [[sources/erdogan-2016-improved-mvdr-mask-prediction|Erdogan, Hershey, Watanabe, Mandel & Le Roux 2016: Improved MVDR Beamforming Using Single-Channel Mask Prediction Networks]] — the same group's MSA-trained mask network, repurposed from speech reconstruction to MVDR steering
