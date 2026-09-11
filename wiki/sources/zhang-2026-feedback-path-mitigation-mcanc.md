---
type: source
created: 2026-09-11
updated: 2026-09-11
sources:
  - raw/papers/zhang-2026-feedback-path-mitigation-mcanc/full-text.md
  - https://cmsworkshops.com/eusipco2026/papers/accepted_papers.php
  - zotero://select/items/0_LVZPGG2Q
tags:
  - active-noise-control
  - feedforward-anc
  - multichannel-anc
  - acoustic-feedback
  - feedback-path-modeling
  - relative-transfer-matrix
  - covariance-subtraction
  - spatial-covariance-matrix
---

# Zhang, Abhayapala, Samarasinghe & Bastine 2026: Acoustic Feedback Path Mitigation for Multichannel ANC

**Authors**: [[entities/yile-angela-zhang|Yile (Angela) Zhang]], [[entities/thushara-d-abhayapala|Thushara D. Abhayapala]], [[entities/prasanga-n-samarasinghe|Prasanga N. Samarasinghe]], [[entities/amy-bastine|Amy Bastine]]
**Affiliation**: Audio & Acoustic Signal Processing Group, The Australian National University, Canberra, Australia

**Published**: EUSIPCO 2026 (31 Aug – 4 Sep 2026, Bruges, Belgium) — 5 pages, paper ID 2140
**DOI**: not yet assigned (accepted-papers stage)
**URL**: [EUSIPCO 2026 accepted papers](https://cmsworkshops.com/eusipco2026/papers/accepted_papers.php)
**📎 Zotero**: [zotero://select/items/0_LVZPGG2Q](zotero://select/items/0_LVZPGG2Q)

> **Citation-metadata note**: the Zotero record lists only three creators (Abhayapala, Samarasinghe, Bastine) and no date/venue. The PDF title page is authoritative: **Yile (Angela) Zhang** is the first author, and the venue is EUSIPCO 2026 per the conference accepted-papers list. This page follows the PDF.

## Summary

Acoustic feedback from secondary loudspeakers back to the reference microphones is the classical stability limiter of multichannel feedforward ANC, and conventional [[concepts/online-feedback-path-modeling|feedback-path modeling]] (FBPM) is normally done offline by probing the loudspeakers while the primary noise is silenced. This paper removes the "silence the primary noise" requirement: microphones are split into a **reference group** used by the ANC controller and an additional **feedback group** used to observe loudspeaker leakage, and a [[concepts/relative-transfer-matrix|Relative Transfer Matrix]] (ReTM) is estimated as the spatial mapping between the two groups. The ReTM for the *secondary-loudspeaker-only* field is isolated by **[[concepts/covariance-subtraction|covariance subtraction]]** — two measurement stages (primary-only with loudspeakers disabled, then total with probing enabled and primary still present) whose covariance difference cancels the primary-noise contribution. Because the ReTM depends only on the acoustic transfer structure $(S_{\mathrm{ref}}, S_{\mathrm{fb}})$ and not on the emitted signal or the primary noise, the estimated matrix is then used to subtract the loudspeaker leakage from the reference signals ahead of a conventional multichannel normalized frequency-domain FxLMS controller. In image-source simulations with two washer–dryer noise recordings, the proposed method stays stable across every tested step size and loudspeaker spacing, lands within **0.4–2.8 dB** of an ideal secondary-only upper bound, and stays robust when the primary source is displaced and the noise recording is swapped mid-run — whereas the no-mitigation baseline diverges and a naive "total-field ReTM" baseline collapses to ≈ −2 dB.

## Problem Formulation

The setup (Fig. 1) is a room ANC system with $J$ primary sources, $L$ secondary loudspeakers, $R$ error microphones, plus the two microphone groups being introduced here: a reference group of $J_{\mathrm{R}}$ microphones (feeding the ANC controller) and an additional feedback group of $J_{\mathrm{F}}$ microphones.

![[raw/papers/zhang-2026-feedback-path-mitigation-mcanc/figures/8d3d0a0a5c310e2109396c9420d3f761189408b6c3393b654fac3a3c66e2a5cc.jpg|Figure 1: Problem setup — secondary outputs leak to the reference microphones and must be mitigated.]]
*Figure 1: Problem setup — secondary outputs leak to the reference microphones, forming the acoustic feedback paths that must be mitigated.*

All signals are in the STFT domain with frequency bin $f$ and time frame $t$; $\mathbf{x}(f,t)$ ($J\times1$) are the emitted primary noise signals, $\mathbf{y}(f,t)$ ($L\times1$) the secondary loudspeaker signals, and $\mathbf{e}(f,t)$ ($R\times1$) the error microphone signals. Denoting the primary-noise contribution at the microphone groups as $\mathbf{P}$ and the secondary (feedback) contribution as $\mathbf{F}$, the group signals are

$$
\mathbf{M}_{\mathrm{R}}(f,t) = \mathbf{P}_{\mathrm{R}}(f,t) + \mathbf{F}_{\mathrm{R}}(f,t), \tag{1}
$$

$$
\mathbf{M}_{\mathrm{F}}(f,t) = \mathbf{P}_{\mathrm{F}}(f,t) + \mathbf{F}_{\mathrm{F}}(f,t). \tag{2}
$$

The FxLMS weight update depends on the reference signal $\mathbf{M}_{\mathrm{R}}$, which is contaminated by the loudspeaker leakage $\mathbf{F}_{\mathrm{R}}$. **The objective** is to use the extra information in $\mathbf{M}_{\mathrm{F}}$, *in the presence of persistent primary noise*, to neutralize the feedback component in $\mathbf{M}_{\mathrm{R}}$ before it reaches the downstream adaptive controller — without ever switching the primary noise off.

## Methodology

### Relative Transfer Matrix (ReTM)

The ReTM $\mathbf{R}_{\mathrm{RF}} \in \mathbb{C}^{J_{\mathrm{R}} \times J_{\mathrm{F}}}$ is defined as the spatial mapping from the feedback group to the reference group,

$$
\mathbf{M}_{\mathrm{R}} = \mathbf{R}_{\mathrm{RF}}\, \mathbf{M}_{\mathrm{F}}. \tag{3}
$$

For feedback neutralization only the **secondary-loudspeaker-only** field matters. With $\mathbf{F}_{\mathrm{R}} = \mathbf{S}_{\mathrm{ref}}\mathbf{y}$ and $\mathbf{F}_{\mathrm{F}} = \mathbf{S}_{\mathrm{fb}}\mathbf{y}$ (Eq. 4), where $\mathbf{S}_{\mathrm{ref}} \in \mathbb{C}^{J_{\mathrm{R}} \times L}$ and $\mathbf{S}_{\mathrm{fb}} \in \mathbb{C}^{J_{\mathrm{F}} \times L}$, the secondary-field ReTM is

$$
\mathbf{R}_{\mathrm{RF}}^{(\mathrm{Sec})} \triangleq \mathbf{S}_{\mathrm{ref}}\, \mathbf{S}_{\mathrm{fb}}^{\dagger}, \tag{5}
$$

with $(\cdot)^{\dagger}$ the pseudo-inverse. The key structural property is that $\mathbf{R}_{\mathrm{RF}}^{(\mathrm{Sec})}$ **depends only on the acoustic transfer structure $(\mathbf{S}_{\mathrm{ref}}, \mathbf{S}_{\mathrm{fb}})$** — not on the emitted signal $\mathbf{y}$ and not on the primary noise characteristics.

In the idealized case where the primary noise *can* be silenced, $\mathbf{R}_{\mathrm{RF}}^{(\mathrm{Sec})}$ follows from secondary-only probe measurements via $\mathbf{M}_{\mathrm{R}}^{(\mathrm{Sec})} = \mathbf{R}_{\mathrm{RF}}^{(\mathrm{Sec})}\mathbf{M}_{\mathrm{F}}^{(\mathrm{Sec})}$ (Eq. 6) and the covariance estimate

$$
\mathbf{R}_{\mathrm{RF}}^{(\mathrm{Sec})} \approx \boldsymbol{\Phi}_{\mathrm{RR}}^{(\mathrm{Sec})}\, \boldsymbol{\Phi}_{\mathrm{FR}}^{(\mathrm{Sec})^{\dagger}}, \qquad
\boldsymbol{\Phi}_{\mathrm{RR}}^{(\mathrm{Sec})} = \mathbb{E}\{\mathbf{M}_{\mathrm{R}}^{(\mathrm{Sec})}\mathbf{M}_{\mathrm{R}}^{(\mathrm{Sec})^H}\},\quad
\boldsymbol{\Phi}_{\mathrm{FR}}^{(\mathrm{Sec})} = \mathbb{E}\{\mathbf{M}_{\mathrm{F}}^{(\mathrm{Sec})}\mathbf{M}_{\mathrm{R}}^{(\mathrm{Sec})^H}\}, \tag{7,8}
$$

where $\mathbb{E}\{\cdot\}$ is approximated by averaging across time frames. This is the **oracle "Sec-only" baseline** used later in the experiments.

### Covariance subtraction (the enabling trick)

The paper's central estimator replaces the infeasible "silence the primary noise" step with two *both-noisy* measurement stages, exploiting **covariance additivity for mutually independent source components**:

1. **Primary-only stage** — secondary loudspeakers disabled, primary noise running:

$$
\boldsymbol{\Phi}_{\mathrm{RR}}^{(\mathrm{Pri})} = \sum_{j=1}^{J}\boldsymbol{\Phi}_{\mathrm{RR}}^{(j)}, \qquad
\boldsymbol{\Phi}_{\mathrm{FR}}^{(\mathrm{Pri})} = \sum_{j=1}^{J}\boldsymbol{\Phi}_{\mathrm{FR}}^{(j)}. \tag{9}
$$

2. **Total stage** — loudspeakers emit mutually independent probing signals *while the primary noise continues*:

$$
\boldsymbol{\Phi}_{\mathrm{RR}}^{(\mathrm{Tot})} = \sum_{j=1}^{J}\boldsymbol{\Phi}_{\mathrm{RR}}^{(j)} + \sum_{l=1}^{L}\boldsymbol{\Phi}_{\mathrm{RR}}^{(l)}, \qquad
\boldsymbol{\Phi}_{\mathrm{FR}}^{(\mathrm{Tot})} = \sum_{j=1}^{J}\boldsymbol{\Phi}_{\mathrm{FR}}^{(j)} + \sum_{l=1}^{L}\boldsymbol{\Phi}_{\mathrm{FR}}^{(l)}. \tag{10,11}
$$

Subtracting the two isolates the secondary-only covariance contributions — and hence the ReTM:

$$
\boldsymbol{\Phi}_{\mathrm{RR}}^{(\mathrm{Sec})} = \boldsymbol{\Phi}_{\mathrm{RR}}^{(\mathrm{Tot})} - \boldsymbol{\Phi}_{\mathrm{RR}}^{(\mathrm{Pri})}, \qquad
\boldsymbol{\Phi}_{\mathrm{FR}}^{(\mathrm{Sec})} = \boldsymbol{\Phi}_{\mathrm{FR}}^{(\mathrm{Tot})} - \boldsymbol{\Phi}_{\mathrm{FR}}^{(\mathrm{Pri})}, \tag{12,13}
$$

$$
\mathbf{R}_{\mathrm{RF}}^{(\mathrm{Sec})} \approx \left(\boldsymbol{\Phi}_{\mathrm{RR}}^{(\mathrm{Tot})} - \boldsymbol{\Phi}_{\mathrm{RR}}^{(\mathrm{Pri})}\right)\left(\boldsymbol{\Phi}_{\mathrm{FR}}^{(\mathrm{Tot})} - \boldsymbol{\Phi}_{\mathrm{FR}}^{(\mathrm{Pri})}\right)^{\dagger}. \tag{14}
$$

Because the primary-noise term cancels identically in the covariance difference, the estimate is **unbiased by persistent primary noise** — which is exactly what defeats naive FBPM. Note the requirement that the primary and secondary components be **mutually independent**, so that their covariance contributions add; the probing signals are therefore chosen mutually independent across loudspeakers.

### Feedback subtraction and the ANC controller

During ANC operation the ReTM removes the loudspeaker leakage from the reference signal (Fig. 2):

![[raw/papers/zhang-2026-feedback-path-mitigation-mcanc/figures/b5653fdde31a76c7fb2289f33d26f49976d61eb1c22ce54cdd672981d01308bf.jpg|Figure 2: Proposed ANC system with feedback subtraction using the ReTM.]]
*Figure 2: Proposed ANC system with feedback subtraction using the ReTM.*

$$
\begin{aligned}
\mathbf{M}_{\mathrm{R}}^{(\mathrm{filt})} &= \mathbf{M}_{\mathrm{R}} - \mathbf{R}_{\mathrm{RF}}^{(\mathrm{Sec})}\mathbf{M}_{\mathrm{F}}
= (\mathbf{P}_{\mathrm{R}} + \mathbf{F}_{\mathrm{R}}) - \mathbf{R}_{\mathrm{RF}}^{(\mathrm{Sec})}(\mathbf{P}_{\mathrm{F}} + \mathbf{F}_{\mathrm{F}})\\
&= \mathbf{P}_{\mathrm{R}} + \underbrace{\left(\mathbf{S}_{\mathrm{ref}}\mathbf{y} - \mathbf{R}_{\mathrm{RF}}^{(\mathrm{Sec})}\mathbf{S}_{\mathrm{fb}}\mathbf{y}\right)}_{\approx 0} - \mathbf{R}_{\mathrm{RF}}^{(\mathrm{Sec})}\mathbf{P}_{\mathrm{F}}
\approx \mathbf{P}_{\mathrm{R}} - \mathbf{R}_{\mathrm{RF}}^{(\mathrm{Sec})}\mathbf{P}_{\mathrm{F}}.
\end{aligned} \tag{15}
$$

The filtered reference $\mathbf{M}_{\mathrm{R}}^{(\mathrm{filt})}$ depends exclusively on primary-noise components and remains proportional to the primary source signal $\mathbf{x}$.

The controller is the **normalized frequency-domain FxLMS** of [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo & Morgan 1999]]:

$$
\mathbf{W}(f,t+1) = \mathbf{W}(f,t) + \boldsymbol{\mu}(f,t)\, \mathbf{M}_{\mathrm{R}}^{\prime *}(f,t)\, \mathbf{e}(f,t), \tag{16}
$$

$$
\boldsymbol{\mu}(f,t) = \frac{\mu}{\hat{\mathbf{P}}(f,t)}, \qquad
\hat{\mathbf{P}}(f,t) = (1-\alpha)\hat{\mathbf{P}}(f,t-1) + \alpha\left|\mathbf{M}_{\mathrm{R}}(f,t)\right|^2, \tag{17,18}
$$

where $\mathbf{M}_{\mathrm{R}}^{\prime}$ is the reference signal filtered by the secondary path, $(\cdot)^{*}$ the complex conjugate, $\mu$ the step size, and $\alpha$ the power-smoothing factor. With feedback subtraction, the update uses the filtered **feedback-subtracted** reference $\mathbf{M}_{\mathrm{R}}^{(\mathrm{filt})^\prime}$, and the power normalizer in Eq. (18) uses $\mathbf{M}_{\mathrm{R}}^{(\mathrm{filt})}$.

## Experimental Setup

| Item | Value |
|------|-------|
| **Room** | $[6, 7, 3]$ m, $T_{60} = 0.7$ s |
| **RIR generation** | Image-source method (Allen & Berkley 1979; Habets RIR generator) |
| **Primary source** | $J = 1$, at $[4.78,\ 3.6,\ 1.59]$ m |
| **Secondary loudspeakers** | $L = 2$, placed symmetrically on a circle centred at $[3.08,\ 3.6,\ 1.54]$ m, radius $r_s \in \{0.2,\ 0.3,\ 0.35\}$ m |
| **Error microphones** | $R = 2$, on a concentric circle of radius $0.3$ m in the same plane |
| **Reference / feedback groups** | $J_{\mathrm{R}} = 8$ and $J_{\mathrm{F}} = 8$, **interleaved** on a circle of radius $0.5$ m in the same plane |
| **Speed of sound** | $340$ m/s |
| **Evaluation band** | 50 – 600 Hz |
| **Noise signals** | Two washer–dryer recordings (Reddy et al., Interspeech 2019) resampled to $f_s = 8$ kHz |
| **Noise change over time** | Recording 1 used for ReTM identification and initial ANC; recording 2 introduced at $t = 120$ s |
| **Probing signal** | Mutually independent white Gaussian, scaled to **0 dB probe-to-primary-noise ratio** at the reference microphone group |
| **Measurement noise** | Independent per channel, 40 dB SNR |
| **Step sizes swept** | $\mu \in \{0.0025,\ 0.005,\ 0.01\}$ |
| **Power smoothing** | $\alpha = 0.1$ |
| **Secondary path** | Assumed known, i.e. $\hat{S}_e = S_e$ |
| **Robustness test** | Primary source displaced by $[0.05,\ -0.05,\ -0.1]$ m at $t = 60$ s; noise recording changed at $t = 120$ s ($\mu = 0.01$, $r_s = 0.3$ m) |

Performance is the average noise reduction

$$
\mathrm{NR(dB)} = 10\log_{10}\!\left(\frac{\frac{1}{R}\sum_{r=1}^{R}\|\mathbf{e}_r\|_2^2}{\frac{1}{R}\sum_{r=1}^{R}\|\mathbf{d}_r\|_2^2}\right), \tag{19}
$$

with $\mathbf{d}$ the uncontrolled primary noise at the error microphones (ANC off). Because the residual energy sits in the numerator, **more negative NR means more attenuation** — all reported values in Table I are negative.

Four variants are compared:

| Variant | Definition |
|---------|-----------|
| **Sec-only** | ReTM identified from loudspeaker-only probes with **no** primary-noise contamination (oracle upper bound). Feedback is still physically present during ANC operation. |
| **Total-ReTM** | ReTM estimated directly from the total field (Eqs. 7–8 applied to $\boldsymbol{\Phi}^{(\mathrm{Tot})}$), i.e. **without** covariance subtraction — isolates the effect of primary-noise bias. |
| **Proposed** | Covariance subtraction (Eqs. 12–14) before the pseudo-inverse. |
| **NoSub** | Plain multichannel FxLMS with no feedback mitigation at all — the divergence baseline. |

## Results

### Steady-state noise reduction (Table I)

NR (dB) after convergence on the initial washer–dryer noise. `NaN` indicates instability (divergence).

| $r_s$ (m) | Method | $\mu = 0.0025$ | $\mu = 0.005$ | $\mu = 0.01$ |
|-----------|--------|---------------|--------------|-------------|
| **0.2** | Sec-only | −13.461 | −17.110 | −18.308 |
| | Total-ReTM | −1.591 | −1.823 | −2.169 |
| | **Proposed** | **−12.128** | **−14.691** | **−15.467** |
| | NoSub | −12.150 | −14.646 | −14.989 |
| **0.3** | Sec-only | −12.150 | −14.495 | −15.351 |
| | Total-ReTM | −1.448 | −1.627 | −1.731 |
| | **Proposed** | **−11.389** | **−13.481** | **−14.285** |
| | NoSub | −10.039 | −11.321 | **NaN** |
| **0.35** | Sec-only | −10.928 | −12.415 | −12.742 |
| | Total-ReTM | −1.217 | −1.310 | −1.067 |
| | **Proposed** | **−10.480** | **−11.871** | **−12.380** |
| | NoSub | **NaN** | **NaN** | **NaN** |

**Reading of the table**:

- **Stability**: `NoSub` diverges as the source–microphone coupling strengthens — unstable at $r_s = 0.3$ m for the largest step size, and unstable at **every** step size once $r_s = 0.35$ m. The proposed method is stable in all nine configurations, consistent with acoustic feedback being the closed-loop stability limiter.
- **Bias of the naive estimator**: `Total-ReTM` sits at ≈ −1 to −2 dB everywhere — essentially no attenuation — because the total-field covariances are dominated by the (much stronger) persistent primary noise, so the pseudo-inverse returns a heavily biased mapping. This is the single clearest demonstration that covariance subtraction is not a refinement but a prerequisite.
- **Distance to the oracle**: the proposed method lands **0.4–2.8 dB** from `Sec-only`. The gap is widest at the tightest loudspeaker spacing with the largest step size ($r_s = 0.2$, $\mu = 0.01$: 2.8 dB) and narrows to under 0.6 dB at $r_s = 0.35$ m — the regime where feedback is most damaging and the naive baseline is worst.
- **Where mitigation is not yet needed**: at $r_s = 0.2$ m and small $\mu$, `Proposed` ≈ `NoSub` (−12.128 vs −12.150; −14.691 vs −14.646) — the feedback is not yet strong enough to destabilize, so the two curves coincide. The benefit appears exactly where the baseline breaks.

### Robustness to primary-noise variation (Figs. 3–4)

With $\mu = 0.01$ and $r_s = 0.3$ m, the primary source is displaced at $t = 60$ s and the washer–dryer recording is swapped at $t = 120$ s.

![[raw/papers/zhang-2026-feedback-path-mitigation-mcanc/figures/71b110aff98622e002cd019ead00e61db31162597406e22a93067de729f6000c.jpg|Figure 3: Time-domain residual error for ANC off, Proposed, Sec-only, and Total-ReTM.]]
*Figure 3: Time-domain residual signal at the error microphone for ANC off, Proposed, Sec-only, and Total-ReTM. The Sec-only curve overlaps the proposed curve and is visually indistinguishable. Vertical markers indicate scenario changes at $t = 60$ s (primary source displacement) and $t = 120$ s (washer–dryer noise change).*

![[raw/papers/zhang-2026-feedback-path-mitigation-mcanc/figures/9c15fbd16e960ac62996dc231bdb7aae30d47520d91e7e2722772ed6827a5811.jpg|Figure 4: Frequency-domain NR snapshots before the source displacement, before the noise change, and at t = 180 s.]]
*Figure 4: Frequency-domain NR snapshots computed for time before $t = 60$ s (top), $t = 120$ s (middle), and $t = 180$ s (bottom).*

- The proposed method tracks the secondary-only upper bound so closely that the two time-domain curves are **visually indistinguishable**, and it has smaller transients at both scenario changes than the total-ReTM baseline; the no-subtraction baseline is omitted from Fig. 3 because it diverges.
- In the frequency domain (Fig. 4), the proposed method beats the total-ReTM baseline over most of 50–600 Hz at **all three** time stages, with a typical separation of **6–10 dB** in the dominant frequency regions. This robustness follows directly from the structural property of Eq. (5): the ReTM is a function of the acoustic transfer geometry, so displacing the primary source or changing the primary signal does not invalidate it — only a change in the *secondary-path* geometry would.

## Key Contributions

1. **Framing multichannel feedback mitigation as a spatial mapping problem.** By splitting the microphones into a reference group and an added feedback group and estimating a [[concepts/relative-transfer-matrix|Relative Transfer Matrix]] between them, the method avoids identifying each of the $J_{\mathrm{R}} \times L$ individual feedback paths; one $J_{\mathrm{R}} \times J_{\mathrm{F}}$ matrix replaces them.
2. **A covariance-subtraction estimator that works under persistent primary noise.** Two measurement stages — primary-only (loudspeakers off) and total (loudspeakers probing, primary still on) — let the primary-noise covariance contribution cancel exactly, so the secondary-only ReTM is identified **without ever silencing the primary noise**, which is the practical blocker for conventional FBPM.
3. **Signal-independence of the estimated quantity.** Because $\mathbf{R}_{\mathrm{RF}}^{(\mathrm{Sec})} = \mathbf{S}_{\mathrm{ref}}\mathbf{S}_{\mathrm{fb}}^{\dagger}$ depends only on the acoustic transfer structure and not on the emitted or primary signals, a single identification is robust to changes in primary source location and primary noise signal — demonstrated empirically at two scenario change points.
4. **A drop-in integration point.** The subtraction is applied to the reference signal *ahead of* a standard multichannel normalized frequency-domain FxLMS controller (Eqs. 16–18), so it does not require modifying the ANC adaptation law itself.
5. **Systematic ablation.** Four variants (Sec-only / Total-ReTM / Proposed / NoSub) across three loudspeaker spacings and three step sizes isolate stability, primary-noise bias, and the oracle gap — showing that covariance subtraction is the decisive ingredient rather than an incremental improvement.

## Limitations and Caveats

- **No online tracking.** The ReTM is identified in an initial offline stage and then held fixed; the authors explicitly list extension to online tracking of time-varying feedback paths as future work. Drift in the *secondary* geometry (the only thing the ReTM depends on) is therefore uncompensated.
- **The filtered reference is not the clean primary reference.** Equation (15) yields $\mathbf{M}_{\mathrm{R}}^{(\mathrm{filt})} \approx \mathbf{P}_{\mathrm{R}} - \mathbf{R}_{\mathrm{RF}}^{(\mathrm{Sec})}\mathbf{P}_{\mathrm{F}}$, not $\mathbf{P}_{\mathrm{R}}$. The subtraction removes the loudspeaker leakage but mixes in a (filtered, negated) copy of the primary field observed by the feedback microphones — effectively altering the primary path seen by the controller. The consequences for the achieved optimum are not analysed.
- **Covariance additivity is assumed.** The derivation relies on mutual independence of the primary and secondary components (and across secondary loudspeakers). Any correlation between the probing signal and the primary noise, or non-stationarity within a covariance-averaging window, breaks the exact cancellation.
- **Hardware cost and channel conditioning.** The method adds $J_{\mathrm{F}} = 8$ microphones (16 total in the simulated array) and requires $\boldsymbol{\Phi}_{\mathrm{FR}}^{(\mathrm{Sec})}$ to be well enough conditioned for a meaningful pseudo-inverse; the paper does not report the conditioning or its sensitivity to probe level.
- **Favourable simulation assumptions.** Perfect secondary-path knowledge ($\hat{S}_e = S_e$), loudspeaker probing at 0 dB probe-to-primary ratio, 40 dB measurement SNR, and a single primary source ($J = 1$) with two loudspeakers. No measurement of the ReTM identification cost (number of frames, convergence) or of real-time complexity is given; the comparison is simulation-only.

## Related Concepts

- [[concepts/acoustic-feedback|Acoustic Feedback]] — the physical phenomenon being mitigated
- [[concepts/relative-transfer-matrix|Relative Transfer Matrix (ReTM)]] — newly created concept page; the spatial mapping estimated here
- [[concepts/covariance-subtraction|Covariance Subtraction]] — newly created concept page; the estimator that makes identification possible under persistent primary noise
- [[concepts/relative-transfer-function|Relative Transfer Function (RTF)]] — the single-source ancestor of the ReTM
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]] — the second-order statistics operated on by the estimator
- [[concepts/active-noise-control|Active Noise Control]] — parent domain
- [[concepts/feedforward-anc|Feedforward ANC]] — host architecture
- [[concepts/broad-band-feedforward-anc|Broad-Band Feedforward ANC]] — the ANC class where feedback is most damaging
- [[concepts/multi-channel-anc|Multi-Channel ANC]] — the multichannel setting that makes per-path FBPM impractical
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — the controller updated from the feedback-subtracted reference
- [[concepts/frequency-domain-anc|Frequency-Domain ANC]] — normalized frequency-domain FxLMS formulation used here
- [[concepts/online-feedback-path-modeling|Online Feedback-Path Modeling]] — the adaptive alternative this method avoids
- [[concepts/offline-secondary-path-modeling|Offline Secondary-Path Modeling]] — comparison case where offline identification is unbiased because the excitation is uncorrelated with the primary noise
- [[concepts/secondary-path-modeling|Secondary Path Modeling]] — the sibling identification problem, assumed solved here
- [[concepts/adaptive-feedback-cancellation|Adaptive Feedback Cancellation]] — the echo-cancellation lineage of feedback subtraction
- [[concepts/image-source-method|Image Source Method]] — used to generate all primary/secondary/feedback RIRs
- [[concepts/spatially-selective-anc|Spatially Selective ANC]] — another multichannel ANC branch from the same research group

