---
type: source
created: 2026-08-27
updated: 2026-08-27
sources:
  - raw/papers/guldenschuh-2014-secondary-path-irregularities/full-text.md
  - https://doi.org/10.1109/TASLP.2014.2321475
  - zotero://select/items/0_U78ASKLL
tags:
  - active-noise-control
  - feedback-anc
  - secondary-path
  - robust-stability
  - adaptive-filtering
  - headphones
---

# Guldenschuh & de Callafon 2014: Detection of Secondary-Path Irregularities in ANC Headphones

**Authors**: [[entities/markus-guldenschuh|Markus Guldenschuh]], [[entities/raymond-de-callafon|Raymond de Callafon]]

**Institutions**: Institute of Electronic Music and Acoustics, Graz University of Technology / University of Music and Performing Arts Graz; Dynamic Systems and Control Group, University of California, San Diego

**Venue**: IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 22, no. 7

**Year**: 2014 | **Type**: Journal Article | **DOI**: [10.1109/TASLP.2014.2321475](https://doi.org/10.1109/TASLP.2014.2321475)

**Zotero**: [U78ASKLL](zotero://select/items/0_U78ASKLL)

## Summary

Adaptive feedback ANC headphones (IMC structure with FxLMS adaptation) perform well when the secondary-path $G(j\omega)$ is well known, but $G$ changes considerably when the headphones are lifted or worn leaky. This paper shows that such changes mainly affect the **low frequencies** of $G$ (magnitude drop-off), and that the resulting low-frequency poles drive both the adaptation and the feedback loop unstable. Since the adaptive filter $W$ effectively identifies $G^{-1}$, lifting the headphones forces $W$ to boost its low-frequency (DC) gain — so a simple time-domain check of the filter's DC gain suffices to detect secondary-path irregularities. A cost-efficient algorithm (6 MACs per update) interrupts the LMS adaptation on violation and smoothly converges to a stable default filter, avoiding instabilities even under sudden path changes — without auxiliary noise injection or real-time Fourier transforms.

## Problem Formulation

The feedback ANC system uses an internal model controller (IMC): the secondary-path model $\hat{G}(j\omega)$ estimates the primary noise $x(n)$ from the error signal, allowing the control filter $W(j\omega)$ to be adapted with FxLMS. The sensitivity function is

$$
S = \frac{E}{X} = \frac{1 - W\hat{G}}{1 - W(\hat{G} - G)}
$$

When $G = \hat{G}$, the denominator is unity and $W$ converges toward $G^{-1}$ (in an $H_2$/$H_\infty$ optimal sense, since $\hat{G}$ is generally non-minimum phase). Two distinct stability problems arise when $G$ deviates from $\hat{G}$:

1. **Adaptation stability**: FxLMS convergence requires the phase deviation between $\hat{G}$ and $G$ to stay below 90°; larger phase errors cause divergence.
2. **Feedback stability**: with additive uncertainty $U(\omega) = |\hat{G}(j\omega) - G_i(j\omega)|$, the robust IMC constraint requires

$$
|W(j\omega)| < \frac{1}{U_{\max}(\omega)}
$$

Existing remedies either embed this constraint in the controller design (loss of performance, real-time FFTs needed — cf. [[concepts/constrained-fdlms|constrained FDLMS]]), or track $G$ via online secondary-path estimation, which fails under large sudden changes and requires injecting auxiliary noise into the headphones.

![[raw/papers/guldenschuh-2014-secondary-path-irregularities/figures/61860049d222465bba7c2ea7c9f7c2bcad49a88aafebcfb478dd5d4c48269751.jpg|Feedback ANC with internal model controller]]
*Figure 1: Feedback ANC with an internal model controller. The internal model $\hat{G}$ of the secondary-path provides the noise estimate $\hat{x}(n)$ and filters the LMS adaptation input.*

## Methodology

### Step 1: Characterize secondary-path variability

Measurements on a dummy head with prototype headphones under four conditions — tight (nominal), one leak, two leaks, and completely loose — show that increased leakage primarily causes a **low-frequency magnitude drop-off** of $G$.

![[raw/papers/guldenschuh-2014-secondary-path-irregularities/figures/7fcbdf0b615a3499776bf473ce6791de09bb59db7477c73b1e5c623fbcdd2516.jpg|Magnitude response of secondary-path for tight, leaky and loose headphones]]
*Figure 3(a): Magnitude response of the secondary-path for tight, leaky and completely loose headphones — leakage causes a low-frequency drop-off.*

The additive uncertainty $U_{\max}(\omega)$ relative to the tight nominal model reaches **17.3 dB below 300 Hz** (dominated by the leaky paths) and the phase error exceeds 90° around 1300 Hz for open headphones.

![[raw/papers/guldenschuh-2014-secondary-path-irregularities/figures/7d531fb0a2f6a424e93a0b5261978b989b3f1b825081963f317c832d2919e994.jpg|Magnitude of additive uncertainty]]
![[raw/papers/guldenschuh-2014-secondary-path-irregularities/figures/d251c1cbe783b752a156ca6b8804c7252158105c679b8db792ecf61b26b9b930.jpg|Phase error of differently positioned headphones]]
*Figure 4: (a) Magnitude of the additive uncertainty and (b) phase error of differently positioned headphones vs. the nominal model of tight-fitting headphones.*

### Step 2: Leaky NFxLMS for adaptation stability

The phase error >90° would make plain FxLMS diverge, so the normalized **leaky FxLMS** is used (leakage factor $\gamma = 0.005$, the smallest value yielding stable updates). Leakage additionally prevents excessive high-frequency filter gain that would amplify sensor noise.

### Step 3: High-shelf filter for high-frequency uncertainty

High-frequency uncertainty is inherent (small plant changes → large phase differences), and critical around 3000 Hz where $|W \cdot U_{\max}|$ exceeds unity above 1200 Hz. A high-shelf filter amplifying the error above 1200 Hz by 7 dB penalizes high-frequency filter gain, pushing the adaptive filter to roll off there.

### Step 4: DC-gain constraint for low-frequency stability

The key observation: when headphones are lifted, $|W(\hat{G} - G_1)|$ first violates unity gain **below 300 Hz**, and the adapting $W$ must amplify these low frequencies to invert the attenuated $G$. With a short filter ($L = 6$ taps at $f_s = 7350$ Hz → 1200 Hz per frequency bin), all low-frequency adaptation shows up in the **DC bin**, so the robust constraint simplifies to a time-domain sum of coefficients:

$$
\sum_l w_l < \frac{1}{U_{\max}(0)}
$$

requiring only **6 MACs per filter update** (vs. $O(N \log_2 N)$ for a full Fourier transform). On violation, the filter does not update; instead it smoothly converges over the next $M$ samples toward a stable default filter — a scaled Kronecker impulse at $-20$ dB (with $\epsilon = 2.7$ dB headroom below the $1/U_{\max}(0)$ bound) — using a normalized difference update. Afterwards the leaky NFxLMS resumes.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Headphones | Prototype ANC headphones |
| Secondary-path measurements | Dummy head (4 conditions) + 2 persons in tight/leaky/lifted positions (16 measurements, 1 s sine sweeps) |
| Sampling rate | $f_s = 7350$ Hz (1/6 of 44.1 kHz; anti-aliasing via passive attenuation) |
| Filter length | $L = 6$ taps (1200 Hz per bin) |
| Step size | $\mu = \frac{1}{2\lambda_{\max}}$ |
| Leakage factor | $\gamma = 0.005$ |
| High-shelf filter | +7 dB above 1200 Hz |
| Uncertainty threshold | $U_{\max}(0) = 17.3$ dB; default filter at $-20$ dB ($\epsilon = 2.7$ dB) |
| Excitations | Sinusoidal (50 Hz; 100–1400 Hz in 100 Hz steps), narrowband (Q = 8 peak filter), broadband white and pink noise, all shaped by 2nd-order 500 Hz low-pass emulating passive attenuation |
| Path switching | Measured secondary-paths swapped every 0.5 s (tight/leaky alternating) |
| Ringing detection (evaluation) | $E_e(n) > E_e(n-M)$, $E_e(n) > 2E_x(n)$, and error growth twice the excitation growth, over $M = 167$ samples (one 50 Hz period) |

## Results

### DC-gain as instability predictor

Across all excitation types and path-change scenarios, the DC-gain of $W$ **always exceeded the $-17.3$ dB threshold before ringing occurred** — the constraint is a robust predictor of instability (occasionally conservative, switching to the default filter while the loop would still have been stable).

![[raw/papers/guldenschuh-2014-secondary-path-irregularities/figures/fe08845cb0daba225246930b9d6222858d36a7c43143c521eabee392cd87f56d.jpg|DC-gain distribution under stable and unstable conditions]]
*Figure 11: DC-gain distribution of $W$ under stable conditions and when the feedback drives unstable. The DC-gain always exceeds $-17.3$ dB before instability occurred.*

### Comparison with existing approaches

Without any constraint, abrupt path changes every 0.5 s lead to +10 dB error amplification and complete instability within seconds. With constraints applied, the paper compares three methods on the real-person measurement data:

| Approach | Stability | Narrowband reduction | Broadband reduction | Cost per update |
|----------|-----------|---------------------|---------------------|-----------------|
| **DC-gain constraint (this paper)** | Preserved | 14 dB (vs. 16 dB MMSE) | Comparable to Rafaely | **6 MACs** (one summation) |
| Rafaely & Elliott 2000 (constrained FDLMS, penalty in cost function) | Preserved | 2–5 dB better (4–6 dB avg. in 100 Hz band) | Comparable | ≥ 661 MACs (24-pt FFT ×2 + IFFT) |
| Zhang et al. 2003 (online SPM + norm constraint) | Preserved | Slightly better than this paper | **50–62% less** reduction (auxiliary noise + hard norm constraint) | Time-domain, but 3 LMS updates |

![[raw/papers/guldenschuh-2014-secondary-path-irregularities/figures/f133252202fe4b3996537d01ac5ce7d9293a4cd18db7697af0ac4b30331142f7.jpg|Residual error of unconstrained leaky FxLMS]]
*Figure 13: Residual error of the normalized leaky FxLMS without further constraints — abrupt secondary-path changes every 0.5 s cause +10 dB error and complete instability.*

![[raw/papers/guldenschuh-2014-secondary-path-irregularities/figures/62ee5920654ad4844de9561737988a60b9456ca78300c687980e955332b9b1fc.jpg|Comparison for broadband noise]]
![[raw/papers/guldenschuh-2014-secondary-path-irregularities/figures/0c2e76e78752e49ce9fc8f1fe56f1ca872c61c5a2996c7762f014e48496d57ee.jpg|Comparison for narrowband noise]]
*Figure 14: Residual error for (a) broadband noise and (b) narrowband noise around 100 Hz under abrupt path changes, with the DC constraint, Rafaely's, and Zhang's constraints applied.*

The 6-tap filter costs ~2 dB narrowband reduction vs. a 12-tap filter (which would require extending the frequency analysis to the 612 Hz bin, 60 MACs total); the authors judge the complexity saving worth the small loss. Zhang's method, proposed for feedforward ANC, is shown to extend to feedback ANC but at a clear broadband performance penalty.

## Key Contributions

1. **Low-frequency characterization of secondary-path irregularities**: lifting and leaks mainly cause a low-frequency magnitude drop-off of $G$ (uncertainty up to 17.3 dB below 300 Hz), and the resulting low-frequency poles are what drive the feedback loop unstable.
2. **Irregularity detection via the adaptive filter**: since $W$ performs system identification of $G^{-1}$, secondary-path changes manifest as low-frequency gain growth of $W$ — independent of the excitation spectrum — making the DC gain a sufficient detector.
3. **Time-domain DC-gain constraint**: a robust stability check requiring only 6 MACs per filter update (a coefficient summation), replacing full-band frequency-domain constraint checking ($\geq 661$ MACs) — no real-time FFT and no auxiliary noise injection needed.
4. **Stable default-filter fallback**: on constraint violation, smooth convergence to a scaled-impulse default filter guarantees stability even under sudden, large path changes, after which adaptation resumes.
5. **Experimental validation and comparison**: stability preserved on real-person data across all excitations, with broadband performance matching Rafaely's constrained FDLMS at ~1% of its computational cost.

## Related Concepts

- [[concepts/dc-gain-stability-constraint|DC-Gain Stability Constraint]] — the paper's core algorithm
- [[concepts/secondary-path-variability|Secondary Path Variability]] — the phenomenon of fit-dependent $G$ changes
- [[concepts/feedback-anc|Feedback ANC]] — application architecture
- [[concepts/internal-model-control|Internal Model Control]] — control structure providing the noise estimate
- [[concepts/leaky-fxlms-algorithm|Leaky FxLMS Algorithm]] — adaptation-stability ingredient
- [[concepts/secondary-path-modeling|Secondary Path Modeling]] — nominal model identification
- [[concepts/online-secondary-path-modeling|Online Secondary-Path Modeling]] — alternative strategy (Zhang et al.), rejected here
- [[concepts/uncertainty-modeling-for-anc|Uncertainty Modeling for ANC]] — additive uncertainty framework
- [[concepts/robust-stability-constraint|Robust Stability Constraint]] — general $|W| < 1/U_{\max}$ condition
- [[concepts/constrained-fdlms|Constrained FDLMS]] — Rafaely's frequency-domain penalty approach, direct comparison baseline
- [[concepts/primary-path-variability|Primary Path Variability]] — the feedforward-side analog of path variability

## Related Sources

- [[sources/rafaely-2000-constrained-fdlms|Rafaely & Elliott 2000: Constrained FDLMS]] — frequency-domain constraint baseline used in the comparison
- [[sources/akhtar-2006-vss-lms-online-spm|Akhtar 2006: VSS-LMS Online SPM]] — cited online-SPM approach
- [[sources/liebich-2018-doa-dependency-anc-headphones|Liebich 2018: DOA Dependency of ANC Headphones]] — later headphone path-variability work citing Guldenschuh's leak measurements

## Related Synthesis

- [[synthesis/feedback-anc-filter-design|Feedback ANC Filter Design]]
- [[synthesis/secondary-path-modeling-evolution|Secondary Path Modeling Evolution]]
