---
type: source
created: 2026-10-17
updated: 2026-10-17
sources:
  - raw/papers/maeda-1999-anc-simultaneous-perturbation/full-text.md
  - zotero://select/items/0_APFVMHY2
tags:
  - active-noise-control
  - secondary-path
  - adaptive-filtering
  - gradient-free-optimization
  - stochastic-approximation
---

# Maeda & Yoshida 1999: An Active Noise Control Without Estimation of Secondary-Path — ANC Using Simultaneous Perturbation

| Field | Detail |
|-------|--------|
| **Authors** | [[entities/yutaka-maeda|Yutaka Maeda]], [[entities/takao-yoshida|Takao Yoshida]] |
| **Institution** | Department of Electrical Engineering, Faculty of Engineering, Kansai University, Suita, Osaka, Japan |
| **Venue** | ACTIVE 99 — International Symposium on Active Control of Sound and Vibration, Fort Lauderdale, Florida, USA, December 2–4, 1999 |
| **Year** | 1999 |
| **Type** | Conference paper (Zotero item mistyped as journalArticle) |
| **Zotero** | [Link](zotero://select/items/0_APFVMHY2) |

## Summary

This paper proposes an ANC system in which the adaptive filter coefficients are updated by the **simultaneous perturbation** method and its **time-difference** variant — stochastic-approximation schemes that need only *values* of the objective function, never its gradient. Because the update is driven purely by the error power measured by the error microphone, **no estimation of the secondary path is required at all** (nor a filtered reference signal). A real-time duct experiment on a TMS320C30 DSP demonstrates feasibility: about 25 dB attenuation of a 200 Hz sinusoid with the simultaneous perturbation method and about 15 dB with the time-difference variant.

## Problem Formulation

The conventional [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] updates the control filter using a reference signal filtered through an estimate $\hat{S}(z)$ of the **secondary path**. This creates two practical difficulties:

1. $S(z)$ varies with temperature and other environmental conditions, so a fixed estimate goes stale;
2. On-line re-estimation of $S(z)$ is difficult and interferes with control.

The authors reframe the problem: instead of identifying $S(z)$ to reconstruct the gradient of the error surface, **measure** the gradient directly by perturbing all filter coefficients simultaneously and observing the resulting change in error power. The optimization objective is the error power over a block of $\lambda$ samples:

$$
J(\boldsymbol{w}_t) = \sum_{k=1}^{\lambda} e^2(k)
$$

where $t$ is the block number and $k$ indexes samples within the block — a finite-sample replacement for the unobservable expectation $E[e^2]$.

![[raw/papers/maeda-1999-anc-simultaneous-perturbation/figures/6f7a2abf90d737e86257af0e7b883aa322b7c9e0ba1cd8cb4a01cf84d222210f.jpg|Figure 1: Schematic diagram of the conventional ANC system (filtered-x LMS)]]

*Figure 1: Schematic diagram of the conventional ANC system.*

## Methodology

### Simultaneous Perturbation (SP)

The simultaneous perturbation method (Spall 1992; Alspector et al. 1992; Cauwenberghs 1993; Maeda's independent neural-network learning rules 1993–1997) estimates the gradient of an unknown objective $J(\boldsymbol{w}) \in \Re$, $\boldsymbol{w} \in \Re^n$, from **two function evaluations**, regardless of dimension $n$:

$$
\boldsymbol{w}_{t+1} = \boldsymbol{w}_t - \alpha \Delta \boldsymbol{w}_t
$$

$$
\Delta w_t^i = \frac{J(\boldsymbol{w}_t + c\boldsymbol{s}_t) - J(\boldsymbol{w}_t)}{c}\, s_t^i
$$

where $\boldsymbol{s}_t$ is a random sign vector with elements $\pm 1$ satisfying $E(s_t^i) = 0$ and $E(s_t^i s_t^j) = 0$ for $i \neq j$, $c$ is the perturbation magnitude, and $\alpha$ the step size. Expanding $J(\boldsymbol{w}_t + c\boldsymbol{s}_t)$ and taking expectations shows

$$
E(\Delta w_t^i) = \frac{\partial J(\boldsymbol{w}_t)}{\partial w_t^i}
$$

so the algorithm is a stochastic gradient method whose "gradient" is measured rather than computed. This contrasts with the finite-difference approach, which requires $n$ evaluations to estimate one gradient.

### Time Difference Simultaneous Perturbation (TDSP)

Maeda's time-difference variant (1996) reduces the requirement to **one measurement per iteration** by using the difference between consecutive objective values:

$$
\boldsymbol{w}_{t+1} = \boldsymbol{w}_t - \alpha \Delta \boldsymbol{w}_t + c\boldsymbol{s}_t
$$

$$
\Delta w_t^i = \begin{cases}
\Delta w_{\max} & \text{if } \frac{J(\boldsymbol{w}_t) - J(\boldsymbol{w}_{t-1})}{c\,s_{t-1}^i} > \Delta w_{\max} \\
-\Delta w_{\max} & \text{if } \frac{J(\boldsymbol{w}_t) - J(\boldsymbol{w}_{t-1})}{c\,s_{t-1}^i} < -\Delta w_{\max} \\
\frac{J(\boldsymbol{w}_t) - J(\boldsymbol{w}_{t-1})}{c\,s_{t-1}^i} & \text{otherwise}
\end{cases}
$$

The clip at $\pm\Delta w_{\max}$ bounds the per-step modification. The third term of the update re-injects the fresh random perturbation $c\boldsymbol{s}_t$ into all weights; since $E(\boldsymbol{s}_t) = 0$, the weights move only by the gradient term in expectation, and the expectation of $\Delta w_t^i$ again equals the true partial derivative.

### Application to ANC

![[raw/papers/maeda-1999-anc-simultaneous-perturbation/figures/4b3ca2fa2e800145fdde1a4611b3c06d307bd97a5bd2185356a705a7283e615d.jpg|Figure 2: Schematic diagram of ANC using the simultaneous perturbation or the time difference simultaneous perturbation]]

*Figure 2: Schematic diagram of ANC using the simultaneous perturbation or the time difference simultaneous perturbation.*

The coefficients $\boldsymbol{w}$ of the adaptive (anti-noise) FIR filter are the parameters to optimize, and the block error power $J(\boldsymbol{w}_t) = \sum_{k=1}^{\lambda} e^2(k)$ is the objective. Notably, the update procedure uses **neither the reference signal nor a secondary-path estimate** — the error microphone signal alone carries enough information, because the perturbation experiment itself reveals the local error surface geometry. Since $J$ must be evaluated at $\boldsymbol{w}_t$ and $\boldsymbol{w}_t + c\boldsymbol{s}_t$, the SP version updates the coefficients **every two block intervals**; TDSP needs only $J(\boldsymbol{w}_t)$ and the previous $J(\boldsymbol{w}_{t-1})$, so it updates **every one block interval**.

![[raw/papers/maeda-1999-anc-simultaneous-perturbation/figures/90d26b65a669b069c257775f32559cf64b48ee9b69fdae28daa091b85a677ecd.jpg|Figure 3: Block interval and sampling interval]]

*Figure 3: Block interval and sampling interval.*

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| **Plant** | Single-channel acrylic duct, 150 mm × 150 mm × 1300 mm |
| **Sensors** | Reference microphone + error microphone |
| **Primary source** | Loudspeaker at one end of the duct |
| **Secondary source** | Loudspeaker near the error microphone |
| **Controller** | TMS320C30 DSP, 32 MHz |
| **Converters** | 12-bit A/D and D/A |
| **Noise source** | 200 Hz sinusoidal wave |
| **Control filter** | 5-tap FIR adaptive filter |
| **Objective** | Block-summed squared error $J(\boldsymbol{w}) = \sum_k e^2(k)$ |

![[raw/papers/maeda-1999-anc-simultaneous-perturbation/figures/98bcc2cfe32119c4b667db9a6b7b399f5d57aa0a5326af577b6d8e3efddcbe8d.jpg|Figure 4: Block diagram of the experimental ANC system]]

*Figure 4: Block diagram of the experimental ANC system used.*

The authors stress that the 5-tap filter only serves to confirm basic feasibility; practical applications would need more taps.

## Results

### Simultaneous Perturbation

![[raw/papers/maeda-1999-anc-simultaneous-perturbation/figures/9249d22219019aeaff4221e7a4f890b42477032d164eae215787a08c3ce25732.jpg|Figure 5: Error microphone signal with and without ANC using the simultaneous perturbation method]]

*Figure 5: Error microphone signal with and without ANC using the simultaneous perturbation method.*

![[raw/papers/maeda-1999-anc-simultaneous-perturbation/figures/89d1c8ffe92c65daa72e1b79687dd3f1dd1a2af82c69cc7a321a47d3b2684974.jpg|Figure 6: Power spectra of the result using the simultaneous perturbation method]]

*Figure 6: Power spectra of the result using the simultaneous perturbation method.*

About **25 dB attenuation at 200 Hz**.

### Time Difference Simultaneous Perturbation

![[raw/papers/maeda-1999-anc-simultaneous-perturbation/figures/ec82ac75d18ad53289f5275afbe3a614278c5cd4656b5d3626d09a4532550c9d.jpg|Figure 7: Error microphone signal with and without ANC using the time difference simultaneous perturbation method]]

*Figure 7: Error microphone signal with and without ANC using the time difference simultaneous perturbation method.*

![[raw/papers/maeda-1999-anc-simultaneous-perturbation/figures/00e340f8aa3a45a2a117d9dc5d3fd43341b33a4c73716707534d11b9ce134385.jpg|Figure 8: Power spectra of the result using the time difference simultaneous perturbation method]]

*Figure 8: Power spectra of the result using the time difference simultaneous perturbation method.*

About **15 dB attenuation at 200 Hz** — weaker than the two-measurement SP variant, the price of halving the measurements per update.

## Key Contributions

1. **First application of simultaneous perturbation to ANC**: introduces a secondary-path-estimation-free ANC system in which the control filter is adapted by perturbation-based stochastic gradient descent, using only error-microphone measurements — no $\hat{S}(z)$, no filtered reference, no auxiliary noise injection.
2. **One-measurement variant**: brings the time-difference simultaneous perturbation method (one objective evaluation per iteration instead of two) into the ANC setting.
3. **Block-interval objective**: replaces the unobservable $E[e^2]$ with a block-summed squared error $J(\boldsymbol{w}) = \sum_k e^2(k)$, defining the practical evaluation cadence (two blocks per SP update, one per TDSP update).
4. **Real-time experimental validation**: implements both algorithms on a TMS320C30 DSP controlling a physical duct, achieving ~25 dB (SP) and ~15 dB (TDSP) attenuation of a 200 Hz sinusoid with a 5-tap FIR filter.
5. **Origin of a research lineage**: the acknowledged discussions with Kajikawa and Nomura (Kansai University) foreshadow the subsequent Kansai line of perturbation-based ANC — frequency-domain and variable-perturbation variants (Kajikawa & Nomura 2000–2003; Tokoro, Kajikawa & Nomura 2007) — making this paper the earliest entry in the "bypass the secondary path entirely" route.

## Related Concepts

- [[concepts/simultaneous-perturbation|Simultaneous Perturbation]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/simultaneous-equations-method|Simultaneous Equations Method]]
- [[concepts/heuristic-anc-algorithms|Heuristic ANC Algorithms]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/adaptive-filtering|Adaptive Filtering]]

## Related Synthesis

- [[synthesis/secondary-path-modeling-evolution|Secondary Path Modeling: From Offline Identification to Model-Free Evolution]]
