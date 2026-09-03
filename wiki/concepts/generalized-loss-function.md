---
type: concept
created: 2026-09-03
updated: 2026-09-03
sources:
  - raw/papers/li-2020-residual-noise-control/full-text.md
tags:
  - loss-function
  - deep-learning
  - speech-enhancement
  - residual-noise-control
  - noise-shaping
---

# Generalized Loss Function

The **generalized loss function (GL)** is a family of training objectives for supervised (DNN-based) speech enhancement, introduced by [[entities/andong-li|Andong Li]] et al. ([[sources/li-2020-residual-noise-control|Li et al. 2020]]), that makes the trade-off between speech distortion and residual noise explicit and controllable *inside the loss*. Whereas standard losses (MSE, TMSE, SI-SDR) implicitly drive residual noise toward zero at noise-only segments — producing unnatural-sounding suppression artifacts — the GL drives the residual noise toward a **preset level** $\beta$, transplanting classical noise shaping ideas into deep-learning training.

## Key Formulations

### The Loss Family

The GL is derived by (i) writing the speech-distortion and residual-noise errors separately, (ii) promoting the subband criterion to a fullband training loss, and (iii) generalizing the square error to exponents $\gamma \ge 0$ (error norm) and $\alpha$ (spectral exponent):

$$\mathcal{J}_x^{\gamma,\alpha} = \mathcal{J}_s^{\gamma,\alpha} + \mu\, \mathcal{J}_d^{\gamma,\alpha,\mathrm{con}}$$

For the magnitude-domain instantiation ($f=|a|$, $g=|ac|$, $h=|bc|$, $\bar\lambda = \beta|b|$):

$$\mathcal{J}_s^{\gamma,\alpha} = \sum_l \sum_k \left| (1 - M_l^\alpha(k))\, S_l^\alpha(k) \right|^\gamma \qquad \text{(speech distortion term)}$$

$$\mathcal{J}_d^{\gamma,\alpha,\mathrm{con}} = \sum_l \sum_k \left| |M_l(k) D_l(k)|^{\alpha\gamma} - |\beta_l(k) D_l(k)|^{\alpha\gamma} \right| \qquad \text{(residual noise control term)}$$

The second term penalizes the *deviation* of the filtered noise from the target residual $\beta_l(k) D_l(k)$, not the noise power itself. Since $\beta_l(k) \in [0,1]$ may be frequency- and frame-dependent, the residual noise can be shaped per T-F bin.

### Special Cases (unification)

| Setting | Reduces to |
|----------|-----------|
| $\gamma = 2$, $\alpha = 1$, $\lvert\bar\lambda\rvert \equiv 0$ | **Components loss** (Xu et al. 2019): $\mathcal{J}_s + \mu \mathcal{J}_d$ |
| $\gamma = 2$, $\alpha = 1$, control on | Constrained fullband MSE with residual noise control |
| $f = a$, $g = (a+b)c$ decomposition | **Fullband complex-spectral MSE** — $E\{J_x\} = E\{J_s\} + E\{J_d\}$, i.e. the complex MSE is itself a (weighted) combination of speech distortion and residual noise |
| Subband with known PDFs | Unsupervised MMSE estimators (Ephraim–Malah STSA / log-STSA), perceptually weighted criteria |

### Analytic Gain (subband solution)

Solving the constrained program $\min E\{J_s^{\gamma,\alpha}\}$ s.t. $E\{J_d^{\gamma,\alpha}\} = |\bar\lambda|^{\gamma}$ by Lagrange multipliers gives the generalized Wiener gain

$$M_l(k) = \left( \frac{(\xi_l(k))^{c_1}}{(\mu_l(k))^{(2c_1 c_2 - 1)} + (\xi_l(k))^{c_1}} \right)^{c_2}, \qquad c_1 = \frac{\alpha\gamma}{2\gamma-2}, \; c_2 = \frac{1}{\alpha}$$

with a priori SNR $\xi_l(k)$. This reproduces the intuitively-motivated gain family of Inoue et al. 2011, providing its missing theoretical derivation, and reduces to the parametric Wiener gain $M = \xi/(\xi + \mu)$ at $\gamma = 2, \alpha = 1$ — the supervised analogue of the [[concepts/speech-distortion-constrained-noise-reduction|speech-distortion-constrained noise reduction]] closed form.

## Parameter Map (empirical, causal U-Net on TIMIT)

| Parameter | Role | Empirical effect |
|-----------|------|------------------|
| $\beta_0$ | preset residual noise floor (e.g. −10/−20/−30 dB) | raising it *lowers* noise attenuation by design — residual noise converges toward the threshold and stays natural |
| $\mu$ | Lagrange weight ($\mu \uparrow$ = more emphasis on noise reduction) | more suppression but more speech distortion |
| $\gamma$ | error exponent | $\gamma = 2$ best objective quality; $\gamma = 1, 3$ worse NA and SA |
| $\alpha_0$ | spectral exponent (in practice constant, 1–2) | raising it lowers NA *and* SA (gains move toward 1) but degrades PESQ/SDR — extra residual noise outweighs the distortion reduction; $\alpha < 1$ causes infinite gradients |

Recommended configurations: $(\gamma, \beta_0, \mu) = (2, -30\,\mathrm{dB}, 0.5)$, $(2, -30\,\mathrm{dB}, 1)$, $(2, -20\,\mathrm{dB}, 1)$, with $\alpha_0 = 1$. Subjectively, GL at $(2, -20\,\mathrm{dB}, 1)$ is preferred over MSE/TMSE/SI-SDR-trained models by ~70% of listeners (10 listeners, AB test) — comparable objective scores but natural residual noise.

## Positioning Among Residual-Noise-Control Mechanisms

The GL is the **training-time** member of the residual-noise-control family (see [[concepts/noise-attenuation-control|Noise Attenuation Control]]):

| Mechanism | Where it acts | Representative |
|-----------|--------------|----------------|
| Filter-level (noisy target $Z = \text{speech} + c\,\text{noise}$) | classical multichannel filtering | [[sources/braun-2015-residual-noise-control|Braun et al. 2015]] PMWF |
| **Training-time (this page)** | DNN loss function | [[sources/li-2020-residual-noise-control|Li et al. 2020]] GL |
| Inference-time (residual mixing) | post-processing after DNN | [[sources/shetu-2026-munet|Shetu et al. 2026]] NAL |

## Related Concepts

- [[concepts/noise-attenuation-control|Noise Attenuation Control]]
- [[concepts/speech-distortion-constrained-noise-reduction|Speech-Distortion-Constrained Noise Reduction]]
- [[concepts/frequency-domain-loss|Frequency-Domain Loss]]
- [[concepts/power-law-compression|Power-Law Compression]]
- [[concepts/parametric-multi-channel-wiener-filter|Parametric Multi-Channel Wiener Filter (PMWF)]]
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/li-2020-residual-noise-control|Li, Peng, Zheng & Li 2020: A Supervised Speech Enhancement Approach with Residual Noise Control]] — introduces the family
- [[sources/braun-2015-residual-noise-control|Braun, Kowalczyk & Habets 2015: Residual Noise Control PMWF]] — the filter-level mechanism the GL transplants into training
- [[sources/zheng-2023-survey-frequency-domain-speech-enhancement|Zheng et al. 2023: Sixty Years of Frequency-Domain Monaural Speech Enhancement]] — surveys the T-F-domain loss landscape the GL generalizes
