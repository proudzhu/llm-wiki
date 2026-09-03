---
type: concept
created: 2026-08-31
updated: 2026-09-03
sources:
  - raw/papers/shetu-2026-munet/full-text.md
  - raw/papers/braun-2015-residual-noise-control/full-text.md
  - raw/papers/li-2020-residual-noise-control/full-text.md
  - raw/papers/ke-2021-low-complexity-artificial-noise-suppression/full-text.md
tags:
  - speech-enhancement
  - noise-suppression
  - post-processing
  - tunable-inference
---

# Noise Attenuation Control

**Noise attenuation control (NAL control)** is a post-processing mechanism for DNN-based speech enhancement that allows a configurable trade-off between noise suppression and speech quality at inference time, without retraining the model. Given an enhanced estimate $\hat{\mathbf{s}}$ and estimated residual noise $\hat{\mathbf{n}}=\mathbf{x}-\hat{\mathbf{s}}$, the adjusted output is:

$$\hat{\mathbf{s}}_{-\text{dB}}=\hat{\mathbf{s}}+\beta\,\hat{\mathbf{n}}, \qquad \beta=\sqrt{\frac{P_{\hat{s}}}{P_{\hat{n}}\cdot 10^{(\text{NAL}_{\text{dB}}/10)}}}$$

where $P_{\hat{s}}$ and $P_{\hat{n}}$ are the mean powers of the enhanced speech and residual noise, and $\text{NAL}_{\text{dB}}$ is the user-defined noise attenuation level in dB. A more negative NAL mixes *more* noise back into the output — paradoxically improving PESQ, because aggressive neural suppressors tend to distort non-harmonic speech components along with the noise.

## Origin

The concept originates with the **parametric multichannel Wiener filter with residual noise control** of [[sources/braun-2015-residual-noise-control|Braun, Kowalczyk & Habets 2015]]. They redefine the multichannel target signal as speech plus a scaled portion of the noise, $Z = \mathbf{e}_1^T\mathbf{x} + c\,\mathbf{e}_1^T\mathbf{v}$ with $0 \le c \le 1$, and derive the MMSE-optimal filter

$$\mathbf{h}_Z = \left(\boldsymbol{\Phi}_x + \mu\boldsymbol{\Phi}_v\right)^{-1}\left(\boldsymbol{\Phi}_x\mathbf{e}_1 + \mu\boldsymbol{\Phi}_v\mathbf{c}_1\right) = (1-c)\,\mathbf{h}_X + c\,\mathbf{e}_1$$

an interpolation between the standard [[concepts/parametric-multi-channel-wiener-filter|PMWF]] and the reference microphone that (i) directly caps the maximum noise reduction at $c$ (low SNR asymptote), (ii) requires no rank-one assumption on $\Phi_x$ — unlike spectral-gain flooring, which fails for reverberant/higher-rank desired signals — and (iii) bounds the speech distortion index at $(1-c)^2$ times the standard PMWF's. Two mechanisms select $c$: a fixed (optionally frequency-dependent) value for constant maximum suppression and spectral shaping of the residual noise, or a noise-adaptive rule $c = \min[\sqrt{\phi_0/(\mu\,\phi_V)}, 1]$ that keeps the *output noise power* constant in slowly time-varying noise fields.

[[sources/li-2020-residual-noise-control|Li et al. 2020]] first carried the idea into *supervised training*, five years before μNet: their [[concepts/generalized-loss-function|generalized loss function]] replaces the residual-noise penalty with a **noise-control term** $\sum_{l,k}\big||M_l(k)D_l(k)|^{\alpha\gamma} - |\beta_0 D_l(k)|^{\alpha\gamma}\big|$ that drives the filtered noise toward a preset threshold $\beta_0$ (e.g. −20 dB) instead of toward zero. With $\beta_0 = -20$ dB, listeners preferred the trained model over MSE/TMSE/SI-SDR baselines by ~70%, mainly because the residual noise retains the character of the background noise. Unlike Braun's $c$ and Shetu's NAL, this mechanism acts at *training time* — the trade-off is baked into the weights, and changing $\beta_0$ requires retraining.

[[sources/ke-2021-low-complexity-artificial-noise-suppression|Ke et al. 2021]] — the same group — take the complementary *suppression* route: a classical MMSE noise-PSD postfilter on the DNN output drives the [[concepts/artificial-residual-noise|artificial residual noise]] (which exceeds the speech masking threshold by 10–50 dB) down toward inaudibility, using three re-designed SPP inputs for the noise tracker. Unlike NAL or Braun's $c$, it exposes no user-facing trade-off knob — its design choice is the SPP input strategy — and at 0.0098–0.016 MFLOPs/frame it is the lowest-complexity member of the residual-noise family.

[[sources/shetu-2026-munet|Shetu et al. 2026]] transplanted the idea to single-channel DNN enhancement as the user-facing NAL knob on μNet — mixing a scaled residual-noise estimate back into the enhanced output. This mirrors how classical hearing-aid noise reduction exposes a suppression-depth parameter to the fitter/user.

## Relationship to Power-Law Compression

Shetu et al. empirically show that the power-law compression factor (PF, α) and NAL act as **near-equivalent knobs** on the same speech-quality vs. suppression trade-off: increasing α improves speech quality at the cost of less noise suppression, functionally like setting a higher (less aggressive) NAL. The difference:

- **PF** requires retraining for each operating point
- **NAL** is configurable at inference time, making it suitable as a user preference setting (e.g., a "noise control" slider on a hearable)

They recommend the NAL mechanism because most listeners prefer strong noise suppression but are highly sensitive to speech distortion: for $\text{NAL}_{\text{dB}}$ up to −35 dB, speech quality improves while noise remains effectively suppressed.

## Results with μNet

On the DNS non-reverb test set (μNet trained with MSE loss, PF 0.3):

| NAL | PESQ | SI-SDR | BAK |
|-----|-----:|-------:|----:|
| default | 1.90 | 13.24 | 4.03 |
| −25 dB | 2.24 | 13.61 | 3.55 |
| −30 dB | 2.27 | 13.53 | 3.71 |

NAL −30 dB achieves the best PESQ of all models in the comparison (including GTCRN at 2.26), at some cost in BAK.

## Related Concepts

- [[concepts/munet|μNet]]
- [[concepts/power-law-compression|Power-Law Compression]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask (cRM)]]
- [[concepts/parametric-multi-channel-wiener-filter|Parametric Multi-Channel Wiener Filter (PMWF)]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/generalized-loss-function|Generalized Loss Function]]
- [[concepts/artificial-residual-noise|Artificial Residual Noise]]

## Related Sources

- [[sources/shetu-2026-munet|Shetu et al. 2026: μNet]]
- [[sources/braun-2015-residual-noise-control|Braun, Kowalczyk & Habets 2015: Residual Noise Control PMWF]]
- [[sources/li-2020-residual-noise-control|Li, Peng, Zheng & Li 2020: Supervised Speech Enhancement with Residual Noise Control]] — training-time member: residual-noise-control term in the loss
- [[sources/ke-2021-low-complexity-artificial-noise-suppression|Ke, Li, Zheng, Peng & Li 2021: Low-Complexity Artificial Noise Suppression]] — postfilter member: MMSE/SPP suppression (no trade-off knob) of artificial residual noise on DNN output
