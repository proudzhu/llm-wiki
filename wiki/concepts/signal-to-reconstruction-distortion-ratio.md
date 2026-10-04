---
type: concept
created: 2026-10-04
updated: 2026-10-04
sources:
  - raw/papers/yamaoka-2021-bin-wise-beamformer-combination/full-text.md
tags:
  - evaluation-metric
  - speech-enhancement
  - distortionless
  - beamforming
---

# Signal-to-Reconstruction Distortion Ratio (SRDR)

The **signal-to-reconstruction distortion ratio (SRDR)**, defined by [[sources/yamaoka-2021-bin-wise-beamformer-combination|Yamaoka et al. 2021]], quantifies how much an enhancement algorithm *itself* distorts the target signal — as opposed to distortion caused by residual interference:

$$
\mathrm{SRDR} = 10 \log_{10} \frac{\|s\|^2}{\|\check{s} - s\|^2},
$$

where $s$ is the reference (the interference-free reverberant source image at the reference microphone) and $\check{s}$ is the enhanced output. SRDR → ∞ as the output matches the reference.

## Distinction from SDR

In the standard SDR/SIR/SAR decomposition (Vincent et al. 2006), "distortion" aggregates interference, noise, and artifacts. SRDR instead isolates **algorithmic distortion**: it evaluates the enhancement operator $G$ applied to the *noise-free* observation, testing the *distortionless property* ($s = G[\boldsymbol{a}s; \theta, \boldsymbol{a}]$) directly. It is closely related to the speech-distortion index (SD), but unlike SD it does not vary with the input SNR. Target cancellation by a beamformer is not captured by SRDR (it manifests as SDR loss instead).

## Use

[[sources/yamaoka-2021-bin-wise-beamformer-combination|Yamaoka et al. 2021]] use SRDR to verify that [[concepts/tflc-beamformer|RTFLC beamforming]] keeps the MVDR-level distortionless response while gaining noise reduction: RTFLC-N attains +17.4 dB SRDR over time-varying MWF at only −0.6 dB SDR, and stays within 2.2 dB of MVDR's SRDR while gaining 5.9 dB SDR.

## Related Concepts

- [[concepts/tflc-beamformer|TFLC Beamforming]] — the distortionless enhancement framework SRDR was defined to evaluate
- [[concepts/mvdr-beamformer|MVDR Beamformer]] — the archetypal distortionless method
- [[concepts/si-sdr|SI-SDR]] — another reference-based ratio metric (scale-invariant, separation context)

## Related Sources

- [[sources/yamaoka-2021-bin-wise-beamformer-combination|Yamaoka, Ono & Makino 2021: TF-Bin-Wise Linear Combination of Beamformers]] — defines SRDR
