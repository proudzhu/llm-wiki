---
type: concept
created: 2026-08-25
updated: 2026-09-02
sources:
  - raw/papers/bagheri-2019-pmwf-spp/full-text.md
  - raw/papers/braun-2015-residual-noise-control/full-text.md
tags:
  - speech-enhancement
  - wiener-filter
  - multi-channel
  - noise-reduction
---

# Parametric Multi-Channel Wiener Filter (PMWF)

The **Parametric Multi-Channel Wiener Filter (PMWF)** (Souden, Benesty & Affes, IEEE TASLP 2010) is a family of multi-channel linear filters derived from a constrained optimization: maximize the local noise reduction factor while keeping the local speech distortion index below a frequency-dependent threshold. A single time-frequency-dependent trade-off parameter $\beta(\ell,k)$ (the inverse of the Lagrange multiplier) parameterizes the continuum between the distortionless [[concepts/mvdr-beamformer|MVDR beamformer]] ($\beta = 0$) and the conventional [[concepts/multi-channel-wiener-filter|multi-channel Wiener filter]] ($\beta = 1$). Unlike classical beamforming, the formulation assumes **no array geometry**, making it suitable for distributed microphones with unknown relative geometry (e.g., wireless acoustic sensor networks, multi-device smart loudspeakers).

## Formulation

With $\mathbf{h}_i(\ell,k)$ the filter estimating the speech component at reference microphone $i$ from observation $\mathbf{y}(\ell,k)$, the PMWF is

$$\mathbf{h}_i(\ell,k) = \frac{\boldsymbol{\Phi}_{vv}^{-1} \boldsymbol{\Phi}_{yy} - \mathbf{I}_N}{\beta(\ell,k) + \mathrm{tr}\{\boldsymbol{\Phi}_{vv}^{-1} \boldsymbol{\Phi}_{yy}\} - N}\, \mathbf{u}_i$$

requiring only the input PSD matrix $\boldsymbol{\Phi}_{yy}$ and the noise PSD matrix $\boldsymbol{\Phi}_{vv}$. The multi-channel a priori SNR $\xi(\ell,k) = \mathrm{tr}\{\boldsymbol{\Phi}_{vv}^{-1}\boldsymbol{\Phi}_{yy}\} - N$ in the denominator is also the theoretical output SNR of the filter. Souden et al. (2010) unified MVDR, GSC, and PMWF in this common frequency-domain framework.

## Practical Implementation via MC-SPP (Bagheri & Giacobello 2019)

[[sources/bagheri-2019-pmwf-spp|Bagheri & Giacobello 2019]] provide a practical implementation that exploits the [[concepts/multi-channel-speech-presence-probability|MC-SPP]] at three points:

1. **Noise PSD matrix tracking** — SPP-weighted recursive averaging (a multi-channel generalization of MCRA), with the *inverse* $\widehat{\boldsymbol{\Phi}}_{vv}^{-1}$ updated directly via the Woodbury/Sherman–Morrison identity since each recursion is a rank-1 correction — avoiding per-frame matrix inversions.
2. **SPP-controlled trade-off parameter** — $\beta(\ell,k) = \beta_0 / (\alpha_\beta + (1-\alpha_\beta)\beta_0 \bar{p}(\ell,k))$: small $\beta$ (low distortion) when speech is present, large $\beta$ (strong noise reduction) when absent; $\alpha_\beta$ interpolates between fixed and purely SPP-driven trade-off. This outperforms the traditional fixed-$\beta$ PMWF.
3. **MMSE output estimate** — $\widehat{X}_i = \bar{p}\,\mathbf{h}_i^H\mathbf{y} + (1-\bar{p})\,G_{\min} Y_i$ blends the filtered signal with a $G_{\min}$-floored reference channel, bounding suppression during speech absence and mitigating SPP estimation errors.

Additional implementation safeguards: smoothing the SPP with clamping to $[p_{\min}, p_{\max}]$; falling back to $\widehat{\boldsymbol{\Phi}}_{vv}^{-1} = \widehat{\boldsymbol{\Phi}}_{yy}^{-1}$ when estimated $\gamma$ or $\xi$ go negative; and a short noise-only initialization period ($L \geq N$ frames) for consistent convergence.