## Related Synthesis

- [[synthesis/multichannel-anc-efficiency-and-robustness|Multichannel ANC: Computational Efficiency and Spatial Robustness]] — adds the acoustic-feedback axis to that synthesis: the closed loop, not the compute budget, sets the usable step size in MIMO arrays, and the covariance-subtracted ReTM acts as a dimensionality reduction on the *feedback* model

## Related Sources

- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo & Morgan 1999: Active Noise Control — A Tutorial Review]] — supplies the normalized frequency-domain FxLMS controller (Eqs. 16–18) and the classical offline feedback-neutralization framing that this paper removes the "silence the primary noise" precondition from
- [[sources/ma-2027-robust-ffanc-online-path-modeling|Ma 2027: Robust FFANC with Simultaneous OSPM and OFBPM]] — the online-modeling counterpart: adaptively tracks FBPM/OSPM during operation using injected auxiliary noise, whereas this paper identifies a spatial ReTM once and holds it fixed
- [[sources/xiao-2023-spatially-selective-anc|Xiao 2023: Spatially Selective Active Noise Control Systems]] — uses relative impulse responses (the time-domain RTF/ReTM counterpart) as design-time constraints in a multichannel ANC system from the same group
- [[sources/zhang-2024-active-noise-control-soundfield-interpolation-pinn|Zhang et al. 2024: ANC with PINN-based Soundfield Interpolation]] — prior multichannel ANC work from the same ANU group
