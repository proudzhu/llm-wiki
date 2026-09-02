---
type: source
created: 2026-09-02
updated: 2026-09-02
sources:
  - raw/papers/braun-2015-residual-noise-control/full-text.md
  - https://doi.org/10.1109/ICASSP.2015.7177991
  - zotero://select/items/0_3986SHVW
tags:
  - speech-enhancement
  - multi-channel
  - wiener-filter
  - noise-reduction
  - array-processing
  - residual-noise-control
---

# Braun, Kowalczyk & Habets 2015: Residual Noise Control Using a Parametric Multichannel Wiener Filter

**Authors**: [[entities/sebastian-braun|Sebastian Braun]]¹, [[entities/konrad-kowalczyk|Konrad Kowalczyk]]², [[entities/emanuel-habets|Emanuel A. P. Habets]]¹

**Affiliation**: ¹International Audio Laboratories Erlangen, Erlangen, Germany; ²affiliation footnote (†/‡) not recoverable from the PDF — contemporary publications place Kowalczyk at the University of Erlangen-Nuremberg (LMS chair)

**Venue**: Proc. IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Brisbane, Australia

**Year**: 2015 | **Type**: Conference paper | **Pages**: 360–364 | **DOI**: [10.1109/ICASSP.2015.7177991](https://doi.org/10.1109/ICASSP.2015.7177991)

**Zotero**: [3986SHVW](zotero://select/items/0_3986SHVW)

## Summary

This paper derives a **generalized parametric multichannel Wiener filter (PMWF) with residual noise control**: instead of estimating the clean speech alone, the filter estimates a target signal defined as *speech plus a scaled portion* $c$ of the noise, which makes the maximum noise reduction directly controllable. The resulting filter reduces to the elegant interpolation $\mathbf{h}_Z = (1-c)\,\mathbf{h}_X + c\,\mathbf{e}_1$ between the standard PMWF and the reference microphone. Unlike spectral-gain-limiting approaches, no rank-one assumption on the desired-signal PSD matrix is needed, so the control remains valid for reverberant (higher-rank) desired signals. An adaptive choice of $c$ additionally keeps the output noise level constant in slowly time-varying noise fields.

## Problem Formulation

An array of $M$ microphones captures the STFT-domain signal model

$$\mathbf{y}(k,n) = \mathbf{x}(k,n) + \mathbf{v}(k,n), \qquad \Phi_y = \Phi_x + \Phi_v$$

where $\mathbf{x}$ is the desired speech, $\mathbf{v}$ the noise, and both are uncorrelated. The classical objective extracts the speech at the reference microphone, $X_1 = \mathbf{e}_1^T\mathbf{x}$ with $\mathbf{e}_1 = [1,0,\ldots,0]^T$.

Leaving **some residual noise** in the output is desirable: it masks the musical tones caused by PSD estimation errors and avoids perceptually unpleasant periods of complete silence. Single-channel algorithms achieve this by limiting the spectral gain to a floor $G_{\min} > 0$, but multichannel gain limiting requires decomposing the filter into a spatial filter plus a spectral gain — possible **only if $\Phi_x$ is rank-one**, which generally fails in reverberant environments (e.g., when analysis frames are shorter than the reverberation time).

The paper's redefinition: the target signal is the sum of speech and *desired* residual noise,

$$Z(k,n) = \mathbf{e}_1^T \mathbf{x}(k,n) + c(k)\,\mathbf{e}_1^T \mathbf{v}(k,n), \qquad 0 \le c(k) \le 1$$

where $c$ controls the noise reduction. The filter $\hat{Z} = \mathbf{h}^H \mathbf{y}$ minimizes the speech distortion subject to the filtered noise staying within a threshold $\sigma$ of the desired residual noise:

$$\mathbf{h}_Z = \arg\min_{\mathbf{h}} \mathrm{E}\!\left\{\left| \mathbf{e}_1^T\mathbf{x} - \mathbf{h}^H\mathbf{x} \right|^2\right\} \quad \text{s.t.} \quad \mathrm{E}\!\left\{\left| c_1^T\mathbf{v} - \mathbf{h}^H\mathbf{v} \right|^2\right\} \le \sigma$$

with $c_1 = c\,\mathbf{e}_1$. This is the [[concepts/speech-distortion-constrained-noise-reduction|speech-distortion-constrained noise reduction]] program with a modified (noise-containing) target.

## Methodology

### Derivation

Solving the constrained program via the Lagrangian multiplier $\mu$ yields the proposed filter

$$\mathbf{h}_Z(k,n) = \left(\boldsymbol{\Phi}_x + \mu \boldsymbol{\Phi}_v\right)^{-1} \left(\boldsymbol{\Phi}_x \mathbf{e}_1 + \mu \boldsymbol{\Phi}_v \mathbf{c}_1\right).$$

### Decomposition and Special Cases

With the modified input PSD $\widetilde{\Phi}_y = \Phi_x + \mu\Phi_v$, the filter decomposes into a weighted sum of two Wiener filters — one extracting speech ($\mathbf{h}_X$), one extracting noise ($\mathbf{h}_V$, complementary to $\mathbf{h}_X$) — and simplifies to

$$\mathbf{h}_Z = (1 - c)\,\mathbf{h}_X + c\,\mathbf{e}_1$$

i.e., a simple interpolation between the standard PMWF and the (unfiltered) reference microphone. Consequences:

- $c = 0$ recovers the **standard PMWF** (target = speech only).
- $\mu = 1$ gives an MWF with residual noise control similar to the binaural hearing-aid filter of Van den Bogaert et al. (2009).
- $\mu$ acts as a noise over/underestimation factor; increasing $\mu$ increases speech distortion.
- Because any speech-extraction filter $\mathbf{h}_X$ can be combined with its complementary noise extractor, the $(1-c)\mathbf{h}_X + c\mathbf{e}_1$ construction is applicable to arbitrary filters, not just the PMWF.

### Why the Standard PMWF Cannot Do This

For the standard PMWF ($c = 0$), controlling the residual noise via $\mu$ requires $\mu$ to be **linearly dependent on the input SNR** (to keep the noise reduction factor constant) and constant above the SNR where the desired limit is reached — with a closed-form $\mu(\sigma)$ available only under the rank-one assumption. Fig. 1 shows the contour analysis: a fixed $\sigma$ with a constant $\mu$ cannot bound the noise reduction, and for arbitrary-rank $\Phi_x$ no closed-form $\mu$ exists.

![[raw/papers/braun-2015-residual-noise-control/figures/9a88807e3f5523344d1c9d6a7531bac615479965b8fba32ebd58f7d69098b5d0.jpg|Noise reduction factor contours of the standard PMWF over μ and input SNR]]
*Figure 1: Noise reduction factor for a standard PMWF depending on $\mu$ and the input SNR (M = 4, 3 cm spacing, $\omega = \pi/5$). Contour lines mark equal noise reduction; the red line shows an ad-hoc $\mu$ trajectory limiting noise reduction to 20 dB. Constant noise reduction requires $\mu$ linearly dependent on SNR.*

### Selection of the Residual Noise Control Parameter

Two mechanisms for choosing $c$:

1. **Fixed (possibly frequency-dependent) $c$** — limits the maximum noise reduction to $c$; a frequency-dependent $c$ shapes the residual noise spectrally (more suppression where clarity matters, less where artifacts must be masked).
2. **Noise-adaptive $c$** — for a constant output noise power $\phi_0(k)$ at low SNRs, even under slowly time-varying noise:

$$c(k,n) = \min\left[ \sqrt{\frac{\phi_0(k)}{\mu\,\mathbf{e}_1^T \boldsymbol{\Phi}_v(k,n)\,\mathbf{e}_1}},\; 1 \right]$$

The min-limiting avoids amplifying noise that is already below the desired level; frequency-dependent $\phi_0(k)$ shapes the residual noise spectrum.

### Theoretical Performance (Rank-One Analysis)

Under the rank-one assumption $\Phi_x = \phi_X \mathbf{a}\mathbf{a}^H$ (with $\mathbf{a}$ the [[concepts/relative-transfer-function|relative transfer function]] vector), the speech distortion index and noise reduction factor of the proposed filter are

$$\nu_{\mathrm{sd}}(\mathbf{h}_Z) = (1-c)^2 \left| \frac{\mu}{\mu + \phi_X \mathbf{a}^H \Phi_v^{-1} \mathbf{a}} \right|^2, \qquad \zeta_{\mathrm{nr}}(\mathbf{h}_Z) = \frac{(\mu+\lambda)^2}{(1-c)^2 \eta_1 \lambda + \eta_1\, 2(1-c)c\,(\mu+\lambda) + c^2 (\mu+\lambda)^2}$$

with input SNR $\eta_1 = \phi_X \phi_V^{-1}$ and multichannel a priori SNR $\lambda = \phi_X \mathbf{a}^H\Phi_v^{-1}\mathbf{a}$. For $c > 0$ the speech distortion is *bounded* by $(1-c)^2$ relative to the standard PMWF. In the single-channel case ($\eta_1 = \lambda$) the noise reduction factor reduces to $(\mu+\lambda)^2/(\mu + c\lambda)^2$: at low SNR the filter asymptotically approaches its maximum noise reduction $c$, while $\mu$ shifts the curve along the SNR axis (Fig. 2).

![[raw/papers/braun-2015-residual-noise-control/figures/a4a655f8214b33daedd2b5f8548ee981d183d7adb8833ab73056dc403e5ff301.jpg|Noise reduction of the proposed PMWF vs input SNR for different c]]
*Figure 2: Noise reduction of the proposed PMWF with residual noise control depending on the input SNR (values of $c$ in dB). At low SNR the filter approaches its maximum noise reduction $c$; $\mu$ shifts the curves along the SNR axis; $c = 0$ equals the standard PMWF, for which no constant lower noise bound exists at any fixed $\mu$.*

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Sampling rate | 16 kHz |
| STFT | 512-point FFT, square-root Hann window 32 ms, hop 16 ms |
| Array | Uniform linear, M = 4, 5 cm spacing |
| Room | $5 \times 4 \times 6$ m, $T_{60} = 200$ ms (image-source method) |
| Source | Broadside direction, 2 m distance; speech = 60 s concatenation from EBU-SQAM |
| Noise types | Speech-spectrum-shaped diffuse noise, cafeteria babble, train station noise (DEMAND) |
| Input SNR | [−10, 30] dB |
| Noise PSD estimation | Multichannel SPP-based approach (Taseska & Habets 2012) — [[concepts/multi-channel-speech-presence-probability\|MC-SPP]] |
| Speech PSD estimation | $\hat{\Phi}_x = \Phi_y - \hat{\Phi}_v$ (PSD subtraction, positive semi-definiteness enforced); $\Phi_y$ via recursive averaging, 30 ms time constant |

## Results

### Objective measures

Averaged over all SNRs and noise types (Fig. 3): controlling the residual noise ($c > 0$) **increases the speech distortion index (SDI) and signal-to-artifact ratio (SAR)** quality, traded against a slightly smaller improvement in speech-intelligibility-weighted segmental SNR ($\mathrm{SNR}_{\mathrm{SI}}$). Artifacts caused by PSD estimation errors (musical tones) are clearly reduced. Decreasing $\mu$ also mitigates distortion and musical tones, but at a much lower SNR improvement.

![[raw/papers/braun-2015-residual-noise-control/figures/ec05cdeaa51b3d821ba50f3a92004c7e6f88db0100beb65af9ed553e2e89e451.jpg|Objective measures for the proposed filter]]
*Figure 3: Objective measures (SDI, SAR, SNR_SI) for the proposed filter, averaged over noise types and SNRs. Residual noise control (c > 0) improves SDI and SAR at a slight cost in SNR_SI.*

### Constant output noise power

With slowly time-varying white Gaussian noise (Fig. 4, $\mu = 1$ throughout):

- Uncontrolled ($c = 0$): output noise follows the standard MWF behavior.
- Constant $c = -10$ dB: the output tracks the input noise at a constant 10 dB lower level — **constant noise reduction**.
- Adaptive $c$ via the $\phi_0$-based rule with $\phi_0 = -40$ dB: the output noise power stays **constant at the desired level** independent of the time-varying input power, provided the noise PSD is tracked sufficiently fast (possible with SPP-based estimators for slowly time-varying noise).

![[raw/papers/braun-2015-residual-noise-control/figures/cbbfabeee1207659d3f9c37c2eae8869a4bb1e0323324f34460ef951a929ce1d.jpg|Power of time-varying noise at the filter input and output]]
*Figure 4: Power of time-varying noise at the filter input (black) and output. Green: constant $c = -10$ dB yields constant 10 dB noise reduction. Red: adaptive $c$ (8) with $\phi_0 = -40$ dB yields constant output noise power.*

## Key Contributions

1. **Generalized PMWF with residual noise control**: redefines the target as speech plus $c\,\times$ noise, deriving the MMSE-optimal filter $\mathbf{h}_Z = (\Phi_x + \mu\Phi_v)^{-1}(\Phi_x\mathbf{e}_1 + \mu\Phi_v\mathbf{c}_1)$ that enables *direct* control of the maximum noise reduction without a spectral-gain-limiting step.
2. **Rank-one-free control**: valid for desired signals of arbitrary rank — unlike gain-limited decompositions, which break down in reverberant environments — while the standard PMWF (with its SNR-dependent $\mu$ closed forms) is recovered exactly at $c = 0$.
3. **Interpolation insight**: $\mathbf{h}_Z = (1-c)\,\mathbf{h}_X + c\,\mathbf{e}_1$ — the controlled filter is a weighted sum of any speech-extraction filter and the reference microphone, generalizable beyond the PMWF.
4. **Two parameter-selection mechanisms**: fixed/frequency-dependent $c$ (bounded suppression + spectral shaping of residual noise) and noise-adaptive $c$ for a constant output noise power in slowly time-varying noise fields.
5. **Analytical characterization**: closed-form speech distortion index and noise reduction factor under the rank-one assumption, showing $c$ bounds the distortion and caps the maximum noise reduction.

## Related Concepts

- [[concepts/parametric-multi-channel-wiener-filter|Parametric Multi-Channel Wiener Filter (PMWF)]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/speech-distortion-constrained-noise-reduction|Speech-Distortion-Constrained Noise Reduction]]
- [[concepts/noise-attenuation-control|Noise Attenuation Control]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/multi-channel-speech-presence-probability|Multi-Channel Speech Presence Probability (MC-SPP)]]

## Related Sources

- [[sources/shetu-2026-munet|Shetu et al. 2026: μNet]] — adapts the residual-noise-control idea as the single-channel NAL post-processing knob on a DNN speech enhancer
- [[sources/bagheri-2019-pmwf-spp|Bagheri & Giacobello 2019: Exploiting MC-SPP in PMWF]] — the other main extension of the PMWF line: SPP-controlled trade-off parameter
- [[sources/yan-2014-dual-mic-bt-noise-reduction|Yan, Qiu & Lu 2014]] — uses the speech-distortion-constrained framework that this paper generalizes with a noise-containing target

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[synthesis/deep-speech-enhancement|Deep Speech Enhancement]]