## Residual Noise Control Extension (Braun, Kowalczyk & Habets 2015)

[[sources/braun-2015-residual-noise-control|Braun, Kowalczyk & Habets 2015]] generalize the PMWF by redefining the target as *speech plus a fraction $c$ of the noise*, $Z = \mathbf{e}_1^T\mathbf{x} + c\,\mathbf{e}_1^T\mathbf{v}$ ($0 \le c \le 1$), and solving the speech-distortion-constrained program (minimize speech distortion subject to the filtered noise staying near the desired residual level). The Lagrangian solution is

$$\mathbf{h}_Z = \left(\Phi_x + \mu\Phi_v\right)^{-1}\left(\Phi_x\mathbf{e}_1 + \mu\Phi_v\mathbf{c}_1\right) = (1-c)\,\mathbf{h}_X + c\,\mathbf{e}_1$$

where $c = 0$ recovers the standard PMWF and $\mu = 1$ an MWF similar to binaural hearing-aid filters. The $c$ axis is *orthogonal* to the $\mu$/$\beta$ distortion-vs-suppression trade-off: $c$ directly caps the **maximum** noise reduction (asymptote at low SNR) and bounds the speech distortion index at $(1-c)^2$, while $\mu$ only over/underestimates the noise (shifting the noise-reduction curve along the SNR axis). Crucially, this control works **without the rank-one assumption** on $\Phi_x$: gain-limited decomposition into spatial filter + spectral gain is unnecessary, so the bound holds for reverberant (higher-rank) desired signals — where the standard PMWF has no closed-form $\mu(\sigma)$ and would need iterative/adaptive multiplier computation. The single-channel DNN descendant of this mechanism is [[concepts/noise-attenuation-control|Noise Attenuation Control]].

## Empirical Positioning

On a 4-mic circular array (TIMIT speech, babble/pink NOISEX-92 interference, $T_{60} = 300$ ms, input SINR −5 to 15 dB): MCWF beats MVDR on all metrics except speech distortion; the SPP-controlled PMWF improves ΔSINR, ΔSegSNR, and noise reduction over MCWF at nearly unchanged distortion; adding the MMSE output gives the best overall performance (gains largest for pink noise) at a marginal distortion increase. Gains over MCWF shrink as input SINR grows.

## Relation to Other Frameworks

- The PMWF generalizes the SDW-MWF variant on the [[concepts/multi-channel-wiener-filter|MWF]] page: both expose a distortion/noise-reduction trade-off parameter, but the PMWF derivation starts from the noise-reduction-maximization/distortion-constraint program rather than a weighted MSE.
- In the [[concepts/informed-spatial-filter|informed spatial filter]] framework (Taseska & Habets 2018), the SPP similarly serves as the PMWF trade-off parameter for blind speech extraction.
- As a special case of the [[concepts/variable-span-linear-filter|Variable Span Linear Filter]] family, the MVDR and MWF endpoints correspond to $\mu = 0$ and $\mu = 1$.

## Related Concepts

- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/multi-channel-speech-presence-probability|Multi-Channel Speech Presence Probability (MC-SPP)]]
- [[concepts/multichannel-mcra|Multichannel MCRA]]
- [[concepts/informed-spatial-filter|Informed Spatial Filter (ISF)]]
- [[concepts/variable-span-linear-filter|Variable Span Linear Filter]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/noise-attenuation-control|Noise Attenuation Control]]

## Related Sources

- [[sources/bagheri-2019-pmwf-spp|Bagheri & Giacobello 2019: Exploiting MC-SPP in Parametric Multi-Channel Wiener Filter]]
- [[sources/braun-2015-residual-noise-control|Braun, Kowalczyk & Habets 2015: Residual Noise Control PMWF]]
- [[sources/taseska-2018-informed-spatial-filters|Taseska 2018: Informed Spatial Filters for Speech Enhancement]]
